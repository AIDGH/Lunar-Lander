# Lunar Lander Experiment Review Input

Generated: 2026-07-27T17:32:08+03:30

## Current repository state
```text
experiment/deterministic-vanilla-search
378ac9e (HEAD -> experiment/deterministic-vanilla-search) experiment: replicate vanilla configuration A with seed 43
a5859ea experiment: test epsilon decay 0.997
27d1b2e experiment: test target update interval 2000
d01c8d4 experiment: add deterministic vanilla DQN control harness
265dc8d (tag: dqn-baseline-v1, origin/main, origin/experiment/double-dqn, origin/HEAD, main, experiment/vanilla-lr5e-4, experiment/dueling-dqn, experiment/double-dqn) merge: integrate validated LunarLander DQN baseline
c1c57aa (origin/ehsan, ehsan) feat: finalize validated DQN baseline with greedy checkpoint selection
c5b1ce2 fixed agent.py and added additional prints to train.py
ecf235d test.py done
b1f5d46 train.py and model.py done
f2614cb agent.py done
c3697b5 Created project skeleton (Empty code files)
9a60a2d Revise README with detailed project overview and features
```

## Run directory inventory
```text
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/agent.py
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/double_dqn_buffer50k_benchmark_a.json
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/double_dqn_buffer50k_benchmark_a.log
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/double_dqn_buffer50k_benchmark_b.json
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/double_dqn_buffer50k_benchmark_b.log
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/game.py
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/model.py
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/requirements.txt
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/test.py
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/train.py
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/training_metrics.json
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/training_metrics_double_dqn_buffer50k_seed42.json
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/training_plot.png
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/training_plot_double_dqn_buffer50k_seed42.png
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/training_run_double_dqn_buffer50k_seed42.log
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/weights.pth
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530/weights_double_dqn_buffer50k_seed42.pth
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/agent.py
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/double_dqn_benchmark_a.log
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/double_dqn_benchmark_a_1234_1283.json
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/double_dqn_benchmark_b.log
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/double_dqn_benchmark_b_5000_5099.json
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/game.py
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/model.py
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/requirements.txt
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/test.py
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/train.py
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/training_metrics.json
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/training_metrics_double_dqn_seed42.json
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/training_plot.png
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/training_plot_double_dqn_seed42.png
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/training_run_double_dqn_seed42.log
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/weights.pth
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745/weights_double_dqn_seed42.pth
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/agent.py
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/dueling_dqn_benchmark_a.log
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/dueling_dqn_benchmark_a_1234_1283.json
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/dueling_dqn_benchmark_b.log
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/dueling_dqn_benchmark_b_5000_5099.json
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/game.py
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/model.py
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/requirements.txt
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/test.py
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/train.py
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/training_metrics.json
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/training_metrics_dueling_dqn_seed42.json
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/training_plot.png
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/training_plot_dueling_dqn_seed42.png
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/training_run_dueling_dqn_seed42.log
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/weights.pth
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220/weights_dueling_dqn_seed42.pth
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/A_seed43_benchmark_a.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/A_seed43_benchmark_a.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/A_seed43_benchmark_b.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/A_seed43_benchmark_b.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/combined_summary.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/experiment_manifest.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/source_branch.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/source_commit.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/source_status.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/training_A_seed43.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/training_metrics.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/training_plot.png
/mnt/e/uni/ai/project/runs/vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138/weights.pth
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/combined_summary.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/experiment_manifest.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/lr1e-3_benchmark_a.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/lr1e-3_benchmark_a.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/lr1e-3_benchmark_b.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/lr1e-3_benchmark_b.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/source_branch.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/source_commit.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/source_status.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/training_lr1e-3_target1000.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/training_metrics.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/training_plot.png
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049/weights.pth
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/combined_summary.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/eps997_benchmark_a.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/eps997_benchmark_a.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/eps997_benchmark_b.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/eps997_benchmark_b.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/experiment_manifest.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/source_branch.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/source_commit.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/source_status.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/training_eps997.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/training_metrics.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/training_plot.png
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205/weights.pth
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/control_benchmark_a.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/control_benchmark_a.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/control_benchmark_b.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/control_benchmark_b.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/source_branch.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/source_commit.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/training_control.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/training_metrics.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/training_plot.png
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329/weights.pth
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/combined_summary.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/experiment_manifest.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/source_branch.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/source_commit.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/source_status.txt
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/target2000_benchmark_a.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/target2000_benchmark_a.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/target2000_benchmark_b.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/target2000_benchmark_b.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/training_lr1e-3_target1000.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/training_metrics.json
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/training_plot.png
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/training_target2000.log
/mnt/e/uni/ai/project/runs/vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427/weights.pth
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/agent.py
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/game.py
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/model.py
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/requirements.txt
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/test.py
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/train.py
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/training_metrics.json
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/training_metrics_vanilla_lr5e-4_seed42.json
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/training_plot.png
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/training_plot_vanilla_lr5e-4_seed42.png
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/training_run_vanilla_lr5e-4_seed42.log
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/vanilla_lr5e-4_benchmark_a.log
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/vanilla_lr5e-4_benchmark_a_1234_1283.json
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/vanilla_lr5e-4_benchmark_b.log
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/vanilla_lr5e-4_benchmark_b_5000_5099.json
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/weights.pth
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019/weights_vanilla_lr5e-4_seed42.pth
```


## Run: double-dqn-buffer50k-seed42-20260726-185530

### Training log tail
```text
--- training_run_double_dqn_buffer50k_seed42.log ---
[Validation @ ep 800] mean=121.99 median=104.36 std=118.57 solved=30%
Episode 810, Total Reward: 11.98, Average Max Q-Value: 72.7422, Epsilon: 0.0172
Episode 820, Total Reward: -29.56, Average Max Q-Value: 73.9948, Epsilon: 0.0164
Episode 830, Total Reward: 17.08, Average Max Q-Value: 77.8534, Epsilon: 0.0156
Episode 840, Total Reward: 35.15, Average Max Q-Value: 79.3117, Epsilon: 0.0148
Episode 850, Total Reward: 40.44, Average Max Q-Value: 80.9435, Epsilon: 0.0141
[Validation @ ep 850] mean=150.36 median=143.10 std=122.72 solved=50%
Episode 860, Total Reward: 293.50, Average Max Q-Value: 81.5676, Epsilon: 0.0134
Episode 870, Total Reward: 29.04, Average Max Q-Value: 80.6830, Epsilon: 0.0128
Episode 880, Total Reward: 253.06, Average Max Q-Value: 80.8775, Epsilon: 0.0121
Episode 890, Total Reward: 272.63, Average Max Q-Value: 81.2709, Epsilon: 0.0115
Episode 900, Total Reward: 308.42, Average Max Q-Value: 82.1286, Epsilon: 0.0110
[Validation @ ep 900] mean=196.55 median=267.59 std=116.50 solved=60%
Episode 910, Total Reward: -19.14, Average Max Q-Value: 80.7923, Epsilon: 0.0104
Episode 920, Total Reward: 308.34, Average Max Q-Value: 82.3118, Epsilon: 0.0100
Episode 930, Total Reward: 25.53, Average Max Q-Value: 81.5115, Epsilon: 0.0100
Episode 940, Total Reward: 315.55, Average Max Q-Value: 84.8158, Epsilon: 0.0100
Episode 950, Total Reward: 23.91, Average Max Q-Value: 84.8965, Epsilon: 0.0100
[Validation @ ep 950] mean=71.38 median=43.91 std=80.82 solved=10%
Episode 960, Total Reward: 60.81, Average Max Q-Value: 83.9831, Epsilon: 0.0100
Episode 970, Total Reward: 32.54, Average Max Q-Value: 79.3393, Epsilon: 0.0100
Episode 980, Total Reward: 283.90, Average Max Q-Value: 79.2634, Epsilon: 0.0100
Episode 990, Total Reward: 303.99, Average Max Q-Value: 78.4960, Epsilon: 0.0100
Episode 1000, Total Reward: 255.32, Average Max Q-Value: 76.4195, Epsilon: 0.0100
[Validation @ ep 1000] mean=256.02 median=268.75 std=70.94 solved=90%  <- NEW BEST (saved)
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 81.46
Reward Variance: 19118.08
Final Moving-Avg Reward (w=50): 159.61
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- double_dqn_buffer50k_benchmark_a.log ---
  Ep  40 [    ][   ] reward=   43.40  len= 109  streak(L,R)=(3,2)
  Ep  41 [SOLVED][   ] reward=  263.37  len= 197  streak(L,R)=(10,2)
  Ep  42 [    ][   ] reward=   15.05  len= 158  streak(L,R)=(7,1)
  Ep  43 [SOLVED][   ] reward=  287.12  len= 163  streak(L,R)=(3,1)
  Ep  44 [SOLVED][   ] reward=  276.76  len= 163  streak(L,R)=(1,2)
  Ep  45 [SOLVED][   ] reward=  263.61  len= 268  streak(L,R)=(6,2)
  Ep  46 [    ][   ] reward=  166.72  len=1000  streak(L,R)=(4,4)
  Ep  47 [SOLVED][   ] reward=  284.49  len= 235  streak(L,R)=(10,7)
  Ep  48 [SOLVED][   ] reward=  281.21  len= 252  streak(L,R)=(5,10)
  Ep  49 [SOLVED][   ] reward=  289.59  len= 250  streak(L,R)=(6,18)
  Ep  50 [SOLVED][   ] reward=  288.23  len= 152  streak(L,R)=(2,3)
==============================
Diagnostic Summary
  Mean reward   : 175.97   Median: 258.07   Std: 122.21
  Min / Max     : -48.76 / 307.97
  Solved (>=200): 30/50 (60.0%)
  Low (<0)      : 5/50 (10.0%)
  Mean length   : 285.8
  Action %      : no_op=42.3%, fire_left_orientation_engine=9.9%, fire_main_engine=25.8%, fire_right_orientation_engine=22.0%
  Max side streak: L=42, R=88
  Report saved  : double_dqn_buffer50k_benchmark_a.json
==============================
--- double_dqn_buffer50k_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  295.30  len= 212  streak(L,R)=(11,2)
  Ep  91 [    ][   ] reward=  103.95  len=1000  streak(L,R)=(3,1)
  Ep  92 [    ][   ] reward=   35.30  len= 106  streak(L,R)=(1,2)
  Ep  93 [SOLVED][   ] reward=  311.77  len= 230  streak(L,R)=(6,8)
  Ep  94 [    ][   ] reward=   21.24  len= 131  streak(L,R)=(10,8)
  Ep  95 [SOLVED][   ] reward=  270.01  len= 179  streak(L,R)=(5,3)
  Ep  96 [SOLVED][   ] reward=  280.62  len= 172  streak(L,R)=(7,13)
  Ep  97 [    ][   ] reward=   16.27  len= 219  streak(L,R)=(13,4)
  Ep  98 [    ][   ] reward=   41.27  len= 108  streak(L,R)=(1,1)
  Ep  99 [SOLVED][   ] reward=  245.98  len= 170  streak(L,R)=(8,2)
  Ep 100 [SOLVED][   ] reward=  307.16  len= 178  streak(L,R)=(27,7)
==============================
Diagnostic Summary
  Mean reward   : 192.12   Median: 259.15   Std: 112.41
  Min / Max     : -2.60 / 311.77
  Solved (>=200): 64/100 (64.0%)
  Low (<0)      : 2/100 (2.0%)
  Mean length   : 280.1
  Action %      : no_op=40.4%, fire_left_orientation_engine=8.3%, fire_main_engine=27.7%, fire_right_orientation_engine=23.6%
  Max side streak: L=27, R=68
  Report saved  : double_dqn_buffer50k_benchmark_b.json
==============================
```

