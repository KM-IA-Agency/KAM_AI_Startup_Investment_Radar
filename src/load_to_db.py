from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.db import execute_sql_file, get_engine
from src.run_tracking import finish_analysis_run, log_table_refresh, start_analysis_run, utc_now_iso
from src.scoring import score_dataframe
from src.stage_analysis import refresh_growth_stage_tables

SEED_PATH = Path("data/seeds/startups_seed.csv")
PRODUCT_MAPPING_PATH = Path("data/seeds/company_product_mapping_seed.csv")
AI_TOOLS_TAXONOMY_PATH = Path("data/seeds/ai_tools_trending_by_category_july2026.csv")
VIBE_CODING_TOP20_PATH = Path("data/seeds/vibe_coding_top20_july2026.csv")
BENCHMARK_PATH = Path("data/seeds/benchmark_metrics_seed.csv")
FINANCIAL_EVENTS_PATH = Path("data/seeds/financial_events_seed.csv")
IPO_EVENTS_PATH = Path("data/seeds/ipo_events_seed.csv")
PUBLIC_MARKET_PATH = Path("data/seeds/public_market_observations_seed.csv")
UPCOMING_EVENTS_PATH = Path("data/seeds/upcoming_events_seed.csv")
FORECAST_PATH = Path("reports/forecasts/scenario_forecasts.csv")
FORECAST_SHORT_PATH = Path("reports/forecasts/scenario_forecasts_short_term.csv")

STARTUP_COLUMNS = [
    "name", "website", "country", "region", "sector", "sub_sector",
    "stage", "description", "source_url",
]

SCORE_COLUMNS = [
    "market_score", "problem_pain_score", "product_maturity_score", "traction_score",
    "team_score", "technical_moat_score", "valuation_score", "investor_quality_score",
    "exit_potential_score", "risk_score", "kamel_edge_score", "total_score",
    "decision", "score_explanation",
]

RESET_TABLES = [
    "stage_opportunities", "growth_stage_snapshots", "ai_tools", "product_mappings",
    "upcoming_events", "benchmark_metrics", "financial_events", "ipo_events",
    "public_market_observations", "scenario_forecasts", "scores", "startups",
]


def reset_seed_tables(engine) -> None:
    with engine.begin() as conn:
        for table in RESET_TABLES:
            conn.execute(text(f"DELETE FROM {table}"))


def _startup_ids(engine) -> pd.DataFrame:
    with engine.begin() as conn:
        return pd.read_sql("select id as startup_id, name from startups", conn)


def _resolve_startup_id(frame: pd.DataFrame, engine, company_column: str = "company_name") -> pd.DataFrame:
    ids = _startup_ids(engine)
    if frame.empty or company_column not in frame.columns:
        frame["startup_id"] = None
        return frame

    lookup = ids.rename(columns={"name": "__startup_lookup_name"})
    resolved = frame.merge(
        lookup,
        left_on=company_column,
        right_on="__startup_lookup_name",
        how="left",
    )
    return resolved.drop(columns=["__startup_lookup_name"], errors="ignore")


def _clean_numeric_columns(frame: pd.DataFrame, numeric_columns: list[str]) -> pd.DataFrame:
    for col in numeric_columns:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
    return frame


def _tag_run(frame: pd.DataFrame, run_id: int) -> pd.DataFrame:
    frame = frame.copy()
    frame["analysis_run_id"] = run_id
    frame["refreshed_at"] = utc_now_iso()
    return frame


def _load_csv_with_startup_id(
    engine,
    path: Path,
    table: str,
    name_column: str,
    cols: list[str],
    run_id: int,
    numeric_cols: list[str] | None = None,
    observed_from_col: str | None = None,
    observed_to_col: str | None = None,
) -> int:
    if not path.exists():
        log_table_refresh(engine, run_id, table, 0, source_name=path.name, source_path=str(path), status="missing")
        return 0
    frame = pd.read_csv(path)
    if frame.empty:
        log_table_refresh(engine, run_id, table, 0, source_name=path.name, source_path=str(path), status="empty")
        return 0
    frame = _resolve_startup_id(frame, engine, name_column)
    if numeric_cols:
        frame = _clean_numeric_columns(frame, numeric_cols)
    frame = _tag_run(frame, run_id)
    selected_cols = [col for col in cols + ["analysis_run_id", "refreshed_at"] if col in frame.columns]
    frame[selected_cols].to_sql(table, engine, if_exists="append", index=False)

    observed_from = None
    observed_to = None
    if observed_from_col and observed_from_col in frame.columns:
        observed_from = str(pd.to_datetime(frame[observed_from_col], errors="coerce").min())
    if observed_to_col and observed_to_col in frame.columns:
        observed_to = str(pd.to_datetime(frame[observed_to_col], errors="coerce").max())

    log_table_refresh(
        engine,
        run_id,
        table,
        len(frame),
        source_name=path.name,
        source_path=str(path),
        observed_from=observed_from,
        observed_to=observed_to,
    )
    return len(frame)


