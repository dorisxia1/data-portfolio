# Marketing Experiment & Incrementality Analysis

An A/B testing project evaluating whether an advertising campaign generated incremental conversions compared with a PSA control group, and whether the observed lift was large enough to justify continued investment.

The analysis combines **Python, statistical hypothesis testing, SQL, data visualization, and business sensitivity analysis** to move from experimental results to an actionable campaign recommendation.

---

## Project Overview

Digital marketing experiments often answer a statistical question — *did the treatment outperform the control?* — without answering the more important business question:

> **Was the improvement large enough to justify the investment?**

This project analyzes a marketing experiment in which users were assigned to either:

- **Advertising (`ad`)** — users exposed to the advertising campaign
- **PSA (`psa`)** — users exposed to a public service announcement as the control condition

The primary objective is to determine whether advertising increased conversion and translate the estimated treatment effect into incremental conversions and break-even campaign economics.

Additional exploratory analyses examine whether conversion patterns differ by exposure frequency, day, and hour.

---

## Business Questions

The analysis addresses five questions:

1. Did the advertising campaign significantly increase conversion?
2. How large was the treatment effect in practical terms?
3. How many incremental conversions can be attributed to the advertising condition?
4. Under different values per conversion, how much could the campaign cost before becoming uneconomical?
5. What additional hypotheses can be generated from exposure-frequency and campaign-timing patterns?

---

## Dataset

**Source:** [Marketing A/B Testing — Kaggle](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing)

The dataset contains **588,101 user-level observations**.

| Variable | Description |
|---|---|
| `user id` | Unique user identifier |
| `test group` | Experimental assignment (`ad` or `psa`) |
| `converted` | Whether the user converted |
| `total ads` | Number of campaign exposures recorded for the user |
| `most ads day` | Day on which the user received the most exposures |
| `most ads hour` | Hour during which the user received the most exposures |

After validation:

- 588,101 rows
- 588,101 unique users
- No duplicate user IDs
- No missing values in the analytical fields

The observed experiment allocation was approximately **96% advertising and 4% PSA**. Because the intended allocation probability is not provided with the dataset, this imbalance is documented rather than treated as evidence of sample-ratio mismatch.

---

## Tools & Methods

**Python**
- pandas
- NumPy
- Matplotlib
- statsmodels

**SQL**
- SQLite
- Aggregation
- Conditional logic
- Window functions
- Segmentation

**Statistical methods**
- Two-proportion z-test
- 95% confidence interval for difference in proportions
- Absolute and relative treatment lift
- Incremental conversion estimation
- Break-even sensitivity analysis

---

## Experiment Design

The primary metric is **conversion rate**.

### Hypotheses

**Null hypothesis (H₀):**

The conversion rate is equal between users assigned to advertising and users assigned to PSA.

**Alternative hypothesis (H₁):**

The conversion rates differ between the advertising and PSA conditions.

A two-sided hypothesis test with **α = 0.05** was used.

The primary treatment effect is evaluated using both statistical significance and effect magnitude rather than relying on the p-value alone.

---

## Key Results

| Metric | PSA Control | Advertising |
|---|---:|---:|
| Users | 23,524 | 564,577 |
| Conversions | 420 | 14,423 |
| Conversion Rate | **1.785%** | **2.555%** |

The advertising condition produced:

- **+0.769 percentage points absolute lift**
- **+43.1% relative lift**
- **z-statistic: 7.37**
- **p-value: < 0.001**
- **95% CI for absolute lift: +0.595 to +0.943 percentage points**

The confidence interval lies entirely above zero, providing strong evidence that assignment to advertising increased conversion relative to the PSA condition.

---

## Primary Experiment Result

![Advertising vs. PSA Conversion Rate](outputs/figures/01_conversion_rate_comparison.png)

Users assigned to advertising converted at **2.555%**, compared with **1.785%** for the PSA control.

While the difference is statistically significant, the analysis goes beyond significance testing by estimating the number of conversions generated incrementally by the treatment.

---

## Incremental Conversion Impact

If users in the advertising group had instead converted at the PSA control rate, approximately:

**10,080 conversions**

would have been expected.

The advertising group actually produced:

**14,423 conversions**

This implies approximately:

> **4,343 incremental conversions**

The 95% confidence interval for the treatment effect corresponds to approximately:

> **3,360 to 5,326 incremental conversions**

This translates the statistical treatment effect into a metric that can be used for business decision-making.

---

## Business Significance

The dataset does not provide campaign cost, revenue per conversion, or contribution margin per conversion.

Rather than inventing a single ROI estimate, the analysis uses a **break-even sensitivity analysis**.

For a given value per incremental conversion:

**Break-even campaign cost = estimated incremental conversions × value per incremental conversion**

For example, if an incremental conversion contributes **$100 in business value**:

- Estimated break-even campaign cost: **~$434,000**
- Conservative break-even threshold using the lower 95% confidence bound: **~$336,000**

![Break-Even Campaign Analysis](outputs/figures/02_break_even_analysis.png)

This allows the experimental result to support a real business decision:

> If actual campaign costs fall comfortably below the relevant break-even threshold, continued investment is supported by the experimental evidence.

---

## Exposure Frequency Analysis

