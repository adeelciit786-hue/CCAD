# Monthly Campaign Engine - Champion Cleaners UAE

## Overview

The Monthly Campaign Engine is a comprehensive Python-based analysis system that processes multiple monthly Google Ads export files to deliver intelligent campaign insights, performance trend analysis, and strategic recommendations for Champion Cleaners UAE.

## Architecture

The engine is built with 8 modular components, each with a specific responsibility:

### 1. **file_loader.py** - Data Discovery & Loading
- **Purpose**: Discover and load monthly CSV files from Google Ads exports
- **Key Features**:
  - Regex-based file discovery (pattern: "Mon YYYY.csv", e.g., "Mar 2025.csv")
  - Month/year extraction and automatic month numbering
  - Automatic filtering of Google Ads metadata rows and total rows
  - Combines all months into time-series dataframe
- **Main Class**: `MonthlyFileLoader`
- **Example Usage**:
```python
from file_loader import MonthlyFileLoader
loader = MonthlyFileLoader('/path/to/data')
df = loader.combine_all_months()  # Returns combined dataframe
```

### 2. **column_mapper.py** - Column Normalization
- **Purpose**: Handle variable column names across different Google Ads exports
- **Key Features**:
  - Maps 13 column types to standard names
  - Handles multiple aliases per column (e.g., "Impr." vs "Impressions")
  - Cleans numeric values (removes commas, handles percentages)
  - Defensive design - continues if columns missing
- **Standard Columns Created**:
  - `campaign_name`, `campaign_type`, `impressions`, `clicks`, `cost`
  - `conversions`, `conv_value`, `conv_rate`, `interaction_rate`
  - `avg_cpc`, `campaign_status`, `optimization_score`, `bid_strategy`
- **Main Class**: `ColumnMapper`

### 3. **metrics_engine.py** - Performance Metric Calculation
- **Purpose**: Calculate standard marketing metrics from normalized data
- **Metrics Calculated**:
  - **CTR** (Click-Through Rate) - % of impressions that clicked
  - **CVR** (Conversion Rate) - % of interactions that converted
  - **CPC** (Cost Per Click) - AED spent per click
  - **CPA** (Cost Per Acquisition) - AED spent per conversion
  - **ROAS** (Return on Ad Spend) - Revenue multiplier on spend
  - **Spend Share** - % of monthly total budget
- **Main Class**: `MetricsEngine`
- **Output**: Dataframe with all metrics plus monthly aggregates

### 4. **trend_analyzer.py** - Trend & Seasonality Analysis
- **Purpose**: Detect patterns and trends across monthly data
- **Analysis Types**:
  - **Growth Trends**: GROWING/DECLINING/FLAT classification based on conversions and CPA
  - **Seasonal Patterns**: Peak months, low months, seasonality ratio
  - **Volatility Detection**: Campaign stability rating (STABLE/MODERATE/UNSTABLE)
  - **Month-over-Month Changes**: Percentage changes in any metric
- **Main Class**: `TrendAnalyzer`

### 5. **loss_detector.py** - Performance Loss Detection
- **Purpose**: Identify lost opportunities and performance leaks
- **Detection Types**:
  - **Spend-Conversion Mismatch**: Spend up but conversions down (efficiency loss)
  - **Declining Efficiency**: Rising CPA over time (30%+ increase triggers alert)
  - **Sudden Drops**: Abrupt CTR or CVR declines (50%+ drop triggers alert)
  - **High Spend, Low ROI**: Campaigns with poor profit margins (ROAS < 1.0)
  - **Inactive Campaigns**: Zero impressions or zero conversions for full month
- **Main Class**: `LossDetector`
- **Severity Levels**: HIGH, MEDIUM, LOW

### 6. **business_context.py** - Business Context Integration
- **Purpose**: Map campaigns to Champion Cleaners services and analyze alignment
- **Services Mapped**:
  - Home Cleaning (35% importance)
  - Office Cleaning (25% importance)
  - Carpet Cleaning (15% importance)
  - Deep Cleaning (12% importance)
  - Window Cleaning (8% importance)
  - Moving Cleaning (5% importance)
- **Analysis Types**:
  - Service coverage analysis
  - Platform budget alignment (Search 40%, PMax 30%, Android 15%, iOS 15%)
  - High-performing services by ROI
  - Service gaps and underrepresented services
- **Main Class**: `BusinessContextAnalyzer`

### 7. **recommendation_engine.py** - Strategic Recommendations
- **Purpose**: Generate actionable recommendations from all analyses
- **Recommendation Types**:
  - **Budget Recommendations**: Increase/decrease budgets based on ROI
  - **Loss Remediation**: Actions to fix detected issues (pause, optimize, refresh creatives, etc.)
  - **Growth Opportunities**: Campaigns to scale based on strong ROAS
  - **Strategic Initiatives**: Platform rebalancing, service expansion
- **Recommendation Fields**:
  - Type, target campaign/service
  - Root cause hypothesis
  - Expected impact
  - Confidence score (0-1)
  - Priority (CRITICAL, HIGH, MEDIUM)
- **Main Class**: `RecommendationEngine`

