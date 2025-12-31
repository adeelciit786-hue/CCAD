"""
WSGI Server Launcher - Uses Waitress (Windows-compatible)
This is more stable than Flask's development server
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

from app_stable import app

if __name__ == '__main__':
    print("\n" + "="*70)
    print("STARTING WAITRESS WSGI SERVER (WINDOWS STABLE)")
    print("="*70)
    print("\nServer will be available at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("="*70 + "\n")
    
    try:
        from waitress import serve
        serve(app, host='127.0.0.1', port=5000, threads=4)
    except ImportError:
        print("ERROR: waitress not installed. Install with: pip install waitress")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
