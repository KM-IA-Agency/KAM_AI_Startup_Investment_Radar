# Growth Stage and Opportunity Analysis

## Objective

For every identified startup or future company in the radar, estimate:

- current growth stage;
- basis for the stage estimate;
- latest known round or IPO/public status;
- next likely stage;
- short-term opportunity window;
- signals to monitor;
- suggested investor action.

## Why this matters

The same company can represent very different opportunities depending on maturity:

| Stage | Typical opportunity |
|---|---|
| Pre-Seed / Seed | early watchlist, founder tracking, first traction, future Seed or Series A |
| Series A / B | follow-on rounds, enterprise adoption, valuation reset, category leadership |
| Series C+ / Growth | pre-IPO secondary, strategic M&A, late-stage growth access |
| IPO / Public | public market entry, lock-up expiry, rerating, multiple compression |
| Unknown | data validation before interpretation |

## Tables

Two tables have been added.

### growth_stage_snapshots

Stores the current stage estimate:

- `startup_id`
- `company_name`
- `current_stage`
- `stage_basis`
- `last_known_round`
- `last_round_date`
- `last_round_amount`
- `last_known_valuation`
- `estimated_revenue_band`
- `estimated_headcount_band`
- `next_likely_stage`
- `next_stage_horizon`
- `stage_confidence_score`
- `analysis_run_id`
- `refreshed_at`

### stage_opportunities

Stores the next-step opportunity hypothesis:

- `startup_id`
- `company_name`
- `current_stage`
- `next_likely_stage`
- `opportunity_type`
- `opportunity_window`
- `opportunity_title`
- `opportunity_description`
- `probability_pct`
- `expected_impact_score`
- `access_difficulty_score`
- `investor_action`
- `watch_signals`
- `confidence_score`
- `analysis_run_id`
- `refreshed_at`

## Generation logic

The current MVP derives these tables from:

- `startups.stage`
- `financial_events`
- `benchmark_metrics`
- `ipo_events`

The generator is implemented in:

```text
src/stage_analysis.py
```

It is executed during:

```bash
python src/run_market_refresh.py --cadence manual --trigger-source manual_cli
```

through:

```text
src/load_to_db.py
```

## UI

A new Streamlit tab has been added:

```text
Stage & Opportunities
```

It shows:

- selected company stage;
- next likely stage;
- horizon;
- confidence;
- stage snapshot table;
- opportunity table;
- weighted impact chart;
- portfolio distribution by stage.

The sidebar `Startup focus` is propagated to this tab.

## Important limitation

The current stage analysis is a heuristic derived from existing internal seed and generated tables.

It should be improved with verified external sources:

- funding databases;
- company announcements;
- investor press releases;
- IPO filings;
- public market data;
- revenue/ARR/headcount signals;
- product usage signals.

## Next improvements

- Add source citation per stage estimate.
- Add manual validation status: unverified / analyst reviewed / source verified.
- Add stage history over time.
- Add stage transition alerts.
- Add opportunity scoring tied to Kamel Edge Score.
- Add secondary market and IPO watchlist feeds.
