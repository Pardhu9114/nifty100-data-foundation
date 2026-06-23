-- Query 1: Total companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- Query 2: Top 10 companies by sales
SELECT company_id, year, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- Query 3: Top 10 companies by net profit
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- Query 4: Highest ROE companies
SELECT company_id, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- Query 5: Highest ROCE companies
SELECT company_id, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- Query 6: Top market cap companies
SELECT company_id, market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- Query 7: Companies with negative cash flow
SELECT company_id, year, net_cash_flow
FROM cashflow
WHERE net_cash_flow < 0;

-- Query 8: Companies with highest debt
SELECT company_id, year, borrowings
FROM balancesheet
ORDER BY borrowings DESC
LIMIT 10;

-- Query 9: Sector distribution
SELECT broad_sector, COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

-- Query 10: Companies with highest dividend payout
SELECT company_id, year, dividend_payout
FROM profitandloss
ORDER BY dividend_payout DESC
LIMIT 10;