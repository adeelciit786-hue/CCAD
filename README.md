# Champion Cleaners UAE - Google Ads Decision Support Bot

An AI-powered decision-support system for optimizing Google Ads campaigns. This bot analyzes campaign performance across multiple platforms (Search, Display, App) and generates intelligent, data-driven recommendations.

## Features

### 📊 Data Validation & Loading
- Load campaign data from CSV files
- Automatic data quality checks and warnings
- Validation of required columns and data types
- Detection of missing or anomalous values

### 📈 Performance Analysis
- **Per-Campaign Metrics**: CTR, Conversion Rate, CPA, ROAS, CPC
- **Cross-Campaign Comparison**: Identify best and worst performers
- **Platform Analysis**: Aggregate metrics by Search, Display, App
- **Device OS Analysis**: iOS vs Android performance comparison
- **Trend Detection**: Identify rising CPA, falling conversion rates, high spend/low return

### 💡 Intelligent Recommendations
- **High CPA Campaigns**: Suggestions for tightening targeting, improving copy
- **Low CTR Campaigns**: Creative optimization recommendations
- **Low Conversion Rate**: Landing page and funnel improvement tips
- **Low ROAS**: Revenue tracking validation and pricing review
- **High Spend/Low Return**: Budget reallocation and restructuring guidance
- **Good Performers**: Scaling and expansion strategies

### 💰 Budget Allocation Optimization
- Data-driven budget allocation recommendations
- Efficiency score calculations based on ROAS and conversion rates
- Suggested budget adjustments for each campaign
- Sustainable growth focus without platform exclusion

### 📁 Structured Output
- **Console Summary**: Human-readable analysis with visual indicators
- **JSON Export**: Machine-readable recommendations for system integration
- **Modular Design**: Ready for Streamlit dashboard and API integration

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup

1. **Create and activate virtual environment**:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # On Windows
source .venv/bin/activate     # On macOS/Linux
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Analysis
```bash
python main.py sample_data.csv
```

### Export Recommendations to JSON
```bash
python main.py sample_data.csv --output recommendations.json
```

### Suppress Detailed Output
```bash
python main.py sample_data.csv --no-verbose
```

## CSV Input Format

Your CSV file should contain the following columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `date` | Date | ✓ | Campaign date (YYYY-MM-DD) |
| `campaign_name` | String | ✓ | Name of the campaign |
| `campaign_type` | String | ✓ | Type: Search / PMax / Android App / iOS App |
| `impressions` | Integer | ✓ | Number of impressions |
| `clicks` | Integer | ✓ | Number of clicks |
| `cost` | Float | ✓ | Cost in AED |
| `conversions` | Integer | ✓ | Number of conversions |
| `revenue` | Float | - | Revenue in AED (optional) |
| `installs` | Integer | - | App installs (optional) |
| `platform` | String | - | Platform: Search / Display / App (optional) |
| `device_os` | String | - | Device OS: iOS / Android / Web (optional) |

### Example CSV Row
```
2025-12-01,Search_Brand,Search,15000,900,3000,45,9000,Search,Web
```

## Project Structure

```
Google ADS/
├── main.py                 # Entry point and bot orchestrator
├── requirements.txt        # Python dependencies
├── sample_data.csv         # Example data for testing
├── recommendations.json    # Output file (generated)
└── src/
    ├── __init__.py
    ├── data_loader.py      # CSV loading and validation
    ├── analyzer.py         # Performance metrics calculation
    └── recommender.py      # Recommendation generation
```

## Module Documentation

### data_loader.py
- `DataLoader`: Handles CSV loading, validation, and data cleaning
- Methods:
  - `load()`: Load and validate CSV
  - `validate_data_quality()`: Perform comprehensive data checks
  - `get_summary()`: Get overview of loaded data

### analyzer.py
- `PerformanceAnalyzer`: Calculate metrics and detect issues
- Methods:
  - `get_campaign_metrics()`: Get metrics for campaigns
  - `compare_campaigns()`: Rank campaigns by various metrics
  - `detect_trends_and_risks()`: Identify issues and anomalies
  - `analyze_by_platform()`: Platform-level analysis
  - `analyze_by_device_os()`: Device OS-level analysis

