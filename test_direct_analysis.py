"""Test keyword analysis through direct function call"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

from keyword_main import KeywordIntelligenceEngine

def test_keyword_analysis():
    print("\n" + "="*60)
    print("TESTING KEYWORD ANALYSIS - DIRECT CALL")
    print("="*60 + "\n")
    
    try:
        # Load the file
        print("1. Creating engine...")
        engine = KeywordIntelligenceEngine()
        
        print("2. Loading keywords from: website traffic 2 keywords.csv")
        if not engine.load_keywords('website traffic 2 keywords.csv'):
            print("   FAILED to load keywords")
            return False
        
        if engine.keywords_df is not None:
            print(f"   SUCCESS - Loaded {len(engine.keywords_df)} keywords\n")
        else:
            print("   FAILED - keywords_df is None")
            return False
        
        print("3. Running full analysis...")
        if not engine.run_full_analysis():
            print("   FAILED - Analysis returned False")
            return False
            
        print("   SUCCESS - Analysis completed\n")
        
        print("4. Getting results summary...")
        results = engine.get_results_summary()
        print("   SUCCESS - Got results\n")
        
        # Display summary
        summary = results.get('summary', {})
        print("="*60)
        print("ANALYSIS RESULTS")
        print("="*60)
        print(f"Total keywords analyzed: {summary.get('total_keywords', 0)}")
        print(f"Keywords with issues: {summary.get('keywords_with_issues', 0)}")
        print(f"Lost search opportunities: {summary.get('lost_search_opportunities', 0)}")
        print(f"Match type conversions recommended: {summary.get('match_type_conversions_recommended', 0)}")
        print(f"New keywords suggested: {summary.get('new_keywords_suggested', 0)}")
        print(f"Total recommendations: {summary.get('total_recommendations', 0)}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_keyword_analysis()
    sys.exit(0 if success else 1)
