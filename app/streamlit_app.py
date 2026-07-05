from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.db import get_engine
from src.scoring import score_dataframe

DATA_PATH = ROOT / "data" / "seeds" / "startups_seed.csv"
BENCHMARK_PATH = ROOT / "data" / "seeds" / "benchmark_metrics_seed.csv"
FORECAST_PATH = ROOT / "reports" / "forecasts" / "scenario_forecasts.csv"
FORECAST_SHORT_PATH = ROOT / "reports" / "forecasts" / "scenario_forecasts_short_term.csv"

st.set_page_config(page_title="KAM AI Startup Radar", layout="wide")

st.title("KAM AI Startup Investment Radar")
st.caption("MVP de veille, scoring, benchmark, forecasts et watchlist startup IA / Deeptech")


def load_from_csv():
    df = pd.read_csv(DATA_PATH)
    scored = score_dataframe(df)
    return scored, "CSV seed"


def load_from_database():
    engine = get_engine()
    query = """
    SELECT
        s.name,
        s.website,
        s.country,
        s.region,
        s.sector,
        s.sub_sector,
        s.stage,
        s.description,
        s.source_url,
        sc.market_score,
        sc.problem_pain_score,
        sc.product_maturity_score,
        sc.traction_score,
        sc.team_score,
        sc.technical_moat_score,
        sc.valuation_score,
        sc.investor_quality_score,
        sc.exit_potential_score,
        sc.risk_score,
        sc.kamel_edge_score,
        sc.total_score,
        sc.decision,
        sc.score_explanation
    FROM startups s
    LEFT JOIN scores sc ON sc.startup_id = s.id
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        raise ValueError("database is empty")
    return df.sort_values(["total_score", "kamel_edge_score"], ascending=False), "Database"


@st.cache_data
def load_data():
    try:
        return load_from_database()
    except Exception:
        return load_from_csv()


@st.cache_data
def load_benchmark():
    if BENCHMARK_PATH.exists():
        return pd.read_csv(BENCHMARK_PATH)
    return pd.DataFrame()


@st.cache_data
def load_forecasts(short_term=False):
    path = FORECAST_SHORT_PATH if short_term else FORECAST_PATH
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def metric_value(df, column, default=0):
    if df.empty or column not in df.columns:
        return default
    value = df[column].mean()
    if pd.isna(value):
        return default
    return round(value, 1)


def display_score_metrics(frame):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Startups", len(frame))
    c2.metric("Score moyen", metric_value(frame, "total_score"))
    c3.metric("Top score", int(frame["total_score"].max()) if len(frame) else 0)
    c4.metric("Kamel Edge moy.", metric_value(frame, "kamel_edge_score"))
    c5.metric("Risque moy.", metric_value(frame, "risk_score"))


def safe_columns(frame, columns):
    return [col for col in columns if col in frame.columns]


try:
    df, data_source = load_data()
except Exception as exc:
    st.error(f"Impossible de charger le dataset: {exc}")
    st.stop()

benchmark_df = load_benchmark()
forecast_df = load_forecasts(short_term=False)
forecast_short_df = load_forecasts(short_term=True)

st.info(f"Source de données active : {data_source}")

with st.sidebar:
    st.header("Filtres")
    countries = sorted(df["country"].dropna().unique().tolist())
    sectors = sorted(df["sector"].dropna().unique().tolist())
    decisions = sorted(df["decision"].dropna().unique().tolist())

    selected_countries = st.multiselect("Pays", countries, default=countries)
    selected_sectors = st.multiselect("Secteurs", sectors, default=sectors)
    selected_decisions = st.multiselect("Décisions", decisions, default=decisions)
    min_score = st.slider("Score minimum", 0, 100, 0)
    selected_startup = st.selectbox("Startup focus", df["name"].tolist() if len(df) else [])

filtered = df[
    df["country"].isin(selected_countries)
    & df["sector"].isin(selected_sectors)
    & df["decision"].isin(selected_decisions)
    & (df["total_score"] >= min_score)
]

tab_overview, tab_watchlist, tab_benchmark, tab_forecast, tab_robotics, tab_detail = st.tabs([
    "Overview",
    "Watchlist",
    "Benchmark",
    "Forecasts",
    "Physical AI",
    "Startup Detail",
])

with tab_overview:
    st.subheader("Vue exécutive")
    display_score_metrics(filtered)

    left, right = st.columns(2)
    with left:
        st.markdown("### Répartition par secteur")
        sector_counts = filtered["sector"].value_counts().reset_index()
        sector_counts.columns = ["sector", "count"]
        st.bar_chart(sector_counts.set_index("sector"))
    with right:
        st.markdown("### Score moyen par secteur")
        sector_score = filtered.groupby("sector")["total_score"].mean().sort_values(ascending=False)
        st.bar_chart(sector_score)

    st.markdown("### Top opportunités")
    st.dataframe(
        filtered.head(10)[safe_columns(filtered, ["name", "country", "sector", "sub_sector", "stage", "total_score", "kamel_edge_score", "risk_score", "decision"])],
        use_container_width=True,
    )

with tab_watchlist:
    st.subheader("Watchlist filtrable")
    st.dataframe(
        filtered[safe_columns(filtered, [
            "name", "country", "region", "sector", "sub_sector", "stage", "total_score",
            "market_score", "traction_score", "technical_moat_score", "valuation_score",
            "risk_score", "kamel_edge_score", "decision", "website"
        ])],
        use_container_width=True,
    )

    st.markdown("### Comparaison score vs risque")
    chart_df = filtered[["name", "total_score", "risk_score", "kamel_edge_score"]].dropna().set_index("name")
    if not chart_df.empty:
        st.scatter_chart(chart_df, x="risk_score", y="total_score", size="kamel_edge_score")

with tab_benchmark:
    st.subheader("Benchmark classique : CA, valorisation, funding, croissance")
    if benchmark_df.empty:
        st.warning("Aucun benchmark disponible. Lance ou renseigne data/seeds/benchmark_metrics_seed.csv.")
    else:
        merged = filtered[["name", "sector", "total_score", "risk_score", "kamel_edge_score", "decision"]].merge(benchmark_df, on="name", how="left")
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Valorisation moy.", round(merged["valuation_latest"].dropna().mean() / 1_000_000_000, 2) if "valuation_latest" in merged else 0)
        b2.metric("Funding moyen", round(merged["total_funding"].dropna().mean() / 1_000_000_000, 2) if "total_funding" in merged else 0)
        b3.metric("Croissance effectifs moy.", metric_value(merged, "employee_growth_6m_pct"))
        b4.metric("Confiance données", metric_value(merged, "data_confidence"))

        st.markdown("### Tableau benchmark")
        st.dataframe(
            merged[safe_columns(merged, [
                "name", "sector", "total_score", "risk_score", "valuation_latest", "valuation_date",
                "total_funding", "latest_round_amount", "employees_latest", "employee_growth_6m_pct",
                "revenue_latest", "revenue_growth_yoy_pct", "data_confidence", "notes"
            ])].sort_values("valuation_latest", ascending=False, na_position="last"),
            use_container_width=True,
        )

        st.markdown("### Top valorisations")
        val_chart = merged.dropna(subset=["valuation_latest"])[["name", "valuation_latest"]].sort_values("valuation_latest", ascending=False).head(15)
        if not val_chart.empty:
            st.bar_chart(val_chart.set_index("name") / 1_000_000_000)

with tab_forecast:
    st.subheader("Scénarios prévisionnels")
    st.caption("Ces résultats sont des scénarios, pas des prédictions certaines ni des conseils financiers.")

    selected_forecast_view = st.radio("Vue", ["Court terme 1/2/3/6 mois", "Complet 1 à 60 mois"], horizontal=True)
    active_forecast = forecast_short_df if selected_forecast_view.startswith("Court") else forecast_df

    if active_forecast.empty:
        st.warning("Aucun forecast généré. Lance `python src/forecasting.py`.")
    else:
        focus_forecast = active_forecast[active_forecast["name"] == selected_startup]
        if focus_forecast.empty:
            st.info("Pas de forecast pour la startup sélectionnée.")
        else:
            st.markdown(f"### Forecast — {selected_startup}")
            st.dataframe(
                focus_forecast[safe_columns(focus_forecast, [
                    "horizon_months", "scenario_label", "metric_name", "current_value", "forecast_value",
                    "implied_cagr_pct", "probability_pct", "confidence_score", "assumptions"
                ])].sort_values(["horizon_months", "scenario_label"]),
                use_container_width=True,
            )
            pivot = focus_forecast.pivot_table(index="horizon_months", columns="scenario_label", values="forecast_value", aggfunc="mean")
            if not pivot.empty:
                st.line_chart(pivot / 1_000_000_000)

        st.markdown("### Expected value — Top startups")
        ev = active_forecast.copy()
        ev["weighted_value"] = ev["forecast_value"] * (ev["probability_pct"] / 100)
        ev = ev.groupby(["name", "horizon_months"]).agg(expected_value=("weighted_value", "sum"), confidence=("confidence_score", "mean")).reset_index()
        st.dataframe(ev.sort_values(["horizon_months", "expected_value"], ascending=[True, False]).head(30), use_container_width=True)

with tab_robotics:
    st.subheader("Physical AI / Robotics")
    robotics = filtered[filtered["sector"].str.contains("Physical AI", na=False)]
    if robotics.empty:
        st.info("Aucune startup Physical AI dans le filtre actuel.")
    else:
        display_score_metrics(robotics)
        st.dataframe(
            robotics[safe_columns(robotics, ["name", "country", "sub_sector", "stage", "total_score", "technical_moat_score", "risk_score", "kamel_edge_score", "decision"])],
            use_container_width=True,
        )
        st.markdown("### Score vs risque — Robotique")
        robot_chart = robotics[["name", "total_score", "risk_score", "technical_moat_score"]].dropna().set_index("name")
        if not robot_chart.empty:
            st.scatter_chart(robot_chart, x="risk_score", y="total_score", size="technical_moat_score")

with tab_detail:
    st.subheader("Fiche startup")
    if selected_startup:
        row = df[df["name"] == selected_startup].iloc[0]
        st.markdown(f"### {row['name']}")
        st.write(row.get("description", ""))
        a, b, c, d = st.columns(4)
        a.metric("Score total", int(row["total_score"]))
        b.metric("Kamel Edge", int(row["kamel_edge_score"]))
        c.metric("Risque", int(row["risk_score"]))
        d.metric("Moat tech", int(row.get("technical_moat_score", 0)))
        st.markdown("**Décision :** " + str(row["decision"]))
        st.markdown("**Explication :** " + str(row["score_explanation"]))
        st.markdown("**Site / source :**")
        st.write(row.get("website", ""))
        st.write(row.get("source_url", ""))

st.warning("Ce MVP produit des scores, scénarios et benchmarks de veille. Il ne constitue pas un conseil en investissement financier personnalisé.")
