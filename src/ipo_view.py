from __future__ import annotations

import pandas as pd
import streamlit as st

from src.formatting import add_readable_columns, format_number


def render_ipo_and_share_view(
    ipo_df: pd.DataFrame,
    market_df: pd.DataFrame,
    selected_company: str | None = None,
) -> None:
    st.subheader("IPO & Actions")
    st.caption("Introduction en bourse, prix IPO, cours après IPO, évolution du cours et capitalisation si disponible.")

    if ipo_df.empty and market_df.empty:
        st.warning("Aucune donnée IPO/action disponible. Renseigne data/seeds/ipo_events_seed.csv et data/seeds/public_market_observations_seed.csv.")
        return

    available_names = sorted(
        set(ipo_df.get("name", pd.Series(dtype=str)).dropna().tolist())
        | set(market_df.get("name", pd.Series(dtype=str)).dropna().tolist())
    )
    if not available_names:
        st.warning("Aucune société cotée / comparable public disponible.")
        return

    default_index = available_names.index(selected_company) if selected_company in available_names else 0
    selected_public = st.selectbox(
        "Société cotée / comparable public",
        available_names,
        index=default_index,
        key="ipo_public_company",
    )
    if selected_company and selected_company in available_names:
        st.caption(f"Filtre initial propagé depuis Startup focus : {selected_company}")

    ipo = ipo_df[ipo_df["name"] == selected_public].copy() if not ipo_df.empty else pd.DataFrame()
    market = market_df[market_df["name"] == selected_public].copy() if not market_df.empty else pd.DataFrame()

    if not ipo.empty:
        row = ipo.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Prix IPO", format_number(row.get("ipo_price")))
        c2.metric("Clôture J1", format_number(row.get("first_day_close")))
        c3.metric("Dernier cours", format_number(row.get("latest_share_price")))
        c4.metric("Market cap latest", format_number(row.get("market_cap_latest")))

        readable_ipo = add_readable_columns(
            ipo,
            money_columns=["ipo_price", "first_day_close", "latest_share_price", "market_cap_latest"],
        )
        cols = [
            "name", "ipo_date", "ticker", "exchange_name", "ipo_price_readable",
            "first_day_close_readable", "latest_share_price_readable",
            "market_cap_latest_readable", "currency", "confidence_score", "description",
        ]
        st.markdown("### Données IPO")
        st.dataframe(readable_ipo[[col for col in cols if col in readable_ipo.columns]], use_container_width=True)

    if not market.empty:
        market["observed_at"] = pd.to_datetime(market["observed_at"])
        market = market.sort_values("observed_at")
        readable_market = add_readable_columns(market, money_columns=["share_price", "market_cap", "enterprise_value"])
        cols = [
            "observed_at", "name", "ticker", "exchange_name", "share_price_readable",
            "market_cap_readable", "enterprise_value_readable", "currency", "confidence_score", "source",
        ]
        st.markdown("### Observations de marché")
        st.dataframe(readable_market[[col for col in cols if col in readable_market.columns]], use_container_width=True)

        price = market.dropna(subset=["share_price"])[["observed_at", "share_price"]].set_index("observed_at")
        if not price.empty:
            st.markdown("### Évolution du cours de l'action")
            st.line_chart(price)

        cap = market.dropna(subset=["market_cap"])[["observed_at", "market_cap"]].set_index("observed_at")
        if not cap.empty:
            st.markdown("### Évolution de la capitalisation")
            st.line_chart(cap / 1_000_000_000)
            st.caption("Axe en milliards.")

    st.info("Les données seed sont des placeholders de structure. Les cours, market cap et prix IPO doivent être remplacés par des données vérifiées et datées.")
