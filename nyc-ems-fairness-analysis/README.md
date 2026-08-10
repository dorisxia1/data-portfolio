# NYC EMS Fairness Analysis

> A severity-controlled audit of emergency response-time disparities using real-world NYC EMS and demographic data.

This project investigates whether emergency response times differ across New York City neighborhoods after accounting for medical urgency and operational factors.

The analysis focuses on **conditional fairness**: comparing response outcomes across demographic groups for incidents with similar levels of medical severity.

---

## Research Question

> Do NYC neighborhoods receive comparable emergency response times for similar levels of medical urgency?

Rather than comparing neighborhoods only at an aggregate level, the analysis stratifies incidents by severity and evaluates whether demographic and socioeconomic disparities persist within comparable urgency levels.

---

## Analysis Pipeline

The project follows an end-to-end analytical workflow:

1. **Data Ingestion**
   - Collect and prepare NYC EMS dispatch data
   - Retrieve American Community Survey demographic data

2. **Data Cleaning & Integration**
   - Clean EMS records and standardize ZIP/ZCTA identifiers
   - Merge EMS incidents with neighborhood-level demographic data
   - Create demographic and income-group variables

3. **Severity Stratification**
   - Group incidents into High, Medium, and Low severity tiers
   - Enable comparisons between incidents with similar medical urgency

4. **Fairness Evaluation**
   - Compare response times across demographic and socioeconomic groups within severity tiers
   - Apply statistical tests to evaluate observed differences

5. **Regression & Robustness**
   - Estimate regression models controlling for operational factors
   - Evaluate whether demographic relationships persist after adjustment
   - Conduct geographic robustness checks

6. **Reporting**
   - Generate final statistical tables and visualizations
   - Summarize findings in the final report

---

## Methods

The analysis uses several complementary approaches:

- Severity-stratified analysis
- Welch's t-test
- Mann–Whitney U test
- One-way ANOVA
- False Discovery Rate (FDR) correction
- OLS regression with operational controls
- Geographic robustness / MAUP sensitivity analysis

Operational controls include factors such as **incident severity, borough, and time of day**.

---

## Key Findings

- Response times were consistently higher in ZIP codes with higher Black population shares, including within comparable severity tiers.
- Response-time disparities became larger as clinical urgency decreased.
- Lower-income neighborhoods experienced longer response times, particularly for less-critical incidents.
- Neighborhood demographic composition remained statistically associated with response time after controlling for operational factors.

These findings suggest that aggregate system efficiency can coexist with systematic geographic disparities in service outcomes.

Because demographic characteristics are measured at the ZIP/ZCTA level rather than for individual patients, these results should be interpreted as **area-level associations rather than individual-level effects**.

---

## Selected Results

### Response-Time Differences by Neighborhood Demographics

![Response-time differences by neighborhood demographics](outputs/figures/demographic_impact_plot.png)

### Response-Time Differences with Borough Controls

![Response-time differences with borough controls](outputs/figures/demographic_impact_plot_borough.png)

Additional figures and statistical results are available in [`outputs/`](outputs/).

---

## Data

### NYC EMS Incident Dispatch Data

The analysis uses NYC EMS Incident Dispatch Data from **Q1 2024**, including incident timing, location, and operational information used to calculate and analyze emergency response times.

