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

RECENT_SIGNAL_KEYWORDS = [
    "GLM-5.2", "ZCode", "Cursor", "Claude Code", "Codex", "Lovable",
    "Windsurf", "Replit Agent", "Bolt.new", "OpenRouter", "LangGraph", "n8n"
]


INVESTABILITY_RULES = [
    ("Public", 90),
    ("Public comparable", 85),
    ("Public/strategic", 75),
    ("Strategic platform", 55),
    ("Private AI coding", 45),
    ("Private agents", 45),
    ("Private automation", 45),
    ("Private", 40),
    ("Mixed", 35),
    ("Open-source", 25),
    ("Workflow", 20),
]


def _safe_cols(df: pd.DataFrame, cols: list[str]) -> list[str]:
    return [col for col in cols if col in df.columns]


def _normalize_company_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    if frame.empty:
        return frame
    if "company_name" not in frame.columns and "company_or_owner" in frame.columns:
        frame["company_name"] = frame["company_or_owner"]
    if "company_or_owner" not in frame.columns and "company_name" in frame.columns:
        frame["company_or_owner"] = frame["company_name"]
    if "company_product_label" not in frame.columns:
        company = frame.get("company_name", pd.Series("", index=frame.index)).fillna("").astype(str)
        tool = frame.get("tool_or_group", pd.Series("", index=frame.index)).fillna("").astype(str)
        frame["company_product_label"] = company + " → " + tool
    return frame


def _priority_rank(value: str) -> int:
    try:
        return PRIORITY_ORDER.index(str(value))
    except ValueError:
        return len(PRIORITY_ORDER)


def _contains_any(value: str, keywords: list[str]) -> bool:
    text = str(value).lower()
    return any(keyword.lower() in text for keyword in keywords)


def _score_impact(row: pd.Series) -> int:
    text = " ".join(str(row.get(col, "")) for col in ["tool_or_group", "company_name", "category", "role", "notes"])
    priority = str(row.get("radar_priority", ""))
    relevance = str(row.get("investment_relevance", ""))

    score = 50
    if priority == "High":
        score += 25
    elif priority == "Medium":
        score += 12
    elif priority == "Low":
        score += 3

    if _contains_any(text, CORE_VIBE_CODING_KEYWORDS):
        score += 15
    if _contains_any(text, RECENT_SIGNAL_KEYWORDS):
        score += 10
    if any(keyword in relevance.lower() for keyword in ["strategic", "public", "private ai coding", "automation"]):
        score += 8
    if any(keyword in str(row.get("category", "")).lower() for keyword in ["code", "agents", "automatisation"]):
        score += 8

    return min(score, 100)


def _score_investability(row: pd.Series) -> int:
    relevance = str(row.get("investment_relevance", ""))
    text = " ".join(str(row.get(col, "")) for col in ["tool_or_group", "company_name", "company_or_owner", "category", "notes"])

    score = 30
    for keyword, value in INVESTABILITY_RULES:
        if keyword.lower() in relevance.lower():
            score = max(score, value)

    if _contains_any(text, ["Microsoft", "Alphabet", "Adobe", "Z.ai", "Kuaishou", "Wix"]):
        score = max(score, 75)
    if _contains_any(text, ["OpenAI", "Anthropic", "xAI"]):
        score = min(score, 55)
    if "workflow utility" in relevance.lower():
        score = min(score, 45)

    return min(score, 100)


def _add_matrix_scores(tools_df: pd.DataFrame) -> pd.DataFrame:
    frame = _normalize_company_columns(tools_df)
    if frame.empty:
        return frame
    frame["strategic_impact_score"] = frame.apply(_score_impact, axis=1)
    frame["investability_score"] = frame.apply(_score_investability, axis=1)
    frame["priority_score"] = frame["radar_priority"].map({"High": 3, "Medium": 2, "Low": 1}).fillna(1)
    frame["top10_score"] = (
        frame["strategic_impact_score"] * 0.55
        + frame["investability_score"] * 0.25
        + frame["priority_score"] * 8
    )
    frame["quadrant"] = frame.apply(_quadrant_label, axis=1)
    return frame


