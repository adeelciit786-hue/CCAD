"""
Flask Web Server - PRODUCTION STABLE VERSION
Handles Google Ads keyword analysis with proper error handling
"""

from flask import Flask, jsonify, request, render_template, send_file
from pathlib import Path
import sys
import json
import logging
from werkzeug.exceptions import RequestEntityTooLarge
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

# Import modules
try:
    from main_windows import ChampionCleanersBot
    logger.info("ChampionCleanersBot imported successfully")
except Exception as e:
    logger.warning(f"ChampionCleanersBot import failed: {e}")
    ChampionCleanersBot = None

try:
    from keyword_main import KeywordIntelligenceEngine
    logger.info("KeywordIntelligenceEngine imported successfully")
except Exception as e:
    logger.warning(f"KeywordIntelligenceEngine import failed: {e}")
    KeywordIntelligenceEngine = None

# Create Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)

def serialize_for_json(obj):
    """Convert objects to JSON-serializable types"""
    if isinstance(obj, dict):
        return {key: serialize_for_json(val) for key, val in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, (int, float)):
        return float(obj) if isinstance(obj, float) else int(obj)
    elif obj is None or isinstance(obj, (str, bool)):
        return obj
    else:
        return str(obj)

@app.route('/')
def index():
    """Home page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Index route error: {e}")
        return jsonify({'error': 'Page not found', 'details': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': str(Path.cwd())})

@app.route('/api/analyze-keywords', methods=['POST'])
def analyze_keywords():
    """Analyze uploaded keyword CSV"""
    response_data = {'status': 'error', 'error': 'Unknown error'}
    status_code = 500
    
    try:
        logger.info("Received keyword analysis request")
        
        # Validate file
        if 'file' not in request.files:
            logger.warning("No file in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file.filename or file.filename == '':
            logger.warning("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Only CSV files allowed'}), 400
        
        # Save file
        csv_path = UPLOAD_FOLDER / file.filename
        file.save(csv_path)
        logger.info(f"Saved file: {csv_path}")
        
        # Check if engine is available
        if KeywordIntelligenceEngine is None:
            logger.error("KeywordIntelligenceEngine not available")
            return jsonify({'error': 'Keyword engine not available'}), 500
        
        # Run analysis
        logger.info("Creating keyword engine instance")
        engine = KeywordIntelligenceEngine()
        
        logger.info(f"Loading keywords from {csv_path}")
        if not engine.load_keywords(str(csv_path)):
            logger.error("Failed to load keywords")
            return jsonify({'error': 'Failed to load keywords'}), 400
        
        logger.info("Running full analysis")
        if not engine.run_full_analysis():
            logger.error("Analysis failed")
            return jsonify({'error': 'Analysis failed'}), 500
        
        logger.info("Getting results summary")
        results = engine.get_results_summary()
        summary = results.get('summary', {})
        
        response_data = {
            'status': 'success',
            'summary': {
                'total_keywords': int(summary.get('total_keywords', 0)),
                'keywords_with_issues': int(summary.get('keywords_with_issues', 0)),
                'lost_search_opportunities': int(summary.get('lost_search_opportunities', 0)),
                'match_type_conversions': int(summary.get('match_type_conversions_recommended', 0)),
                'new_keywords_suggested': int(summary.get('new_keywords_suggested', 0)),
                'total_recommendations': int(summary.get('total_recommendations', 0))
            },
            'timestamp': 'Analysis complete'
        }
        status_code = 200
        logger.info("Analysis completed successfully")
        
    except RequestEntityTooLarge:
        logger.error("File too large")
        response_data = {'error': 'File too large (max 16MB)'}
        status_code = 413
    except Exception as e:
        logger.error(f"Exception in analyze_keywords: {str(e)}", exc_info=True)
        response_data = {'error': f'Server error: {str(e)}'}
        status_code = 500
    
    return jsonify(response_data), status_code

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze campaign data"""
    try:
        logger.info("Received campaign analysis request")
        
        if ChampionCleanersBot is None:
            return jsonify({'error': 'Bot not available'}), 500
        
        use_sample = request.form.get('use_sample') == 'true'
        
        if use_sample:
            csv_path = Path(__file__).parent / 'sample_data.csv'
        else:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if not file.filename or file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            csv_path = UPLOAD_FOLDER / file.filename
            file.save(csv_path)
        
        bot = ChampionCleanersBot(str(csv_path), use_emojis=False)
        results = bot.run_analysis(verbose=False)
        
        if not results:
            return jsonify({'error': 'Analysis failed'}), 500
        
        response = {
            'status': 'success',
            'data_summary': results.get('data_summary', {}),
            'campaign_metrics': serialize_for_json(results.get('campaign_metrics', {})),
            'detected_issues': results.get('detected_issues', []),
            'recommendations': results.get('recommendations', [])[:10],
            'platform_analysis': serialize_for_json(results.get('platform_analysis', {}))
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in analyze: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.path}")
    return jsonify({'error': 'Not found', 'path': request.path}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("CHAMPION CLEANERS BOT - WEB SERVER (STABLE VERSION)")
    print("="*70)
    print("\nServer Configuration:")
    print(f"  Host: 127.0.0.1")
    print(f"  Port: 5000")
    print(f"  URL: http://localhost:5000")
    print(f"  Upload folder: {UPLOAD_FOLDER}")
    print("\nAvailable Endpoints:")
    print("  GET  /                      - Home page")
    print("  GET  /api/health            - Health check")
    print("  POST /api/analyze           - Campaign analysis")
    print("  POST /api/analyze-keywords  - Keyword analysis")
    print("\nStarting server...")
    print("="*70 + "\n")
    
    try:
        # Use threaded=True for better request handling on Windows
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True,
            use_debugger=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        sys.exit(1)
