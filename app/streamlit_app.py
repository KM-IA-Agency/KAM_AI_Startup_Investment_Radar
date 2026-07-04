from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.scoring import score_dataframe

DATA_PATH = ROOT / "data" / "seeds" / "startups_seed.csv"

st.set_page_config(page_title="KAM AI Startup Radar", layout="wide")

st.title("KAM AI Startup Investment Radar")
st.caption("MVP de veille, scoring et watchlist startup IA / Deeptech")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return score_dataframe(df)

try:
    df = load_data()
except Exception as exc:
    st.error(f"Impossible de charger le dataset: {exc}")
    st.stop()

with st.sidebar:
    st.header("Filtres")
    countries = sorted(df["country"].dropna().unique().tolist())
    sectors = sorted(df["sector"].dropna().unique().tolist())
    decisions = sorted(df["decision"].dropna().unique().tolist())

    selected_countries = st.multiselect("Pays", countries, default=countries)
    selected_sectors = st.multiselect("Secteurs", sectors, default=sectors)
    selected_decisions = st.multiselect("Décisions", decisions, default=decisions)
    min_score = st.slider("Score minimum", 0, 100, 0)

filtered = df[
    df["country"].isin(selected_countries)
    & df["sector"].isin(selected_sectors)
    & df["decision"].isin(selected_decisions)
    & (df["total_score"] >= min_score)
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Startups", len(filtered))
col2.metric("Score moyen", round(filtered["total_score"].mean(), 1) if len(filtered) else 0)
col3.metric("Top score", int(filtered["total_score"].max()) if len(filtered) else 0)
col4.metric("Investigation+", int(filtered[filtered["decision"].isin(["Priority investigation", "Investable potential"])].shape[0]))

st.subheader("Top 10 Watchlist")
top10 = filtered.head(10)
st.dataframe(
    top10[[
        "name",
        "country",
        "sector",
        "sub_sector",
        "stage",
        "total_score",
        "kamel_edge_score",
        "decision",
        "score_explanation",
    ]],
    use_container_width=True,
)

st.subheader("Toutes les startups filtrées")
st.dataframe(
    filtered[[
        "name",
        "country",
        "region",
        "sector",
        "sub_sector",
        "stage",
        "total_score",
        "kamel_edge_score",
        "decision",
        "website",
    ]],
    use_container_width=True,
)

st.subheader("Fiche startup")
startup_name = st.selectbox("Choisir une startup", filtered["name"].tolist() if len(filtered) else [])
if startup_name:
    row = filtered[filtered["name"] == startup_name].iloc[0]
    st.markdown(f"### {row['name']}")
    st.write(row.get("description", ""))
    a, b, c = st.columns(3)
    a.metric("Score total", int(row["total_score"]))
    b.metric("Kamel Edge", int(row["kamel_edge_score"]))
    c.metric("Risque", int(row["risk_score"]))
    st.markdown("**Décision :** " + row["decision"])
    st.markdown("**Explication :** " + row["score_explanation"])
    st.markdown("**Site / source :**")
    st.write(row.get("website", ""))
    st.write(row.get("source_url", ""))

st.warning("Ce MVP produit des scores de veille et de priorisation. Il ne constitue pas un conseil en investissement financier personnalisé.")
