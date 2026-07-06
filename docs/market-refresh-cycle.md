# Market Refresh Cycle

## Objective

The radar should not be a static dashboard.

Market maps, trend analyses, benchmarks, forecasts and startup watchlists need to be refreshed on a recurring cycle.

Recommended cadences:

- weekly for slower market maps and investment notes;
- every 2 or 3 days for fast-moving AI coding, model, funding and product signals;
- daily only for high-frequency market or news monitoring.

## Run tracking

Every refresh execution creates a row in:

```text
analysis_runs
```

Every refreshed table creates rows in:

```text
table_refresh_log
```

This allows the app to know:

- when an analysis was executed;
- which tables were updated;
- how many rows were loaded;
- the source file or source type;
- whether the run succeeded or failed;
- whether it was manual, cron, GitHub Actions or another scheduler.

## Main refresh command

Manual refresh:

```bash
python src/run_market_refresh.py --cadence manual --trigger-source manual_cli
```

Every 2 days:

```bash
python src/run_market_refresh.py --cadence every_2_days --trigger-source cron
```

Every 3 days:

```bash
python src/run_market_refresh.py --cadence every_3_days --trigger-source cron
```

Weekly:

```bash
python src/run_market_refresh.py --cadence weekly --trigger-source cron
```

Skip forecast regeneration and only load existing outputs:

```bash
python src/run_market_refresh.py --skip-forecasting
```

## Current refresh flow

```text
forecast generation
        ↓
seed/data loading
        ↓
SQLite table refresh
        ↓
analysis_runs entry
        ↓
table_refresh_log entries
        ↓
Streamlit DB-first tabs
```

## Tables tracked

Current tracked tables include:

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

## Strategic implication

Each market analysis should have a visible freshness date.

Examples:

- `AI Tools Stack` should show when the taxonomy was last refreshed.
- `Benchmark` should show the last data refresh.
- `Forecasts` should show the forecast generation date.
- `Products & Events` should show the latest event hypothesis refresh.

## Future scheduler options

### Local cron

Example every 3 days at 08:00:

```cron
0 8 */3 * * cd /path/to/KAM_AI_Startup_Investment_Radar && python src/run_market_refresh.py --cadence every_3_days --trigger-source cron
```

### GitHub Actions

Useful later for cloud refresh, but requires a decision about whether to commit generated SQLite artifacts or deploy them elsewhere.

### External scheduler

Can be connected later through:

- n8n;
- GitHub Actions;
- a VPS cron;
- Streamlit Cloud scheduled job if available;
- Airflow / Prefect / Dagster for a more mature data platform.

## Next improvements

- Add a Streamlit freshness panel.
- Add validation thresholds per table.
- Add upsert logic instead of full reset.
- Add source-level freshness and confidence scoring.
- Add RSS/API ingestion for fast-moving signals.
- Add notification when a major signal changes category or priority.