## Run: double-dqn-seed42-20260726-182745

### Training log tail
```text
--- training_run_double_dqn_seed42.log ---
[Validation @ ep 800] mean=120.86 median=112.53 std=151.04 solved=50%
Episode 810, Total Reward: 55.03, Average Max Q-Value: 99.7451, Epsilon: 0.0172
Episode 820, Total Reward: 32.72, Average Max Q-Value: 99.5187, Epsilon: 0.0164
Episode 830, Total Reward: 249.58, Average Max Q-Value: 98.6523, Epsilon: 0.0156
Episode 840, Total Reward: 52.75, Average Max Q-Value: 97.1544, Epsilon: 0.0148
Episode 850, Total Reward: 38.65, Average Max Q-Value: 98.7007, Epsilon: 0.0141
[Validation @ ep 850] mean=92.69 median=28.18 std=126.39 solved=30%
Episode 860, Total Reward: 34.74, Average Max Q-Value: 100.1611, Epsilon: 0.0134
Episode 870, Total Reward: 12.59, Average Max Q-Value: 99.2878, Epsilon: 0.0128
Episode 880, Total Reward: 38.07, Average Max Q-Value: 98.6391, Epsilon: 0.0121
Episode 890, Total Reward: 27.08, Average Max Q-Value: 97.8689, Epsilon: 0.0115
Episode 900, Total Reward: 22.41, Average Max Q-Value: 93.3268, Epsilon: 0.0110
[Validation @ ep 900] mean=189.47 median=272.03 std=120.97 solved=60%
Episode 910, Total Reward: 33.41, Average Max Q-Value: 91.3518, Epsilon: 0.0104
Episode 920, Total Reward: 43.57, Average Max Q-Value: 87.8243, Epsilon: 0.0100
Episode 930, Total Reward: 275.82, Average Max Q-Value: 84.2116, Epsilon: 0.0100
Episode 940, Total Reward: 247.22, Average Max Q-Value: 81.7418, Epsilon: 0.0100
Episode 950, Total Reward: 21.98, Average Max Q-Value: 80.8053, Epsilon: 0.0100
[Validation @ ep 950] mean=95.55 median=150.72 std=235.80 solved=50%
Episode 960, Total Reward: 257.11, Average Max Q-Value: 83.9573, Epsilon: 0.0100
Episode 970, Total Reward: 308.77, Average Max Q-Value: 83.5226, Epsilon: 0.0100
Episode 980, Total Reward: 268.12, Average Max Q-Value: 84.2068, Epsilon: 0.0100
Episode 990, Total Reward: 23.12, Average Max Q-Value: 85.3402, Epsilon: 0.0100
Episode 1000, Total Reward: 287.45, Average Max Q-Value: 82.3265, Epsilon: 0.0100
[Validation @ ep 1000] mean=121.61 median=56.51 std=134.78 solved=40%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 84.16
Reward Variance: 23878.41
Final Moving-Avg Reward (w=50): 149.58
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- double_dqn_benchmark_a.log ---
  Ep  40 [SOLVED][   ] reward=  260.24  len= 347  streak(L,R)=(132,3)
  Ep  41 [SOLVED][   ] reward=  260.63  len= 204  streak(L,R)=(6,2)
  Ep  42 [SOLVED][   ] reward=  250.99  len= 334  streak(L,R)=(11,3)
  Ep  43 [SOLVED][   ] reward=  278.74  len= 274  streak(L,R)=(6,2)
  Ep  44 [SOLVED][   ] reward=  241.03  len= 216  streak(L,R)=(11,33)
  Ep  45 [SOLVED][   ] reward=  261.93  len= 240  streak(L,R)=(10,5)
  Ep  46 [SOLVED][   ] reward=  286.80  len= 201  streak(L,R)=(3,5)
  Ep  47 [SOLVED][   ] reward=  284.24  len= 255  streak(L,R)=(10,15)
  Ep  48 [SOLVED][   ] reward=  261.69  len= 327  streak(L,R)=(12,7)
  Ep  49 [SOLVED][   ] reward=  281.82  len= 267  streak(L,R)=(5,8)
  Ep  50 [SOLVED][   ] reward=  275.79  len= 324  streak(L,R)=(4,2)
==============================
Diagnostic Summary
  Mean reward   : 200.70   Median: 258.22   Std: 129.15
  Min / Max     : -222.92 / 304.98
  Solved (>=200): 38/50 (76.0%)
  Low (<0)      : 4/50 (8.0%)
  Mean length   : 281.8
  Action %      : no_op=27.6%, fire_left_orientation_engine=20.2%, fire_main_engine=41.2%, fire_right_orientation_engine=10.9%
  Max side streak: L=132, R=33
  Report saved  : double_dqn_benchmark_a_1234_1283.json
==============================
--- double_dqn_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  260.25  len= 337  streak(L,R)=(12,3)
  Ep  91 [SOLVED][   ] reward=  222.13  len= 204  streak(L,R)=(30,3)
  Ep  92 [SOLVED][   ] reward=  257.57  len= 251  streak(L,R)=(52,33)
  Ep  93 [SOLVED][   ] reward=  289.56  len= 196  streak(L,R)=(19,11)
  Ep  94 [SOLVED][   ] reward=  305.28  len= 207  streak(L,R)=(14,8)
  Ep  95 [SOLVED][   ] reward=  261.12  len= 241  streak(L,R)=(7,8)
  Ep  96 [SOLVED][   ] reward=  286.68  len= 209  streak(L,R)=(4,7)
  Ep  97 [SOLVED][   ] reward=  273.70  len= 295  streak(L,R)=(26,6)
  Ep  98 [SOLVED][   ] reward=  276.39  len= 314  streak(L,R)=(16,2)
  Ep  99 [SOLVED][   ] reward=  221.10  len= 277  streak(L,R)=(86,2)
  Ep 100 [    ][   ] reward=  166.90  len=1000  streak(L,R)=(20,6)
==============================
Diagnostic Summary
  Mean reward   : 240.84   Median: 262.00   Std: 71.25
  Min / Max     : -31.30 / 308.36
  Solved (>=200): 84/100 (84.0%)
  Low (<0)      : 2/100 (2.0%)
  Mean length   : 327.9
  Action %      : no_op=23.9%, fire_left_orientation_engine=26.3%, fire_main_engine=33.0%, fire_right_orientation_engine=16.9%
  Max side streak: L=86, R=66
  Report saved  : double_dqn_benchmark_b_5000_5099.json
==============================
```

## Run: dueling-dqn-seed42-20260726-191220

### Training log tail
```text
--- training_run_dueling_dqn_seed42.log ---
[Validation @ ep 800] mean=158.72 median=121.30 std=116.21 solved=40%
Episode 810, Total Reward: 22.00, Average Max Q-Value: 88.7863, Epsilon: 0.0172
Episode 820, Total Reward: 32.94, Average Max Q-Value: 90.2349, Epsilon: 0.0164
Episode 830, Total Reward: 30.39, Average Max Q-Value: 88.8349, Epsilon: 0.0156
Episode 840, Total Reward: 31.10, Average Max Q-Value: 89.3333, Epsilon: 0.0148
Episode 850, Total Reward: 278.72, Average Max Q-Value: 89.2191, Epsilon: 0.0141
[Validation @ ep 850] mean=204.65 median=215.25 std=79.94 solved=50%
Episode 860, Total Reward: 10.35, Average Max Q-Value: 87.7879, Epsilon: 0.0134
Episode 870, Total Reward: 154.57, Average Max Q-Value: 87.8157, Epsilon: 0.0128
Episode 880, Total Reward: 279.53, Average Max Q-Value: 89.1177, Epsilon: 0.0121
Episode 890, Total Reward: -19.77, Average Max Q-Value: 89.1345, Epsilon: 0.0115
Episode 900, Total Reward: 29.23, Average Max Q-Value: 87.9303, Epsilon: 0.0110
[Validation @ ep 900] mean=67.86 median=42.76 std=77.85 solved=10%
Episode 910, Total Reward: 263.19, Average Max Q-Value: 88.4640, Epsilon: 0.0104
Episode 920, Total Reward: 222.78, Average Max Q-Value: 86.4173, Epsilon: 0.0100
Episode 930, Total Reward: 283.58, Average Max Q-Value: 83.7513, Epsilon: 0.0100
Episode 940, Total Reward: 26.62, Average Max Q-Value: 81.9131, Epsilon: 0.0100
Episode 950, Total Reward: -168.61, Average Max Q-Value: 80.5013, Epsilon: 0.0100
[Validation @ ep 950] mean=46.08 median=102.05 std=222.46 solved=30%
Episode 960, Total Reward: 255.90, Average Max Q-Value: 79.8928, Epsilon: 0.0100
Episode 970, Total Reward: 267.58, Average Max Q-Value: 80.5252, Epsilon: 0.0100
Episode 980, Total Reward: 291.12, Average Max Q-Value: 78.4932, Epsilon: 0.0100
Episode 990, Total Reward: 280.63, Average Max Q-Value: 76.5709, Epsilon: 0.0100
Episode 1000, Total Reward: 264.32, Average Max Q-Value: 74.8972, Epsilon: 0.0100
[Validation @ ep 1000] mean=101.50 median=129.32 std=151.64 solved=30%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 92.22
Reward Variance: 25453.73
Final Moving-Avg Reward (w=50): 131.07
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- dueling_dqn_benchmark_a.log ---
  Ep  40 [SOLVED][   ] reward=  258.20  len= 189  streak(L,R)=(7,3)
  Ep  41 [SOLVED][   ] reward=  257.03  len= 195  streak(L,R)=(8,8)
  Ep  42 [    ][   ] reward=   36.18  len= 159  streak(L,R)=(7,2)
  Ep  43 [SOLVED][   ] reward=  282.16  len= 178  streak(L,R)=(3,9)
  Ep  44 [SOLVED][   ] reward=  279.58  len= 160  streak(L,R)=(5,1)
  Ep  45 [SOLVED][   ] reward=  259.95  len= 221  streak(L,R)=(7,5)
  Ep  46 [SOLVED][   ] reward=  268.90  len= 236  streak(L,R)=(2,5)
  Ep  47 [    ][   ] reward=  153.98  len=1000  streak(L,R)=(29,23)
  Ep  48 [SOLVED][   ] reward=  272.71  len= 290  streak(L,R)=(27,37)
  Ep  49 [    ][   ] reward=   49.87  len= 151  streak(L,R)=(14,12)
  Ep  50 [SOLVED][   ] reward=  287.38  len= 168  streak(L,R)=(7,9)
==============================
Diagnostic Summary
  Mean reward   : 223.43   Median: 259.67   Std: 95.69
  Min / Max     : -151.56 / 317.31
  Solved (>=200): 38/50 (76.0%)
  Low (<0)      : 1/50 (2.0%)
  Mean length   : 315.1
  Action %      : no_op=21.0%, fire_left_orientation_engine=34.5%, fire_main_engine=25.1%, fire_right_orientation_engine=19.5%
  Max side streak: L=50, R=49
  Report saved  : dueling_dqn_benchmark_a_1234_1283.json
==============================
--- dueling_dqn_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  309.06  len= 184  streak(L,R)=(11,7)
  Ep  91 [    ][   ] reward=  128.97  len=1000  streak(L,R)=(29,1)
  Ep  92 [SOLVED][   ] reward=  278.39  len= 186  streak(L,R)=(4,8)
  Ep  93 [    ][   ] reward=   71.01  len= 136  streak(L,R)=(17,15)
  Ep  94 [SOLVED][   ] reward=  277.90  len= 288  streak(L,R)=(22,23)
  Ep  95 [    ][   ] reward=  131.65  len=1000  streak(L,R)=(6,4)
  Ep  96 [SOLVED][   ] reward=  231.92  len= 472  streak(L,R)=(3,8)
  Ep  97 [SOLVED][   ] reward=  278.93  len= 403  streak(L,R)=(32,7)
  Ep  98 [SOLVED][   ] reward=  281.49  len= 180  streak(L,R)=(4,9)
  Ep  99 [SOLVED][   ] reward=  246.30  len= 154  streak(L,R)=(6,3)
  Ep 100 [SOLVED][   ] reward=  298.51  len= 193  streak(L,R)=(10,13)
==============================
Diagnostic Summary
  Mean reward   : 220.95   Median: 259.81   Std: 90.09
  Min / Max     : -134.02 / 310.29
  Solved (>=200): 74/100 (74.0%)
  Low (<0)      : 2/100 (2.0%)
  Mean length   : 321.1
  Action %      : no_op=25.2%, fire_left_orientation_engine=31.3%, fire_main_engine=26.5%, fire_right_orientation_engine=17.0%
  Max side streak: L=93, R=35
  Report saved  : dueling_dqn_benchmark_b_5000_5099.json
==============================
```

