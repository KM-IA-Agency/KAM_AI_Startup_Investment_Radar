-- KAM AI Startup Investment Radar - MVP schema

CREATE TABLE IF NOT EXISTS startups (
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    name TEXT NOT NULL,
    role TEXT,
    linkedin_url TEXT,
    background TEXT,
    technical_score INTEGER
);

CREATE TABLE IF NOT EXISTS funding_rounds (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER REFERENCES startups(id),
    round_type TEXT,
    amount NUMERIC,
    currency TEXT,
    announced_date DATE,
    investors TEXT,
    valuation_estimate NUMERIC,
    source_url TEXT
);

CREATE TABLE IF NOT EXISTS signals (
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
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
