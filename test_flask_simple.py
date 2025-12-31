"""Simple Flask server test without analysis"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/test')
def test():
    return jsonify({'message': 'Server is working'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Testing Flask Server - Simple Routes Only")
    print("="*60)
    print("Starting server on http://127.0.0.1:5000")
    print("Testing routes: /health, /test")
    print("="*60 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)
