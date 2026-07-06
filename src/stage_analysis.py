from __future__ import annotations

from datetime import date

import pandas as pd
from sqlalchemy import text

from src.run_tracking import log_table_refresh, utc_now_iso


STAGE_ORDER = [
    "Pre-Seed",
    "Seed",
    "Series A",
    "Series B",
    "Series C+",
    "Growth / Pre-IPO",
    "IPO / Public",
    "Post-IPO",
    "Unknown",
]

NEXT_STAGE = {
    "Pre-Seed": "Seed",
    "Seed": "Series A",
    "Series A": "Series B",
    "Series B": "Series C+",
    "Series C+": "Growth / Pre-IPO",
    "Growth / Pre-IPO": "IPO / Secondary / M&A",
    "IPO / Public": "Post-IPO expansion / Public market rerating",
    "Post-IPO": "Public market rerating / Strategic acquisition",
    "Unknown": "Data validation required",
}


def normalize_stage(raw_stage: str | None) -> str:
    text_value = str(raw_stage or "").strip().lower()
    if not text_value:
        return "Unknown"
    if "pre" in text_value and "seed" in text_value:
        return "Pre-Seed"
    if "seed" in text_value:
        return "Seed"
    if "series a" in text_value or text_value in {"a", "serie a", "série a"}:
        return "Series A"
    if "series b" in text_value or text_value in {"b", "serie b", "série b"}:
        return "Series B"
    if any(token in text_value for token in ["series c", "series d", "series e", "serie c", "série c", "late"]):
        return "Series C+"
    if any(token in text_value for token in ["growth", "pre-ipo", "pre ipo", "scaleup"]):
        return "Growth / Pre-IPO"
    if any(token in text_value for token in ["ipo", "public", "listed", "cotée", "cotee"]):
        return "IPO / Public"
    return str(raw_stage) if raw_stage else "Unknown"


def infer_stage_from_latest_round(stage: str, latest_round: str | None, has_ipo: bool) -> str:
    if has_ipo:
        return "IPO / Public"
    round_text = str(latest_round or "").lower()
    if not round_text:
        return stage
    if "pre-seed" in round_text or "pre seed" in round_text:
        return "Pre-Seed"
    if "seed" in round_text:
        return "Seed"
    if "series a" in round_text or "serie a" in round_text or "série a" in round_text:
        return "Series A"
    if "series b" in round_text or "serie b" in round_text or "série b" in round_text:
        return "Series B"
    if any(token in round_text for token in ["series c", "series d", "series e", "series f", "growth", "late"]):
        return "Series C+"
    if "ipo" in round_text or "public" in round_text:
        return "IPO / Public"
    return stage


def stage_horizon(stage: str) -> str:
    if stage in {"Pre-Seed", "Seed"}:
        return "6-18 months"
    if stage in {"Series A", "Series B"}:
        return "6-24 months"
    if stage in {"Series C+", "Growth / Pre-IPO"}:
        return "3-18 months"
    if stage in {"IPO / Public", "Post-IPO"}:
        return "0-12 months"
    return "Unknown"


