from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.db import execute_sql_file, get_engine
from src.scoring import score_dataframe

SEED_PATH = Path("data/seeds/startups_seed.csv")
PRODUCT_MAPPING_PATH = Path("data/seeds/company_product_mapping_seed.csv")
AI_TOOLS_TAXONOMY_PATH = Path("data/seeds/ai_tools_trending_by_category_july2026.csv")
VIBE_CODING_TOP20_PATH = Path("data/seeds/vibe_coding_top20_july2026.csv")

STARTUP_COLUMNS = [
    "name",
    "website",
    "country",
    "region",
    "sector",
    "sub_sector",
    "stage",
    "description",
    "source_url",
]

SCORE_COLUMNS = [
    "market_score",
    "problem_pain_score",
    "product_maturity_score",
    "traction_score",
    "team_score",
    "technical_moat_score",
    "valuation_score",
    "investor_quality_score",
    "exit_potential_score",
    "risk_score",
    "kamel_edge_score",
    "total_score",
    "decision",
    "score_explanation",
]


def reset_seed_tables(engine) -> None:
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM ai_tools"))
        conn.execute(text("DELETE FROM product_mappings"))
        conn.execute(text("DELETE FROM scores"))
        conn.execute(text("DELETE FROM startups"))


def _startup_ids(engine) -> pd.DataFrame:
    with engine.begin() as conn:
        return pd.read_sql("select id as startup_id, name from startups", conn)


def _resolve_startup_id(frame: pd.DataFrame, engine, company_column: str = "company_name") -> pd.DataFrame:
    ids = _startup_ids(engine)
    if frame.empty or company_column not in frame.columns:
        frame["startup_id"] = None
        return frame
    resolved = frame.merge(ids, left_on=company_column, right_on="name", how="left")
    resolved = resolved.drop(columns=["name"], errors="ignore")
    return resolved


def _load_product_mappings(engine) -> None:
    if not PRODUCT_MAPPING_PATH.exists():
        return

    mapping = pd.read_csv(PRODUCT_MAPPING_PATH)
    if mapping.empty:
        return

    mapping = _resolve_startup_id(mapping, engine, "company_name")
    cols = [
        "startup_id",
        "company_name",
        "public_name",
        "flagship_product",
        "product_category",
        "related_startup_or_segment",
        "ticker",
        "exchange_name",
        "status",
        "notes",
    ]
    mapping[[col for col in cols if col in mapping.columns]].to_sql(
        "product_mappings", engine, if_exists="append", index=False
    )


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
            top20_norm = pd.DataFrame(
                {
                    "tool_or_group": top20.get("tool_or_group"),
                    "company_name": top20.get("company_or_owner"),
                    "category": top20.get("category"),
                    "role": top20.get("primary_role"),
                    "investment_relevance": top20.get("investable_entity"),
                    "radar_priority": "High",
                    "status": top20.get("status"),
                    "source_dataset": VIBE_CODING_TOP20_PATH.name,
                    "notes": top20.get("radar_action"),
                }
            )
            frames.append(top20_norm)

    if not frames:
        return pd.DataFrame()

    tools = pd.concat(frames, ignore_index=True)
    tools = tools.dropna(subset=["tool_or_group", "category"])
    tools = tools.drop_duplicates(subset=["tool_or_group", "company_name", "category"], keep="first")
    return tools


def _load_ai_tools(engine) -> None:
    tools = _normalize_ai_tools_seed()
    if tools.empty:
        return

    tools = _resolve_startup_id(tools, engine, "company_name")
    cols = [
        "startup_id",
        "company_name",
        "tool_or_group",
        "category",
        "role",
        "investment_relevance",
        "radar_priority",
        "status",
        "source_dataset",
        "notes",
    ]
    tools[[col for col in cols if col in tools.columns]].to_sql(
        "ai_tools", engine, if_exists="append", index=False
    )


def load_seed_to_db(seed_path: str | Path = SEED_PATH, reset: bool = True) -> None:
    execute_sql_file()
    engine = get_engine()
    if reset:
        reset_seed_tables(engine)

    df = pd.read_csv(seed_path)
    scored = score_dataframe(df)

    startups = scored[[col for col in STARTUP_COLUMNS if col in scored.columns]].copy()
    startups.to_sql("startups", engine, if_exists="append", index=False)

    ids = _startup_ids(engine)

    scores = scored.merge(ids.rename(columns={"startup_id": "id"}), on="name", how="left")
    scores = scores.rename(columns={"id": "startup_id"})
    scores = scores[["startup_id"] + [col for col in SCORE_COLUMNS if col in scores.columns]].copy()
    scores.to_sql("scores", engine, if_exists="append", index=False)

    _load_product_mappings(engine)
    _load_ai_tools(engine)


if __name__ == "__main__":
    load_seed_to_db()
    print("Seed dataset, product mappings and AI tools taxonomy loaded to database")
