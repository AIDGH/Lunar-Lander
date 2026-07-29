# LunarLander DQN Project Handoff

This document is the operational handoff for final candidate selection, candidate
freezing, the one-time final holdout, final analysis, report writing, and
submission. It is based on the repository source, experiment plans, and archived
run metadata available through the completed Deep D3QN seed-44 suite.

## Packaged handoff assets

The repository is now a self-contained handoff package. A teammate who clones it
receives:

- the [complete copied `runs/` archive](runs/), including legacy runs and the
  completed finite-runner suites;
- archived source snapshots, trained weights, training metrics and plots,
  Benchmark A/B JSON and logs, run statuses, provenance records, combined
  summaries, and runner logs contained in that archive;
- the current authoritative [run artifact index](RUNS_INDEX.md);
- [historical experiment-review input](docs/handoff_context/Lunar_Lander_Experiment_Review_Input.md);
- [Persian continuation context for another assistant/chat](docs/handoff_context/Lunar_Lander_Next_Chat_Starter_FA.txt);
- [the earlier Persian project handoff](docs/handoff_context/Lunar_Lander_Project_Handoff_FA.md);
- [context-document guidance](docs/handoff_context/README.md).

`PROJECT_HANDOFF.md` and `RUNS_INDEX.md` are the current authoritative handoff
documents. The three files under `docs/handoff_context/` preserve earlier
context and may be outdated.

Archived manifests, status files, and logs contain absolute paths from the
original execution machine, especially `/mnt/e/uni/ai/project/runs/...`. Those
paths are provenance, not clone-time instructions. After cloning, use paths
relative to the repository root, beginning with `runs/`. Directory links above
are navigational only; use the concrete artifact links in `RUNS_INDEX.md` when a
Markdown viewer does not render directory listings.

The files are present in the packaged workspace audited for this handoff.
Because `.gitignore` excludes `*.log`, Git tracking of the copied runner and
per-run logs could not be verified without a prohibited Git command. Confirm
that those logs are present in a fresh clone before relying on them.

## 1. Executive status

The core implementation is complete. Deterministic training, greedy validation,
development benchmarking, experiment isolation, and source/configuration
provenance tooling are implemented. The planned model search and all authorized
training runs are complete.

The reserved final-holdout seeds **10000–10099 have not been used**. The
experiment plans mark them as reserved, the runner excludes them from generated
experiment commands, and no archived diagnostic or benchmark report inspected
for this handoff had `base_seed` 10000.

The remaining work is:

1. choose and record the final candidate;
2. freeze that checkpoint and its exact archived source snapshot;
3. execute the final holdout exactly once;
4. analyze the holdout without reopening model selection;
5. finish the report and submission package.

> **Stopping rule:** No additional training, rescue, tuning, or replication is
> currently authorized. The remaining work is final governance and evaluation,
> not model search.

## 2. Repository and environment

| Item | Authoritative value |
|---|---|
| Repository after cloning | repository root (`.`) |
| Original execution-machine repository | `/mnt/e/uni/ai/project/Lunar-Lander` |
| Packaged runs archive | [`runs/`](runs/) |
| Original execution-time runs root | `/mnt/e/uni/ai/project/runs` (provenance only) |
| WSL environment activation | `source /root/venvs/lunar-lander/bin/activate` |
| Correct WSL interpreter | `/root/venvs/lunar-lander/bin/python` |
| Current experiment branch | `experiment/deterministic-vanilla-search` |
| Latest completed experiment-suite source commit | `133b7c315f64eda25f798ec2cfbbec319041fe62` |
| Final handoff documentation commit | `<fill after committing this document>` |
| Environment | `LunarLander-v2` |
| Gymnasium | `0.29.1` |
| PyTorch | `2.13.0+cu130` |

The repository-local `.venv` is a **Windows** virtual environment. Do not use it
from WSL. Archived runner launch records confirm that completed suites used
`/root/venvs/lunar-lander/bin/python`.

`requirements.txt` pins Gymnasium (including the Box2D extra) to `0.29.1` and
specifies `torch>=2.0.0`; it does not itself record the exact installed PyTorch
build. The exact `2.13.0+cu130` value above is the project owner's recorded
environment value and should be captured again in the final reproducibility
record.

The commit above is the clean source commit recorded by the latest completed
Deep D3QN seed-44 suite. The later documentation commit that adds this handoff
will necessarily have a different hash. After committing this file, replace the
placeholder with—or otherwise record—the documentation commit hash without
altering any archived run.

## 3. Operating and safety rules

- `game.py` was never intentionally modified. The important archived snapshots
  have the same `game.py` SHA-256, and the project specification treats it as the
  instructor-provided wrapper.
- A human launches all training, benchmarking, Git, freezing, and final-holdout
  commands. Codex is used only for explicitly authorized inspection and file
  editing.
- Archived run directories are immutable evidence. Never train, benchmark, or
  write outputs in place over an archived run.
