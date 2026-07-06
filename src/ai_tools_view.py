from __future__ import annotations

import pandas as pd
import streamlit as st


PRIORITY_ORDER = ["High", "Medium", "Low"]


WORKFLOW_STEPS = [
    ("1. Idée / stratégie", ["ChatGPT", "Claude", "Gemini", "Perplexity", "Grok"]),
    ("2. Recherche", ["Perplexity", "ChatGPT Search", "Gemini / AI Mode Google", "Genspark", "You.com"]),
    ("3. Synthèse documents", ["NotebookLM", "Claude", "ChatGPT", "Notion AI", "Glean"]),
    ("4. Code / agents dev", ["Cursor", "Claude Code", "OpenAI Codex", "GitHub Copilot", "Windsurf", "GLM-5.2"]),
    ("5. App builders", ["Lovable", "Bolt.new", "Replit Agent", "v0", "Base44"]),
    ("6. Déploiement / frontend", ["Replit Agent", "Vercel", "v0", "Bolt.new"]),
    ("7. Automatisation", ["n8n AI", "Zapier AI", "Make AI", "LangGraph", "AutoGen", "CrewAI"]),
    ("8. Design / image", ["Canva AI", "Ideogram", "DALL-E", "Midjourney", "Adobe Firefly"]),
    ("9. Vidéo / démo", ["Sora", "Google Veo", "Runway", "Kling AI", "Luma Dream Machine", "CapCut AI"]),
    ("10. Audio / voix", ["ElevenLabs", "Suno", "Udio", "Descript", "HeyGen"]),
    ("11. Présentation / vente", ["Gamma", "Canva AI", "ChatGPT", "Claude", "Microsoft 365 Copilot"]),
    ("12. Monitoring / routage", ["OpenRouter", "Glean", "Microsoft Copilot Studio", "Claude MCP / Connectors"]),
]


CORE_VIBE_CODING_KEYWORDS = [
    "Cursor", "Claude Code", "OpenAI Codex", "GitHub Copilot", "Windsurf",
    "Replit Agent", "Lovable", "Bolt.new", "v0", "Base44", "Devin", "GLM-5.2", "ZCode"
]


def _safe_cols(df: pd.DataFrame, cols: list[str]) -> list[str]:
    return [col for col in cols if col in df.columns]


def _priority_rank(value: str) -> int:
    try:
        return PRIORITY_ORDER.index(str(value))
    except ValueError:
        return len(PRIORITY_ORDER)


def _contains_any(value: str, keywords: list[str]) -> bool:
    text = str(value).lower()
    return any(keyword.lower() in text for keyword in keywords)


def _filter_tools(tools_df: pd.DataFrame) -> pd.DataFrame:
    filtered = tools_df.copy()

    with st.expander("Filtres Market Map", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            categories = sorted(filtered.get("category", pd.Series(dtype=str)).dropna().unique().tolist())
            selected_categories = st.multiselect("Catégories", categories, default=categories)
        with c2:
            priorities = sorted(filtered.get("radar_priority", pd.Series(dtype=str)).dropna().unique().tolist(), key=_priority_rank)
            selected_priorities = st.multiselect("Priorité radar", priorities, default=priorities)
        with c3:
            relevance = sorted(filtered.get("investment_relevance", pd.Series(dtype=str)).dropna().unique().tolist())
            selected_relevance = st.multiselect("Pertinence investissement", relevance, default=relevance)

    if "category" in filtered.columns and selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]
    if "radar_priority" in filtered.columns and selected_priorities:
        filtered = filtered[filtered["radar_priority"].isin(selected_priorities)]
    if "investment_relevance" in filtered.columns and selected_relevance:
        filtered = filtered[filtered["investment_relevance"].isin(selected_relevance)]

    return filtered