def _load_product_mappings(engine, run_id: int) -> int:
    cols = ["startup_id", "company_name", "public_name", "flagship_product", "product_category", "related_startup_or_segment", "ticker", "exchange_name", "status", "notes"]
    return _load_csv_with_startup_id(engine, PRODUCT_MAPPING_PATH, "product_mappings", "company_name", cols, run_id)


def _normalize_ai_tools_seed() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    if AI_TOOLS_TAXONOMY_PATH.exists():
        taxonomy = pd.read_csv(AI_TOOLS_TAXONOMY_PATH)
        if not taxonomy.empty:
            taxonomy = taxonomy.rename(columns={"company_or_owner": "company_name"})
            taxonomy["status"] = "unknown"
            taxonomy["source_dataset"] = AI_TOOLS_TAXONOMY_PATH.name
            frames.append(taxonomy)
    if VIBE_CODING_TOP20_PATH.exists():
        top20 = pd.read_csv(VIBE_CODING_TOP20_PATH)
        if not top20.empty:
            frames.append(pd.DataFrame({
                "tool_or_group": top20.get("tool_or_group"),
                "company_name": top20.get("company_or_owner"),
                "category": top20.get("category"),
                "role": top20.get("primary_role"),
                "investment_relevance": top20.get("investable_entity"),
                "radar_priority": "High",
                "status": top20.get("status"),
                "source_dataset": VIBE_CODING_TOP20_PATH.name,
                "notes": top20.get("radar_action"),
            }))
    if not frames:
        return pd.DataFrame()
    tools = pd.concat(frames, ignore_index=True)
    tools = tools.dropna(subset=["tool_or_group", "category"])
    return tools.drop_duplicates(subset=["tool_or_group", "company_name", "category"], keep="first")


def _load_ai_tools(engine, run_id: int) -> int:
    tools = _normalize_ai_tools_seed()
    if tools.empty:
        log_table_refresh(engine, run_id, "ai_tools", 0, source_name="ai_tools seeds", source_type="seed_csv", status="empty")
        return 0
    tools = _resolve_startup_id(tools, engine, "company_name")
    tools = _tag_run(tools, run_id)
    cols = ["startup_id", "company_name", "tool_or_group", "category", "role", "investment_relevance", "radar_priority", "status", "source_dataset", "notes", "analysis_run_id", "refreshed_at"]
    tools[[col for col in cols if col in tools.columns]].to_sql("ai_tools", engine, if_exists="append", index=False)
    log_table_refresh(engine, run_id, "ai_tools", len(tools), source_name="AI tools seed bundle", source_type="seed_csv", source_path="data/seeds/*ai_tools* + vibe_coding_top20")
    return len(tools)


def _load_benchmark_metrics(engine, run_id: int) -> int:
    cols = ["startup_id", "currency", "revenue_latest", "revenue_period", "revenue_growth_yoy_pct", "valuation_latest", "valuation_date", "total_funding", "latest_round_amount", "latest_round_date", "employees_latest", "employee_growth_6m_pct", "web_traffic_growth_3m_pct", "github_stars", "github_stars_growth_3m_pct", "customer_count_estimate", "data_confidence", "notes"]
    nums = ["revenue_latest", "revenue_growth_yoy_pct", "valuation_latest", "total_funding", "latest_round_amount", "employees_latest", "employee_growth_6m_pct", "web_traffic_growth_3m_pct", "github_stars", "github_stars_growth_3m_pct", "customer_count_estimate", "data_confidence"]
    return _load_csv_with_startup_id(engine, BENCHMARK_PATH, "benchmark_metrics", "name", cols, run_id, nums, "valuation_date", "latest_round_date")


def _load_financial_events(engine, run_id: int) -> int:
    cols = ["startup_id", "event_date", "event_type", "event_title", "amount", "valuation", "currency", "share_price", "ticker", "exchange_name", "description", "source_url", "confidence_score"]
    nums = ["amount", "valuation", "share_price", "confidence_score"]
    return _load_csv_with_startup_id(engine, FINANCIAL_EVENTS_PATH, "financial_events", "name", cols, run_id, nums, "event_date", "event_date")


def _load_ipo_events(engine, run_id: int) -> int:
    cols = ["startup_id", "name", "ipo_date", "event_type", "ipo_price", "first_day_close", "latest_share_price", "shares_outstanding", "market_cap_latest", "currency", "ticker", "exchange_name", "description", "source_url", "confidence_score"]
    nums = ["ipo_price", "first_day_close", "latest_share_price", "shares_outstanding", "market_cap_latest", "confidence_score"]
    return _load_csv_with_startup_id(engine, IPO_EVENTS_PATH, "ipo_events", "name", cols, run_id, nums, "ipo_date", "ipo_date")


