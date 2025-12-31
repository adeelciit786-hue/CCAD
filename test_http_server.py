"""
Simple HTTP Server - No Flask complexity
Just for testing connectivity
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'keyword_engine_v2'))

class SimpleHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        print(f"GET {self.path}")
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Welcome to Champion Cleaners Bot</h1><p>Server is running!</p></body></html>')
        
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'status': 'ok', 'message': 'Server is running'}
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': 'Not found', 'path': self.path}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 5000), SimpleHandler)
    print("\n" + "="*70)
    print("SIMPLE HTTP SERVER - TESTING CONNECTIVITY")
    print("="*70)
    print("\nServer running at: http://localhost:5000")
    print("Endpoints:")
    print("  GET /           - Home page")
    print("  GET /api/health - Health check")
    print("\nPress CTRL+C to stop")
    print("="*70 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)
