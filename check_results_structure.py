"""Check what keys are in the keyword engine results"""

from keyword_engine_v2.keyword_main import KeywordIntelligenceEngine
import json

print('\n' + '='*70)
print('ANALYZING KEYWORD ENGINE RESULTS STRUCTURE')
print('='*70 + '\n')

engine = KeywordIntelligenceEngine()

if engine.load_keywords('website traffic 2 keywords.csv'):
    print('✓ Keywords loaded\n')
    
    if engine.run_full_analysis():
        print('✓ Analysis completed\n')
        
        results = engine.get_results_summary()
        
        print('KEYS IN RESULTS:')
        print(f'  {list(results.keys())}\n')
        
        print('KEYS IN SUMMARY:')
        summary = results.get('summary', {})
        print(f'  {list(summary.keys())}\n')
        
        # Check each major key
        print('DATA STRUCTURE:')
        for key in ['audit', 'lost_searches', 'match_recommendations', 'new_keywords', 
                    'service_gaps', 'recommendations']:
            data = results.get(key, [])
            print(f'  • {key}: {type(data).__name__} - {len(data) if isinstance(data, (list, dict)) else "N/A"} items')
            if isinstance(data, list) and len(data) > 0:
                print(f'      First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else "N/A"}')
