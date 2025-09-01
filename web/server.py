"""Unified server for Biblical Calendar Web - Render.com deployment.

Serves both frontend static files and backend API from a single Flask app.
Optimized for Render.com free tier deployment.

Author:
    Vander Loto - DATAMETRIA
"""

import os
import sys
from flask import send_from_directory, request

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import the main Flask app
from app import app

# Configure static file serving
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static_or_spa(path=''):
    """Serve static files or SPA routes."""
    # Don't intercept API routes - let Flask handle them
    if path.startswith('api/'):
        # This should not be reached due to route priority
        pass
    
    # Serve index.html for root
    if path == '':
        return send_from_directory(STATIC_DIR, 'index.html')
    
    # Try to serve static file
    try:
        return send_from_directory(STATIC_DIR, path)
    except:
        # For SPA routing, serve index.html
        return send_from_directory(STATIC_DIR, 'index.html')

# Health check endpoint (already exists in app.py)
# /api/health

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🚀 Starting Biblical Calendar Web Server on port {port}")
    print(f"📁 Static files directory: {STATIC_DIR}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )