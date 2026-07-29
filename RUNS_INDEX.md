# Packaged LunarLander Runs Index

This is the authoritative artifact index for the repository-relative
[`runs/`](runs/) archive. It covers **all 18 top-level entries** currently
packaged there:

- 4 complete experiment suites containing 6 child runs;
- 10 individual historical run directories;
- 4 standalone runner logs.

Benchmark A (seeds 1234–1283) and Benchmark B (seeds 5000–5099) are development
sets. Final-holdout seeds 10000–10099 remain unused and are not represented by a
result artifact.

## Candidate status

- **Protocol-consistent recommended final candidate:** Vanilla Configuration A,
  training seed 44 (A44), at
  [`runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/`](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/).
- **Strongest observed but non-replicated development checkpoint:** Deep D3QN
  seed 42, at
  [`runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/`](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/).
- Deep D3QN seed 44 failed the predeclared replication gate. Under the declared
  rule, that failure retains A44. See
  [`PROJECT_HANDOFF.md`](PROJECT_HANDOFF.md) for the complete decision and
  stopping rule.

## Complete top-level inventory

“No formal status” means the legacy directory predates `run_status.json`; it
does not mean that a modern runner reported failure.

| Repository-relative top-level path | Type | Family / seed | Protocol | Status | Most important result or relevance |
|---|---|---|---|---|---|
| [`runs/deep-d3qn-rescue-20260729-023441.log`](runs/deep-d3qn-rescue-20260729-023441.log) | standalone runner log | Deep D3QN / 42 | deterministic harness v1 | ends `completed` | Console transcript for the Deep42 rescue suite |
| [`runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/`](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/) | complete experiment suite | Deep D3QN / 42 | deterministic harness v1 | completed; child succeeded | Mean 265.0437; solved 95.33%; low 0%; length 246.90; 3 timeouts |
| [`runs/deep-d3qn-seed44-replication-20260729-025223.log`](runs/deep-d3qn-seed44-replication-20260729-025223.log) | standalone runner log | Deep D3QN / 44 | deterministic harness v1 | ends `completed` | Console transcript for the failed Deep44 replication gate |
| [`runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/`](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/) | complete experiment suite | Deep D3QN / 44 | deterministic harness v1 | completed; child succeeded | Mean 208.9290; solved 74.67%; low 2.67%; length 341.68; 11 timeouts |
| [`runs/double-dqn-buffer50k-seed42-20260726-185530/`](runs/double-dqn-buffer50k-seed42-20260726-185530/) | individual historical run | Double DQN / 42; “50k” disputed | historical, protocol-incomparable | no formal status | Mean 186.7352; solved 62.67%; low 4.67%; length 281.99; 9 timeouts; source contradicts 50k filename |
| [`runs/double-dqn-seed42-20260726-182745/`](runs/double-dqn-seed42-20260726-182745/) | individual historical run | Double DQN / 42 | historical, protocol-incomparable | no formal status | Mean 227.4591; solved 81.33%; low 4%; length 312.53; 11 timeouts |
| [`runs/dueling-d3qn-runner-20260729-015305.log`](runs/dueling-d3qn-runner-20260729-015305.log) | standalone runner log | direct Dueling DQN and D3QN / 42 | deterministic harness v1 | ends `completed` | Console transcript for the two-run direct-head suite |
| [`runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/) | complete experiment suite | direct Dueling DQN and D3QN / 42 | deterministic harness v1 | completed; both children succeeded | Dueling mean 224.1384; direct D3QN mean 208.2221; both rejected |
| [`runs/dueling-dqn-seed42-20260726-191220/`](runs/dueling-dqn-seed42-20260726-191220/) | individual historical run | historical direct-head Dueling DQN / 42 | historical, protocol-incomparable | no formal status | Mean 221.7734; solved 74.67%; low 2%; length 319.11; 16 timeouts |
| [`runs/next-batch-runner-20260729-004749.log`](runs/next-batch-runner-20260729-004749.log) | standalone runner log | Double DQN 42 and Vanilla A44 | deterministic harness v1 | ends `completed` | Console transcript for the Double42/A44 suite |
| [`runs/next-batch-suite-20260728T211749605393Z/`](runs/next-batch-suite-20260728T211749605393Z/) | complete experiment suite | Double DQN 42 and Vanilla A44 | deterministic harness v1 | completed; both children succeeded | Contains the recommended A44 checkpoint and deterministic Double42 screen |
| [`runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/`](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/) | individual historical run | Vanilla Configuration A / 43 | deterministic manual harness | artifacts present; no formal status | Mean 233.94; solved 86%; low 0.67%; length 311.65; 3 timeouts |
| [`runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/`](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/) | individual historical run | Vanilla target-2000 B / 43 | deterministic manual harness | artifacts present; no formal status | Mean 225.96; solved 78.67%; low 2.67%; length 350.13; 15 timeouts |
| [`runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/`](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/) | individual historical run | Vanilla LR `1e-3` / 42 | deterministic manual harness | artifacts present; dirty source status | Mean 170.47; solved 51.33%; low 9.33%; length 335.84; 27 timeouts |
| [`runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/`](runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/) | individual historical run | Vanilla epsilon decay `0.997` / 42 | deterministic manual harness | artifacts present; no formal status | Mean 203.70; solved 69.33%; low 0.67%; length 252.56; 7 timeouts |
| [`runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/`](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/) | individual historical run | Vanilla Configuration A / 42 | deterministic manual harness | incomplete modern provenance; no formal status | Mean 230.1198; solved 77.33%; low 0%; length 244.59; 9 timeouts |
| [`runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/`](runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/) | individual historical run | Vanilla target-2000 B / 42 | deterministic manual harness | directory contaminated by later LR-`1e-3` run | Target-2000 evaluation mean 235.79; solved 86.67%; low 5.33%; length 324.17; 11 timeouts |
| [`runs/vanilla-lr5e-4-seed42-20260726-193019/`](runs/vanilla-lr5e-4-seed42-20260726-193019/) | individual historical run | Vanilla LR `5e-4` / 42 | historical, nondeterministic and incomparable | no formal status | Mean 240.3599; solved 80.67%; low 0%; length 333.03; 14 timeouts |

## Complete deterministic suites

All six child runs below used 1000 episodes, learning rate `0.0005`, target
interval 1000 learning/optimizer updates, epsilon `1.0` to `0.01` with decay
`0.995` per episode, replay capacity 10,000, batch size 64, and gamma `0.99`.
Every suite has a complete `suite_summary.md`, and every child has all expected
modern run artifacts.

### Next-batch suite: Double42 and Vanilla A44

Suite: [`runs/next-batch-suite-20260728T211749605393Z/`](runs/next-batch-suite-20260728T211749605393Z/)  
Summary: [`suite_summary.md`](runs/next-batch-suite-20260728T211749605393Z/suite_summary.md)  
Status/provenance: completed, branch `experiment/deterministic-vanilla-search`,
commit `d286e4be15f681d790ae35f611ab63359f553f7b`.

#### Deterministic Double DQN seed 42

Combined result: mean `236.6064`; solved 126/150 (`84%`); low 3/150
(`2%`); mean length `310.76`; 7 timeouts; maximum side streak L=65, R=502.
This run improved primary metrics over A42 but failed its reliability,
efficiency, and behavioral screen.

Artifacts:
[run status](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/run_status.json),
[combined summary](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/combined_summary.txt),
[weights](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/weights.pth),
[training metrics](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/training_metrics.json),
[Benchmark A](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/benchmark_a.json),
[Benchmark B](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/benchmark_b.json),
[source snapshot](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/source_snapshot/)
([`train.py`](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/source_snapshot/train.py),
[`test.py`](runs/next-batch-suite-20260728T211749605393Z/deterministic-double-dqn-seed42-20260728T211749605393Z/source_snapshot/test.py)).

#### Vanilla Configuration A seed 44 — critical final-candidate run

Combined result: mean `237.9290`; solved 134/150 (`89.33%`); low 0/150;
mean length `283.11`; 1 timeout; maximum side streak L=116, R=30. This is
the protocol-consistent recommended final candidate.

Artifacts:
[run status](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/run_status.json),
[combined summary](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/combined_summary.txt),
[weights](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/weights.pth),
[training metrics](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/training_metrics.json),
[Benchmark A](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/benchmark_a.json),
[Benchmark B](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/benchmark_b.json),
[source snapshot](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/source_snapshot/)
([`train.py`](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/source_snapshot/train.py),
[`test.py`](runs/next-batch-suite-20260728T211749605393Z/deterministic-vanilla-A-seed44-20260728T211749605393Z/source_snapshot/test.py)).

### Direct-head Dueling/D3QN seed-42 suite

Suite: [`runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/)  
Summary: [`suite_summary.md`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/suite_summary.md)  
Status/provenance: completed, commit
`d40997c6b974141b8ce9c915af5503711a55e882`.

