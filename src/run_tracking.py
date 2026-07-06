from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import text


UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def start_analysis_run(
    engine,
    run_name: str,
    run_type: str = "market_refresh",
    cadence: str = "manual",
    trigger_source: str = "manual",
    notes: str | None = None,
) -> int:
    """Create an analysis run and return its database id.

    This is intentionally lightweight and SQLite-compatible.
    """
    started_at = utc_now_iso()
    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                INSERT INTO analysis_runs (
                    run_name, run_type, cadence, started_at, status, trigger_source, notes
                ) VALUES (
                    :run_name, :run_type, :cadence, :started_at, 'running', :trigger_source, :notes
                )
                """
            ),
            {
                "run_name": run_name,
                "run_type": run_type,
                "cadence": cadence,
                "started_at": started_at,
                "trigger_source": trigger_source,
                "notes": notes,
            },
        )
        return int(result.lastrowid)


def finish_analysis_run(engine, run_id: int, status: str = "success", notes: str | None = None) -> None:
    finished_at = utc_now_iso()
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                UPDATE analysis_runs
                SET finished_at = :finished_at,
                    status = :status,
                    notes = COALESCE(:notes, notes)
                WHERE id = :run_id
                """
            ),
            {"finished_at": finished_at, "status": status, "notes": notes, "run_id": run_id},
        )


def log_table_refresh(
    engine,
    run_id: int,
    table_name: str,
    rows_loaded: int,
    source_name: str | None = None,
    source_type: str | None = "seed_csv",
    source_path: str | None = None,
    status: str = "success",
    observed_from: str | None = None,
    observed_to: str | None = None,
    notes: str | None = None,
) -> None:
    refreshed_at = utc_now_iso()
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO table_refresh_log (
                    analysis_run_id, table_name, source_name, source_type, source_path,
                    rows_loaded, observed_from, observed_to, refreshed_at, status, notes
                ) VALUES (
                    :analysis_run_id, :table_name, :source_name, :source_type, :source_path,
                    :rows_loaded, :observed_from, :observed_to, :refreshed_at, :status, :notes
                )
                """
            ),
            {
                "analysis_run_id": run_id,
                "table_name": table_name,
                "source_name": source_name,
                "source_type": source_type,
                "source_path": source_path,
                "rows_loaded": rows_loaded,
                "observed_from": observed_from,
                "observed_to": observed_to,
                "refreshed_at": refreshed_at,
                "status": status,
                "notes": notes,
            },
        )


def summarize_latest_refreshes(engine) -> list[dict[str, Any]]:
    """Return the latest refresh per table as simple dictionaries."""
    query = text(
        """
        SELECT table_name,
               MAX(refreshed_at) AS last_refreshed_at,
               SUM(rows_loaded) AS rows_loaded_total
        FROM table_refresh_log
        GROUP BY table_name
        ORDER BY table_name
        """
    )
    with engine.begin() as conn:
        rows = conn.execute(query).mappings().all()
        return [dict(row) for row in rows]
