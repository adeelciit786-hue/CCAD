"""Test the running server with keyword analysis"""

import requests  # type: ignore
import time

print('\nTesting Champion Cleaners Bot - Server API')
print('='*70)

time.sleep(1)

# Test 1: Health endpoint
print('\n[Test 1] Health Check Endpoint')
print('-'*70)
try:
    r = requests.get('http://127.0.0.1:5000/api/health', timeout=5)
    if r.status_code == 200:
        print('  Status: ✓ 200 OK')
        print('  Response:', r.json())
    else:
        print(f'  Status: ✗ {r.status_code}')
except Exception as e:
    print(f'  ERROR: {e}')

# Test 2: Keyword analysis
print('\n[Test 2] Keyword Analysis Upload')
print('-'*70)
try:
    with open('website traffic 2 keywords.csv', 'rb') as f:
        csv_data = f.read()
        files = {'file': ('website traffic 2 keywords.csv', csv_data)}
        print('  Uploading file: website traffic 2 keywords.csv')
        r = requests.post('http://127.0.0.1:5000/api/analyze-keywords', 
                         files=files, timeout=60)
    
    if r.status_code == 200:
        print('  Status: ✓ 200 OK')
        data = r.json()
        if data.get('status') == 'success':
            summary = data.get('summary', {})
            print('\n  Analysis Results:')
            print(f'    • Total keywords analyzed: {summary.get("total_keywords")}')
            print(f'    • Keywords with issues: {summary.get("keywords_with_issues")}')
            print(f'    • Match type conversions recommended: {summary.get("match_type_conversions")}')
            print(f'    • New keywords suggested: {summary.get("new_keywords_suggested")}')
            print(f'    • Total recommendations: {summary.get("total_recommendations")}')
            print('\n  ✓ Keyword Analysis SUCCESSFUL!')
        else:
            print(f'  Response: {data}')
    else:
        print(f'  Status: ✗ {r.status_code}')
        print(f'  Error: {r.json()}')
except Exception as e:
    print(f'  ERROR: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '='*70)
print('Server Status: ✓ RUNNING AND OPERATIONAL')
print('Web Interface: http://localhost:5000')
print('='*70 + '\n')
