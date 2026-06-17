"""
04_load_mysql.py
Customer Intelligence & Revenue Analytics
----------------------------------------------
Loads cleaned CSVs into a MySQL database.
Run AFTER 00_mysql_setup.sql has been executed.

Prerequisites:
    pip install mysql-connector-python pandas

Usage:
    python scripts/04_load_mysql.py \
        --host localhost --user root --password yourpassword

The script uses batch inserts (1,000 rows/batch) for performance.
"""

import pandas as pd
import argparse
import os
import sys

CLEAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_transactions.csv')
RFM_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'rfm_segments.csv')

def load_data(host, user, password, database='retail_analytics', port=3306):
    try:
        import mysql.connector
    except ImportError:
        print("Install connector first:  pip install mysql-connector-python")
        sys.exit(1)

    print(f"Connecting to MySQL at {host}:{port} ...")
    conn = mysql.connector.connect(
        host=host, user=user, password=password,
        database=database, port=port
    )
    cursor = conn.cursor()
    print("  Connected.\n")

    # ── Load transactions ─────────────────────────────────────
    print("Loading transactions ...")
    df = pd.read_csv(CLEAN_PATH)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']).dt.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("TRUNCATE TABLE transactions")
    cols = ['Invoice','StockCode','Description','Quantity','InvoiceDate',
            'Price','Customer ID','Country','Revenue','YearMonth','Year',
            'Month','DayOfWeek','Hour']
    insert_sql = """
        INSERT INTO transactions
            (Invoice, StockCode, Description, Quantity, InvoiceDate,
             Price, CustomerID, Country, Revenue, YearMonth, Year,
             Month, DayOfWeek, Hour)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    batch_size = 1000
    rows = [tuple(r) for r in df[cols].itertuples(index=False)]
    for i in range(0, len(rows), batch_size):
        cursor.executemany(insert_sql, rows[i:i+batch_size])
        if i % 100000 == 0:
            print(f"  Inserted {i:,} / {len(rows):,} rows ...")
            conn.commit()
    conn.commit()
    print(f"  transactions: {len(rows):,} rows inserted.\n")

    # ── Load RFM segments ─────────────────────────────────────
    print("Loading rfm_segments ...")
    rfm = pd.read_csv(RFM_PATH)
    cursor.execute("TRUNCATE TABLE rfm_segments")
    rfm_sql = """
        INSERT INTO rfm_segments
            (CustomerID, Recency, Frequency, Monetary,
             R_Score, F_Score, M_Score, RFM_Score, RFM_Total, Segment)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    rfm_cols = ['Customer ID','Recency','Frequency','Monetary',
                'R_Score','F_Score','M_Score','RFM_Score','RFM_Total','Segment']
    rfm_rows = [tuple(r) for r in rfm[rfm_cols].itertuples(index=False)]
    cursor.executemany(rfm_sql, rfm_rows)
    conn.commit()
    print(f"  rfm_segments : {len(rfm_rows):,} rows inserted.\n")

    cursor.close()
    conn.close()
    print("Done. All data loaded into MySQL.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load retail data into MySQL')
    parser.add_argument('--host',     default='localhost')
    parser.add_argument('--user',     default='root')
    parser.add_argument('--password', required=True)
    parser.add_argument('--database', default='retail_analytics')
    parser.add_argument('--port',     default=3306, type=int)
    args = parser.parse_args()
    load_data(args.host, args.user, args.password, args.database, args.port)
