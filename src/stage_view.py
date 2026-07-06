from __future__ import annotations

import pandas as pd
import streamlit as st

from src.formatting import add_readable_columns, format_number


def _safe_cols(df: pd.DataFrame, cols: list[str]) -> list[str]:
    return [col for col in cols if col in df.columns]


def render_stage_opportunities_view(
    stage_df: pd.DataFrame,
    opportunities_df: pd.DataFrame,
    selected_company: str | None = None,
) -> None:
    st.subheader("Growth Stage & Opportunités")
    st.caption("Stade actuel, prochain stade probable, signaux à surveiller et opportunités court terme.")

    if stage_df.empty and opportunities_df.empty:
        st.warning("Aucune donnée stage/opportunité disponible. Lance `python src/run_market_refresh.py`.")
        return

    companies = sorted(
        set(stage_df.get("company_name", pd.Series(dtype=str)).dropna().tolist())
        | set(opportunities_df.get("company_name", pd.Series(dtype=str)).dropna().tolist())
    )
    if not companies:
        st.warning("Aucune société disponible dans les tables de stage.")
        return

    default_index = companies.index(selected_company) if selected_company in companies else 0
    selected = st.selectbox("Société / startup", companies, index=default_index, key="stage_company_select")
    if selected_company and selected_company in companies:
        st.caption(f"Filtre initial propagé depuis Startup focus : {selected_company}")

    focus_stage = stage_df[stage_df["company_name"] == selected].copy() if not stage_df.empty else pd.DataFrame()
    focus_opp = opportunities_df[opportunities_df["company_name"] == selected].copy() if not opportunities_df.empty else pd.DataFrame()

    if not focus_stage.empty:
        latest = focus_stage.sort_values("refreshed_at", ascending=False).iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Stage actuel", str(latest.get("current_stage", "")))
        c2.metric("Prochain stade", str(latest.get("next_likely_stage", ""))[:30])
        c3.metric("Horizon", str(latest.get("next_stage_horizon", "")))
        c4.metric("Confiance", int(latest.get("stage_confidence_score", 0) or 0))

        readable_stage = add_readable_columns(
            focus_stage,
            money_columns=["last_round_amount", "last_known_valuation"],
        )
        cols = [
            "company_name", "current_stage", "stage_basis", "last_known_round", "last_round_date",
            "last_round_amount_readable", "last_known_valuation_readable", "currency",
            "estimated_revenue_band", "estimated_headcount_band", "next_likely_stage",
            "next_stage_horizon", "stage_confidence_score", "refreshed_at",
        ]
        st.markdown("### Snapshot de maturité")
        st.dataframe(readable_stage[_safe_cols(readable_stage, cols)], use_container_width=True)

    if not focus_opp.empty:
        st.markdown("### Opportunités liées aux prochaines étapes")
        focus_opp = focus_opp.sort_values(
            ["opportunity_window", "expected_impact_score", "probability_pct"],
            ascending=[True, False, False],
        )
        cols = [
            "company_name", "current_stage", "next_likely_stage", "opportunity_type",
            "opportunity_window", "opportunity_title", "probability_pct",
            "expected_impact_score", "access_difficulty_score", "investor_action",
            "watch_signals", "confidence_score", "refreshed_at",
        ]
        st.dataframe(focus_opp[_safe_cols(focus_opp, cols)], use_container_width=True)

        impact = focus_opp[["opportunity_type", "probability_pct", "expected_impact_score"]].copy()
        if not impact.empty:
            impact["weighted_impact"] = impact["probability_pct"] * impact["expected_impact_score"] / 100
            chart = impact.groupby("opportunity_type")["weighted_impact"].sum().sort_values(ascending=False)
            st.markdown("### Impact pondéré par type d'opportunité")
            st.bar_chart(chart)

    st.markdown("### Vue portefeuille par stage")
    if not stage_df.empty:
        latest_portfolio = stage_df.sort_values("refreshed_at", ascending=False).drop_duplicates("company_name")
        stage_counts = latest_portfolio["current_stage"].value_counts()
        st.bar_chart(stage_counts)
        portfolio_cols = [
            "company_name", "current_stage", "next_likely_stage", "next_stage_horizon",
            "stage_confidence_score", "last_known_round", "last_round_date", "refreshed_at",
        ]
        st.dataframe(latest_portfolio[_safe_cols(latest_portfolio, portfolio_cols)], use_container_width=True)

    st.info("Les stages et opportunités sont des estimations de veille. Ils doivent être confirmés par des sources datées : levées de fonds, filings IPO, communiqués, données financières, traction produit et signaux marché.")