def _quadrant_label(row: pd.Series) -> str:
    impact = row.get("strategic_impact_score", 0)
    investability = row.get("investability_score", 0)
    if impact >= 75 and investability >= 65:
        return "High impact / Investable"
    if impact >= 75 and investability < 65:
        return "High impact / Hard to access"
    if impact < 75 and investability >= 65:
        return "Investable comparable"
    return "Workflow / Watchlist"


def _filter_tools(tools_df: pd.DataFrame, selected_company: str | None = None) -> pd.DataFrame:
    filtered = _normalize_company_columns(tools_df)

    focus_available = bool(
        selected_company
        and "company_name" in filtered.columns
        and selected_company in filtered["company_name"].dropna().unique().tolist()
    )

    with st.expander("Filtres Market Map", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            apply_focus = st.checkbox(
                "Appliquer Startup focus",
                value=focus_available,
                disabled=not focus_available,
                help="Filtre la Market Map sur la société sélectionnée dans la sidebar quand elle existe dans ai_tools.",
            )
        with c2:
            categories = sorted(filtered.get("category", pd.Series(dtype=str)).dropna().unique().tolist())
            selected_categories = st.multiselect("Catégories", categories, default=categories)
        with c3:
            priorities = sorted(filtered.get("radar_priority", pd.Series(dtype=str)).dropna().unique().tolist(), key=_priority_rank)
            selected_priorities = st.multiselect("Priorité radar", priorities, default=priorities)
        with c4:
            relevance = sorted(filtered.get("investment_relevance", pd.Series(dtype=str)).dropna().unique().tolist())
            selected_relevance = st.multiselect("Pertinence investissement", relevance, default=relevance)

    if focus_available and apply_focus:
        filtered = filtered[filtered["company_name"] == selected_company]
    if "category" in filtered.columns and selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]
    if "radar_priority" in filtered.columns and selected_priorities:
        filtered = filtered[filtered["radar_priority"].isin(selected_priorities)]
    if "investment_relevance" in filtered.columns and selected_relevance:
        filtered = filtered[filtered["investment_relevance"].isin(selected_relevance)]

    return filtered


def _render_market_map(filtered: pd.DataFrame) -> None:
    filtered = _normalize_company_columns(filtered)
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
        "company_product_label", "company_name", "tool_or_group", "category", "role",
        "investment_relevance", "radar_priority", "notes",
    ]
    st.dataframe(filtered[_safe_cols(filtered, display_cols)], use_container_width=True)

    st.markdown("#### Cartes par catégorie")
    for category, group in filtered.groupby("category"):
        with st.expander(f"{category} — {len(group)} outils", expanded=False):
            cols = ["company_product_label", "company_name", "tool_or_group", "role", "investment_relevance", "radar_priority", "notes"]
            st.dataframe(group[_safe_cols(group, cols)], use_container_width=True)


def _render_builder_workflow(tools_df: pd.DataFrame, selected_company: str | None = None) -> None:
    tools_df = _normalize_company_columns(tools_df)
    st.markdown("### Builder Workflow")
    st.caption("Vue opérationnelle : de l'idée au produit vendable, puis automatisé et monitoré.")
    if selected_company and "company_name" in tools_df.columns and selected_company in tools_df["company_name"].dropna().unique().tolist():
        st.caption(f"Startup focus disponible dans cette vue : {selected_company}")

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
                cols = ["company_product_label", "company_name", "tool_or_group", "category", "role", "investment_relevance", "radar_priority"]
                st.dataframe(matches[_safe_cols(matches, cols)].drop_duplicates(), use_container_width=True)


def _render_vibe_coding_core(tools_df: pd.DataFrame, top20_df: pd.DataFrame) -> None:
    tools_df = _normalize_company_columns(tools_df)
    top20_df = _normalize_company_columns(top20_df)
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
        cols = ["company_product_label", "company_name", "tool_or_group", "role", "investment_relevance", "radar_priority", "notes"]
        st.dataframe(core[_safe_cols(core, cols)], use_container_width=True)
        if "radar_priority" in core.columns:
            st.markdown("#### Priorité radar — Vibe Coding")
            st.bar_chart(core["radar_priority"].value_counts())

    if not top20_df.empty:
        st.markdown("### Top 20 July 2026 — version courte")
        cols = ["rank", "company_product_label", "tool_or_group", "company_name", "primary_role", "category", "investable_entity", "status", "radar_action"]
        st.dataframe(top20_df[_safe_cols(top20_df, cols)], use_container_width=True)


