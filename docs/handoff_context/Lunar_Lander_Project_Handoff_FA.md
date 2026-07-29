# گزارش تحویل پروژه Lunar Lander DQN

**تاریخ تهیه:** 2026-07-26  
**هدف:** این فایل برای شروع یک گفت‌وگوی جدید با ChatGPT یا ادامه کار با Codex تهیه شده است. ابتدا کل فایل خوانده شود و سپس پیش از هر تغییری، وضعیت واقعی Git و فایل‌ها بررسی شود.

---

## 1) خلاصه اجرایی

پروژه یک عامل DQN برای `LunarLander-v2` است. یک Baseline معتبر و قوی ساخته، ارزیابی و در Git ثبت شده است. سپس چهار آزمایش کنترل‌شده انجام شد:

1. Double DQN با Replay Buffer برابر 10,000
2. Double DQN با Replay Buffer برابر 50,000
3. Dueling DQN با Bellman Target وانیلا
4. Vanilla DQN با Learning Rate برابر `5e-4`

نتیجه مهم تا این لحظه:

- **Baseline با `lr=1e-3`** سریع‌ترین و کم‌Timeoutترین سیاست است.
- **Vanilla با `lr=5e-4`** بهترین میانگین Reward و کمترین شکست منفی را دارد، اما Hover/Timeout آن زیاد است.
- Double DQN فقط بهبود جزئی و ناپایدار داشت و رفتار طولانی‌تر ایجاد کرد.
- Replay Buffer برابر 50,000 به‌وضوح شکست خورد.
- Dueling DQN به‌تنهایی از Baseline بهتر نشد.
- Final holdout با Seedهای `10000–10099` هنوز اجرا نشده و باید تا تثبیت تنظیمات دست‌نخورده بماند.

---

## 2) تقسیم وظایف و قرارداد کاری

### نقش کاربر

- تمام دستورات WSL، Python، Training، Benchmark و Git را شخصاً اجرا می‌کند.
- خروجی دستورات، Logها و JSONهای موردنیاز را برای تحلیل می‌فرستد.
- هیچ Final Holdout یا Commit مهمی را بدون تصمیم قبلی اجرا نمی‌کند.

### نقش ChatGPT

- مدیر آزمایش و حافظه تحلیلی پروژه است.
- آزمایش بعدی را طراحی می‌کند، معیارهای پذیرش را از قبل مشخص می‌کند و نتایج را با Baseline مقایسه می‌کند.
- دستورات دقیق و قابل کپی برای کاربر می‌نویسد.
- Prompt کوتاه و دقیق برای Codex آماده می‌کند.
- کد Codex را دوباره خط‌به‌خط بازبینی نمی‌کند، مگر اینکه خروجی‌ها یا خطاها نشانه مشکل باشند.
- نباید ادعا کند به مسیرهای محلی WSL دسترسی دارد. برای خواندن Logهای محلی باید کاربر فایل را Upload کند یا خروجی را Paste کند.

### نقش Codex در VS Code

- Workspace و فایل‌های پروژه را می‌خواند و درباره پیاده‌سازی فنی مستقلاً تصمیم می‌گیرد.
- فقط فایل‌هایی را که صریحاً اجازه داده شده ویرایش می‌کند.
- **مطلقاً نباید هیچ Command اجرا کند:** Terminal، Shell، Python، Test، Training، Benchmark، Git، Package Installation یا Sandbox.
- بعد از ویرایش فقط گزارش کوتاه شامل فایل تغییرکرده، تغییر دقیق و دستورات پیشنهادی برای اجرای دستی ارائه می‌دهد.
- `game.py` را تغییر نمی‌دهد.
- Artifactهای Baseline را overwrite نمی‌کند.

### متن ثابت برای ابتدای Promptهای Codex

```text
Permanent operating rule:
Do not execute terminal commands, shell commands, Python, tests, training,
benchmarks, Git operations, package installation, or any runtime tool.
You may inspect files and edit only files explicitly authorized.
After editing, report what changed and stop. I will run everything manually.
```

---

## 3) محیط اجرا و مسیرها

### WSL Environment

```bash
source /root/venvs/lunar-lander/bin/activate
```

### Repository

```text
/mnt/e/uni/ai/project/Lunar-Lander
```

### پوشه Runهای ایزوله

```text
/mnt/e/uni/ai/project/runs
```

Runهای موجود طبق آخرین `ls` کاربر:

```text
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019
```

### آرشیو Baseline

