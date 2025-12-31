# Keyword Intelligence Engine V2 - Analysis Output Guide

## Overview
When you upload the **website traffic 2 keywords.csv** file, the system now performs a comprehensive 7-step analysis and provides the following detailed insights:

---

## 1. KEYWORD AUDIT (Deep CSV Analysis)
**What it detects:**
- Keywords with high impressions but zero clicks (engagement failure)
- Keywords with clicks but zero conversions (funnel leakage)
- Low Click-Through Rate (CTR) keywords
- High Cost Per Acquisition (CPA) keywords
- Low Return On Ad Spend (ROAS)
- High-spend keywords with minimal conversions

**Example Output:**
```
Keyword: "dry clean near me"
Campaign: DC_SEARCH_1
Issue Type: HIGH_SPEND_LOW_RETURN
Severity: High
Description: High spend (AED 1850.00) with minimal conversions (1)
Recommendation: Review keyword relevance or pause if unprofitable
```

---

## 2. LOST SEARCHES & DEMAND GAP DETECTION
**What it identifies:**
- High-impression keywords with low engagement (lost clicks)
- Keywords getting traffic but no conversions (landing page mismatch)
- Match type coverage gaps (broad exists but exact doesn't)
- Unmatched search intent

**Example Output:**
```
Keyword: "upholstery cleaning dubai"
Loss Type: CLICK_NO_CONVERSION
Severity: High
Description: Getting 18 clicks but zero conversions - funnel issue
Potential Lost Searches: 18
Recommendation: Check landing page relevance or adjust targeting
```

---

## 3. MATCH TYPE INTELLIGENCE
**What it analyzes:**
- Current match type performance (exact vs. phrase vs. broad)
- Conversion rate by match type
- Cost efficiency by match type
- Recommended conversions

**Example Output:**
```
Keyword: "express laundry"
Current Match Type: Broad
Recommended Match Type: Exact
Current Performance: 22 clicks, 2 conversions (CVR: 9.09%)
Expected Impact: Higher conversion rate, better CPA
Confidence: High
Action: Convert to Exact match
Reason: Broad match converting well - should be exact for better control
```

---

## 4. WEBSITE & SERVICE ALIGNMENT CHECK
**What it validates:**
- Keywords align with actual services offered
- Service pages have adequate keyword coverage
- Landing page relevance to keywords
- Uncovered services or overrepresented keywords

**Example Output:**
```
Service Analysis:
- Dry Cleaning: 8 keywords (WELL_COVERED)
- Laundry: 12 keywords (WELL_COVERED)
- Carpet Cleaning: 6 keywords (COVERED)
- Curtain Cleaning: 5 keywords (COVERED)
- Sofa Cleaning: 4 keywords (MINIMAL)
- Corporate Services: 3 keywords (MINIMAL)

Alignment Status: 29 of 30 keywords are well-aligned with services
```

---

## 5. CUSTOMER LOSS SIGNALS
**What it flags:**
- High CTR but no conversions (landing page mismatch)
- High impressions but low engagement (ad copy issue)
- Keywords with declining performance metrics
- Funnel leakage points

**Example:**
```
"furniture cleaning dubai" (Broad match)
- Getting 15 clicks
- Zero conversions
- Status: LANDING PAGE MISMATCH
- Fix: Ensure landing page matches "furniture cleaning" intent
```

---

## 6. MARKET & SEARCH TREND INFERENCE
**What it identifies:**
- Trending service themes in your keyword base
- Seasonal or growing keywords
- Location + service combinations
- Service gaps with no keyword coverage

**Example Output:**
```
Trending Themes:
1. "express/same-day" services (3 keywords)
2. Location-based searches (10+ keywords with "dubai", "near me")
3. Service-specific cleaning (carpet, curtain, sofa)

Identified Gaps:
- No keywords for "eco-friendly laundry"
- Limited coverage for "corporate laundry"
- Missing "mattress cleaning" keywords
```

---

## 7. ACTIONABLE RECOMMENDATIONS
**What it generates:**
- Prioritized action items (High/Medium/Low)
- Specific campaigns and keywords to fix
- Expected business impact
- Implementation steps

**Example Output:**
```
High Priority Actions:
1. [PAUSE] "dry clean near me" (Broad)
   - Spend: AED 1,850
   - Conversions: 1 (extremely high CPA)
   - Impact: Save AED 1,850+/month

2. [CONVERT] "express laundry" (Broad → Exact)
   - Current: 22 clicks, 2 conversions
   - Expected: +3-5 conversions/month
   - Reason: Performing well but losing to broad match variations

3. [ADD] New Exact match keywords
   - "premium laundry dubai" (Exact)
   - "same-day dry cleaning" (Exact)
   - "professional laundry service" (Exact)
   - Expected impact: +15-20 conversions/month

4. [REVIEW] Landing pages for:
   - Furniture cleaning
   - Wedding dress cleaning
   - Carpet cleaning categories
```

---

## Summary Metrics Provided

| Metric | Purpose |
|--------|---------|
| Total Keywords | Total keywords in your portfolio |
| Keywords with Issues | Count of underperforming keywords |
| Lost Search Opportunities | Potential customers not converting |
| Match Type Conversions | Recommended changes from broad to exact |
| New Keywords Suggested | Gaps identified for new keyword additions |
| Total Recommendations | Number of actionable items |

---

## How the Output is Displayed

The web interface organizes results into **6 tabs**:

1. **Summary** - Key metrics at a glance
2. **Keyword Audit** - Health issues detected
3. **Lost Searches** - Demand gaps and funnel issues
4. **Match Types** - Current vs. recommended match types
5. **Alignment** - Website-keyword alignment analysis
6. **Recommendations** - Prioritized action plan

---

## Next Steps After Analysis

### For High Priority Issues:
1. Pause low-converting, high-cost keywords
2. Convert broad match keywords to exact match
3. Review landing pages for misaligned keywords

### For Growth Opportunities:
1. Add suggested new keywords (exact match)
2. Create targeted ads for underserved services
3. Optimize budget allocation to high-performing services

### For Ongoing Optimization:
1. Implement recommended changes
2. Monitor performance for 2-3 weeks
3. Re-run analysis monthly to track improvements

---

## Support & Questions

All analysis is based on:
- ✅ Actual performance data from your CSV
- ✅ Champion Cleaners' service offerings
- ✅ Industry best practices for SEM
- ✅ Intent matching and user behavior patterns

The engine combines multiple AI models to provide business-focused recommendations prioritized by expected impact on sales.
