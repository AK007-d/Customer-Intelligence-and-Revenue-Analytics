"""
01_data_cleaning.py
Customer Intelligence & Revenue Analytics
----------------------------------------------
Cleans the UCI Online Retail II dataset and exports a validated,
analysis-ready CSV used by all downstream scripts.

Raw data: data/online_retail_II.csv (1,067,371 rows)
Output  : data/cleaned_transactions.csv
"""

import pandas as pd
import os

RAW_PATH     = os.path.join(os.path.dirname(__file__), '..', 'data', 'online_retail_II.csv')
CLEAN_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_transactions.csv')
CANCEL_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'cancelled_transactions.csv')

# ── 1. Load ──────────────────────────────────────────────────────────────────
print("Loading raw data...")
df = pd.read_csv(RAW_PATH, encoding='utf-8', low_memory=False)
print(f"  Raw rows        : {len(df):,}")

# ── 2. Parse dates ───────────────────────────────────────────────────────────
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Year']        = df['InvoiceDate'].dt.year
df['Month']       = df['InvoiceDate'].dt.month
df['YearMonth']   = df['InvoiceDate'].dt.to_period('M').astype(str)
df['DayOfWeek']   = df['InvoiceDate'].dt.day_name()
df['Hour']        = df['InvoiceDate'].dt.hour

# ── 3. Separate cancellations ─────────────────────────────────────────────────
cancelled = df[df['Invoice'].astype(str).str.startswith('C')].copy()
df        = df[~df['Invoice'].astype(str).str.startswith('C')].copy()
print(f"  Cancellations   : {len(cancelled):,}")

# ── 4. Drop rows missing Customer ID (guest checkouts) ───────────────────────
before = len(df)
df = df.dropna(subset=['Customer ID'])
print(f"  Dropped (no CID): {before - len(df):,}")

# ── 5. Drop negative / zero quantity & price ──────────────────────────────────
df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]
print(f"  After qty/price filter: {len(df):,}")

# ── 6. Derived columns ────────────────────────────────────────────────────────
df['Revenue']     = df['Quantity'] * df['Price']
df['Customer ID'] = df['Customer ID'].astype(int).astype(str)

# ── 7. Drop test / adjustment stock codes ────────────────────────────────────
bad_codes = ['POST', 'D', 'M', 'BANK CHARGES', 'PADS', 'DOT']
df = df[~df['StockCode'].isin(bad_codes)]

# ── 8. Export ─────────────────────────────────────────────────────────────────
df.to_csv(CLEAN_PATH,  index=False)
cancelled.to_csv(CANCEL_PATH, index=False)

print(f"\n  Clean rows      : {len(df):,}")
print(f"  Date range      : {df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}")
print(f"  Unique customers: {df['Customer ID'].nunique():,}")
print(f"  Unique products : {df['StockCode'].nunique():,}")
print(f"  Countries       : {df['Country'].nunique()}")
print(f"  Total revenue   : £{df['Revenue'].sum():,.0f}")
print(f"\n[01] Cleaning complete. Output -> data/cleaned_transactions.csv")
