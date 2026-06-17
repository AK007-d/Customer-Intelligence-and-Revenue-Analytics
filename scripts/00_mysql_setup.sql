-- ============================================================
-- 00_mysql_setup.sql
-- Customer Intelligence & Revenue Analytics
-- ============================================================
-- Run this FIRST to create the schema and tables.
-- Then load data using 04_load_mysql.py or via MySQL Workbench.
--
-- Tested on: MySQL 8.0+
-- Usage    : mysql -u root -p < scripts/00_mysql_setup.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS retail_analytics
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE retail_analytics;

-- ── Drop if re-running ────────────────────────────────────────
DROP TABLE IF EXISTS rfm_segments;
DROP TABLE IF EXISTS transactions;

-- ── Core transactions table ───────────────────────────────────
CREATE TABLE transactions (
    id            INT            NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Invoice       VARCHAR(20)    NOT NULL,
    StockCode     VARCHAR(20)    NOT NULL,
    Description   VARCHAR(255),
    Quantity      INT            NOT NULL,
    InvoiceDate   DATETIME       NOT NULL,
    Price         DECIMAL(10,2)  NOT NULL,
    CustomerID    VARCHAR(20)    NOT NULL,
    Country       VARCHAR(100)   NOT NULL,
    Revenue       DECIMAL(12,2)  NOT NULL,
    YearMonth     VARCHAR(7)     NOT NULL,   -- e.g. '2010-12'
    Year          SMALLINT       NOT NULL,
    Month         TINYINT        NOT NULL,
    DayOfWeek     VARCHAR(10)    NOT NULL,
    Hour          TINYINT        NOT NULL,

    INDEX idx_customer   (CustomerID),
    INDEX idx_invoice    (Invoice),
    INDEX idx_yearmonth  (YearMonth),
    INDEX idx_country    (Country),
    INDEX idx_stockcode  (StockCode),
    INDEX idx_date       (InvoiceDate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── RFM segments table ────────────────────────────────────────
CREATE TABLE rfm_segments (
    CustomerID    VARCHAR(20)    NOT NULL PRIMARY KEY,
    Recency       INT            NOT NULL,   -- days since last purchase
    Frequency     INT            NOT NULL,   -- number of orders
    Monetary      DECIMAL(12,2)  NOT NULL,   -- total spend
    R_Score       TINYINT        NOT NULL,
    F_Score       TINYINT        NOT NULL,
    M_Score       TINYINT        NOT NULL,
    RFM_Score     VARCHAR(3)     NOT NULL,
    RFM_Total     TINYINT        NOT NULL,
    Segment       VARCHAR(50)    NOT NULL,

    INDEX idx_segment    (Segment),
    INDEX idx_rfm_total  (RFM_Total)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT 'Schema created successfully.' AS Status;
