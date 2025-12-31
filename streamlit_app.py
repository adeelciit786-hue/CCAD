"""
Streamlit Web Application - Champion Cleaners Google Ads Bot
Exact replica of Flask localhost app on Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
import sys
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

try:
    from main_windows import ChampionCleanersBot
    from keyword_main import KeywordIntelligenceEngine
except ImportError as e:
    st.error(f"Error loading modules: {e}")
    sys.exit(1)

# Configure page
st.set_page_config(
    page_title="Champion Cleaners - Google Ads Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching localhost
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 2em;
        font-weight: bold;
        color: #667eea;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1em;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_type' not in st.session_state:
    st.session_state.analysis_type = 'campaign'
if 'campaign_results' not in st.session_state:
    st.session_state.campaign_results = None
if 'keyword_results' not in st.session_state:
    st.session_state.keyword_results = None

# Header
st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #667eea;">🤖 Champion Cleaners - Google Ads Bot</h1>
        <p style="font-size: 1.1em; color: #666;">AI-Powered Google Ads Analysis & Optimization</p>
    </div>
""", unsafe_allow_html=True)

# Main tabs for analysis type
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Campaign Analysis", key="campaign_btn", use_container_width=True):
        st.session_state.analysis_type = 'campaign'
        st.rerun()

with col2:
    if st.button("🔍 Keyword Engine", key="keyword_btn", use_container_width=True):
        st.session_state.analysis_type = 'keyword'
        st.rerun()

st.markdown("---")

