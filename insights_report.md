# EXECUTIVE STRATEGIC REPORT: CUSTOMER INTELLIGENCE & REVENUE ANALYTICS
**Project Title:** Customer Intelligence & Revenue Analytics: RFM Segmentation, Cohort Retention & Growth Intelligence Pipeline
**Reporting Period:** Dec 2009 – Dec 2011  |  **Analysis Framework:** RFM · Cohort · LTV · Market Intelligence

---

## 1. Executive Summary

An end-to-end analytics pipeline was executed across two years of real transactional data from a UK-based online gift-ware retailer operating across 41 countries. The pipeline evaluated **802,932** transactions representing **£17,451,756** in total revenue across 5,862 unique customers and 36,645 invoices.

| KPI | Value |
|-----|-------|
| Total Transactions Analysed | 802,932 |
| Total Portfolio Revenue | £17,451,756 |
| Unique Customers | 5,862 |
| Total Invoices | 36,645 |
| Average Order Value | £476.24 |
| Countries | 41 |
| Cancelled Transactions (separated) | 19,494 |
| Analysis Modules | 4 (RFM · Cohort · LTV · Market Intelligence) |
| MySQL Queries Executed | 7 |

---

## 2. RFM Segment Performance

| Segment | Customers | Avg Recency (Days) | Avg Orders | Avg Rev / Customer | Total Revenue | Revenue Share |
|---------|-----------|-------------------|-----------|-------------------|---------------|---------------|
| Champions | 1,297 | 20 | 17.0 | £9,204 | £11,937,871 | 68.4% |
| Loyal Customers | 1,123 | 73 | 5.9 | £2,239 | £2,514,864 | 14.4% |
| At Risk | 551 | 302 | 5.3 | £2,164 | £1,192,697 | 6.8% |
| About to Sleep | 466 | 512 | 3.2 | £1,294 | £603,312 | 3.5% |
| New Customers | 451 | 28 | 1.5 | £930 | £419,034 | 2.4% |
| Need Attention | 618 | — | 1.3 | £440 | £271,969 | 1.6% |
| Lost | 593 | — | 1.2 | £362 | £214,740 | 1.2% |
| Potential Loyalists | 355 | — | 2.7 | £600 | £213,051 | 1.2% |
| Promising | 211 | — | 1.1 | £238 | £50,283 | 0.3% |
| Hibernating | 197 | — | 1.4 | £172 | £33,936 | 0.2% |
| **Total** | **5,862** | | | | **£17,451,757** | **100%** |

**Highest revenue concentration:** Champions (1,297 customers, 22% of base) generated £11.9M at an average of 17 orders per customer and avg recency of 20 days — indicating a highly active, high-value cohort with strong purchasing habit.

**Highest risk:** At Risk (551 customers, avg 302 days inactive) and About to Sleep (466 customers, avg 512 days inactive) together represent **£1,795,009** in historical revenue now at risk of permanent loss.

---

## 3. Cohort Retention Analysis

| Metric | Value |
|--------|-------|
| Avg M+1 Retention | 21.0% |
| Avg M+3 Retention | 21.7% |
| Avg M+12 Retention | 18.2% |
| Retention Stabilisation Point | Month 3 |
| Customers Lost After First Purchase | ~79% |

**Key pattern:** 79% of new customers do not return after their first purchase. Retention drops sharply after M+1, then stabilises from M+3 onwards at 18–22%. Customers who transact again within 3 months demonstrate consistent long-term behaviour — indicating a clear activation threshold that intervention programmes should target.

**Implication:** Acquisition spend is being wasted for 4 in 5 new buyers. A 5-point improvement in M+1 retention (21% to 26%) recovers approximately 290 additional retained customers per cohort without any additional acquisition spend.

---

## 4. Market Intelligence — UK vs International

### Year-over-Year Revenue Growth

| Region | Revenue 2010 | Revenue 2011 | YoY Revenue Growth | Customers 2010 | Customers 2011 | YoY Customer Growth |
|--------|-------------|-------------|-------------------|---------------|---------------|---------------------|
| United Kingdom | £7,246,698 | £6,768,934 | -6.6% | 3,873 | 3,808 | -1.7% |
| International | £1,323,817 | £1,430,778 | +8.1% | 344 | 406 | +18.0% |