#### Direct-head Dueling DQN seed 42

Combined result: mean `224.1384`; solved 112/150 (`74.67%`); low 3/150
(`2%`); mean length `317.17`; 15 timeouts; maximum side streak L=25, R=58.

Artifacts:
[run status](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/run_status.json),
[combined summary](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/combined_summary.txt),
[weights](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/weights.pth),
[training metrics](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/training_metrics.json),
[Benchmark A](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/benchmark_a.json),
[Benchmark B](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/benchmark_b.json),
[source snapshot](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/source_snapshot/)
([`train.py`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/source_snapshot/train.py),
[`test.py`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-dueling-dqn-seed42-20260728T222305935637Z/source_snapshot/test.py)).

#### Direct-head D3QN seed 42

Combined result: mean `208.2221`; solved 108/150 (`72%`); low 1/150
(`0.67%`); mean length `269.29`; 8 timeouts; maximum side streak L=80,
R=491.

Artifacts:
[run status](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/run_status.json),
[combined summary](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/combined_summary.txt),
[weights](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/weights.pth),
[training metrics](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/training_metrics.json),
[Benchmark A](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/benchmark_a.json),
[Benchmark B](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/benchmark_b.json),
[source snapshot](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/source_snapshot/)
([`train.py`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/source_snapshot/train.py),
[`test.py`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/deterministic-d3qn-seed42-20260728T222305935637Z/source_snapshot/test.py)).

