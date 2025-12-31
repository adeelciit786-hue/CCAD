"""
Main Orchestrator Module (Windows-Compatible Version)
Coordinates data loading, analysis, and recommendation generation.
Uses text symbols instead of emojis for Windows PowerShell compatibility.
"""

import sys
import os
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.analyzer import PerformanceAnalyzer
from src.recommender import RecommendationEngine


class ChampionCleanersBot:
    """AI-powered decision-support bot for Champion Cleaners Google Ads."""
    
    def __init__(self, csv_filepath: str, use_emojis: bool = False):
        """
        Initialize the bot.
        
        Args:
            csv_filepath: Path to CSV file with campaign data
            use_emojis: Whether to use emoji symbols (disable on Windows)
        """
        self.csv_filepath = csv_filepath
        self.use_emojis = use_emojis
        self.loader = None
        self.analyzer = None
        self.recommender = None
        self.df = None
        
        # Symbol definitions
        self.icons = {
            'data': '[DATA]' if not use_emojis else '📊',
            'chart': '[CHART]' if not use_emojis else '📈',
            'warning': '[WARN]' if not use_emojis else '⚠️',
            'success': '[OK]' if not use_emojis else '✓',
            'error': '[ERROR]' if not use_emojis else '❌',
            'bulb': '[TIP]' if not use_emojis else '💡',
            'money': '[BUDGET]' if not use_emojis else '💰',
            'trophy': '[BEST]' if not use_emojis else '🏆',
            'high': '[HIGH]' if not use_emojis else '🔴',
            'medium': '[MED]' if not use_emojis else '🟡',
            'low': '[LOW]' if not use_emojis else '🟢',
        }
    
    def run_analysis(self, verbose: bool = True) -> dict | None:
        """
        Run complete analysis and generate recommendations.
        
        Args:
            verbose: Whether to print detailed output
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        try:
            if verbose:
                print("\n" + "="*80)
                print("CHAMPION CLEANERS UAE - GOOGLE ADS DECISION SUPPORT BOT")
                print("="*80 + "\n")
            
            # Step 1: Load and validate data
            if verbose:
                print(f"{self.icons['data']} STEP 1: Loading and Validating Data")
                print("-" * 80)
            
            self.loader = DataLoader(self.csv_filepath)
            self.df = self.loader.load()
            
            is_valid, warnings, errors = self.loader.validate_data_quality()
            
            if errors:
                print(f"{self.icons['error']} VALIDATION ERRORS:")
                for error in errors:
                    print(f"   • {error}")
                return None
            
            if warnings:
                print(f"{self.icons['warning']} VALIDATION WARNINGS:")
                for warning in warnings:
                    print(f"   • {warning}")
            
            summary = self.loader.get_summary()
            if verbose:
                print(f"\nData Summary:")
                print(f"  • Date Range: {summary['date_range']}")
                print(f"  • Total Campaigns: {summary['campaigns']}")
                print(f"  • Campaign Types: {', '.join(summary['campaign_types'])}")
                print(f"  • Total Impressions: {summary['total_impressions']:,}")
                print(f"  • Total Spend: AED {summary['total_cost']:,.2f}")
                print(f"  • Total Conversions: {summary['total_conversions']}")
            
            # Step 2: Performance Analysis
            if verbose:
                print(f"\n{self.icons['chart']} STEP 2: Performance Analysis")
                print("-" * 80)
            
            self.analyzer = PerformanceAnalyzer(self.df)
            campaign_metrics = self.analyzer.get_campaign_metrics()
            comparisons = self.analyzer.compare_campaigns()
            issues = self.analyzer.detect_trends_and_risks()
            
            if verbose:
                print(f"\nCampaign Performance Metrics:")
                for campaign, metrics in campaign_metrics.items():
                    print(f"\n  {campaign} ({metrics['campaign_type']})")
                    print(f"    • Impressions: {metrics['impressions']:,}")
                    print(f"    • Clicks: {metrics['clicks']:,} (CTR: {metrics['ctr']}%)")
                    print(f"    • Cost: AED {metrics['cost']:,.2f}")
                    print(f"    • Conversions: {metrics['conversions']}")
                    revenue: int | float | str = metrics['revenue']
                    if isinstance(revenue, (int, float)) and revenue > 0:
                        print(f"    • Revenue: AED {revenue:,.2f} (ROAS: {metrics['roas']:.2f}x)")
                    print(f"    • CPA: AED {metrics['cpa']:.2f} | Conv Rate: {metrics['conversion_rate']}%")
            
            # Cross-campaign comparison
            if verbose and comparisons.get('best_cpa'):
                print(f"\n{self.icons['trophy']} Cross-Campaign Insights:")
                print(f"  • Best CPA: {comparisons['best_cpa'][0]} (AED {comparisons['best_cpa'][1]:.2f})")
                print(f"  • Best ROAS: {comparisons['best_roas'][0]} ({comparisons['best_roas'][1]:.2f}x)")
                print(f"  • Best CTR: {comparisons['best_ctr'][0]} ({comparisons['best_ctr'][1]}%)")
                print(f"  • Best Conversion Rate: {comparisons['best_conversion_rate'][0]} ({comparisons['best_conversion_rate'][1]}%)")
            
            # Platform analysis
            platform_data = self.analyzer.analyze_by_platform()
            if verbose and platform_data:
                print(f"\n[PLATFORM] Platform Analysis:")
                for platform, metrics in platform_data.items():
                    print(f"\n  {platform}")
                    print(f"    • Budget: AED {metrics['cost']:,.2f} ({metrics['percentage_of_budget']}%)")
                    print(f"    • CTR: {metrics['ctr']}% | Conversion Rate: {metrics['conversion_rate']}%")
                    print(f"    • CPA: AED {metrics['cpa']:.2f} | ROAS: {metrics['roas']:.2f}x")
            
            # Device OS analysis
            device_data = self.analyzer.analyze_by_device_os()
            if verbose and device_data:
                print(f"\n[DEVICE] Device OS Analysis:")
                for device_os, metrics in device_data.items():
                    print(f"\n  {device_os}")
                    print(f"    • Budget: AED {metrics['cost']:,.2f} ({metrics['percentage_of_budget']}%)")
                    print(f"    • CTR: {metrics['ctr']}% | Conversion Rate: {metrics['conversion_rate']}%")
                    print(f"    • CPA: AED {metrics['cpa']:.2f} | ROAS: {metrics['roas']:.2f}x")
            
            # Step 3: Risk Detection
            if verbose:
                print(f"\n{self.icons['warning']} STEP 3: Risk & Trend Detection")
                print("-" * 80)
            
            if issues:
                print(f"\nDetected {len(issues)} issue(s):\n")
                for idx, issue in enumerate(issues, 1):
                    severity_icon = self.icons['high'] if issue['severity'] == "High" else self.icons['medium']
                    print(f"  {idx}. {severity_icon} [{issue['severity']}] {issue['campaign']}")
                    print(f"     Issue: {issue['description']}")
            else:
                print(f"{self.icons['success']} No major issues detected!")
            
            # Step 4: Generate Recommendations
            if verbose:
                print(f"\n{self.icons['bulb']} STEP 4: Intelligent Recommendations")
                print("-" * 80)
            
            self.recommender = RecommendationEngine(campaign_metrics, issues, comparisons)
            recommendations = self.recommender.generate_recommendations()
            
            if verbose:
                for idx, rec in enumerate(recommendations, 1):
                    confidence_icon = self.icons['high'] if rec['confidence_level'] == "High" else self.icons['medium']
                    print(f"\n  {idx}. {rec['campaign_name']}")
                    print(f"     {confidence_icon} Confidence: {rec['confidence_level']}")
                    print(f"     Issue: {rec['issue_detected']}")
                    print(f"     Action: {rec['recommendation']}")
            
            # Budget allocation recommendation
            if verbose:
                print(f"\n{self.icons['money']} STEP 5: Budget Allocation Recommendation")
                print("-" * 80)
            
            budget_rec = self.recommender.generate_budget_allocation_recommendation()
            
            if verbose:
                print(f"\nTotal Monthly Budget: AED {budget_rec['total_monthly_budget']:,.2f}\n")
                print(f"{'Campaign':<40} {'Current %':<12} {'Recommended %':<15} {'Adjust':<12}")
                print("-" * 80)
                for campaign, alloc in budget_rec['allocations'].items():
                    adjust = alloc.get('budget_adjustment', 0)
                    adjust_str = f"{adjust:+.1f}%" if adjust != 0 else "No change"
                    rec_pct = alloc.get('recommended_percentage', alloc['current_percentage'])
                    print(f"{campaign:<40} {alloc['current_percentage']:<12.1f} {rec_pct:<15.1f} {adjust_str:<12}")
            
            # Compile results
            results = {
                'status': 'success',
                'data_summary': summary,
                'campaign_metrics': campaign_metrics,
                'platform_analysis': platform_data,
                'device_analysis': device_data,
                'detected_issues': issues,
                'recommendations': recommendations,
                'budget_allocation': budget_rec
            }
            
            if verbose:
                print("\n" + "="*80)
                print("Analysis Complete!")
                print("="*80 + "\n")
            
            return results
        
        except FileNotFoundError as e:
            print(f"{self.icons['error']} Error: {str(e)}")
            return None
        except Exception as e:
            print(f"{self.icons['error']} Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def export_recommendations(self, output_path: str | None = None) -> None:
        """
        Export recommendations to JSON file.
        
        Args:
            output_path: Path to save JSON recommendations
        """
        if not self.recommender:
            print(f"{self.icons['error']} No recommendations to export. Run analysis first.")
            return
        
        if output_path is None:
            output_path = str(Path(self.csv_filepath).parent / "recommendations.json")
        
        self.recommender.export_recommendations_json(output_path)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Champion Cleaners Google Ads Decision Support Bot')
    parser.add_argument('csv_file', help='Path to CSV file with campaign data')
    parser.add_argument('--output', '-o', help='Output path for JSON recommendations')
    parser.add_argument('--no-verbose', action='store_true', help='Suppress detailed output')
    parser.add_argument('--emojis', action='store_true', help='Use emoji symbols (disable on Windows)')
    
    args = parser.parse_args()
    
    bot = ChampionCleanersBot(args.csv_file, use_emojis=args.emojis)
    results = bot.run_analysis(verbose=not args.no_verbose)
    
    if results and args.output:
        bot.export_recommendations(args.output)
    
    return results


if __name__ == '__main__':
    main()
