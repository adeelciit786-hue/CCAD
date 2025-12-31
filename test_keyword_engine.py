#!/usr/bin/env python
"""Test keyword engine with uploaded file"""

import sys
import traceback
from pathlib import Path

# Add keyword engine to path
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

try:
    print("Step 1: Import KeywordIntelligenceEngine...")
    from keyword_main import KeywordIntelligenceEngine
    print("  SUCCESS")
    
    print("Step 2: Create engine instance...")
    engine = KeywordIntelligenceEngine()
    print("  SUCCESS")
    
    print("Step 3: Load keywords...")
    result = engine.load_keywords('website traffic 2 keywords.csv')
    print(f"  SUCCESS - Loaded: {result}")
    
    print("Step 4: Run analysis...")
    result = engine.run_full_analysis()
    print(f"  SUCCESS - Analysis completed")
    
    print("Step 5: Get results...")
    results = engine.get_results_summary()
    print(f"  SUCCESS - Got results")
    
    print("\nALL STEPS COMPLETED SUCCESSFULLY!")
    print(f"Keywords analyzed: {results['summary'].get('total_keywords', 0)}")
    
except Exception as e:
    print(f"\nERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
