-- KAM AI Startup Investment Radar - MVP schema
-- Compatible with PostgreSQL-oriented design and SQLite local fallback.

CREATE TABLE IF NOT EXISTS analysis_runs (
    id INTEGER PRIMARY KEY,
    run_name TEXT NOT NULL,
    run_type TEXT NOT NULL,
    cadence TEXT,
    started_at TIMESTAMP NOT NULL,
    finished_at TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'running',
    trigger_source TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS table_refresh_log (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    table_name TEXT NOT NULL,
    source_name TEXT,
    source_type TEXT,
    source_path TEXT,
    rows_loaded INTEGER DEFAULT 0,
    observed_from TIMESTAMP,
    observed_to TIMESTAMP,
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'success',
    notes TEXT
);

CREATE TABLE IF NOT EXISTS startups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    website TEXT,
    country TEXT,
    region TEXT,
    sector TEXT NOT NULL,
    sub_sector TEXT,
    stage TEXT,
    founded_year INTEGER,
    description TEXT,
    status TEXT DEFAULT 'unknown',
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS founders (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    name TEXT NOT NULL,
    role TEXT,
    linkedin_url TEXT,
    background TEXT,
    technical_score INTEGER
);

CREATE TABLE IF NOT EXISTS funding_rounds (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    round_type TEXT,
    amount NUMERIC,
    currency TEXT,
    announced_date DATE,
    investors TEXT,
    valuation_estimate NUMERIC,
    source_url TEXT
);

CREATE TABLE IF NOT EXISTS financial_events (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    event_date DATE NOT NULL,
    event_type TEXT NOT NULL,
    event_title TEXT NOT NULL,
    amount NUMERIC,
    valuation NUMERIC,
    currency TEXT DEFAULT 'USD',
    share_price NUMERIC,
    ticker TEXT,
    exchange_name TEXT,
    description TEXT,
    source_url TEXT,
    confidence_score INTEGER,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ipo_events (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    name TEXT NOT NULL,
    ipo_date DATE,
    event_type TEXT,
    ipo_price NUMERIC,
    first_day_close NUMERIC,
    latest_share_price NUMERIC,
    shares_outstanding NUMERIC,
    market_cap_latest NUMERIC,
    currency TEXT DEFAULT 'USD',
    ticker TEXT,
    exchange_name TEXT,
    description TEXT,
    source_url TEXT,
    confidence_score INTEGER,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, ipo_date, ticker)
);

CREATE TABLE IF NOT EXISTS public_market_observations (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    observed_at DATE NOT NULL,
    ticker TEXT,
    exchange_name TEXT,
    share_price NUMERIC,
    market_cap NUMERIC,
    enterprise_value NUMERIC,
    currency TEXT DEFAULT 'USD',
    source TEXT,
    source_url TEXT,
    confidence_score INTEGER,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_mappings (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    company_name TEXT NOT NULL,
    public_name TEXT,
    flagship_product TEXT,
    product_category TEXT,
    related_startup_or_segment TEXT,
    ticker TEXT,
    exchange_name TEXT,
    status TEXT,
    notes TEXT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_name, public_name, flagship_product)
);

CREATE TABLE IF NOT EXISTS ai_tools (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    company_name TEXT,
    tool_or_group TEXT NOT NULL,
    category TEXT NOT NULL,
    role TEXT,
    investment_relevance TEXT,
    radar_priority TEXT,
    status TEXT,
    source_dataset TEXT,
    notes TEXT,
    strategic_impact_score INTEGER,
    investability_score INTEGER,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tool_or_group, company_name, category)
);

CREATE TABLE IF NOT EXISTS upcoming_events (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    company_name TEXT NOT NULL,
    product_or_segment TEXT,
    event_window TEXT,
    event_type TEXT,
    event_title TEXT,
    probability_pct NUMERIC,
    impact_score INTEGER,
    confidence_score INTEGER,
    expected_effect TEXT,
    watch_signals TEXT,
    notes TEXT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_name, product_or_segment, event_window, event_type, event_title)
);