## Run: vanilla-deterministic-A-lr5e-4-target1000-eps995-seed43-20260727-165138

### Source
```text
experiment/deterministic-vanilla-search
378ac9e1a47eebbc4d8e20e283acfd3217d78013
```

### Experiment manifest
Experiment: Configuration A Replication — Training Seed 43

Purpose:
Measure full training-run variance of the balanced Vanilla DQN configuration.

Algorithm: Vanilla DQN
Training seed: 43
Training episode seeds: 20043–21042
Training action-space seed: 21043
Hold-out initial environment seed: 30043
Hold-out action-space seed: 40043
Episodes: 1000

Learning rate: 5e-4
Target update frequency: 1000 optimizer updates
Replay capacity: 10000
Batch size: 64
Gamma: 0.99
Epsilon start: 1.0
Epsilon minimum: 0.01
Epsilon decay: 0.995 per episode

Paired reference:
The identical configuration trained with seed 42.

Archived A42 results:
- Combined mean reward: 230.12
- Solved: 116/150 (77.33%)
- Low below zero: 0/150
- Mean episode length: 244.57
- Timeouts: 9/150

Benchmark A:
seeds 1234–1283

Benchmark B:
seeds 5000–5099

Reserved final holdout:
seeds 10000–10099 — DO NOT RUN

Interpretation caveats:
- Changing SEED changes network initialization, exploration/replay randomness,
  and derived training-environment seeds together.
- This measures complete training-run variance rather than initialization-only variance.
- Fixed validation seeds may introduce shared checkpoint-selection bias.
- Policy-dependent episode lengths change the total number of optimizer updates.
- Timeout truncation remains treated as done.

Observed results:

Benchmark A:
- Mean reward: 238.12
- Solved: 45/50 (90.00%)
- Low below zero: 0/50
- Mean length: 320.94
- Timeouts: 1/50

Benchmark B:
- Mean reward: 231.85
- Solved: 84/100 (84.00%)
- Low below zero: 1/100 (1.00%)
- Mean length: 307.00
- Timeouts: 2/100

Combined:
- Mean reward: 233.94
- Solved: 129/150 (86.00%)
- Low below zero: 1/150 (0.67%)
- Mean length: 311.65
- Timeouts: 3/150

Comparison against Configuration A, seed 42:
- Mean reward: +3.82
- Solved rate: +8.67 percentage points
- Low rate: +0.67 percentage points
- Mean length: +67.08 steps
- Timeouts: -6

Two-training-seed aggregate for Configuration A:
- Total benchmark episodes: 300
- Mean reward: 232.03
- Solved: 245/300 (81.67%)
- Low below zero: 1/300 (0.33%)
- Mean length: 278.11
- Timeouts: 12/300 (4.00%)

Interpretation:
Configuration A remained strong on seed 43 and improved solved rate and
cross-benchmark consistency. Episode length varied substantially by training
seed, but the longer seed-43 behavior rarely reached timeout and did not show
the extreme side-engine streaks previously observed with target interval 2000.

### Combined benchmark summary
```text
Benchmark A:
  episodes     = 50
  mean reward  = 238.12
  solved       = 45/50 (90.00%)
  low          = 0/50 (0.00%)
  mean length  = 320.94
  timeouts     = 1/50

Benchmark B:
  episodes     = 100
  mean reward  = 231.85
  solved       = 84/100 (84.00%)
  low          = 1/100 (1.00%)
  mean length  = 307.00
  timeouts     = 2/100

Combined:
  mean reward  = 233.94
  solved       = 129/150 (86.00%)
  low          = 1/150 (0.67%)
  mean length  = 311.65
  timeouts     = 3/150
```

### Training log tail
```text
--- training_A_seed43.log ---
[Validation @ ep 800] mean=103.39 median=50.88 std=104.09 solved=20%
Episode 810, Total Reward: 29.26, Average Max Q-Value: 95.0177, Epsilon: 0.0172
Episode 820, Total Reward: 38.63, Average Max Q-Value: 95.1543, Epsilon: 0.0164
Episode 830, Total Reward: 35.19, Average Max Q-Value: 95.3450, Epsilon: 0.0156
Episode 840, Total Reward: 33.94, Average Max Q-Value: 94.4293, Epsilon: 0.0148
Episode 850, Total Reward: 53.90, Average Max Q-Value: 90.9603, Epsilon: 0.0141
[Validation @ ep 850] mean=72.28 median=46.43 std=56.22 solved=0%
Episode 860, Total Reward: 282.22, Average Max Q-Value: 89.6100, Epsilon: 0.0134
Episode 870, Total Reward: 4.74, Average Max Q-Value: 90.1946, Epsilon: 0.0128
Episode 880, Total Reward: 177.63, Average Max Q-Value: 94.3773, Epsilon: 0.0121
Episode 890, Total Reward: 259.05, Average Max Q-Value: 98.9794, Epsilon: 0.0115
Episode 900, Total Reward: 14.51, Average Max Q-Value: 97.5605, Epsilon: 0.0110
[Validation @ ep 900] mean=117.66 median=57.67 std=128.89 solved=30%
Episode 910, Total Reward: 41.43, Average Max Q-Value: 95.7548, Epsilon: 0.0104
Episode 920, Total Reward: 261.56, Average Max Q-Value: 94.2359, Epsilon: 0.0100
Episode 930, Total Reward: 280.07, Average Max Q-Value: 90.7235, Epsilon: 0.0100
Episode 940, Total Reward: 46.62, Average Max Q-Value: 88.2891, Epsilon: 0.0100
Episode 950, Total Reward: 232.22, Average Max Q-Value: 84.1614, Epsilon: 0.0100
[Validation @ ep 950] mean=121.42 median=132.87 std=152.10 solved=40%
Episode 960, Total Reward: 237.85, Average Max Q-Value: 80.8304, Epsilon: 0.0100
Episode 970, Total Reward: 251.37, Average Max Q-Value: 74.0585, Epsilon: 0.0100
Episode 980, Total Reward: 219.98, Average Max Q-Value: 71.3642, Epsilon: 0.0100
Episode 990, Total Reward: 240.87, Average Max Q-Value: 70.1123, Epsilon: 0.0100
Episode 1000, Total Reward: 243.49, Average Max Q-Value: 70.0926, Epsilon: 0.0100
[Validation @ ep 1000] mean=278.16 median=280.26 std=17.99 solved=100%  <- NEW BEST (saved)
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 95.48
Reward Variance: 24374.53
Final Moving-Avg Reward (w=50): 211.62
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- A_seed43_benchmark_a.log ---
Starting evaluation...
Test Episode 1: Total Reward = 56.11
Test Episode 2: Total Reward = 48.03
Test Episode 3: Total Reward = 263.46
Test Episode 4: Total Reward = 274.99
Test Episode 5: Total Reward = 244.77
==============================
Mean Evaluation Reward (over 5 episodes): 177.47
==============================
--- A_seed43_benchmark_b.log ---
  Ep  90 [    ][   ] reward=  179.54  len=1000  streak(L,R)=(13,12)
  Ep  91 [SOLVED][   ] reward=  228.75  len= 208  streak(L,R)=(3,2)
  Ep  92 [    ][   ] reward=   48.14  len= 120  streak(L,R)=(2,2)
  Ep  93 [    ][LOW] reward=  -19.17  len=  91  streak(L,R)=(6,15)
  Ep  94 [SOLVED][   ] reward=  242.35  len= 523  streak(L,R)=(3,13)
  Ep  95 [SOLVED][   ] reward=  263.56  len= 260  streak(L,R)=(7,9)
  Ep  96 [    ][   ] reward=  175.13  len=1000  streak(L,R)=(4,8)
  Ep  97 [SOLVED][   ] reward=  272.81  len= 356  streak(L,R)=(10,8)
  Ep  98 [SOLVED][   ] reward=  279.06  len= 166  streak(L,R)=(2,3)
  Ep  99 [SOLVED][   ] reward=  227.42  len= 256  streak(L,R)=(2,3)
  Ep 100 [SOLVED][   ] reward=  279.11  len= 270  streak(L,R)=(2,11)
==============================
Diagnostic Summary
  Mean reward   : 231.85   Median: 253.93   Std: 69.78
  Min / Max     : -19.17 / 308.54
  Solved (>=200): 84/100 (84.0%)
  Low (<0)      : 1/100 (1.0%)
  Mean length   : 307.0
  Action %      : no_op=29.6%, fire_left_orientation_engine=16.2%, fire_main_engine=41.9%, fire_right_orientation_engine=12.3%
  Max side streak: L=71, R=30
  Report saved  : A_seed43_benchmark_b.json
==============================
```

## Run: vanilla-deterministic-lr1e-3-target1000-seed42-20260727-153049

### Source
```text
experiment/deterministic-vanilla-search
27d1b2e97acd684323b2449b60cae92d0a715e4e
 M train.py
```

### Experiment manifest
Experiment: Deterministic Vanilla DQN — Learning Rate 1e-3

Algorithm: Vanilla DQN
Training seed: 42
Training episode seeds: 20042–21041
Episodes: 1000

Learning rate: 1e-3
Target update frequency: 1000 optimizer updates
Replay capacity: 10000
Batch size: 64
Gamma: 0.99
Epsilon start: 1.0
Epsilon minimum: 0.01
Epsilon decay: 0.995 per episode

Paired control:
Vanilla DQN, lr=5e-4, target_update_freq=1000,
same deterministic harness and seed schedule.

Archived paired-control results:
- Combined mean reward: 230.12
- Solved: 116/150 (77.33%)
- Low below zero: 0/150
- Mean episode length: 244.57
- Timeouts: 9/150

Benchmark A: seeds 1234–1283
Benchmark B: seeds 5000–5099

Reserved final holdout:
seeds 10000–10099 — DO NOT RUN

Interpretation caveats:
- Comparison currently uses one deterministic training seed.
- Different learned policies can produce different episode lengths and therefore
  different total optimizer-update counts.
- Timeout truncation remains treated as done by the unchanged environment wrapper.

Observed results:

Benchmark A:
- Mean reward: 138.04
- Solved: 23/50 (46.00%)
- Low below zero: 6/50 (12.00%)
- Mean length: 208.70
- Timeouts: 2/50

Benchmark B:
- Mean reward: 186.69
- Solved: 54/100 (54.00%)
- Low below zero: 8/100 (8.00%)
- Mean length: 399.41
- Timeouts: 25/100

