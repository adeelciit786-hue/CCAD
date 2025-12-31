"""
Streamlit Web Application for Keyword Intelligence Platform
AI-powered Google Ads keyword analysis with ROI metrics
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import sys
from io import BytesIO
from datetime import datetime

# Add keyword engine to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

try:
    from keyword_main import KeywordIntelligenceEngine
    from keyword_recommender import KeywordRecommender
except ImportError as e:
    st.error(f"Error loading keyword engine: {e}")
    sys.exit(1)

# Configure Streamlit page
st.set_page_config(
    page_title="Keyword Intelligence Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_file' not in st.session_state:
    st.session_state.current_file = None

# Title and header
st.title("🔍 Keyword Intelligence Platform")
st.markdown("""
**AI-Powered Google Ads Keyword Analysis with ROI Metrics**

Analyze your Google Ads keywords and get actionable recommendations with estimated ROI impact.
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    # File upload
    st.subheader("📁 Upload CSV File")
    uploaded_file = st.file_uploader(
        "Upload your Google Ads keywords CSV",
        type=['csv'],
        help="CSV file with keyword data"
    )
    
    st.markdown("---")
    st.subheader("📊 Analysis Options")
    
    analysis_type = st.radio(
        "Analysis Type",
        ["Full Analysis", "Quick Summary", "Top Recommendations"]
    )
    
    st.markdown("---")
    st.info("""
    **About This Platform:**
    - Analyzes keywords for optimization opportunities
    - Identifies lost demand and improvement areas
    - Provides ROI estimates for each recommendation
    - Generates professional reports
    """)

