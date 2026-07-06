# AI Tools Data Normalization Strategy

## Problem

The first version of the `AI Tools Stack` view used standalone CSV files:

```text
data/seeds/ai_tools_trending_by_category_july2026.csv
data/seeds/vibe_coding_top20_july2026.csv
```

This was useful for fast prototyping, but it created a problem: the AI tools taxonomy was partly decoupled from the main startup radar entities.

The rest of the project is structured around:

- `startups`;
- `scores`;
- `benchmark_metrics`;
- `financial_events`;
- `public_market_observations`;
- product/company mappings.

A separate CSV-only market map risks duplicating company names and losing the relationship between product, owner, score, events, benchmark and investability.

## Correct design

CSV files should be treated as seed/import files, not as the final source of truth.

The normalized database should use:

```text
startups
  └── product_mappings
  └── ai_tools
  └── scores
  └── benchmark_metrics
  └── financial_events
  └── public_market_observations
```

## New table

A new table has been added:

```sql
ai_tools
```

It contains:

- `startup_id` when the company exists in `startups`;
- `company_name`;
- `tool_or_group`;
- `category`;
- `role`;
- `investment_relevance`;
- `radar_priority`;
- `status`;
- `source_dataset`;
- `notes`;
- optional scoring fields.

## Product mapping table

A normalized table has also been added:

```sql
product_mappings
```

It links:

- company;
- public product name;
- flagship product;
- product category;
- ticker;
- exchange;
- status;
- startup_id where available.

## Loader behavior

`src/load_to_db.py` now loads:

1. `startups_seed.csv` into `startups`;
2. scores into `scores`;
3. `company_product_mapping_seed.csv` into `product_mappings`;
4. `ai_tools_trending_by_category_july2026.csv` and `vibe_coding_top20_july2026.csv` into `ai_tools`.

Where possible, it resolves `startup_id` by matching `company_name` to `startups.name`.

## Streamlit behavior

`app/streamlit_app.py` now tries to read from database tables first:

```text
ai_tools
product_mappings
```

If these tables are empty or unavailable, it falls back to CSV seed files.

This keeps the MVP easy to run while allowing the data model to evolve toward a normalized database.

## Rule going forward

Do not create standalone analysis CSVs that are permanently disconnected from the main entity model.

For every new market map or taxonomy, decide whether it should link to:

- `startup_id`;
- `company_name`;
- `product_mappings`;
- `signals`;
- `financial_events`;
- `benchmark_metrics`.

CSV files can remain useful for quick seed data, but the app should prefer the normalized database when available.
