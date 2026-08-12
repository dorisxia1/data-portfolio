# Steam Player Engagement & Product Analytics

I wanted a project that used the same kind of thinking I was doing at my Game Analyst internship — engagement, satisfaction, onboarding — but on a dataset big enough that I couldn't just eyeball it. Steam's public recommendations dataset fit: over 41 million user reviews across tens of thousands of games, which is close to the scale of real product data.

The question I kept running into during the internship was one I wanted to test more rigorously here: **does high engagement actually mean players are happy, or are we just measuring how much time something takes to finish?** Playtime and satisfaction get used interchangeably a lot, and I don't think they should be.

## What I actually did

Python handled validation and feature engineering on the raw data — checking for duplicate IDs, broken foreign keys, weird playtime outliers, that kind of thing. After filtering down to games with at least 100 reviews (so a couple of extreme reviews couldn't swing a small game's recommendation rate), I ended up with a working sample of 12,460 games.

From there, SQL (SQLite) did the heavier analytical lifting — CTEs, `CASE WHEN` segmentation, window functions for ranking — and I built dashboard-ready views so the Power BI report could pull clean, pre-aggregated data instead of raw tables.

```text
Raw Steam Data → Python validation/features → 12,460-game reliable sample
→ SQL product analysis → Power BI dashboard → findings & recommendations
```

## The four questions I was actually trying to answer

1. Does satisfaction track with engagement, or can they move independently?
2. Can a game be highly engaging without being well-liked?
3. Do paid games meaningfully outperform free ones?
4. Does price tell you anything about how engaged players end up being?

## What the segmentation showed

I split games into four quadrants using recommendation rate (satisfaction) and median playtime (engagement):

| Segment | Games | Avg. Recommendation Rate | Avg. Median Playtime |
|---|---:|---:|---:|
| High Satisfaction / High Engagement | 3,571 | 91.56% | 25.74 hrs |
| High Satisfaction / Low Engagement | 2,663 | 91.42% | 3.06 hrs |
| Low Satisfaction / High Engagement | 2,676 | 73.13% | 24.22 hrs |
| Low Satisfaction / Low Engagement | 3,550 | 66.59% | 2.95 hrs |

This is basically the whole point of the project in one table. Look at the top two rows — recommendation rate is nearly identical (91.56% vs. 91.42%) even though one group holds players for 25+ hours and the other for about 3. A short game isn't a weaker product; it just does something different. Meanwhile the "Low Satisfaction / High Engagement" row is the one I'd actually flag for a product team — players are sinking real time in, but a quarter of them aren't recommending it, which usually means something's off (grind, monetization friction, etc.) rather than the game being genuinely bad.

Paid vs. free games surprised me a little less — paid games edged out free ones on both metrics (80.69% vs. 79.30% recommendation rate, 14.30 vs. 12.94 hrs median playtime), but the gap is small enough that I wouldn't call pricing model a real driver of quality. Price on its own also turned out to be a weak predictor of engagement — games at the same price point varied wildly in playtime.

## Takeaways I'd actually bring to a product team

- Track satisfaction and engagement side by side. Neither one alone tells you if a product is working.
- The high-engagement / low-satisfaction quadrant is worth digging into — that's where friction hides.
- Don't treat short playtime as a red flag by default; check what the game is trying to be first.
- Free vs. paid is a strategy choice, not a quality signal, at least not in this data.

Full writeup with more detail is in [`findings/recommendations.md`](findings/recommendations.md).

## Dashboard

Three pages in Power BI: an overview page (totals, segment mix, free/paid split, release-year filter), an engagement-vs-satisfaction page, and a pricing/performance page.

![Overview Dashboard](dashboard/images/01_overview.png)
![Engagement and Satisfaction Dashboard](dashboard/images/02_engagement_satisfaction.png)
![Pricing and Product Performance Dashboard](dashboard/images/03_pricing_product_performance.png)

## Data

**Source:** [Game Recommendations on Steam — Kaggle](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam)

Four source files: `games.csv` (game-level info — release date, platform, price, ratings), `recommendations.csv` (41M+ user recommendation records), `users.csv`, and `games_metadata.json`. Raw files aren't in this repo since they're too large for git — grab them from the Kaggle link above and drop them in `data/raw/`. Everything downstream gets built from `notebooks/01_data_analysis.ipynb`.

## Tools

Python (pandas, NumPy, Matplotlib) for cleaning and feature engineering, SQLite/SQL for the analytical layer, Power BI for the dashboard, Git for version control.

## Repo layout

```text
gaming-product-analytics/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/                              # not tracked — download from Kaggle
│   │   ├── games.csv
│   │   ├── games_metadata.json
│   │   ├── recommendations.csv
│   │   └── users.csv
│   └── processed/
│       ├── game_analysis.csv
│       ├── gaming_analytics.db
│       └── reliable_games.csv
│
├── notebooks/
│   └── 01_data_analysis.ipynb
│
├── sql/
│   ├── 01_setup.sql
│   ├── 02_product_analysis.sql
│   └── 03_dashboard_queries.sql
│
├── dashboard/
│   └── images/
│
└── findings/
    └── recommendations.md
```

## Reproducing it

```bash
pip install -r requirements.txt
```

Run `notebooks/01_data_analysis.ipynb` first — it builds the cleaned datasets everything else depends on. Then, from the project root:

```bash
sqlite3 data/processed/gaming_analytics.db < sql/01_setup.sql
sqlite3 -header -column data/processed/gaming_analytics.db < sql/02_product_analysis.sql
sqlite3 data/processed/gaming_analytics.db < sql/03_dashboard_queries.sql
```

## Where I'd push this further

Steam recommendations are a blunt instrument for "satisfaction" — it's a binary thumbs up/down, not a rating scale, and review activity itself varies a lot by game and audience. Playtime also means different things depending on genre (a 10-hour narrative game and a 10-hour roguelike are not the same kind of "engaged"). And the price/discount data is a single snapshot, not a history, so I can't say anything about how pricing changes affected behavior over time. If I extended this, genre, multiplayer status, and monetization design (cosmetics vs. pay-to-win, etc.) are the variables I'd want next — I suspect they'd explain a lot more than price does.

Everything here describes association, not causation — I'm not claiming price *causes* engagement changes, just describing what the data shows.