def opportunity_for_stage(company_name: str, current_stage: str, next_stage: str) -> dict:
    if current_stage in {"Pre-Seed", "Seed"}:
        return {
            "company_name": company_name,
            "current_stage": current_stage,
            "next_likely_stage": next_stage,
            "opportunity_type": "early_round_watch",
            "opportunity_window": "6-18 months",
            "opportunity_title": f"Track {company_name} next early-stage financing",
            "opportunity_description": "Potential opportunity to monitor Seed or Series A financing, accelerator signals, lead investor quality, product traction and first enterprise pilots.",
            "probability_pct": 45,
            "expected_impact_score": 7,
            "access_difficulty_score": 8,
            "investor_action": "Build watchlist, track founders, product traction, hiring and early customers.",
            "watch_signals": "new lead investor, seed/series A filing, enterprise pilots, GitHub/product usage, hiring acceleration",
            "confidence_score": 2,
        }
    if current_stage in {"Series A", "Series B"}:
        return {
            "company_name": company_name,
            "current_stage": current_stage,
            "next_likely_stage": next_stage,
            "opportunity_type": "follow_on_growth_round",
            "opportunity_window": "6-24 months",
            "opportunity_title": f"Monitor {company_name} for next institutional growth round",
            "opportunity_description": "Potential opportunity around Series B/C style repricing, expansion round, enterprise adoption acceleration or valuation reset.",
            "probability_pct": 50,
            "expected_impact_score": 8,
            "access_difficulty_score": 7,
            "investor_action": "Track ARR proxies, enterprise customers, headcount growth, strategic partnerships and round rumors.",
            "watch_signals": "ARR milestone, large customers, new funds, hiring, pricing changes, analyst coverage",
            "confidence_score": 2,
        }
    if current_stage in {"Series C+", "Growth / Pre-IPO"}:
        return {
            "company_name": company_name,
            "current_stage": current_stage,
            "next_likely_stage": next_stage,
            "opportunity_type": "pre_ipo_secondary_or_ipo_watch",
            "opportunity_window": "3-18 months",
            "opportunity_title": f"Watch {company_name} for secondary, M&A or IPO window",
            "opportunity_description": "Potential opportunity around private secondary access, IPO preparation, strategic acquisition or public comparable rerating.",
            "probability_pct": 40,
            "expected_impact_score": 8,
            "access_difficulty_score": 9,
            "investor_action": "Track S-1 rumors, CFO hiring, audited metrics, profitability path, secondary market signals and strategic acquirers.",
            "watch_signals": "CFO hire, bankers, S-1 filing, secondary market pricing, M&A rumors, public comps movement",
            "confidence_score": 2,
        }
    if current_stage in {"IPO / Public", "Post-IPO"}:
        return {
            "company_name": company_name,
            "current_stage": current_stage,
            "next_likely_stage": next_stage,
            "opportunity_type": "public_market_entry_or_rerating",
            "opportunity_window": "0-12 months",
            "opportunity_title": f"Track {company_name} public market entry points and rerating signals",
            "opportunity_description": "Potential opportunity through public market volatility, earnings revisions, lock-up expiry, multiple compression or strategic rerating.",
            "probability_pct": 55,
            "expected_impact_score": 7,
            "access_difficulty_score": 3,
            "investor_action": "Track share price, volume, lock-up expiry, earnings, guidance, valuation multiples and comparable basket.",
            "watch_signals": "earnings, lock-up expiry, analyst upgrades, multiple compression, sector rerating",
            "confidence_score": 3,
        }
    return {
        "company_name": company_name,
        "current_stage": current_stage,
        "next_likely_stage": next_stage,
        "opportunity_type": "data_validation",
        "opportunity_window": "0-3 months",
        "opportunity_title": f"Validate growth stage for {company_name}",
        "opportunity_description": "Current stage is uncertain. The immediate opportunity is to improve data quality before investment interpretation.",
        "probability_pct": 80,
        "expected_impact_score": 5,
        "access_difficulty_score": 5,
        "investor_action": "Find latest funding round, product traction, headcount, public filing or reliable company profile.",
        "watch_signals": "funding database update, company profile, press release, investor announcement, public registry",
        "confidence_score": 1,
    }


def _read_sql(engine, query: str) -> pd.DataFrame:
    with engine.begin() as conn:
        return pd.read_sql(query, conn)


