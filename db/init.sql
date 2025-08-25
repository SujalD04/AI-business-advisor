-- ------------------------------
-- Main Startup Table
-- ------------------------------
DROP TABLE IF EXISTS startup_info;

CREATE TABLE startup_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    stage VARCHAR(50),

    -- Financial
    revenue NUMERIC,
    costs NUMERIC,
    marketing_spend NUMERIC,
    profit NUMERIC,
    profit_margin NUMERIC,
    burn_rate NUMERIC,
    gross_margin NUMERIC,
    cac NUMERIC,
    ltv NUMERIC,
    cash_flow NUMERIC,
    cash_reserves NUMERIC,
    monthly_growth_rate NUMERIC,
    market_share NUMERIC,

    -- Operational
    churn_rate NUMERIC,
    retention_rate NUMERIC,
    employee_count INT,
    productivity NUMERIC,
    product_launches INT,
    nps_score NUMERIC,

    -- Market/Digital
    market_size NUMERIC,
    competition_index NUMERIC,
    website_traffic NUMERIC,
    conversion_rate NUMERIC,
    social_engagement NUMERIC,

    -- Label
    growth_category VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ------------------------------
-- Operational Metrics Table
-- ------------------------------
CREATE TABLE IF NOT EXISTS operational_metrics (
    id SERIAL PRIMARY KEY,
    startup_id INT REFERENCES startup_info(id) ON DELETE CASCADE,
    month DATE NOT NULL,
    active_users INT,
    new_customers INT,
    retention_rate NUMERIC,
    nps_score NUMERIC,
    support_tickets INT,
    infra_costs NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
