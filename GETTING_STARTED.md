# 🚀 Getting Started - Champion Cleaners Bot

## Welcome! 👋

Your AI-powered Google Ads decision-support bot is ready to use. This guide will get you started in 5 minutes.

---

## ⚡ 5-Minute Quick Start

### 1. Verify Environment (30 seconds)
Your virtual environment is already active. Just confirm:
```bash
.\.venv\Scripts\python.exe --version
```
Expected: Python 3.14.x

### 2. Run Demo Analysis (2 minutes)
```bash
python main_windows.py sample_data.csv
```

This analyzes our test data with 5 campaigns across 3 platforms.

### 3. Review Output (2 minutes)
- Read the console recommendations
- Note which campaigns need optimization
- Review the budget allocation suggestions

### 4. Export Results (30 seconds)
```bash
python main_windows.py sample_data.csv --output my_analysis.json
```

Open `my_analysis.json` to see the structured output.

---

## 📊 What You're Looking At

### The Bot Analyzes:
- **Campaign Performance**: CTR, CPA, ROAS, conversion rates
- **Platform Performance**: Search vs Display vs App
- **Device Performance**: iOS vs Android vs Web
- **Issues**: High CPA, low CTR, poor ROAS, etc.
- **Opportunities**: Which campaigns to scale, where to optimize

### The Bot Recommends:
- **How to improve each campaign**
- **How to reallocate your budget**
- **What to optimize (copy, landing page, targeting)**
- **Which campaigns to scale**

---

## 📈 Understanding the Output

### Key Metrics

**CTR (Click-Through Rate)**
- Formula: Clicks ÷ Impressions
- Good range: 2-5%
- Meaning: Higher = better ad relevance

**Conversion Rate**
- Formula: Conversions ÷ Clicks
- Good range: 2-5%
- Meaning: Higher = better funnel quality

**CPA (Cost Per Acquisition)**
- Formula: Cost ÷ Conversions
- Good range: < 100 AED
- Meaning: Lower = more efficient

**ROAS (Return on Ad Spend)**
- Formula: Revenue ÷ Cost
- Good range: 2x or higher
- Meaning: 2x = Every AED 1 spent returns AED 2

### Confidence Levels
- 🟢 **High Confidence**: Strong recommendation with clear data
- 🟡 **Medium Confidence**: Valid but needs investigation
- 🔴 **Low Confidence**: Weak signal with limited data

---

## 🎯 Next Steps

### Immediate (Today)
1. ✅ Run demo analysis
2. ✅ Review the recommendations
3. ✅ Understand the budget suggestions

### Short-Term (This Week)
1. Prepare your actual campaign data as CSV
2. Run analysis on your real data
3. Review recommendations
4. Share findings with team
5. Plan implementation

### Medium-Term (This Month)
1. Implement top recommendations
2. Set up automated data exports from Google Ads
3. Run weekly analyses
4. Track performance improvements

### Long-Term (This Quarter)
1. Integrate with Streamlit for visual dashboard
2. Connect to Google Ads API for daily updates
3. Set up automated alerts for issues
4. Build custom threshold configurations

---

## 📝 Using Your Own Data

### Step 1: Prepare CSV
Export your Google Ads data as CSV with these columns:

Required:
- `date` (format: 2025-12-01)
- `campaign_name`
- `campaign_type` (Search / PMax / Android App / iOS App)
- `impressions`
- `clicks`
- `cost` (in AED)
- `conversions`

Optional:
- `revenue` (for ROAS calculation)
- `platform` (Search / Display / App)
- `device_os` (iOS / Android / Web)

### Step 2: Run Analysis
```bash
python main_windows.py your_data.csv
```

### Step 3: Review Recommendations
```bash
python main_windows.py your_data.csv --output analysis.json
```

### Step 4: Implement Changes
Use the recommendations to optimize your campaigns.

---

## 💡 Common Use Cases

### Use Case 1: Identify Underperformers
```bash
python main_windows.py data.csv
# Look for "Low ROAS" and "High Spend Low Return" issues
```

