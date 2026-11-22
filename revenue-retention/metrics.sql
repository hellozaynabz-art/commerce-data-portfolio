-- Executed against cleaned line-item data in SQLite by analysis.py.
-- Gross = positive non-cancelled merchandise sales; credits are not matched returns.
SELECT month, region,
 ROUND(SUM(CASE WHEN Quantity > 0 AND cancel = 0 THEN amount ELSE 0 END),2) AS gross_sales,
 ROUND(-SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END),2) AS credit_value,
 ROUND(SUM(amount),2) AS net_sales,
 COUNT(DISTINCT CASE WHEN Quantity > 0 AND cancel = 0 THEN InvoiceNo END) AS orders
FROM lines
GROUP BY month, region
ORDER BY month, region;