CREATE TABLE IF NOT EXISTS benchmark_metrics (
    startup_id INTEGER PRIMARY KEY REFERENCES startups(id),
    currency TEXT DEFAULT 'USD',
    revenue_latest NUMERIC,
    revenue_period TEXT,
    revenue_growth_yoy_pct NUMERIC,
    revenue_growth_qoq_pct NUMERIC,
    valuation_latest NUMERIC,
    valuation_date DATE,
    total_funding NUMERIC,
    latest_round_amount NUMERIC,
    latest_round_date DATE,
    employees_latest INTEGER,
    employee_growth_6m_pct NUMERIC,
    web_traffic_growth_3m_pct NUMERIC,
    github_stars INTEGER,
    github_stars_growth_3m_pct NUMERIC,
    customer_count_estimate INTEGER,
    data_confidence INTEGER,
    notes TEXT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS metric_observations (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    observed_at TIMESTAMP NOT NULL,
    period_type TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC,
    metric_unit TEXT,
    source TEXT,
    source_url TEXT,
    confidence_score INTEGER,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scenario_forecasts (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    forecast_date DATE NOT NULL,
    horizon_months INTEGER NOT NULL,
    scenario TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    current_value NUMERIC,
    forecast_value NUMERIC,
    implied_cagr_pct NUMERIC,
    probability_pct NUMERIC,
    confidence_score INTEGER,
    assumptions TEXT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    signal_type TEXT NOT NULL,
    signal_date DATE,
    title TEXT NOT NULL,
    summary TEXT,
    source TEXT,
    source_url TEXT,
    impact_score INTEGER,
    confidence_score INTEGER,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scores (
    startup_id INTEGER PRIMARY KEY REFERENCES startups(id),
    market_score INTEGER,
    problem_pain_score INTEGER,
    product_maturity_score INTEGER,
    traction_score INTEGER,
    team_score INTEGER,
    technical_moat_score INTEGER,
    valuation_score INTEGER,
    investor_quality_score INTEGER,
    exit_potential_score INTEGER,
    risk_score INTEGER,
    kamel_edge_score INTEGER,
    total_score INTEGER,
    decision TEXT,
    score_explanation TEXT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS investment_memos (
    id INTEGER PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    memo_date DATE DEFAULT CURRENT_DATE,
    summary TEXT,
    problem TEXT,
    solution TEXT,
    market TEXT,
    technology TEXT,
    traction TEXT,
    moat TEXT,
    valuation TEXT,
    risks TEXT,
    decision TEXT,
    next_actions TEXT,
    analysis_run_id INTEGER REFERENCES analysis_runs(id),
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_analysis_runs_started ON analysis_runs(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_analysis_runs_type ON analysis_runs(run_type, cadence, status);
CREATE INDEX IF NOT EXISTS idx_table_refresh_log_run ON table_refresh_log(analysis_run_id);
CREATE INDEX IF NOT EXISTS idx_table_refresh_log_table ON table_refresh_log(table_name, refreshed_at DESC);
CREATE INDEX IF NOT EXISTS idx_startups_country ON startups(country);
CREATE INDEX IF NOT EXISTS idx_startups_sector ON startups(sector);
CREATE INDEX IF NOT EXISTS idx_startups_stage ON startups(stage);
CREATE INDEX IF NOT EXISTS idx_scores_total_score ON scores(total_score DESC);
CREATE INDEX IF NOT EXISTS idx_scores_decision ON scores(decision);
CREATE INDEX IF NOT EXISTS idx_signals_startup_date ON signals(startup_id, signal_date DESC);
CREATE INDEX IF NOT EXISTS idx_metric_observations_startup_metric ON metric_observations(startup_id, metric_name, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_metric_observations_period ON metric_observations(period_type, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_scenario_forecasts_startup ON scenario_forecasts(startup_id, metric_name, horizon_months, scenario);
CREATE INDEX IF NOT EXISTS idx_financial_events_startup_date ON financial_events(startup_id, event_date DESC);
CREATE INDEX IF NOT EXISTS idx_ipo_events_startup_date ON ipo_events(startup_id, ipo_date DESC);
CREATE INDEX IF NOT EXISTS idx_public_market_obs_startup_date ON public_market_observations(startup_id, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_product_mappings_startup ON product_mappings(startup_id);
CREATE INDEX IF NOT EXISTS idx_product_mappings_company ON product_mappings(company_name);
CREATE INDEX IF NOT EXISTS idx_ai_tools_startup ON ai_tools(startup_id);
CREATE INDEX IF NOT EXISTS idx_ai_tools_category ON ai_tools(category);
CREATE INDEX IF NOT EXISTS idx_ai_tools_priority ON ai_tools(radar_priority);
CREATE INDEX IF NOT EXISTS idx_upcoming_events_startup ON upcoming_events(startup_id);
CREATE INDEX IF NOT EXISTS idx_upcoming_events_company ON upcoming_events(company_name);