- Root-level baseline artifacts such as `weights.pth`,
  `training_metrics.json`, plots, and diagnostic reports are historical files;
  do not overwrite them and do not treat them as the selected candidate.
- Every new run, freeze, or final-evaluation record must use a unique,
  non-overwriting directory.
- Final-holdout seeds 10000–10099 remain forbidden until a candidate decision
  has been signed off and that candidate has been frozen and hash-verified.
- Benchmark A and Benchmark B are development/model-selection sets. They are
  not unseen final test data.
- After the final holdout, development results must not be used to reopen
  candidate selection.
- An unfavorable final holdout must be reported. It is not permission to
  retrain, switch checkpoints, tune, or try another seed.

## 4. Deterministic protocol

### Training configuration

The runner supplies the effective configuration explicitly on the training
command line; candidate runs do not depend on `train.py` defaults.

| Setting | Configuration A / controlled challenger value |
|---|---:|
| Training episodes | 1000 |
| Learning rate | `5e-4` |
| Discount factor (`gamma`) | `0.99` |
| Batch size | 64 |
| Uniform replay capacity | 10,000 transitions |
| Epsilon start | `1.0` |
| Epsilon minimum | `0.01` |
| Epsilon decay | `0.995` per completed episode |
| Target synchronization | hard copy at an interval of 1000 successful optimizer updates |
| Optimizer | Adam on the policy network |
| Loss | Huber / Smooth L1 |
| Gradient clipping | global norm clipped to `1.0` |

Python `random`, NumPy, and PyTorch are seeded with the experiment training
seed. Training uses a fresh deterministic environment reset for every episode:

```text
training environment seed = 20000 + training_seed + episode - 1
training action-space seed = 21000 + training_seed
```

For a 1000-episode seed-42 run, training environment seeds are 20042–21041.
For seed 44, they are 20044–21043. The action-space seeds are 21042 and 21044,
respectively. Exploration and replay sampling use the seeded Python RNG; the
environment action-space stream is also explicitly seeded.

Training collects 200 fixed states for Q-value diagnostics in a **separate**
environment:

```text
Q-diagnostic environment initial seed = 30000 + training_seed
Q-diagnostic action-space seed        = 40000 + training_seed
```

If a diagnostic rollout terminates during collection, its reset seed increments
by one. The actual last seed is recorded in `training_metrics.json`. This
internal Q-diagnostic state collection is not the reserved final holdout and
does not use seeds 10000–10099.

Once the replay buffer contains 64 transitions, the implementation performs one
uniform-sample learning/optimizer update per environment transition. Terminal
masking uses the wrapper's combined `done` flag. The Vanilla Bellman target is

```text
r + gamma * max_a Q_target(s', a) * (1 - done)
```

and the Double target selects with the online network and evaluates that action
with the target network.

There is an implementation-order nuance worth preserving in any reproduction:
after `optimizer.step()`, the code checks `steps_done % target_update_freq == 0`,
copies policy weights to the target network if true, and then increments
`steps_done`. Because the counter starts at zero, synchronization occurs after
the first successful optimizer update and then after updates 1001, 2001, and so
on. The gap is 1000 optimizer updates; do not silently “correct” the initial
update behavior.

The harness seeds all RNG streams it actually uses, but it does not enable
`torch.use_deterministic_algorithms`. The implementation runs on CPU in the
recorded workflow. Treat repeatability as controlled within this
software/hardware protocol, not as a formal cross-platform bitwise guarantee.

### Validation and checkpoint selection

- Validation runs every 50 completed training episodes.
- Each validation contains 10 greedy, non-rendered episodes.
- Validation seeds are fixed at 901–910.
- Validation uses a separate environment and direct `argmax`, without consuming
  training RNG draws, adding replay transitions, changing epsilon, or learning.
- A reward of at least 200 counts as solved.
- `weights.pth` retains the checkpoint with the highest validation mean reward.
- An exact mean-reward tie is broken only by a strictly higher solved rate.

### Development evaluation

| Set | Seeds | Episodes | Policy |
|---|---:|---:|---|
| Benchmark A | 1234–1283 | 50 | greedy |
| Benchmark B | 5000–5099 | 100 | greedy |
| Combined development result | both ranges | 150 | greedy |

Benchmark A and B are known development sets that were consulted repeatedly
during model selection. They must be labeled as development results in the
report.

### Reserved final holdout

- Seeds: **10000–10099**
- Episodes: 100
- Policy: greedy
- Use: exactly once, only after candidate selection and freezing

The holdout is the final evaluation set. It must not influence training,
checkpoint selection, or candidate replacement.

## 5. Supported algorithm modes

| Algorithm | Network | Bellman target | Persisted architecture |
|---|---|---|---|
| `vanilla` | Standard `DQN` | target-network max | `standard` |
| `double_dqn` | Standard `DQN` | online argmax, target evaluation | `standard` |
| `dueling_dqn` | Direct-head `DuelingDQN` | target-network max | `dueling` |
| `d3qn` | Direct-head `DuelingDQN` | online argmax, target evaluation | `dueling` |
| `deep_d3qn` | `DeepDuelingDQN` | online argmax, target evaluation | `dueling_deep` |

