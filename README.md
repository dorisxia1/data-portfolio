# Data Portfolio

Hi, I'm Doris! I hold an **M.S. in Applied Data Science from the University of Southern California** and a **B.S. in Business Analytics and Information Technology from Rutgers University-New Brunswick**.

I'm interested in using data to understand how products, systems, and people behave — and turning that analysis into decisions that are actually useful.

This portfolio includes projects across **product analytics, experimentation, statistical analysis, data visualization, and data systems**, using tools including Python, SQL, Power BI, Tableau, and statistical modeling.

---

## Projects

### [Steam Player Engagement & Product Analytics](gaming-product-analytics/)

**Product Analytics · SQL · Python · Power BI**

Analyzed **41M+ Steam recommendation records** to understand how player engagement, satisfaction, pricing, and review volume relate to product performance.

Built an end-to-end analytics workflow spanning data preparation, SQL analysis, dashboard development, and product recommendations.

**Highlights**
- Created a validated analytical sample of **12,460 games**
- Used SQL to segment and compare engagement, satisfaction, and pricing patterns
- Built a three-page Power BI dashboard covering portfolio health, engagement, satisfaction, and product performance
- Translated behavioral patterns into recommendations for product and portfolio strategy

[View Project →](gaming-product-analytics/)

---

### [Marketing Experiment & Incrementality Analysis](marketing-experiment-analysis/)

**Experimentation · Python · SQL · Statistical Analysis**

Analyzed a **588K-user marketing A/B experiment** to determine whether advertising generated incremental conversions relative to a PSA control group and whether the observed lift was economically meaningful.

Combined statistical inference with business sensitivity analysis to translate experimental lift into incremental conversions and break-even campaign thresholds.

**Highlights**
- Measured conversion lift from **1.785% to 2.555%**, a **43.1% relative increase**
- Applied a two-proportion z-test and 95% confidence interval to evaluate the treatment effect
- Estimated approximately **4,343 incremental conversions** attributable to the advertising condition
- Built a break-even sensitivity analysis connecting incremental conversions to campaign economics
- Used SQL to reproduce core experiment metrics and segment conversion behavior
- Distinguished causal experiment results from descriptive post-treatment exposure and timing patterns

[View Project →](marketing-experiment-analysis/)

---

### [NYC EMS Fairness Analysis](nyc-ems-fairness-analysis/)

**Statistical Analysis · Python · Data Integration · Fairness Evaluation**

Investigated whether emergency response times differ across NYC neighborhoods after accounting for medical urgency and operational factors.

Built an end-to-end analytical pipeline combining NYC EMS dispatch records with U.S. Census demographic data to evaluate disparities within comparable severity levels.

**Highlights**
- Built a multi-stage Python pipeline for data ingestion, cleaning, integration, and analysis
- Compared response times across demographic and socioeconomic groups within severity tiers
- Applied hypothesis testing and OLS regression to evaluate observed disparities
- Conducted geographic robustness analysis and generated final statistical tables and visualizations

[View Project →](nyc-ems-fairness-analysis/)

---

### [Dementia Risk Hotspots Visualization](dementia-risk-hotspots-visualization/)

**Data Visualization · Regression · Vue.js · Geographic Analysis**

Developed an interactive county-level visualization exploring where dementia prevalence is substantially higher or lower than expected based on underlying health risk factors.

This portfolio project highlights my individual contribution to a collaborative USC data visualization project.

**Highlights**
- Developed a regression-based **Mismatch Index** comparing observed and expected dementia prevalence
- Integrated NORC Dementia DataHub and CDC PLACES health measures
- Built an interactive county-level choropleth to reveal geographic patterns
- Added state-level highlighting and interactive exploration to surface unusually high- or low-mismatch areas

[View Project →](dementia-risk-hotspots-visualization/)

---

### [ChatDB — Natural Language Database Interface](chatdb-natural-language-database/)

**Databases · Python · SQL · MongoDB · LLMs**

Built an application that translates natural-language questions into executable queries across relational and NoSQL databases.

The project explores how natural-language interfaces can make structured and semi-structured data easier to query without requiring users to write database queries directly.

**Highlights**
- Translated natural-language questions into SQL and MongoDB queries
- Built schema-aware workflows for relational and NoSQL databases
- Developed data-loading and transformation pipelines for MySQL and MongoDB
- Created an application interface for querying and exploring database results

[View Project →](chatdb-natural-language-database/)

---

## Technical Skills

**Programming & Data:** Python, SQL, Pandas, NumPy, Data Cleaning, ETL, Data Validation  
**Databases:** MySQL, SQLite, MongoDB  
**Visualization & BI:** Power BI, Tableau, Matplotlib, Amplitude  
**Analytics:** A/B Testing, Experimentation, Statistical Analysis, Hypothesis Testing, Confidence Intervals, Regression  
**Tools:** Git, Excel, AWS

---

## Portfolio Structure

```text
data-portfolio/
├── gaming-product-analytics/
├── marketing-experiment-analysis/
├── nyc-ems-fairness-analysis/
├── dementia-risk-hotspots-visualization/
├── chatdb-natural-language-database/
└── README.md
```

Each project contains its own documentation covering the data, methodology, analysis, results, and relevant project files.