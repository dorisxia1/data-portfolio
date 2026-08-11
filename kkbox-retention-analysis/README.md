# KKBox Cohort Retention Analysis

## Project Overview

This project analyzes longitudinal listening behavior from the KKBox
churn-prediction dataset to understand how user retention evolves after
registration and which early behaviors are associated with stronger
long-term engagement.

Rather than treating churn labels as the primary outcome, the project
constructs behavioral retention directly from monthly listening
activity. A user is considered retained in a month when they record at
least one day of listening activity during that month.

## Business Questions

-   How quickly does retention decline after initial activation?
-   How much do registration cohorts differ in post-activation
    retention?
-   Is deeper engagement during the registration month associated with
    stronger future retention?
-   Do acquisition channels differ in downstream user quality?
-   Can transaction attributes add useful retention information without
    introducing selection bias?

## Data

**Source:** [WSDM - KKBox's Churn Prediction Challenge — Kaggle](https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge/overview)

The analysis uses KKBox competition data, including member registration
records, daily listening logs, transaction histories, and churn labels.

Raw competition data are **not included in this repository**. Users
should obtain the data directly from the original Kaggle competition and
comply with its competition rules.

The listening logs span January 2015 through March 2017 and contain
hundreds of millions of daily activity records. They are processed in
chunks and consolidated into one row per user-month before analysis.

## Methodology

### Cohort definition

Users are grouped by registration month from January 2015 through March
2017.

### Activation

A registered user is considered activated when they record listening
activity during Month 0, their registration month.

### Retention

Post-activation retention measures the share of Month-0 activated users
who record listening activity in a later cohort month.

### Early engagement

Because users registering late in a calendar month have fewer possible
active days, Month-0 engagement is normalized as:

**active days / calendar days available after registration**

The measure is capped at 100% for a very small number of inconsistent
records.

## Key Findings

-   **84.0% of eligible registered users activate in Month 0.**
-   Weighted post-activation retention falls to **25.4% at M1**, **13.3%
    at M3**, **11.8% at M6**, and **11.2% at M12**.
-   Month-1 retention rises sharply with normalized early engagement:
    -   ≤10% of available days active: **5.9%**
    -   11--25%: **12.3%**
    -   26--50%: **33.4%**
    -   51--75%: **64.6%**
    -   76--100%: **80.6%**
-   The M1 retention gap between the highest- and lowest-engagement
    groups is **74.7 percentage points**, or approximately **13.7×**.
-   The relationship persists through M12: the two highest-engagement
    groups retain roughly **31.6%--35.0%**, compared with about
    **2%--5%** for the two lowest-engagement groups.
-   Major acquisition channels have relatively similar activation rates
    but dramatically different downstream retention. The largest channel
    has **14.4% M1 retention**, while Channel 7 reaches **88.6%** among
    activated users.
-   Transaction data cover only a selected subgroup. Users with a
    transaction observed within 30 days have **89.5% M1 retention**
    versus **25.4%** overall, so transaction-based comparisons are not
    treated as population-level estimates.

## Business Recommendations

1.  **Prioritize the Month-0 to Month-1 transition.** The largest
    retention loss occurs immediately after activation.
2.  **Measure onboarding depth, not activation alone.** Repeated
    activity during the first available days is much more informative
    than a binary activation event.
3.  **Evaluate acquisition channels on downstream quality.**
    Registration volume can obscure large differences in early
    engagement and retention.
4.  **Experiment rather than infer causality.** Early engagement is
    strongly associated with retention, but observational results do not
    establish that forcing additional activity will cause the same
    retention gains.

## Repository Structure

``` text
kkbox-retention-analysis/
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_cohort_retention_analysis.ipynb
├── data/
│   ├── raw/                  # ignored; obtain from Kaggle
│   └── processed/            # generated intermediate outputs
└── README.md
```

## Technical Highlights

-   Memory-safe processing of hundreds of millions of listening-log rows
-   Chunked CSV ingestion with pandas
-   Parquet-based intermediate storage
-   User-month aggregation
-   Registration-cohort construction
-   Cohort retention matrices and heatmaps
-   Exposure-normalized early-engagement segmentation
-   Data-quality validation for implausible listening-time values
-   Selection-bias checks for transaction-based analysis

## Important Limitations

The analysis is observational and does not establish causal effects.
Later cohorts have shorter follow-up windows. A small number of
pre-registration activity records are excluded. Physically implausible
listening-time values are treated as missing for listening-time
comparisons. Transaction data represent a strongly selected subgroup.
`registered_via` is anonymized, so acquisition-channel mechanisms cannot
be identified from the supplied data.

## Environment

Python with pandas, NumPy, Matplotlib, and a Parquet engine such as
`pyarrow`.

The full data-preparation notebook is computationally expensive because
the original listening history contains hundreds of millions of rows.
Executed notebook outputs can be retained in the portfolio version so
reviewers can inspect the completed pipeline without rerunning the
raw-data processing.