Combined:
- Mean reward: 170.47
- Solved: 77/150 (51.33%)
- Low below zero: 14/150 (9.33%)
- Mean length: 335.84
- Timeouts: 27/150

Paired comparison against deterministic lr=5e-4, target=1000:
- Mean reward: -59.65
- Solved rate: -26.00 percentage points
- Low rate: +9.33 percentage points, worse
- Mean length: +91.27 steps, worse
- Timeouts: +18, worse

Decision:
Rejected. Under the deterministic harness and training seed 42, lr=1e-3 is
substantially worse than lr=5e-4 across reward, reliability, episode length,
and timeout count.

### Combined benchmark summary
```text
Benchmark A:
  episodes     = 50
  mean reward  = 138.04
  solved       = 23/50 (46.00%)
  low          = 6/50 (12.00%)
  mean length  = 208.70
  timeouts     = 2/50

Benchmark B:
  episodes     = 100
  mean reward  = 186.69
  solved       = 54/100 (54.00%)
  low          = 8/100 (8.00%)
  mean length  = 399.41
  timeouts     = 25/100

Combined:
  mean reward  = 170.47
  solved       = 77/150 (51.33%)
  low          = 14/150 (9.33%)
  mean length  = 335.84
  timeouts     = 27/150
```

### Training log tail
```text
--- training_lr1e-3_target1000.log ---
[Validation @ ep 800] mean=157.79 median=171.29 std=101.05 solved=40%
Episode 810, Total Reward: 43.97, Average Max Q-Value: 101.2384, Epsilon: 0.0172
Episode 820, Total Reward: 27.84, Average Max Q-Value: 101.4732, Epsilon: 0.0164
Episode 830, Total Reward: 229.74, Average Max Q-Value: 99.6440, Epsilon: 0.0156
Episode 840, Total Reward: 256.99, Average Max Q-Value: 98.7255, Epsilon: 0.0148
Episode 850, Total Reward: -192.70, Average Max Q-Value: 97.6563, Epsilon: 0.0141
[Validation @ ep 850] mean=114.49 median=165.17 std=187.70 solved=50%
Episode 860, Total Reward: -175.84, Average Max Q-Value: 97.2262, Epsilon: 0.0134
Episode 870, Total Reward: -160.56, Average Max Q-Value: 96.8049, Epsilon: 0.0128
Episode 880, Total Reward: 48.99, Average Max Q-Value: 94.1210, Epsilon: 0.0121
Episode 890, Total Reward: 296.27, Average Max Q-Value: 89.7597, Epsilon: 0.0115
Episode 900, Total Reward: 36.61, Average Max Q-Value: 87.0746, Epsilon: 0.0110
[Validation @ ep 900] mean=115.42 median=52.52 std=112.76 solved=30%
Episode 910, Total Reward: 253.60, Average Max Q-Value: 82.9785, Epsilon: 0.0104
Episode 920, Total Reward: 52.76, Average Max Q-Value: 78.1365, Epsilon: 0.0100
Episode 930, Total Reward: 268.66, Average Max Q-Value: 77.4713, Epsilon: 0.0100
Episode 940, Total Reward: 274.07, Average Max Q-Value: 76.0841, Epsilon: 0.0100
Episode 950, Total Reward: -46.20, Average Max Q-Value: 75.4265, Epsilon: 0.0100
[Validation @ ep 950] mean=240.94 median=287.70 std=84.30 solved=70%  <- NEW BEST (saved)
Episode 960, Total Reward: 282.75, Average Max Q-Value: 74.7185, Epsilon: 0.0100
Episode 970, Total Reward: 279.81, Average Max Q-Value: 73.7043, Epsilon: 0.0100
Episode 980, Total Reward: 7.21, Average Max Q-Value: 74.9564, Epsilon: 0.0100
Episode 990, Total Reward: 306.40, Average Max Q-Value: 79.3798, Epsilon: 0.0100
Episode 1000, Total Reward: 253.44, Average Max Q-Value: 81.3624, Epsilon: 0.0100
[Validation @ ep 1000] mean=203.05 median=187.32 std=81.03 solved=40%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 69.32
Reward Variance: 21897.41
Final Moving-Avg Reward (w=50): 226.02
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- lr1e-3_benchmark_a.log ---
  Ep  40 [SOLVED][   ] reward=  274.59  len= 165  streak(L,R)=(7,3)
  Ep  41 [SOLVED][   ] reward=  259.95  len= 201  streak(L,R)=(6,28)
  Ep  42 [SOLVED][   ] reward=  280.34  len= 220  streak(L,R)=(8,5)
  Ep  43 [SOLVED][   ] reward=  262.51  len= 325  streak(L,R)=(3,27)
  Ep  44 [SOLVED][   ] reward=  284.46  len= 193  streak(L,R)=(2,5)
  Ep  45 [SOLVED][   ] reward=  290.92  len= 189  streak(L,R)=(15,7)
  Ep  46 [SOLVED][   ] reward=  265.72  len= 168  streak(L,R)=(24,6)
  Ep  47 [    ][   ] reward=   56.97  len= 136  streak(L,R)=(15,7)
  Ep  48 [    ][   ] reward=   63.59  len= 161  streak(L,R)=(13,7)
  Ep  49 [    ][LOW] reward=  -36.93  len= 118  streak(L,R)=(2,14)
  Ep  50 [    ][   ] reward=   34.97  len= 139  streak(L,R)=(4,3)
==============================
Diagnostic Summary
  Mean reward   : 138.04   Median: 106.70   Std: 135.83
  Min / Max     : -192.98 / 302.83
  Solved (>=200): 23/50 (46.0%)
  Low (<0)      : 6/50 (12.0%)
  Mean length   : 208.7
  Action %      : no_op=28.1%, fire_left_orientation_engine=16.0%, fire_main_engine=34.7%, fire_right_orientation_engine=21.2%
  Max side streak: L=24, R=34
  Report saved  : lr1e-3_benchmark_a.json
==============================
--- lr1e-3_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  306.22  len= 238  streak(L,R)=(14,11)
  Ep  91 [SOLVED][   ] reward=  257.01  len= 203  streak(L,R)=(5,7)
  Ep  92 [    ][   ] reward=   34.53  len= 137  streak(L,R)=(4,3)
  Ep  93 [    ][LOW] reward=  -16.46  len= 105  streak(L,R)=(2,13)
  Ep  94 [    ][LOW] reward=  -50.25  len= 117  streak(L,R)=(3,16)
  Ep  95 [SOLVED][   ] reward=  284.10  len= 222  streak(L,R)=(12,7)
  Ep  96 [SOLVED][   ] reward=  296.26  len= 159  streak(L,R)=(24,12)
  Ep  97 [    ][   ] reward=   76.25  len= 184  streak(L,R)=(14,5)
  Ep  98 [    ][   ] reward=  160.05  len=1000  streak(L,R)=(4,8)
  Ep  99 [SOLVED][   ] reward=  250.46  len= 146  streak(L,R)=(4,2)
  Ep 100 [SOLVED][   ] reward=  271.86  len= 217  streak(L,R)=(15,33)
==============================
Diagnostic Summary
  Mean reward   : 186.69   Median: 245.94   Std: 116.27
  Min / Max     : -202.35 / 306.22
  Solved (>=200): 54/100 (54.0%)
  Low (<0)      : 8/100 (8.0%)
  Mean length   : 399.4
  Action %      : no_op=32.9%, fire_left_orientation_engine=11.8%, fire_main_engine=21.4%, fire_right_orientation_engine=33.9%
  Max side streak: L=80, R=51
  Report saved  : lr1e-3_benchmark_b.json
==============================
```

## Run: vanilla-deterministic-lr5e-4-target1000-eps997-seed42-20260727-161205

### Source
```text
experiment/deterministic-vanilla-search
a5859ea5a7c3afbca02747decc0422743fd729a1
```

### Experiment manifest
Experiment: Deterministic Vanilla DQN — Epsilon Decay 0.997

Algorithm: Vanilla DQN
Training seed: 42
Training episode seeds: 20042–21041
Episodes: 1000

Learning rate: 5e-4
Target update frequency: 1000 optimizer updates
Replay capacity: 10000
Batch size: 64
Gamma: 0.99
Epsilon start: 1.0
Epsilon minimum: 0.01
Epsilon decay: 0.997 per episode
Expected epsilon after 1000 episodes: approximately 0.050

Paired control:
Vanilla DQN, lr=5e-4, target_update_freq=1000,
epsilon_decay=0.995, episodes=1000,
same deterministic harness and seeds.

Archived paired-control results:
- Combined mean reward: 230.12
- Solved: 116/150 (77.33%)
- Low below zero: 0/150
- Mean episode length: 244.57
- Timeouts: 9/150

Only intended experimental change:
- Epsilon decay: 0.995 -> 0.997

Benchmark A: seeds 1234–1283
Benchmark B: seeds 5000–5099

Reserved final holdout:
seeds 10000–10099 — DO NOT RUN

Interpretation caveats:
- This run tests sustained exploration.
- Epsilon does not reach the 0.01 minimum during the 1000 episodes.
- Benchmark evaluation remains fully greedy with epsilon=0.
- Comparison currently uses one deterministic training seed.
- Policy episode lengths can change the total number of optimizer updates.
- Timeout truncation remains treated as done.

Observed results:

Benchmark A:
- Mean reward: 194.78
- Solved: 32/50 (64.00%)
- Low below zero: 0/50
- Mean length: 218.64
- Timeouts: 2/50

Benchmark B:
- Mean reward: 208.16
- Solved: 72/100 (72.00%)
- Low below zero: 1/100 (1.00%)
- Mean length: 269.52
- Timeouts: 5/100

Combined:
- Mean reward: 203.70
- Solved: 104/150 (69.33%)
- Low below zero: 1/150 (0.67%)
- Mean length: 252.56
- Timeouts: 7/150

Paired comparison against epsilon_decay=0.995:
- Mean reward: -26.42
- Solved rate: -8.00 percentage points
- Low rate: +0.67 percentage points, worse
- Mean length: +7.99 steps, worse
- Timeouts: -2, better

Decision:
Rejected as a standalone 1000-episode configuration. Slower epsilon decay
reduced timeouts slightly but substantially reduced reward and solved rate.
A later 1500-episode schedule test is retained because epsilon remained near
0.05 at the end of this run.

Observed results:

Benchmark A:
- Mean reward: 194.78
- Solved: 32/50 (64.00%)
- Low below zero: 0/50
- Mean length: 218.64
- Timeouts: 2/50

Benchmark B:
- Mean reward: 208.16
- Solved: 72/100 (72.00%)
- Low below zero: 1/100 (1.00%)
- Mean length: 269.52
- Timeouts: 5/100

Combined:
- Mean reward: 203.70
- Solved: 104/150 (69.33%)
- Low below zero: 1/150 (0.67%)
- Mean length: 252.56
- Timeouts: 7/150

Paired comparison against epsilon_decay=0.995:
- Mean reward: -26.42
- Solved rate: -8.00 percentage points
- Low rate: +0.67 percentage points, worse
- Mean length: +7.99 steps, worse
- Timeouts: -2, better

Decision:
Rejected as a 1000-episode configuration. Sustained exploration reduced
timeouts slightly but produced a less mature greedy checkpoint. Further
schedule experiments are deferred until training-seed variance is measured.

### Combined benchmark summary
```text
Benchmark A:
  episodes     = 50
  mean reward  = 194.78
  solved       = 32/50 (64.00%)
  low          = 0/50 (0.00%)
  mean length  = 218.64
  timeouts     = 2/50

Benchmark B:
  episodes     = 100
  mean reward  = 208.16
  solved       = 72/100 (72.00%)
  low          = 1/100 (1.00%)
  mean length  = 269.52
  timeouts     = 5/100

Combined:
  mean reward  = 203.70
  solved       = 104/150 (69.33%)
  low          = 1/150 (0.67%)
  mean length  = 252.56
  timeouts     = 7/150
```

