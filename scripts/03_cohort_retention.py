"""
03_cohort_retention.py
Customer Intelligence & Revenue Analytics
----------------------------------------------
Builds a monthly cohort retention matrix and plots a heatmap.
Each cohort = customers who made their FIRST purchase in a given month.
Retention % = how many of them transacted again N months later.

Input  : data/cleaned_transactions.csv
Outputs: data/cohort_retention_matrix.csv
         outputs/cohort_retention_heatmap.png
         outputs/cohort_avg_retention_curve.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os

CLEAN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_transactions.csv')
OUT_DIR    = os.path.join(os.path.dirname(__file__), '..', 'outputs')
DATA_DIR   = os.path.join(os.path.dirname(__file__), '..', 'data')

# ── 1. Load & derive cohort month ────────────────────────────────────────────
df = pd.read_csv(CLEAN_PATH, parse_dates=['InvoiceDate'])
df['OrderMonth']  = df['InvoiceDate'].dt.to_period('M')

cohort_map = df.groupby('Customer ID')['OrderMonth'].min().rename('CohortMonth')
df = df.merge(cohort_map, on='Customer ID')
df['CohortIndex'] = (df['OrderMonth'].astype(int) - df['CohortMonth'].astype(int))

# ── 2. Build retention matrix ─────────────────────────────────────────────────
cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['Customer ID'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='Customer ID')

# Cohort sizes (month 0 = acquisition)
cohort_sizes = cohort_pivot.iloc[:, 0]
retention    = cohort_pivot.divide(cohort_sizes, axis=0) * 100
retention    = retention.round(1)

# Keep only cohorts with enough follow-up data (first 24 months)
retention = retention.iloc[:, :24]

# Save
retention.to_csv(os.path.join(DATA_DIR, 'cohort_retention_matrix.csv'))

# ── 3. Plot A: Retention Heatmap ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

# Only show cohorts that have at least 3 months of data
plot_ret = retention.dropna(thresh=3).copy()
matrix   = plot_ret.values.astype(float)

# Custom green colormap
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('ret', ['#1a1a2e', '#16213e', '#0f3460', '#1a7a4a', '#2ecc71'])

im = ax.imshow(matrix, aspect='auto', cmap=cmap, vmin=0, vmax=100)

# Annotate cells
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        if not np.isnan(val):
            color = 'white' if val < 60 else '#0f1117'
            weight = 'bold' if j == 0 else 'normal'
            ax.text(j, i, f'{val:.0f}%', ha='center', va='center',
                    fontsize=7.5, color=color, fontweight=weight)

ax.set_xticks(range(matrix.shape[1]))
ax.set_xticklabels([f'M+{i}' for i in range(matrix.shape[1])],
                   color='#aaaaaa', fontsize=9)
ax.set_yticks(range(len(plot_ret.index)))
ax.set_yticklabels([str(c) for c in plot_ret.index],
                   color='#aaaaaa', fontsize=9)

ax.set_xlabel('Months Since First Purchase', color='#aaaaaa', fontsize=11, labelpad=10)
ax.set_ylabel('Cohort (Acquisition Month)', color='#aaaaaa', fontsize=11, labelpad=10)
ax.set_title('Monthly Cohort Retention Matrix\n% of Customers Active N Months After Acquisition',
             color='white', fontsize=14, fontweight='bold', pad=15)
ax.spines[:].set_visible(False)
ax.tick_params(length=0)

cbar = plt.colorbar(im, ax=ax, fraction=0.02, pad=0.01)
cbar.ax.tick_params(colors='#aaaaaa')
cbar.set_label('Retention %', color='#aaaaaa')

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'cohort_retention_heatmap.png'), dpi=150,
            bbox_inches='tight', facecolor='#0f1117')
plt.close()
print("  Heatmap saved.")

# ── 4. Plot B: Average retention curve ───────────────────────────────────────
avg_ret = retention.mean(axis=0).dropna()

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#111827')

x = avg_ret.index.astype(int)
y = avg_ret.values

ax.fill_between(x, y, alpha=0.25, color='#2ecc71')
ax.plot(x, y, color='#2ecc71', linewidth=2.5, marker='o', markersize=5)

for xi, yi in zip(x[::3], y[::3]):
    ax.annotate(f'{yi:.1f}%', (xi, yi), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=9, color='#2ecc71')

ax.set_xlim(0, len(x)-1)
ax.set_ylim(0, 110)
ax.set_xlabel('Months Since First Purchase', color='#aaaaaa', fontsize=11)
ax.set_ylabel('Avg Retention Rate (%)',      color='#aaaaaa', fontsize=11)
ax.set_title('Average Customer Retention Curve\nAcross All Acquisition Cohorts',
             color='white', fontsize=14, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.tick_params(colors='#aaaaaa')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#333')
ax.spines['bottom'].set_color('#333')
ax.grid(axis='y', color='#222', linewidth=0.8)

# Highlight M+1 and M+3 drop
ax.axvline(1, color='#e74c3c', linestyle='--', linewidth=1, alpha=0.6)
ax.axvline(3, color='#f39c12', linestyle='--', linewidth=1, alpha=0.6)
ax.text(1.1, 95, 'M+1 Drop', color='#e74c3c', fontsize=9)
ax.text(3.1, 95, 'M+3 Stabilisation', color='#f39c12', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'cohort_avg_retention_curve.png'), dpi=150,
            bbox_inches='tight', facecolor='#0f1117')
plt.close()
print("  Retention curve saved.")

print(f"\n  Avg M+1 retention : {avg_ret.get(1, float('nan')):.1f}%")
print(f"  Avg M+3 retention : {avg_ret.get(3, float('nan')):.1f}%")
print(f"  Avg M+12 retention: {avg_ret.get(12, float('nan')):.1f}%")
print(f"\n[03] Cohort analysis complete.")