```text
/mnt/e/uni/ai/project/Lunar-Lander/local_archive/validated-dqn-baseline
```

### فایل صورت پروژه محلی

```text
/mnt/e/uni/ai/project/Lunar-Lander/project4-lunar-lander-dqn.md
```

این فایل نباید Commit شود. بهتر است در `.git/info/exclude` باقی بماند.

### نکته دسترسی

- Codex ممکن است بتواند مسیرهای محلی بالا را در VS Code بخواند، مشروط به اینکه Workspace دسترسی داشته باشد.
- ChatGPT در گفت‌وگوی جدید فقط با دیدن مسیر نمی‌تواند فایل محلی WSL را بخواند. گزارش، Log یا JSON باید Upload شود یا خروجی دستور Paste شود.

---

## 4) وضعیت Git ثبت‌شده در این گفتگو

Baseline معتبر قبلاً ثبت شده است:

```text
Baseline commit on ehsan: c1c57aa
Merge commit on main:     265dc8d
Tag:                      dqn-baseline-v1
Repository:               https://github.com/AIDGH/Lunar-Lander.git
```

Branchهای ساخته‌شده در طول کار:

```text
main
ehsan
experiment/double-dqn
experiment/dueling-dqn
experiment/vanilla-lr5e-4
```

ممکن است Stashهایی برای تغییرات Double یا Dueling وجود داشته باشد، ولی این موضوع در پایان گفتگو دوباره تأیید نشده است.

### اولین بررسی در جلسه بعد

```bash
source /root/venvs/lunar-lander/bin/activate
cd /mnt/e/uni/ai/project/Lunar-Lander

git branch --show-current
git status --short
git stash list
git log --oneline --decorate -8
```

**هیچ Branch یا Stash نباید بر اساس حدس حذف شود.**

---

## 5) Baseline معتبر

### الگوریتم

Vanilla DQN با:

- شبکه `8 → 128 → 128 → 4`
- تعداد پارامتر تقریبی: `18,180`
- Replay Buffer
- Epsilon-greedy
- Policy Network و Target Network
- Huber Loss
- Gradient Clipping
- Hard Target Update هر 1000 Learning Step

### Hyperparameterها

```text
Episodes:             1000
Batch size:           64
Gamma:                0.99
Adam learning rate:   1e-3
Replay capacity:      10,000
Epsilon decay:        0.995
Minimum epsilon:      0.01
Training seed:        42
```

### Validation و Checkpoint

- Validation هر 50 اپیزود
- 10 اپیزود با Seedهای `901–910`
- انتخاب بهترین Checkpoint بر اساس Validation mean و سپس solved-rate
- بهترین Checkpoint: اپیزود 950
- Validation mean: `292.8741`
- Validation solved: `100%`
- Final moving average: حدود `246.90`

### محدودیت پروتکل Validation

یک مجموعه ثابت 10-Seed در 20 نوبت بررسی شده است؛ بنابراین احتمال overfitting در انتخاب Checkpoint وجود دارد. هنگام مقایسه الگوریتم‌ها این پروتکل ثابت نگه داشته شد تا عامل مخدوش‌کننده جدید اضافه نشود، ولی نباید Validation داخلی به‌تنهایی معیار نهایی باشد.

### Benchmarkهای Baseline

#### Benchmark A — Seedهای 1234 تا 1283، تعداد 50

```text
Mean:          226.52
Median:        269.24
Std:           106.42
Solved:        78%
Low (<0):      10%
Mean length:   209.5
Timeouts:      0/50
```

#### Benchmark B — Seedهای 5000 تا 5099، تعداد 100

```text
Mean:          224.78
Median:        265.93
Std:           101.48
Solved:        80%
Low (<0):      8%
Mean length:   226.9
Timeouts:      3/100
```

#### ترکیبی

```text
Combined mean:         225.36
Combined solved rate:  79.33%
Combined low rate:     8.67%
Combined mean length:  221.1
Timeouts:              3/150
```

---

## 6) آزمایش‌های انجام‌شده و نتایج

### جدول خلاصه

| Configuration | Combined Mean | Solved | Low | Mean Length | Timeouts / 150 | تصمیم |
|---|---:|---:|---:|---:|---:|---|
| Vanilla, lr=1e-3 | 225.36 | 79.33% | 8.67% | **221.1** | **3** | Baseline معتبر |
| Double DQN, buffer=10k | 227.46 | **81.33%** | 4.00% | 312.5 | 11 | بهبود جزئی، Hover زیاد، برنده قطعی نیست |
| Double DQN, buffer=50k | 186.74 | 62.67% | 4.67% | 282.0 | 9 | رد کامل |
| Dueling DQN | 221.78 | 74.67% | 2.00% | 319.1 | 16 | رد |
| **Vanilla, lr=5e-4** | **240.36** | 80.67% | **0.00%** | 333.0 | 14 | بهترین Reward؛ Candidate اصلی ولی کند |

