# KKBox Cohort Retention Analysis

I picked KKBox specifically because I wanted a retention project built on real production-scale data, not a simulated event log. That decision made the project considerably more painful than it needed to be — the listening logs alone run to hundreds of millions of rows — but I think it's the more honest version of what a retention analysis actually involves.

## Why I didn't just use the churn labels

KKBox's competition comes with pre-built churn labels, and the easy path would've been to treat those as ground truth. I didn't want to do that. The labels are defined around subscription renewal windows, which conflates "stopped listening" with "stopped paying" — those aren't the same thing, and for a retention analysis I cared more about actual listening behavior. So instead I built retention straight from the daily activity logs: a user counts as retained in a given month if they logged at least one day of listening in it. It's a more direct measure, even if it's more work to build.

## Cohorts and the activation/retention split

Users are grouped by registration month (Jan 2015 – Mar 2017). Within each cohort, I split the question into two stages:

- **Activation** — did the user listen at all during their registration month (Month 0)?
- **Retention** — of the users who activated, how many come back in Month 1, 3, 6, 12?

Splitting it this way matters because a cohort's total registration count isn't the right denominator for a retention curve — you want to know what happens to the people who actually engaged in the first place.

## Getting the data into a usable shape

This ended up being most of the actual engineering work. The raw logs don't fit comfortably in memory, so I built a chunked pipeline: read a million rows at a time, aggregate each chunk down to partial user-month summaries, write to Parquet, repeat. Before running it on the full 27-month history I validated it against just the March 2017 file (the smaller of the two log files) — checked that active-day counts never exceeded the days in the month, and specifically checked whether the same user-month was getting split across chunk boundaries (it was, occasionally, so I added a consolidation pass to merge those back together before trusting the numbers).

Once that was validated, I ran the same pipeline against the full history and consolidated it month by month rather than trying to hold everything in memory at once.

Somewhere in the middle of this I also found about 46,671 user-month records (0.17% of the data) with physically impossible listening-time totals — more seconds of listening than exist in the days available. Rather than silently including or dropping them, I set them to missing specifically for listening-time calculations and kept the underlying activity records intact for everything else.

## What the retention curve actually looks like

Activation is high — 84.0% of registered users listen at least once in their registration month. Retention drops off fast after that:

| Month | Retention |
|---|---:|
| M1 | 25.4% |
| M3 | 13.3% |
| M6 | 11.8% |
| M12 | 11.2% |

Most of the loss happens in that first month-to-month transition, then the curve flattens. That's the single most useful thing this analysis produced — if you're only going to intervene once, the window right after activation is where it matters.

![Retention Heatmap](outputs/figures/retention_heatmap.png)

## The early-engagement pattern

I wanted to know whether *how much* someone listened in Month 0 predicted whether they'd stick around, not just whether they listened at all. Since users register at different points in the calendar month, raw active-day counts aren't comparable across users — someone who registers on the 28th only has a few days to rack up activity. So I normalized: active days ÷ calendar days actually available since registration, capped at 100% for a handful of edge cases where the raw data didn't cooperate.

The relationship is steep:

| Normalized Month-0 activity | M1 Retention |
|---|---:|
| ≤10% | 5.9% |
| 11–25% | 12.3% |
| 26–50% | 33.4% |
| 51–75% | 64.6% |
| 76–100% | 80.6% |

That's a 74.7-point gap between the top and bottom bands — roughly 13.7x — and it holds up all the way to Month 12, where the top two bands still retain 31.6–35.0% of users versus 2–5% for the bottom two.

To be clear about what this isn't: this is an association, not a causal claim. Users who happen to engage heavily in their first month are probably different in ways I can't observe — more interested in the product to begin with, better matched by whatever brought them there, etc. I'd want a real intervention test (e.g., an onboarding nudge) before concluding that pushing early activity would cause the same retention lift.

## Acquisition channel and transaction data — two things worth flagging

Registration channels look pretty similar at the activation stage (80–89% across the major ones), but downstream retention diverges hard — the largest channel sits at 14.4% M1 retention while another (anonymized as Channel 7) reaches 88.6% among activated users. Volume and quality clearly aren't the same thing here, even though `registered_via` is anonymized so I can't say *why* channels differ, just that they do.

I also looked at transaction data (plan type, auto-renew) as a possible retention signal, but had to be careful with it — only a subset of activated users have an observed transaction within 30 days of registering, and that subgroup retains at 89.5% versus 25.4% for the full population. That's a huge selection effect. Users who show up in the transaction data are already the ones sticking around, so I'm not treating transaction-based comparisons as representative of the whole population — I'm flagging that limitation directly rather than glossing over it.

## What I'd tell a product team

1. **The Month 0 → Month 1 transition is where almost all the loss happens.** That's where onboarding investment should go.
2. **Look at depth of early activity, not just whether someone showed up once.** A single Month-0 session and five days of Month-0 activity predict very different outcomes.
3. **Don't judge acquisition channels by volume alone** — the retention numbers tell a very different story than registration counts do.
4. **This is observational, not causal.** Before acting on the engagement finding, I'd want a real test, not just a strong correlation.

## Data

**Source:** [WSDM - KKBox's Churn Prediction Challenge — Kaggle](https://www.kaggle.com/competitions/kkbox-churn-prediction-challenge/overview)

Raw competition files aren't included here — pull them from Kaggle directly and follow the competition's usage terms. The logs cover January 2015 through March 2017 and run into the hundreds of millions of rows; they get processed in chunks and consolidated down to one row per user-month before any of the retention analysis happens.

## Repo layout

```text
kkbox-retention-analysis/
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_cohort_retention_analysis.ipynb
├── data/
│   ├── raw/                  # not included — get from Kaggle
│   └── processed/            # generated intermediate output
└── README.md
```

## Running it

Needs pandas, NumPy, Matplotlib, and a Parquet engine (pyarrow). Fair warning: `01_data_preparation.ipynb` is genuinely slow to run end to end because it's working through the full listening history — I kept the executed outputs in the notebooks so the pipeline is inspectable without requiring anyone to rerun a multi-hour job just to see what it produced.

## What this analysis can't establish

It's observational — none of this proves causality. Later cohorts naturally have shorter follow-up windows since the data cuts off in March 2017. A small number of listening records predate the recorded registration date and get excluded. Physically implausible listening-time values are treated as missing rather than real. Transaction-based comparisons only apply to a selected subgroup, not the full population. And `registered_via` being anonymized means I can describe channel differences but can't explain their cause.
