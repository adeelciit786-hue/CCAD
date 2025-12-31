"""Test the fixed keyword analysis API"""

import requests  # type: ignore
import json
import time

print('\n' + '='*70)
print('TESTING FIXED KEYWORD ANALYSIS API')
print('='*70)

time.sleep(2)

# Test the keyword analysis
print('\nUploading and analyzing: website traffic 2 keywords.csv')
print('-'*70)

try:
    with open('website traffic 2 keywords.csv', 'rb') as f:
        csv_data = f.read()
    
    files = {'file': ('website traffic 2 keywords.csv', csv_data)}
    
    response = requests.post(
        'http://127.0.0.1:5000/api/analyze-keywords',
        files=files,
        timeout=90
    )
    
    print(f'Response Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get('status') == 'success':
            print('\n✓ Analysis SUCCESSFUL!\n')
            
            summary = data.get('summary', {})
            print('SUMMARY:')
            print(f'  • Total keywords analyzed: {summary.get("total_keywords")}')
            print(f'  • Keywords with issues: {summary.get("keywords_with_issues")}')
            print(f'  • Lost search opportunities: {summary.get("lost_search_opportunities")}')
            print(f'  • Match type conversions recommended: {summary.get("match_type_conversions")}')
            print(f'  • New keywords suggested: {summary.get("new_keywords_suggested")}')
            print(f'  • Total recommendations: {summary.get("total_recommendations")}')
            
            print(f'\nKEY FINDINGS:')
            print(f'  • Keyword audit items: {len(data.get("keyword_audit", []))}')
            print(f'  • Lost searches: {len(data.get("lost_searches", []))}')
            print(f'  • Match recommendations: {len(data.get("match_recommendations", []))}')
            print(f'  • New keywords: {len(data.get("new_keywords", []))}')
            print(f'  • Service gaps: {len(data.get("service_gaps", []))}')
            print(f'  • Top recommendations: {len(data.get("top_recommendations", []))}')
            
            print('\n✓ ALL TESTS PASSED - API IS WORKING!')
        else:
            print(f'\n✗ Error: {data.get("error", "Unknown error")}')
    else:
        print(f'\n✗ HTTP Error {response.status_code}')
        print(f'Response: {response.text}')
        
except Exception as e:
    print(f'\n✗ Exception: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '='*70 + '\n')
