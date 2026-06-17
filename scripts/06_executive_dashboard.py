"""
06_executive_dashboard.py
Customer Intelligence & Revenue Analytics
----------------------------------------------
Generates individual chart exports for Power BI and presentation use.

Input  : outputs/q*.csv  (produced by 05_run_analytics.py)
Outputs: outputs/chart_revenue_trend.png
         outputs/chart_country_performance.png
         outputs/chart_peak_hours_heatmap.png
         outputs/chart_top_products.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import numpy as np
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')

BG       = '#0f1117'
PANEL    = '#1a1d27'
GREEN    = '#2ecc71'
BLUE     = '#3498db'
ORANGE   = '#e67e22'
RED      = '#e74c3c'
PURPLE   = '#9b59b6'
GREY     = '#aaaaaa'
WHITE    = 'white'

def styled_ax(ax, title='', xlabel='', ylabel=''):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=GREY, labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#333')
    ax.spines['bottom'].set_color('#333')
    ax.grid(axis='y', color='#252535', linewidth=0.8)
    if title:   ax.set_title(title,   color=WHITE,  fontsize=11, fontweight='bold', pad=10)
    if xlabel:  ax.set_xlabel(xlabel, color=GREY,   fontsize=9)
    if ylabel:  ax.set_ylabel(ylabel, color=GREY,   fontsize=9)

# ── Load query results ────────────────────────────────────────
q1  = pd.read_csv(os.path.join(OUT_DIR, 'q1_monthly_revenue.csv'))
q2  = pd.read_csv(os.path.join(OUT_DIR, 'q2_country_performance.csv'))
q3  = pd.read_csv(os.path.join(OUT_DIR, 'q3_top_products.csv'))
q5  = pd.read_csv(os.path.join(OUT_DIR, 'q5_peak_hours.csv'))
q7  = pd.read_csv(os.path.join(OUT_DIR, 'q7_segment_summary.csv'))
q8  = pd.read_csv(os.path.join(OUT_DIR, 'q8_yoy_growth.csv'))
rfm = pd.read_csv(os.path.join(OUT_DIR.replace('outputs','data'), 'rfm_segments.csv'))

# ════════════════════════════════════════════════════════════
# CHART 1: Monthly Revenue Trend (standalone)
# ════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 5))
fig.patch.set_facecolor(BG)
styled_ax(ax, 'Monthly Revenue Trend (Dec 2009 – Dec 2011)',
          'Month', 'Revenue (£)')

x = range(len(q1))
ax.fill_between(x, q1['Total_Revenue'], alpha=0.18, color=GREEN)
ax.plot(x, q1['Total_Revenue'], color=GREEN, linewidth=2.5, marker='o', markersize=4)

# Annotate peak
peak_idx = q1['Total_Revenue'].idxmax()
ax.annotate(f"Peak: £{q1.loc[peak_idx,'Total_Revenue']/1e3:.0f}K",
            (peak_idx, q1.loc[peak_idx,'Total_Revenue']),
            xytext=(peak_idx-3, q1.loc[peak_idx,'Total_Revenue']*1.05),
            fontsize=9, color=GREEN,
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

ax.set_xticks(list(x)[::3])
ax.set_xticklabels(q1['YearMonth'].iloc[::3], rotation=45, ha='right')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f'£{v/1e3:.0f}K'))
ax.set_xlim(0, len(q1)-1)

# Add MoM growth line (secondary axis)
ax2 = ax.twinx()
ax2.set_facecolor(PANEL)
valid = q1.dropna(subset=['MoM_Growth_Pct'])
ax2.bar(valid.index, valid['MoM_Growth_Pct'],
        color=[GREEN if v>=0 else RED for v in valid['MoM_Growth_Pct']],
        alpha=0.35, width=0.6)
ax2.axhline(0, color='#555', linewidth=0.8)
ax2.set_ylabel('MoM Growth %', color=GREY, fontsize=9)
ax2.tick_params(colors=GREY, labelsize=8)
ax2.spines[:].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_revenue_trend.png'),
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  chart_revenue_trend.png saved")

# ════════════════════════════════════════════════════════════
# CHART 2: Country Performance (top 10 ex-UK)
# ════════════════════════════════════════════════════════════
fig, (ax_rev, ax_rpc) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor(BG)

top10 = q2.head(10).sort_values('Total_Revenue')
colors_bar = [BLUE if i < 7 else ORANGE for i in range(len(top10))]

# Revenue
styled_ax(ax_rev, 'Revenue by Country (ex-UK, Top 10)', '', 'Country')
bars = ax_rev.barh(top10['Country'], top10['Total_Revenue'],
                   color=colors_bar, edgecolor='none', height=0.6)
for bar, val in zip(bars, top10['Total_Revenue']):
    ax_rev.text(bar.get_width() + 2000, bar.get_y() + bar.get_height()/2,
                f'£{val/1e3:.0f}K', va='center', fontsize=8.5, color=WHITE, fontweight='bold')
ax_rev.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f'£{v/1e3:.0f}K'))
ax_rev.tick_params(axis='y', colors=WHITE)

# Revenue per customer
styled_ax(ax_rpc, 'Revenue per Customer by Country', '', '')
bars2 = ax_rpc.barh(top10['Country'], top10['Revenue_Per_Customer'],
                    color=PURPLE, edgecolor='none', height=0.6, alpha=0.85)
for bar, val in zip(bars2, top10['Revenue_Per_Customer']):
    ax_rpc.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
                f'£{val:,.0f}', va='center', fontsize=8.5, color=WHITE, fontweight='bold')
ax_rpc.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f'£{v:,.0f}'))
ax_rpc.tick_params(axis='y', colors=WHITE)

plt.suptitle('International Market Performance', color=WHITE, fontsize=13,
             fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_country_performance.png'),
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  chart_country_performance.png saved")

# ════════════════════════════════════════════════════════════
# CHART 3: Peak Hours Heatmap
# ════════════════════════════════════════════════════════════
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot_hrs  = q5.pivot_table(index='DayOfWeek', columns='Hour',
                             values='Revenue', aggfunc='sum')
pivot_hrs  = pivot_hrs.reindex([d for d in day_order if d in pivot_hrs.index])

fig, ax = plt.subplots(figsize=(16, 5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

from matplotlib.colors import LinearSegmentedColormap
cmap2 = LinearSegmentedColormap.from_list('hrs', [BG, '#0f3460', BLUE, GREEN])
im = ax.imshow(pivot_hrs.values, aspect='auto', cmap=cmap2)

for i in range(pivot_hrs.shape[0]):
    for j in range(pivot_hrs.shape[1]):
        val = pivot_hrs.values[i, j]
        if not np.isnan(val):
            ax.text(j, i, f'£{val/1e3:.0f}K', ha='center', va='center',
                    fontsize=7, color=WHITE if val > pivot_hrs.values.mean() else GREY)

ax.set_xticks(range(pivot_hrs.shape[1]))
ax.set_xticklabels([f'{h:02d}:00' for h in pivot_hrs.columns], color=GREY, fontsize=8, rotation=45)
ax.set_yticks(range(len(pivot_hrs.index)))
ax.set_yticklabels(pivot_hrs.index, color=WHITE, fontsize=9)
ax.set_title('Peak Trading Hours Heatmap — Revenue by Day & Hour',
             color=WHITE, fontsize=13, fontweight='bold', pad=12)
ax.spines[:].set_visible(False)
ax.tick_params(length=0)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_peak_hours_heatmap.png'),
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  chart_peak_hours_heatmap.png saved")

# ════════════════════════════════════════════════════════════
# CHART 4: Top 15 Products
# ════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor(BG)
styled_ax(ax, 'Top 15 Products by Total Revenue', 'Revenue (£)', '')

top15 = q3.head(15).sort_values('Total_Revenue')
short_desc = top15['Description'].str[:35]
bar_colors = [GREEN if i >= 10 else BLUE for i in range(len(top15))]
bars = ax.barh(short_desc, top15['Total_Revenue'], color=bar_colors,
               edgecolor='none', height=0.65)
for bar, val in zip(bars, top15['Total_Revenue']):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f'£{val/1e3:.0f}K', va='center', fontsize=8.5, color=WHITE, fontweight='bold')
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f'£{v/1e3:.0f}K'))
ax.tick_params(axis='y', colors=WHITE, labelsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'chart_top_products.png'),
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  chart_top_products.png saved")