Parameter counts below are per policy or target network for LunarLander's
8-dimensional state and 4 discrete actions.

### Standard DQN

```text
8 -> 128 (ReLU) -> 128 (ReLU) -> 4
18,180 parameters
```

### Direct-head DuelingDQN

```text
shared:    8 -> 128 (ReLU) -> 128 (ReLU)
value:     128 -> 1
advantage: 128 -> 4
18,309 parameters
```

### DeepDuelingDQN

```text
shared:    8 -> 128 (ReLU) -> 128 (ReLU)
value:     128 -> 128 (ReLU) -> 1
advantage: 128 -> 128 (ReLU) -> 4
51,333 parameters
```

Both dueling variants aggregate the streams as:

```text
Q = V + A - mean(A, dim=-1, keepdim=True)
```

The direct-head model changes the final parameterization but adds little
post-trunk functional capacity. The deep-stream model adds independent nonlinear
representations for value and advantage after the shared trunk. This distinction
is material: the direct-head D3QN result is not an evaluation of the same
architecture as `deep_d3qn`.

## 6. Experiment runner and artifacts

`experiment_runner.py` is a finite, configuration-driven runner. It:

- accepts strict JSON plans and executes only enabled experiments in plan order;
- requires a clean, committed Git working tree, including for dry-run;
- captures source branch, commit, and clean status;
- requires deterministic-harness protocol version 1 and the fixed seed ranges;
- rejects plans that overlap or attempt to use final-holdout seeds;
- at execution time, creates timestamped, unique, non-overwriting suite and run
  directories outside the source repository; the completed archive has since
  been copied intact into repository-relative [`runs/`](runs/) for handoff;
- snapshots `agent.py`, `model.py`, `train.py`, `test.py`, and `game.py`, with
  recorded SHA-256 values;
- launches training and then Benchmark A and B sequentially from the snapshot,
  with the run directory as the working directory;
- verifies resolved hyperparameters, reproducibility metadata, validation
  checkpoint production, benchmark seeds/counts/summaries, and run-local
  weights;
- writes logs, metrics, plots, benchmark JSON, and a combined summary;
- supports a non-writing dry-run that prints the finite commands;
- has conservative resume behavior tied to the stored plan digest, clean branch,
  and exact commit;
- skips terminal completed/failed phases and refuses unsafe in-place reruns of
  interrupted `*_running` phases;
- requires `automatic_followup: false` and never selects or schedules another
  experiment.

The runner itself and the resolved plan are retained at suite level; each run's
source snapshot contains the five executable project source files. Suite-level
artifacts include `resolved_plan.json`, `suite_state.json`, and summaries in
JSON, CSV, and Markdown.

Expected per-run artifacts are:

```text
experiment_manifest.txt
resolved_config.json
run_status.json
source_branch.txt
source_commit.txt
source_status.txt
source_snapshot/
training.log
weights.pth
training_metrics.json
training_plot.png
benchmark_a.log
benchmark_a.json
benchmark_b.log
benchmark_b.json
combined_summary.txt
```

For an archived checkpoint, its archived `source_snapshot/`,
`resolved_config.json`, and provenance files are authoritative. Do not substitute
the current workspace source, current `train.py` defaults, or root-level
artifacts. The current no-argument `train.py` defaults still reflect an earlier
B43 experiment (`vanilla`, seed 43, target interval 2000); this is harmless for
explicit runner plans but unsafe for an ad hoc no-argument training launch.

## 7. Main experimental results

All metrics in the first table use deterministic-harness Benchmark A and B
unless explicitly labeled otherwise. “Low” means reward below zero. “Max side”
is the maximum contiguous left- or right-orientation-engine action streak across
the 150 development episodes.

| Run | Seed(s) | Mean reward | Solved | Low | Mean length | Timeouts | Max side |
|---|---:|---:|---:|---:|---:|---:|---:|
| Vanilla Configuration A, A42 | 42 | 230.12 | 116/150 (77.33%) | 0/150 (0%) | 244.59 | 9 | 83 |
| Vanilla Configuration A, A43 | 43 | 233.94 | 129/150 (86.00%) | 1/150 (0.67%) | 311.65 | 3 | 71 |
| Vanilla Configuration A, A44 | 44 | 237.929 | 134/150 (89.33%) | 0/150 (0%) | 283.11 | 1 | 116 |
| Configuration A descriptive aggregate | 42, 43, 44 | ~234.00 | 379/450 (84.22%) | 1/450 (0.22%) | ~279.78 | 13/450 | 116 |
| Double DQN | 42 | 236.6064 | 126/150 (84.00%) | 3/150 (2.00%) | 310.76 | 7 | 502 |
| Direct-head Dueling DQN | 42 | 224.1384 | 112/150 (74.67%) | 3/150 (2.00%) | 317.17 | 15 | 58 |
| Direct-head D3QN | 42 | 208.2221 | 108/150 (72.00%) | 1/150 (0.67%) | 269.29 | 8 | 491 |
| Deep-stream D3QN | 42 | 265.0437 | 143/150 (95.33%) | 0/150 (0%) | 246.90 | 3 | 28 |
| Deep-stream D3QN replication | 44 | 208.929 | 112/150 (74.67%) | 4/150 (2.67%) | 341.68 | 11 | 161 |

