# SQLite Schema Migrations

## Why this exists

SQLite does not update an existing table when `CREATE TABLE IF NOT EXISTS` is executed.

So if a local database was created before new columns were added to `sql/schema.sql`, the table keeps its old structure.

Example error:

```text
sqlite3.OperationalError: table scores has no column named analysis_run_id
```

This happens because the local `scores` table was created before these columns were added:

```text
analysis_run_id
refreshed_at
```

## Fix implemented

The project now includes:

```text
src/sqlite_migrations.py
```

It applies lightweight, additive SQLite migrations after `schema.sql` is executed.

`src/db.py` now calls:

```python
ensure_sqlite_schema_compatibility(engine)
```

after schema creation.

## What it does

For existing SQLite databases, it checks important analysis tables and adds missing columns such as:

```text
analysis_run_id INTEGER
refreshed_at TIMESTAMP
```

It does not drop or rewrite existing tables.

## How to use

After pulling the latest code, run again:

```bash
python src/run_market_refresh.py --cadence manual --trigger-source manual_cli
```

or:

```bash
python src/load_to_db.py
```

The migration should run automatically.

## Emergency fallback

If the local SQLite database is only a disposable MVP/demo database, the simplest reset remains:

```bash
rm startup_radar_local.db
python src/run_market_refresh.py --cadence manual --trigger-source manual_cli
```

On Windows PowerShell:

```powershell
Remove-Item startup_radar_local.db
python src/run_market_refresh.py --cadence manual --trigger-source manual_cli
```

But normally this should no longer be needed for additive schema changes.

## Migration rule

When new columns are added to existing SQLite tables, also update:

```text
src/sqlite_migrations.py
```

This prevents local MVP databases from breaking after schema evolution.