def _load_public_market_observations(engine, run_id: int) -> int:
    cols = ["startup_id", "observed_at", "ticker", "exchange_name", "share_price", "market_cap", "enterprise_value", "currency", "source", "source_url", "confidence_score"]
    nums = ["share_price", "market_cap", "enterprise_value", "confidence_score"]
    return _load_csv_with_startup_id(engine, PUBLIC_MARKET_PATH, "public_market_observations", "name", cols, run_id, nums, "observed_at", "observed_at")


def _load_upcoming_events(engine, run_id: int) -> int:
    cols = ["startup_id", "company_name", "product_or_segment", "event_window", "event_type", "event_title", "probability_pct", "impact_score", "confidence_score", "expected_effect", "watch_signals", "notes"]
    nums = ["probability_pct", "impact_score", "confidence_score"]
    return _load_csv_with_startup_id(engine, UPCOMING_EVENTS_PATH, "upcoming_events", "company_name", cols, run_id, nums)


def _load_forecasts(engine, run_id: int) -> int:
    frames = []
    for path in [FORECAST_PATH, FORECAST_SHORT_PATH]:
        if path.exists():
            frame = pd.read_csv(path)
            if not frame.empty:
                frame["source_path"] = str(path)
                frames.append(frame)
    if not frames:
        log_table_refresh(engine, run_id, "scenario_forecasts", 0, source_name="forecast files", source_type="generated_csv", status="missing_or_empty")
        return 0
    forecasts = pd.concat(frames, ignore_index=True).drop_duplicates()
    forecasts = _resolve_startup_id(forecasts, engine, "name")
    forecasts = _clean_numeric_columns(forecasts, ["horizon_months", "current_value", "forecast_value", "implied_cagr_pct", "probability_pct", "confidence_score"])
    forecasts = _tag_run(forecasts, run_id)
    cols = ["startup_id", "forecast_date", "horizon_months", "scenario", "metric_name", "current_value", "forecast_value", "implied_cagr_pct", "probability_pct", "confidence_score", "assumptions", "analysis_run_id", "refreshed_at"]
    forecasts[[col for col in cols if col in forecasts.columns]].to_sql("scenario_forecasts", engine, if_exists="append", index=False)
    log_table_refresh(engine, run_id, "scenario_forecasts", len(forecasts), source_name="forecast outputs", source_type="generated_csv", source_path="reports/forecasts/*.csv", observed_from=str(pd.to_datetime(forecasts["forecast_date"], errors="coerce").min()), observed_to=str(pd.to_datetime(forecasts["forecast_date"], errors="coerce").max()))
    return len(forecasts)


def load_seed_to_db(
    seed_path: str | Path = SEED_PATH,
    reset: bool = True,
    cadence: str = "manual",
    run_type: str = "seed_refresh",
    trigger_source: str = "manual",
) -> None:
    execute_sql_file()
    engine = get_engine()
    run_id = start_analysis_run(engine, run_name="SQLite seed refresh", run_type=run_type, cadence=cadence, trigger_source=trigger_source)
    try:
        if reset:
            reset_seed_tables(engine)
        df = pd.read_csv(seed_path)
        scored = score_dataframe(df)
        startups = scored[[col for col in STARTUP_COLUMNS if col in scored.columns]].copy()
        startups["updated_at"] = utc_now_iso()
        startups.to_sql("startups", engine, if_exists="append", index=False)
        log_table_refresh(engine, run_id, "startups", len(startups), source_name=Path(seed_path).name, source_path=str(seed_path))

        ids = _startup_ids(engine)
        scores = scored.merge(ids.rename(columns={"startup_id": "id"}), on="name", how="left")
        scores = scores.rename(columns={"id": "startup_id"})
        scores = scores[["startup_id"] + [col for col in SCORE_COLUMNS if col in scores.columns]].copy()
        scores = _tag_run(scores, run_id)
        scores.to_sql("scores", engine, if_exists="append", index=False)
        log_table_refresh(engine, run_id, "scores", len(scores), source_name=Path(seed_path).name, source_path=str(seed_path))

        counts = {
            "product_mappings": _load_product_mappings(engine, run_id),
            "ai_tools": _load_ai_tools(engine, run_id),
            "benchmark_metrics": _load_benchmark_metrics(engine, run_id),
            "financial_events": _load_financial_events(engine, run_id),
            "ipo_events": _load_ipo_events(engine, run_id),
            "public_market_observations": _load_public_market_observations(engine, run_id),
            "upcoming_events": _load_upcoming_events(engine, run_id),
            "scenario_forecasts": _load_forecasts(engine, run_id),
        }
        counts.update(refresh_growth_stage_tables(engine, run_id=run_id))
        finish_analysis_run(engine, run_id, status="success")
        print(f"Analysis run id: {run_id}")
        print("Loaded rows:")
        print(f"- startups: {len(startups)}")
        print(f"- scores: {len(scores)}")
        for table, count in counts.items():
            print(f"- {table}: {count}")
    except Exception as exc:
        finish_analysis_run(engine, run_id, status="failed", notes=str(exc))
        raise


if __name__ == "__main__":
    load_seed_to_db()
    print("Seed datasets loaded to SQLite database")