### Deep D3QN seed-42 rescue suite

Suite: [`runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/`](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/)  
Summary: [`suite_summary.md`](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/suite_summary.md)  
Status/provenance: completed, commit
`8ada1525507738fd2e9460a86e359b8a09c78457`.

Combined result: mean `265.0437`; solved 143/150 (`95.33%`); low 0/150;
mean length `246.90`; 3 timeouts; maximum side streak L=23, R=28. This is
the strongest observed development checkpoint, but one seed could only earn a
replication and could not replace A44.

Artifacts:
[run status](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/run_status.json),
[combined summary](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/combined_summary.txt),
[weights](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/weights.pth),
[training metrics](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/training_metrics.json),
[Benchmark A](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/benchmark_a.json),
[Benchmark B](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/benchmark_b.json),
[source snapshot](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/source_snapshot/)
([`train.py`](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/source_snapshot/train.py),
[`test.py`](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/deterministic-deep-d3qn-seed42-20260728T230445902051Z/source_snapshot/test.py)).

### Deep D3QN seed-44 replication suite

Suite: [`runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/`](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/)  
Summary: [`suite_summary.md`](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/suite_summary.md)  
Status/provenance: completed, commit
`133b7c315f64eda25f798ec2cfbbec319041fe62`.

Combined result: mean `208.9290`; solved 112/150 (`74.67%`); low 4/150
(`2.67%`); mean length `341.68`; 11 timeouts; maximum side streak L=97,
R=161. The exact replication failed the declared gate and therefore retained
A44.

Artifacts:
[run status](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/run_status.json),
[combined summary](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/combined_summary.txt),
[weights](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/weights.pth),
[training metrics](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/training_metrics.json),
[Benchmark A](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/benchmark_a.json),
[Benchmark B](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/benchmark_b.json),
[source snapshot](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/source_snapshot/)
([`train.py`](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/source_snapshot/train.py),
[`test.py`](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/deterministic-deep-d3qn-seed44-20260728T232223819431Z/source_snapshot/test.py)).