The Configuration A aggregate is descriptive, not a confidence interval or an
independent 450-seed test: the same 150 development seeds were evaluated for
each of three independently initialized training runs.

### Deep D3QN benchmark and validation detail

| Run | Benchmark A mean / solved | Benchmark B mean / solved | Best validation episode | Best validation mean | Best validation solved |
|---|---|---|---:|---:|---:|
| Deep D3QN seed 42 | 274.5898 / 49 of 50 (98%) | 260.2707 / 94 of 100 (94%) | 1000 | 285.1657 | 100% |
| Deep D3QN seed 44 | 204.2186 / 37 of 50 (74%) | 211.2842 / 75 of 100 (75%) | 450 | 212.8224 | 80% |

For completeness, A44's best validation checkpoint was episode 950, with mean
reward `273.88455018419546` and solved rate 100%.

### Search sequence and interpretation

1. The project began with a pre-harness Vanilla baseline and manually archived
   exploratory Double, larger-replay, Dueling, and lower-learning-rate runs.
2. A corrected deterministic harness established A42 and controlled learning
   rate, target-interval, and epsilon-decay comparisons.
3. A43/B43 provided the second target-interval pairing. A44 added a third
   Vanilla Configuration A training seed.
4. Finite runner suites evaluated deterministic Double DQN, direct-head Dueling
   DQN, direct-head D3QN, the deep-stream D3QN rescue, and its seed-44
   replication.
5. Deep D3QN seed 42 earned replication, but seed 44 failed its predeclared
   replication gate. The declared stopping rule then ended model search.

### Historical and protocol-limited results

| Run | Protocol status | Mean | Solved | Low | Mean length | Timeouts |
|---|---|---:|---:|---:|---:|---:|
| Reported initial Vanilla reference, LR `1e-3` | historical, validation-selected, pre-deterministic harness | 225.36 | 79.33% | 8.67% | 221.1 | 3 |
| Vanilla LR `5e-4` seed 42 | historical, nondeterministic training protocol | 240.36 | 80.67% | 0% | 333.0 | 14 |
| Double DQN, replay 10k, seed 42 | historical exploratory protocol | 227.46 | 81.33% | 4.00% | 312.5 | 11 |
| Double DQN, replay 50k, seed 42 | historical exploratory protocol | 186.74 | 62.67% | 4.67% | 282.0 | 9 |
| Historical Dueling DQN, seed 42 | historical exploratory protocol | 221.78 | 74.67% | 2.00% | 319.1 | 16 |
| Deterministic Vanilla, LR `1e-3`, target 1000, seed 42 | deterministic harness | 170.47 | 51.33% | 9.33% | 335.84 | 27 |
| Deterministic Vanilla, epsilon decay `0.997`, seed 42 | deterministic harness | 203.70 | 69.33% | 0.67% | 252.56 | 7 |
| Deterministic target interval 2000, seed 42 | deterministic harness; artifact caveat below | 235.79 | 86.67% | 5.33% | 324.17 | 11 |
| Deterministic target interval 2000, seed 43 | deterministic harness | 225.96 | 78.67% | 2.67% | 350.13 | 15 |

The quoted `225.36` historical reference is supported by the 50-episode
`diagnostic_report_final_candidate.json`/`diagnostic_report_final_50.json`
development report and the 100-episode
`diagnostic_report_final_unseen_100.json` report in
the original-host-only `local_archive/validated-dqn-baseline`. That directory is
excluded by `.gitignore` and must not be assumed to exist after cloning; the
packaged [historical experiment-review input](docs/handoff_context/Lunar_Lander_Experiment_Review_Input.md)
preserves the relevant review context. Several baseline files are duplicate or
similarly named, so those filenames and their seed ranges—not the word “final”
alone—must be cited in the report. The archive also contains an earlier
predecessor checkpoint whose available 50-episode seed-1234 diagnostic has mean
`183.8055`; that is not the validation-selected checkpoint underlying the
quoted combined `225.36` reference. The misleading word `unseen` in the
100-episode filename does not make it final holdout data: its embedded
configuration is base seed 5000, i.e. known Benchmark B.

The pre-harness runs used earlier reproducibility behavior and manual archive
layouts. In particular, action-space sampling and environment consumption were
not isolated in the same way as the deterministic harness. Their results are
useful exploratory history, but they are not direct paired evidence against the
deterministic runs.

