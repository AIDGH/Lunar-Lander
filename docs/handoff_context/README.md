# Handoff context documents

This directory preserves earlier project context for historical reference and
for continuing the work in another assistant/chat. These files are not equally
current.

## Files

- [`Lunar_Lander_Experiment_Review_Input.md`](Lunar_Lander_Experiment_Review_Input.md)
  is the historical experiment-review input and artifact context assembled
  during the deterministic Vanilla search. It includes original-machine paths
  and predates the final Dueling/D3QN suites.

- [`Lunar_Lander_Next_Chat_Starter_FA.txt`](Lunar_Lander_Next_Chat_Starter_FA.txt)
  is Persian continuation context intended to initialize another
  assistant/chat. Its proposed next steps and absolute paths are historical.

- [`Lunar_Lander_Project_Handoff_FA.md`](Lunar_Lander_Project_Handoff_FA.md)
  is an earlier Persian project handoff. It documents an earlier point in the
  search and does not include the complete deterministic experiment history.

- [`PROJECT_HANDOFF.md`](../../PROJECT_HANDOFF.md) at the repository root is the
  current authoritative technical and experimental handoff, including the
  stopping rule, candidate-selection decision, freeze procedure, and final
  holdout governance.

- [`RUNS_INDEX.md`](../../RUNS_INDEX.md) at the repository root is the current
  authoritative index of the packaged `runs/` archive and its concrete
  artifacts.

## Precedence and paths

If an older context document conflicts with `PROJECT_HANDOFF.md` or
`RUNS_INDEX.md`, the two current root documents take precedence. In particular,
older suggestions to continue target-interval experiments or other model search
are superseded by the declared stopping rule.

Absolute `/mnt/e/uni/ai/project/...` paths in the copied documents record the
original workstation. After cloning, use repository-relative paths such as
`runs/...` and the concrete links in `RUNS_INDEX.md`.
