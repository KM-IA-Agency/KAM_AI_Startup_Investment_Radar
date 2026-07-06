from __future__ import annotations

import pandas as pd
import streamlit as st


def _safe_cols(df: pd.DataFrame, cols: list[str]) -> list[str]:
    return [col for col in cols if col in df.columns]


def _add_company_product_label(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    if frame.empty:
        return frame
    if "company_product_label" not in frame.columns:
        company = frame.get("company_name", pd.Series("", index=frame.index)).fillna("").astype(str)
        product = frame.get("flagship_product", frame.get("product_or_segment", pd.Series("", index=frame.index))).fillna("").astype(str)
        frame["company_product_label"] = company + " → " + product
    return frame


def render_product_and_events_view(
    mapping_df: pd.DataFrame,
    upcoming_df: pd.DataFrame,
    selected_company: str | None = None,
) -> None:
    st.subheader("Produits phares & événements probables")
    st.caption("Lien société cotée / startup privée / produit phare, puis prochains événements à surveiller.")

    if mapping_df.empty and upcoming_df.empty:
        st.warning("Aucune donnée disponible. Renseigne company_product_mapping_seed.csv et upcoming_events_seed.csv.")
        return

    mapping_df = _add_company_product_label(mapping_df)
    upcoming_df = _add_company_product_label(upcoming_df)

    names = sorted(
        set(mapping_df.get("company_name", pd.Series(dtype=str)).dropna().tolist())
        | set(upcoming_df.get("company_name", pd.Series(dtype=str)).dropna().tolist())
    )
    if not names:
        st.warning("Aucune société / startup disponible dans les mappings produits ou événements.")
        return

    default_index = names.index(selected_company) if selected_company in names else 0
    selected = st.selectbox("Société / startup", names, index=default_index, key="product_event_company")
    if selected_company and selected_company in names:
        st.caption(f"Filtre initial propagé depuis Startup focus : {selected_company}")

    mapping = mapping_df[mapping_df["company_name"] == selected].copy() if not mapping_df.empty else pd.DataFrame()
    events = upcoming_df[upcoming_df["company_name"] == selected].copy() if not upcoming_df.empty else pd.DataFrame()

    if not mapping.empty:
        st.markdown("### Correspondance société ↔ produit phare")
        cols = [
            "company_product_label", "company_name", "public_name", "flagship_product", "product_category",
            "related_startup_or_segment", "ticker", "exchange_name", "status", "notes",
        ]
        st.dataframe(mapping[_safe_cols(mapping, cols)], use_container_width=True)

    if not events.empty:
        st.markdown("### Prochains événements probables")
        events = events.sort_values(["event_window", "impact_score", "probability_pct"], ascending=[True, False, False])
        cols = [
            "company_product_label", "company_name", "product_or_segment", "event_window", "event_type",
            "event_title", "probability_pct", "impact_score", "confidence_score", "expected_effect",
            "watch_signals", "notes",
        ]
        st.dataframe(events[_safe_cols(events, cols)], use_container_width=True)

        impact = events[["event_type", "probability_pct", "impact_score"]].copy()
        if not impact.empty:
            impact["weighted_impact"] = impact["probability_pct"] * impact["impact_score"] / 100
            chart = impact.groupby("event_type")["weighted_impact"].sum().sort_values(ascending=False)
            st.markdown("### Impact probable pondéré par type d'événement")
            st.bar_chart(chart)

    st.info("Ces événements sont des hypothèses de veille. Ils doivent être remplacés ou confirmés par des signaux réels : communiqués, S-1/IPO filings, earnings, annonces produit, tours de table, partenariats.")
