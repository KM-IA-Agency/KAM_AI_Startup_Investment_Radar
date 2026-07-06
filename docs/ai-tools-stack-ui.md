# AI Tools Stack UI

## Purpose

The Streamlit app now includes a dedicated tab:

```text
AI Tools Stack
```

This tab presents the July 2026 AI tools taxonomy as an interactive market map.

## Data sources

The view reads:

```text
data/seeds/ai_tools_trending_by_category_july2026.csv
data/seeds/vibe_coding_top20_july2026.csv
```

## Subviews

### 1. Market Map

Shows all tools by category with filters for:

- category;
- radar priority;
- investment relevance.

Also includes:

- tool count;
- category count;
- high-priority count;
- number of code/dev tools;
- count by category chart;
- expandable category cards.

### 2. Builder Workflow

Shows the builder chain:

```text
idea → research → synthesis → prototype → code → app builder → automation → design → video/audio → presentation → monitoring
```

Each step displays associated tools.

### 3. Vibe Coding Core

Focuses on tools that directly build software or code workflows:

- Cursor;
- Claude Code;
- Codex;
- GitHub Copilot;
- Windsurf;
- Lovable;
- Bolt.new;
- Replit Agent;
- v0;
- Base44;
- Devin;
- Z.ai GLM-5.2 / ZCode.

### 4. Investability

Separates:

- public comparables;
- private startups;
- strategic platform risks;
- workflow utilities.

### 5. Tool Detail

Displays a detailed card for one selected tool or product group.

## Run

```bash
streamlit run app/streamlit_app.py
```

Then open:

```text
AI Tools Stack
```

## Next improvements

- Add heatmap by impact versus investability.
- Add public/private status from product mapping.
- Add monthly Top 10 priorities.
- Connect event signals from `upcoming_events_seed.csv`.
- Add charts for category momentum over time.
