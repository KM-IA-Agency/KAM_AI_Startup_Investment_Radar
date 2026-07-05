from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

METRICS_PATH = Path("data/seeds/benchmark_metrics_seed.csv")
OUTPUT_DIR = Path("reports/benchmarks")

KEY_METRICS = [
    "valuation_latest",
    "total_funding",
    "latest_round_amount",
    "employees_latest",
    "employee_growth_6m_pct",
    "revenue_growth_yoy_pct",
    "web_traffic_growth_3m_pct",
    "github_stars_growth_3m_pct",
]


def load_metrics(path: str | Path = METRICS_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def benchmark_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "name",
        "currency",
        "valuation_latest",
        "revenue_latest",
        "revenue_growth_yoy_pct",
        "total_funding",
        "latest_round_amount",
        "employees_latest",
        "employee_growth_6m_pct",
        "data_confidence",
    ]
    return df[[col for col in cols if col in df.columns]].sort_values("valuation_latest", ascending=False)


def generate_synthetic_observations(
    df: pd.DataFrame,
    metric_name: str = "valuation_latest",
    periods: int = 12,
    period_type: str = "monthly",
) -> pd.DataFrame:
    rows = []
    date_index = pd.date_range(end=pd.Timestamp.today().normalize(), periods=periods, freq={
        "daily": "D",
        "weekly": "W",
        "monthly": "ME",
    }.get(period_type, "ME"))

    for _, row in df.iterrows():
        base = row.get(metric_name)
        if pd.isna(base) or float(base) <= 0:
            continue
        growth = row.get("employee_growth_6m_pct", 20)
        if pd.isna(growth):
            growth = 20
        trend = np.linspace(1 - min(float(growth), 100) / 250, 1, periods)
        noise = np.linspace(-0.03, 0.03, periods)
        values = float(base) * (trend + noise)
        for observed_at, value in zip(date_index, values):
            rows.append({
                "name": row["name"],
                "observed_at": observed_at.date().isoformat(),
                "period_type": period_type,
                "metric_name": metric_name,
                "metric_value": max(value, 0),
                "metric_unit": row.get("currency", "USD"),
                "source": "synthetic_mvp",
                "confidence_score": 1,
            })
    return pd.DataFrame(rows)


def save_observations(df: pd.DataFrame, output_dir: str | Path = OUTPUT_DIR) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for period_type, periods in [("daily", 30), ("weekly", 12), ("monthly", 12)]:
        observations = generate_synthetic_observations(df, periods=periods, period_type=period_type)
        path = output_dir / f"observations_{period_type}.csv"
        observations.to_csv(path, index=False)
        paths.append(path)
    return paths


def plot_top_valuations(df: pd.DataFrame, output_dir: str | Path = OUTPUT_DIR) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    top = df.dropna(subset=["valuation_latest"]).sort_values("valuation_latest", ascending=False).head(12)
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(top["name"], top["valuation_latest"] / 1_000_000_000)
    ax.set_title("Top startup valuations - MVP benchmark")
    ax.set_ylabel("Valuation, $/€ billions")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    path = output_dir / "top_valuations.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def plot_metric_history(observations: pd.DataFrame, output_dir: str | Path = OUTPUT_DIR) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_names = observations["name"].drop_duplicates().head(6).tolist()
    sample = observations[observations["name"].isin(sample_names)].copy()
    sample["observed_at"] = pd.to_datetime(sample["observed_at"])
    fig, ax = plt.subplots(figsize=(11, 6))
    for name, group in sample.groupby("name"):
        ax.plot(group["observed_at"], group["metric_value"] / 1_000_000_000, label=name)
    ax.set_title("Valuation history - synthetic MVP time series")
    ax.set_ylabel("Valuation, $/€ billions")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "valuation_history_monthly.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def generate_benchmark_outputs() -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_metrics()
    table_path = OUTPUT_DIR / "benchmark_table.csv"
    benchmark_table(df).to_csv(table_path, index=False)
    paths = [table_path]
    paths.extend(save_observations(df))
    paths.append(plot_top_valuations(df))
    monthly = pd.read_csv(OUTPUT_DIR / "observations_monthly.csv")
    paths.append(plot_metric_history(monthly))
    return paths


if __name__ == "__main__":
    for path in generate_benchmark_outputs():
        print(path)
