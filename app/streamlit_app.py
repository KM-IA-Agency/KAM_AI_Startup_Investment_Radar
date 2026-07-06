from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.ai_tools_view import render_ai_tools_stack_view
from src.db import get_engine
from src.events_view import render_product_and_events_view
from src.formatting import add_readable_columns, format_number, format_percent
from src.ipo_view import render_ipo_and_share_view
from src.refresh_service import refresh_market_data
from src.scoring import score_dataframe
from src.stage_view import render_stage_opportunities_view

DATA_PATH = ROOT / "data" / "seeds" / "startups_seed.csv"
BENCHMARK_PATH = ROOT / "data" / "seeds" / "benchmark_metrics_seed.csv"
FINANCIAL_EVENTS_PATH = ROOT / "data" / "seeds" / "financial_events_seed.csv"
IPO_EVENTS_PATH = ROOT / "data" / "seeds" / "ipo_events_seed.csv"
PUBLIC_MARKET_PATH = ROOT / "data" / "seeds" / "public_market_observations_seed.csv"
PRODUCT_MAPPING_PATH = ROOT / "data" / "seeds" / "company_product_mapping_seed.csv"
UPCOMING_EVENTS_PATH = ROOT / "data" / "seeds" / "upcoming_events_seed.csv"
AI_TOOLS_TAXONOMY_PATH = ROOT / "data" / "seeds" / "ai_tools_trending_by_category_july2026.csv"
VIBE_CODING_TOP20_PATH = ROOT / "data" / "seeds" / "vibe_coding_top20_july2026.csv"
FORECAST_PATH = ROOT / "reports" / "forecasts" / "scenario_forecasts.csv"
FORECAST_SHORT_PATH = ROOT / "reports" / "forecasts" / "scenario_forecasts_short_term.csv"
EMPTY_FALLBACK_PATH = ROOT / "data" / "seeds" / "__empty_fallback.csv"

st.set_page_config(page_title="KAM AI Startup Radar", layout="wide")
st.title("KAM AI Startup Investment Radar")
st.caption("MVP de veille, scoring, market map IA, benchmark, forecasts, IPO, actions, produits et événements startup IA / Deeptech")


def load_from_csv():
    return score_dataframe(pd.read_csv(DATA_PATH)), "CSV seed"