# Main content
if uploaded_file is not None:
    try:
        # Read uploaded file
        df = pd.read_csv(uploaded_file)
        st.session_state.current_file = uploaded_file.name
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File", uploaded_file.name[-30:], delta=None)
        with col2:
            st.metric("Rows", len(df), delta=None)
        with col3:
            st.metric("Columns", len(df.columns), delta=None)
        
        st.markdown("---")
        
        # Show data preview
        with st.expander("📄 Data Preview"):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Run analysis button
        if st.button("🚀 Run Analysis", key="analyze_btn"):
            with st.spinner("Analyzing keywords... This may take a moment..."):
                try:
                    # Initialize analysis engine
                    engine = KeywordIntelligenceEngine()
                    
                    # Run analysis
                    results = engine.analyze_keywords(df)
                    st.session_state.analysis_results = results
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
        
        # Display results if available
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            # Create tabs for different analyses
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📈 Overview",
                "⭐ Top Performers",
                "🔴 Lost Demand",
                "🎯 Match Types",
                "🌐 Relevance",
                "📉 Market Trends"
            ])
            
            with tab1:
                st.subheader("Analysis Overview")
                if isinstance(results, dict) and 'recommendations' in results:
                    recommendations = results['recommendations']
                    
                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Total Keywords",
                            len(df),
                            delta=None
                        )
                    
                    with col2:
                        st.metric(
                            "Recommendations",
                            len(recommendations),
                            delta=None
                        )
                    
                    with col3:
                        avg_roi = sum([r.get('estimated_roi', 0) for r in recommendations]) / len(recommendations) if recommendations else 0
                        st.metric(
                            "Avg ROI",
                            f"{avg_roi:.0f}%",
                            delta=None
                        )
                    
                    with col4:
                        total_revenue = sum([r.get('monthly_revenue_impact', 0) for r in recommendations])
                        st.metric(
                            "Total Revenue Impact",
                            f"AED {total_revenue:,.0f}",
                            delta=None
                        )
                    
                    st.markdown("---")
                    
                    # Recommendations table
                    st.subheader("🎯 Top Recommendations")
                    
                    # Create dataframe from recommendations
                    rec_data = []
                    for i, rec in enumerate(recommendations[:10], 1):
                        rec_data.append({
                            "Priority": "🔴 High" if i <= 5 else "🟡 Medium",
                            "Recommendation": rec.get('recommendation', 'N/A')[:50],
                            "ROI": f"{rec.get('estimated_roi', 0):.0f}%",
                            "Revenue Impact": f"AED {rec.get('monthly_revenue_impact', 0):,.0f}",
                            "Conversions": f"+{rec.get('conversions_impact', 0)}",
                            "Cost Savings": f"AED {rec.get('cost_savings', 0):,.0f}"
                        })
                    
                    rec_df = pd.DataFrame(rec_data)
                    st.dataframe(rec_df, use_container_width=True)
                else:
                    st.warning("No recommendations available")
            
            with tab2:
                st.subheader("⭐ Top Performing Keywords")
                if isinstance(results, dict) and 'top_keywords' in results:
                    top_keywords = results.get('top_keywords', [])
                    if top_keywords:
                        for i, kw in enumerate(top_keywords[:5], 1):
                            with st.container():
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    st.write(f"**{i}. {kw.get('keyword', 'N/A')}**")
                                with col2:
                                    st.write(f"Score: {kw.get('score', 0):.0f}")
                                with col3:
                                    st.write(f"CPC: {kw.get('cpc', 0):.2f} AED")
                    else:
                        st.info("No top keywords identified")
                else:
                    st.info("Top performers data not available")
            
            with tab3:
                st.subheader("🔴 Lost Demand Keywords")
                if isinstance(results, dict) and 'lost_demand' in results:
                    lost_keywords = results.get('lost_demand', [])
                    if lost_keywords:
                        for i, kw in enumerate(lost_keywords[:5], 1):
                            with st.container():
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    st.write(f"**{i}. {kw.get('keyword', 'N/A')}**")
                                with col2:
                                    st.write(f"Impressions: {kw.get('impressions', 0):,}")
                                with col3:
                                    st.write(f"Potential: AED {kw.get('potential_revenue', 0):,.0f}")
                    else:
                        st.info("No lost demand identified")
                else:
                    st.info("Lost demand data not available")
            
            with tab4:
                st.subheader("🎯 Match Type Optimization")
                st.info("Optimize your match types for better performance")
                st.write("Recommendations for match type adjustments...")
            
            with tab5:
                st.subheader("🌐 Website Relevance")
                st.info("Check keyword-to-page relevance")
                st.write("Website relevance analysis results...")
            
            with tab6:
                st.subheader("📉 Market Insights & Trends")
                st.info("Market trends and competitive analysis")
                st.write("Market insights data...")
            
            # Export section
            st.markdown("---")
            st.subheader("💾 Export Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Export to JSON
                if st.button("📥 Download as JSON"):
                    json_str = json.dumps(results, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_str,
                        file_name=f"keyword_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col2:
                # Export to CSV
                if st.button("📥 Download as CSV"):
                    if isinstance(results, dict) and 'recommendations' in results:
                        rec_df = pd.DataFrame(results['recommendations'])
                        csv_str = rec_df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv_str,
                            file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )

else:
    # Empty state
    st.info("👈 Upload a CSV file in the sidebar to get started")
    
    # Show example
    with st.expander("📋 Example CSV Format"):
        example_data = {
            "Keyword": ["google ads", "facebook ads", "digital marketing"],
            "Match Type": ["Broad", "Phrase", "Exact"],
            "Impressions": [1500, 800, 200],
            "Clicks": [75, 40, 20],
            "Conversions": [10, 8, 5],
            "Cost": [375, 200, 100],
            "Revenue": [2000, 1600, 1000]
        }
        example_df = pd.DataFrame(example_data)
        st.dataframe(example_df, use_container_width=True)
        
        # Download example
        csv = example_df.to_csv(index=False)
        st.download_button(
            label="Download Example CSV",
            data=csv,
            file_name="example_keywords.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📚 [Documentation](https://github.com/adeelciit786-hue/CCAD)**")
with col2:
    st.markdown("**🐛 [Report Issues](https://github.com/adeelciit786-hue/CCAD/issues)**")
with col3:
    st.markdown("**⭐ [GitHub Repository](https://github.com/adeelciit786-hue/CCAD)**")

st.caption(f"Keyword Intelligence Platform v2.0.0 | Last updated: {datetime.now().strftime('%B %d, %Y')}")