### Top International Markets (ex-UK)

| Rank | Country | Total Revenue | Customers | Revenue / Customer | Avg Order Value |
|------|---------|--------------|-----------|-------------------|-----------------|
| 1 | EIRE | £602,058 | 5 | £120,412 | £1,111 |
| 2 | Netherlands | £549,953 | 22 | £24,998 | £2,546 |
| 3 | Germany | £388,960 | 107 | £3,636 | £515 |
| 4 | France | £315,714 | 95 | £3,323 | £532 |
| 5 | Australia | £168,485 | 15 | £11,232 | £1,893 |
| 6 | Spain | £77,759 | 31 | £2,508 | £425 |
| 7 | Switzerland | £73,285 | 12 | £6,107 | £874 |

**Note:** UK is excluded from the country chart — at £14M it dwarfs all other markets and makes international breakdowns unreadable. UK vs International comparison is in the YoY table above.

---

## 5. Product Performance — Top 10 by Revenue

| Rank | Product | Orders | Units Sold | Total Revenue | Avg Unit Price |
|------|---------|--------|-----------|---------------|----------------|
| 1 | REGENCY CAKESTAND 3 TIER | 3,317 | 56,630 | £286,486 | £12.75 |
| 2 | WHITE HANGING HEART T-LIGHT HOLDER | 5,055 | 96,893 | £247,931 | £2.55 |
| 3 | JUMBO BAG RED RETROSPOT | 3,146 | 93,925 | £232,989 | £2.08 |
| 4 | PARTY BUNTING | 2,426 | 67,860 | £224,413 | £4.95 |
| 5 | RABBIT NIGHT LIGHT | 2,303 | 49,649 | £216,756 | £9.95 |
| 6 | LUNCH BAG RED RETROSPOT | 2,736 | 81,022 | £185,085 | £1.65 |
| 7 | PAPER CRAFT, LITTLE BIRDIE | 74 | 80,995 | £168,470 | £2.08 |
| 8 | MEDIUM CERAMIC TOP STORAGE JAR | 1,561 | 77,028 | £152,814 | £1.25 |
| 9 | REGENCY CAKESTAND CHRISTMAS | 876 | 17,640 | £145,059 | £10.95 |
| 10 | SMALL POPCORN HOLDER | 2,196 | 59,476 | £140,044 | £1.25 |

**Top 20 SKUs account for approximately 28% of total revenue.** The top 5 share the same profile — high order frequency, broad customer reach, moderate unit price. A stockout on any of these would have an immediate and measurable revenue impact.

---

## 6. Peak Trading Patterns

| Day | Revenue | Share of Weekly Revenue |
|-----|---------|------------------------|
| Thursday | £3,790,000 | 25.3% |
| Tuesday | £3,330,000 | 22.2% |
| Wednesday | £3,080,000 | 20.5% |
| Monday | £2,750,000 | 18.3% |
| Friday | £2,690,000 | 17.9% |
| Sunday | £1,810,000 | — (low) |
| Saturday | £10,000 | negligible |

**Peak hour:** Wednesday 12:00 — £545,977 single-hour revenue. Weekend trading is negligible (Saturday: 0.3% of weekly revenue), consistent with a predominantly B2B wholesale buyer base operating on business hours.

---

## 7. Strategic Recommendations

### Rec 1 — Launch Champions Retention Programme
- **Finding:** 1,297 Champions generate £11.9M (68.4% of revenue) with avg recency of 20 days. A 10% churn in this segment eliminates more revenue than all Lost + Hibernating + Promising customers combined.
- **Recommendation:** Assign dedicated account management to top 100 customers by LTV (threshold: £50K+). Set automated frequency-drop alerts — trigger win-back outreach when any Champion's order cadence falls below their 90-day baseline.
- **Impact:** Protect £11,937,871 revenue base

### Rec 2 — Deploy M+1 Re-Engagement Sequence
- **Finding:** 79% of new customers do not return after first purchase. Avg M+1 retention of 21.0% means acquisition spend is wasted for 4 in 5 new buyers.
- **Recommendation:** Introduce a 30-day post-purchase re-engagement sequence (email on day 7, 14, 28) with category-matched offers. Surface products purchased by retained M+1 customers in post-purchase communications.
- **Impact:** A 5-point improvement (21% to 26%) recovers ~290 additional retained customers per cohort