The historical directory named `double-dqn-buffer50k-seed42-20260726-185530`
does **not** prove that a 50,000-transition replay buffer was used. Its archived
`agent.py` default is 10,000 and its archived `train.py` passes no override;
only filenames claim 50k. Treat the reported metrics as an ambiguously labeled
exploratory run, not as valid replay-capacity ablation evidence.

The seed-42 target-2000 directory was later contaminated by an unrelated
LR-`1e-3`, target-1000 execution. Its generic manifest, training metrics, plot,
and `weights.pth` describe the later run. The retained target-2000
`source_snapshot/`, `training_target2000.log`, target-named benchmark JSON, and
`combined_summary.txt` support the target-2000 evaluation. Therefore the
target-2000 summary can be cited as historical evaluation evidence, but that
directory is not a coherent candidate package and its checkpoint must never be
selected.

No completed 1500-episode epsilon-`0.997` artifact exists under the inspected
runs root. A previously discussed longer schedule must not be reported as an
executed experiment.

Across deterministic seeds 42 and 43, target interval 2000 did not deliver a
repeatable primary-performance advantage and consistently increased low-score
failures, episode length, timeouts, and pathological side-engine behavior.
Deterministic Double DQN and the deep-stream D3QN rescue each showed attractive
seed-42 primary metrics but failed the project's reliability/replication
requirements. Vanilla Configuration A is the only leading configuration backed
by three training seeds.

## 8. Exact important run paths

All expected artifacts listed below were verified present. Each run has
`status: succeeded`, `phase: completed`, and an empty `source_status.txt`. The
checkpoint files were checked for existence only; their tensor contents were not
loaded during preparation of this handoff. The paths in this section are
repository-relative and authoritative after cloning. Absolute paths embedded in
the artifacts record the original execution machine only.

### Vanilla A44

```text
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z
```

- Algorithm/seed: `vanilla`, 44
- Source commit: `d286e4be15f681d790ae35f611ab63359f553f7b`
- Checkpoint: `weights.pth`
- Archived implementation: `source_snapshot/`
- Effective protocol/configuration: `resolved_config.json`
- Training evidence: `training_metrics.json`
- Benchmark evidence: `benchmark_a.json`, `benchmark_b.json`
- Combined evidence: `combined_summary.txt`
- Completion/provenance state: `run_status.json`

The exact candidate paths are therefore:

```text
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/weights.pth
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/source_snapshot/
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/resolved_config.json
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/training_metrics.json
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/benchmark_a.json
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/benchmark_b.json
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/combined_summary.txt
runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/run_status.json
```

Concrete packaged links: [weights](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/weights.pth),
[source snapshot](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/source_snapshot/),
[resolved configuration](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/resolved_config.json),
[training metrics](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/training_metrics.json),
[Benchmark A](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/benchmark_a.json),
[Benchmark B](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/benchmark_b.json),
[combined summary](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/combined_summary.txt), and
[run status](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/run_status.json).

### Deep D3QN seed 42

```text
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z
```

- Algorithm/seed: `deep_d3qn`, 42
- Source commit: `8ada1525507738fd2e9460a86e359b8a09c78457`
- Checkpoint: `weights.pth`
- Archived implementation: `source_snapshot/`
- Effective protocol/configuration: `resolved_config.json`
- Training evidence: `training_metrics.json`
- Benchmark evidence: `benchmark_a.json`, `benchmark_b.json`
- Combined evidence: `combined_summary.txt`
- Completion/provenance state: `run_status.json`

The exact candidate paths are:

```text
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/weights.pth
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/source_snapshot/
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/resolved_config.json
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/training_metrics.json
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/benchmark_a.json
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/benchmark_b.json
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/combined_summary.txt
runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/run_status.json
```

Concrete packaged links: [weights](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/weights.pth),
[source snapshot](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/source_snapshot/),
[resolved configuration](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/resolved_config.json),
[training metrics](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/training_metrics.json),
[Benchmark A](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/benchmark_a.json),
[Benchmark B](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/benchmark_b.json),
[combined summary](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/combined_summary.txt), and
[run status](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/run_status.json).

### Deep D3QN seed 44

```text
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z
```

- Algorithm/seed: `deep_d3qn`, 44
- Source commit: `133b7c315f64eda25f798ec2cfbbec319041fe62`
- Checkpoint: `weights.pth`
- Archived implementation: `source_snapshot/`
- Effective protocol/configuration: `resolved_config.json`
- Training evidence: `training_metrics.json`
- Benchmark evidence: `benchmark_a.json`, `benchmark_b.json`
- Combined evidence: `combined_summary.txt`
- Completion/provenance state: `run_status.json`

The exact paths are:

```text
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/weights.pth
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/source_snapshot/
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/resolved_config.json
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/training_metrics.json
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/benchmark_a.json
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/benchmark_b.json
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/combined_summary.txt
runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/run_status.json
```

