"""
Monthly Campaign Engine - Main Orchestrator
Ties all modules together for comprehensive monthly analysis.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

from file_loader import MonthlyFileLoader
from column_mapper import ColumnMapper
from metrics_engine import MetricsEngine
from trend_analyzer import TrendAnalyzer
from loss_detector import LossDetector
from business_context import BusinessContextAnalyzer
from recommendation_engine import RecommendationEngine


class MonthlyCampaignEngine:
    """Main orchestrator for monthly campaign analysis."""
    
    def __init__(self, data_directory: Optional[str] = None):
        """Initialize the engine."""
        if data_directory is None:
            data_directory = str(Path(__file__).parent.parent / 'uploads')
        
        self.data_directory = Path(data_directory)
        self.raw_data = None
        self.normalized_data = None
        self.metrics_data = None
        self.analysis_results = {}
    
    def run_analysis(self, output_json: bool = True, output_console: bool = True) -> Dict:
        """Run complete analysis pipeline."""
        print("=" * 80)
        print("CHAMPION CLEANERS - MONTHLY CAMPAIGN ANALYSIS ENGINE")
        print("=" * 80)
        
        # Step 1: Load data
        print("\n[1/7] Loading monthly CSV files...")
        self.raw_data = self._load_files()
        if self.raw_data is None or self.raw_data.empty:
            print("ERROR: No data loaded. Check file paths.")
            return {}
        
        print(f"✓ Loaded {len(self.raw_data)} campaign records from {self.data_directory}")
        
        # Step 2: Normalize columns
        print("\n[2/7] Normalizing column names...")
        self.normalized_data = self._map_columns()
        print(f"✓ Standardized {len(self.normalized_data.columns)} columns")
        
        # Step 3: Calculate metrics
        print("\n[3/7] Calculating performance metrics...")
        self.metrics_data = self._calculate_metrics()
        print(f"✓ Computed metrics for {self.metrics_data['campaign_name'].nunique()} campaigns across {self.metrics_data['Month'].nunique()} months")
        
        # Step 4: Analyze trends
        print("\n[4/7] Analyzing trends and seasonality...")
        trends = self._analyze_trends()
        self.analysis_results['trends'] = trends
        print(f"✓ Identified trends in {len(trends)} campaign trajectories")
        
        # Step 5: Detect losses
        print("\n[5/7] Detecting performance losses...")
        losses = self._detect_losses()
        self.analysis_results['losses'] = losses
        print(f"✓ Found {len(losses)} performance issues (sorted by severity)")
        
        # Step 6: Business context
        print("\n[6/7] Analyzing business context...")
        business_context = self._analyze_business_context()
        self.analysis_results['business_context'] = business_context
        print(f"✓ Service coverage: {sum(1 for s, m in business_context.get('service_coverage', {}).items() if m.get('status') == 'BALANCED')} balanced services")
        
        # Step 7: Generate recommendations
        print("\n[7/7] Generating strategic recommendations...")
        recommendations = self._generate_recommendations(trends, losses, business_context)
        self.analysis_results['recommendations'] = recommendations
        print(f"✓ Generated {recommendations['summary'].get('total_recommendations', 0)} actionable recommendations")
        
        # Output results
        if output_console:
            self._print_console_summary()
        
        if output_json:
            output_file = self._export_json()
            print(f"\n✓ Full analysis exported to: {output_file}")
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        
        return self.analysis_results
    
    def _load_files(self) -> Optional[pd.DataFrame]:
        """Load monthly CSV files."""
        loader = MonthlyFileLoader(str(self.data_directory))
        
        files = loader.find_monthly_files()
        if not files:
            return None
        
        return loader.combine_all_months()
    
    def _map_columns(self) -> pd.DataFrame:
        """Normalize column names."""
        assert self.raw_data is not None, "No data loaded"
        mapper = ColumnMapper(self.raw_data)
        df, _ = mapper.map_and_clean()  # Unpack tuple
        return df
    
    def _calculate_metrics(self) -> pd.DataFrame:
        """Calculate performance metrics."""
        assert self.normalized_data is not None, "No normalized data"
        engine = MetricsEngine(self.normalized_data)
        return engine.calculate_all_metrics()
    
    def _analyze_trends(self) -> Dict:
        """Analyze trends across months."""
        assert self.metrics_data is not None, "No metrics data"
        analyzer = TrendAnalyzer(self.metrics_data)
        
        return {
            'growth_trends': analyzer.detect_growth_trends(),
            'seasonal_patterns': analyzer.detect_seasonal_patterns(),
            'volatility': analyzer.detect_volatility(),
            'month_over_month_changes': analyzer.calculate_month_over_month_change('conversions')
        }
    
    def _detect_losses(self) -> list:
        """Detect performance losses."""
        assert self.metrics_data is not None, "No metrics data"
        detector = LossDetector(self.metrics_data)
        return detector.get_all_losses()
    
    def _analyze_business_context(self) -> Dict:
        """Analyze business context."""
        assert self.metrics_data is not None, "No metrics data"
        analyzer = BusinessContextAnalyzer(self.metrics_data)
        return analyzer.get_context_summary()
    
    def _generate_recommendations(self, trends: Dict, losses: list, 
                                 business_context: Dict) -> Dict:
        """Generate strategic recommendations."""
        assert self.metrics_data is not None, "No metrics data"
        engine = RecommendationEngine(
            self.metrics_data,
            trends,
            losses,
            business_context
        )
        
        all_recs = engine.generate_all_recommendations()
        
        # Count recommendations
        total = (len(all_recs.get('budget_recommendations', [])) +
                len(all_recs.get('loss_remediation', [])) +
                len(all_recs.get('growth_opportunities', [])) +
                len(all_recs.get('strategic_initiatives', [])))
        
        all_recs['summary']['total_recommendations'] = total
        all_recs['summary']['critical_count'] = len([
            r for r in all_recs.get('loss_remediation', [])
            if r.get('priority') == 'CRITICAL'
        ])
        all_recs['summary']['high_priority_count'] = len([
            r for rec_list in all_recs.values()
            if isinstance(rec_list, list)
            for r in rec_list
            if r.get('priority') == 'HIGH'
        ])
        all_recs['summary']['medium_priority_count'] = len([
            r for rec_list in all_recs.values()
            if isinstance(rec_list, list)
            for r in rec_list
            if r.get('priority') == 'MEDIUM'
        ])
        
        return all_recs
    
    def _print_console_summary(self):
        """Print executive summary to console."""
        print("\n" + "=" * 80)
        print("EXECUTIVE SUMMARY")
        print("=" * 80)
        
        # Data overview
        if self.metrics_data is not None:
            print(f"\n📊 CAMPAIGN OVERVIEW:")
            print(f"   • Total Campaigns: {self.metrics_data['campaign_name'].nunique()}")
            print(f"   • Months Analyzed: {self.metrics_data['Month'].nunique()}")
            print(f"   • Total Spend: AED {self.metrics_data['cost'].sum():,.2f}")
            print(f"   • Total Conversions: {int(self.metrics_data['conversions'].sum())}")
            print(f"   • Average ROI (ROAS): {self.metrics_data['roas'].mean():.2f}x")
        
        # Performance issues
        losses = self.analysis_results.get('losses', [])
        if losses:
            critical = [l for l in losses if l.get('severity') == 'HIGH']
            print(f"\n⚠️  PERFORMANCE ISSUES DETECTED:")
            print(f"   • High Severity: {len(critical)}")
            print(f"   • Total Issues: {len(losses)}")
            if critical:
                print(f"\n   Top Critical Issues:")
                for issue in critical[:3]:
                    print(f"   - {issue['campaign_name']}: {issue['description']}")
        
        # Business context
        context = self.analysis_results.get('business_context', {})
        if context:
            service_coverage = context.get('service_coverage', {})
            print(f"\n🎯 SERVICE COVERAGE:")
            balanced = sum(1 for s, m in service_coverage.items() if m.get('status') == 'BALANCED')
            gaps = sum(1 for s, m in service_coverage.items() if m.get('status') == 'UNREPRESENTED')
            print(f"   • Balanced Services: {balanced}")
            print(f"   • Missing Services: {gaps}")
        
        # Recommendations
        recs = self.analysis_results.get('recommendations', {})
        summary = recs.get('summary', {})
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"   • Total Actions: {summary.get('total_recommendations', 0)}")
        print(f"   • Critical: {summary.get('critical_count', 0)}")
        print(f"   • High Priority: {summary.get('high_priority_count', 0)}")
        print(f"   • Medium Priority: {summary.get('medium_priority_count', 0)}")
        
        # Growth opportunities
        growth = recs.get('growth_opportunities', [])
        if growth:
            print(f"\n📈 GROWTH OPPORTUNITIES:")
            for opp in growth[:3]:
                print(f"   • {opp['target']}: Scale from AED {opp['current_monthly_spend']:.2f} to AED {opp['recommended_monthly_spend']:.2f}")
    
    def _export_json(self) -> str:
        """Export full analysis to JSON."""
        assert self.metrics_data is not None, "No metrics data to export"
        output_file = self.data_directory.parent / f"monthly_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert DataFrames to serializable format
        export_data = {
            'analysis_date': datetime.now().isoformat(),
            'data_directory': str(self.data_directory),
            'summary': {
                'total_campaigns': int(self.metrics_data['campaign_name'].nunique()),
                'months_analyzed': int(self.metrics_data['Month'].nunique()),
                'total_spend': float(self.metrics_data['cost'].sum()),
                'total_conversions': int(self.metrics_data['conversions'].sum()),
                'average_roas': float(self.metrics_data['roas'].mean())
            },
            'analysis_results': self.analysis_results
        }
        
        # Make sure all values are JSON serializable
        def make_serializable(obj):
            if isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [make_serializable(item) for item in obj]
            elif isinstance(obj, pd.Timestamp):
                return obj.isoformat()
            elif isinstance(obj, (int, float, str, bool, type(None))):
                return obj
            else:
                return str(obj)
        
        export_data = make_serializable(export_data)
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return str(output_file)


def main():
    """Run analysis from command line."""
    import sys
    
    # Get directory from command line or use default
    data_dir = sys.argv[1] if len(sys.argv) > 1 else None
    
    engine = MonthlyCampaignEngine(data_dir)
    engine.run_analysis(output_json=True, output_console=True)


if __name__ == '__main__':
    main()
