"""
02_rfm_segmentation.py
Customer Intelligence & Revenue Analytics
----------------------------------------------
Builds RFM (Recency, Frequency, Monetary) scores for every customer,
assigns a named segment, and exports the segment table.

Input  : data/cleaned_transactions.csv
Outputs: data/rfm_segments.csv
         outputs/rfm_segment_distribution.png
         outputs/rfm_revenue_by_segment.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

CLEAN_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_transactions.csv')
RFM_PATH    = os.path.join(os.path.dirname(__file__), '..', 'data', 'rfm_segments.csv')
OUT_DIR     = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)

PALETTE = {
    'Champions':          '#2ecc71',
    'Loyal Customers':    '#27ae60',
    'Potential Loyalists':'#58d68d',
    'Promising':          '#a9dfbf',
    'At Risk':            '#e67e22',
    'Hibernating':        '#e74c3c',
    'Lost':               '#c0392b',
    'New Customers':      '#3498db',
    'Need Attention':     '#f39c12',
    'About to Sleep':     '#f8c471',
}

# ── 1. Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(CLEAN_PATH, parse_dates=['InvoiceDate'])
snapshot = df['InvoiceDate'].max() + pd.Timedelta(days=1)   # analysis reference date

# ── 2. Compute raw RFM metrics ────────────────────────────────────────────────
rfm = df.groupby('Customer ID').agg(
    Recency   = ('InvoiceDate', lambda x: (snapshot - x.max()).days),
    Frequency = ('Invoice',     'nunique'),
    Monetary  = ('Revenue',     'sum')
).reset_index()

# ── 3. Score each dimension 1-5 (5 = best) ───────────────────────────────────
rfm['R_Score'] = pd.qcut(rfm['Recency'],   5, labels=[5,4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'),  5, labels=[1,2,3,4,5]).astype(int)
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Total'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

# ── 4. Assign named segments ──────────────────────────────────────────────────
def segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'New Customers'
    elif r >= 3 and f >= 2 and m >= 2:
        return 'Potential Loyalists'
    elif r >= 3 and f <= 2 and m <= 2:
        return 'Promising'
    elif r == 2 and f >= 3:
        return 'At Risk'
    elif r == 2 and f <= 2:
        return 'Need Attention'
    elif r <= 2 and f >= 2 and m >= 2:
        return 'About to Sleep'
    elif r == 1 and f >= 2:
        return 'Hibernating'
    else:
        return 'Lost'

rfm['Segment'] = rfm.apply(segment, axis=1)
rfm.to_csv(RFM_PATH, index=False)

# ── 5. Summary ────────────────────────────────────────────────────────────────
summary = rfm.groupby('Segment').agg(
    Customers   = ('Customer ID', 'count'),
    Avg_Recency = ('Recency',     'mean'),
    Avg_Orders  = ('Frequency',   'mean'),
    Total_Rev   = ('Monetary',    'sum')
).sort_values('Total_Rev', ascending=False).reset_index()
summary['Revenue_Pct'] = (summary['Total_Rev'] / summary['Total_Rev'].sum() * 100).round(1)

print("\nRFM Segment Summary:")
print(summary[['Segment','Customers','Avg_Orders','Total_Rev','Revenue_Pct']].to_string(index=False))

# ── 6. Plot A: Customer count by segment (bar) ────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

seg_order = summary.sort_values('Customers', ascending=True)
colors    = [PALETTE.get(s, '#888') for s in seg_order['Segment']]
bars = ax.barh(seg_order['Segment'], seg_order['Customers'], color=colors, edgecolor='none', height=0.6)

for bar, val in zip(bars, seg_order['Customers']):
    ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', ha='left', fontsize=10, color='white', fontweight='bold')

ax.set_xlabel('Number of Customers', color='#aaaaaa', fontsize=11)
ax.set_title('RFM Customer Segmentation\nCustomer Distribution by Segment',
             color='white', fontsize=14, fontweight='bold', pad=15)
ax.tick_params(colors='#aaaaaa')
ax.spines[:].set_visible(False)
ax.xaxis.set_tick_params(color='#333')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'rfm_segment_distribution.png'), dpi=150, bbox_inches='tight',
            facecolor='#0f1117')
plt.close()

# ── 7. Plot B: Revenue contribution by segment (donut) ───────────────────────
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

top = summary.nlargest(6, 'Total_Rev')
others_rev = summary.iloc[6:]['Total_Rev'].sum()
if others_rev > 0:
    top = pd.concat([top, pd.DataFrame([{'Segment': 'Others', 'Total_Rev': others_rev,
                                          'Revenue_Pct': others_rev/summary['Total_Rev'].sum()*100}])])

colors_donut = [PALETTE.get(s, '#888888') for s in top['Segment']]
wedges, texts, autotexts = ax.pie(
    top['Total_Rev'], labels=None,
    colors=colors_donut, autopct='%1.1f%%',
    startangle=90, pctdistance=0.82,
    wedgeprops=dict(width=0.5, edgecolor='#0f1117', linewidth=2)
)
for at in autotexts:
    at.set_color('white'); at.set_fontsize(9); at.set_fontweight('bold')

ax.legend(wedges, [f"{s}" for s in top['Segment']],
          loc='lower center', bbox_to_anchor=(0.5, -0.08),
          ncol=3, frameon=False,
          labelcolor='white', fontsize=10)
ax.set_title('Revenue Contribution by RFM Segment\n(% of £17.4M Total Revenue)',
             color='white', fontsize=14, fontweight='bold', pad=20)
total_txt = f"£{summary['Total_Rev'].sum()/1e6:.1f}M"
ax.text(0, 0, total_txt, ha='center', va='center', fontsize=16, color='white', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'rfm_revenue_by_segment.png'), dpi=150, bbox_inches='tight',
            facecolor='#0f1117')
plt.close()

print(f"\n[02] RFM complete. Segments -> data/rfm_segments.csv | Charts -> outputs/")
