-- ============================================================
-- 05_mysql_analytics.sql
-- Customer Intelligence & Revenue Analytics
-- ============================================================
-- 8 business-critical queries covering:
--   Q1  Monthly Revenue Trend + MoM Growth
--   Q2  Country Performance Ranking
--   Q3  Top 20 Products by Revenue
--   Q4  Customer Lifetime Value Ranking
--   Q5  Peak Trading Hours (Day x Hour matrix)

--   Q7  RFM Segment Revenue Summary
--   Q8  Year-over-Year Growth: UK vs International
--
-- Syntax : MySQL 8.0+  (CTEs, window functions, LAG, RANK, NTILE)
-- Usage  : mysql -u root -p retail_analytics < scripts/05_mysql_analytics.sql
-- ============================================================

USE retail_analytics;

-- ════════════════════════════════════════════════════════════
-- Q1: Monthly Revenue Trend with MoM Growth %
-- Window: LAG() to compare each month vs prior month
-- ════════════════════════════════════════════════════════════
WITH monthly AS (
    SELECT
        YearMonth,
        ROUND(SUM(Revenue), 2)              AS Total_Revenue,
        COUNT(DISTINCT CustomerID)           AS Active_Customers,
        COUNT(DISTINCT Invoice)              AS Total_Orders,
        ROUND(SUM(Revenue)
              / COUNT(DISTINCT Invoice), 2)  AS Avg_Order_Value
    FROM transactions
    GROUP BY YearMonth
)
SELECT
    YearMonth,
    Total_Revenue,
    Active_Customers,
    Total_Orders,
    Avg_Order_Value,
    LAG(Total_Revenue) OVER (ORDER BY YearMonth)     AS Prev_Month_Revenue,
    ROUND(
        (Total_Revenue - LAG(Total_Revenue) OVER (ORDER BY YearMonth))
        / LAG(Total_Revenue) OVER (ORDER BY YearMonth) * 100
    , 1)                                             AS MoM_Growth_Pct
FROM monthly
ORDER BY YearMonth;


-- ════════════════════════════════════════════════════════════
-- Q2: Country Performance Ranking (ex-UK)
-- Window: RANK() on revenue, DENSE_RANK() on customer count
-- ════════════════════════════════════════════════════════════
SELECT
    Country,
    COUNT(DISTINCT CustomerID)                          AS Customers,
    COUNT(DISTINCT Invoice)                             AS Orders,
    ROUND(SUM(Revenue), 2)                              AS Total_Revenue,
    ROUND(SUM(Revenue) / COUNT(DISTINCT CustomerID), 2) AS Revenue_Per_Customer,
    ROUND(SUM(Revenue) / COUNT(DISTINCT Invoice), 2)    AS Avg_Order_Value,
    RANK()       OVER (ORDER BY SUM(Revenue) DESC)      AS Revenue_Rank,
    DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT CustomerID) DESC) AS Customer_Rank
FROM transactions
WHERE Country != 'United Kingdom'
GROUP BY Country
ORDER BY Total_Revenue DESC
LIMIT 15;


-- ════════════════════════════════════════════════════════════
-- Q3: Top 20 Products by Revenue
-- Window: RANK() + NTILE(4) for revenue quartile
-- ════════════════════════════════════════════════════════════
WITH product_stats AS (
    SELECT
        StockCode,
        Description,
        COUNT(DISTINCT Invoice)     AS Times_Ordered,
        SUM(Quantity)               AS Total_Units_Sold,
        ROUND(SUM(Revenue), 2)      AS Total_Revenue,
        ROUND(AVG(Price), 2)        AS Avg_Unit_Price,
        COUNT(DISTINCT CustomerID)  AS Unique_Customers
    FROM transactions
    WHERE Description IS NOT NULL
    GROUP BY StockCode, Description
)
SELECT
    StockCode,
    Description,
    Times_Ordered,
    Total_Units_Sold,
    Total_Revenue,
    Avg_Unit_Price,
    Unique_Customers,
    RANK()    OVER (ORDER BY Total_Revenue DESC)     AS Revenue_Rank,
    NTILE(4)  OVER (ORDER BY Total_Revenue DESC)     AS Revenue_Quartile
FROM product_stats
ORDER BY Total_Revenue DESC
LIMIT 20;


