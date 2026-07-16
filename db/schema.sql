PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS financial_ratios;
DROP TABLE IF EXISTS market_cap;
DROP TABLE IF EXISTS peer_groups;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS companies;

CREATE TABLE companies (
    company_id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    ticker TEXT UNIQUE NOT NULL,
    sector TEXT
);

CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,
    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,
    free_cash_flow_cr REAL,
    capex_cr REAL,
    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,
    total_debt_cr REAL,
    cash_from_operations_cr REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE market_cap (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,
    market_cap_crore REAL,
    enterprise_value_crore REAL,
    pe_ratio REAL,
    pb_ratio REAL,
    ev_ebitda REAL,
    dividend_yield_pct REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY,
    peer_group_name TEXT,
    company_id TEXT NOT NULL,
    is_benchmark INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    adjusted_close REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);