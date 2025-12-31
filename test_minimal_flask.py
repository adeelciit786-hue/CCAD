"""Minimal Flask test server with keyword analysis"""

from flask import Flask, jsonify, request
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

from keyword_main import KeywordIntelligenceEngine

app = Flask(__name__)
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/analyze-keywords', methods=['POST'])
def analyze_keywords():
    """Analyze uploaded keyword CSV file"""
    try:
        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file.filename or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files allowed'}), 400
        
        # Save the file
        csv_path = UPLOAD_FOLDER / file.filename
        file.save(csv_path)
        
        print(f"[DEBUG] Saved file to: {csv_path}")
        print(f"[DEBUG] Creating keyword engine...")
        
        # Create and run analysis
        engine = KeywordIntelligenceEngine()
        
        print(f"[DEBUG] Loading keywords...")
        if not engine.load_keywords(str(csv_path)):
            return jsonify({'error': 'Failed to load keywords'}), 400
        
        print(f"[DEBUG] Running analysis...")
        if not engine.run_full_analysis():
            return jsonify({'error': 'Analysis failed'}), 500
        
        print(f"[DEBUG] Getting results...")
        results = engine.get_results_summary()
        
        summary = results.get('summary', {})
        response = {
            'status': 'success',
            'summary': {
                'total_keywords': summary.get('total_keywords', 0),
                'keywords_with_issues': summary.get('keywords_with_issues', 0),
                'lost_search_opportunities': summary.get('lost_search_opportunities', 0),
                'match_type_conversions': summary.get('match_type_conversions_recommended', 0),
                'new_keywords_suggested': summary.get('new_keywords_suggested', 0),
                'total_recommendations': summary.get('total_recommendations', 0)
            }
        }
        
        print(f"[DEBUG] Returning response: {response}")
        return jsonify(response)
        
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("MINIMAL FLASK SERVER - KEYWORD ANALYSIS TEST")
    print("="*60)
    print("Starting server on http://127.0.0.1:5000")
    print("Endpoint: POST /api/analyze-keywords")
    print("="*60 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