Concrete packaged links: [weights](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/weights.pth),
[source snapshot](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/source_snapshot/),
[resolved configuration](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/resolved_config.json),
[training metrics](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/training_metrics.json),
[Benchmark A](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/benchmark_a.json),
[Benchmark B](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/benchmark_b.json),
[combined summary](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/combined_summary.txt), and
[run status](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/run_status.json).

Deep42 and Deep44 have identical archived SHA-256 values for all five
`source_snapshot/` files. Their configuration differs only in training seed.
A44 predates the expanded algorithm-provenance fields in training metrics, but
its manifest and resolved configuration explicitly identify `vanilla`; this is
a schema-age difference, not a configuration conflict.

## 9. Candidate-selection decision

### Predeclared/default decision

The predeclared replication rule stated:

- Deep D3QN seed 42 could only earn a separately reviewed seed-44 replication.
- A one-training-seed Deep D3QN result could not replace A44.
- If Deep D3QN seed 44 passed its declared gate, the seed-44 Deep D3QN
  checkpoint would become the frozen final candidate.
- If seed 44 failed, the archived Vanilla A44 checkpoint would be retained.
- Adaptive selection between Deep42 and Deep44 was forbidden.
- No further training, rescue, tuning, or replication was authorized after that
  result.

Deep44 failed both primary gate alternatives and failed the limits on negative
episodes, timeouts, mean length, maximum side-engine streak, both-benchmark
acceptability, and confirming the seed-42 performance direction.

Therefore, the protocol-consistent and recommended final candidate is:

- **Configuration:** Vanilla Configuration A
- **Algorithm:** `vanilla`
- **Training seed:** 44
- **Checkpoint:** the archived A44 `weights.pth` listed in Section 8
- **Implementation:** the archived A44 `source_snapshot/` from the same run

This decision is supported by three-training-seed Vanilla evidence, A44's strong
and balanced development result, zero negative episodes, and only one timeout.
Deep D3QN displayed severe training-seed sensitivity. Selecting Deep42 after its
authorized replication failed would be a post-hoc adaptive choice based on the
repeatedly consulted development sets.

### Optional deliberate deviation

A teammate could choose Deep D3QN seed 42 only by explicitly declaring a
methodology deviation before touching the final holdout. Such a decision would
prioritize the best observed development result:

- mean reward `265.0437`;
- solved 143/150 (`95.33%`);
- no negative episodes;
- three timeouts.

The scientific risks are:

- the exact seed-44 replication failed decisively;
- performance is strongly training-seed-sensitive;
- choosing the best of Deep42 and Deep44 after seeing both is post-hoc
  selection;
- the result has weaker cross-training-seed generalization evidence than
  Vanilla Configuration A;
- it violates the declared no-adaptive-choice rule.

Deep42 is **not** the default recommendation. If selected, the report must
describe it as a deliberate protocol deviation, not as the outcome of the
predeclared rule.

Complete this decision record before creating a frozen-candidate directory:

```text
Selected final candidate:
Checkpoint path:
Source snapshot path:
Algorithm:
Selection rationale:
Whether this follows the predeclared rule:
Any declared methodology deviation:
Decision date:
Responsible teammate:
```

## 10. External team result

Unverified external context reports:

- D3QN mean reward approximately 278;
- solved rate 100%;
- standard deviation 17;
- “stability score” 258.

No recipe, code, training configuration, test episode count, evaluation seeds,
environment/version details, or stability-score formula is available. These
numbers are not directly comparable with this project's deterministic
development benchmarks and must not override the project's evidence or stopping
rule.

## 11. Remaining work

### A. Record final candidate decision

- [ ] Fill every field in the Section 9 decision record.
- [ ] Have the responsible teammate date and approve it.
- [ ] Record whether the choice follows the predeclared A44 rule.
- [ ] Do not inspect or use final-holdout seeds before this record is complete.

### B. Freeze the candidate

Create a new, uniquely timestamped, non-overwriting final-candidate directory
outside the repository and outside all existing run directories. Never mutate
the source run. Record both the packaged repository-relative origin path and the
immutable original provenance fields in its manifest. Copy every required item
from **one selected run only**:

- the selected `weights.pth`;
- the complete selected `source_snapshot/`;
- `resolved_config.json`;
- `training_metrics.json`;
- `source_branch.txt`, `source_commit.txt`, and `source_status.txt`;
- `experiment_manifest.txt` and `run_status.json`;
- selected `benchmark_a.json`, `benchmark_b.json`, and
  `combined_summary.txt`;
- the completed candidate decision record.

Do not mix files from different runs. Do not use the current workspace source
in place of the archived snapshot.

Create an immutable candidate manifest containing:

- candidate identifier and creation timestamp;
- exact originating run path;
- algorithm and architecture;
- training seed and complete effective configuration;
- source branch and source commit;
- relative path, byte size, and SHA-256 for every frozen payload file;
- the reserved final-holdout range;
- the decision-record text or its exact relative path;
- an explicit statement that no holdout result existed at freeze time.