### Training log tail
```text
--- training_eps997.log ---
[Validation @ ep 800] mean=131.11 median=67.55 std=98.82 solved=30%
Episode 810, Total Reward: -18.23, Average Max Q-Value: 96.2724, Epsilon: 0.0877
Episode 820, Total Reward: -7.42, Average Max Q-Value: 94.3269, Epsilon: 0.0851
Episode 830, Total Reward: -62.33, Average Max Q-Value: 94.8588, Epsilon: 0.0826
Episode 840, Total Reward: 17.95, Average Max Q-Value: 93.9372, Epsilon: 0.0802
Episode 850, Total Reward: 50.15, Average Max Q-Value: 94.7031, Epsilon: 0.0778
[Validation @ ep 850] mean=76.54 median=44.51 std=81.54 solved=10%
Episode 860, Total Reward: 38.79, Average Max Q-Value: 95.6308, Epsilon: 0.0755
Episode 870, Total Reward: 40.85, Average Max Q-Value: 95.4958, Epsilon: 0.0732
Episode 880, Total Reward: 272.71, Average Max Q-Value: 96.4387, Epsilon: 0.0711
Episode 890, Total Reward: 51.61, Average Max Q-Value: 97.4195, Epsilon: 0.0690
Episode 900, Total Reward: 26.30, Average Max Q-Value: 97.7632, Epsilon: 0.0669
[Validation @ ep 900] mean=262.37 median=286.03 std=78.55 solved=90%  <- NEW BEST (saved)
Episode 910, Total Reward: 29.90, Average Max Q-Value: 98.1680, Epsilon: 0.0650
Episode 920, Total Reward: 258.35, Average Max Q-Value: 98.7035, Epsilon: 0.0630
Episode 930, Total Reward: 46.88, Average Max Q-Value: 100.1469, Epsilon: 0.0612
Episode 940, Total Reward: 263.48, Average Max Q-Value: 99.7410, Epsilon: 0.0594
Episode 950, Total Reward: 51.51, Average Max Q-Value: 100.2363, Epsilon: 0.0576
[Validation @ ep 950] mean=199.99 median=255.05 std=110.04 solved=70%
Episode 960, Total Reward: 277.75, Average Max Q-Value: 99.8438, Epsilon: 0.0559
Episode 970, Total Reward: -3.89, Average Max Q-Value: 99.5856, Epsilon: 0.0542
Episode 980, Total Reward: 33.54, Average Max Q-Value: 102.0746, Epsilon: 0.0526
Episode 990, Total Reward: -11.40, Average Max Q-Value: 102.7013, Epsilon: 0.0511
Episode 1000, Total Reward: 20.76, Average Max Q-Value: 102.3167, Epsilon: 0.0496
[Validation @ ep 1000] mean=152.12 median=123.75 std=114.80 solved=40%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 45.36
Reward Variance: 18150.05
Final Moving-Avg Reward (w=50): 102.54
Final Epsilon: 0.0496
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- eps997_benchmark_a.log ---
  Ep  40 [SOLVED][   ] reward=  259.62  len= 193  streak(L,R)=(7,1)
  Ep  41 [    ][   ] reward=   26.14  len= 129  streak(L,R)=(1,3)
  Ep  42 [    ][   ] reward=   27.69  len= 163  streak(L,R)=(2,1)
  Ep  43 [SOLVED][   ] reward=  288.26  len= 201  streak(L,R)=(2,1)
  Ep  44 [SOLVED][   ] reward=  262.35  len= 179  streak(L,R)=(2,1)
  Ep  45 [SOLVED][   ] reward=  262.33  len= 208  streak(L,R)=(5,3)
  Ep  46 [SOLVED][   ] reward=  289.86  len= 162  streak(L,R)=(2,1)
  Ep  47 [SOLVED][   ] reward=  277.04  len= 320  streak(L,R)=(4,8)
  Ep  48 [SOLVED][   ] reward=  270.09  len= 277  streak(L,R)=(4,9)
  Ep  49 [    ][   ] reward=   41.97  len= 141  streak(L,R)=(1,6)
  Ep  50 [SOLVED][   ] reward=  286.11  len= 201  streak(L,R)=(3,1)
==============================
Diagnostic Summary
  Mean reward   : 194.78   Median: 260.98   Std: 107.70
  Min / Max     : 5.36 / 306.49
  Solved (>=200): 32/50 (64.0%)
  Low (<0)      : 0/50 (0.0%)
  Mean length   : 218.6
  Action %      : no_op=47.8%, fire_left_orientation_engine=9.1%, fire_main_engine=32.8%, fire_right_orientation_engine=10.3%
  Max side streak: L=15, R=84
  Report saved  : eps997_benchmark_a.json
==============================
--- eps997_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  297.47  len= 184  streak(L,R)=(8,20)
  Ep  91 [    ][   ] reward=  108.57  len=1000  streak(L,R)=(8,1)
  Ep  92 [SOLVED][   ] reward=  275.46  len= 191  streak(L,R)=(2,1)
  Ep  93 [SOLVED][   ] reward=  274.80  len= 262  streak(L,R)=(98,10)
  Ep  94 [    ][   ] reward=   50.09  len= 139  streak(L,R)=(2,8)
  Ep  95 [SOLVED][   ] reward=  261.54  len= 199  streak(L,R)=(3,2)
  Ep  96 [    ][   ] reward=   35.08  len= 111  streak(L,R)=(2,2)
  Ep  97 [SOLVED][   ] reward=  232.30  len= 733  streak(L,R)=(37,3)
  Ep  98 [    ][   ] reward=   61.32  len= 129  streak(L,R)=(1,2)
  Ep  99 [SOLVED][   ] reward=  223.96  len= 190  streak(L,R)=(18,1)
  Ep 100 [SOLVED][   ] reward=  270.81  len= 266  streak(L,R)=(8,42)
==============================
Diagnostic Summary
  Mean reward   : 208.16   Median: 259.08   Std: 99.28
  Min / Max     : -117.45 / 306.11
  Solved (>=200): 72/100 (72.0%)
  Low (<0)      : 1/100 (1.0%)
  Mean length   : 269.5
  Action %      : no_op=45.3%, fire_left_orientation_engine=12.7%, fire_main_engine=27.4%, fire_right_orientation_engine=14.6%
  Max side streak: L=98, R=67
  Report saved  : eps997_benchmark_b.json
==============================
```

## Run: vanilla-deterministic-lr5e-4-target1000-seed42-20260727-121329

### Source
```text
experiment/deterministic-vanilla-search
d01c8d4b3c6a0415b934bf51c2bd12222b5237f3
```

### Training log tail
```text
--- training_control.log ---
[Validation @ ep 800] mean=261.31 median=286.04 std=73.73 solved=90%  <- NEW BEST (saved)
Episode 810, Total Reward: 28.61, Average Max Q-Value: 98.8413, Epsilon: 0.0172
Episode 820, Total Reward: 14.85, Average Max Q-Value: 99.2519, Epsilon: 0.0164
Episode 830, Total Reward: 36.09, Average Max Q-Value: 99.6065, Epsilon: 0.0156
Episode 840, Total Reward: 253.84, Average Max Q-Value: 99.8346, Epsilon: 0.0148
Episode 850, Total Reward: 230.54, Average Max Q-Value: 100.3445, Epsilon: 0.0141
[Validation @ ep 850] mean=289.45 median=290.00 std=13.22 solved=100%  <- NEW BEST (saved)
Episode 860, Total Reward: 304.53, Average Max Q-Value: 101.0241, Epsilon: 0.0134
Episode 870, Total Reward: 306.03, Average Max Q-Value: 100.9613, Epsilon: 0.0128
Episode 880, Total Reward: 268.73, Average Max Q-Value: 101.0638, Epsilon: 0.0121
Episode 890, Total Reward: 302.13, Average Max Q-Value: 101.5850, Epsilon: 0.0115
Episode 900, Total Reward: 263.82, Average Max Q-Value: 101.5516, Epsilon: 0.0110
[Validation @ ep 900] mean=199.05 median=269.64 std=121.69 solved=60%
Episode 910, Total Reward: 285.28, Average Max Q-Value: 101.3905, Epsilon: 0.0104
Episode 920, Total Reward: 265.61, Average Max Q-Value: 101.9190, Epsilon: 0.0100
Episode 930, Total Reward: 58.93, Average Max Q-Value: 101.9913, Epsilon: 0.0100
Episode 940, Total Reward: 284.36, Average Max Q-Value: 101.9391, Epsilon: 0.0100
Episode 950, Total Reward: 35.80, Average Max Q-Value: 102.2033, Epsilon: 0.0100
[Validation @ ep 950] mean=248.23 median=303.25 std=101.67 solved=80%
Episode 960, Total Reward: 40.75, Average Max Q-Value: 101.9030, Epsilon: 0.0100
Episode 970, Total Reward: 290.31, Average Max Q-Value: 101.6198, Epsilon: 0.0100
Episode 980, Total Reward: 295.89, Average Max Q-Value: 102.3091, Epsilon: 0.0100
Episode 990, Total Reward: 54.22, Average Max Q-Value: 101.7059, Epsilon: 0.0100
Episode 1000, Total Reward: 271.93, Average Max Q-Value: 102.2967, Epsilon: 0.0100
[Validation @ ep 1000] mean=269.64 median=296.93 std=72.76 solved=90%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 124.19
Reward Variance: 23619.70
Final Moving-Avg Reward (w=50): 227.94
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- control_benchmark_a.log ---
  Ep  40 [    ][   ] reward=   47.17  len= 117  streak(L,R)=(3,3)
  Ep  41 [SOLVED][   ] reward=  257.66  len= 194  streak(L,R)=(1,4)
  Ep  42 [SOLVED][   ] reward=  264.87  len= 192  streak(L,R)=(56,3)
  Ep  43 [SOLVED][   ] reward=  285.78  len= 183  streak(L,R)=(8,10)
  Ep  44 [    ][   ] reward=   70.11  len=  90  streak(L,R)=(2,1)
  Ep  45 [SOLVED][   ] reward=  269.31  len= 227  streak(L,R)=(5,12)
  Ep  46 [SOLVED][   ] reward=  270.04  len= 189  streak(L,R)=(2,3)
  Ep  47 [SOLVED][   ] reward=  281.07  len= 195  streak(L,R)=(8,16)
  Ep  48 [SOLVED][   ] reward=  287.92  len= 222  streak(L,R)=(4,29)
  Ep  49 [SOLVED][   ] reward=  276.57  len= 210  streak(L,R)=(12,5)
  Ep  50 [SOLVED][   ] reward=  289.08  len= 162  streak(L,R)=(2,6)
==============================
Diagnostic Summary
  Mean reward   : 249.19   Median: 271.80   Std: 78.29
  Min / Max     : 20.73 / 311.24
  Solved (>=200): 43/50 (86.0%)
  Low (<0)      : 0/50 (0.0%)
  Mean length   : 227.9
  Action %      : no_op=39.6%, fire_left_orientation_engine=12.2%, fire_main_engine=34.8%, fire_right_orientation_engine=13.4%
  Max side streak: L=56, R=29
  Report saved  : control_benchmark_a.json
==============================
--- control_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  309.55  len= 221  streak(L,R)=(11,20)
  Ep  91 [    ][   ] reward=   20.21  len= 103  streak(L,R)=(4,1)
  Ep  92 [    ][   ] reward=   57.32  len= 115  streak(L,R)=(3,4)
  Ep  93 [SOLVED][   ] reward=  309.07  len= 258  streak(L,R)=(38,10)
  Ep  94 [    ][   ] reward=  156.52  len=1000  streak(L,R)=(6,4)
  Ep  95 [SOLVED][   ] reward=  267.63  len= 182  streak(L,R)=(3,21)
  Ep  96 [    ][   ] reward=  163.57  len=1000  streak(L,R)=(4,6)
  Ep  97 [SOLVED][   ] reward=  304.46  len= 249  streak(L,R)=(6,11)
  Ep  98 [    ][   ] reward=   47.44  len= 113  streak(L,R)=(3,4)
  Ep  99 [SOLVED][   ] reward=  249.72  len= 182  streak(L,R)=(15,1)
  Ep 100 [SOLVED][   ] reward=  294.47  len= 379  streak(L,R)=(10,5)
==============================
Diagnostic Summary
  Mean reward   : 220.58   Median: 268.26   Std: 94.99
  Min / Max     : 13.06 / 309.55
  Solved (>=200): 73/100 (73.0%)
  Low (<0)      : 0/100 (0.0%)
  Mean length   : 252.9
  Action %      : no_op=42.7%, fire_left_orientation_engine=10.6%, fire_main_engine=30.6%, fire_right_orientation_engine=16.1%
  Max side streak: L=83, R=47
  Report saved  : control_benchmark_b.json
==============================
```

