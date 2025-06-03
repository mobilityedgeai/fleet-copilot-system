import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.copilot import copilot_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para integração com FlutterFlow
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

from src.routes.flutterflow import flutterflow_bp

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
app.register_blueprint(flutterflow_bp, url_prefix='/api/flutterflow')

# uncomment if you need to use database
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # Página de boas-vindas se index.html não existir
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Fleet Copilot API</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                           margin: 0; padding: 20px; background: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; 
                                padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #2563eb; margin-bottom: 20px; }
                    .endpoint { background: #f8fafc; padding: 15px; margin: 10px 0; 
                               border-left: 4px solid #2563eb; border-radius: 5px; }
                    .method { background: #10b981; color: white; padding: 3px 8px; 
                             border-radius: 3px; font-size: 12px; font-weight: bold; }
                    .method.post { background: #f59e0b; }
                    code { background: #e5e7eb; padding: 2px 6px; border-radius: 3px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚛 Fleet Copilot API</h1>
                    <p>API do Copiloto Inteligente de Gestão de Frotas - Pronta para integração com FlutterFlow!</p>
                    
                    <h2>📋 Endpoints Disponíveis:</h2>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/copilot/health</code><br>
                        <small>Health check da API</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/copilot/summary</code><br>
                        <small>Resumo da frota (ideal para cards no FlutterFlow)</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/copilot/vehicles</code><br>
                        <small>Performance de veículos (para listas no FlutterFlow)</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/copilot/drivers</code><br>
                        <small>Performance de motoristas</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/copilot/insights</code><br>
                        <small>Insights e alertas (para notificações)</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method post">POST</span> <code>/api/copilot/question</code><br>
                        <small>Responder perguntas em linguagem natural (para chat)</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/copilot/dashboard</code><br>
                        <small>Dashboard HTML (para WebView no FlutterFlow)</small>
                    </div>
                    
                    <h2>🔗 Integração FlutterFlow:</h2>
                    <p><strong>WebView URL:</strong> <code>https://sua-app.onrender.com/api/copilot/dashboard</code></p>
                    <p><strong>API Base URL:</strong> <code>https://sua-app.onrender.com/api/copilot</code></p>
                    
                    <h2>📖 Parâmetros:</h2>
                    <ul>
                        <li><code>enterpriseId</code> - ID da empresa (padrão: sA9EmrE3ymtnBqJKcYn7)</li>
                        <li><code>days</code> - Período em dias (padrão: 30)</li>
                        <li><code>priority</code> - Prioridade dos insights (all, high, medium, low)</li>
                    </ul>
                </div>
            </body>
            </html>
            ''', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

