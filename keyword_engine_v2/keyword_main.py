"""
Keyword Intelligence Engine V2 - Main Orchestrator
Ties all keyword analysis modules together.
"""

import pandas as pd
import json
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add current directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

from keyword_loader import KeywordLoader
from keyword_audit import KeywordAuditor
from lost_demand_detector import LostDemandDetector
from match_type_optimizer import MatchTypeOptimizer
from market_insights import MarketInsights
from website_relevance_checker import WebsiteRelevanceChecker
from keyword_recommender import KeywordRecommender


class KeywordIntelligenceEngine:
    """Main orchestrator for keyword-level intelligence."""
    
    def __init__(self):
        """Initialize the keyword engine."""
        self.keywords_df = None
        self.audit = None
        self.lost_demand = None
        self.match_optimizer = None
        self.market = None
        self.recommender = None
        self.results = {}
    
    def load_keywords(self, csv_file: str) -> bool:
        """Load and validate keyword data."""
        try:
            loader = KeywordLoader(csv_file)
            self.keywords_df = loader.load()
            if self.keywords_df is None or self.keywords_df.empty:
                print("ERROR: Failed to load keywords from CSV")
                return False
            print(f"SUCCESS: Loaded {len(self.keywords_df)} keywords")
            return True
        except Exception as e:
            print(f"ERROR: Could not load keywords: {str(e)}")
            return False
    
    def run_full_analysis(self) -> bool:
        """Execute complete keyword intelligence pipeline."""
        if self.keywords_df is None or self.keywords_df.empty:
            print("ERROR: No keyword data loaded. Call load_keywords() first.")
            return False
        
        print("\n" + "="*60)
        print("KEYWORD INTELLIGENCE ENGINE V2 - RUNNING ANALYSIS")
        print("="*60)
        
        # 1. Keyword Health Audit
        print("\n[1/6] Running Keyword Health Audit...")
        try:
            self.audit = KeywordAuditor(self.keywords_df)
            audit_results = self.audit.audit_keyword_health()
            self.results['audit'] = audit_results
            print(f"Found {len(audit_results)} issues across {len(audit_results)} keywords")
        except Exception as e:
            print(f"WARNING: Audit failed: {str(e)}")
            self.results['audit'] = []
        
        # 2. Lost Demand Detection
        print("\n[2/6] Detecting Lost Searches...")
        try:
            self.lost_demand = LostDemandDetector(self.keywords_df)
            lost_searches = self.lost_demand.detect_lost_searches()
            self.results['lost_searches'] = lost_searches
            print(f"Detected {len(lost_searches)} lost search opportunities")
        except Exception as e:
            print(f"WARNING: Lost demand detection failed: {str(e)}")
            self.results['lost_searches'] = []
        
        # 3. Match Type Optimization
        print("\n[3/6] Analyzing Match Type Performance...")
        try:
            self.match_optimizer = MatchTypeOptimizer(self.keywords_df)
            match_analysis = self.match_optimizer.analyze_match_type_performance()
            match_recs = self.match_optimizer.recommend_match_type_changes()
            self.results['match_analysis'] = match_analysis
            self.results['match_recommendations'] = match_recs
            print(f"Generated {len(match_recs)} match type recommendations")
        except Exception as e:
            print(f"WARNING: Match type optimization failed: {str(e)}")
            self.results['match_recommendations'] = []
        
        # 4. Market Insights
        print("\n[4/6] Identifying Market Opportunities...")
        try:
            self.market = MarketInsights(self.keywords_df)
            trends = self.market.identify_trending_themes()
            new_keywords = self.market.identify_new_keyword_opportunities()
            location_opps = self.market.analyze_location_opportunity()
            service_gaps = self.market.identify_service_gaps()
            
            self.results['trends'] = trends
            self.results['new_keywords'] = new_keywords
            self.results['location_opportunities'] = location_opps
            self.results['service_gaps'] = service_gaps
            print(f"Found {len(new_keywords)} new keyword opportunities")
            print(f"Identified {len(service_gaps)} service gaps")
        except Exception as e:
            print(f"WARNING: Market insights failed: {str(e)}")
            self.results['new_keywords'] = []
        
        # 5. Website Alignment Analysis
        print("\n[5/7] Checking Website-Keyword Alignment...")
        try:
            from website_relevance_checker import WebsiteRelevanceChecker
            alignment_checker = WebsiteRelevanceChecker()
            alignment_results = alignment_checker.check_keyword_alignment(self.keywords_df)
            self.results['alignment_analysis'] = alignment_results
            aligned_count = len([r for r in alignment_results if r.get('status') == 'ALIGNED'])
            print(f"Analyzed keyword alignment: {aligned_count} aligned keywords")
        except Exception as e:
            print(f"WARNING: Website alignment check failed: {str(e)}")
            self.results['alignment_analysis'] = []
        
        # 6. Generate Recommendations
        print("\n[6/7] Generating Recommendations...")
        try:
            self.recommender = KeywordRecommender(
                audit_issues=self.results.get('audit', []),
                match_recommendations=self.results.get('match_recommendations', []),
                lost_searches=self.results.get('lost_searches', []),
                opportunities=self.results.get('new_keywords', [])
            )
            recommendations = self.recommender.generate_comprehensive_recommendations()
            self.results['recommendations'] = recommendations
            
            high_priority = len([r for r in recommendations if r.get('priority') == 'High'])
            print(f"Generated {len(recommendations)} total recommendations")
            print(f"High priority actions: {high_priority}")
        except Exception as e:
            print(f"WARNING: Recommendation generation failed: {str(e)}")
            self.results['recommendations'] = []
        
        # 7. Summary
        print("\n[7/7] Building Summary Report...")
        self._build_summary_report()
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        return True
    
    def _build_summary_report(self):
        """Build summary statistics."""
        summary = {
            'total_keywords': len(self.keywords_df) if self.keywords_df is not None else 0,
            'keywords_with_issues': len(self.results.get('audit', [])),
            'lost_search_opportunities': len(self.results.get('lost_searches', [])),
            'match_type_conversions_recommended': len(self.results.get('match_recommendations', [])),
            'new_keywords_suggested': len(self.results.get('new_keywords', [])),
            'total_recommendations': len(self.results.get('recommendations', []))
        }
        self.results['summary'] = summary
    
    def print_report(self):
        """Print analysis report to console."""
        if not self.results:
            print("No analysis results. Run run_full_analysis() first.")
            return
        
        print("\n" + "="*80)
        print("KEYWORD INTELLIGENCE ENGINE V2 - ANALYSIS REPORT")
        print("="*80)
        
        # Summary
        summary = self.results.get('summary', {})
        print(f"\nKEYWORD PORTFOLIO OVERVIEW")
        print(f"  Total Keywords: {summary.get('total_keywords', 0)}")
        print(f"  Keywords with Issues: {summary.get('keywords_with_issues', 0)}")
        print(f"  Lost Search Opportunities: {summary.get('lost_search_opportunities', 0)}")
        print(f"  Match Type Conversions Recommended: {summary.get('match_type_conversions_recommended', 0)}")
        print(f"  New Keywords to Add: {summary.get('new_keywords_suggested', 0)}")
        
        # Top Issues
        audit_issues = self.results.get('audit', [])
        if audit_issues:
            print(f"\nTOP HEALTH ISSUES (Showing first 5):")
            for i, issue in enumerate(audit_issues[:5], 1):
                print(f"  {i}. [{issue.get('campaign', 'N/A')}] {issue['keyword']} - {issue['issue_type']}")
                print(f"     Value: {issue.get('value', 'N/A')}")
        
        # Top Recommendations
        recs = self.results.get('recommendations', [])
        if recs:
            print(f"\nTOP 5 ACTIONABLE RECOMMENDATIONS:")
            for i, rec in enumerate(recs[:5], 1):
                print(f"  {i}. [{rec.get('priority', 'Medium')}] {rec['keyword']}")
                print(f"     Action: {rec.get('action', 'N/A')}")
                print(f"     Reason: {rec['problem']}")
        
        # Service Gaps
        service_gaps = self.results.get('service_gaps', [])
        if service_gaps:
            print(f"\nSERVICE GAPS IDENTIFIED:")
            for gap in service_gaps:
                print(f"  • {gap['service']} - {gap.get('gap_type', 'Unknown')}")
        
        # Opportunities
        opportunities = self.results.get('new_keywords', [])
        if opportunities:
            print(f"\nNEW KEYWORD OPPORTUNITIES:")
            for opp in opportunities:
                print(f"  • {opp.get('suggested_keyword', 'N/A')} ({opp.get('intent_type', 'N/A')})")
        
        print("\n" + "="*80)
    
    def export_results_json(self, output_file: str) -> bool:
        """Export analysis results to JSON file."""
        try:
            # Convert dataframes to dict format
            export_data = {
                'summary': self.results.get('summary', {}),
                'audit_issues': [
                    {k: (str(v) if pd.isna(v) else v) for k, v in issue.items()}
                    for issue in self.results.get('audit', [])
                ],
                'lost_searches': self.results.get('lost_searches', []),
                'match_recommendations': self.results.get('match_recommendations', []),
                'new_keywords': self.results.get('new_keywords', []),
                'service_gaps': self.results.get('service_gaps', []),
                'top_recommendations': [
                    {k: (str(v) if pd.isna(v) else v) for k, v in rec.items()}
                    for rec in self.results.get('recommendations', [])[:10]
                ]
            }
            
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"SUCCESS: Results exported to {output_file}")
            return True
        except Exception as e:
            print(f"ERROR: Could not export results: {str(e)}")
            return False
    
    def get_results_summary(self) -> Dict:
        """Get results summary as dictionary."""
        return {
            'summary': self.results.get('summary', {}),
            'recommendations': self.results.get('recommendations', []),
            'audit': self.results.get('audit', []),
            'lost_searches': self.results.get('lost_searches', []),
            'match_recommendations': self.results.get('match_recommendations', []),
            'alignment_analysis': self.results.get('alignment_analysis', []),
            'new_keywords': self.results.get('new_keywords', []),
            'service_gaps': self.results.get('service_gaps', [])
        }


def main():
    """Main CLI entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python keyword_main.py <csv_file> [output_file.json]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "keyword_analysis_results.json"
    
    engine = KeywordIntelligenceEngine()
    
    if not engine.load_keywords(csv_file):
        sys.exit(1)
    
    if not engine.run_full_analysis():
        sys.exit(1)
    
    engine.print_report()
    engine.export_results_json(output_file)


if __name__ == "__main__":
    main()