After the manifest is finalized, record the manifest's own SHA-256 in the
repository decision/submission record. Verify source and frozen-copy hashes
match, then make the frozen payload read-only. This standard “payload hashes in
the manifest; manifest hash in the external decision record” avoids a circular
self-hash while providing a trust root.

### C. Final holdout

Only after A and B are complete:

1. Create a separate, new, non-overwriting final-evaluation output directory.
   Do not write the holdout JSON, log, or bytecode into the frozen candidate or
   original archived run.
2. Re-verify the frozen manifest and candidate hashes immediately before
   evaluation.
3. Use `/root/venvs/lunar-lander/bin/python`, with Python bytecode writing
   disabled, and execute the selected archived `source_snapshot/test.py`.
4. Run exactly 100 non-rendered greedy episodes with base seed 10000, yielding
   seeds 10000–10099, and the selected archived `weights.pth`.
5. Use the candidate's correct architecture/mode:
   - A44's archived evaluator predates the `--algorithm` option and directly
     constructs the standard Vanilla DQN. For A44, omit an unsupported
     algorithm flag and record `algorithm: vanilla` in the freeze and execution
     records.
   - If the deliberate Deep42 deviation is chosen, its archived evaluator
     requires `--algorithm deep_d3qn`.
6. Record the exact command, UTC execution timestamp, interpreter path and
   version, candidate-manifest hash, checkpoint hash, source hashes, output JSON
   and log paths, and exit status.
7. Archive the output and immediately mark the holdout as consumed.

Do not retrain, reselect, or rerun because of the score. A rerun is allowed only
after a documented technical invalidation—such as failure before any valid
episodes were produced or proven input corruption—and must use identical
candidate bytes, source bytes, seeds, interpreter, and arguments. Preserve the
invalidated output and incident record rather than deleting them.

No final-holdout command is provided in this handoff because the candidate
decision and immutable freeze must happen first.

### D. Final analysis

From the single valid holdout JSON, calculate and report:

- mean and median reward;
- population and sample standard deviation, clearly labeled;
- solved count and rate at reward `>= 200`;
- negative count and rate at reward `< 0`;
- timeout count using the documented length-1000 inference;
- mean episode length;
- minimum and maximum reward;
- relevant quantiles, with the chosen method stated (for example 5th, 25th,
  75th, and 95th percentiles);
- maximum same-side-engine streak;
- Benchmark A, Benchmark B, and holdout comparisons clearly labeled as
  development versus final evaluation.

Do not call a custom metric “stability score” unless the report explicitly
defines its formula, inputs, and interpretation.

### E. Report and submission

The final report should cover:

- the problem and `LunarLander-v2` environment;
- the from-scratch DQN implementation;
- replay, epsilon-greedy behavior, Bellman targets, and target network;
- deterministic seeding and evaluation protocol;
- all three architectures and their parameter counts;
- training, validation, and checkpoint selection;
- the experiment matrix and controlled ablations;
- training-seed sensitivity and protocol-sensitive historical evidence;
- final-candidate rationale and any declared deviation;
- the one-time final-holdout results;
- limitations and future work;
- exact reproducibility instructions.

Prepare the submission package with the required source files, frozen final
weights, final evaluation JSON/log, plots, result tables, README, report, and
dependency/version information. Verify course naming and packaging requirements
against the specification immediately before submission.

## 12. Recommended next commands

These commands are for the teammate to run manually in WSL. They are not final
holdout commands.

### Repository and environment status

```bash
cd /path/to/cloned/Lunar-Lander
REPO_ROOT="$(pwd -P)"
source /root/venvs/lunar-lander/bin/activate
git status --short
git branch --show-current
git log -1 --oneline
```

Do not proceed to freezing unless the branch is
`experiment/deterministic-vanilla-search`, the expected experiment source
commits are present in the archives, and any current repository changes are
understood.

### Inspect A44 read-only

```bash
A44_RUN="$REPO_ROOT/runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z"
ls -la "$A44_RUN"
cat "$A44_RUN/combined_summary.txt"
cat "$A44_RUN/source_branch.txt"
cat "$A44_RUN/source_commit.txt"
sed -n '1,220p' "$A44_RUN/resolved_config.json"
grep -nE '"status"|"phase"|"best_val_mean_reward"|"best_val_solved_rate"|"best_val_episode"' "$A44_RUN/run_status.json" "$A44_RUN/training_metrics.json"
```

### Inspect Deep D3QN seed 42 read-only

```bash
DEEP42_RUN="$REPO_ROOT/runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z"
ls -la "$DEEP42_RUN"
cat "$DEEP42_RUN/combined_summary.txt"
cat "$DEEP42_RUN/source_branch.txt"
cat "$DEEP42_RUN/source_commit.txt"
sed -n '1,260p' "$DEEP42_RUN/resolved_config.json"
grep -nE '"status"|"phase"|"best_val_mean_reward"|"best_val_solved_rate"|"best_val_episode"' "$DEEP42_RUN/run_status.json" "$DEEP42_RUN/training_metrics.json"
```