def _render_market_map(filtered: pd.DataFrame) -> None:
    st.markdown("### Market Map par catégorie")
    if filtered.empty:
        st.warning("Aucun outil ne correspond aux filtres.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Outils", len(filtered))
    c2.metric("Catégories", filtered["category"].nunique() if "category" in filtered else 0)
    c3.metric("High priority", int((filtered.get("radar_priority") == "High").sum()) if "radar_priority" in filtered else 0)
    c4.metric("Core code/dev", int(filtered.get("category", pd.Series(dtype=str)).str.contains("Code", na=False).sum()) if "category" in filtered else 0)

    if "category" in filtered.columns:
        st.markdown("#### Nombre d'outils par catégorie")
        st.bar_chart(filtered["category"].value_counts())

    display_cols = [
        "category", "tool_or_group", "company_or_owner", "role",
        "investment_relevance", "radar_priority", "notes",
    ]
    st.dataframe(filtered[_safe_cols(filtered, display_cols)], use_container_width=True)

    st.markdown("#### Cartes par catégorie")
    for category, group in filtered.groupby("category"):
        with st.expander(f"{category} — {len(group)} outils", expanded=False):
            cols = ["tool_or_group", "company_or_owner", "role", "investment_relevance", "radar_priority", "notes"]
            st.dataframe(group[_safe_cols(group, cols)], use_container_width=True)


def _render_builder_workflow(tools_df: pd.DataFrame) -> None:
    st.markdown("### Builder Workflow")
    st.caption("Vue opérationnelle : de l'idée au produit vendable, puis automatisé et monitoré.")

    for step, keywords in WORKFLOW_STEPS:
        matches = tools_df[
            tools_df.get("tool_or_group", pd.Series(dtype=str)).apply(lambda x: _contains_any(x, keywords))
            | tools_df.get("role", pd.Series(dtype=str)).apply(lambda x: _contains_any(x, keywords))
        ].copy()
        with st.expander(step, expanded=step.startswith("4") or step.startswith("5") or step.startswith("7")):
            st.markdown("**Outils cibles :** " + ", ".join(keywords))
            if matches.empty:
                st.info("Aucune ligne directement associée dans le CSV pour cette étape.")
            else:
                cols = ["tool_or_group", "company_or_owner", "category", "role", "investment_relevance", "radar_priority"]
                st.dataframe(matches[_safe_cols(matches, cols)].drop_duplicates(), use_container_width=True)


def _render_vibe_coding_core(tools_df: pd.DataFrame, top20_df: pd.DataFrame) -> None:
    st.markdown("### Vibe Coding Core")
    st.caption("Focus sur les outils qui construisent réellement du logiciel, des apps, des PR ou des workflows dev.")

    core = tools_df[
        tools_df.get("tool_or_group", pd.Series(dtype=str)).apply(lambda x: _contains_any(x, CORE_VIBE_CODING_KEYWORDS))
        | tools_df.get("role", pd.Series(dtype=str)).apply(lambda x: _contains_any(x, CORE_VIBE_CODING_KEYWORDS))
        | tools_df.get("category", pd.Series(dtype=str)).str.contains("Code", na=False)
    ].copy()

    if core.empty:
        st.warning("Aucun outil core Vibe Coding trouvé.")
    else:
        cols = ["tool_or_group", "company_or_owner", "role", "investment_relevance", "radar_priority", "notes"]
        st.dataframe(core[_safe_cols(core, cols)], use_container_width=True)
        if "radar_priority" in core.columns:
            st.markdown("#### Priorité radar — Vibe Coding")
            st.bar_chart(core["radar_priority"].value_counts())

    if not top20_df.empty:
        st.markdown("### Top 20 July 2026 — version courte")
        cols = ["rank", "tool_or_group", "company_or_owner", "primary_role", "category", "investable_entity", "status", "radar_action"]
        st.dataframe(top20_df[_safe_cols(top20_df, cols)], use_container_width=True)