# ==================== CAMPAIGN ANALYSIS ====================
if st.session_state.analysis_type == 'campaign':
    st.subheader("📊 Campaign Analysis")
    
    # Tabs for input
    tab1, tab2 = st.tabs(["Sample Data", "Upload CSV"])
    
    with tab1:
        st.write("Analyze using sample campaign data")
        if st.button("▶️ Run Sample Analysis", key="campaign_sample_btn", use_container_width=True):
            with st.spinner("Analyzing sample data..."):
                try:
                    sample_path = Path(__file__).parent / 'sample_data.csv'
                    if sample_path.exists():
                        bot = ChampionCleanersBot(str(sample_path), use_emojis=False)
                        results = bot.run_analysis(verbose=False)
                        st.session_state.campaign_results = results
                        st.success("✅ Analysis complete!")
                    else:
                        st.error("Sample data file not found")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.write("Upload your CSV file for analysis")
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key="campaign_upload")
        if uploaded_file is not None:
            if st.button("▶️ Run Analysis", key="campaign_upload_btn", use_container_width=True):
                with st.spinner("Analyzing data..."):
                    try:
                        upload_path = Path(__file__).parent / 'uploads' / uploaded_file.name
                        upload_path.parent.mkdir(exist_ok=True)
                        with open(upload_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        
                        bot = ChampionCleanersBot(str(upload_path), use_emojis=False)
                        results = bot.run_analysis(verbose=False)
                        st.session_state.campaign_results = results
                        st.success("✅ Analysis complete!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Display results
    if st.session_state.campaign_results:
        results = st.session_state.campaign_results
        st.markdown("---")
        st.subheader("📈 Analysis Results")
        
        # Results tabs
        res_tab1, res_tab2, res_tab3, res_tab4, res_tab5, res_tab6 = st.tabs([
            "Campaign Metrics",
            "Platform Analysis",
            "Device Analysis",
            "Issues Detected",
            "Recommendations",
            "Budget Allocation"
        ])
        
        with res_tab1:
            st.write("### Campaign Metrics")
            if 'campaign_metrics' in results:
                metrics = results['campaign_metrics']
                col1, col2, col3, col4 = st.columns(4)
                
                metrics_to_display = list(metrics.items())[:4]
                for idx, (key, value) in enumerate(metrics_to_display):
                    with [col1, col2, col3, col4][idx]:
                        st.metric(key.replace('_', ' ').title(), f"{value:,}" if isinstance(value, (int, float)) else value)
                
                # Display all metrics as table
                metrics_df = pd.DataFrame([metrics])
                st.dataframe(metrics_df, use_container_width=True)
        
        with res_tab2:
            st.write("### Platform Analysis")
            if 'platform_analysis' in results:
                platform = results['platform_analysis']
                col1, col2, col3 = st.columns(3)
                platform_items = list(platform.items())
                for idx, (key, value) in enumerate(platform_items[:3]):
                    with [col1, col2, col3][idx]:
                        st.metric(key.replace('_', ' ').title(), f"{value:,}" if isinstance(value, (int, float)) else value)
                
                platform_df = pd.DataFrame([platform])
                st.dataframe(platform_df, use_container_width=True)
        
        with res_tab3:
            st.write("### Device Analysis")
            if 'device_analysis' in results:
                device = results['device_analysis']
                col1, col2, col3 = st.columns(3)
                device_items = list(device.items())
                for idx, (key, value) in enumerate(device_items[:3]):
                    with [col1, col2, col3][idx]:
                        st.metric(key.replace('_', ' ').title(), f"{value:,}" if isinstance(value, (int, float)) else value)
                
                device_df = pd.DataFrame([device])
                st.dataframe(device_df, use_container_width=True)
        
        with res_tab4:
            st.write("### Issues Detected")
            if 'detected_issues' in results:
                issues = results['detected_issues']
                if issues:
                    for i, issue in enumerate(issues, 1):
                        st.warning(f"**{i}. {issue}**")
                else:
                    st.success("No issues detected ✅")
        
        with res_tab5:
            st.write("### Recommendations")
            if 'recommendations' in results:
                recommendations = results['recommendations']
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        st.info(f"**{i}. {rec}**")
                else:
                    st.info("No recommendations available")
        
        with res_tab6:
            st.write("### Budget Allocation")
            if 'budget_allocation' in results:
                budget = results['budget_allocation']
                col1, col2, col3 = st.columns(3)
                budget_items = list(budget.items())
                for idx, (key, value) in enumerate(budget_items[:3]):
                    with [col1, col2, col3][idx]:
                        st.metric(key.replace('_', ' ').title(), f"{value:,}" if isinstance(value, (int, float)) else value)
                
                budget_df = pd.DataFrame([budget])
                st.dataframe(budget_df, use_container_width=True)
        
        # Export buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export as JSON", key="export_json"):
                json_str = json.dumps(results, indent=2, default=str)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Export as Excel", key="export_excel"):
                try:
                    from openpyxl import Workbook
                    from openpyxl.styles import Font, PatternFill
                    
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Analysis"
                    
                    # Headers
                    header_fill = PatternFill(start_color='667eea', end_color='667eea', fill_type='solid')
                    header_font = Font(bold=True, color='FFFFFF')
                    
                    headers = ['Metric', 'Value']
                    for col_num, header in enumerate(headers, 1):
                        cell = ws.cell(row=1, column=col_num)
                        cell.value = header
                        cell.fill = header_fill
                        cell.font = header_font
                    
                    # Data
                    row = 2
                    for key, value in results.get('campaign_metrics', {}).items():
                        ws.cell(row=row, column=1).value = key
                        ws.cell(row=row, column=2).value = value
                        row += 1
                    
                    # Save to bytes
                    from io import BytesIO
                    output = BytesIO()
                    wb.save(output)
                    output.seek(0)
                    
                    st.download_button(
                        label="Download Excel",
                        data=output.getvalue(),
                        file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except ImportError:
                    st.error("Excel export requires openpyxl package")

# ==================== KEYWORD ENGINE ====================
else:
    st.subheader("🔍 Keyword Intelligence Engine")
    
    # Tabs for input
    tab1, tab2 = st.tabs(["Sample Keywords", "Upload Keywords"])
    
    with tab1:
        st.write("Analyze using sample keywords data")
        if st.button("▶️ Run Keyword Analysis", key="keyword_sample_btn", use_container_width=True):
            with st.spinner("Analyzing sample keywords..."):
                try:
                    sample_path = Path(__file__).parent / 'sample_keywords.csv'
                    if sample_path.exists():
                        engine = KeywordIntelligenceEngine()
                        df = pd.read_csv(sample_path)
                        results = engine.analyze_keywords(df)
                        st.session_state.keyword_results = results
                        st.success("✅ Keyword analysis complete!")
                    else:
                        st.error("Sample keywords file not found")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.write("Upload your keywords CSV file")
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key="keyword_upload")
        if uploaded_file is not None:
            if st.button("▶️ Run Keyword Analysis", key="keyword_upload_btn", use_container_width=True):
                with st.spinner("Analyzing keywords..."):
                    try:
                        df = pd.read_csv(uploaded_file)
                        engine = KeywordIntelligenceEngine()
                        results = engine.analyze_keywords(df)
                        st.session_state.keyword_results = results
                        st.success("✅ Keyword analysis complete!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Display results
    if st.session_state.keyword_results:
        results = st.session_state.keyword_results
        st.markdown("---")
        st.subheader("📊 Keyword Analysis Results")
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Keywords", len(results.get('all_keywords', [])))
        with col2:
            st.metric("Recommendations", len(results.get('recommendations', [])))
        with col3:
            avg_roi = np.mean([r.get('estimated_roi', 0) for r in results.get('recommendations', [])]) if results.get('recommendations') else 0
            st.metric("Avg ROI", f"{avg_roi:.0f}%")
        with col4:
            total_revenue = sum([r.get('monthly_revenue_impact', 0) for r in results.get('recommendations', [])])
            st.metric("Revenue Impact", f"AED {total_revenue:,.0f}")
        
        st.markdown("---")
        
        # Recommendations table
        st.subheader("🎯 Top Recommendations")
        if 'recommendations' in results and results['recommendations']:
            rec_data = []
            for i, rec in enumerate(results['recommendations'][:10], 1):
                rec_data.append({
                    "#": i,
                    "Recommendation": rec.get('recommendation', 'N/A')[:60],
                    "ROI %": f"{rec.get('estimated_roi', 0):.0f}%",
                    "Revenue AED": f"{rec.get('monthly_revenue_impact', 0):,.0f}",
                    "Conversions": f"+{rec.get('conversions_impact', 0)}",
                    "Savings AED": f"{rec.get('cost_savings', 0):,.0f}"
                })
            
            rec_df = pd.DataFrame(rec_data)
            st.dataframe(rec_df, use_container_width=True, hide_index=True)
        
        # Export buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export as JSON", key="keyword_export_json"):
                json_str = json.dumps(results, indent=2, default=str)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"keyword_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Export as Excel", key="keyword_export_excel"):
                try:
                    from openpyxl import Workbook
                    
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Recommendations"
                    
                    # Headers
                    from openpyxl.styles import PatternFill, Font
                    header_fill = PatternFill(start_color='667eea', end_color='667eea', fill_type='solid')
                    header_font = Font(bold=True, color='FFFFFF')
                    
                    headers = ['#', 'Recommendation', 'ROI %', 'Revenue AED', 'Conversions', 'Savings AED']
                    for col_num, header in enumerate(headers, 1):
                        cell = ws.cell(row=1, column=col_num)
                        cell.value = header
                        cell.fill = header_fill
                        cell.font = header_font
                    
                    # Data
                    for row_num, rec in enumerate(results.get('recommendations', [])[:20], 2):
                        ws.cell(row=row_num, column=1).value = row_num - 1
                        ws.cell(row=row_num, column=2).value = rec.get('recommendation', '')
                        ws.cell(row=row_num, column=3).value = rec.get('estimated_roi', 0)
                        ws.cell(row=row_num, column=4).value = rec.get('monthly_revenue_impact', 0)
                        ws.cell(row=row_num, column=5).value = rec.get('conversions_impact', 0)
                        ws.cell(row=row_num, column=6).value = rec.get('cost_savings', 0)
                    
                    # Save to bytes
                    from io import BytesIO
                    output = BytesIO()
                    wb.save(output)
                    output.seek(0)
                    
                    st.download_button(
                        label="Download Excel",
                        data=output.getvalue(),
                        file_name=f"keyword_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except ImportError:
                    st.error("Excel export requires openpyxl package")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📚 [Documentation](https://github.com/adeelciit786-hue/CCAD)**")
with col2:
    st.markdown("**🐛 [Report Issues](https://github.com/adeelciit786-hue/CCAD/issues)**")
with col3:
    st.markdown("**⭐ [GitHub](https://github.com/adeelciit786-hue/CCAD)**")

st.caption(f"Champion Cleaners Google Ads Bot v2.0.0 | {datetime.now().strftime('%B %d, %Y')}")
