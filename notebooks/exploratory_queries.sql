-- 1. Count companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. List all companies
SELECT *
FROM companies;

-- 3. Count financial ratio records
SELECT COUNT(*) AS total_ratio_records
FROM financial_ratios;

-- 4. Year coverage
SELECT
    company_id,
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(DISTINCT year) AS total_years
FROM financial_ratios
GROUP BY company_id;

-- 5. Companies with less than 5 years
SELECT
    company_id,
    COUNT(DISTINCT year) AS years_available
FROM financial_ratios
GROUP BY company_id
HAVING COUNT(DISTINCT year) < 5;

-- 6. Average ROE by company
SELECT
    company_id,
    AVG(return_on_equity_pct) AS average_roe
FROM financial_ratios
GROUP BY company_id;

-- 7. Average profit margin
SELECT
    company_id,
    AVG(net_profit_margin_pct) AS average_profit_margin
FROM financial_ratios
GROUP BY company_id;

-- 8. Market cap information
SELECT
    company_id,
    MAX(market_cap_crore) AS highest_market_cap
FROM market_cap
GROUP BY company_id;

-- 9. Stock price record count
SELECT
    company_id,
    COUNT(*) AS price_records
FROM stock_prices
GROUP BY company_id;

-- 10. Check missing company references
SELECT
    fr.company_id
FROM financial_ratios fr
LEFT JOIN companies c
ON fr.company_id = c.company_id
WHERE c.company_id IS NULL;