# Monthly Campaign Engine - Quick Start Guide

## ⚡ 30-Second Start

```bash
cd monthly_campaign_engine
python monthly_main.py /path/to/csv/folder
```

That's it! The engine will:
1. Load all monthly CSV files
2. Normalize columns
3. Calculate 6 performance metrics
4. Detect trends and seasonal patterns
5. Identify 17+ performance issues
6. Analyze service coverage
7. Generate 14+ strategic recommendations
8. Export results to JSON

## 📊 What You'll Get

### Console Output
Real-time status updates with:
- Campaign overview (4 campaigns, 7 months, AED 91k spend)
- Performance issues found (11 HIGH severity)
- Service coverage analysis
- Recommendation summary
- Growth opportunities

### JSON Export
Structured report with:
- Complete analysis results
- All detected issues with details
- Strategic recommendations with confidence scores
- Business context analysis
- Timestamped for tracking

## 🚀 Use Cases

### 1. Monthly Performance Review
```bash
python monthly_main.py /data/google-ads-exports
```
Get executive summary of monthly performance and trends

### 2. Integrate with Flask Dashboard
```python
from monthly_main import MonthlyCampaignEngine

@app.route('/api/campaign-analysis')
def analyze():
    engine = MonthlyCampaignEngine()
    results = engine.run_analysis(output_json=False)
    return jsonify(results)
```

### 3. Programmatic Access
```python
from monthly_main import MonthlyCampaignEngine

engine = MonthlyCampaignEngine('/data/exports')
results = engine.run_analysis()

# Access individual analyses
trends = results['trends']
losses = results['losses']
recommendations = results['recommendations']
```

### 4. Automated Monthly Reports
```python
import schedule
from monthly_main import MonthlyCampaignEngine

def monthly_report():
    engine = MonthlyCampaignEngine()
    results = engine.run_analysis(output_json=True)
    # Email results
    send_email(results)

schedule.every().month.do(monthly_report)
```

## 📈 Key Metrics Tracked

- **CTR**: Click-Through Rate (% of impressions that clicked)
- **CVR**: Conversion Rate (% of interactions that converted)
- **CPC**: Cost Per Click (AED per click)
- **CPA**: Cost Per Acquisition (AED per conversion)
- **ROAS**: Return on Ad Spend (revenue multiplier)
- **Spend Share**: Budget distribution across campaigns

## 🎯 Analysis Dimensions

### Trends
- Growth trends (GROWING/DECLINING/FLAT)
- Seasonal patterns (peak/low months)
- Volatility measurement (STABLE/MODERATE/UNSTABLE)
- Month-over-month changes

### Losses Detected
- Spend-Conversion mismatch (spend up but conversions down)
- Declining efficiency (CPA increasing 30%+)
- Sudden drops (CTR/CVR decrease 50%+)
- High spend, low ROI (ROAS < 1.0)
- Inactive campaigns (zero activity)

### Business Intelligence
- Service coverage analysis (6 services mapped)
- Platform budget alignment (Search, PMax, Android, iOS)
- High-performing services
- Service gaps and opportunities

### Recommendations
- Budget increase/decrease suggestions
- Loss remediation actions (pause, optimize, refresh)
- Campaign scaling opportunities
- Strategic initiatives

## 📁 File Structure

```
monthly_campaign_engine/
├── file_loader.py          # Load CSV files
├── column_mapper.py        # Normalize columns
├── metrics_engine.py       # Calculate metrics
├── trend_analyzer.py       # Detect trends
├── loss_detector.py        # Find issues
├── business_context.py     # Service analysis
├── recommendation_engine.py# Generate recommendations
├── monthly_main.py         # Orchestration
├── README.md               # Full documentation
└── IMPLEMENTATION_COMPLETE.md # Implementation details
```

## 🔍 Sample Analysis Results

### Executive Summary
```
📊 CAMPAIGN OVERVIEW:
   • Total Campaigns: 4
   • Months Analyzed: 7
   • Total Spend: AED 91,031.55
   • Total Conversions: 7,256
   • Average ROI (ROAS): 0.03x

⚠️  PERFORMANCE ISSUES DETECTED:
   • High Severity: 11
   • Total Issues: 17

🎯 SERVICE COVERAGE:
   • Balanced Services: 0
   • Missing Services: 6

💡 RECOMMENDATIONS:
   • Total Actions: 14
   • Critical: 8
   • High Priority: 2
   • Medium Priority: 4
```

## 🛠️ Customization

### Change CSV Directory
```python
engine = MonthlyCampaignEngine('/my/custom/path')
results = engine.run_analysis()
```

### Control Output
```python
# JSON only (no console output)
engine.run_analysis(output_json=True, output_console=False)

# Console only (no JSON export)
engine.run_analysis(output_json=False, output_console=True)

# Both
engine.run_analysis(output_json=True, output_console=True)
```

### Individual Module Access
```python
from file_loader import MonthlyFileLoader
from column_mapper import ColumnMapper
from metrics_engine import MetricsEngine

# Use individual modules
loader = MonthlyFileLoader('/path')
df = loader.combine_all_months()

mapper = ColumnMapper(df)
normalized_df, _ = mapper.map_and_clean()

metrics = MetricsEngine(normalized_df)
metrics_df = metrics.calculate_all_metrics()
```

## 📝 CSV Format

Supports Google Ads export format:
- Filename: "MonthName Year.csv" (e.g., "Mar 2025.csv")
- Supports both old and new column names
- Automatically filters metadata and summary rows

## ✅ System Requirements

- Python 3.8+
- pandas
- numpy

Install dependencies:
```bash
pip install pandas numpy
```

## 🐛 Troubleshooting

**Issue**: No CSV files found
- ✅ Check directory path
- ✅ Verify CSV filenames follow "MonthName Year.csv" pattern
- ✅ Example: "Mar 2025.csv", "Apr 2025.csv"

**Issue**: Column not found
- ✅ Automatic - mapper handles most Google Ads variations
- ✅ Check CSV file has valid data rows
- ✅ Review README.md for supported column names

**Issue**: Empty dataframe
- ✅ Verify CSV has campaign data (not just headers)
- ✅ Check rows aren't filtered as "Total:" rows

## 📚 Documentation

- **README.md** - Complete module documentation
- **IMPLEMENTATION_COMPLETE.md** - Implementation details
- **This file** - Quick start guide

## 🚀 Next Steps

1. **Run Analysis**
   ```bash
   python monthly_main.py /path/to/exports
   ```

2. **Review Results**
   - Check console output for key insights
   - Review JSON file for complete analysis

3. **Take Action**
   - Implement top 3 recommendations
   - Track performance improvements
   - Schedule monthly analysis

4. **Integrate Further** (Optional)
   - Connect to Streamlit dashboard
   - Add Flask API endpoint
   - Set up email reporting

## 📧 Support

For questions or issues:
1. Check README.md for detailed documentation
2. Review IMPLEMENTATION_COMPLETE.md for architecture
3. Check individual module docstrings
4. Review test_monthly_engine.py for examples

---

**Status**: ✅ Production Ready
**Last Updated**: December 2024
**For**: Champion Cleaners UAE
