-- Example SQL Server queries after importing Retail_sales_cleaned.csv
-- Import into dbo.RetailSales with typed columns (OrderDate date; Revenue, Profit,
-- Discount and ProfitMargin numeric). Adjust the table name if needed.

-- Executive KPIs
SELECT
    COUNT(DISTINCT OrderID) AS TotalOrders,
    SUM(Revenue) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    CAST(SUM(Revenue) / NULLIF(COUNT(DISTINCT OrderID), 0) AS decimal(18, 2)) AS AverageOrderValue,
    CAST(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0) AS decimal(8, 2)) AS WeightedProfitMarginPct
FROM dbo.RetailSales;

-- Regional performance
SELECT Region, COUNT(DISTINCT OrderID) AS Orders,
       SUM(Revenue) AS Revenue, SUM(Profit) AS Profit
FROM dbo.RetailSales
GROUP BY Region
ORDER BY Revenue DESC;

-- Monthly trend, preserving the year
SELECT YEAR(OrderDate) AS OrderYear, MONTH(OrderDate) AS OrderMonth,
       SUM(Revenue) AS Revenue, SUM(Profit) AS Profit
FROM dbo.RetailSales
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY OrderYear, OrderMonth;

-- Customer-segment comparison
SELECT Segment, COUNT(DISTINCT OrderID) AS Orders,
       AVG(Revenue) AS AverageOrderRevenue,
       SUM(Profit) AS TotalProfit
FROM dbo.RetailSales
GROUP BY Segment
ORDER BY TotalProfit DESC;

-- Discount-band comparison. Descriptive association, not causal impact.
SELECT DiscountLevel, COUNT(*) AS Orders,
       AVG(Discount) AS AverageDiscount,
       AVG(Profit) AS AverageOrderProfit,
       CAST(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0) AS decimal(8, 2)) AS WeightedProfitMarginPct
FROM dbo.RetailSales
GROUP BY DiscountLevel
ORDER BY AverageDiscount;
