import requests
import json

try:
    # Test health endpoint first
    response = requests.get('http://127.0.0.1:5000/api/health', timeout=5)
    print("Health check:", response.status_code)
    
    # Now test analyze endpoint
    with open('website traffic 2 keywords.csv', 'rb') as f:
        files = {'file': f}
        response = requests.post('http://127.0.0.1:5000/api/analyze-keywords', files=files, timeout=30)
    
    print('Analysis Status:', response.status_code)
    data = response.json()
    
    if response.status_code == 200:
        print('\nSUCCESS! Keyword Analysis Results:')
        print('=' * 50)
        print('Total keywords analyzed:', data.get('summary', {}).get('total_keywords'))
        print('Keywords with issues:', data.get('summary', {}).get('keywords_with_issues'))
        print('Total recommendations:', data.get('summary', {}).get('total_recommendations'))
        print('Match type conversions recommended:', data.get('summary', {}).get('match_type_conversions'))
        print('New keywords suggested:', data.get('summary', {}).get('new_keywords_suggested'))
    else:
        print('Error:', data.get('error', 'Unknown error'))
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