## Individual historical run directories

These ten entries predate the finite runner. The first four use the older
nondeterministic training protocol and are not direct comparisons with the
deterministic harness. The later six use the corrected deterministic seed
scheme but lack some or all modern suite-level status/provenance files.

### Historical Double DQN seed 42, replay nominally 10k

Path: `runs/double-dqn-seed42-20260726-182745/`  
Purpose: exploratory Double-target comparison under the older protocol.  
Result: mean `227.4591`; solved 122/150 (`81.33%`); low 6/150 (`4%`);
mean length `312.53`; 11 timeouts.

Useful files:
[training metrics](runs/double-dqn-seed42-20260726-182745/training_metrics_double_dqn_seed42.json),
[Benchmark A](runs/double-dqn-seed42-20260726-182745/double_dqn_benchmark_a_1234_1283.json),
[Benchmark B](runs/double-dqn-seed42-20260726-182745/double_dqn_benchmark_b_5000_5099.json),
[training log](runs/double-dqn-seed42-20260726-182745/training_run_double_dqn_seed42.log),
[weights](runs/double-dqn-seed42-20260726-182745/weights_double_dqn_seed42.pth),
and archived [`agent.py`](runs/double-dqn-seed42-20260726-182745/agent.py) /
[`train.py`](runs/double-dqn-seed42-20260726-182745/train.py).

### Historical directory labeled Double DQN replay 50k, seed 42

Path: `runs/double-dqn-buffer50k-seed42-20260726-185530/`  
Purpose: intended replay-capacity comparison, but **not valid 50k evidence**.
The archived `agent.py` default is 10,000 and `train.py` passes no replay
override; only filenames assert 50k.  
Result: mean `186.7352`; solved 94/150 (`62.67%`); low 7/150 (`4.67%`);
mean length `281.99`; 9 timeouts.

Useful files:
[training metrics](runs/double-dqn-buffer50k-seed42-20260726-185530/training_metrics_double_dqn_buffer50k_seed42.json),
[Benchmark A](runs/double-dqn-buffer50k-seed42-20260726-185530/double_dqn_buffer50k_benchmark_a.json),
[Benchmark B](runs/double-dqn-buffer50k-seed42-20260726-185530/double_dqn_buffer50k_benchmark_b.json),
[training log](runs/double-dqn-buffer50k-seed42-20260726-185530/training_run_double_dqn_buffer50k_seed42.log),
and the contradictory archived
[`agent.py`](runs/double-dqn-buffer50k-seed42-20260726-185530/agent.py) /
[`train.py`](runs/double-dqn-buffer50k-seed42-20260726-185530/train.py).

### Historical direct-head Dueling DQN seed 42

Path: `runs/dueling-dqn-seed42-20260726-191220/`  
Purpose: exploratory Dueling architecture comparison under the older protocol.  
Result: mean `221.7734`; solved 112/150 (`74.67%`); low 3/150 (`2%`);
mean length `319.11`; 16 timeouts.

Useful files:
[training metrics](runs/dueling-dqn-seed42-20260726-191220/training_metrics_dueling_dqn_seed42.json),
[Benchmark A](runs/dueling-dqn-seed42-20260726-191220/dueling_dqn_benchmark_a_1234_1283.json),
[Benchmark B](runs/dueling-dqn-seed42-20260726-191220/dueling_dqn_benchmark_b_5000_5099.json),
[training log](runs/dueling-dqn-seed42-20260726-191220/training_run_dueling_dqn_seed42.log),
[weights](runs/dueling-dqn-seed42-20260726-191220/weights_dueling_dqn_seed42.pth),
and archived [`model.py`](runs/dueling-dqn-seed42-20260726-191220/model.py).

### Historical nondeterministic Vanilla LR `5e-4`, seed 42

Path: `runs/vanilla-lr5e-4-seed42-20260726-193019/`  
Purpose: initial lower-learning-rate exploration; not paired with corrected
deterministic runs.  
Result: mean `240.3599`; solved 121/150 (`80.67%`); low 0; mean length
`333.03`; 14 timeouts.

