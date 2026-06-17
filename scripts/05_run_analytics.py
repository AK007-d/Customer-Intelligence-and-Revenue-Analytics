"""
05_run_analytics.py
Customer Intelligence & Revenue Analytics
----------------------------------------------
Executes all 8 analytical queries from 05_mysql_analytics.sql
using SQLite (same logic, MySQL-compatible syntax).
Exports results to outputs/q*.csv for Power BI import.

Input  : data/cleaned_transactions.csv, data/rfm_segments.csv
Outputs: outputs/q1_monthly_revenue.csv ... q8_yoy_growth.csv
"""

import pandas as pd
import sqlite3
import os

CLEAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_transactions.csv')
RFM_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'rfm_segments.csv')
OUT_DIR    = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load into in-memory SQLite ────────────────────────────────
print("Loading data into database ...")
conn = sqlite3.connect(':memory:')
df   = pd.read_csv(CLEAN_PATH)
rfm  = pd.read_csv(RFM_PATH)
rfm.rename(columns={'Customer ID': 'CustomerID'}, inplace=True)
df.rename(columns={'Customer ID': 'CustomerID'}, inplace=True)
df.to_sql('transactions',  conn, if_exists='replace', index=False)
rfm.to_sql('rfm_segments', conn, if_exists='replace', index=False)
print(f"  transactions : {len(df):,} rows")
print(f"  rfm_segments : {len(rfm):,} rows\n")

def run(name, description, sql):
    print(f"Running {name}: {description}")
    result = pd.read_sql_query(sql, conn)
    result.to_csv(os.path.join(OUT_DIR, f'{name}.csv'), index=False)
    print(result.head(5).to_string(index=False))
    print()
    return result

# ── Q1: Monthly Revenue Trend + MoM Growth ───────────────────
run('q1_monthly_revenue', 'Monthly Revenue Trend with MoM Growth %', """
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
        LAG(Total_Revenue) OVER (ORDER BY YearMonth)  AS Prev_Month_Revenue,
        ROUND(
            (Total_Revenue - LAG(Total_Revenue) OVER (ORDER BY YearMonth))
            / LAG(Total_Revenue) OVER (ORDER BY YearMonth) * 100
        , 1) AS MoM_Growth_Pct
    FROM monthly
    ORDER BY YearMonth
""")

# ── Q2: Country Performance Ranking ──────────────────────────
run('q2_country_performance', 'Top 15 Countries by Revenue (ex-UK)', """
    SELECT
        Country,
        COUNT(DISTINCT CustomerID)                          AS Customers,
        COUNT(DISTINCT Invoice)                             AS Orders,
        ROUND(SUM(Revenue), 2)                              AS Total_Revenue,
        ROUND(SUM(Revenue) / COUNT(DISTINCT CustomerID), 2) AS Revenue_Per_Customer,
        ROUND(SUM(Revenue) / COUNT(DISTINCT Invoice), 2)    AS Avg_Order_Value,
        RANK() OVER (ORDER BY SUM(Revenue) DESC)            AS Revenue_Rank
    FROM transactions
    WHERE Country != 'United Kingdom'
    GROUP BY Country
    ORDER BY Total_Revenue DESC
    LIMIT 15
""")

# ── Q3: Top 20 Products ───────────────────────────────────────
run('q3_top_products', 'Top 20 Products by Revenue', """
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
        RANK() OVER (ORDER BY Total_Revenue DESC) AS Revenue_Rank
    FROM product_stats
    ORDER BY Total_Revenue DESC
    LIMIT 20
""")

# ── Q4: Customer LTV Ranking ──────────────────────────────────
run('q4_customer_ltv', 'Top 25 Customers by Lifetime Value', """
    WITH customer_stats AS (
        SELECT
            t.CustomerID,
            r.Segment,
            COUNT(DISTINCT t.Invoice)                             AS Total_Orders,
            ROUND(SUM(t.Revenue), 2)                              AS Lifetime_Value,
            ROUND(SUM(t.Revenue) / COUNT(DISTINCT t.Invoice), 2)  AS Avg_Order_Value,
            MIN(t.InvoiceDate)                                    AS First_Purchase,
            MAX(t.InvoiceDate)                                    AS Last_Purchase,
            r.Recency                                             AS Days_Since_Last_Order
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
        Days_Since_Last_Order,
        RANK() OVER (ORDER BY Lifetime_Value DESC) AS LTV_Rank
    FROM customer_stats
    ORDER BY Lifetime_Value DESC
    LIMIT 25
""")

# ── Q5: Peak Trading Hours ────────────────────────────────────
run('q5_peak_hours', 'Revenue by Day of Week and Hour', """
    SELECT
        DayOfWeek,
        Hour,
        COUNT(DISTINCT Invoice)    AS Orders,
        ROUND(SUM(Revenue), 2)     AS Revenue,
        COUNT(DISTINCT CustomerID) AS Unique_Customers,
        RANK() OVER (
            PARTITION BY DayOfWeek
            ORDER BY SUM(Revenue) DESC
        ) AS Hour_Rank_Within_Day
    FROM transactions
    GROUP BY DayOfWeek, Hour
    ORDER BY
        CASE DayOfWeek
            WHEN 'Monday'    THEN 1 WHEN 'Tuesday'   THEN 2
            WHEN 'Wednesday' THEN 3 WHEN 'Thursday'  THEN 4
            WHEN 'Friday'    THEN 5 WHEN 'Saturday'  THEN 6
            ELSE 7 END,
        Hour
""")

# ── Q7: RFM Segment Summary ───────────────────────────────────
run('q7_segment_summary', 'Revenue & Engagement by RFM Segment', """
    SELECT
        Segment,
        COUNT(CustomerID)           AS Customers,
        ROUND(AVG(Recency),   1)    AS Avg_Recency_Days,
        ROUND(AVG(Frequency), 1)    AS Avg_Orders,
        ROUND(AVG(Monetary),  2)    AS Avg_Revenue_Per_Customer,
        ROUND(SUM(Monetary),  2)    AS Total_Segment_Revenue,
        ROUND(
            SUM(Monetary) * 100.0
            / SUM(SUM(Monetary)) OVER ()
        , 1)                        AS Revenue_Share_Pct,
        RANK() OVER (ORDER BY SUM(Monetary) DESC) AS Revenue_Rank
    FROM rfm_segments
    GROUP BY Segment
    ORDER BY Total_Segment_Revenue DESC
""")

# ── Q8: Year-over-Year Growth ─────────────────────────────────
run('q8_yoy_growth', 'YoY Revenue Growth: UK vs International', """
    WITH yearly AS (
        SELECT
            Year,
            CASE WHEN Country = 'United Kingdom'
                 THEN 'United Kingdom' ELSE 'International'
            END                         AS Region,
            ROUND(SUM(Revenue), 2)      AS Total_Revenue,
            COUNT(DISTINCT CustomerID)  AS Unique_Customers,
            COUNT(DISTINCT Invoice)     AS Total_Orders
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
    ORDER BY Revenue_2011 DESC
""")

conn.close()
print("[05] All 8 queries complete. Results exported to outputs/")
