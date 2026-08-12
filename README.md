# Data Portfolio

Hi, I'm Doris. I have an M.S. in Applied Data Science from USC and a B.S. in Business Analytics and Information Technology from Rutgers, and I like using data to figure out how products, systems, and people actually behave — not just to produce a chart, but to get to a decision someone can act on.

The projects below span product analytics, experimentation, statistical analysis, visualization, and a couple of data-systems detours. Tools I used across them: Python, SQL, Power BI, Tableau, and a fair amount of statistical modeling.

---

## Projects

### [Steam Player Engagement & Product Analytics](gaming-product-analytics/)
*Product Analytics · SQL · Python · Power BI*

Started from a question I kept running into at my Game Analyst internship: does high engagement actually mean players are happy, or does it just mean the game takes a long time? Worked through 41M+ Steam recommendation records down to a reliable sample of 12,460 games, then used SQL for the segmentation and a three-page Power BI dashboard to make the findings usable. The short version: satisfaction and engagement move pretty independently, and treating playtime as a proxy for quality is a mistake.

[View Project →](gaming-product-analytics/)

---

### [Marketing Experiment & Incrementality Analysis](marketing-experiment-analysis/)
*Experimentation · Python · SQL · Statistical Analysis*

An A/B test analysis built to answer two questions instead of one: did the campaign work, and was it worth what it cost? 588K users, conversion lift from 1.785% to 2.555% (a two-proportion z-test with a 95% CI that never touches zero), which works out to roughly 4,343 incremental conversions. Since the dataset doesn't include cost or revenue data, I built a break-even sensitivity analysis instead of guessing at an ROI number — translates the lift into "how much would a conversion need to be worth for this to pay for itself."

[View Project →](marketing-experiment-analysis/)

---

### [KKBox Cohort Retention Analysis](kkbox-retention-analysis/)
*Product Analytics · Retention · Python · Cohort Analysis*

Wanted a retention project on real production-scale data instead of something simulated, which meant building a chunked pipeline to process 392M+ rows of daily listening logs into user-month activity. Cohorts show 84.0% Month-0 activation but retention drops fast after that — 25.4% at Month 1, down to 11.2% by Month 12. The more interesting finding: how deeply someone engages in their first month (normalized for how many days they'd actually had since registering) predicts a 74.7-point gap in Month-1 retention between the highest- and lowest-engagement groups. Also found that acquisition channels look similar on activation but diverge hugely on downstream retention.

[View Project →](kkbox-retention-analysis/)

---

### [NYC EMS Fairness Analysis](nyc-ems-fairness-analysis/)
*Statistical Analysis · Python · Data Integration · Fairness Evaluation*

A conditional-fairness question: after controlling for how urgent an incident actually was, do NYC neighborhoods still see different emergency response times? Merged EMS dispatch data with Census ACS demographics, split incidents into severity tiers, and compared response times within tiers rather than across raw citywide averages. Response times were consistently longer in ZIP codes with higher Black population share and in lower-income neighborhoods, and the association held up after regression controls for borough and time of day. I'm careful throughout about what this can and can't establish — it's an area-level, observational association, not a claim about individual patients or a specific cause.

[View Project →](nyc-ems-fairness-analysis/)

---

### [Dementia Risk Hotspots Visualization](dementia-risk-hotspots-visualization/)
*Data Visualization · Regression · Vue.js · Geographic Analysis*

My piece of a team data-viz project from a USC course. Built a regression-based "Mismatch Index" comparing each county's actual dementia prevalence to what you'd expect given its stroke, diabetes, and cognitive-disability rates, then mapped the gap as an interactive choropleth with state-level highlighting to surface the biggest outliers.

[View Project →](dementia-risk-hotspots-visualization/)

---

### [ChatDB — Natural Language Database Interface](chatdb-natural-language-database/)
*Databases · Python · SQL · MongoDB · LLMs*

A group project — an app that takes a plain-English question and figures out on its own whether it belongs to a MySQL database or a MongoDB one, generates the right query with an LLM, and returns a readable answer. My piece was the MongoDB half: designing the schema for wage-by-education data, building the load pipeline, and getting it to plug into the same natural-language interface as the SQL side.

[View Project →](chatdb-natural-language-database/)

---

## Technical Skills

**Programming & Data:** Python, SQL, Pandas, NumPy, Data Cleaning, ETL, Data Validation
**Databases:** MySQL, SQLite, MongoDB
**Visualization & BI:** Power BI, Tableau, Matplotlib, Amplitude
**Analytics:** Product Analytics, Cohort Analysis, Retention Analysis, A/B Testing, Experimentation, Statistical Analysis, Hypothesis Testing, Confidence Intervals, Regression
**Tools:** Git, Excel, AWS

---

## Structure

```text
data-portfolio/
├── gaming-product-analytics/
├── marketing-experiment-analysis/
├── kkbox-retention-analysis/
├── nyc-ems-fairness-analysis/
├── dementia-risk-hotspots-visualization/
├── chatdb-natural-language-database/
└── README.md
```

Each project folder has its own README with the full data, methodology, and results — this page is just the map.
