"""Test Flask app using test client"""

from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).parent))

from test_minimal_flask import app

def test_keyword_analysis():
    """Test using Flask test client"""
    print("\n" + "="*60)
    print("TESTING KEYWORD ANALYSIS - FLASK TEST CLIENT")
    print("="*60 + "\n")
    
    client = app.test_client()
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = client.get('/health')
        print(f"   Status: {response.status_code}")
        print(f"   Data: {response.json}")
        
        # Test keyword analysis
        print("\n2. Testing keyword analysis endpoint...")
        with open('website traffic 2 keywords.csv', 'rb') as f:
            data = {'file': (f, 'website traffic 2 keywords.csv')}
            response = client.post('/api/analyze-keywords', data=data, content_type='multipart/form-data')
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json
            if result:
                print(f"\n   SUCCESS! Results:")
                print(f"   Status: {result.get('status')}")
                summary = result.get('summary', {})
                print(f"   Total keywords: {summary.get('total_keywords')}")
                print(f"   Keywords with issues: {summary.get('keywords_with_issues')}")
                print(f"   Lost opportunities: {summary.get('lost_search_opportunities')}")
                print(f"   Match type conversions: {summary.get('match_type_conversions')}")
                print(f"   New keywords suggested: {summary.get('new_keywords_suggested')}")
                print(f"   Total recommendations: {summary.get('total_recommendations')}")
                return True
        else:
            print(f"   ERROR: {response.json}")
            return False
            
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_keyword_analysis()
    print("\n" + "="*60)
    if success:
        print("TEST PASSED - Keyword analysis working correctly!")
    else:
        print("TEST FAILED")
    print("="*60 + "\n")
    sys.exit(0 if success else 1)
