from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


# SQLite keeps existing table definitions when CREATE TABLE IF NOT EXISTS is executed.
# These lightweight migrations add columns introduced after the first MVP schema.
SQLITE_COMPAT_COLUMNS: dict[str, list[tuple[str, str]]] = {
    "financial_events": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "ipo_events": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "public_market_observations": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "product_mappings": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "ai_tools": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "upcoming_events": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "benchmark_metrics": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "metric_observations": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "scenario_forecasts": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "signals": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "scores": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
    "investment_memos": [
        ("analysis_run_id", "INTEGER"),
        ("refreshed_at", "TIMESTAMP"),
    ],
}


def _table_exists(conn, table_name: str) -> bool:
    result = conn.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"),
        {"table_name": table_name},
    ).fetchone()
    return result is not None


def _existing_columns(conn, table_name: str) -> set[str]:
    rows = conn.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
    return {row[1] for row in rows}


def ensure_sqlite_schema_compatibility(engine: Engine) -> None:
    """Apply lightweight ALTER TABLE migrations for existing SQLite DBs.

    This keeps the MVP simple while avoiding local breakages when schema.sql evolves.
    It is intentionally additive only: it never drops or rewrites existing columns.
    """
    if engine.dialect.name != "sqlite":
        return

    with engine.begin() as conn:
        for table_name, columns in SQLITE_COMPAT_COLUMNS.items():
            if not _table_exists(conn, table_name):
                continue
            existing = _existing_columns(conn, table_name)
            for column_name, column_type in columns:
                if column_name not in existing:
                    conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