The dataset also records the number of exposures accumulated by each user.

Advertising exposure was highly right-skewed:

- Median advertising exposure: **13**
- 99th percentile: **201**
- Maximum observed exposure: **2,065**

Conversion increased substantially across higher exposure-frequency bands.

However, this pattern appeared in **both the advertising and PSA groups**.

![Conversion by Exposure Frequency](outputs/figures/03_exposure_frequency_comparison.png)

For example, advertising-group conversion increased from approximately **0.25% among users with 1–5 exposures** to **17.68% among users with 101–200 exposures**.

But PSA conversion also increased substantially across exposure bands.

This is an important analytical distinction.

`total ads` is an observed **post-assignment variable**, not an independently randomized treatment. Users accumulating many exposures may also be more active, spend more time on the platform, or simply have more opportunities to convert.

Therefore:

> **The analysis does not conclude that showing users more ads causes higher conversion.**

A separate experiment randomizing exposure frequency would be required to estimate diminishing returns or establish an optimal frequency cap.

---

## Campaign Timing Analysis

Conversion was also examined by the day and hour of highest exposure.

The advertising group generally maintained higher observed conversion rates than the PSA group, but the magnitude of the difference varied across timing segments.

Some low-traffic hourly PSA segments contained relatively small samples because only approximately 4% of users belonged to the control condition.

Because exposure timing was not independently randomized, these patterns are treated as **hypothesis-generating rather than causal**.

They could inform future experiments testing whether randomized delivery windows improve campaign efficiency.

---

## Business Recommendation

### Continue the advertising campaign — conditional on campaign economics.

The experiment provides strong evidence that advertising generated incremental conversions:

- Conversion increased from **1.785% to 2.555%**
- Relative lift was approximately **43.1%**
- Approximately **4,343 incremental conversions** were estimated
- The estimated treatment effect remained positive across the entire 95% confidence interval

However, statistical significance does not automatically imply profitability.

The final investment decision should compare:

**Actual campaign cost**

against

**Incremental conversions × contribution value per conversion**

If campaign costs fall comfortably below the corresponding break-even threshold, continued investment is supported.

The exposure-frequency and timing analyses should **not** be used to immediately implement frequency caps or scheduling changes because those variables were not independently randomized.

Instead, they provide hypotheses for future controlled experiments.

---

## Recommended Next Experiments

### 1. Randomized Exposure-Frequency Test

Assign users to predefined advertising-frequency levels to estimate:

- Incremental lift by exposure level
- Diminishing returns
- Marginal conversion value
- Economically efficient frequency caps

### 2. Randomized Campaign-Timing Test

Randomize advertising delivery across time windows to determine whether observed day/hour differences represent genuine treatment-effect heterogeneity.

### 3. Economics-Integrated Experiment

Capture campaign spend and contribution value per conversion alongside experimental outcomes.

This would allow future analyses to estimate:

- Incremental revenue
- Incremental profit
- Cost per incremental conversion
- Experiment-level ROI

---

## Limitations

- Campaign cost and contribution value per conversion are unavailable.
- The intended experimental allocation ratio is undocumented.
- Limited pre-treatment user characteristics are available for additional balance checks.
- Exposure frequency was not independently randomized.
- Day and hour of highest exposure were not independently randomized.
- Some exploratory PSA segments contain relatively small sample sizes because of the 96/4 treatment allocation.

These limitations do not invalidate the primary advertising-versus-PSA comparison, but they constrain the causal interpretation of secondary exposure and timing analyses.

---

## SQL Analysis

The core experiment metrics were also reproduced using SQL.

The SQL analysis includes:

- Treatment-group sample sizes
- Conversion counts
- Conversion rates
- Treatment allocation
- Exposure-frequency segmentation

Statistical inference, including the two-proportion z-test and confidence interval, was performed in Python.

See:

`sql/experiment_metrics.sql`

---

## Project Structure

```text
marketing-experiment-analysis/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── marketing_AB.csv
│   └── processed/
│       └── marketing_ab_clean.csv
│
├── notebooks/
│   └── 01_experiment_analysis.ipynb
│
├── sql/
│   └── experiment_metrics.sql
│
├── findings/
│   └── recommendation.md
│
└── outputs/
    └── figures/
        ├── 01_conversion_rate_comparison.png
        ├── 02_break_even_analysis.png
        ├── 03_exposure_frequency_comparison.png
        └── 04_hourly_conversion_patterns.png
```

---

## Reproducing the Analysis

Clone the repository and install the required Python packages:

```bash
pip install -r requirements.txt
```

Then run:

```text
notebooks/01_experiment_analysis.ipynb
```

The notebook performs the complete workflow from data validation through statistical inference, business sensitivity analysis, exploratory segmentation, and final recommendation.

---

## Key Takeaway

The advertising campaign generated a **statistically significant and practically meaningful increase in conversion**, corresponding to approximately **4,343 incremental conversions**.

The experiment supports continued advertising investment **provided that actual campaign costs are below the economic value generated by those incremental conversions**.

Just as importantly, the secondary analysis demonstrates why strong observational relationships — such as higher conversion among heavily exposed users — should not automatically be interpreted as causal without additional randomization.