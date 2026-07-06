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

### 4. Impact × Investability

Displays a scatter matrix:

- X axis: `investability_score`
- Y axis: `strategic_impact_score`
- Bubble size: radar priority

Quadrants:

| Quadrant | Meaning |
|---|---|
| High impact / Investable | High strategic value and easier public or comparable exposure |
| High impact / Hard to access | Strategically important but private or difficult to access |
| Investable comparable | Public/comparable exposure but lower direct startup upside |
| Workflow / Watchlist | Useful builder workflow tools or weaker investment signal |

The current scoring is heuristic. It combines:

- radar priority;
- category;
- investment relevance;
- recent signal keywords;
- core Vibe Coding keywords;
- public/private/platform accessibility.

It is intended for prioritization, not as financial advice.

### 5. Top 10

Creates a monthly-style Top 10 list of tools/signals to watch.

The score combines:

- strategic impact;
- investability;
- radar priority;
- recent signal bonus.

Recent signal keywords currently include:

- GLM-5.2;
- ZCode;
- Cursor;
- Claude Code;
- Codex;
- Lovable;
- Windsurf;
- Replit Agent;
- Bolt.new;
- OpenRouter;
- LangGraph;
- n8n.

This produces a practical watchlist for monthly review.

### 6. Investability

Separates:

- public comparables;
- private startups;
- strategic platform risks;
- workflow utilities.

### 7. Tool Detail

Displays a detailed card for one selected tool or product group, including:

- category;
- radar priority;
- company/owner;
- strategic impact score;
- investability score;
- quadrant;
- role;
- investment relevance;
- notes.

## Run

```bash
streamlit run app/streamlit_app.py
```

Then open:

```text
AI Tools Stack
```

## Next improvements

- Add real event signals from `upcoming_events_seed.csv`.
- Add source citations and validation status per tool.
- Add public/private status from product mapping.
- Add monthly history to track ranking changes.
- Add charts for category momentum over time.
- Add export of the Top 10 monthly watchlist.