### 8. **monthly_main.py** - Orchestration & Output
- **Purpose**: Tie all modules together and coordinate analysis pipeline
- **Pipeline Steps**:
  1. Load monthly CSV files
  2. Normalize columns
  3. Calculate metrics
  4. Analyze trends
  5. Detect losses
  6. Analyze business context
  7. Generate recommendations
- **Output Formats**:
  - Console summary (executive summary with highlights)
  - JSON export with full analysis results
- **Main Class**: `MonthlyCampaignEngine`

## Usage

### Command Line
```bash
cd monthly_campaign_engine
python monthly_main.py /path/to/csv/folder
```

### Python API
```python
from monthly_main import MonthlyCampaignEngine

engine = MonthlyCampaignEngine('/path/to/csv/folder')
results = engine.run_analysis(output_json=True, output_console=True)

# Access individual analyses
print(f"Trends: {results['trends']}")
print(f"Losses: {results['losses']}")
print(f"Recommendations: {results['recommendations']}")
```

## CSV Format Requirements

Monthly CSV files should follow Google Ads export format:
- Filename pattern: "MonthName Year.csv" (e.g., "Mar 2025.csv")
- Contains campaign performance data with headers
- Supports both old ("Impr.", "Interactions") and new ("Impressions", "Clicks") column names

Example supported filenames:
- Mar 2025.csv
- Apr 2025.csv
- May 2025.csv
- June 2025.csv
- July 2025.csv
- Aug 2025.csv
- Sep 2025.csv
- Oct 2025.csv
- Nov 2025.csv

## Output

### Console Output
Displays executive summary with:
- Campaign overview (count, months, total spend, conversions, avg ROAS)
- Performance issues summary (severity distribution)
- Top critical issues (3 highest severity)
- Service coverage analysis
- Recommendations summary (by priority level)
- Growth opportunities (campaigns to scale)

### JSON Export
Structured JSON file containing:
- Analysis timestamp and metadata
- Summary statistics
- Complete trends analysis
- All detected losses with details
- Business context analysis
- All generated recommendations with confidence scores

## Integration Points

The monthly campaign engine is designed for easy integration:

### With Streamlit Dashboard
```python
from monthly_main import MonthlyCampaignEngine
engine = MonthlyCampaignEngine()
results = engine.run_analysis(output_json=False, output_console=False)
# Display results in Streamlit UI
```

### With Flask API
```python
@app.route('/api/analyze-monthly-campaigns', methods=['POST'])
def analyze_monthly():
    csv_dir = request.json.get('csv_directory')
    engine = MonthlyCampaignEngine(csv_dir)
    results = engine.run_analysis()
    return jsonify(results)
```

### With Existing Keyword Engine
The monthly campaign engine complements the keyword_engine_v2:
- Keyword engine: Deep-dives into individual keyword performance
- Monthly engine: Holistic multi-month campaign trends and strategic insights

## Technical Details

### Python Version
- Python 3.8+ (tested with Python 3.14.2)

### Dependencies
- pandas (data manipulation)
- numpy (numerical operations)
- pathlib (file path handling)
- json (output serialization)
- datetime (timestamps)

### Data Types
- All numeric columns: float64 (for precision)
- Campaign/month identifiers: object (strings)
- Month field: Categorical (for proper sorting)

### Error Handling
- Missing column handling: Defensive mapping with fallbacks
- NaN/Inf handling: Replaces with 0 for calculations
- Empty CSV handling: Returns empty dataframe without crashing
- File not found: Logs warning and continues

## Performance Insights

The engine analyzes:
- **Efficiency Trends**: Are we getting better ROI over time?
- **Seasonal Patterns**: Which months perform best?
- **Risk Indicators**: Early warning of declining campaigns
- **Opportunity Detection**: Which campaigns can be scaled?
- **Service Alignment**: Are we investing in the right services?
- **Platform Balance**: Is our budget distributed correctly?

## Example Analysis Flow

```
Raw CSV Files (7 months)
        ↓
File Loader (discovers and loads)
        ↓
Column Mapper (normalizes 13+ columns)
        ↓
Metrics Engine (calculates 6 metrics)
        ↓
Trend Analyzer (detects 4 pattern types)
        ↓
Loss Detector (identifies 5 issue types)
        ↓
Business Context (maps to 6 services)
        ↓
Recommendation Engine (generates strategies)
        ↓
JSON Export + Console Summary
```

## Troubleshooting

**Issue**: "No data loaded. Check file paths."
- Solution: Ensure CSV files are in the correct directory and use "Mon YYYY.csv" naming

**Issue**: Column not found errors
- Solution: Automatic - mapper handles most Google Ads export variations. If column truly missing, it will log warning and continue.

**Issue**: Empty results
- Solution: Verify CSV files contain campaign data rows (not just headers)

## Future Enhancements

- Real-time monitoring alerts
- Predictive trend forecasting
- A/B test comparison analysis
- Competitor benchmarking integration
- Custom metric definitions
- Automated report scheduling

---

**Status**: Production Ready ✅
**Last Updated**: December 2024
**Created for**: Champion Cleaners UAE