---

### 6.1 Double DQN، Buffer 10,000

**Run:**

```text
/mnt/e/uni/ai/project/runs/double-dqn-seed42-20260726-182745
```

**تغییر واحد:** Target Double DQN؛ تمام تنظیمات دیگر Baseline.

Training:

```text
Best validation mean:     282.6155
Best validation solved:   100%
Best checkpoint episode:  750
Final moving average:     149.58
```

Benchmark A:

```text
Mean 200.70 | Solved 76% | Low 8% | Std 129.15 | Length 281.8 | Timeouts 2
```

Benchmark B:

```text
Mean 240.84 | Solved 84% | Low 2% | Std 71.25 | Length 327.9 | Timeouts 9
```

**برداشت:** شکست‌های منفی کمتر شد، اما نتیجه بین دو Benchmark ناسازگار بود و Hover/Timeout افزایش یافت. به‌تنهایی جایگزین Baseline نشد.

---

### 6.2 Double DQN، Buffer 50,000

**Run:**

```text
/mnt/e/uni/ai/project/runs/double-dqn-buffer50k-seed42-20260726-185530
```

**تغییر واحد نسبت به Double قبلی:** Replay Buffer از 10,000 به 50,000.

Training:

```text
Best validation mean:     256.02
Best validation solved:   90%
Best checkpoint episode:  1000
Final moving average:     159.61
```

Benchmark A:

```text
Mean 175.97 | Solved 60% | Low 10% | Length 285.8 | Timeouts 3
```

Benchmark B:

```text
Mean 192.12 | Solved 64% | Low 2% | Length 280.1 | Timeouts 6
```

**برداشت:** افزایش Buffer عملکرد را به‌شدت کاهش داد و مشکل Hover را حل نکرد. این Configuration رد شد. این مقایسه برای بخش Hyperparameter Tuning گزارش ارزشمند است.

---

### 6.3 Dueling DQN با Vanilla Target

**Run:**

```text
/mnt/e/uni/ai/project/runs/dueling-dqn-seed42-20260726-191220
```

**تغییر واحد:** خروجی شبکه به Value Head و Advantage Head تبدیل شد؛ Bellman Target وانیلا باقی ماند.

Architecture:

```text
Shared trunk:   8 → 128 → 128
Value head:     128 → 1
Advantage head: 128 → 4
Aggregation:    Q = V + A - mean(A)
Parameters:     تقریباً 18,309، یعنی 129 پارامتر بیشتر
```

Training:

```text
Best validation mean:     240.1585
Best validation solved:   70%
Best checkpoint episode:  700
Final moving average:     131.07
```

Benchmark A:

```text
Mean 223.43 | Solved 76% | Low 2% | Length 315.1 | Timeouts 5
```

Benchmark B:

```text
Mean 220.95 | Solved 74% | Low 2% | Length 321.1 | Timeouts 11
```

**برداشت:** سقوط‌های شدید کمتر شد، ولی solved-rate پایین آمد و Timeout زیاد شد. Dueling مستقل موفق نبود؛ بنابراین فعلاً D3QN اولویت ندارد.

---

### 6.4 Vanilla DQN با Learning Rate برابر 5e-4

**Run:**

```text
/mnt/e/uni/ai/project/runs/vanilla-lr5e-4-seed42-20260726-193019
```

**تغییر واحد:** Adam Learning Rate از `1e-3` به `5e-4`؛ الگوریتم، معماری، Buffer و پروتکل بدون تغییر.

Training:

```text
Best validation mean:     246.6868
Best validation solved:   80%
Best checkpoint episode:  800
Final moving average:     175.72
```

Validation پس از اوج دوباره افت کرد؛ بنابراین Learning Rate کمتر ناپایداری بعد از اوج را کاملاً حل نکرد.

Benchmark A:

```text
Mean:          251.12
Median:        271.88
Std:           57.30
Solved:        84%
Low:           0%
Mean length:   331.6
Timeouts:      3/50
No-op:         39.4%
```

Benchmark B:

```text
Mean:          234.98
Median:        262.15
Std:           70.43
Solved:        79%
Low:           0%
Mean length:   333.7
Timeouts:      11/100
No-op:         39.4%
```

