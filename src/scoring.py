from pathlib import Path

import pandas as pd

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
]


def clamp(value, low=0, high=100):
    try:
        value = float(value)
    except Exception:
        value = 0
    return int(max(low, min(high, round(value))))


def total_score(row):
    base = sum(clamp(row.get(col, 0), 0, 15) for col in SCORE_COLUMNS)
    risk_penalty = clamp(row.get("risk_score", 0), 0, 10)
    return clamp(base - risk_penalty, 0, 100)


def decision(total, kamel_edge):
    kamel_edge = clamp(kamel_edge, 0, 25)
    if total >= 80 and kamel_edge >= 21:
        return "Investable potential"
    if total >= 80 and kamel_edge >= 18:
        return "Priority investigation"
    if total >= 65 and kamel_edge >= 15:
        return "Strong watch"
    if total >= 50 and kamel_edge >= 15:
        return "Deep dive"
    if total >= 50:
        return "Watch"
    return "Pass"


def explanation(row):
    strengths = []
    if clamp(row.get("market_score", 0), 0, 15) >= 13:
        strengths.append("large market")
    if clamp(row.get("traction_score", 0), 0, 15) >= 12:
        strengths.append("visible traction")
    if clamp(row.get("technical_moat_score", 0), 0, 15) >= 12:
        strengths.append("technical moat")
    if clamp(row.get("kamel_edge_score", 0), 0, 25) >= 20:
        strengths.append("strong Kamel Edge")
    return ", ".join(strengths) if strengths else "needs more data"


def score_dataframe(df):
    scored = df.copy()
    for col in SCORE_COLUMNS + ["risk_score", "kamel_edge_score"]:
        if col not in scored.columns:
            scored[col] = 0
        scored[col] = scored[col].apply(clamp)
    scored["total_score"] = scored.apply(total_score, axis=1)
    scored["decision"] = scored.apply(lambda r: decision(r["total_score"], r["kamel_edge_score"]), axis=1)
    scored["score_explanation"] = scored.apply(explanation, axis=1)
    return scored.sort_values(["total_score", "kamel_edge_score"], ascending=False)


def load_seed(path="data/seeds/startups_seed.csv"):
    return pd.read_csv(path)


def save_scored_dataset(input_path="data/seeds/startups_seed.csv", output_path="data/processed/scored_startups.csv"):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scored = score_dataframe(load_seed(input_path))
    scored.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    print(save_scored_dataset())