**Source:** [NYC Open Data — EMS Incident Dispatch Data](https://data.cityofnewyork.us/Public-Safety/EMS-Incident-Dispatch-Data/76xm-jjuj)

### American Community Survey

Neighborhood demographic and socioeconomic measures come from the **2022 American Community Survey (ACS)** and are matched to EMS incidents using ZIP/ZCTA geography.

Because individual-level demographic information is not available in the EMS data, demographic characteristics are approximated using neighborhood-level measures.

**Source:** [U.S. Census Bureau — American Community Survey](https://www.census.gov/programs-surveys/acs)

### Data Pipeline

The `data/` directory preserves both source data and intermediate datasets produced throughout the analytical workflow:

```text
data/
├── raw/
│   ├── nyc_ems_2024q1_raw.parquet
│   ├── acs_2022_acs5_zcta_full.parquet
│   └── acs_2022_zip.parquet
│
└── processed/
    ├── nyc_ems_2024q1_usable.parquet
    ├── merged_ems_acs.parquet
    ├── merged_ems_acs_w_groups.parquet
    └── merged_ems_acs_with_severity.parquet
```

The processed files represent successive stages of the pipeline, from cleaned EMS records through demographic integration, group construction, and the final severity-enriched analysis dataset.

---

## Project Structure

```text
nyc-ems-fairness-analysis/
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── nyc_ems_2024q1_raw.parquet
│   │   ├── acs_2022_acs5_zcta_full.parquet
│   │   └── acs_2022_zip.parquet
│   │
│   └── processed/
│       ├── nyc_ems_2024q1_usable.parquet
│       ├── merged_ems_acs.parquet
│       ├── merged_ems_acs_w_groups.parquet
│       └── merged_ems_acs_with_severity.parquet
│
├── notebooks/
│   ├── 01_data_ingest.ipynb
│   ├── 02_cleaning_and_merging.ipynb
│   ├── 03_severity_grouping.ipynb
│   ├── 04_fairness_evaluation.ipynb
│   ├── 05_regression_and_robustness.ipynb
│   └── 06_generate_final_tables_figures.ipynb
│
├── outputs/
│   ├── figures/
│   └── tables/
│       └── final/
│
└── report/
    └── final_report.pdf
```

### Notebook Workflow

| Notebook | Purpose |
|---|---|
| `01_data_ingest.ipynb` | Ingest and prepare EMS and demographic data |
| `02_cleaning_and_merging.ipynb` | Clean records and integrate EMS with ACS data |
| `03_severity_grouping.ipynb` | Construct severity tiers for conditional comparisons |
| `04_fairness_evaluation.ipynb` | Evaluate disparities across demographic and income groups |
| `05_regression_and_robustness.ipynb` | Run adjusted regression models and robustness analyses |
| `06_generate_final_tables_figures.ipynb` | Produce final tables and visualizations |

---

## Tech Stack

- **Python:** pandas, NumPy
- **Statistical Analysis:** SciPy, statsmodels
- **Data Processing:** PyArrow
- **Visualization:** Matplotlib
- **Data Sources/APIs:** NYC Open Data, U.S. Census ACS
- **Environment:** Jupyter Notebook, python-dotenv

---

## How to Run

1. Clone the portfolio repository and navigate to this project:

```bash
git clone <your-data-portfolio-url>
cd data-portfolio/nyc-ems-fairness-analysis
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. If regenerating ACS data through the Census API, create a `.env` file containing:

```text
CENSUS_API_KEY=your_key_here
```

The `.env` file should not be committed to GitHub.

5. Run the notebooks sequentially:

```text
01 → 02 → 03 → 04 → 05 → 06
```

Each notebook represents a stage of the analytical pipeline, with intermediate datasets saved under `data/processed/`.

---

## My Contributions

- Designed the severity-tier framework used for conditional fairness analysis.
- Implemented statistical testing using Welch's t-test, Mann–Whitney U tests, and ANOVA.
- Built the conditional disparity analysis comparing demographic and socioeconomic groups within severity tiers.
- Conducted regression and robustness analyses with operational and geographic controls.
- Generated key statistical tables and visualizations used to communicate the results.
- Contributed to the interpretation and documentation of the final analysis.

---

## Final Report

For the complete methodology, statistical results, and discussion:

**[View the Final Report](report/final_report.pdf)**

---

## Limitations

- Demographic characteristics are measured at the **ZIP/ZCTA level**, not at the individual patient level.
- Results therefore represent **area-level associations** and should not be interpreted as evidence about individual patients.
- Observational analysis cannot establish that neighborhood demographics cause differences in response times.
- Internal EMS dispatch decision systems are not observable; the project evaluates disparities through observed response outcomes.
- Geographic aggregation can affect measured relationships, so robustness analyses are used to examine sensitivity to geographic specification.