def load_from_database():
    engine = get_engine()
    query = """
    SELECT s.name, s.website, s.country, s.region, s.sector, s.sub_sector,
           s.stage, s.description, s.source_url,
           sc.market_score, sc.problem_pain_score, sc.product_maturity_score,
           sc.traction_score, sc.team_score, sc.technical_moat_score,
           sc.valuation_score, sc.investor_quality_score, sc.exit_potential_score,
           sc.risk_score, sc.kamel_edge_score, sc.total_score, sc.decision,
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
def load_optional_csv(path):
    return pd.read_csv(path) if Path(path).exists() else pd.DataFrame()


@st.cache_data
def load_optional_db_query(query: str, fallback_path: str | Path) -> tuple[pd.DataFrame, str]:
    try:
        engine = get_engine()
        frame = pd.read_sql(query, engine)
        if not frame.empty:
            return frame, "Database"
    except Exception:
        pass
    fallback = load_optional_csv(fallback_path)
    return fallback, f"CSV:{Path(fallback_path).name}"


@st.cache_data
def load_forecasts_db_first() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    query = """
    SELECT s.name,
           sf.forecast_date,
           sf.horizon_months,
           CASE WHEN sf.horizon_months <= 6 THEN 'short_term' ELSE 'long_term' END AS horizon_bucket,
           sf.scenario,
           sf.scenario AS scenario_label,
           sf.metric_name,
           sf.current_value,
           sf.forecast_value,
           sf.implied_cagr_pct,
           sf.probability_pct,
           sf.confidence_score,
           sf.assumptions
    FROM scenario_forecasts sf
    LEFT JOIN startups s ON s.id = sf.startup_id
    """
    try:
        engine = get_engine()
        frame = pd.read_sql(query, engine)
        if not frame.empty:
            short = frame[frame["horizon_months"] <= 6].copy()
            return frame, short, "Database"
    except Exception:
        pass
    full = load_optional_csv(FORECAST_PATH)
    short = load_optional_csv(FORECAST_SHORT_PATH)
    return full, short, "CSV forecast files"


def metric_value(df, column, default=0):
    if df.empty or column not in df.columns:
        return default
    value = df[column].mean()
    return default if pd.isna(value) else round(value, 1)


def safe_columns(frame, columns):
    return [col for col in columns if col in frame.columns]


def display_score_metrics(frame):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Startups", len(frame))
    c2.metric("Score moyen", metric_value(frame, "total_score"))
    c3.metric("Top score", int(frame["total_score"].max()) if len(frame) else 0)
    c4.metric("Kamel Edge moy.", metric_value(frame, "kamel_edge_score"))
    c5.metric("Risque moy.", metric_value(frame, "risk_score"))


with st.sidebar:
    st.header("Actualisation")
    fast_refresh = st.checkbox(
        "Mode rapide : ne pas recalculer les forecasts",
        value=False,
        help="Utile pour recharger les tables depuis les seeds/sources sans régénérer les scénarios prévisionnels.",
    )
    if st.button("🔄 Actualiser maintenant", type="primary", use_container_width=True):
        try:
            with st.spinner("Actualisation des données, écriture SQLite et vidage du cache..."):
                result = refresh_market_data(
                    cadence="manual",
                    trigger_source="streamlit_button",
                    skip_forecasting=fast_refresh,
                    reset=True,
                )
                st.cache_data.clear()
                st.session_state["refresh_message"] = result.message
            st.rerun()
        except Exception as exc:
            st.error(f"Échec de l'actualisation : {exc}")

if "refresh_message" in st.session_state:
    st.success(st.session_state.pop("refresh_message"))


df, data_source = load_data()
benchmark_df, benchmark_source = load_optional_db_query(
    """
    SELECT s.name, bm.*
    FROM benchmark_metrics bm
    LEFT JOIN startups s ON s.id = bm.startup_id
    """,
    BENCHMARK_PATH,
)
financial_events_df, financial_events_source = load_optional_db_query(
    """
    SELECT s.name, fe.*
    FROM financial_events fe
    LEFT JOIN startups s ON s.id = fe.startup_id
    """,
    FINANCIAL_EVENTS_PATH,
)
ipo_events_df, ipo_source = load_optional_db_query(
    "SELECT ie.* FROM ipo_events ie",
    IPO_EVENTS_PATH,
)
public_market_df, public_market_source = load_optional_db_query(
    """
    SELECT s.name, pmo.*
    FROM public_market_observations pmo
    LEFT JOIN startups s ON s.id = pmo.startup_id
    """,
    PUBLIC_MARKET_PATH,
)
product_mapping_df, product_mapping_source = load_optional_db_query(
    "SELECT * FROM product_mappings",
    PRODUCT_MAPPING_PATH,
)
upcoming_events_df, upcoming_events_source = load_optional_db_query(
    "SELECT * FROM upcoming_events",
    UPCOMING_EVENTS_PATH,
)
ai_tools_taxonomy_df, ai_tools_source = load_optional_db_query(
    "SELECT * FROM ai_tools",
    AI_TOOLS_TAXONOMY_PATH,
)
growth_stage_df, growth_stage_source = load_optional_db_query(
    "SELECT * FROM growth_stage_snapshots",
    EMPTY_FALLBACK_PATH,
)
stage_opportunities_df, stage_opportunities_source = load_optional_db_query(
    "SELECT * FROM stage_opportunities",
    EMPTY_FALLBACK_PATH,
)
vibe_coding_top20_df = load_optional_csv(VIBE_CODING_TOP20_PATH)
forecast_df, forecast_short_df, forecast_source = load_forecasts_db_first()

st.info(
    f"Sources : startups={data_source} · ai_tools={ai_tools_source} · products={product_mapping_source} · "
    f"benchmark={benchmark_source} · forecasts={forecast_source} · events={upcoming_events_source} · stages={growth_stage_source}"
)

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
    st.caption("Ce focus est propagé aux onglets compatibles : AI Tools, Benchmark, Forecasts, Timeline, Stage, IPO, Products & Events, Startup Detail.")

filtered = df[
    df["country"].isin(selected_countries)
    & df["sector"].isin(selected_sectors)
    & df["decision"].isin(selected_decisions)
    & (df["total_score"] >= min_score)
]

tabs = st.tabs([
    "Overview", "Watchlist", "AI Tools Stack", "Benchmark", "Forecasts",
    "Financial Timeline", "Stage & Opportunities", "IPO & Actions",
    "Products & Events", "Physical AI", "Startup Detail"
])

with tabs[0]:
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
        st.bar_chart(filtered.groupby("sector")["total_score"].mean().sort_values(ascending=False))
    st.markdown("### Top opportunités")
    st.dataframe(filtered.head(10)[safe_columns(filtered, ["name", "country", "sector", "sub_sector", "stage", "total_score", "kamel_edge_score", "risk_score", "decision"])], use_container_width=True)

with tabs[1]:
    st.subheader("Watchlist filtrable")
    watch_cols = ["name", "country", "region", "sector", "sub_sector", "stage", "total_score", "market_score", "traction_score", "technical_moat_score", "valuation_score", "risk_score", "kamel_edge_score", "decision", "website"]
    st.dataframe(filtered[safe_columns(filtered, watch_cols)], use_container_width=True)
    st.markdown("### Comparaison score vs risque")
    chart_df = filtered[["name", "total_score", "risk_score", "kamel_edge_score"]].dropna().set_index("name")
    if not chart_df.empty:
        st.scatter_chart(chart_df, x="risk_score", y="total_score", size="kamel_edge_score")

with tabs[2]:
    render_ai_tools_stack_view(ai_tools_taxonomy_df, vibe_coding_top20_df, selected_company=selected_startup)

with tabs[3]:
    st.subheader("Benchmark classique : CA, valorisation, funding, croissance")
    if benchmark_df.empty:
        st.warning("Aucun benchmark disponible. Lance ou renseigne data/seeds/benchmark_metrics_seed.csv.")
    else:
        merged = filtered[["name", "sector", "total_score", "risk_score", "kamel_edge_score", "decision"]].merge(benchmark_df, on="name", how="left")
        focus_benchmark = merged[merged["name"] == selected_startup].copy()
        if not focus_benchmark.empty:
            st.markdown(f"### Focus benchmark — {selected_startup}")
            focus_row = focus_benchmark.iloc[0]
            f1, f2, f3, f4 = st.columns(4)
            f1.metric("Valorisation", format_number(focus_row.get("valuation_latest")))
            f2.metric("Funding total", format_number(focus_row.get("total_funding")))
            f3.metric("Dernier round", format_number(focus_row.get("latest_round_amount")))
            f4.metric("Effectifs", format_number(focus_row.get("employees_latest")))
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Valorisation moy.", format_number(merged["valuation_latest"].dropna().mean()))
        b2.metric("Funding moyen", format_number(merged["total_funding"].dropna().mean()))
        b3.metric("Croissance effectifs moy.", format_percent(metric_value(merged, "employee_growth_6m_pct")))
        b4.metric("Confiance données", metric_value(merged, "data_confidence"))
        readable = add_readable_columns(merged, ["valuation_latest", "total_funding", "latest_round_amount", "revenue_latest"], ["employee_growth_6m_pct", "revenue_growth_yoy_pct"])
        display_cols = ["name", "sector", "total_score", "risk_score", "valuation_latest_readable", "valuation_date", "total_funding_readable", "latest_round_amount_readable", "employees_latest", "employee_growth_6m_pct_readable", "revenue_latest_readable", "revenue_growth_yoy_pct_readable", "data_confidence", "notes"]
        st.dataframe(readable[safe_columns(readable, display_cols)], use_container_width=True)
        st.caption("Les colonnes financières sont affichées en k / M / Mrd pour faciliter la lecture.")

with tabs[4]:
    st.subheader("Scénarios prévisionnels")
    st.caption("Scénarios, pas prédictions certaines ni conseils financiers.")
    selected_view = st.radio("Vue", ["Court terme 1/2/3/6 mois", "Complet 1 à 60 mois"], horizontal=True)
    active_forecast = forecast_short_df if selected_view.startswith("Court") else forecast_df
    if active_forecast.empty:
        st.warning("Aucun forecast généré. Lance `python src/forecasting.py` puis `python src/load_to_db.py`.")
    else:
        focus = active_forecast[active_forecast["name"] == selected_startup]
        if not focus.empty:
            focus_readable = add_readable_columns(focus, ["current_value", "forecast_value"])
            cols = ["horizon_months", "scenario_label", "metric_name", "current_value_readable", "forecast_value_readable", "implied_cagr_pct", "probability_pct", "confidence_score", "assumptions"]
            st.dataframe(focus_readable[safe_columns(focus_readable, cols)], use_container_width=True)
            pivot = focus.pivot_table(index="horizon_months", columns="scenario_label", values="forecast_value", aggfunc="mean")
            if not pivot.empty:
                st.line_chart(pivot / 1_000_000_000)
                st.caption("Axe en milliards. Exemple : 13 = 13 Mrd.")
        else:
            st.info("Aucun forecast pour la startup sélectionnée.")

with tabs[5]:
    st.subheader("Financial Timeline")
    st.caption("Levées de fonds, valorisations, événements majeurs et scénarios futurs.")
    if financial_events_df.empty:
        st.warning("Aucune timeline disponible. Renseigne data/seeds/financial_events_seed.csv.")
    else:
        events = financial_events_df[financial_events_df["name"] == selected_startup].copy()
        if events.empty:
            st.info("Aucun événement financier pour la startup sélectionnée.")
        else:
            events["event_date"] = pd.to_datetime(events["event_date"])
            events = events.sort_values("event_date")
            readable_events = add_readable_columns(events, ["amount", "valuation", "share_price"])
            display_cols = ["event_date", "event_type", "event_title", "amount_readable", "valuation_readable", "currency", "share_price_readable", "ticker", "exchange_name", "confidence_score", "description"]
            st.dataframe(readable_events[safe_columns(readable_events, display_cols)], use_container_width=True)
            funding = events.dropna(subset=["amount"])[["event_date", "amount"]].set_index("event_date")
            valuation = events.dropna(subset=["valuation"])[["event_date", "valuation"]].set_index("event_date")
            if not funding.empty:
                st.markdown("### Levées de fonds")
                st.bar_chart(funding / 1_000_000_000)
            if not valuation.empty:
                st.markdown("### Évolution de la valorisation")
                st.line_chart(valuation / 1_000_000_000)

with tabs[6]:
    render_stage_opportunities_view(growth_stage_df, stage_opportunities_df, selected_company=selected_startup)

with tabs[7]:
    render_ipo_and_share_view(ipo_events_df, public_market_df, selected_company=selected_startup)

with tabs[8]:
    render_product_and_events_view(product_mapping_df, upcoming_events_df, selected_company=selected_startup)

with tabs[9]:
    st.subheader("Physical AI / Robotics")
    robotics = filtered[filtered["sector"].str.contains("Physical AI", na=False)]
    if robotics.empty:
        st.info("Aucune startup Physical AI dans le filtre actuel.")
    else:
        display_score_metrics(robotics)
        st.dataframe(robotics[safe_columns(robotics, ["name", "country", "sub_sector", "stage", "total_score", "technical_moat_score", "risk_score", "kamel_edge_score", "decision"])], use_container_width=True)
        robot_chart = robotics[["name", "total_score", "risk_score", "technical_moat_score"]].dropna().set_index("name")
        if not robot_chart.empty:
            st.scatter_chart(robot_chart, x="risk_score", y="total_score", size="technical_moat_score")

with tabs[10]:
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
        detail_benchmark = benchmark_df[benchmark_df["name"] == selected_startup] if not benchmark_df.empty else pd.DataFrame()
        if not detail_benchmark.empty:
            bmk = detail_benchmark.iloc[0]
            st.markdown("### Chiffres clés")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Valorisation", format_number(bmk.get("valuation_latest")))
            k2.metric("Funding total", format_number(bmk.get("total_funding")))
            k3.metric("Dernier round", format_number(bmk.get("latest_round_amount")))
            k4.metric("Effectifs", format_number(bmk.get("employees_latest")))
        related_stage = growth_stage_df[growth_stage_df.get("company_name", pd.Series(dtype=str)) == selected_startup] if not growth_stage_df.empty else pd.DataFrame()
        if not related_stage.empty:
            st.markdown("### Stage de croissance estimé")
            cols = ["company_name", "current_stage", "next_likely_stage", "next_stage_horizon", "stage_confidence_score", "refreshed_at"]
            st.dataframe(related_stage[safe_columns(related_stage, cols)], use_container_width=True)
        related_tools = ai_tools_taxonomy_df[ai_tools_taxonomy_df.get("company_name", pd.Series(dtype=str)) == selected_startup] if not ai_tools_taxonomy_df.empty else pd.DataFrame()
        if not related_tools.empty:
            st.markdown("### Outils / produits IA associés")
            cols = ["company_name", "tool_or_group", "category", "role", "investment_relevance", "radar_priority", "notes"]
            st.dataframe(related_tools[safe_columns(related_tools, cols)], use_container_width=True)
        related_products = product_mapping_df[product_mapping_df.get("company_name", pd.Series(dtype=str)) == selected_startup] if not product_mapping_df.empty else pd.DataFrame()
        if not related_products.empty:
            st.markdown("### Produits phares associés")
            cols = ["company_name", "public_name", "flagship_product", "product_category", "ticker", "exchange_name", "status", "notes"]
            st.dataframe(related_products[safe_columns(related_products, cols)], use_container_width=True)
        st.markdown("**Site / source :**")
        st.write(row.get("website", ""))
        st.write(row.get("source_url", ""))

st.warning("Ce MVP produit des scores, scénarios et benchmarks de veille. Il ne constitue pas un conseil en investissement financier personnalisé.")
