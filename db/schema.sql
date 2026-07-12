PRAGMA foreign_keys = ON;
CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    ticker TEXT UNIQUE NOT NULL,
    sector TEXT
);
CREATE TABLE profitandloss (
    pnl_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    operating_profit REAL,
    net_profit REAL,
    eps REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE balancesheet (
    bs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    equity REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE cashflow (
    cf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    operating_cashflow REAL,
    investing_cashflow REAL,
    financing_cashflow REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE analysis (
    analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    analysis TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    document_name TEXT,
    document_url TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE prosandcons (
    pc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    pros TEXT,
    cons TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE stock_prices (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    trade_date DATE,
    close_price REAL,
    volume INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE financial_ratios (
    ratio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    roe REAL,
    roce REAL,
    pe_ratio REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE peer_groups (
    peer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    peer_company TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
CREATE TABLE sectors (
    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT UNIQUE
);