Useful files:
[training metrics](runs/vanilla-lr5e-4-seed42-20260726-193019/training_metrics_vanilla_lr5e-4_seed42.json),
[Benchmark A](runs/vanilla-lr5e-4-seed42-20260726-193019/vanilla_lr5e-4_benchmark_a_1234_1283.json),
[Benchmark B](runs/vanilla-lr5e-4-seed42-20260726-193019/vanilla_lr5e-4_benchmark_b_5000_5099.json),
[training log](runs/vanilla-lr5e-4-seed42-20260726-193019/training_run_vanilla_lr5e-4_seed42.log),
and [weights](runs/vanilla-lr5e-4-seed42-20260726-193019/weights_vanilla_lr5e-4_seed42.pth).

### Deterministic Vanilla Configuration A seed 42

Path: `runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/`  
Purpose: corrected deterministic A42 control.  
Result: mean `230.1198`; solved 116/150 (`77.33%`); low 0; mean length
`244.59`; 9 timeouts.  
Limitation: no manifest, `source_status.txt`, source snapshot, formal
`run_status.json`, or combined summary.

Useful files:
[training metrics](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/training_metrics.json),
[Benchmark A](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/control_benchmark_a.json),
[Benchmark B](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/control_benchmark_b.json),
[training log](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/training_control.log),
[weights](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/weights.pth),
[source branch](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/source_branch.txt),
and [source commit](runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/source_commit.txt).

### Deterministic Vanilla target interval 2000, seed 42

Path: `runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/`  
Purpose: paired target-interval experiment B42.  
Target-2000 result: mean `235.79`; solved 130/150 (`86.67%`); low 8/150
(`5.33%`); mean length `324.17`; 11 timeouts.  
Limitation: an unrelated LR-`1e-3`, target-1000 execution later overwrote the
generic manifest, training metrics, plot, and `weights.pth`. Do not select or
evaluate that checkpoint as B42.

Authoritative target-2000 evidence:
[combined summary](runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/combined_summary.txt),
[Benchmark A](runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/target2000_benchmark_a.json),
[Benchmark B](runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/target2000_benchmark_b.json),
[target-2000 training log](runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/training_target2000.log),
and archived
[`source_snapshot/train.py`](runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/source_snapshot/train.py).

### Deterministic Vanilla LR `1e-3`, target 1000, seed 42

Path: `runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/`  
Purpose: deterministic learning-rate comparison.  
Result: mean `170.47`; solved 77/150 (`51.33%`); low 14/150 (`9.33%`);
mean length `335.84`; 27 timeouts.  
Limitation: `source_status.txt` records a modified `train.py`, so provenance is
not clean by modern-runner standards.

Useful files:
[manifest](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/experiment_manifest.txt),
[combined summary](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/combined_summary.txt),
[training metrics](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/training_metrics.json),
[Benchmark A](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/lr1e-3_benchmark_a.json),
[Benchmark B](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/lr1e-3_benchmark_b.json),
[source status](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/source_status.txt),
and [`source_snapshot/train.py`](runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/source_snapshot/train.py).

### Deterministic Vanilla epsilon decay `0.997`, seed 42

Path: `runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/`  
Purpose: isolate slower epsilon decay at 1000 episodes.  
Result: mean `203.70`; solved 104/150 (`69.33%`); low 1/150 (`0.67%`);
mean length `252.56`; 7 timeouts. No completed 1500-episode artifact exists.

Useful files:
[manifest](runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/experiment_manifest.txt),
[combined summary](runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/combined_summary.txt),
[training metrics](runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/training_metrics.json),
[Benchmark A](runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/eps997_benchmark_a.json),
[Benchmark B](runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/eps997_benchmark_b.json),
and [`source_snapshot/train.py`](runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/source_snapshot/train.py).

### Deterministic Vanilla Configuration A seed 43

Path: `runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/`  
Purpose: second Configuration A training-seed replication.  
Result: mean `233.94`; solved 129/150 (`86%`); low 1/150 (`0.67%`);
mean length `311.65`; 3 timeouts.

