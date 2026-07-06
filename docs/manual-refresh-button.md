# Manual Refresh Button

## Purpose

The Streamlit app now includes a sidebar button:

```text
🔄 Actualiser maintenant
```

This button lets the user refresh market data at any time, without waiting for the scheduled weekly or 2/3-day cycle.

## What the button does

When clicked, the button:

1. optionally regenerates forecasts;
2. reloads seed/generated data into SQLite;
3. creates an `analysis_runs` entry;
4. logs every refreshed table in `table_refresh_log`;
5. clears Streamlit cached data with `st.cache_data.clear()`;
6. triggers `st.rerun()`;
7. reloads all DB-first visual tabs from SQLite.

## Sidebar option

The sidebar includes:

```text
Mode rapide : ne pas recalculer les forecasts
```

Use this when the user wants a quick reload of market-map tables, benchmark seeds, events and product mappings without recalculating scenario forecasts.

## Behavior

Full refresh:

```text
forecasting → SQLite reload → cache clear → UI rerun
```

Fast refresh:

```text
SQLite reload → cache clear → UI rerun
```

## Files added/updated

- `src/refresh_service.py`
- `app/streamlit_app.py`

## Notes

The button currently refreshes the data sources available to the local MVP: seed files and generated forecast outputs.

For true last-minute market data, future ingestion scripts should be added for:

- RSS/news;
- public market APIs;
- OpenRouter/model adoption metrics;
- GitHub/Hugging Face metrics;
- funding/news signals;
- benchmark providers.

Once those ingestion scripts exist, the same button can trigger them before loading data into SQLite.

## Safety

The current button uses reset mode by default. It rebuilds the SQLite seed-backed tables to avoid duplicated rows until upsert logic is implemented.

Future improvement:

- replace reset with table-level upserts;
- add per-source refresh options;
- add progress logs in the UI;
- add confirmation for expensive refreshes;
- add role-based access if deployed publicly.