-- ════════════════════════════════════════════════════════════
-- Q4: Customer Lifetime Value Ranking — Top 25
-- Window: RANK() on LTV, PERCENT_RANK() for percentile position
-- ════════════════════════════════════════════════════════════
WITH customer_stats AS (
    SELECT
        t.CustomerID,
        r.Segment,
        COUNT(DISTINCT t.Invoice)                          AS Total_Orders,
        ROUND(SUM(t.Revenue), 2)                           AS Lifetime_Value,
        ROUND(SUM(t.Revenue) / COUNT(DISTINCT t.Invoice), 2) AS Avg_Order_Value,
        MIN(t.InvoiceDate)                                 AS First_Purchase,
        MAX(t.InvoiceDate)                                 AS Last_Purchase,
        DATEDIFF(MAX(t.InvoiceDate), MIN(t.InvoiceDate))   AS Customer_Lifespan_Days,
        r.Recency                                          AS Days_Since_Last_Order
    FROM transactions t
    LEFT JOIN rfm_segments r ON t.CustomerID = r.CustomerID
    GROUP BY t.CustomerID, r.Segment, r.Recency
)
SELECT
    CustomerID,
    Segment,
    Total_Orders,
    Lifetime_Value,
    Avg_Order_Value,
    First_Purchase,
    Last_Purchase,
    Customer_Lifespan_Days,
    Days_Since_Last_Order,
    RANK()         OVER (ORDER BY Lifetime_Value DESC)  AS LTV_Rank,
    ROUND(
        PERCENT_RANK() OVER (ORDER BY Lifetime_Value) * 100
    , 1)                                                AS LTV_Percentile
FROM customer_stats
ORDER BY Lifetime_Value DESC
LIMIT 25;


-- ════════════════════════════════════════════════════════════
-- Q5: Peak Trading Hours — Day x Hour Revenue Matrix
-- Useful for campaign scheduling and ops planning
-- ════════════════════════════════════════════════════════════
SELECT
    DayOfWeek,
    Hour,
    COUNT(DISTINCT Invoice)       AS Orders,
    ROUND(SUM(Revenue), 2)        AS Revenue,
    COUNT(DISTINCT CustomerID)    AS Unique_Customers,
    RANK() OVER (
        PARTITION BY DayOfWeek
        ORDER BY SUM(Revenue) DESC
    )                             AS Hour_Rank_Within_Day
FROM transactions
GROUP BY DayOfWeek, Hour
ORDER BY
    FIELD(DayOfWeek,
          'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'),
    Hour;


-- ════════════════════════════════════════════════════════════
-- Q7: RFM Segment Revenue & Engagement Summary
-- Window: SUM() OVER() for revenue share without a subquery
-- ════════════════════════════════════════════════════════════
SELECT
    Segment,
    COUNT(CustomerID)                                  AS Customers,
    ROUND(AVG(Recency),   1)                           AS Avg_Recency_Days,
    ROUND(AVG(Frequency), 1)                           AS Avg_Orders,
    ROUND(AVG(Monetary),  2)                           AS Avg_Revenue_Per_Customer,
    ROUND(SUM(Monetary),  2)                           AS Total_Segment_Revenue,
    ROUND(
        SUM(Monetary) * 100.0
        / SUM(SUM(Monetary)) OVER ()
    , 1)                                               AS Revenue_Share_Pct,
    RANK() OVER (ORDER BY SUM(Monetary) DESC)          AS Revenue_Rank
FROM rfm_segments
GROUP BY Segment
ORDER BY Total_Segment_Revenue DESC;


-- ════════════════════════════════════════════════════════════
-- Q8: Year-over-Year Revenue & Customer Growth
-- UK vs International, 2010 vs 2011
-- Window: conditional aggregation + YoY delta calculation
-- ════════════════════════════════════════════════════════════
WITH yearly AS (
    SELECT
        Year,
        CASE
            WHEN Country = 'United Kingdom' THEN 'United Kingdom'
            ELSE 'International'
        END                             AS Region,
        ROUND(SUM(Revenue), 2)          AS Total_Revenue,
        COUNT(DISTINCT CustomerID)      AS Unique_Customers,
        COUNT(DISTINCT Invoice)         AS Total_Orders
    FROM transactions
    WHERE Year IN (2010, 2011)
    GROUP BY Year, Region
)
SELECT
    Region,
    MAX(CASE WHEN Year = 2010 THEN Total_Revenue    END) AS Revenue_2010,
    MAX(CASE WHEN Year = 2011 THEN Total_Revenue    END) AS Revenue_2011,
    ROUND(
        (MAX(CASE WHEN Year = 2011 THEN Total_Revenue END)
       - MAX(CASE WHEN Year = 2010 THEN Total_Revenue END))
        / MAX(CASE WHEN Year = 2010 THEN Total_Revenue END) * 100
    , 1)                                                 AS YoY_Revenue_Growth_Pct,
    MAX(CASE WHEN Year = 2010 THEN Unique_Customers END) AS Customers_2010,
    MAX(CASE WHEN Year = 2011 THEN Unique_Customers END) AS Customers_2011,
    ROUND(
        (MAX(CASE WHEN Year = 2011 THEN Unique_Customers END)
       - MAX(CASE WHEN Year = 2010 THEN Unique_Customers END))
        * 1.0 / MAX(CASE WHEN Year = 2010 THEN Unique_Customers END) * 100
    , 1)                                                 AS YoY_Customer_Growth_Pct
FROM yearly
GROUP BY Region
ORDER BY Revenue_2011 DESC;