def _render_investability(tools_df: pd.DataFrame) -> None:
    st.markdown("### Investability Matrix")
    st.caption("Produit connu ≠ société investissable. Cette vue sépare plateformes cotées, privées, risques stratégiques et utilities.")

    if tools_df.empty:
        st.warning("Aucune donnée disponible.")
        return

    matrix_cols = ["tool_or_group", "company_or_owner", "category", "investment_relevance", "radar_priority", "notes"]
    public_like = tools_df[tools_df.get("investment_relevance", pd.Series(dtype=str)).str.contains("Public", case=False, na=False)]
    private_like = tools_df[tools_df.get("investment_relevance", pd.Series(dtype=str)).str.contains("Private", case=False, na=False)]
    strategic_like = tools_df[tools_df.get("investment_relevance", pd.Series(dtype=str)).str.contains("Strategic", case=False, na=False)]
    utility_like = tools_df[tools_df.get("investment_relevance", pd.Series(dtype=str)).str.contains("utility|Workflow|automation", case=False, na=False)]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Public comparables", len(public_like))
    c2.metric("Private / startups", len(private_like))
    c3.metric("Strategic platforms", len(strategic_like))
    c4.metric("Workflow utilities", len(utility_like))

    buckets = [
        ("Public comparables", public_like),
        ("Private / startups", private_like),
        ("Strategic platform risk", strategic_like),
        ("Workflow utilities", utility_like),
    ]
    for title, frame in buckets:
        with st.expander(title, expanded=title.startswith("Public") or title.startswith("Private")):
            if frame.empty:
                st.info("Aucune ligne.")
            else:
                st.dataframe(frame[_safe_cols(frame, matrix_cols)], use_container_width=True)


def _render_tool_detail(tools_df: pd.DataFrame, top20_df: pd.DataFrame) -> None:
    st.markdown("### Tool Detail")
    all_tools = sorted(tools_df.get("tool_or_group", pd.Series(dtype=str)).dropna().unique().tolist())
    if not all_tools:
        st.warning("Aucun outil disponible.")
        return

    selected = st.selectbox("Outil / groupe", all_tools, key="ai_tool_detail_select")
    row = tools_df[tools_df["tool_or_group"] == selected].iloc[0]

    st.markdown(f"## {selected}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Catégorie", str(row.get("category", ""))[:30])
    c2.metric("Priorité", str(row.get("radar_priority", "")))
    c3.metric("Société", str(row.get("company_or_owner", ""))[:30])

    st.markdown("**Rôle :** " + str(row.get("role", "")))
    st.markdown("**Pertinence investissement :** " + str(row.get("investment_relevance", "")))
    st.markdown("**Notes :** " + str(row.get("notes", "")))

    match_top = top20_df[top20_df.get("tool_or_group", pd.Series(dtype=str)) == selected] if not top20_df.empty else pd.DataFrame()
    if not match_top.empty:
        st.markdown("### Vue Top 20")
        cols = ["rank", "primary_role", "category", "investable_entity", "status", "why_it_matters", "radar_action"]
        st.dataframe(match_top[_safe_cols(match_top, cols)], use_container_width=True)


def render_ai_tools_stack_view(tools_df: pd.DataFrame, top20_df: pd.DataFrame) -> None:
    st.subheader("AI Tools Stack / Market Map — July 2026")
    st.caption("Taxonomie IA : Vibe Coding, agents, recherche, productivité, créatif, vidéo, audio et automation.")

    if tools_df.empty and top20_df.empty:
        st.warning("Aucune donnée disponible. Renseigne ai_tools_trending_by_category_july2026.csv et vibe_coding_top20_july2026.csv.")
        return

    active_df = tools_df.copy() if not tools_df.empty else pd.DataFrame()
    filtered = _filter_tools(active_df) if not active_df.empty else active_df

    sub_tabs = st.tabs([
        "Market Map", "Builder Workflow", "Vibe Coding Core",
        "Investability", "Tool Detail"
    ])

    with sub_tabs[0]:
        _render_market_map(filtered)
    with sub_tabs[1]:
        _render_builder_workflow(active_df)
    with sub_tabs[2]:
        _render_vibe_coding_core(active_df, top20_df)
    with sub_tabs[3]:
        _render_investability(active_df)
    with sub_tabs[4]:
        _render_tool_detail(active_df, top20_df)

    st.info("Lecture recommandée : sépare toujours produit visible, société propriétaire, statut investissable, comparable coté et rôle réel dans la chaîne builder.")
