-- KAM AI Startup Investment Radar - MVP schema
-- Compatible with PostgreSQL-oriented design and SQLite local fallback.

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
CREATE INDEX IF NOT EXISTS idx_public_market_obs_startup_date ON public_market_observations(startup_id, observed_at DESC);