**برداشت:** اولین بهبود واضح در Mean روی هر دو Benchmark و حذف کامل Reward منفی بود. مشکل اصلی آن Hover، No-op زیاد، طول اپیزود بالا و Timeout است. این مدل Candidate اصلی فعلی است، ولی هنوز برنده نهایی نیست.

---

## 7) نتیجه تحلیلی تا این لحظه

### چیزهایی که تقریباً می‌دانیم

1. ظرفیت شبکه عامل اصلی محدودیت نیست؛ مدل بارها Reward بالای 300 تولید کرده است.
2. پیچیده‌ترکردن معماری به‌تنهایی مشکل را حل نکرد.
3. Double و Dueling شکست‌های منفی را به رفتارهای طولانی و نامطمئن تبدیل کردند.
4. Replay Buffer برابر 50,000 برای این پروتکل بدتر بود.
5. کاهش Learning Rate به `5e-4` کیفیت Reward و reliability را به‌وضوح بهتر کرد.
6. مشکل بعدی محدود و مشخص است: حفظ Reward بالای مدل `5e-4` و کاهش Hover/Timeout.
7. یک Training seed برای نتیجه نهایی کافی نیست؛ ولی ابتدا باید Configuration بهتر انتخاب شود، سپس با چند Seed آموزش تکرار شود.

### چیزهایی که هنوز قطعی نیست

- علت دقیق افت پس از Checkpointهای خوب
- میزان حساسیت هر Configuration به Training seed
- اینکه Target Update کندتر واقعاً Hover را کاهش می‌دهد یا نه
- عملکرد نهایی روی Final Holdout

---

## 8) داده‌ها و Artifactهای اصلی

### Repository Root

طبق آخرین `ls`:

```text
README.md
agent.py
model.py
train.py
test.py
game.py
random_agent.py
requirements.txt
weights.pth
training_metrics.json
training_plot.png
diagnostic_report_validation.json
diagnostic_report_unseen_100.json
project4-lunar-lander-dqn.md
local_archive/
```

Artifactهای Root مربوط به Baseline معتبر هستند و نباید توسط آزمایش‌های جدید overwrite شوند.

### داخل هر Run

معمولاً فایل‌های زیر وجود دارند:

```text
training_run_*.log
training_metrics_*.json
training_plot_*.png
weights_*.pth
*_benchmark_a*.json
*_benchmark_a.log
*_benchmark_b*.json
*_benchmark_b.log
```

برای تحلیل کامل، JSONهای Diagnostic از خلاصه Log بهترند، ولی Logها برای مشاهده روند و Validation history لازم‌اند.

---

## 9) پیشنهاد فنی مشخص برای جلسه بعد

### آزمایش بعدی پیشنهادی

از Candidate فعلی شروع شود:

```text
Vanilla DQN
Learning rate = 5e-4
Target update interval: 1000 → 2000 learning steps
تمام عوامل دیگر ثابت
Training seed = 42
Episodes = 1000
```

### فرضیه

Target Network دیرتر به‌روزرسانی شود تا جهش Targetها کمتر شود و رفتار پس از نقطه اوج باثبات‌تر گردد. این فرضیه قطعی نیست و باید با یک آزمایش تک‌عاملی بررسی شود.

### معیار پذیرش از پیش تعیین‌شده

```text
Combined mean:          حداقل 235
Combined solved:        حداقل 80%
Combined low:           حداکثر 2%
Mean episode length:    ترجیحاً زیر 280
Timeouts over 150:      حداکثر 7
هر دو Benchmark:        بدون افت شدید مستقل
```

اگر Mean کمی کمتر از `240.36` شود ولی Timeout به شکل واضح کاهش پیدا کند، ممکن است Configuration جدید از نظر کلی بهتر باشد.

### ترتیب پیشنهادی ادامه

1. وضعیت Git و Branchها را تأیید کنید.
2. تغییر `lr=5e-4` را روی Branch خودش حفظ کنید؛ حذف یا overwrite نشود.
3. Branch فرزند برای Target Update 2000 بسازید.
4. Codex فقط محل Effective target-update را پیدا و همان یک مقدار را تغییر دهد؛ هیچ Command اجرا نکند.
5. Training و Benchmark A/B در Run Directory جدید انجام شود.
6. Candidate برتر بین Baseline، `lr=5e-4` و `lr=5e-4 + target2000` انتخاب شود.
7. Configuration برتر با حداقل دو Training seed دیگر مانند `123` و `2026` تکرار شود.
8. بعد از Freeze کامل، Final Holdout `10000–10099` دقیقاً یک بار اجرا شود.