## Run: vanilla-deterministic-lr5e-4-target2000-seed42-20260727-130427

### Source
```text
experiment/deterministic-vanilla-search
27d1b2e97acd684323b2449b60cae92d0a715e4e
```

### Experiment manifest
Experiment: Deterministic Vanilla DQN — Learning Rate 1e-3

Algorithm: Vanilla DQN
Training seed: 42
Training episode seeds: 20042–21041
Episodes: 1000

Learning rate: 1e-3
Target update frequency: 1000 optimizer updates
Replay capacity: 10000
Batch size: 64
Gamma: 0.99
Epsilon start: 1.0
Epsilon minimum: 0.01
Epsilon decay: 0.995 per episode

Paired control:
Vanilla DQN, lr=5e-4, target_update_freq=1000,
same deterministic harness and seed schedule.

Archived paired-control results:
- Combined mean reward: 230.12
- Solved: 116/150 (77.33%)
- Low below zero: 0/150
- Mean episode length: 244.57
- Timeouts: 9/150

Benchmark A: seeds 1234–1283
Benchmark B: seeds 5000–5099

Reserved final holdout:
seeds 10000–10099 — DO NOT RUN

Interpretation caveats:
- Comparison currently uses one deterministic training seed.
- Different learned policies can produce different episode lengths and therefore
  different total optimizer-update counts.
- Timeout truncation remains treated as done by the unchanged environment wrapper.

### Combined benchmark summary
```text
Benchmark A:
  episodes     = 50
  mean reward  = 245.70
  solved       = 46/50 (92.00%)
  low          = 1/50 (2.00%)
  mean length  = 290.66
  timeouts     = 3/50

Benchmark B:
  episodes     = 100
  mean reward  = 230.84
  solved       = 84/100 (84.00%)
  low          = 7/100 (7.00%)
  mean length  = 340.93
  timeouts     = 8/100

Combined:
  mean reward  = 235.79
  solved       = 130/150 (86.67%)
  low          = 8/150 (5.33%)
  mean length  = 324.17
  timeouts     = 11/150
```

### Training log tail
```text
--- training_lr1e-3_target1000.log ---
[Validation @ ep 800] mean=157.79 median=171.29 std=101.05 solved=40%
Episode 810, Total Reward: 43.97, Average Max Q-Value: 101.2384, Epsilon: 0.0172
Episode 820, Total Reward: 27.84, Average Max Q-Value: 101.4732, Epsilon: 0.0164
Episode 830, Total Reward: 229.74, Average Max Q-Value: 99.6440, Epsilon: 0.0156
Episode 840, Total Reward: 256.99, Average Max Q-Value: 98.7255, Epsilon: 0.0148
Episode 850, Total Reward: -192.70, Average Max Q-Value: 97.6563, Epsilon: 0.0141
[Validation @ ep 850] mean=114.49 median=165.17 std=187.70 solved=50%
Episode 860, Total Reward: -175.84, Average Max Q-Value: 97.2262, Epsilon: 0.0134
Episode 870, Total Reward: -160.56, Average Max Q-Value: 96.8049, Epsilon: 0.0128
Episode 880, Total Reward: 48.99, Average Max Q-Value: 94.1210, Epsilon: 0.0121
Episode 890, Total Reward: 296.27, Average Max Q-Value: 89.7597, Epsilon: 0.0115
Episode 900, Total Reward: 36.61, Average Max Q-Value: 87.0746, Epsilon: 0.0110
[Validation @ ep 900] mean=115.42 median=52.52 std=112.76 solved=30%
Episode 910, Total Reward: 253.60, Average Max Q-Value: 82.9785, Epsilon: 0.0104
Episode 920, Total Reward: 52.76, Average Max Q-Value: 78.1365, Epsilon: 0.0100
Episode 930, Total Reward: 268.66, Average Max Q-Value: 77.4713, Epsilon: 0.0100
Episode 940, Total Reward: 274.07, Average Max Q-Value: 76.0841, Epsilon: 0.0100
Episode 950, Total Reward: -46.20, Average Max Q-Value: 75.4265, Epsilon: 0.0100
[Validation @ ep 950] mean=240.94 median=287.70 std=84.30 solved=70%  <- NEW BEST (saved)
Episode 960, Total Reward: 282.75, Average Max Q-Value: 74.7185, Epsilon: 0.0100
Episode 970, Total Reward: 279.81, Average Max Q-Value: 73.7043, Epsilon: 0.0100
Episode 980, Total Reward: 7.21, Average Max Q-Value: 74.9564, Epsilon: 0.0100
Episode 990, Total Reward: 306.40, Average Max Q-Value: 79.3798, Epsilon: 0.0100
Episode 1000, Total Reward: 253.44, Average Max Q-Value: 81.3624, Epsilon: 0.0100
[Validation @ ep 1000] mean=203.05 median=187.32 std=81.03 solved=40%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 69.32
Reward Variance: 21897.41
Final Moving-Avg Reward (w=50): 226.02
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
--- training_target2000.log ---
[Validation @ ep 800] mean=158.75 median=215.68 std=138.33 solved=50%
Episode 810, Total Reward: 242.40, Average Max Q-Value: 104.5391, Epsilon: 0.0172
Episode 820, Total Reward: 235.61, Average Max Q-Value: 105.3920, Epsilon: 0.0164
Episode 830, Total Reward: 16.13, Average Max Q-Value: 104.9754, Epsilon: 0.0156
Episode 840, Total Reward: 262.70, Average Max Q-Value: 104.6473, Epsilon: 0.0148
Episode 850, Total Reward: 249.00, Average Max Q-Value: 104.2810, Epsilon: 0.0141
[Validation @ ep 850] mean=187.55 median=269.73 std=114.43 solved=60%
Episode 860, Total Reward: 290.11, Average Max Q-Value: 103.7424, Epsilon: 0.0134
Episode 870, Total Reward: 259.99, Average Max Q-Value: 101.9275, Epsilon: 0.0128
Episode 880, Total Reward: 266.18, Average Max Q-Value: 100.9577, Epsilon: 0.0121
Episode 890, Total Reward: 288.11, Average Max Q-Value: 100.4947, Epsilon: 0.0115
Episode 900, Total Reward: 250.27, Average Max Q-Value: 99.5982, Epsilon: 0.0110
[Validation @ ep 900] mean=183.45 median=227.76 std=115.66 solved=50%
Episode 910, Total Reward: 307.43, Average Max Q-Value: 99.5007, Epsilon: 0.0104
Episode 920, Total Reward: 30.08, Average Max Q-Value: 98.4317, Epsilon: 0.0100
Episode 930, Total Reward: 53.99, Average Max Q-Value: 98.8185, Epsilon: 0.0100
Episode 940, Total Reward: 275.47, Average Max Q-Value: 98.3293, Epsilon: 0.0100
Episode 950, Total Reward: 26.62, Average Max Q-Value: 98.2385, Epsilon: 0.0100
[Validation @ ep 950] mean=174.60 median=207.16 std=118.48 solved=50%
Episode 960, Total Reward: 284.92, Average Max Q-Value: 97.7632, Epsilon: 0.0100
Episode 970, Total Reward: 35.51, Average Max Q-Value: 97.4929, Epsilon: 0.0100
Episode 980, Total Reward: 100.01, Average Max Q-Value: 97.5417, Epsilon: 0.0100
Episode 990, Total Reward: -39.39, Average Max Q-Value: 96.8197, Epsilon: 0.0100
Episode 1000, Total Reward: 255.91, Average Max Q-Value: 97.9120, Epsilon: 0.0100
[Validation @ ep 1000] mean=69.66 median=40.16 std=83.56 solved=10%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 108.15
Reward Variance: 24586.30
Final Moving-Avg Reward (w=50): 216.91
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- target2000_benchmark_a.log ---
  Ep  40 [SOLVED][   ] reward=  260.15  len= 200  streak(L,R)=(1,6)
  Ep  41 [SOLVED][   ] reward=  245.75  len= 231  streak(L,R)=(1,7)
  Ep  42 [SOLVED][   ] reward=  253.10  len= 226  streak(L,R)=(56,4)
  Ep  43 [SOLVED][   ] reward=  277.92  len= 205  streak(L,R)=(1,1)
  Ep  44 [SOLVED][   ] reward=  258.11  len= 186  streak(L,R)=(1,2)
  Ep  45 [SOLVED][   ] reward=  248.34  len= 277  streak(L,R)=(2,6)
  Ep  46 [SOLVED][   ] reward=  275.50  len= 177  streak(L,R)=(8,24)
  Ep  47 [SOLVED][   ] reward=  205.36  len= 439  streak(L,R)=(3,30)
  Ep  48 [SOLVED][   ] reward=  220.07  len= 338  streak(L,R)=(1,27)
  Ep  49 [SOLVED][   ] reward=  287.51  len= 287  streak(L,R)=(4,10)
  Ep  50 [SOLVED][   ] reward=  285.03  len= 171  streak(L,R)=(1,1)
==============================
Diagnostic Summary
  Mean reward   : 245.70   Median: 261.16   Std: 69.59
  Min / Max     : -35.98 / 300.68
  Solved (>=200): 46/50 (92.0%)
  Low (<0)      : 1/50 (2.0%)
  Mean length   : 290.7
  Action %      : no_op=32.1%, fire_left_orientation_engine=10.4%, fire_main_engine=42.8%, fire_right_orientation_engine=14.8%
  Max side streak: L=93, R=115
  Report saved  : target2000_benchmark_a.json
==============================
--- target2000_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  297.61  len= 208  streak(L,R)=(7,17)
  Ep  91 [    ][   ] reward=  187.54  len= 257  streak(L,R)=(38,1)
  Ep  92 [SOLVED][   ] reward=  279.50  len= 168  streak(L,R)=(1,1)
  Ep  93 [SOLVED][   ] reward=  302.33  len= 236  streak(L,R)=(2,6)
  Ep  94 [SOLVED][   ] reward=  294.05  len= 308  streak(L,R)=(9,7)
  Ep  95 [SOLVED][   ] reward=  266.41  len= 203  streak(L,R)=(2,9)
  Ep  96 [SOLVED][   ] reward=  201.83  len= 509  streak(L,R)=(2,70)
  Ep  97 [SOLVED][   ] reward=  204.59  len= 538  streak(L,R)=(31,6)
  Ep  98 [SOLVED][   ] reward=  278.51  len= 172  streak(L,R)=(1,1)
  Ep  99 [SOLVED][   ] reward=  216.28  len= 361  streak(L,R)=(103,3)
  Ep 100 [SOLVED][   ] reward=  256.15  len= 381  streak(L,R)=(19,6)
==============================
Diagnostic Summary
  Mean reward   : 230.84   Median: 257.44   Std: 83.34
  Min / Max     : -66.65 / 312.55
  Solved (>=200): 84/100 (84.0%)
  Low (<0)      : 7/100 (7.0%)
  Mean length   : 340.9
  Action %      : no_op=32.7%, fire_left_orientation_engine=11.5%, fire_main_engine=36.4%, fire_right_orientation_engine=19.4%
  Max side streak: L=206, R=311
  Report saved  : target2000_benchmark_b.json
==============================
```

