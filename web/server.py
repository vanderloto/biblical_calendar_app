"""Unified server for Biblical Calendar Web - Render.com deployment.

Serves both frontend static files and backend API from a single Flask app.
Optimized for Render.com free tier deployment.

Author:
    Vander Loto - DATAMETRIA
"""

import os
import sys
from flask import send_from_directory, request, render_template_string

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import the main Flask app
from app import app

# Configure static file serving
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

# Simple HTML template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblical Calendar App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .api-test { background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #2980b9; }
        #result { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; margin-top: 20px; font-family: monospace; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌙 Biblical Calendar App</h1>
        <p><strong>Calendário bíblico-lunissolar dinâmico com cálculos astronômicos precisos</strong></p>
        
        <div class="api-test">
            <h3>🔧 Teste da API</h3>
            <p>Teste os endpoints da API REST:</p>
            <button class="btn" onclick="testHealth()">Health Check</button>
            <button class="btn" onclick="testCalendar()">Calendário 2025</button>
            <button class="btn" onclick="testCalendarVisibility()">Com Heurística</button>
        </div>
        
        <div id="result"></div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #bdc3c7;">
            <h3>📚 Endpoints Disponíveis</h3>
            <ul>
                <li><code>GET /api/health</code> - Status da aplicação</li>
                <li><code>GET /api/calendar/{year}</code> - Calendário para um ano</li>
                <li><code>GET /api/calendar/{year}?visibility=true</code> - Com heurística de visibilidade</li>
                <li><code>GET /api/calendar/{year}?academic=true</code> - Modo acadêmico (DE440)</li>
                <li><code>GET /api/export/csv/{year}</code> - Exportar CSV</li>
                <li><code>GET /api/export/ics/{year}</code> - Exportar ICS</li>
            </ul>
        </div>
    </div>

    <script>
        async function apiCall(url) {
            try {
                const response = await fetch(url);
                const data = await response.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').textContent = 'Erro: ' + error.message;
            }
        }
        
        function testHealth() {
            apiCall('/api/health');
        }
        
        function testCalendar() {
            apiCall('/api/calendar/2025');
        }
        
        function testCalendarVisibility() {
            apiCall('/api/calendar/2025?visibility=true');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def serve_index():
    """Serve the main page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/<path:path>')
def serve_static_or_spa(path):
    """Serve static files or SPA routes."""
    # Don't intercept API routes
    if path.startswith('api/'):
        return app.send_static_file('404.html'), 404
    
    # Try to serve static file if exists
    static_file_path = os.path.join(STATIC_DIR, path)
    if os.path.exists(static_file_path):
        return send_from_directory(STATIC_DIR, path)
    
    # Check if we have Vue.js index.html
    vue_index = os.path.join(STATIC_DIR, 'index.html')
    if os.path.exists(vue_index):
        return send_from_directory(STATIC_DIR, 'index.html')
    
    # Fallback to test page
    return render_template_string(HTML_TEMPLATE)

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