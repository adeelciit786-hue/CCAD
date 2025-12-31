# Champion Cleaners Bot - Quick Start Guide

## ✅ Setup (Already Done!)

Your virtual environment is active and the bot is ready to use. All dependencies are installed.

## 🚀 Quick Start

### 1. Test the Bot with Sample Data
```bash
python main.py sample_data.csv
```

**Output**: Full analysis with console recommendations + performance metrics

### 2. Export Recommendations to JSON
```bash
python main.py sample_data.csv --output recommendations.json
```

**Output**: Both console summary + structured JSON file for integration

### 3. Quiet Mode (Data Only, No Verbose Output)
```bash
python main.py sample_data.csv --no-verbose
```

## 📋 Using Your Own Data

### Step 1: Prepare Your CSV
Ensure your CSV contains these columns:
- `date` (YYYY-MM-DD format)
- `campaign_name`
- `campaign_type` (Search / PMax / Android App / iOS App)
- `impressions` (numeric)
- `clicks` (numeric)
- `cost` (numeric, in AED)
- `conversions` (numeric)

### Optional Columns
- `revenue` (for ROAS calculation)
- `platform` (Search / Display / App)
- `device_os` (iOS / Android / Web)

### Step 2: Run Analysis
```bash
python main.py your_data.csv --output your_analysis.json
```

## 📊 Understanding the Output

### Key Metrics
| Metric | What It Means |
|--------|---------------|
| **CTR** | Click-Through Rate (%) - higher is better |
| **Conversion Rate** | % of clicks that convert - higher is better |
| **CPA** | Cost Per Acquisition (AED) - lower is better |
| **ROAS** | Return on Ad Spend - higher is better |

### Confidence Levels
- 🟢 **High**: Strong recommendation with clear data support
- 🟡 **Medium**: Valid concern, investigate further
- 🔴 **Low**: Weak signal, limited data

### Issue Severity
- 🔴 **High**: Immediate action recommended
- 🟡 **Medium**: Monitor and address soon
- 🟢 **Low**: Keep in mind during optimization

## 💡 What the Bot Does

### 1. **Data Validation**
✓ Checks for missing values  
✓ Validates data types  
✓ Warns about low-volume campaigns  
✓ Detects anomalies  

### 2. **Performance Analysis**
✓ Calculates key metrics (CTR, CPA, ROAS, etc.)  
✓ Compares campaigns side-by-side  
✓ Analyzes by platform and device  
✓ Identifies trends and issues  

### 3. **Intelligent Recommendations**
✓ Tailored actions for each campaign  
✓ Budget allocation optimization  
✓ Copy and landing page improvement suggestions  
✓ Scaling strategies for winners  

### 4. **Structured Output**
✓ Human-readable console summary  
✓ Machine-readable JSON file  
✓ Ready for dashboards and APIs  

## 🎯 Key Insights for Champion Cleaners

### What the Bot Looks For
1. **High Cost Per Acquisition** → Tighten targeting or improve landing page
2. **Low Click-Through Rate** → Refresh ad copy and creative
3. **Low Conversion Rate** → Fix booking form, reduce friction
4. **Low ROAS** → Verify tracking, review pricing
5. **High Spend + Low Return** → Pause low performers, reallocate budget

### What the Bot DOES NOT Do
❌ Recommend excluding platforms (all evaluated on merit)  
❌ Make assumptions without data  
❌ Sacrifice quality for volume  
❌ Recommend short-term tricks over sustainable growth  

## 📁 Project Structure

```
Google ADS/
├── main.py                 ← Run this file
├── requirements.txt        ← Dependencies
├── sample_data.csv         ← Example data
├── recommendations.json    ← Output file (auto-generated)
├── README.md              ← Full documentation
├── QUICKSTART.md          ← This file
└── src/
    ├── data_loader.py     ← CSV loading
    ├── analyzer.py        ← Metrics calculation
    └── recommender.py     ← Recommendations
```

## 🔧 Troubleshooting

### "Command not found" or "not recognized"
Make sure you're in the right directory:
```bash
cd "c:\Users\adeel\Google ADS"
```

### Virtual environment not activated
Activate it:
```bash
.\.venv\Scripts\Activate.ps1
```

### Module not found errors
Install dependencies:
```bash
pip install -r requirements.txt
```

### CSV errors
Check that:
- File path is correct
- All required columns exist
- No special characters in column names
- Data types are numeric where expected

## 📞 Next Steps

1. **Run with your real data** - Replace sample_data.csv with actual campaign data
2. **Review recommendations** - Check the JSON output for insights
3. **Implement changes** - Use recommendations to optimize campaigns
4. **Set up dashboard** - (Future) Integrate with Streamlit UI
5. **Automate** - (Future) Connect to Google Ads API for daily updates

## 💻 For Developers

### Running Individual Modules
```python
from src.data_loader import DataLoader
from src.analyzer import PerformanceAnalyzer

loader = DataLoader('sample_data.csv')
df = loader.load()

analyzer = PerformanceAnalyzer(df)
metrics = analyzer.get_campaign_metrics()
```

### Extending the Bot
- Add custom metrics in `analyzer.py`
- Create new recommendation logic in `recommender.py`
- Integrate with APIs in separate modules
- Build Streamlit dashboard using bot outputs

## ✨ Features Ready for Production
- ✅ Modular code structure
- ✅ Error handling and validation
- ✅ JSON export for integrations
- ✅ Comprehensive documentation
- ✅ Extensible architecture
- ✅ Ready for Streamlit dashboard
- ✅ Ready for API integration

---

**Need help?** Check README.md for detailed documentation.