Useful files:
[manifest](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/experiment_manifest.txt),
[combined summary](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/combined_summary.txt),
[training metrics](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/training_metrics.json),
[Benchmark A](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/A_seed43_benchmark_a.json),
[Benchmark B](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/A_seed43_benchmark_b.json),
[weights](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/weights.pth),
and [`source_snapshot/train.py`](runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/source_snapshot/train.py).

### Deterministic Vanilla target interval 2000, seed 43

Path: `runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/`  
Purpose: B43, completing the two-seed target-interval pairing.  
Result: mean `225.96`; solved 118/150 (`78.67%`); low 4/150 (`2.67%`);
mean length `350.13`; 15 timeouts. It reproduced the reliability, length,
timeout, and side-engine harms of target interval 2000.

Useful files:
[manifest](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/experiment_manifest.txt),
[combined summary](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/combined_summary.txt),
[training metrics](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/training_metrics.json),
[Benchmark A](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/B_seed43_benchmark_a.json),
[Benchmark B](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/B_seed43_benchmark_b.json),
[weights](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/weights.pth),
and [`source_snapshot/train.py`](runs/vanilla-deterministic-B-lr5e-4-target2000-eps995-seed43-20260727-192544/source_snapshot/train.py).

## Standalone runner logs

These are top-level console captures. The suite artifacts, not the logs alone,
are authoritative for configuration and results.

| Log | Family / seed(s) | Status | Paired suite |
|---|---|---|---|
| [`runs/next-batch-runner-20260729-004749.log`](runs/next-batch-runner-20260729-004749.log) | Double DQN 42; Vanilla A44 | ends with `Suite status: completed` | [`next-batch-suite-20260728T211749605393Z`](runs/next-batch-suite-20260728T211749605393Z/suite_summary.md) |
| [`runs/dueling-d3qn-runner-20260729-015305.log`](runs/dueling-d3qn-runner-20260729-015305.log) | direct Dueling DQN 42; direct D3QN 42 | ends with `Suite status: completed` | [`dueling-d3qn-seed42-batch-suite-20260728T222305935637Z`](runs/dueling-d3qn-seed42-batch-suite-20260728T222305935637Z/suite_summary.md) |
| [`runs/deep-d3qn-rescue-20260729-023441.log`](runs/deep-d3qn-rescue-20260729-023441.log) | Deep D3QN 42 | ends with `Suite status: completed` | [`deep-d3qn-seed42-rescue-suite-20260728T230445902051Z`](runs/deep-d3qn-seed42-rescue-suite-20260728T230445902051Z/suite_summary.md) |
| [`runs/deep-d3qn-seed44-replication-20260729-025223.log`](runs/deep-d3qn-seed44-replication-20260729-025223.log) | Deep D3QN 44 | ends with `Suite status: completed` | [`deep-d3qn-seed44-replication-suite-20260728T232223819431Z`](runs/deep-d3qn-seed44-replication-suite-20260728T232223819431Z/suite_summary.md) |

## Packaging and provenance caveats

- Absolute `/mnt/e/uni/ai/project/runs/...` paths embedded in manifests, suite
  summaries, status JSON, and logs describe the original machine. Use the
  repository-relative links in this index after cloning.
- Every modern suite and child run has all expected artifacts. Empty
  `source_status.txt` files intentionally denote clean source status.
- Modern source snapshots also contain generated `__pycache__/*.pyc` extras.
  The five `.py` source files are authoritative; do not use bytecode files as
  source or provenance.
- Legacy run directories lack modern `run_status.json` and/or source snapshots
  by design. Their limitations are identified above rather than treated as
  missing modern-suite artifacts.
- The seed-42 target-2000 directory is internally contaminated, and the
  “buffer50k” directory's archived source contradicts its name. Neither is a
  candidate-quality package.
- The repository `.gitignore` excludes `*.log`; the log files are present in
  this workspace, but whether they were force-added to Git could not be checked
  without a prohibited Git command. Verify their presence after cloning.
- No package-wide checksum manifest currently covers every copied file.
- Checkpoint files were indexed by path and presence; their tensor contents were
  not loaded during this audit.
