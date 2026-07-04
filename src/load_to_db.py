from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.db import execute_sql_file, get_engine
from src.scoring import score_dataframe

SEED_PATH = Path("data/seeds/startups_seed.csv")

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


def load_seed_to_db(seed_path: str | Path = SEED_PATH) -> None:
    execute_sql_file()
    engine = get_engine()
    df = pd.read_csv(seed_path)
    scored = score_dataframe(df)

    startups = scored[[col for col in STARTUP_COLUMNS if col in scored.columns]].copy()
    startups.to_sql("startups", engine, if_exists="append", index=False)

    with engine.begin() as conn:
        ids = pd.read_sql("select id, name from startups", conn)

    scores = scored.merge(ids, on="name", how="left")
    scores = scores.rename(columns={"id": "startup_id"})
    scores = scores[["startup_id"] + [col for col in SCORE_COLUMNS if col in scores.columns]].copy()
    scores.to_sql("scores", engine, if_exists="append", index=False)


if __name__ == "__main__":
    load_seed_to_db()
    print("Seed dataset loaded to database")
