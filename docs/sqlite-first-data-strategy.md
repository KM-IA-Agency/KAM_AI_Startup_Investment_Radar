# SQLite-first Data Strategy

## Decision

The MVP should be database-first, but not necessarily PostgreSQL-first.

For the product's current stage, SQLite is a good default because it is:

- simple to deploy;
- file-based;
- easy to ship with a lightweight web app;
- compatible with Streamlit MVP workflows;
- fast enough for small and medium datasets;
- easy to back up and version during early development;
- portable between local dev, demo environments and small hosted deployments.

The long-term design should remain compatible with PostgreSQL and SQL Server, but the MVP can keep SQLite as the lightweight operational database.

## Guiding principle

All dashboard tabs should read from tables.

CSV files are allowed as seed/import files, but they should not remain the primary runtime source for dashboard views once a table exists.

## Target architecture

```text
CSV / API / manual input / web scraping / RSS
        ↓
ingestion loaders
        ↓
SQLite MVP database
        ↓
Streamlit tabs
        ↓
PostgreSQL / SQL Server migration later if needed
```

## Why tables even if independent?

At the beginning, not all datasets need to be fully normalized.

It is acceptable to have independent tables such as:

- `startups`
- `scores`
- `ai_tools`
- `product_mappings`
- `benchmark_metrics`
- `financial_events`
- `public_market_observations`
- `signals`
- `upcoming_events`
- `scenario_forecasts`
- `metric_observations`

Some tables may be loosely connected at first through names or product labels. Over time, they should converge toward a coherent model using:

- `startup_id`
- `company_name`
- `product_id` / product mapping
- `ticker`
- `source_id`
- `event_id`

The priority is to stop hard-coding dashboard logic around CSV files.

## Current rule

Every new dashboard tab should follow this order:

1. Try reading from a database table.
2. If the table is missing or empty, fall back to a seed CSV.
3. Document the target table and migration path.

## MVP database choice

SQLite is the default MVP database.

Recommended local database file:

```text
startup_radar_local.db
```

Recommended command:

```bash
python src/load_to_db.py
```

Then run:

```bash
streamlit run app/streamlit_app.py
```

## Migration path

### Phase 1 — SQLite MVP

- Keep CSV seeds.
- Load all dashboard data into SQLite tables.
- Streamlit reads DB first, CSV fallback second.
- Maintain simple SQL schema.

### Phase 2 — SQLite structured product

- Add ingestion scripts per data domain.
- Add validation checks.
- Add unique keys and indexes.
- Add source tracking and confidence scores.
- Add snapshot/history tables.

### Phase 3 — PostgreSQL / SQL Server optional upgrade

Move to PostgreSQL or SQL Server only when one of these becomes necessary:

- concurrent writes;
- multi-user authentication;
- larger data volume;
- scheduled ingestion jobs;
- API backend;
- advanced SQL analytics;
- vector search / PostGIS / Timescale use cases;
- enterprise deployment requirements.

## Why keep SQLite even later?

Even if a server database is added later, SQLite can remain useful as:

- local demo database;
- offline analyst edition;
- portable MVP distribution;
- test fixture;
- lightweight single-user deployment;
- downloadable analysis package.

## Development rule

Do not build future tabs directly against CSV-only datasets.

Each new data source should include:

- a seed CSV or ingestion file;
- a target SQL table;
- a loader into SQLite;
- a DB-first Streamlit reader;
- optional CSV fallback.