## Run: vanilla-lr5e-4-seed42-20260726-193019

### Training log tail
```text
--- training_run_vanilla_lr5e-4_seed42.log ---
[Validation @ ep 800] mean=246.69 median=283.66 std=72.57 solved=80%  <- NEW BEST (saved)
Episode 810, Total Reward: 70.50, Average Max Q-Value: 104.2721, Epsilon: 0.0172
Episode 820, Total Reward: 39.38, Average Max Q-Value: 107.7910, Epsilon: 0.0164
Episode 830, Total Reward: 248.83, Average Max Q-Value: 108.6723, Epsilon: 0.0156
Episode 840, Total Reward: 242.60, Average Max Q-Value: 106.6137, Epsilon: 0.0148
Episode 850, Total Reward: 254.55, Average Max Q-Value: 105.7912, Epsilon: 0.0141
[Validation @ ep 850] mean=192.31 median=267.18 std=114.59 solved=60%
Episode 860, Total Reward: -68.44, Average Max Q-Value: 103.1672, Epsilon: 0.0134
Episode 870, Total Reward: 268.61, Average Max Q-Value: 103.8044, Epsilon: 0.0128
Episode 880, Total Reward: 290.20, Average Max Q-Value: 104.9041, Epsilon: 0.0121
Episode 890, Total Reward: 302.89, Average Max Q-Value: 105.9986, Epsilon: 0.0115
Episode 900, Total Reward: 277.36, Average Max Q-Value: 106.9590, Epsilon: 0.0110
[Validation @ ep 900] mean=186.41 median=277.29 std=133.12 solved=60%
Episode 910, Total Reward: 252.83, Average Max Q-Value: 107.6269, Epsilon: 0.0104
Episode 920, Total Reward: 278.14, Average Max Q-Value: 107.6838, Epsilon: 0.0100
Episode 930, Total Reward: 268.53, Average Max Q-Value: 107.6151, Epsilon: 0.0100
Episode 940, Total Reward: 259.63, Average Max Q-Value: 108.3783, Epsilon: 0.0100
Episode 950, Total Reward: 39.01, Average Max Q-Value: 108.3876, Epsilon: 0.0100
[Validation @ ep 950] mean=76.14 median=40.04 std=154.26 solved=30%
Episode 960, Total Reward: 254.26, Average Max Q-Value: 109.6919, Epsilon: 0.0100
Episode 970, Total Reward: 30.58, Average Max Q-Value: 111.0751, Epsilon: 0.0100
Episode 980, Total Reward: 288.12, Average Max Q-Value: 109.9378, Epsilon: 0.0100
Episode 990, Total Reward: 283.53, Average Max Q-Value: 108.6627, Epsilon: 0.0100
Episode 1000, Total Reward: 295.71, Average Max Q-Value: 107.2456, Epsilon: 0.0100
[Validation @ ep 1000] mean=95.35 median=59.22 std=90.92 solved=20%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 107.36
Reward Variance: 20096.62
Final Moving-Avg Reward (w=50): 175.72
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### Benchmark log tails
```text
--- vanilla_lr5e-4_benchmark_a.log ---
  Ep  40 [SOLVED][   ] reward=  272.10  len= 187  streak(L,R)=(4,6)
  Ep  41 [SOLVED][   ] reward=  220.98  len= 359  streak(L,R)=(8,7)
  Ep  42 [    ][   ] reward=  142.08  len=1000  streak(L,R)=(7,5)
  Ep  43 [SOLVED][   ] reward=  275.95  len= 192  streak(L,R)=(4,2)
  Ep  44 [SOLVED][   ] reward=  281.67  len= 147  streak(L,R)=(6,6)
  Ep  45 [SOLVED][   ] reward=  260.73  len= 249  streak(L,R)=(10,5)
  Ep  46 [SOLVED][   ] reward=  271.66  len= 256  streak(L,R)=(1,6)
  Ep  47 [    ][   ] reward=  172.85  len=1000  streak(L,R)=(11,21)
  Ep  48 [SOLVED][   ] reward=  276.68  len= 371  streak(L,R)=(9,35)
  Ep  49 [SOLVED][   ] reward=  278.60  len= 217  streak(L,R)=(20,17)
  Ep  50 [SOLVED][   ] reward=  282.88  len= 179  streak(L,R)=(5,2)
==============================
Diagnostic Summary
  Mean reward   : 251.12   Median: 271.88   Std: 57.30
  Min / Max     : 41.11 / 302.91
  Solved (>=200): 42/50 (84.0%)
  Low (<0)      : 0/50 (0.0%)
  Mean length   : 331.6
  Action %      : no_op=39.4%, fire_left_orientation_engine=13.0%, fire_main_engine=32.0%, fire_right_orientation_engine=15.6%
  Max side streak: L=83, R=35
  Report saved  : vanilla_lr5e-4_benchmark_a_1234_1283.json
==============================
--- vanilla_lr5e-4_benchmark_b.log ---
  Ep  90 [SOLVED][   ] reward=  301.81  len= 199  streak(L,R)=(12,9)
  Ep  91 [SOLVED][   ] reward=  255.84  len= 169  streak(L,R)=(4,9)
  Ep  92 [SOLVED][   ] reward=  278.03  len= 199  streak(L,R)=(3,3)
  Ep  93 [SOLVED][   ] reward=  289.91  len= 359  streak(L,R)=(9,15)
  Ep  94 [    ][   ] reward=  177.57  len=1000  streak(L,R)=(11,16)
  Ep  95 [    ][   ] reward=  149.02  len=1000  streak(L,R)=(8,5)
  Ep  96 [    ][   ] reward=  146.62  len=1000  streak(L,R)=(4,6)
  Ep  97 [SOLVED][   ] reward=  206.48  len= 520  streak(L,R)=(19,27)
  Ep  98 [    ][   ] reward=   61.60  len= 126  streak(L,R)=(2,6)
  Ep  99 [SOLVED][   ] reward=  243.23  len= 184  streak(L,R)=(3,5)
  Ep 100 [SOLVED][   ] reward=  279.48  len= 287  streak(L,R)=(16,10)
==============================
Diagnostic Summary
  Mean reward   : 234.98   Median: 262.15   Std: 70.43
  Min / Max     : 20.68 / 308.38
  Solved (>=200): 79/100 (79.0%)
  Low (<0)      : 0/100 (0.0%)
  Mean length   : 333.7
  Action %      : no_op=39.4%, fire_left_orientation_engine=11.3%, fire_main_engine=31.2%, fire_right_orientation_engine=18.1%
  Max side streak: L=59, R=30
  Report saved  : vanilla_lr5e-4_benchmark_b_5000_5099.json