def generate_growth_stage_analysis(engine, run_id: int | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    startups = _read_sql(engine, "SELECT id AS startup_id, name AS company_name, stage FROM startups")
    if startups.empty:
        return pd.DataFrame(), pd.DataFrame()

    financial = _read_sql(
        engine,
        """
        SELECT startup_id, event_date, event_type, event_title, amount, valuation, currency, confidence_score
        FROM financial_events
        ORDER BY startup_id, event_date DESC
        """,
    )
    benchmark = _read_sql(
        engine,
        """
        SELECT startup_id, valuation_latest, valuation_date, latest_round_amount,
               latest_round_date, employees_latest, revenue_latest, currency, data_confidence
        FROM benchmark_metrics
        """,
    )
    ipo = _read_sql(engine, "SELECT DISTINCT startup_id FROM ipo_events")

    latest_financial = financial.dropna(subset=["startup_id"]).drop_duplicates("startup_id") if not financial.empty else pd.DataFrame()
    ipo_ids = set(ipo["startup_id"].dropna().astype(int).tolist()) if not ipo.empty else set()

    merged = startups.merge(latest_financial, on="startup_id", how="left") if not latest_financial.empty else startups.copy()
    merged = merged.merge(benchmark, on="startup_id", how="left", suffixes=("", "_benchmark")) if not benchmark.empty else merged

    snapshots = []
    opportunities = []
    today = date.today().isoformat()
    for _, row in merged.iterrows():
        startup_id = row.get("startup_id")
        company_name = row.get("company_name")
        base_stage = normalize_stage(row.get("stage"))
        latest_round = row.get("event_type") or row.get("event_title")
        has_ipo = pd.notna(startup_id) and int(startup_id) in ipo_ids
        current_stage = infer_stage_from_latest_round(base_stage, latest_round, has_ipo)
        next_stage = NEXT_STAGE.get(current_stage, "Data validation required")
        confidence = 3 if has_ipo else 2
        if pd.notna(row.get("data_confidence")):
            confidence = max(confidence, int(row.get("data_confidence")))

        snapshot = {
            "startup_id": startup_id,
            "company_name": company_name,
            "current_stage": current_stage,
            "stage_basis": "ipo_events" if has_ipo else "startups.stage + latest financial/benchmark seed",
            "last_known_round": latest_round,
            "last_round_date": row.get("event_date") or row.get("latest_round_date"),
            "last_round_amount": row.get("amount") if pd.notna(row.get("amount")) else row.get("latest_round_amount"),
            "last_known_valuation": row.get("valuation") if pd.notna(row.get("valuation")) else row.get("valuation_latest"),
            "currency": row.get("currency") or row.get("currency_benchmark") or "USD",
            "estimated_revenue_band": "unknown" if pd.isna(row.get("revenue_latest")) else "reported_or_estimated",
            "estimated_headcount_band": "unknown" if pd.isna(row.get("employees_latest")) else str(int(row.get("employees_latest"))),
            "next_likely_stage": next_stage,
            "next_stage_horizon": stage_horizon(current_stage),
            "stage_confidence_score": min(confidence, 5),
            "source_url": None,
            "analysis_run_id": run_id,
            "refreshed_at": utc_now_iso(),
        }
        snapshots.append(snapshot)

        opportunity = opportunity_for_stage(str(company_name), current_stage, next_stage)
        opportunity["startup_id"] = startup_id
        opportunity["analysis_run_id"] = run_id
        opportunity["refreshed_at"] = utc_now_iso()
        opportunities.append(opportunity)

    return pd.DataFrame(snapshots), pd.DataFrame(opportunities)


def refresh_growth_stage_tables(engine, run_id: int | None = None) -> dict[str, int]:
    snapshots, opportunities = generate_growth_stage_analysis(engine, run_id=run_id)
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM growth_stage_snapshots"))
        conn.execute(text("DELETE FROM stage_opportunities"))
    if not snapshots.empty:
        snapshots.to_sql("growth_stage_snapshots", engine, if_exists="append", index=False)
    if not opportunities.empty:
        opportunities.to_sql("stage_opportunities", engine, if_exists="append", index=False)

    if run_id is not None:
        log_table_refresh(engine, run_id, "growth_stage_snapshots", len(snapshots), source_name="derived_stage_analysis", source_type="derived_table")
        log_table_refresh(engine, run_id, "stage_opportunities", len(opportunities), source_name="derived_stage_analysis", source_type="derived_table")

    return {
        "growth_stage_snapshots": len(snapshots),
        "stage_opportunities": len(opportunities),
    }
