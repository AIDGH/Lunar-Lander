"""Finite, configuration-driven runner for deterministic DQN experiments.

This runner never chooses experiments. It executes only enabled experiments
listed in an explicitly supplied JSON plan, in plan order, and then stops.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


RUNNER_SCHEMA_VERSION = 1
PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_PLAN = PROJECT_ROOT / "experiment_plans" / "next_batch.json"
SOURCE_FILES = ("agent.py", "model.py", "train.py", "test.py", "game.py")
FINAL_HOLDOUT = (10_000, 10_099)
TIMEOUT_LENGTH = 1000
HOLDOUT_STATE_COUNT = 200
SOLVED_THRESHOLD = 200.0
LOW_SCORE_THRESHOLD = 0.0
ALGORITHM_PROVENANCE = {
    "vanilla": {
        "architecture": "standard",
        "target_strategy": "vanilla",
        "network_class": "DQN",
    },
    "double_dqn": {
        "architecture": "standard",
        "target_strategy": "double",
        "network_class": "DQN",
    },
    "dueling_dqn": {
        "architecture": "dueling",
        "target_strategy": "vanilla",
        "network_class": "DuelingDQN",
    },
    "d3qn": {
        "architecture": "dueling",
        "target_strategy": "double",
        "network_class": "DuelingDQN",
    },
    "deep_d3qn": {
        "architecture": "dueling_deep",
        "target_strategy": "double",
        "network_class": "DeepDuelingDQN",
    },
}
MAX_EXPERIMENTS = 100
MAX_ID_LENGTH = 100
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
CORE_ARTIFACT_FILENAMES = {
    "experiment_manifest.txt",
    "resolved_config.json",
    "run_status.json",
    "source_branch.txt",
    "source_commit.txt",
    "source_status.txt",
    "training.log",
    "weights.pth",
    "training_metrics.json",
    "training_plot.png",
    "combined_summary.txt",
}
PHASE_STATUS = {
    "prepared": "pending",
    "training_running": "running",
    "training_succeeded": "running",
    "benchmark_a_running": "running",
    "benchmark_a_succeeded": "running",
    "benchmark_b_running": "running",
    "benchmark_b_succeeded": "running",
    "completed": "succeeded",
    "failed": "failed",
}

CONFIG_FIELDS = {
    "algorithm",
    "training_seed",
    "episodes",
    "learning_rate",
    "target_update_freq",
    "target_update_unit",
    "epsilon_start",
    "epsilon_min",
    "epsilon_decay",
    "epsilon_decay_unit",
    "replay_capacity",
    "batch_size",
    "gamma",
}


class RunnerError(RuntimeError):
    """Raised for a safely detected runner, plan, or artifact error."""


class ResumeBlocked(RunnerError):
    """Raised when an in-place resume cannot be proven safe."""


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def timestamp_slug():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def reject_json_constant(value):
    raise ValueError(f"non-standard JSON constant is not allowed: {value}")


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_strict(path):
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(
                handle,
                parse_constant=reject_json_constant,
                object_pairs_hook=reject_duplicate_keys,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise RunnerError(f"cannot read valid JSON from {path}: {exc}") from exc


def plan_digest(plan):
    payload = json.dumps(
        plan, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_object(value, label):
    if not isinstance(value, dict):
        raise RunnerError(f"{label} must be a JSON object")
    return value


def require_keys(value, required, allowed, label):
    obj = require_object(value, label)
    missing = set(required) - set(obj)
    unknown = set(obj) - set(allowed)
    if missing:
        raise RunnerError(
            f"{label} is missing required fields: {sorted(missing)}"
        )
    if unknown:
        raise RunnerError(f"{label} has unknown fields: {sorted(unknown)}")
    return obj


def require_int(value, label, minimum=None):
    if isinstance(value, bool) or not isinstance(value, int):
        raise RunnerError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise RunnerError(f"{label} must be at least {minimum}")
    return value


def require_number(value, label, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RunnerError(f"{label} must be a finite number")
    number = float(value)
    if not math.isfinite(number):
        raise RunnerError(f"{label} must be a finite number")
    if minimum is not None and number < minimum:
        raise RunnerError(f"{label} must be at least {minimum}")
    if maximum is not None and number > maximum:
        raise RunnerError(f"{label} must be at most {maximum}")
    return number


def require_safe_id(value, label):
    if (
        not isinstance(value, str)
        or len(value) > MAX_ID_LENGTH
        or not SAFE_ID.fullmatch(value)
    ):
        raise RunnerError(
            f"{label} must be at most {MAX_ID_LENGTH} characters, match "
            f"{SAFE_ID.pattern!r}, and contain no path parts"
        )
    return value


def require_basename(value, label):
    if (
        not isinstance(value, str)
        or not value
        or Path(value).name != value
        or value in {".", ".."}
    ):
        raise RunnerError(f"{label} must be a plain filename")
    return value


def ranges_overlap(first, second):
    return max(first[0], second[0]) <= min(first[1], second[1])


def same_path(first, second):
    return os.path.normcase(str(Path(first).resolve())) == os.path.normcase(
        str(Path(second).resolve())
    )


def path_is_within(path, parent):
    try:
        return os.path.commonpath(
            [str(Path(path).resolve()), str(Path(parent).resolve())]
        ) == str(Path(parent).resolve())
    except ValueError:
        return False


def validate_configuration(config, label, validate_every, reserved_ranges):
    require_keys(config, CONFIG_FIELDS, CONFIG_FIELDS, label)
    if (
        not isinstance(config["algorithm"], str)
        or config["algorithm"] not in ALGORITHM_PROVENANCE
    ):
        raise RunnerError(
            f"{label}.algorithm must be one of "
            f"{tuple(ALGORITHM_PROVENANCE)!r}"
        )

    seed = require_int(config["training_seed"], f"{label}.training_seed", 0)
    episodes = require_int(config["episodes"], f"{label}.episodes", 1)
    if episodes < validate_every:
        raise RunnerError(
            f"{label}.episodes must be at least {validate_every}; otherwise "
            "the unchanged validation protocol cannot create weights.pth"
        )
    require_number(
        config["learning_rate"], f"{label}.learning_rate", minimum=0.0
    )
    if float(config["learning_rate"]) == 0.0:
        raise RunnerError(f"{label}.learning_rate must be positive")
    require_int(
        config["target_update_freq"],
        f"{label}.target_update_freq",
        minimum=1,
    )
    if config["target_update_unit"] != "learning_optimizer_updates":
        raise RunnerError(
            f"{label}.target_update_unit must be "
            "'learning_optimizer_updates'"
        )

    epsilon_start = require_number(
        config["epsilon_start"], f"{label}.epsilon_start", 0.0, 1.0
    )
    epsilon_min = require_number(
        config["epsilon_min"], f"{label}.epsilon_min", 0.0, 1.0
    )
    epsilon_decay = require_number(
        config["epsilon_decay"], f"{label}.epsilon_decay", 0.0, 1.0
    )
    if epsilon_min > epsilon_start:
        raise RunnerError(
            f"{label} must satisfy epsilon_min <= epsilon_start"
        )
    if epsilon_decay == 0.0:
        raise RunnerError(f"{label}.epsilon_decay must be positive")
    if config["epsilon_decay_unit"] != "episode":
        raise RunnerError(
            f"{label}.epsilon_decay_unit must be 'episode'"
        )

    replay_capacity = require_int(
        config["replay_capacity"], f"{label}.replay_capacity", 1
    )
    batch_size = require_int(
        config["batch_size"], f"{label}.batch_size", 1
    )
    if replay_capacity < batch_size:
        raise RunnerError(
            f"{label}.replay_capacity must be at least batch_size"
        )
    require_number(config["gamma"], f"{label}.gamma", 0.0, 1.0)

    training_range = (20_000 + seed, 20_000 + seed + episodes - 1)
    for name, reserved in reserved_ranges.items():
        if ranges_overlap(training_range, reserved):
            raise RunnerError(
                f"{label} training seed range {training_range} overlaps "
                f"reserved {name} range {reserved}"
            )


def validate_reference(reference, label):
    allowed = {
        "id",
        "description",
        "episodes",
        "mean_reward",
        "solved_count",
        "solved_rate_pct",
        "low_score_count",
        "low_score_rate_pct",
        "mean_length",
        "timeout_count",
    }
    require_keys(reference, allowed, allowed, label)
    require_safe_id(reference["id"], f"{label}.id")
    if not isinstance(reference["description"], str):
        raise RunnerError(f"{label}.description must be a string")
    episodes = require_int(reference["episodes"], f"{label}.episodes", 1)
    solved = require_int(
        reference["solved_count"], f"{label}.solved_count", 0
    )
    low = require_int(
        reference["low_score_count"], f"{label}.low_score_count", 0
    )
    timeouts = require_int(
        reference["timeout_count"], f"{label}.timeout_count", 0
    )
    if max(solved, low, timeouts) > episodes:
        raise RunnerError(f"{label} counts cannot exceed episodes")
    require_number(reference["mean_reward"], f"{label}.mean_reward")
    require_number(
        reference["solved_rate_pct"],
        f"{label}.solved_rate_pct",
        0.0,
        100.0,
    )
    require_number(
        reference["low_score_rate_pct"],
        f"{label}.low_score_rate_pct",
        0.0,
        100.0,
    )
    require_number(reference["mean_length"], f"{label}.mean_length", 0.0)
    if not close_number(
        reference["solved_rate_pct"],
        round(100.0 * solved / episodes, 2),
        tolerance=1e-9,
    ):
        raise RunnerError(
            f"{label}.solved_rate_pct is inconsistent with solved_count"
        )
    if not close_number(
        reference["low_score_rate_pct"],
        round(100.0 * low / episodes, 2),
        tolerance=1e-9,
    ):
        raise RunnerError(
            f"{label}.low_score_rate_pct is inconsistent with low_score_count"
        )


def validate_screening_rule(rule, label):
    allowed = {
        "id",
        "automatic_followup",
        "description",
        "combined_constraints",
        "manual_criteria",
    }
    require_keys(rule, allowed, allowed, label)
    require_safe_id(rule["id"], f"{label}.id")
    if rule["automatic_followup"] is not False:
        raise RunnerError(
            f"{label}.automatic_followup must be false; the runner never "
            "selects follow-up experiments"
        )
    if not isinstance(rule["description"], str):
        raise RunnerError(f"{label}.description must be a string")
    constraints = require_keys(
        rule["combined_constraints"],
        {
            "max_low_score_count",
            "max_timeout_count",
            "max_mean_length",
        },
        {
            "max_low_score_count",
            "max_timeout_count",
            "max_mean_length",
        },
        f"{label}.combined_constraints",
    )
    require_int(
        constraints["max_low_score_count"],
        f"{label}.combined_constraints.max_low_score_count",
        0,
    )
    require_int(
        constraints["max_timeout_count"],
        f"{label}.combined_constraints.max_timeout_count",
        0,
    )
    require_number(
        constraints["max_mean_length"],
        f"{label}.combined_constraints.max_mean_length",
        0.0,
    )
    criteria = rule["manual_criteria"]
    if (
        not isinstance(criteria, list)
        or not criteria
        or any(not isinstance(item, str) or not item for item in criteria)
    ):
        raise RunnerError(
            f"{label}.manual_criteria must be a non-empty string list"
        )


def validate_plan(plan):
    top_fields = {
        "schema_version",
        "plan_id",
        "runs_root",
        "protocol",
        "experiments",
    }
    require_keys(plan, top_fields, top_fields, "plan")
    if plan["schema_version"] != RUNNER_SCHEMA_VERSION:
        raise RunnerError(
            f"unsupported plan schema_version: {plan['schema_version']}"
        )
    require_safe_id(plan["plan_id"], "plan.plan_id")
    if not isinstance(plan["runs_root"], str) or not plan["runs_root"]:
        raise RunnerError("plan.runs_root must be a non-empty path string")

    protocol_fields = {
        "name",
        "version",
        "training_env_seed_offset",
        "training_action_space_seed_offset",
        "holdout_env_seed_offset",
        "holdout_action_space_seed_offset",
        "validation",
        "benchmarks",
        "final_holdout",
    }
    protocol = require_keys(
        plan["protocol"], protocol_fields, protocol_fields, "plan.protocol"
    )
    if protocol["name"] != "deterministic_harness":
        raise RunnerError(
            "plan.protocol.name must be 'deterministic_harness'"
        )
    if require_int(protocol["version"], "plan.protocol.version", 1) != 1:
        raise RunnerError("only deterministic_harness protocol version 1 is supported")
    expected_offsets = {
        "training_env_seed_offset": 20_000,
        "training_action_space_seed_offset": 21_000,
        "holdout_env_seed_offset": 30_000,
        "holdout_action_space_seed_offset": 40_000,
    }
    for field, expected in expected_offsets.items():
        if protocol[field] != expected:
            raise RunnerError(
                f"plan.protocol.{field} must be {expected} to match train.py"
            )

    validation_fields = {
        "validate_every",
        "episodes",
        "base_seed",
        "last_seed",
        "greedy",
        "checkpoint_metric",
        "tie_breaker",
    }
    validation = require_keys(
        protocol["validation"],
        validation_fields,
        validation_fields,
        "plan.protocol.validation",
    )
    expected_validation = {
        "validate_every": 50,
        "episodes": 10,
        "base_seed": 901,
        "last_seed": 910,
        "greedy": True,
        "checkpoint_metric": "mean_reward",
        "tie_breaker": "solved_rate",
    }
    for field, expected in expected_validation.items():
        if validation[field] != expected:
            raise RunnerError(
                f"plan.protocol.validation.{field} must be {expected!r}"
            )

    final_fields = {"base_seed", "last_seed", "reserved"}
    final_holdout = require_keys(
        protocol["final_holdout"],
        final_fields,
        final_fields,
        "plan.protocol.final_holdout",
    )
    if (
        final_holdout["base_seed"],
        final_holdout["last_seed"],
    ) != FINAL_HOLDOUT or final_holdout["reserved"] is not True:
        raise RunnerError(
            "final holdout must remain reserved at seeds 10000-10099"
        )

    benchmarks = protocol["benchmarks"]
    if not isinstance(benchmarks, list) or len(benchmarks) != 2:
        raise RunnerError("plan.protocol.benchmarks must contain A and B")
    benchmark_fields = {
        "id",
        "episodes",
        "base_seed",
        "last_seed",
        "json_filename",
        "log_filename",
        "long_streak_threshold",
    }
    expected_benchmarks = {
        "benchmark_a": (50, 1234),
        "benchmark_b": (100, 5000),
    }
    expected_benchmark_files = {
        "benchmark_a": ("benchmark_a.json", "benchmark_a.log"),
        "benchmark_b": ("benchmark_b.json", "benchmark_b.log"),
    }
    benchmark_ids = set()
    benchmark_ranges = {}
    filenames = {name.casefold() for name in CORE_ARTIFACT_FILENAMES}
    for index, benchmark in enumerate(benchmarks):
        label = f"plan.protocol.benchmarks[{index}]"
        require_keys(benchmark, benchmark_fields, benchmark_fields, label)
        benchmark_id = require_safe_id(benchmark["id"], f"{label}.id")
        if benchmark_id in benchmark_ids:
            raise RunnerError(f"duplicate benchmark id: {benchmark_id}")
        benchmark_ids.add(benchmark_id)
        if benchmark_id not in expected_benchmarks:
            raise RunnerError(f"unexpected benchmark id: {benchmark_id}")
        episodes = require_int(
            benchmark["episodes"], f"{label}.episodes", 1
        )
        base_seed = require_int(
            benchmark["base_seed"], f"{label}.base_seed", 0
        )
        if (episodes, base_seed) != expected_benchmarks[benchmark_id]:
            raise RunnerError(
                f"{benchmark_id} must use "
                f"{expected_benchmarks[benchmark_id][0]} episodes at seed "
                f"{expected_benchmarks[benchmark_id][1]}"
            )
        last_seed = base_seed + episodes - 1
        if benchmark["last_seed"] != last_seed:
            raise RunnerError(
                f"{label}.last_seed must equal base_seed + episodes - 1"
            )
        benchmark_range = (base_seed, last_seed)
        if ranges_overlap(benchmark_range, FINAL_HOLDOUT):
            raise RunnerError(
                f"{benchmark_id} overlaps final holdout {FINAL_HOLDOUT}"
            )
        benchmark_ranges[benchmark_id] = benchmark_range
        for field in ("json_filename", "log_filename"):
            filename = require_basename(
                benchmark[field], f"{label}.{field}"
            )
            folded = filename.casefold()
            if folded in filenames:
                raise RunnerError(f"duplicate artifact filename: {filename}")
            filenames.add(folded)
        actual_files = (
            benchmark["json_filename"],
            benchmark["log_filename"],
        )
        if actual_files != expected_benchmark_files[benchmark_id]:
            raise RunnerError(
                f"{benchmark_id} artifact filenames must be "
                f"{expected_benchmark_files[benchmark_id]!r}"
            )
        require_int(
            benchmark["long_streak_threshold"],
            f"{label}.long_streak_threshold",
            1,
        )
    if set(expected_benchmarks) != benchmark_ids:
        raise RunnerError("both benchmark_a and benchmark_b are required")
    if ranges_overlap(
        benchmark_ranges["benchmark_a"],
        benchmark_ranges["benchmark_b"],
    ):
        raise RunnerError("Benchmark A and Benchmark B ranges overlap")

    reserved_ranges = {
        "validation": (
            validation["base_seed"],
            validation["last_seed"],
        ),
        **benchmark_ranges,
        "final_holdout": FINAL_HOLDOUT,
    }

    experiments = plan["experiments"]
    if (
        not isinstance(experiments, list)
        or not experiments
        or len(experiments) > MAX_EXPERIMENTS
    ):
        raise RunnerError(
            f"plan.experiments must contain 1-{MAX_EXPERIMENTS} entries"
        )
    experiment_fields = {
        "id",
        "enabled",
        "purpose",
        "configuration",
        "reference",
        "screening_rule",
    }
    seen_ids = set()
    enabled_count = 0
    for index, experiment in enumerate(experiments):
        label = f"plan.experiments[{index}]"
        require_keys(
            experiment, experiment_fields, experiment_fields, label
        )
        experiment_id = require_safe_id(experiment["id"], f"{label}.id")
        folded = experiment_id.casefold()
        if folded in seen_ids:
            raise RunnerError(
                f"duplicate experiment id (case-insensitive): {experiment_id}"
            )
        seen_ids.add(folded)
        if not isinstance(experiment["enabled"], bool):
            raise RunnerError(f"{label}.enabled must be boolean")
        if experiment["enabled"]:
            enabled_count += 1
        if not isinstance(experiment["purpose"], str):
            raise RunnerError(f"{label}.purpose must be a string")
        validate_configuration(
            experiment["configuration"],
            f"{label}.configuration",
            validation["validate_every"],
            reserved_ranges,
        )
        if experiment["reference"] is not None:
            validate_reference(experiment["reference"], f"{label}.reference")
        if experiment["screening_rule"] is not None:
            validate_screening_rule(
                experiment["screening_rule"],
                f"{label}.screening_rule",
            )
        if (
            experiment["screening_rule"] is not None
            and experiment["reference"] is None
        ):
            raise RunnerError(
                f"{label} has a screening rule but no declared reference"
            )
    if enabled_count == 0:
        raise RunnerError("plan contains no enabled experiments")
    return plan


def resolve_runs_root(plan):
    configured = Path(plan["runs_root"])
    if not configured.is_absolute():
        configured = PROJECT_ROOT / configured
    runs_root = configured.resolve()
    if runs_root.parent == runs_root:
        raise RunnerError("runs_root cannot be a filesystem root")
    if same_path(runs_root, PROJECT_ROOT) or path_is_within(
        runs_root, PROJECT_ROOT
    ):
        raise RunnerError(
            "runs_root must be outside the source repository; refusing to "
            "write generated runs into source or archive directories"
        )
    archive_markers = (
        "run_status.json",
        "suite_state.json",
        "training_metrics.json",
        "weights.pth",
    )
    if any((runs_root / marker).exists() for marker in archive_markers):
        raise RunnerError(
            "runs_root appears to be an individual run or suite directory; "
            "configure its parent instead"
        )
    return runs_root


def git_read(arguments):
    command = ["git", "-C", str(PROJECT_ROOT), *arguments]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RunnerError(
            f"read-only Git command failed ({' '.join(arguments)}): {detail}"
        )
    return completed.stdout.rstrip("\r\n")


def get_clean_git_provenance():
    root = git_read(["rev-parse", "--show-toplevel"])
    if not same_path(root, PROJECT_ROOT):
        raise RunnerError(
            f"runner source root {PROJECT_ROOT} is not Git root {root}"
        )
    branch = git_read(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = git_read(["rev-parse", "HEAD"])
    status = git_read(
        ["status", "--porcelain=v1", "--untracked-files=all"]
    )
    if status:
        raise RunnerError(
            "Git working tree is not clean. Commit or otherwise resolve all "
            "changes before running or dry-running an experiment suite."
        )
    return {
        "root": str(PROJECT_ROOT),
        "branch": branch,
        "commit": commit,
        "status": status,
    }


def write_text_exclusive(path, text):
    path = Path(path)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json_exclusive(path, value):
    write_text_exclusive(
        path, json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    )


def atomic_write_text(path, text):
    path = Path(path)
    temporary = path.with_name(
        f".{path.name}.{os.getpid()}.temporary"
    )
    with temporary.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.replace(temporary, path)


def atomic_write_json(path, value):
    atomic_write_text(
        path, json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    )


def write_text_if_absent_or_same(path, text):
    path = Path(path)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing != text:
            raise RunnerError(
                f"refusing to overwrite conflicting artifact: {path}"
            )
        return
    write_text_exclusive(path, text)


def select_experiments(plan, experiment_id):
    enabled = [item for item in plan["experiments"] if item["enabled"]]
    if experiment_id is None:
        return enabled
    matches = [item for item in enabled if item["id"] == experiment_id]
    if not matches:
        raise RunnerError(
            f"enabled experiment id not found in plan: {experiment_id}"
        )
    return matches


def benchmark_by_id(protocol, benchmark_id):
    for benchmark in protocol["benchmarks"]:
        if benchmark["id"] == benchmark_id:
            return benchmark
    raise RunnerError(f"missing benchmark in validated plan: {benchmark_id}")


def resolve_experiment(experiment, protocol):
    config = dict(experiment["configuration"])
    seed = config["training_seed"]
    episodes = config["episodes"]
    return {
        "protocol": protocol["name"],
        "protocol_version": protocol["version"],
        "experiment_id": experiment["id"],
        "purpose": experiment["purpose"],
        "configuration": config,
        "reproducibility": {
            "global_seed": seed,
            "python_random_seed": seed,
            "numpy_seed": seed,
            "torch_seed": seed,
            "training_env_seed_base": (
                protocol["training_env_seed_offset"] + seed
            ),
            "training_env_seed_scheme": (
                "TRAIN_ENV_SEED_BASE + episode - 1"
            ),
            "training_env_seed_last": (
                protocol["training_env_seed_offset"] + seed + episodes - 1
            ),
            "training_action_space_seed": (
                protocol["training_action_space_seed_offset"] + seed
            ),
            "holdout_uses_separate_environment": True,
            "holdout_state_count": HOLDOUT_STATE_COUNT,
            "holdout_env_seed_base": (
                protocol["holdout_env_seed_offset"] + seed
            ),
            "holdout_env_seed_last": (
                "runtime value from training_metrics.json"
            ),
            "holdout_action_space_seed": (
                protocol["holdout_action_space_seed_offset"] + seed
            ),
        },
        "validation": dict(protocol["validation"]),
        "benchmarks": [dict(item) for item in protocol["benchmarks"]],
        "final_holdout": dict(protocol["final_holdout"]),
        "reference": experiment["reference"],
        "screening_rule": experiment["screening_rule"],
        "automatic_followup": False,
    }


def planned_artifacts():
    return {
        "manifest": "experiment_manifest.txt",
        "resolved_config": "resolved_config.json",
        "run_status": "run_status.json",
        "source_branch": "source_branch.txt",
        "source_commit": "source_commit.txt",
        "source_status": "source_status.txt",
        "source_snapshot": "source_snapshot",
        "training_log": "training.log",
        "weights": "weights.pth",
        "training_metrics": "training_metrics.json",
        "training_plot": "training_plot.png",
        "benchmark_a_log": "benchmark_a.log",
        "benchmark_a_json": "benchmark_a.json",
        "benchmark_b_log": "benchmark_b.log",
        "benchmark_b_json": "benchmark_b.json",
        "combined_summary": "combined_summary.txt",
    }


def build_manifest(resolved, provenance, source_hashes, artifacts):
    lines = [
        "Pre-execution experiment manifest",
        "=================================",
        f"Experiment ID: {resolved['experiment_id']}",
        f"Protocol: {resolved['protocol']}",
        f"Purpose: {resolved['purpose']}",
        "Automatic follow-up scheduling: disabled",
        "",
        "Git provenance:",
        f"  Branch: {provenance['branch']}",
        f"  Commit: {provenance['commit']}",
        "  Status: clean",
        "",
        "Resolved configuration:",
        json.dumps(resolved, indent=2, ensure_ascii=False),
        "",
        "Source snapshot SHA-256:",
    ]
    for filename in SOURCE_FILES:
        lines.append(f"  {filename}: {source_hashes[filename]}")
    lines.extend(
        [
            "",
            "Planned artifacts:",
            json.dumps(artifacts, indent=2, ensure_ascii=False),
            "",
            "Screening metadata is descriptive only. This runner never "
            "schedules a follow-up experiment.",
            "",
        ]
    )
    return "\n".join(lines)


def prepare_run(run_dir, experiment, protocol, provenance):
    final_run_dir = Path(run_dir)
    if final_run_dir.exists():
        raise RunnerError(
            f"refusing to overwrite existing run: {final_run_dir}"
        )
    staging_dir = final_run_dir.with_name(
        f".{final_run_dir.name}.preparing-{timestamp_slug()}"
    )
    try:
        staging_dir.mkdir(parents=False, exist_ok=False)
        snapshot_dir = staging_dir / "source_snapshot"
        snapshot_dir.mkdir(exist_ok=False)

        source_hashes = {}
        for filename in SOURCE_FILES:
            source = PROJECT_ROOT / filename
            if not source.is_file():
                raise RunnerError(
                    f"required source file is missing: {source}"
                )
            destination = snapshot_dir / filename
            shutil.copy2(source, destination)
            source_hashes[filename] = file_sha256(destination)

        artifacts = planned_artifacts()
        resolved = resolve_experiment(experiment, protocol)
        resolved["source_provenance"] = dict(provenance)
        resolved["source_snapshot_sha256"] = source_hashes
        resolved["artifact_paths"] = dict(artifacts)

        write_text_exclusive(
            staging_dir / artifacts["source_branch"],
            provenance["branch"] + "\n",
        )
        write_text_exclusive(
            staging_dir / artifacts["source_commit"],
            provenance["commit"] + "\n",
        )
        write_text_exclusive(
            staging_dir / artifacts["source_status"],
            provenance["status"],
        )
        write_json_exclusive(
            staging_dir / artifacts["resolved_config"], resolved
        )
        write_text_exclusive(
            staging_dir / artifacts["manifest"],
            build_manifest(
                resolved, provenance, source_hashes, artifacts
            ),
        )
        status = {
            "runner_schema_version": RUNNER_SCHEMA_VERSION,
            "experiment_id": experiment["id"],
            "status": "pending",
            "phase": "prepared",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "run_directory": str(final_run_dir.resolve()),
            "artifacts": artifacts,
            "result": None,
            "error": None,
            "history": [
                {
                    "at": utc_now(),
                    "phase": "prepared",
                    "message": (
                        "Source snapshot and pre-execution metadata created."
                    ),
                }
            ],
        }
        write_json_exclusive(
            staging_dir / artifacts["run_status"], status
        )
        staging_dir.rename(final_run_dir)
        return status
    except OSError as exc:
        raise RunnerError(
            f"could not prepare run {final_run_dir}: {exc}. Any staging "
            "directory is intentionally preserved for inspection."
        ) from exc


def load_run_status(run_dir, expected_experiment_id=None):
    status_path = Path(run_dir) / "run_status.json"
    status = load_json_strict(status_path)
    if status.get("runner_schema_version") != RUNNER_SCHEMA_VERSION:
        raise RunnerError(f"invalid runner status marker: {status_path}")
    if not same_path(status.get("run_directory", ""), run_dir):
        raise RunnerError(f"run status path mismatch: {status_path}")
    experiment_id = status.get("experiment_id")
    require_safe_id(experiment_id, f"{status_path}.experiment_id")
    if (
        expected_experiment_id is not None
        and experiment_id != expected_experiment_id
    ):
        raise RunnerError(f"run status experiment mismatch: {status_path}")
    phase = status.get("phase")
    if phase not in PHASE_STATUS:
        raise RunnerError(f"unknown or corrupt run phase {phase!r}: {status_path}")
    if status.get("status") != PHASE_STATUS[phase]:
        raise RunnerError(
            f"run status/phase combination is inconsistent: {status_path}"
        )
    if not isinstance(status.get("history"), list):
        raise RunnerError(f"run history is invalid: {status_path}")
    return status


def verify_run_identity(run_dir, experiment, protocol, provenance):
    run_dir = Path(run_dir)
    status = load_run_status(run_dir, experiment["id"])
    expected_artifacts = planned_artifacts()
    if status.get("artifacts") != expected_artifacts:
        raise RunnerError(f"run artifact map was altered: {run_dir}")

    resolved = load_json_strict(run_dir / "resolved_config.json")
    expected = resolve_experiment(experiment, protocol)
    expected_keys = set(expected) | {
        "source_provenance",
        "source_snapshot_sha256",
        "artifact_paths",
    }
    if set(resolved) != expected_keys:
        raise RunnerError(f"resolved configuration shape was altered: {run_dir}")
    for field, expected_value in expected.items():
        if resolved.get(field) != expected_value:
            raise RunnerError(
                f"resolved configuration field {field} does not match plan"
            )
    if resolved.get("source_provenance") != provenance:
        raise RunnerError(f"run source provenance does not match suite: {run_dir}")
    if resolved.get("artifact_paths") != expected_artifacts:
        raise RunnerError(f"resolved artifact paths were altered: {run_dir}")

    recorded_hashes = resolved.get("source_snapshot_sha256")
    if (
        not isinstance(recorded_hashes, dict)
        or set(recorded_hashes) != set(SOURCE_FILES)
    ):
        raise RunnerError(f"source snapshot hash map is invalid: {run_dir}")
    snapshot_dir = run_dir / "source_snapshot"
    for filename in SOURCE_FILES:
        snapshot_file = snapshot_dir / filename
        require_nonempty_file(snapshot_file, f"snapshot {filename}")
        if file_sha256(snapshot_file) != recorded_hashes[filename]:
            raise RunnerError(
                f"source snapshot file was altered: {snapshot_file}"
            )

    provenance_files = {
        "source_branch.txt": provenance["branch"] + "\n",
        "source_commit.txt": provenance["commit"] + "\n",
        "source_status.txt": provenance["status"],
    }
    for filename, expected_text in provenance_files.items():
        path = run_dir / filename
        try:
            actual_text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RunnerError(
                f"cannot read source provenance file {path}: {exc}"
            ) from exc
        if actual_text != expected_text:
            raise RunnerError(f"source provenance file was altered: {path}")
    return status


def transition_run(run_dir, phase, message, result=None, error=None):
    status_path = Path(run_dir) / "run_status.json"
    status = load_run_status(run_dir)
    if phase not in PHASE_STATUS:
        raise RunnerError(f"runner attempted unknown phase transition: {phase}")
    status["phase"] = phase
    status["updated_at"] = utc_now()
    status["status"] = PHASE_STATUS[phase]
    if result is not None:
        status["result"] = result
    if error is not None:
        status["error"] = error
    status["history"].append(
        {"at": utc_now(), "phase": phase, "message": message}
    )
    atomic_write_json(status_path, status)
    return status


def train_command(snapshot_dir, config):
    return [
        sys.executable,
        "-u",
        str(Path(snapshot_dir) / "train.py"),
        "--algorithm",
        config["algorithm"],
        "--seed",
        str(config["training_seed"]),
        "--episodes",
        str(config["episodes"]),
        "--learning-rate",
        repr(float(config["learning_rate"])),
        "--target-update-freq",
        str(config["target_update_freq"]),
        "--epsilon-start",
        repr(float(config["epsilon_start"])),
        "--epsilon-min",
        repr(float(config["epsilon_min"])),
        "--epsilon-decay",
        repr(float(config["epsilon_decay"])),
        "--replay-capacity",
        str(config["replay_capacity"]),
        "--batch-size",
        str(config["batch_size"]),
        "--gamma",
        repr(float(config["gamma"])),
    ]


def benchmark_command(snapshot_dir, benchmark, config):
    return [
        sys.executable,
        "-u",
        str(Path(snapshot_dir) / "test.py"),
        "--diagnostic",
        "--algorithm",
        config["algorithm"],
        "--episodes",
        str(benchmark["episodes"]),
        "--seed",
        str(benchmark["base_seed"]),
        "--output",
        benchmark["json_filename"],
        "--long-streak",
        str(benchmark["long_streak_threshold"]),
    ]


def display_command(command):
    return subprocess.list2cmdline([str(item) for item in command])


def run_streamed(command, cwd, log_path):
    log_path = Path(log_path)
    if log_path.exists():
        raise RunnerError(f"refusing to overwrite existing log: {log_path}")
    process = None
    try:
        with log_path.open(
            "x", encoding="utf-8", newline="\n"
        ) as log_handle:
            process = subprocess.Popen(
                [str(item) for item in command],
                cwd=str(cwd),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                shell=False,
            )
            if process.stdout is None:
                raise RunnerError("subprocess stdout pipe was not created")
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log_handle.write(line)
                log_handle.flush()
            return process.wait()
    except KeyboardInterrupt:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        raise
    except (OSError, RunnerError) as exc:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        if isinstance(exc, RunnerError):
            raise
        raise RunnerError(
            f"subprocess streaming failed for {display_command(command)}: "
            f"{exc}"
        ) from exc


def require_nonempty_file(path, label):
    path = Path(path)
    try:
        if not path.is_file() or path.stat().st_size == 0:
            raise RunnerError(f"{label} is missing or empty: {path}")
    except OSError as exc:
        raise RunnerError(f"cannot inspect {label} at {path}: {exc}") from exc


def require_paths_absent(paths, label):
    existing = [str(Path(path)) for path in paths if Path(path).exists()]
    if existing:
        raise RunnerError(
            f"{label} has unexpected pre-existing outputs: {existing}"
        )


def close_number(actual, expected, tolerance=1e-12):
    if (
        isinstance(actual, bool)
        or isinstance(expected, bool)
        or not isinstance(actual, (int, float))
        or not isinstance(expected, (int, float))
    ):
        return False
    if not math.isfinite(float(actual)) or not math.isfinite(float(expected)):
        return False
    return math.isclose(
        float(actual), float(expected), rel_tol=tolerance, abs_tol=tolerance
    )


def verify_training_artifacts(run_dir, resolved):
    run_dir = Path(run_dir)
    for filename, label in (
        ("weights.pth", "training checkpoint"),
        ("training_metrics.json", "training metrics"),
        ("training_plot.png", "training plot"),
    ):
        require_nonempty_file(run_dir / filename, label)

    metrics = load_json_strict(run_dir / "training_metrics.json")
    config = resolved["configuration"]
    if metrics.get("seed") != config["training_seed"]:
        raise RunnerError("training_metrics.json seed does not match plan")
    if metrics.get("num_episodes") != config["episodes"]:
        raise RunnerError(
            "training_metrics.json episode count does not match plan"
        )
    hyperparameters = require_object(
        metrics.get("hyperparameters"),
        "training_metrics.hyperparameters",
    )
    algorithm_provenance = ALGORITHM_PROVENANCE[config["algorithm"]]
    expected_hyperparameters = {
        "algorithm": config["algorithm"],
        "architecture": algorithm_provenance["architecture"],
        "target_strategy": algorithm_provenance["target_strategy"],
        "network_class": algorithm_provenance["network_class"],
        "learning_rate": config["learning_rate"],
        "target_update_freq": config["target_update_freq"],
        "target_update_unit": config["target_update_unit"],
        "replay_buffer_capacity": config["replay_capacity"],
        "batch_size": config["batch_size"],
        "gamma": config["gamma"],
        "epsilon_start": config["epsilon_start"],
        "epsilon_min": config["epsilon_min"],
        "epsilon_decay": config["epsilon_decay"],
        "epsilon_decay_unit": config["epsilon_decay_unit"],
        "num_episodes": config["episodes"],
    }
    for field, expected in expected_hyperparameters.items():
        actual = hyperparameters.get(field)
        if isinstance(expected, float):
            if actual is None or not close_number(actual, expected):
                raise RunnerError(
                    f"training metric {field}={actual!r} does not match "
                    f"resolved value {expected!r}"
                )
        elif actual != expected:
            raise RunnerError(
                f"training metric {field}={actual!r} does not match "
                f"resolved value {expected!r}"
            )

    reproducibility = require_object(
        metrics.get("reproducibility"),
        "training_metrics.reproducibility",
    )
    expected_reproducibility = resolved["reproducibility"]
    for field in (
        "global_seed",
        "python_random_seed",
        "numpy_seed",
        "torch_seed",
        "training_env_seed_base",
        "training_env_seed_scheme",
        "training_env_seed_last",
        "training_action_space_seed",
        "holdout_uses_separate_environment",
        "holdout_state_count",
        "holdout_env_seed_base",
        "holdout_action_space_seed",
    ):
        if reproducibility.get(field) != expected_reproducibility[field]:
            raise RunnerError(
                f"training reproducibility field {field} does not match plan"
            )
    holdout_last = require_int(
        reproducibility.get("holdout_env_seed_last"),
        "training_metrics.reproducibility.holdout_env_seed_last",
        reproducibility["holdout_env_seed_base"],
    )
    expected_reserved_ranges = {
        "validation": [901, 910],
        "benchmark_a": [1234, 1283],
        "benchmark_b": [5000, 5099],
        "final_holdout": [10000, 10099],
    }
    if (
        reproducibility.get("reserved_evaluation_seed_ranges")
        != expected_reserved_ranges
    ):
        raise RunnerError(
            "training metrics reserved evaluation ranges do not match "
            "the fixed protocol"
        )

    validation = require_object(
        metrics.get("validation"), "training_metrics.validation"
    )
    validation_config = require_object(
        validation.get("config"), "training_metrics.validation.config"
    )
    expected_validation = resolved["validation"]
    validation_pairs = {
        "validate_every": expected_validation["validate_every"],
        "episodes": expected_validation["episodes"],
        "base_seed": expected_validation["base_seed"],
        "solved_threshold": SOLVED_THRESHOLD,
    }
    for field, expected in validation_pairs.items():
        if validation_config.get(field) != expected:
            raise RunnerError(
                f"training validation field {field} does not match plan"
            )
    if validation.get("best_val_episode") is None:
        raise RunnerError("training produced no selected validation checkpoint")

    return {
        "best_validation_episode": validation["best_val_episode"],
        "best_validation_mean_reward": validation.get(
            "best_val_mean_reward"
        ),
        "best_validation_solved_rate": validation.get(
            "best_val_solved_rate"
        ),
        "mean_training_reward": metrics.get("mean_reward"),
        "final_moving_average_reward": metrics.get(
            "final_moving_avg_reward"
        ),
        "final_epsilon": metrics.get("final_epsilon"),
        "actual_holdout_env_seed_last": holdout_last,
    }


def verify_benchmark_report(report_path, benchmark, expected_configuration):
    report = load_json_strict(report_path)
    config = require_object(report.get("config"), f"{report_path}.config")
    if config.get("weights") != "weights.pth":
        raise RunnerError(
            f"{report_path} did not evaluate the run-local weights.pth"
        )
    algorithm = expected_configuration["algorithm"]
    expected_provenance = {
        "algorithm": algorithm,
        **ALGORITHM_PROVENANCE[algorithm],
    }
    for field, expected in expected_provenance.items():
        if config.get(field) != expected:
            raise RunnerError(
                f"{report_path} {field}={config.get(field)!r} does not "
                f"match expected value {expected!r}"
            )
    if config.get("episodes") != benchmark["episodes"]:
        raise RunnerError(f"{report_path} episode count does not match plan")
    if config.get("base_seed") != benchmark["base_seed"]:
        raise RunnerError(f"{report_path} base seed does not match plan")
    if config.get("long_streak_threshold") != benchmark[
        "long_streak_threshold"
    ]:
        raise RunnerError(
            f"{report_path} long-streak threshold does not match plan"
        )
    expected_diagnostic_config = {
        "solved_threshold": SOLVED_THRESHOLD,
        "low_score_threshold": LOW_SCORE_THRESHOLD,
        "greedy_epsilon": 0.0,
    }
    for field, expected in expected_diagnostic_config.items():
        actual = config.get(field)
        if actual is None or not close_number(actual, expected):
            raise RunnerError(
                f"{report_path} diagnostic field {field} does not match "
                "the fixed benchmark protocol"
            )

    per_episode = report.get("per_episode")
    rewards = report.get("rewards")
    if (
        not isinstance(per_episode, list)
        or len(per_episode) != benchmark["episodes"]
    ):
        raise RunnerError(f"{report_path} has incomplete per_episode data")
    if not isinstance(rewards, list) or len(rewards) != benchmark["episodes"]:
        raise RunnerError(f"{report_path} has incomplete rewards data")

    normalized = []
    for index, episode in enumerate(per_episode):
        label = f"{report_path}.per_episode[{index}]"
        episode = require_object(episode, label)
        expected_seed = benchmark["base_seed"] + index
        if episode.get("episode") != index + 1:
            raise RunnerError(f"{label}.episode is not contiguous")
        if episode.get("seed") != expected_seed:
            raise RunnerError(f"{label}.seed is not the expected seed")
        reward = require_number(episode.get("total_reward"), f"{label}.reward")
        length = require_int(episode.get("length"), f"{label}.length", 1)
        if length > TIMEOUT_LENGTH:
            raise RunnerError(
                f"{label}.length exceeds the environment timeout length"
            )
        if not close_number(rewards[index], reward, tolerance=1e-4):
            raise RunnerError(f"{label} reward disagrees with rewards array")
        normalized.append(
            {
                "benchmark": benchmark["id"],
                "episode": index + 1,
                "seed": expected_seed,
                "reward": reward,
                "length": length,
            }
        )

    summary = require_object(
        report.get("summary"), f"{report_path}.summary"
    )
    mean_reward = sum(item["reward"] for item in normalized) / len(normalized)
    mean_length = sum(item["length"] for item in normalized) / len(normalized)
    solved_count = sum(
        item["reward"] >= SOLVED_THRESHOLD for item in normalized
    )
    low_count = sum(
        item["reward"] < LOW_SCORE_THRESHOLD for item in normalized
    )
    if not close_number(
        summary.get("mean_reward"), mean_reward, tolerance=1e-3
    ):
        raise RunnerError(f"{report_path} summary mean reward is inconsistent")
    if not close_number(
        summary.get("mean_length"), mean_length, tolerance=1e-3
    ):
        raise RunnerError(f"{report_path} summary mean length is inconsistent")
    if summary.get("solved_count") != solved_count:
        raise RunnerError(f"{report_path} solved count is inconsistent")
    if summary.get("low_score_count") != low_count:
        raise RunnerError(f"{report_path} low-score count is inconsistent")
    expected_solved_rate = round(
        100.0 * solved_count / len(normalized), 2
    )
    expected_low_rate = round(100.0 * low_count / len(normalized), 2)
    if not close_number(
        summary.get("solved_rate_pct"),
        expected_solved_rate,
        tolerance=1e-9,
    ):
        raise RunnerError(f"{report_path} solved rate is inconsistent")
    if not close_number(
        summary.get("low_score_rate_pct"),
        expected_low_rate,
        tolerance=1e-9,
    ):
        raise RunnerError(f"{report_path} low-score rate is inconsistent")

    max_streak = require_object(
        summary.get("max_side_engine_streak"),
        f"{report_path}.summary.max_side_engine_streak",
    )
    side_names = {
        "fire_left_orientation_engine",
        "fire_right_orientation_engine",
    }
    if set(max_streak) != side_names:
        raise RunnerError(
            f"{report_path} has invalid side-engine streak fields"
        )
    normalized_streak = {
        name: require_int(
            max_streak[name],
            f"{report_path}.summary.max_side_engine_streak.{name}",
            0,
        )
        for name in side_names
    }
    side_engine_pct = require_number(
        summary.get("side_engine_overall_pct"),
        f"{report_path}.summary.side_engine_overall_pct",
        0.0,
        100.0,
    )
    return {
        "benchmark_id": benchmark["id"],
        "algorithm": algorithm,
        "architecture": expected_provenance["architecture"],
        "target_strategy": expected_provenance["target_strategy"],
        "network_class": expected_provenance["network_class"],
        "episodes": benchmark["episodes"],
        "base_seed": benchmark["base_seed"],
        "last_seed": benchmark["last_seed"],
        "mean_reward": round(mean_reward, 4),
        "solved_count": solved_count,
        "solved_rate_pct": round(
            100.0 * solved_count / len(normalized), 2
        ),
        "low_score_count": low_count,
        "low_score_rate_pct": round(
            100.0 * low_count / len(normalized), 2
        ),
        "mean_length": round(mean_length, 2),
        "timeout_count": sum(
            item["length"] == TIMEOUT_LENGTH for item in normalized
        ),
        "timeout_inference": (
            f"per_episode.length == {TIMEOUT_LENGTH}; game wrapper does not "
            "expose truncation separately"
        ),
        "side_engine_overall_pct": side_engine_pct,
        "max_side_engine_streak": normalized_streak,
        "records": normalized,
    }


def calculate_combined(benchmark_results, reference, screening_rule):
    records = []
    for result in benchmark_results:
        records.extend(result["records"])
    rewards = [item["reward"] for item in records]
    lengths = [item["length"] for item in records]
    total = len(records)
    solved_count = sum(reward >= SOLVED_THRESHOLD for reward in rewards)
    low_count = sum(reward < LOW_SCORE_THRESHOLD for reward in rewards)
    timeout_count = sum(length == TIMEOUT_LENGTH for length in lengths)
    side_names = (
        "fire_left_orientation_engine",
        "fire_right_orientation_engine",
    )
    max_side = {
        name: max(
            int(result["max_side_engine_streak"].get(name, 0))
            for result in benchmark_results
        )
        for name in side_names
    }
    combined = {
        "episodes": total,
        "mean_reward": round(sum(rewards) / total, 4),
        "solved_count": solved_count,
        "solved_rate_pct": round(100.0 * solved_count / total, 2),
        "low_score_count": low_count,
        "low_score_rate_pct": round(100.0 * low_count / total, 2),
        "mean_length": round(sum(lengths) / total, 2),
        "timeout_count": timeout_count,
        "timeout_inference": (
            f"per_episode.length == {TIMEOUT_LENGTH}; truncation and "
            "termination are combined by game.py"
        ),
        "max_side_engine_streak": max_side,
    }
    if reference is not None:
        combined["declared_reference"] = reference
        combined["reference_deltas_approximate"] = {
            "mean_reward": round(
                combined["mean_reward"] - reference["mean_reward"], 4
            ),
            "solved_rate_percentage_points": round(
                combined["solved_rate_pct"]
                - reference["solved_rate_pct"],
                2,
            ),
            "low_score_rate_percentage_points": round(
                combined["low_score_rate_pct"]
                - reference["low_score_rate_pct"],
                2,
            ),
            "mean_length": round(
                combined["mean_length"] - reference["mean_length"], 2
            ),
            "timeout_count": (
                combined["timeout_count"] - reference["timeout_count"]
            ),
        }
    if screening_rule is not None:
        constraints = screening_rule["combined_constraints"]
        combined["screening_observations"] = {
            "manual_review_required": True,
            "automatic_followup": False,
            "low_score_count_within_limit": (
                combined["low_score_count"]
                <= constraints["max_low_score_count"]
            ),
            "timeout_count_within_limit": (
                combined["timeout_count"]
                <= constraints["max_timeout_count"]
            ),
            "mean_length_within_limit": (
                combined["mean_length"]
                <= constraints["max_mean_length"]
            ),
            "manual_criteria": screening_rule["manual_criteria"],
        }
    return combined


def combined_summary_text(resolved, benchmark_results, combined):
    lines = [
        f"Experiment: {resolved['experiment_id']}",
        f"Protocol: {resolved['protocol']}",
        f"Algorithm: {resolved['configuration']['algorithm']}",
        f"Training seed: {resolved['configuration']['training_seed']}",
        "",
    ]
    for result in benchmark_results:
        lines.extend(
            [
                f"{result['benchmark_id']}:",
                f"  seeds        = {result['base_seed']}-{result['last_seed']}",
                f"  episodes     = {result['episodes']}",
                f"  mean reward  = {result['mean_reward']:.4f}",
                (
                    f"  solved       = {result['solved_count']}/"
                    f"{result['episodes']} "
                    f"({result['solved_rate_pct']:.2f}%)"
                ),
                (
                    f"  low          = {result['low_score_count']}/"
                    f"{result['episodes']} "
                    f"({result['low_score_rate_pct']:.2f}%)"
                ),
                f"  mean length  = {result['mean_length']:.2f}",
                f"  timeouts     = {result['timeout_count']}",
                "",
            ]
        )
    lines.extend(
        [
            "Combined:",
            f"  episodes     = {combined['episodes']}",
            f"  mean reward  = {combined['mean_reward']:.4f}",
            (
                f"  solved       = {combined['solved_count']}/"
                f"{combined['episodes']} "
                f"({combined['solved_rate_pct']:.2f}%)"
            ),
            (
                f"  low          = {combined['low_score_count']}/"
                f"{combined['episodes']} "
                f"({combined['low_score_rate_pct']:.2f}%)"
            ),
            f"  mean length  = {combined['mean_length']:.2f}",
            f"  timeouts     = {combined['timeout_count']}",
            (
                "  max side     = "
                f"L={combined['max_side_engine_streak']['fire_left_orientation_engine']}, "
                f"R={combined['max_side_engine_streak']['fire_right_orientation_engine']}"
            ),
            (
                "  timeout rule = episode length 1000; truncation is not "
                "separate in game.py"
            ),
        ]
    )
    if "reference_deltas_approximate" in combined:
        lines.extend(
            [
                "",
                "Approximate deltas against declared rounded reference:",
                json.dumps(
                    combined["reference_deltas_approximate"],
                    indent=2,
                    ensure_ascii=False,
                ),
            ]
        )
    if "screening_observations" in combined:
        lines.extend(
            [
                "",
                "Screening: manual review required.",
                "No follow-up experiment has been or will be scheduled.",
                json.dumps(
                    combined["screening_observations"],
                    indent=2,
                    ensure_ascii=False,
                ),
            ]
        )
    lines.append("")
    return "\n".join(lines)


def execute_experiment(run_dir, experiment, protocol, provenance):
    run_dir = Path(run_dir)
    status = verify_run_identity(
        run_dir, experiment, protocol, provenance
    )
    if status["phase"] == "completed":
        print(f"[skip completed] {experiment['id']}")
        return
    if status["phase"] == "failed":
        print(f"[skip failed] {experiment['id']}")
        return
    if status["phase"].endswith("_running"):
        raise ResumeBlocked(
            f"{experiment['id']} was interrupted during "
            f"{status['phase']}; refusing to rerun or overwrite that phase "
            "in place. Start a new timestamped suite after inspection."
        )

    resolved = load_json_strict(run_dir / "resolved_config.json")
    config = resolved["configuration"]
    snapshot_dir = run_dir / "source_snapshot"

    if status["phase"] == "prepared":
        require_paths_absent(
            [
                run_dir / "training.log",
                run_dir / "weights.pth",
                run_dir / "training_metrics.json",
                run_dir / "training_plot.png",
                run_dir / "benchmark_a.log",
                run_dir / "benchmark_a.json",
                run_dir / "benchmark_b.log",
                run_dir / "benchmark_b.json",
                run_dir / "combined_summary.txt",
            ],
            "prepared training phase",
        )
        command = train_command(snapshot_dir, config)
        transition_run(
            run_dir,
            "training_running",
            f"Launching: {display_command(command)}",
        )
        returncode = run_streamed(
            command, run_dir, run_dir / "training.log"
        )
        if returncode != 0:
            raise RunnerError(
                f"training subprocess exited with code {returncode}"
            )
        verification = verify_training_artifacts(run_dir, resolved)
        transition_run(
            run_dir,
            "training_succeeded",
            "Training completed and required artifacts were verified.",
            result={"training": verification},
        )
        status = load_run_status(run_dir)

    if status["phase"] == "training_succeeded":
        verification = verify_training_artifacts(run_dir, resolved)
        benchmark = benchmark_by_id(protocol, "benchmark_a")
        output_path = run_dir / benchmark["json_filename"]
        require_paths_absent(
            [
                output_path,
                run_dir / benchmark["log_filename"],
                run_dir / "benchmark_b.log",
                run_dir / "benchmark_b.json",
                run_dir / "combined_summary.txt",
            ],
            "pending Benchmark A phase",
        )
        command = benchmark_command(snapshot_dir, benchmark, config)
        transition_run(
            run_dir,
            "benchmark_a_running",
            f"Launching: {display_command(command)}",
            result={"training": verification},
        )
        returncode = run_streamed(
            command, run_dir, run_dir / benchmark["log_filename"]
        )
        if returncode != 0:
            raise RunnerError(
                f"Benchmark A subprocess exited with code {returncode}"
            )
        benchmark_a = verify_benchmark_report(
            output_path, benchmark, config
        )
        transition_run(
            run_dir,
            "benchmark_a_succeeded",
            "Benchmark A completed and its JSON report was verified.",
            result={
                "training": verification,
                "benchmark_a": benchmark_a,
            },
        )
        status = load_run_status(run_dir)

    if status["phase"] == "benchmark_a_succeeded":
        benchmark_a_spec = benchmark_by_id(protocol, "benchmark_a")
        benchmark_a = verify_benchmark_report(
            run_dir / benchmark_a_spec["json_filename"],
            benchmark_a_spec,
            config,
        )
        benchmark = benchmark_by_id(protocol, "benchmark_b")
        output_path = run_dir / benchmark["json_filename"]
        require_paths_absent(
            [
                output_path,
                run_dir / benchmark["log_filename"],
                run_dir / "combined_summary.txt",
            ],
            "pending Benchmark B phase",
        )
        command = benchmark_command(snapshot_dir, benchmark, config)
        transition_run(
            run_dir,
            "benchmark_b_running",
            f"Launching: {display_command(command)}",
            result={
                "training": verify_training_artifacts(run_dir, resolved),
                "benchmark_a": benchmark_a,
            },
        )
        returncode = run_streamed(
            command, run_dir, run_dir / benchmark["log_filename"]
        )
        if returncode != 0:
            raise RunnerError(
                f"Benchmark B subprocess exited with code {returncode}"
            )
        benchmark_b = verify_benchmark_report(
            output_path, benchmark, config
        )
        transition_run(
            run_dir,
            "benchmark_b_succeeded",
            "Benchmark B completed and its JSON report was verified.",
            result={
                "training": verify_training_artifacts(run_dir, resolved),
                "benchmark_a": benchmark_a,
                "benchmark_b": benchmark_b,
            },
        )
        status = load_run_status(run_dir)

    if status["phase"] == "benchmark_b_succeeded":
        benchmark_results = []
        for benchmark_id in ("benchmark_a", "benchmark_b"):
            benchmark = benchmark_by_id(protocol, benchmark_id)
            benchmark_results.append(
                verify_benchmark_report(
                    run_dir / benchmark["json_filename"],
                    benchmark,
                    config,
                )
            )
        combined = calculate_combined(
            benchmark_results,
            experiment["reference"],
            experiment["screening_rule"],
        )
        summary = combined_summary_text(
            resolved, benchmark_results, combined
        )
        write_text_if_absent_or_same(
            run_dir / "combined_summary.txt", summary
        )
        transition_run(
            run_dir,
            "completed",
            "Both benchmarks and combined summary completed. No follow-up "
            "was scheduled.",
            result={
                "training": verify_training_artifacts(run_dir, resolved),
                "benchmark_a": benchmark_results[0],
                "benchmark_b": benchmark_results[1],
                "combined": combined,
                "screening_decision": "manual_review_required",
                "automatic_followup": False,
            },
        )


def suite_rows(suite_dir, state, plan):
    experiments = {item["id"]: item for item in plan["experiments"]}
    rows = []
    for experiment_id in state["selected_experiment_ids"]:
        experiment = experiments[experiment_id]
        config = experiment["configuration"]
        run_name = state["run_directories"][experiment_id]
        run_dir = Path(suite_dir) / run_name
        if (run_dir / "run_status.json").is_file():
            status = load_run_status(run_dir)
            result = status.get("result") or {}
            training_result = result.get("training") or {}
            benchmark_a_result = result.get("benchmark_a") or {}
            benchmark_b_result = result.get("benchmark_b") or {}
            combined = result.get("combined") or {}
            phase = status["phase"]
            outcome = status["status"]
            error = status.get("error")
        else:
            training_result = {}
            benchmark_a_result = {}
            benchmark_b_result = {}
            combined = {}
            phase = "not_created"
            outcome = "pending"
            error = None
        rows.append(
            {
                "experiment_id": experiment_id,
                "protocol": plan["protocol"]["name"],
                "algorithm": config["algorithm"],
                "training_seed": config["training_seed"],
                "episodes": config["episodes"],
                "learning_rate": config["learning_rate"],
                "target_update_freq": config["target_update_freq"],
                "target_update_unit": config["target_update_unit"],
                "epsilon_start": config["epsilon_start"],
                "epsilon_min": config["epsilon_min"],
                "epsilon_decay": config["epsilon_decay"],
                "epsilon_decay_unit": config["epsilon_decay_unit"],
                "replay_capacity": config["replay_capacity"],
                "batch_size": config["batch_size"],
                "gamma": config["gamma"],
                "training_env_seed_base": (
                    20_000 + config["training_seed"]
                ),
                "training_env_seed_last": (
                    20_000
                    + config["training_seed"]
                    + config["episodes"]
                    - 1
                ),
                "training_action_space_seed": (
                    21_000 + config["training_seed"]
                ),
                "holdout_env_seed_base": (
                    30_000 + config["training_seed"]
                ),
                "holdout_env_seed_last": training_result.get(
                    "actual_holdout_env_seed_last"
                ),
                "holdout_action_space_seed": (
                    40_000 + config["training_seed"]
                ),
                "validation": plan["protocol"]["validation"],
                "benchmarks": plan["protocol"]["benchmarks"],
                "source_branch": state["git_provenance"]["branch"],
                "source_commit": state["git_provenance"]["commit"],
                "phase": phase,
                "status": outcome,
                "error": error,
                "run_directory": str(run_dir.resolve()),
                "artifact_paths": {
                    key: str((run_dir / filename).resolve())
                    for key, filename in planned_artifacts().items()
                },
                "artifact_exists": {
                    key: (run_dir / filename).exists()
                    for key, filename in planned_artifacts().items()
                },
                "training": training_result,
                "benchmark_a": benchmark_a_result,
                "benchmark_b": benchmark_b_result,
                "combined": combined,
                "reference": experiment["reference"],
                "screening_rule": experiment["screening_rule"],
                "automatic_followup": False,
            }
        )
    return rows


def write_suite_summaries(suite_dir, state, plan):
    suite_dir = Path(suite_dir)
    rows = suite_rows(suite_dir, state, plan)
    summary = {
        "runner_schema_version": RUNNER_SCHEMA_VERSION,
        "plan_id": plan["plan_id"],
        "protocol": plan["protocol"],
        "suite_status": state["status"],
        "created_at": state["created_at"],
        "updated_at": utc_now(),
        "git_provenance": state["git_provenance"],
        "automatic_followup": False,
        "runs": rows,
    }
    atomic_write_json(suite_dir / "suite_summary.json", summary)

    csv_fields = [
        "experiment_id",
        "status",
        "phase",
        "protocol",
        "algorithm",
        "training_seed",
        "episodes",
        "learning_rate",
        "target_update_freq",
        "target_update_unit",
        "epsilon_start",
        "epsilon_min",
        "epsilon_decay",
        "epsilon_decay_unit",
        "replay_capacity",
        "batch_size",
        "gamma",
        "training_env_seed_base",
        "training_env_seed_last",
        "training_action_space_seed",
        "holdout_env_seed_base",
        "holdout_env_seed_last",
        "holdout_action_space_seed",
        "mean_reward",
        "solved_count",
        "solved_rate_pct",
        "low_score_count",
        "low_score_rate_pct",
        "mean_length",
        "timeout_count",
        "source_branch",
        "source_commit",
        "run_directory",
        "error",
    ]
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=csv_fields)
    writer.writeheader()
    for row in rows:
        flat = {field: row.get(field, "") for field in csv_fields}
        for field in (
            "mean_reward",
            "solved_count",
            "solved_rate_pct",
            "low_score_count",
            "low_score_rate_pct",
            "mean_length",
            "timeout_count",
        ):
            flat[field] = row["combined"].get(field, "")
        writer.writerow(flat)
    atomic_write_text(suite_dir / "suite_summary.csv", output.getvalue())

    markdown = [
        f"# Experiment suite: {plan['plan_id']}",
        "",
        f"- Protocol: `{plan['protocol']['name']}`",
        f"- Status: `{state['status']}`",
        f"- Branch: `{state['git_provenance']['branch']}`",
        f"- Commit: `{state['git_provenance']['commit']}`",
        "- Automatic follow-up scheduling: disabled",
        "",
        "| Experiment | Algorithm | Seed | Status | Mean | Solved | Low | "
        "Length | Timeouts | Run directory |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        combined = row["combined"]
        markdown.append(
            "| {experiment_id} | {algorithm} | {training_seed} | {status} "
            "| {mean} | {solved} | {low} | {length} | {timeouts} | "
            "`{run_directory}` |".format(
                experiment_id=row["experiment_id"],
                algorithm=row["algorithm"],
                training_seed=row["training_seed"],
                status=row["status"],
                mean=combined.get("mean_reward", ""),
                solved=combined.get("solved_rate_pct", ""),
                low=combined.get("low_score_rate_pct", ""),
                length=combined.get("mean_length", ""),
                timeouts=combined.get("timeout_count", ""),
                run_directory=row["run_directory"],
            )
        )
    markdown.extend(
        [
            "",
            "Benchmark A and B are development sets. Screening metadata "
            "requires manual review and cannot schedule another experiment.",
            "",
        ]
    )
    atomic_write_text(
        suite_dir / "suite_summary.md", "\n".join(markdown)
    )


def load_resume_suite(suite_dir):
    suite_dir = Path(suite_dir).resolve()
    state_path = suite_dir / "suite_state.json"
    plan_path = suite_dir / "resolved_plan.json"
    if not state_path.is_file() or not plan_path.is_file():
        raise RunnerError(
            "--resume requires a suite directory created by this runner"
        )
    state = load_json_strict(state_path)
    if state.get("runner_schema_version") != RUNNER_SCHEMA_VERSION:
        raise RunnerError("unsupported or invalid resume suite marker")
    plan = validate_plan(load_json_strict(plan_path))
    if state.get("plan_id") != plan.get("plan_id"):
        raise RunnerError("resume suite plan_id does not match stored plan")
    if state.get("status") not in {
        "running",
        "failed",
        "interrupted",
        "completed",
        "completed_with_failures",
    }:
        raise RunnerError("resume suite has an invalid status")
    if not same_path(state.get("suite_directory", ""), suite_dir):
        raise RunnerError("resume suite path does not match its marker")
    if state.get("plan_digest") != plan_digest(plan):
        raise RunnerError("stored plan digest does not match suite marker")
    runs_root = resolve_runs_root(plan)
    if not path_is_within(suite_dir, runs_root):
        raise RunnerError("resume suite is outside its configured runs root")
    expected_ids = {
        item["id"] for item in plan["experiments"] if item["enabled"]
    }
    selected_ids = state.get("selected_experiment_ids")
    if (
        not isinstance(selected_ids, list)
        or not selected_ids
        or len(selected_ids) != len(set(selected_ids))
        or not set(selected_ids).issubset(expected_ids)
    ):
        raise RunnerError("resume suite has invalid selected experiment IDs")
    run_directories = state.get("run_directories")
    if (
        not isinstance(run_directories, dict)
        or set(run_directories) != set(selected_ids)
    ):
        raise RunnerError("resume suite has invalid run directory mapping")
    folded_run_names = set()
    for experiment_id in selected_ids:
        run_name = run_directories.get(experiment_id)
        require_basename(run_name, f"resume run directory for {experiment_id}")
        folded = run_name.casefold()
        if folded in folded_run_names:
            raise RunnerError("resume suite has colliding run directories")
        folded_run_names.add(folded)
        if not path_is_within(suite_dir / run_name, suite_dir):
            raise RunnerError("resume run directory escapes suite root")
    git_provenance = require_object(
        state.get("git_provenance"), "resume git_provenance"
    )
    for field in ("root", "branch", "commit", "status"):
        if not isinstance(git_provenance.get(field), str):
            raise RunnerError(
                f"resume git_provenance.{field} must be a string"
            )
    return suite_dir, state, plan


def print_dry_run(plan, experiments, provenance, suite_dir, state=None):
    print("DRY RUN: no directories, files, training, or benchmarks will be run.")
    print(f"Plan: {plan['plan_id']}")
    print(f"Protocol: {plan['protocol']['name']}")
    print(f"Clean source: {provenance['branch']} @ {provenance['commit']}")
    print(f"Suite directory: {suite_dir}")
    for experiment in experiments:
        experiment_id = experiment["id"]
        if state is None:
            run_name = f"{experiment_id}-{Path(suite_dir).name.rsplit('-', 1)[-1]}"
            phase = "not_created"
        else:
            run_name = state["run_directories"][experiment_id]
            run_dir = Path(suite_dir) / run_name
            phase = (
                load_run_status(run_dir)["phase"]
                if (run_dir / "run_status.json").is_file()
                else "not_created"
            )
        run_dir = Path(suite_dir) / run_name
        snapshot_dir = run_dir / "source_snapshot"
        print("")
        print(f"Experiment: {experiment_id}")
        print(f"  Current phase: {phase}")
        print(f"  Proposed run directory: {run_dir}")
        print(
            "  Train: "
            + display_command(
                train_command(
                    snapshot_dir, experiment["configuration"]
                )
            )
        )
        for benchmark in plan["protocol"]["benchmarks"]:
            print(
                f"  {benchmark['id']}: "
                + display_command(
                    benchmark_command(
                        snapshot_dir,
                        benchmark,
                        experiment["configuration"],
                    )
                )
            )
    print("")
    print(
        "Final holdout seeds 10000-10099 are reserved and absent from all "
        "commands."
    )


def parse_cli():
    parser = argparse.ArgumentParser(
        description=(
            "Execute a finite deterministic DQN experiment plan. The runner "
            "never selects or schedules follow-up experiments."
        ),
        allow_abbrev=False,
    )
    parser.add_argument(
        "--plan",
        help=(
            "JSON plan path, relative to the repository root when not "
            "absolute. Default: experiment_plans/next_batch.json"
        ),
    )
    parser.add_argument(
        "--experiment-id",
        help="Execute only this enabled experiment ID from the plan.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate plan and clean Git provenance, then print the finite "
            "commands without creating files or launching train.py/test.py."
        ),
    )
    parser.add_argument(
        "--resume",
        help=(
            "Explicit existing suite directory to resume. The stored plan, "
            "selected IDs, branch, and commit are reused; --plan and "
            "--experiment-id are not accepted with --resume."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_cli()
    try:
        provenance = get_clean_git_provenance()

        if args.resume:
            if args.plan or args.experiment_id:
                raise RunnerError(
                    "--resume cannot be combined with --plan or "
                    "--experiment-id; the suite's stored selection is fixed"
                )
            suite_dir, state, plan = load_resume_suite(args.resume)
            recorded = state["git_provenance"]
            if (
                provenance["branch"] != recorded["branch"]
                or provenance["commit"] != recorded["commit"]
            ):
                raise RunnerError(
                    "resume requires the exact clean branch and commit "
                    "recorded when the suite was created"
                )
            experiments_by_id = {
                item["id"]: item for item in plan["experiments"]
            }
            experiments = [
                experiments_by_id[item]
                for item in state["selected_experiment_ids"]
            ]
            if args.dry_run:
                print_dry_run(
                    plan, experiments, provenance, suite_dir, state
                )
                return 0
        else:
            if args.plan:
                plan_path = Path(args.plan)
                if not plan_path.is_absolute():
                    plan_path = PROJECT_ROOT / plan_path
            else:
                plan_path = DEFAULT_PLAN
            plan = validate_plan(load_json_strict(plan_path.resolve()))
            experiments = select_experiments(plan, args.experiment_id)
            runs_root = resolve_runs_root(plan)
            stamp = timestamp_slug()
            suite_dir = runs_root / (
                f"{plan['plan_id']}-suite-{stamp}"
            )
            if args.dry_run:
                print_dry_run(
                    plan, experiments, provenance, suite_dir
                )
                return 0

            runs_root.mkdir(parents=True, exist_ok=True)
            suite_dir.mkdir(exist_ok=False)
            run_directories = {
                item["id"]: f"{item['id']}-{stamp}"
                for item in experiments
            }
            state = {
                "runner_schema_version": RUNNER_SCHEMA_VERSION,
                "plan_id": plan["plan_id"],
                "plan_digest": plan_digest(plan),
                "suite_directory": str(suite_dir.resolve()),
                "created_at": utc_now(),
                "updated_at": utc_now(),
                "status": "running",
                "git_provenance": provenance,
                "selected_experiment_ids": [
                    item["id"] for item in experiments
                ],
                "run_directories": run_directories,
            }
            write_json_exclusive(
                suite_dir / "resolved_plan.json", plan
            )
            write_json_exclusive(
                suite_dir / "suite_state.json", state
            )
            write_suite_summaries(suite_dir, state, plan)

        had_failure = False
        new_failure = False
        experiments_by_id = {
            item["id"]: item for item in plan["experiments"]
        }
        for experiment_id in state["selected_experiment_ids"]:
            experiment = experiments_by_id[experiment_id]
            run_dir = suite_dir / state["run_directories"][experiment_id]
            try:
                if not run_dir.exists():
                    snapshot_provenance = get_clean_git_provenance()
                    if snapshot_provenance != provenance:
                        raise RunnerError(
                            "source branch, commit, or clean status changed "
                            "before snapshot creation"
                        )
                    prepare_run(
                        run_dir,
                        experiment,
                        plan["protocol"],
                        provenance,
                    )
                    if get_clean_git_provenance() != provenance:
                        raise RunnerError(
                            "source provenance changed while the snapshot "
                            "was being created"
                        )
                status = verify_run_identity(
                    run_dir,
                    experiment,
                    plan["protocol"],
                    provenance,
                )
                if status["phase"] == "failed":
                    had_failure = True
                    print(f"[skip previously failed] {experiment_id}")
                    continue
                execute_experiment(
                    run_dir,
                    experiment,
                    plan["protocol"],
                    provenance,
                )
                final_status = load_run_status(run_dir, experiment_id)
                if final_status["phase"] not in {"completed", "failed"}:
                    raise RunnerError(
                        f"{experiment_id} stopped in unexpected phase "
                        f"{final_status['phase']}"
                    )
                if final_status["phase"] == "failed":
                    had_failure = True
            except ResumeBlocked as exc:
                print(f"RESUME BLOCKED {experiment_id}: {exc}", file=sys.stderr)
                raise
            except KeyboardInterrupt:
                current = load_run_status(run_dir)
                transition_run(
                    run_dir,
                    "failed",
                    "Interrupted by user; this phase will not be rerun in "
                    "place.",
                    result=current.get("result"),
                    error={
                        "failed_phase": current["phase"],
                        "message": "KeyboardInterrupt",
                    },
                )
                state["status"] = "interrupted"
                state["updated_at"] = utc_now()
                atomic_write_json(
                    suite_dir / "suite_state.json", state
                )
                write_suite_summaries(suite_dir, state, plan)
                raise
            except (OSError, RunnerError) as exc:
                current = None
                if (run_dir / "run_status.json").is_file():
                    try:
                        current = load_run_status(
                            run_dir, experiment_id
                        )
                    except RunnerError:
                        current = None
                if current is not None:
                    transition_run(
                        run_dir,
                        "failed",
                        "Experiment stopped safely after an error.",
                        result=current.get("result"),
                        error={
                            "failed_phase": current["phase"],
                            "message": str(exc),
                        },
                    )
                print(f"FAILED {experiment_id}: {exc}", file=sys.stderr)
                had_failure = True
                new_failure = True
                break

            write_suite_summaries(suite_dir, state, plan)

        if new_failure:
            state["status"] = "failed"
        elif had_failure:
            state["status"] = "completed_with_failures"
        else:
            state["status"] = "completed"
        state["updated_at"] = utc_now()
        atomic_write_json(suite_dir / "suite_state.json", state)
        write_suite_summaries(suite_dir, state, plan)
        print(f"Suite status: {state['status']}")
        print(f"Suite directory: {suite_dir}")
        return 1 if state["status"] != "completed" else 0
    except KeyboardInterrupt:
        print("Experiment suite interrupted.", file=sys.stderr)
        return 130
    except (OSError, RunnerError) as exc:
        print(f"Experiment runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