def _render_impact_investability_matrix(tools_df: pd.DataFrame) -> None:
    st.markdown("### Impact stratégique × Investissabilité")
    st.caption("Lecture : en haut à droite = impact fort et accès investissement/comparable plus simple. En haut à gauche = stratégique mais difficile d'accès.")

    scored = _add_matrix_scores(tools_df)
    if scored.empty:
        st.warning("Aucune donnée disponible.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("High impact / Investable", int((scored["quadrant"] == "High impact / Investable").sum()))
    c2.metric("High impact / Hard access", int((scored["quadrant"] == "High impact / Hard to access").sum()))
    c3.metric("Investable comparables", int((scored["quadrant"] == "Investable comparable").sum()))
    c4.metric("Workflow / Watchlist", int((scored["quadrant"] == "Workflow / Watchlist").sum()))

    plot_df = scored[["tool_or_group", "strategic_impact_score", "investability_score", "priority_score", "quadrant"]].copy()
    plot_df = plot_df.set_index("tool_or_group")
    st.scatter_chart(plot_df, x="investability_score", y="strategic_impact_score", size="priority_score")

    st.markdown("#### Quadrants")
    display_cols = [
        "company_product_label", "company_name", "tool_or_group", "category", "investment_relevance", "radar_priority",
        "strategic_impact_score", "investability_score", "quadrant", "notes",
    ]
    scored = scored.sort_values(["strategic_impact_score", "investability_score"], ascending=False)
    st.dataframe(scored[_safe_cols(scored, display_cols)], use_container_width=True)

    for quadrant, group in scored.groupby("quadrant"):
        with st.expander(f"{quadrant} — {len(group)}", expanded=quadrant.startswith("High impact")):
            st.dataframe(group[_safe_cols(group, display_cols)].head(25), use_container_width=True)


def _render_monthly_top10(tools_df: pd.DataFrame) -> None:
    st.markdown("### Top 10 du mois — signaux à surveiller")
    st.caption("Classement heuristique basé sur impact stratégique, investissabilité, priorité radar et signaux récents. À valider avec sources réelles.")

    scored = _add_matrix_scores(tools_df)
    if scored.empty:
        st.warning("Aucune donnée disponible.")
        return

    scored["recent_signal_bonus"] = scored.apply(
        lambda row: 1 if _contains_any(
            " ".join(str(row.get(col, "")) for col in ["tool_or_group", "role", "notes"]),
            RECENT_SIGNAL_KEYWORDS,
        ) else 0,
        axis=1,
    )
    scored["top10_score"] = scored["top10_score"] + scored["recent_signal_bonus"] * 12
    top10 = scored.sort_values("top10_score", ascending=False).head(10).copy()
    top10.insert(0, "rank", range(1, len(top10) + 1))

    cols = [
        "rank", "company_product_label", "company_name", "tool_or_group", "category", "role",
        "investment_relevance", "radar_priority", "strategic_impact_score",
        "investability_score", "top10_score", "notes",
    ]
    st.dataframe(top10[_safe_cols(top10, cols)], use_container_width=True)

    st.markdown("#### Pourquoi ces 10 ?")
    for _, row in top10.iterrows():
        st.markdown(
            f"**#{int(row['rank'])} — {row['company_product_label']}**  \n"
            f"Catégorie : `{row.get('category', '')}` · "
            f"Impact : `{int(row.get('strategic_impact_score', 0))}/100` · "
            f"Investissabilité : `{int(row.get('investability_score', 0))}/100`  \n"
            f"Action radar : {row.get('notes', '')}"
        )


def _render_investability(tools_df: pd.DataFrame) -> None:
    tools_df = _normalize_company_columns(tools_df)
    st.markdown("### Investability Matrix")
    st.caption("Produit connu ≠ société investissable. Cette vue sépare plateformes cotées, privées, risques stratégiques et utilities.")

    if tools_df.empty:
        st.warning("Aucune donnée disponible.")
        return

    matrix_cols = ["company_product_label", "company_name", "tool_or_group", "category", "investment_relevance", "radar_priority", "notes"]
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


def _render_tool_detail(tools_df: pd.DataFrame, top20_df: pd.DataFrame, selected_company: str | None = None) -> None:
    st.markdown("### Tool Detail")
    scored = _add_matrix_scores(tools_df)
    all_tools = sorted(scored.get("tool_or_group", pd.Series(dtype=str)).dropna().unique().tolist())
    if not all_tools:
        st.warning("Aucun outil disponible.")
        return

    default_tool = None
    if selected_company and "company_name" in scored.columns:
        focus_tools = scored[scored["company_name"] == selected_company]["tool_or_group"].dropna().tolist()
        if focus_tools:
            default_tool = focus_tools[0]
    default_index = all_tools.index(default_tool) if default_tool in all_tools else 0
    selected = st.selectbox("Outil / groupe", all_tools, index=default_index, key="ai_tool_detail_select")
    row = scored[scored["tool_or_group"] == selected].iloc[0]

    st.markdown(f"## {row.get('company_product_label', selected)}")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Catégorie", str(row.get("category", ""))[:30])
    c2.metric("Priorité", str(row.get("radar_priority", "")))
    c3.metric("Société", str(row.get("company_name", row.get("company_or_owner", "")))[:30])
    c4.metric("Impact", int(row.get("strategic_impact_score", 0)))
    c5.metric("Investissabilité", int(row.get("investability_score", 0)))

    st.markdown("**Quadrant :** " + str(row.get("quadrant", "")))
    st.markdown("**Rôle :** " + str(row.get("role", "")))
    st.markdown("**Pertinence investissement :** " + str(row.get("investment_relevance", "")))
    st.markdown("**Notes :** " + str(row.get("notes", "")))

    top20_df = _normalize_company_columns(top20_df)
    match_top = top20_df[top20_df.get("tool_or_group", pd.Series(dtype=str)) == selected] if not top20_df.empty else pd.DataFrame()
    if not match_top.empty:
        st.markdown("### Vue Top 20")
        cols = ["rank", "company_product_label", "primary_role", "category", "investable_entity", "status", "why_it_matters", "radar_action"]
        st.dataframe(match_top[_safe_cols(match_top, cols)], use_container_width=True)


def render_ai_tools_stack_view(
    tools_df: pd.DataFrame,
    top20_df: pd.DataFrame,
    selected_company: str | None = None,
) -> None:
    st.subheader("AI Tools Stack / Market Map — July 2026")
    st.caption("Taxonomie IA : Vibe Coding, agents, recherche, productivité, créatif, vidéo, audio et automation.")

    if tools_df.empty and top20_df.empty:
        st.warning("Aucune donnée disponible. Renseigne ai_tools_trending_by_category_july2026.csv et vibe_coding_top20_july2026.csv.")
        return

    active_df = _normalize_company_columns(tools_df.copy()) if not tools_df.empty else pd.DataFrame()
    filtered = _filter_tools(active_df, selected_company=selected_company) if not active_df.empty else active_df

    sub_tabs = st.tabs([
        "Market Map", "Builder Workflow", "Vibe Coding Core",
        "Impact × Investability", "Top 10", "Investability", "Tool Detail"
    ])

    with sub_tabs[0]:
        _render_market_map(filtered)
    with sub_tabs[1]:
        _render_builder_workflow(active_df, selected_company=selected_company)
    with sub_tabs[2]:
        _render_vibe_coding_core(active_df, top20_df)
    with sub_tabs[3]:
        _render_impact_investability_matrix(active_df)
    with sub_tabs[4]:
        _render_monthly_top10(active_df)
    with sub_tabs[5]:
        _render_investability(active_df)
    with sub_tabs[6]:
        _render_tool_detail(active_df, top20_df, selected_company=selected_company)

    st.info("Lecture recommandée : sépare toujours produit visible, société propriétaire, statut investissable, comparable coté et rôle réel dans la chaîne builder.")
