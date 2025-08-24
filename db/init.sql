CREATE TABLE IF NOT EXISTS startup_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    stage VARCHAR(50),
    revenue NUMERIC,
    costs NUMERIC,
    churn_rate NUMERIC,
    marketing_spend NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
