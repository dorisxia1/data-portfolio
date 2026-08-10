# Dementia Risk Hotspots Visualization

An interactive county-level visualization exploring where dementia prevalence is higher or lower than expected based on known health risk factors.

![Dementia Risk Hotspots Visualization](images/risk_hotspots_dashboard.png)

## Overview

This visualization explores geographic differences between observed dementia prevalence and the prevalence expected based on underlying health risk factors across U.S. counties.

Using dementia prevalence data from the NORC Dementia DataHub and county-level health measures from CDC PLACES, the analysis estimates expected dementia prevalence and identifies areas where the actual burden is substantially higher or lower than expected.

**Live Demo:** [View the full interactive dashboard](https://dsci-554.github.io/project-vizrd/)

## My Contribution

I designed and implemented the **Risk Hotspots analysis and interactive visualization**, including:

- Developed a regression-based **Mismatch Index** to compare observed dementia prevalence with expected prevalence based on county-level risk factors.
- Integrated dementia prevalence data with CDC PLACES measures for stroke, diabetes, and cognitive disability.
- Built an interactive county-level choropleth visualization to reveal geographic patterns in the mismatch.
- Added state-level highlighting and interactive exploration to make unusually high- or low-mismatch areas easier to identify.

## Key Features

- **County-level choropleth:** Visualizes geographic variation in the Mismatch Index across the United States.
- **Interactive exploration:** Allows users to examine individual areas and their underlying dementia and health-risk measures.
- **Diverging color scale:** Distinguishes areas with higher-than-expected and lower-than-expected dementia prevalence.
- **State-level highlighting:** Draws attention to states where the difference between expected and observed dementia prevalence is particularly large.

## Methodology

The visualization asks a simple question:

> Where is dementia prevalence substantially higher or lower than we would expect given a county's underlying health risk factors?

A linear regression model estimates expected dementia prevalence using county-level prevalence of:

- Stroke
- Diabetes
- Cognitive disability

The **Mismatch Index** is calculated from the difference between observed and predicted dementia prevalence.

- **Positive mismatch:** Dementia prevalence is higher than expected.
- **Negative mismatch:** Dementia prevalence is lower than expected.
- **Near zero:** Observed prevalence is close to the model's expectation.

The resulting metric is joined with county geographic data and displayed as an interactive choropleth map.

The Mismatch Index is intended as an exploratory measure rather than a causal model. Areas with unusually high or low mismatch can highlight geographic patterns that may warrant further investigation.

## Data Sources

### NORC Dementia DataHub

The 2020 Dementia DataHub Public Use File provides national, state, and county-level estimates of dementia-related health outcomes among Medicare beneficiaries. Dementia prevalence was used as the primary outcome for the Risk Hotspots analysis.

**Source:** [NORC at the University of Chicago — Dementia DataHub](https://dementiadatahub.org/)

### CDC PLACES

CDC PLACES provides county-level model-based estimates of chronic disease and health measures. The Risk Hotspots analysis uses prevalence estimates for stroke, diabetes, and cognitive disability as predictors of expected dementia prevalence.

**Source:** [Centers for Disease Control and Prevention — PLACES: Local Data for Better Health](https://www.cdc.gov/places/)

## Technologies

- Python
- Pandas
- Regression Analysis
- Vue.js
- JavaScript
- Mapbox
- HTML/CSS

## Project Structure

```text
dementia-risk-hotspots-visualization/
├── README.md
├── analysis/
│   └── dementia_mismatch_index.py
├── visualization/
│   └── RiskHotspotsView.vue
├── data/
│   └── dementia_mismatch_index.csv
└── images/
    └── risk_hotspots_dashboard.png
```

- analysis/ — Python workflow used to calculate the Mismatch Index.
- visualization/ — Vue component for the interactive Risk Hotspots visualization.
- data/ — Processed county-level data used by the visualization.
- images/ — Screenshot of the completed visualization.

## Project Context

This visualization was originally developed as part of a collaborative USC data visualization project examining dementia burden and health disparities across the United States. The full application contains additional visualizations developed by other team members.

This portfolio project has been simplified to showcase the **analysis, code, and Risk Hotspots visualization that I personally developed**.

**Full Team Project:** [View the interactive dashboard](https://dsci-554.github.io/project-vizrd/)