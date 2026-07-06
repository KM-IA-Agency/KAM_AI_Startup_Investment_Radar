# SQLite Loading Runbook

## Goal

All Streamlit tabs should read database tables first.

CSV files remain seed/import files and fallback sources only.

## Load all seed data into SQLite

Run:

```bash
python src/load_to_db.py
```

The loader now populates:

- `startups`
- `scores`
- `product_mappings`
- `ai_tools`
- `benchmark_metrics`
- `financial_events`
- `ipo_events`
- `public_market_observations`
- `upcoming_events`
- `scenario_forecasts`

It also prints row counts for each loaded table.

## Generate forecasts before loading

If forecast CSVs are missing or stale, run:

```bash
python src/forecasting.py
python src/load_to_db.py
```

This loads generated forecast outputs into:

```text
scenario_forecasts
```

## Run Streamlit

```bash
streamlit run app/streamlit_app.py
```

The app will now try database tables first for:

- Overview / Watchlist
- AI Tools Stack
- Benchmark
- Forecasts
- Financial Timeline
- IPO & Actions
- Products & Events
- Physical AI
- Startup Detail

## Fallback behavior

If a table is missing or empty, the app falls back to the related CSV seed.

This is useful during local development, but production/demo flows should use SQLite.

## SQLite-first command sequence

Recommended full refresh:

```bash
python src/scoring.py
python src/forecasting.py
python src/load_to_db.py
streamlit run app/streamlit_app.py
```

## Next improvements

- Add validation checks after load.
- Add source metadata per row.
- Add migration script instead of full reset.
- Add export/import of SQLite database file for demos.
- Add optional PostgreSQL connection later via environment variable.