==============================
```

## Validated baseline archive inventory
```text
diagnostic_report.json	64 KB
diagnostic_report_baseline.json	64 KB
diagnostic_report_final_50.json	60 KB
diagnostic_report_final_candidate.json	60 KB
diagnostic_report_final_unseen_100.json	128 KB
training_metrics_baseline.json	60 KB
training_metrics_final.json	72 KB
training_metrics_final_candidate.json	72 KB
training_metrics_seed42.json	60 KB
training_metrics_smoke.json	4 KB
training_plot_baseline.png	116 KB
training_plot_final.png	124 KB
training_plot_final_candidate.png	124 KB
training_plot_seed42.png	116 KB
training_plot_smoke.png	64 KB
training_run.log	28 KB
training_run_final.log	12 KB
training_run_final_candidate.log	12 KB
training_run_seed42.log	28 KB
training_run_validation.log	12 KB
weights_baseline.pth	76 KB
weights_before_full_training.pth	76 KB
weights_best_seed42.pth	76 KB
weights_dqn_baseline_224.pth	76 KB
weights_final_backup.pth	76 KB
weights_final_candidate.pth	76 KB
weights_old.pth	76 KB
```

## Baseline archive training-log tails

### training_run.log
```text
New best moving-avg reward: 230.05 (over last 50 episodes). Weights saved to weights.pth.
Episode 790, Total Reward: 161.77, Average Max Q-Value: 121.4600, Epsilon: 0.0191
New best moving-avg reward: 230.40 (over last 50 episodes). Weights saved to weights.pth.
New best moving-avg reward: 233.60 (over last 50 episodes). Weights saved to weights.pth.
Episode 800, Total Reward: 278.69, Average Max Q-Value: 125.1475, Epsilon: 0.0181
Episode 810, Total Reward: 260.30, Average Max Q-Value: 126.5534, Epsilon: 0.0172
Episode 820, Total Reward: 239.40, Average Max Q-Value: 126.3219, Epsilon: 0.0164
Episode 830, Total Reward: 23.39, Average Max Q-Value: 124.2520, Epsilon: 0.0156
Episode 840, Total Reward: -5.30, Average Max Q-Value: 122.8539, Epsilon: 0.0148
Episode 850, Total Reward: 54.88, Average Max Q-Value: 121.1886, Epsilon: 0.0141
Episode 860, Total Reward: 12.08, Average Max Q-Value: 120.1206, Epsilon: 0.0134
Episode 870, Total Reward: -61.56, Average Max Q-Value: 118.7952, Epsilon: 0.0128
Episode 880, Total Reward: -11.46, Average Max Q-Value: 115.8494, Epsilon: 0.0121
Episode 890, Total Reward: 261.64, Average Max Q-Value: 116.2933, Epsilon: 0.0115
Episode 900, Total Reward: 23.15, Average Max Q-Value: 117.3110, Epsilon: 0.0110
Episode 910, Total Reward: -15.56, Average Max Q-Value: 115.9765, Epsilon: 0.0104
Episode 920, Total Reward: -94.66, Average Max Q-Value: 111.0531, Epsilon: 0.0100
Episode 930, Total Reward: -342.12, Average Max Q-Value: 106.1684, Epsilon: 0.0100
Episode 940, Total Reward: 273.96, Average Max Q-Value: 100.8057, Epsilon: 0.0100
Episode 950, Total Reward: 73.18, Average Max Q-Value: 95.5724, Epsilon: 0.0100
Episode 960, Total Reward: 283.80, Average Max Q-Value: 98.5763, Epsilon: 0.0100
Episode 970, Total Reward: -50.00, Average Max Q-Value: 97.3741, Epsilon: 0.0100
Episode 980, Total Reward: 54.60, Average Max Q-Value: 96.6219, Epsilon: 0.0100
Episode 990, Total Reward: 295.04, Average Max Q-Value: 97.0263, Epsilon: 0.0100
Episode 1000, Total Reward: 53.01, Average Max Q-Value: 99.4414, Epsilon: 0.0100
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 86.08
Reward Variance: 22323.96
Final Moving-Avg Reward (w=50): 179.80
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### training_run_final.log
```text
[Validation @ ep 800] mean=234.67 median=284.68 std=102.09 solved=80%
Episode 810, Total Reward: 272.42, Average Max Q-Value: 84.7322, Epsilon: 0.0172
Episode 820, Total Reward: 262.00, Average Max Q-Value: 86.9481, Epsilon: 0.0164
Episode 830, Total Reward: 29.60, Average Max Q-Value: 89.2231, Epsilon: 0.0156
Episode 840, Total Reward: 268.99, Average Max Q-Value: 92.3195, Epsilon: 0.0148
Episode 850, Total Reward: 276.28, Average Max Q-Value: 93.7160, Epsilon: 0.0141
[Validation @ ep 850] mean=252.14 median=286.06 std=76.57 solved=80%
Episode 860, Total Reward: 253.32, Average Max Q-Value: 95.1612, Epsilon: 0.0134
Episode 870, Total Reward: 218.91, Average Max Q-Value: 96.5292, Epsilon: 0.0128
Episode 880, Total Reward: 264.19, Average Max Q-Value: 97.2190, Epsilon: 0.0121
Episode 890, Total Reward: 272.29, Average Max Q-Value: 98.6256, Epsilon: 0.0115
Episode 900, Total Reward: 292.22, Average Max Q-Value: 98.6015, Epsilon: 0.0110
[Validation @ ep 900] mean=281.71 median=297.01 std=35.98 solved=90%  <- NEW BEST (saved)
Episode 910, Total Reward: 267.27, Average Max Q-Value: 99.5904, Epsilon: 0.0104
Episode 920, Total Reward: 277.95, Average Max Q-Value: 99.7292, Epsilon: 0.0100
Episode 930, Total Reward: 273.73, Average Max Q-Value: 100.7088, Epsilon: 0.0100
Episode 940, Total Reward: 296.16, Average Max Q-Value: 101.2376, Epsilon: 0.0100
Episode 950, Total Reward: 295.34, Average Max Q-Value: 101.9003, Epsilon: 0.0100
[Validation @ ep 950] mean=292.87 median=294.48 std=16.10 solved=100%  <- NEW BEST (saved)
Episode 960, Total Reward: 302.54, Average Max Q-Value: 104.1461, Epsilon: 0.0100
Episode 970, Total Reward: 284.96, Average Max Q-Value: 103.9500, Epsilon: 0.0100
Episode 980, Total Reward: 273.53, Average Max Q-Value: 104.5380, Epsilon: 0.0100
Episode 990, Total Reward: 285.15, Average Max Q-Value: 104.4497, Epsilon: 0.0100
Episode 1000, Total Reward: 292.27, Average Max Q-Value: 102.6706, Epsilon: 0.0100
[Validation @ ep 1000] mean=292.52 median=297.60 std=14.67 solved=100%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 132.68
Reward Variance: 24302.56
Final Moving-Avg Reward (w=50): 246.90
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### training_run_final_candidate.log
```text
[Validation @ ep 800] mean=234.67 median=284.68 std=102.09 solved=80%
Episode 810, Total Reward: 272.42, Average Max Q-Value: 84.7322, Epsilon: 0.0172
Episode 820, Total Reward: 262.00, Average Max Q-Value: 86.9481, Epsilon: 0.0164
Episode 830, Total Reward: 29.60, Average Max Q-Value: 89.2231, Epsilon: 0.0156
Episode 840, Total Reward: 268.99, Average Max Q-Value: 92.3195, Epsilon: 0.0148
Episode 850, Total Reward: 276.28, Average Max Q-Value: 93.7160, Epsilon: 0.0141
[Validation @ ep 850] mean=252.14 median=286.06 std=76.57 solved=80%
Episode 860, Total Reward: 253.32, Average Max Q-Value: 95.1612, Epsilon: 0.0134
Episode 870, Total Reward: 218.91, Average Max Q-Value: 96.5292, Epsilon: 0.0128
Episode 880, Total Reward: 264.19, Average Max Q-Value: 97.2190, Epsilon: 0.0121
Episode 890, Total Reward: 272.29, Average Max Q-Value: 98.6256, Epsilon: 0.0115
Episode 900, Total Reward: 292.22, Average Max Q-Value: 98.6015, Epsilon: 0.0110
[Validation @ ep 900] mean=281.71 median=297.01 std=35.98 solved=90%  <- NEW BEST (saved)
Episode 910, Total Reward: 267.27, Average Max Q-Value: 99.5904, Epsilon: 0.0104
Episode 920, Total Reward: 277.95, Average Max Q-Value: 99.7292, Epsilon: 0.0100
Episode 930, Total Reward: 273.73, Average Max Q-Value: 100.7088, Epsilon: 0.0100
Episode 940, Total Reward: 296.16, Average Max Q-Value: 101.2376, Epsilon: 0.0100
Episode 950, Total Reward: 295.34, Average Max Q-Value: 101.9003, Epsilon: 0.0100
[Validation @ ep 950] mean=292.87 median=294.48 std=16.10 solved=100%  <- NEW BEST (saved)
Episode 960, Total Reward: 302.54, Average Max Q-Value: 104.1461, Epsilon: 0.0100
Episode 970, Total Reward: 284.96, Average Max Q-Value: 103.9500, Epsilon: 0.0100
Episode 980, Total Reward: 273.53, Average Max Q-Value: 104.5380, Epsilon: 0.0100
Episode 990, Total Reward: 285.15, Average Max Q-Value: 104.4497, Epsilon: 0.0100
Episode 1000, Total Reward: 292.27, Average Max Q-Value: 102.6706, Epsilon: 0.0100
[Validation @ ep 1000] mean=292.52 median=297.60 std=14.67 solved=100%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 132.68
Reward Variance: 24302.56
Final Moving-Avg Reward (w=50): 246.90
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### training_run_seed42.log
```text
New best moving-avg reward: 230.05 (over last 50 episodes). Weights saved to weights.pth.
Episode 790, Total Reward: 161.77, Average Max Q-Value: 121.4600, Epsilon: 0.0191
New best moving-avg reward: 230.40 (over last 50 episodes). Weights saved to weights.pth.
New best moving-avg reward: 233.60 (over last 50 episodes). Weights saved to weights.pth.
Episode 800, Total Reward: 278.69, Average Max Q-Value: 125.1475, Epsilon: 0.0181
Episode 810, Total Reward: 260.30, Average Max Q-Value: 126.5534, Epsilon: 0.0172
Episode 820, Total Reward: 239.40, Average Max Q-Value: 126.3219, Epsilon: 0.0164
Episode 830, Total Reward: 23.39, Average Max Q-Value: 124.2520, Epsilon: 0.0156
Episode 840, Total Reward: -5.30, Average Max Q-Value: 122.8539, Epsilon: 0.0148
Episode 850, Total Reward: 54.88, Average Max Q-Value: 121.1886, Epsilon: 0.0141
Episode 860, Total Reward: 12.08, Average Max Q-Value: 120.1206, Epsilon: 0.0134
Episode 870, Total Reward: -61.56, Average Max Q-Value: 118.7952, Epsilon: 0.0128
Episode 880, Total Reward: -11.46, Average Max Q-Value: 115.8494, Epsilon: 0.0121
Episode 890, Total Reward: 261.64, Average Max Q-Value: 116.2933, Epsilon: 0.0115
Episode 900, Total Reward: 23.15, Average Max Q-Value: 117.3110, Epsilon: 0.0110
Episode 910, Total Reward: -15.56, Average Max Q-Value: 115.9765, Epsilon: 0.0104
Episode 920, Total Reward: -94.66, Average Max Q-Value: 111.0531, Epsilon: 0.0100
Episode 930, Total Reward: -342.12, Average Max Q-Value: 106.1684, Epsilon: 0.0100
Episode 940, Total Reward: 273.96, Average Max Q-Value: 100.8057, Epsilon: 0.0100
Episode 950, Total Reward: 73.18, Average Max Q-Value: 95.5724, Epsilon: 0.0100
Episode 960, Total Reward: 283.80, Average Max Q-Value: 98.5763, Epsilon: 0.0100
Episode 970, Total Reward: -50.00, Average Max Q-Value: 97.3741, Epsilon: 0.0100
Episode 980, Total Reward: 54.60, Average Max Q-Value: 96.6219, Epsilon: 0.0100
Episode 990, Total Reward: 295.04, Average Max Q-Value: 97.0263, Epsilon: 0.0100
Episode 1000, Total Reward: 53.01, Average Max Q-Value: 99.4414, Epsilon: 0.0100
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 86.08
Reward Variance: 22323.96
Final Moving-Avg Reward (w=50): 179.80
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```

### training_run_validation.log
```text
[Validation @ ep 800] mean=234.67 median=284.68 std=102.09 solved=80%
Episode 810, Total Reward: 272.42, Average Max Q-Value: 84.7322, Epsilon: 0.0172
Episode 820, Total Reward: 262.00, Average Max Q-Value: 86.9481, Epsilon: 0.0164
Episode 830, Total Reward: 29.60, Average Max Q-Value: 89.2231, Epsilon: 0.0156
Episode 840, Total Reward: 268.99, Average Max Q-Value: 92.3195, Epsilon: 0.0148
Episode 850, Total Reward: 276.28, Average Max Q-Value: 93.7160, Epsilon: 0.0141
[Validation @ ep 850] mean=252.14 median=286.06 std=76.57 solved=80%
Episode 860, Total Reward: 253.32, Average Max Q-Value: 95.1612, Epsilon: 0.0134
Episode 870, Total Reward: 218.91, Average Max Q-Value: 96.5292, Epsilon: 0.0128
Episode 880, Total Reward: 264.19, Average Max Q-Value: 97.2190, Epsilon: 0.0121
Episode 890, Total Reward: 272.29, Average Max Q-Value: 98.6256, Epsilon: 0.0115
Episode 900, Total Reward: 292.22, Average Max Q-Value: 98.6015, Epsilon: 0.0110
[Validation @ ep 900] mean=281.71 median=297.01 std=35.98 solved=90%  <- NEW BEST (saved)
Episode 910, Total Reward: 267.27, Average Max Q-Value: 99.5904, Epsilon: 0.0104
Episode 920, Total Reward: 277.95, Average Max Q-Value: 99.7292, Epsilon: 0.0100
Episode 930, Total Reward: 273.73, Average Max Q-Value: 100.7088, Epsilon: 0.0100
Episode 940, Total Reward: 296.16, Average Max Q-Value: 101.2376, Epsilon: 0.0100
Episode 950, Total Reward: 295.34, Average Max Q-Value: 101.9003, Epsilon: 0.0100
[Validation @ ep 950] mean=292.87 median=294.48 std=16.10 solved=100%  <- NEW BEST (saved)
Episode 960, Total Reward: 302.54, Average Max Q-Value: 104.1461, Epsilon: 0.0100
Episode 970, Total Reward: 284.96, Average Max Q-Value: 103.9500, Epsilon: 0.0100
Episode 980, Total Reward: 273.53, Average Max Q-Value: 104.5380, Epsilon: 0.0100
Episode 990, Total Reward: 285.15, Average Max Q-Value: 104.4497, Epsilon: 0.0100
Episode 1000, Total Reward: 292.27, Average Max Q-Value: 102.6706, Epsilon: 0.0100
[Validation @ ep 1000] mean=292.52 median=297.60 std=14.67 solved=100%
==============================
Training Phase Completed!
Total Episodes (Tests): 1000
Mean Reward: 132.68
Reward Variance: 24302.56
Final Moving-Avg Reward (w=50): 246.90
Final Epsilon: 0.0100
==============================
Training metrics saved to training_metrics.json.
Training plot saved to training_plot.png.
```
