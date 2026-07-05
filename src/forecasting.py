from __future__ import annotations

from pathlib import Path
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt

METRICS_PATH = Path("data/seeds/benchmark_metrics_seed.csv")
OUTPUT_DIR = Path("reports/forecasts")

SHORT_TERM_HORIZONS = (1, 2, 3, 6)
LONG_TERM_HORIZONS = (12, 36, 60)
ALL_HORIZONS = SHORT_TERM_HORIZONS + LONG_TERM_HORIZONS

SCENARIOS = {
    "bear": {"growth_multiplier": 0.6, "probability_pct": 35, "label": "Pessimistic"},
    "base": {"growth_multiplier": 1.0, "probability_pct": 45, "label": "Base"},
    "bull": {"growth_multiplier": 1.8, "probability_pct": 20, "label": "Optimistic"},
}

DEFAULT_GROWTH_BY_SECTOR = {
    "Physical AI / Robotics": 45,
    "AI Infrastructure": 50,
    "Data Infrastructure": 35,
    "Climate / MRV": 25,
    "GPU Cloud": 40,
    "Cloud Infrastructure": 20,
    "Satellite / Geospatial": 25,
}


def load_metrics(path=METRICS_PATH):
    return pd.read_csv(path)


def infer_base_growth(row):
    for col in ["revenue_growth_yoy_pct", "employee_growth_6m_pct", "web_traffic_growth_3m_pct", "github_stars_growth_3m_pct"]:
        value = row.get(col)
        if pd.notna(value) and float(value) > 0:
            if col == "employee_growth_6m_pct":
                return min(float(value) * 1.4, 120)
            return min(float(value), 150)
    return DEFAULT_GROWTH_BY_SECTOR.get(row.get("sector", ""), 25)


def short_term_momentum_boost(row):
    """Fast-growth startups can move sharply in 1-6 months.

    This boost is intentionally conservative and should be replaced with
    actual daily or weekly observations when available.
    """
    sector = row.get("sector", "")
    if sector == "Physical AI / Robotics":
        return 1.25
    if sector in ["AI Infrastructure", "GPU Cloud"]:
        return 1.15
    return 1.0


def forecast_value(current_value, annual_growth_pct, horizon_months):
    if pd.isna(current_value) or float(current_value) <= 0:
        return None
    years = horizon_months / 12
    return float(current_value) * ((1 + annual_growth_pct / 100) ** years)


def confidence(row):
    value = row.get("data_confidence", 1)
    if pd.isna(value):
        return 1
    return int(max(1, min(5, int(value))))


def horizon_bucket(horizon_months):
    return "short_term" if horizon_months <= 6 else "long_term"


def generate_forecasts(df, horizons=ALL_HORIZONS, metric_name="valuation_latest"):
    rows = []
    today = date.today().isoformat()
    for _, row in df.iterrows():
        current = row.get(metric_name)
        if pd.isna(current) or float(current) <= 0:
            continue
        base_growth = infer_base_growth(row)
        for horizon in horizons:
            for scenario, params in SCENARIOS.items():
                growth = base_growth * params["growth_multiplier"]
                if horizon <= 6:
                    growth = growth * short_term_momentum_boost(row)
                forecast = forecast_value(current, growth, horizon)
                rows.append({
                    "name": row.get("name"),
                    "forecast_date": today,
                    "horizon_months": horizon,
                    "horizon_bucket": horizon_bucket(horizon),
                    "scenario": scenario,
                    "scenario_label": params["label"],
                    "metric_name": metric_name,
                    "current_value": float(current),
                    "forecast_value": forecast,
                    "implied_cagr_pct": growth,
                    "probability_pct": params["probability_pct"],
                    "confidence_score": confidence(row),
                    "assumptions": "Scenario forecast based on benchmark growth proxies; not a prediction.",
                })
    return pd.DataFrame(rows)


def expected_value(forecasts):
    df = forecasts.copy()
    df["weighted_value"] = df["forecast_value"] * (df["probability_pct"] / 100)
    ev = (
        df.groupby(["name", "horizon_months", "horizon_bucket", "metric_name"])
        .agg(expected_forecast_value=("weighted_value", "sum"), confidence_score=("confidence_score", "mean"))
        .reset_index()
        .sort_values(["horizon_months", "expected_forecast_value"], ascending=[True, False])
    )
    return ev


def plot_forecast_for_startup(forecasts, startup_name, output_dir=OUTPUT_DIR, short_term=False):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = forecasts[forecasts["name"] == startup_name].copy()
    if short_term:
        df = df[df["horizon_months"].isin(SHORT_TERM_HORIZONS)]
    if df.empty:
        raise ValueError(f"No forecast for {startup_name}")
    fig, ax = plt.subplots(figsize=(9, 5))
    for scenario, group in df.groupby("scenario_label"):
        group = group.sort_values("horizon_months")
        ax.plot(group["horizon_months"], group["forecast_value"] / 1_000_000_000, marker="o", label=scenario)
    title_prefix = "Short-term scenario forecast" if short_term else "Scenario forecast"
    ax.set_title(f"{title_prefix} - {startup_name}")
    ax.set_xlabel("Horizon, months")
    ax.set_ylabel("Forecast valuation, billions")
    ax.legend()
    fig.tight_layout()
    suffix = "short_term" if short_term else "full"
    path = output_dir / f"forecast_{startup_name.lower().replace(' ', '_')}_{suffix}.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def generate_forecast_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics = load_metrics()
    forecasts = generate_forecasts(metrics)
    forecast_path = OUTPUT_DIR / "scenario_forecasts.csv"
    short_term_path = OUTPUT_DIR / "scenario_forecasts_short_term.csv"
    expected_path = OUTPUT_DIR / "expected_values.csv"
    expected_short_path = OUTPUT_DIR / "expected_values_short_term.csv"

    forecasts.to_csv(forecast_path, index=False)
    forecasts[forecasts["horizon_months"].isin(SHORT_TERM_HORIZONS)].to_csv(short_term_path, index=False)
    expected_value(forecasts).to_csv(expected_path, index=False)
    expected_value(forecasts[forecasts["horizon_months"].isin(SHORT_TERM_HORIZONS)]).to_csv(expected_short_path, index=False)

    paths = [forecast_path, short_term_path, expected_path, expected_short_path]
    for startup_name in forecasts["name"].drop_duplicates().head(5):
        paths.append(plot_forecast_for_startup(forecasts, startup_name))
        paths.append(plot_forecast_for_startup(forecasts, startup_name, short_term=True))
    return paths


if __name__ == "__main__":
    for path in generate_forecast_outputs():
        print(path)