### Rec 3 — Execute At Risk Win-Back Campaign Within 30 Days
- **Finding:** 551 At Risk (avg 302 days inactive) + 466 About to Sleep (avg 512 days inactive) = £1,795,009 in recoverable revenue.
- **Recommendation:** Personalised win-back campaign segmented by last-purchased product category. Time-limited offer (14-day expiry) before customers migrate to Lost.
- **Impact:** 15% reactivation rate = 83 customers recovered = ~£179,000

### Rec 4 — Activate International B2B Sales Motion
- **Finding:** UK revenue declined 6.6% YoY. International grew 8.1% with customer base expanding 18.0%. EIRE (£120,412/customer) and Netherlands (£24,998/customer) are clearly wholesale accounts.
- **Recommendation:** Structured B2B sales motion for EIRE, Netherlands, and Australia — volume pricing tiers, annual contract options, preferred delivery SLAs. Replicate model to Switzerland (£6,107/customer, 12 accounts).
- **Impact:** International growing at 8.1% YoY; dedicated B2B coverage projected to accelerate to 12–15%

### Rec 5 — Align Campaigns to Peak Trading Window
- **Finding:** Thursday drives 25.3% of weekly revenue. Wednesday 12:00 is the single highest-revenue hour (£545,977). Saturday generates just 0.3% of weekly revenue.
- **Recommendation:** All email campaigns and product launches to land by 09:30 Tuesday or Wednesday. Customer service staffing peaks aligned to 10:00–14:00 Mon–Thu. Sub-1-hour order acknowledgement SLA during peak window.
- **Impact:** Measurable improvement in campaign open rates and order processing speed

### Rec 6 — Classify Top 20 SKUs as Tier 1 Inventory
- **Finding:** Top 20 products by revenue account for 28% of total revenue. REGENCY CAKESTAND 3 TIER: £286,486 from 3,317 orders. All top-5 SKUs share high order frequency + broad customer reach.
- **Recommendation:** Classify top 20 as Tier 1 SKUs with dedicated inventory buffers, preferred supplier contracts, and automated reorder triggers at 30% stock remaining.
- **Impact:** Prevents stockout-driven revenue loss on highest-value SKUs

---

## 8. Projected Impact Matrix

| Recommendation | Segment / Area | Revenue at Stake | Expected Outcome |
|---------------|---------------|-----------------|-----------------|
| Champions Retention | 1,297 customers | £11,937,871 base | Risk protection |
| M+1 Re-Engagement | New Customers (451) | ~290 retained/cohort | +5pp M+1 retention |
| At Risk Win-Back | 1,017 customers | £1,795,009 recoverable | 15% reactivation = £179K |
| International B2B | Netherlands + EIRE + AUS | £1,320,495 intl base | +12–15% YoY growth |
| Campaign Scheduling | All segments | Full revenue base | Engagement uplift |
| Tier 1 SKU Protection | Top 20 products | 28% of £17.5M | Stockout prevention |

---

## 9. Next Steps

1. **Week 1–2:** Activate Champions frequency-drop alerts; identify top 100 by LTV for account assignment
2. **Week 2–3:** Build M+1 re-engagement email sequence; define product-category targeting logic
3. **Month 1:** Deploy At Risk win-back campaign with 14-day expiry offer
4. **Month 1–2:** Engage Netherlands and EIRE accounts with B2B pricing proposal
5. **Month 2:** Reclassify top 20 SKUs as Tier 1; set automated reorder triggers
6. **Ongoing:** Re-run RFM pipeline monthly; track segment migration rates and retention curve

---

*Dashboard: `outputs/power_bi_dashboard.png`*
*Cohort Matrix: `outputs/cohort_retention_heatmap.png`*
*Full SQL Query Suite: `scripts/05_mysql_analytics.sql`*
*Pipeline: RFM · Cohort · LTV · Market Intelligence | Dec 2009 – Dec 2011*
*Dataset: UCI Online Retail II — Chen, D. (2012). DOI: 10.24432/C5CG6D | CC BY 4.0*