### Use Case 2: Budget Optimization
```bash
python main_windows.py data.csv
# Check "Budget Allocation Recommendation" section
```

### Use Case 3: Find Ad Copy Issues
```bash
python main_windows.py data.csv
# Look for "Low CTR" recommendations
```

### Use Case 4: Fix Conversion Problems
```bash
python main_windows.py data.csv
# Look for "Low Conversion Rate" recommendations
```

### Use Case 5: Scale Winners
```bash
python main_windows.py data.csv
# Look for "Strong performance" recommendations
```

---

## 🔧 Customization

### Change CPA Threshold
Edit `config.py`:
```python
CPA_THRESHOLDS = {
    'high': 500,      # Change this value
    'warning': 300,
}
```

### Add Custom Metrics
Edit `src/analyzer.py`:
```python
def calculate_custom_metric(self):
    # Your metric calculation
    pass
```

### Modify Recommendations
Edit `src/recommender.py`:
```python
def _recommend_for_campaign(self):
    # Your recommendation logic
    pass
```

---

## 🚨 Troubleshooting

### "File not found"
- Check the CSV file path is correct
- Use absolute path: `C:\path\to\file.csv`

### "Missing required columns"
- Check your CSV has exactly these columns (case-sensitive):
  - date, campaign_name, campaign_type, impressions, clicks, cost, conversions
- Column names must match exactly

### "No module named 'pandas'"
- Install: `pip install pandas`

### Console shows garbled characters
- You're using `main.py` (emoji issue on Windows)
- Use `main_windows.py` instead

### JSON export fails
- Check you have write permissions in the directory
- Try: `python main_windows.py data.csv --output C:\path\to\output.json`

---

## 📞 Quick Reference

### File Purpose
- `main_windows.py` - Use this (Windows-compatible)
- `config.py` - Adjust thresholds here
- `sample_data.csv` - Test with this
- `README.md` - Full documentation
- `QUICKSTART.md` - More details

### Key Commands
```bash
# Analyze data
python main_windows.py data.csv

# Export to JSON
python main_windows.py data.csv --output report.json

# Quiet mode (no verbose output)
python main_windows.py data.csv --no-verbose

# Help
python main_windows.py --help
```

---

## ✨ Pro Tips

### Tip 1: Compare Over Time
Run analysis weekly and compare recommendations to track progress.

### Tip 2: Data Quality
Ensure your date formats are consistent (YYYY-MM-DD).

### Tip 3: Test First
Always test with sample data before using real data.

### Tip 4: Export & Share
Export JSON for easy sharing with team members.

### Tip 5: Validate Recommendations
Not all recommendations may apply to your business - validate before implementing.

---

## 🎓 How the Bot Works

### Step 1: Data Loading
- Reads your CSV file
- Validates columns and data types
- Flags missing or anomalous values

### Step 2: Analysis
- Calculates all metrics (CTR, CPA, ROAS, etc.)
- Compares campaigns side-by-side
- Detects issues and trends

### Step 3: Recommendations
- Generates tailored suggestions
- Calculates optimal budget allocation
- Assigns confidence levels

### Step 4: Output
- Prints human-readable report
- Exports machine-readable JSON
- Ready for integration

---

## 🎯 Success Indicators

You're using the bot successfully when:
- ✅ You run weekly analyses
- ✅ You implement recommendations
- ✅ Campaign performance improves
- ✅ Budget allocation becomes more efficient
- ✅ Team uses insights for decisions

---

## 📚 Learn More

- `README.md` - Complete documentation
- `QUICKSTART.md` - More examples
- `DEPLOYMENT.md` - Production deployment
- `TESTING.md` - Test results and validation
- `config.py` - All configuration options

---

## 🚀 Ready?

Start with this command:
```bash
python main_windows.py sample_data.csv
```

Then continue with your own data!

---

**Questions?** Check the README.md or relevant .md file for more details.

**Need help?** All code is well-documented with comments.

**Want to extend?** The code is modular and ready for customization.

Enjoy! 🎉