### Inspect Deep D3QN seed 44 read-only

```bash
DEEP44_RUN="$REPO_ROOT/runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z"
ls -la "$DEEP44_RUN"
cat "$DEEP44_RUN/combined_summary.txt"
cat "$DEEP44_RUN/source_branch.txt"
cat "$DEEP44_RUN/source_commit.txt"
sed -n '1,260p' "$DEEP44_RUN/resolved_config.json"
grep -nE '"status"|"phase"|"best_val_mean_reward"|"best_val_solved_rate"|"best_val_episode"' "$DEEP44_RUN/run_status.json" "$DEEP44_RUN/training_metrics.json"
```

Do not run the final holdout until the decision record is complete and the
selected candidate is frozen and hash-verified.

## 13. Known risks and unresolved issues

- **Deep D3QN seed sensitivity:** seed 42 was exceptional, while its exact
  seed-44 replication regressed sharply in reward, solved rate, failures,
  length, timeouts, and side-engine streaks.
- **A44 behavioral caveat:** A44's combined maximum same-side-engine streak was
  116. This did not violate its predeclared fallback rule and is far less severe
  than the 491–502-step pathologies, but it should not be omitted from behavioral
  reporting.
- **Development-set reuse:** Benchmark A/B were repeatedly consulted during the
  search, so reported development performance is selection-biased. This is why
  the untouched holdout and the no-reselection rule matter.
- **Weights do not encode target strategy:** a raw state dictionary contains
  learned parameters, not a label saying whether Vanilla or Double targets
  produced them.
- **Shared checkpoint schemas:** Vanilla and Double DQN use the same standard
  network schema. Direct Dueling and direct D3QN likewise share a schema. A
  checkpoint can therefore load while its training semantics are misidentified.
- **Metadata is authoritative:** use manifests, resolved configurations,
  training metrics, source provenance, and run status together. Do not infer the
  algorithm from checkpoint shape or filename alone.
- **Snapshot/checkpoint coupling:** archived weights must be evaluated with the
  same run's archived source snapshot. Current workspace source is not a
  substitute.
- **A44 evaluator CLI age:** the A44 archived `test.py` has no `--algorithm`
  option and encodes Vanilla directly. Supplying a newer CLI flag to that
  snapshot would be an invocation error.
- **Historical provenance:** older manual archives are incomplete or duplicated,
  and the seed-42 target-2000 directory is contaminated by a later run. They are
  not candidate-quality packages.
- **Packaged-log tracking:** the copied runner and per-run logs are present in
  this audited workspace, but `.gitignore` excludes `*.log`; their inclusion in
  a fresh clone must be verified after the handoff commit.
- **Package integrity:** no package-wide checksum manifest covers every copied
  file. Modern per-run source hashes remain available in their status and
  provenance records.
- **Double42 metadata caveat:** its older runner invocation evaluated a standard
  DQN checkpoint without an explicit Double algorithm label. Greedy inference
  is numerically unaffected because Vanilla and Double share the same network
  and target strategy is training-only, but the benchmark report alone does not
  prove its training semantics.
- **Termination/truncation:** `game.py` returns
  `done = terminated or truncated`. Replay therefore treats time-limit
  truncation as terminal, and diagnostics infer a timeout from episode length
  1000 rather than a separate truncation flag.
- **Determinism scope:** process/environment streams are controlled, but PyTorch
  deterministic algorithms are not explicitly enforced. Training environment
  seed ranges for adjacent training seeds also overlap heavily, although model,
  exploration, and replay RNG states differ.
- **Stale general documentation/defaults:** the README does not describe all
  added algorithm modes, and current no-argument training defaults reflect an
  earlier experiment. Archived manifests and snapshots take precedence.
- **Environment-version record:** Gymnasium is pinned in the repository, but
  exact PyTorch `2.13.0+cu130` is an operationally recorded value rather than an
  exact version embedded in run artifacts. Capture it in the freeze/holdout
  record.
- **External result:** the external “stability score” has no definition and its
  reported metrics have no comparable protocol.
- **Final holdout:** it has not been executed. Absence of a final result is
  expected and must remain so until the candidate is frozen.

## 14. Final handoff checklist

- [ ] Repository pushed
- [ ] Clean working tree confirmed
- [ ] Handoff documentation commit recorded
- [ ] Final candidate explicitly selected
- [ ] Decision record completed and dated
- [ ] Candidate frozen in a new non-overwriting directory
- [ ] All payload hashes and manifest hash verified
- [ ] Final holdout executed exactly once
- [ ] Final output JSON, log, command, timestamp, hashes, and exit status archived
- [ ] Holdout analyzed without reopening candidate selection
- [ ] Report completed
- [ ] Submission package checked against the specification

The project is technically complete through model development. The remaining
work is final-governance, final evaluation, documentation, and submission—not
additional model search.
