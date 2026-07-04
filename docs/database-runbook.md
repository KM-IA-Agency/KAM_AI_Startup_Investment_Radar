# Database Runbook

## Local fallback

The MVP can load the seed dataset into a local SQLite database.

```bash
python src/load_to_db.py
```

Expected output:

```text
startup_radar_local.db
```

## PostgreSQL mode

Set `DATABASE_URL` before running the loader.

```bash
python src/load_to_db.py
```

## Current limitation

The Streamlit app still reads the CSV seed file. Database loading is prepared for the next iteration.
