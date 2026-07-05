from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from src.formatting import format_number

EVENTS_PATH = Path("data/seeds/financial_events_seed.csv")
FORECAST_PATH = Path("reports/forecasts/scenario_forecasts.csv")
OUTPUT_DIR = Path("reports/timelines")


def load_events(path=EVENTS_PATH):
    df = pd.read_csv(path)
    df["event_date"] = pd.to_datetime(df["event_date"])
    return df.sort_values(["name", "event_date"])


def load_forecasts(path=FORECAST_PATH):
    if Path(path).exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def timeline_table(events):
    table = events.copy()
    for col in ["amount", "valuation", "share_price"]:
        if col in table.columns:
            table[f"{col}_readable"] = table[col].apply(format_number)
    return table


def plot_funding_and_valuation(events, startup_name, output_dir=OUTPUT_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = events[events["name"] == startup_name].copy()
    if df.empty:
        raise ValueError(f"No events for {startup_name}")

    fig, ax = plt.subplots(figsize=(11, 6))
    funding = df.dropna(subset=["amount"])
    valuation = df.dropna(subset=["valuation"])

    if not funding.empty:
        ax.bar(funding["event_date"], funding["amount"] / 1_000_000_000, width=35, alpha=0.45, label="Funding round")
    if not valuation.empty:
        ax.plot(valuation["event_date"], valuation["valuation"] / 1_000_000_000, marker="o", label="Valuation")

    for _, row in df.iterrows():
        y = row["valuation"] / 1_000_000_000 if pd.notna(row.get("valuation")) else row["amount"] / 1_000_000_000
        label = row.get("event_type", "event")
        ax.annotate(label, (row["event_date"], y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)

    ax.set_title(f"Funding and valuation timeline - {startup_name}")
    ax.set_ylabel("Amount / valuation, billions")
    ax.legend()
    fig.tight_layout()
    path = output_dir / f"timeline_{startup_name.lower().replace(' ', '_')}.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def plot_valuation_with_forecasts(events, forecasts, startup_name, output_dir=OUTPUT_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    event_df = events[events["name"] == startup_name].dropna(subset=["valuation"]).copy()
    forecast_df = forecasts[forecasts["name"] == startup_name].copy() if not forecasts.empty else pd.DataFrame()
    if event_df.empty and forecast_df.empty:
        raise ValueError(f"No valuation or forecast for {startup_name}")

    fig, ax = plt.subplots(figsize=(11, 6))
    if not event_df.empty:
        ax.plot(event_df["event_date"], event_df["valuation"] / 1_000_000_000, marker="o", label="Historical valuation")

    if not forecast_df.empty:
        base_date = pd.Timestamp.today().normalize()
        forecast_df["forecast_date_plot"] = forecast_df["horizon_months"].apply(lambda m: base_date + pd.DateOffset(months=int(m)))
        for scenario, group in forecast_df.groupby("scenario_label"):
            group = group.sort_values("forecast_date_plot")
            ax.plot(group["forecast_date_plot"], group["forecast_value"] / 1_000_000_000, marker="x", linestyle="--", label=f"Forecast {scenario}")

    ax.set_title(f"Historical valuation and future scenarios - {startup_name}")
    ax.set_ylabel("Valuation, billions")
    ax.legend()
    fig.tight_layout()
    path = output_dir / f"valuation_future_{startup_name.lower().replace(' ', '_')}.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def generate_timeline_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    events = load_events()
    forecasts = load_forecasts()

    table = timeline_table(events)
    table_path = OUTPUT_DIR / "financial_events_table.csv"
    table.to_csv(table_path, index=False)

    paths = [table_path]
    for startup_name in events["name"].drop_duplicates():
        paths.append(plot_funding_and_valuation(events, startup_name))
        try:
            paths.append(plot_valuation_with_forecasts(events, forecasts, startup_name))
        except ValueError:
            pass
    return paths


if __name__ == "__main__":
    for path in generate_timeline_outputs():
        print(path)