### recommender.py
- `RecommendationEngine`: Generate actionable recommendations
- Methods:
  - `generate_recommendations()`: Generate all recommendations
  - `generate_budget_allocation_recommendation()`: Optimal budget split
  - `export_recommendations_json()`: Save recommendations to JSON

### main.py
- `ChampionCleanersBot`: Orchestrate analysis pipeline
- `main()`: CLI entry point with argument parsing

## Output Format

### Console Output Example
```
Campaign Performance Metrics:

  Search_Brand (Search)
    • Impressions: 76,400
    • Clicks: 4,530 (CTR: 5.93%)
    • Cost: AED 15,100.00
    • Conversions: 222
    • CPA: AED 68.02 | Conv Rate: 4.9%

Recommendations:
  1. Search_Brand
     🟢 Confidence: High
     Issue: Strong performance detected
     Action: Excellent ROAS - prioritize scaling this campaign
```

### JSON Output Structure
```json
{
  "summary": {
    "total_campaigns": 5,
    "high_priority_issues": 0,
    "medium_priority_issues": 3
  },
  "recommendations": [
    {
      "campaign_name": "Search_Brand",
      "issue_detected": "Strong performance detected",
      "recommendation": "Scale budget...",
      "confidence_level": "High"
    }
  ],
  "budget_allocation": {
    "total_monthly_budget": 95650.00,
    "allocations": { ... }
  }
}
```

## Confidence Levels

- **High**: Strong data support, clear patterns detected
- **Medium**: Moderate data support, further validation recommended
- **Low**: Limited data or inconclusive patterns

## Key Metrics Explained

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **CTR** | Clicks / Impressions × 100 | Lower = poor ad relevance |
| **Conversion Rate** | Conversions / Clicks × 100 | Lower = funnel issues |
| **CPA** | Cost / Conversions | Lower = more efficient |
| **ROAS** | Revenue / Cost | Higher = better ROI |
| **CPC** | Cost / Clicks | Lower = cheaper traffic |

## Business Logic

### Budget Allocation Algorithm
1. Calculate efficiency score: `ROAS × Conversion Rate`
2. Normalize scores across all campaigns
3. Allocate budget proportional to efficiency
4. Compare recommended vs current allocation
5. Suggest adjustments as percentage changes

### Risk Detection Thresholds
- **High CPA**: > AED 500
- **Low CTR**: < 1.0% (with sufficient impressions)
- **Low Conversion Rate**: < 1.0% (with sufficient clicks)
- **Low ROAS**: < 1.5x (with significant spend)
- **High Spend/Low Return**: > AED 5,000 spend with < 10 conversions

## Future Enhancements

- [ ] Streamlit dashboard for interactive analysis
- [ ] Google Ads API integration for automated data import
- [ ] Time-series trend analysis and forecasting
- [ ] A/B test result analysis
- [ ] Automated alerting system
- [ ] Custom threshold configuration
- [ ] Multi-account support
- [ ] Historical comparison and benchmarking

## Important Notes

### No Platform Exclusion
The bot does NOT recommend platform exclusion by default. Each platform is evaluated on merit:
- iOS being higher value is an insight, not a rule
- All platforms (Search, Display, App) are considered for optimization
- Budget recommendations are data-driven and performance-based

### Quality Over Quantity
- Focus is on customer quality and long-term value
- Sustainable growth takes priority over short-term metrics
- Recommendations consider audience reach expansion

## Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas
```

### "File not found" Error
Ensure the CSV file path is correct and the file exists.

### Missing Columns Warning
Check that your CSV contains all required columns with exact spelling.

### Low Data Volume Warning
Campaigns with < 100 impressions may have unreliable metrics. Consider aggregating data.

## License

Internal use for Champion Cleaners UAE

## Support

For issues or feature requests, please contact the analytics team.

---

**Version**: 1.0.0  
**Last Updated**: December 2025