---

## 10) قواعد غیرقابل‌تغییر

- `game.py` فایل استاد است و نباید تغییر کند.
- هر آزمایش باید فقط یک عامل را تغییر دهد.
- Training در Repository Root اجرا نشود؛ چون Artifactهای Baseline را overwrite می‌کند.
- هر Training در پوشه Timestamped زیر `/mnt/e/uni/ai/project/runs/` اجرا شود.
- Seedهای Benchmark A و B دیگر Unseen محسوب نمی‌شوند؛ آن‌ها Benchmarkهای شناخته‌شده‌اند.
- Final Holdout فقط `10000–10099` است و تا Freeze نهایی اجرا نمی‌شود.
- نتیجه ضعیف با افزایش هم‌زمان Episode count جبران نشود؛ چون attribution از بین می‌رود.
- Configuration جدید فقط با Validation داخلی انتخاب نشود؛ Benchmark A/B و reliability metrics نیز لازم‌اند.

---

## 11) پیشنهاد نهایی درباره سیستم کاری

### توصیه: کاربر + ChatGPT + Codex را حفظ کنید

فقط کارکردن با Codex توصیه نمی‌شود. Codex برای خواندن Workspace و اعمال تغییر دقیق عالی است، اما نگهداری تاریخچه آزمایش‌ها، طراحی معیارهای پذیرش، جلوگیری از تغییر هم‌زمان چند عامل و تحلیل مقایسه‌ای را بهتر است یک ChatGPT جداگانه مدیریت کند.

### سیستم پیشنهادی کم‌هزینه و مؤثر

- **یک ChatGPT اصلی** فقط برای مدیریت پروژه، تحلیل نتایج و نوشتن Promptهای Codex.
- **Codex** فقط برای Inspection و Edit محدود.
- **کاربر** فقط برای اجرای دستی و ارسال Summary/JSON.

برای جلوگیری از طولانی‌شدن ChatGPT:

1. در شروع گفت‌وگوی جدید همین گزارش Upload شود.
2. فقط Summary خروجی‌ها و JSONهای مهم Upload شوند، نه همه خطوط اپیزودها مگر هنگام خطا.
3. هر مرحله یک تصمیم و یک Prompt Codex داشته باشد.
4. ChatGPT بعد از هر آزمایش جدول مرکزی نتایج را به‌روزرسانی کند.
5. هر 3 تا 5 آزمایش یک Handoff Report جدید ساخته شود.

---

## 12) متن آماده برای شروع ChatGPT جدید

```text
این فایل Handoff گزارش کامل پروژه Lunar Lander من است. ابتدا کل آن را بخوان.

نقش تو مدیر آزمایش و تحلیل‌گر است. من تمام Commandها را دستی اجرا می‌کنم.
Codex فقط فایل‌های مجاز را ویرایش می‌کند و مطلقاً هیچ Command، Python، Test،
Training، Benchmark، Git یا Package Installation اجرا نمی‌کند.

قبل از پیشنهاد تغییر جدید:
1. وضعیت فعلی، Baseline، Runها و معیارهای ثبت‌شده در گزارش را خلاصه کن.
2. از من خروجی git branch/status/stash را بخواه یا خروجی موجود را تحلیل کن.
3. Final holdout یعنی seeds 10000–10099 را دست‌نخورده نگه دار.
4. هر بار فقط یک عامل را تغییر بده.

Candidate فعلی Vanilla DQN با lr=5e-4 است:
combined mean=240.36, solved=80.67%, low=0%, mean length=333.0,
timeouts=14/150.

آزمایش بعدی پیشنهادی target-update 1000→2000 با حفظ lr=5e-4 است، اما ابتدا
وضعیت Git را بررسی و سپس مستقل ارزیابی کن که این هنوز بهترین قدم بعدی است یا نه.
```

---

## 13) اولین Command پیشنهادی در جلسه بعد

```bash
source /root/venvs/lunar-lander/bin/activate
cd /mnt/e/uni/ai/project/Lunar-Lander

echo "=== BRANCH ==="
git branch --show-current

echo "=== STATUS ==="
git status --short

echo "=== STASHES ==="
git stash list

echo "=== RECENT COMMITS ==="
git log --oneline --decorate -8
```

خروجی این بلوک باید پیش از هر Branch، Commit، Stash pop یا تغییر Codex بررسی شود.
