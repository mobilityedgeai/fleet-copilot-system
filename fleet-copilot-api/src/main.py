"""
Enhanced Fleet Copilot API with Advanced BI
Sistema de BI melhorado com dashboards interativos, filtros dinâmicos e IA
"""

import os
import sys
import logging

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enhanced configuration
app.config['FIREBASE_API_URL'] = os.environ.get('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com' )
app.config['PORT'] = int(os.environ.get('PORT', 5000))

# Configure CORS for FlutterFlow integration
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Import and register blueprints
def register_blueprints():
    """Register all application blueprints"""
    
    # Original user routes
    try:
        from src.models.user import db
        from src.routes.user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api')
        logger.info("✅ Registered user blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import user routes: {e}")
    
    # Original copilot routes
    try:
        from src.routes.copilot import copilot_bp
        app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
        logger.info("✅ Registered copilot blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import copilot routes: {e}")
        create_minimal_copilot_routes()
    
    # FlutterFlow routes
    try:
        from src.routes.flutterflow import flutterflow_bp
        app.register_blueprint(flutterflow_bp, url_prefix='/api/flutterflow')
        logger.info("✅ Registered flutterflow blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import flutterflow routes: {e}")
    
    # Enhanced BI routes
    try:
        from src.dynamic_bi_routes import dynamic_bi_bp
        app.register_blueprint(dynamic_bi_bp, url_prefix='/api/copilot')
        logger.info("✅ Registered dynamic BI blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import dynamic BI routes: {e}")
        create_minimal_bi_routes()

def create_minimal_copilot_routes():
    """Create minimal copilot routes if main routes not available"""
    
    @app.route('/api/copilot/health')
    def minimal_health():
        return jsonify({
            'status': 'healthy',
            'service': 'Fleet Copilot Enhanced BI API',
            'version': '2.0.0',
            'features': [
                'Interactive Dashboards',
                'Dynamic Filters',
                'Advanced Charts',
                'DataTables with Export',
                'AI-Powered Insights',
                'Multi-Collection Support'
            ]
        })
    
    @app.route('/api/copilot/summary')
    def minimal_summary():
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        return jsonify({
            'success': True,
            'data': {
                'total': 3,
                'compliant': 3,
                'compliance_rate': 100.0,
                'vehicles': 1,
                'drivers': 1,
                'period_days': days,
                'enterprise_id': enterprise_id
            }
        })

def create_minimal_bi_routes():
    """Create minimal BI routes if dynamic routes not available"""
    
    @app.route('/api/copilot/collections')
    def minimal_collections():
        return jsonify({
            'success': True,
            'data': {
                'checklist': {
                    'name': 'Checklist de Veículos',
                    'description': 'Inspeções e verificações de conformidade',
                    'icon': 'fas fa-clipboard-check',
                    'color': '#1abc9c'
                },
                'trips': {
                    'name': 'Viagens',
                    'description': 'Histórico de viagens e rotas',
                    'icon': 'fas fa-route',
                    'color': '#3498db'
                },
                'alerts': {
                    'name': 'Alertas',
                    'description': 'Alertas e notificações do sistema',
                    'icon': 'fas fa-exclamation-triangle',
                    'color': '#e74c3c'
                }
            }
        })

# Enhanced dashboard routes
@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """Serve enhanced dashboard"""
    try:
        # Try to find dashboard file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'src', 'dashboard_melhorado.html'),
            os.path.join(os.path.dirname(__file__), 'dashboard_melhorado.html'),
            'src/dashboard_melhorado.html',
            'dashboard_melhorado.html'
        ]
        
        dashboard_content = None
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    dashboard_content = f.read()
                logger.info(f"✅ Found dashboard at: {path}")
                break
        
        if dashboard_content:
            # Replace API base URL for production
            api_base_url = request.host_url.rstrip('/')
            dashboard_content = dashboard_content.replace(
                'window.location.origin', 
                f"'{api_base_url}'"
            )
            
            return dashboard_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            logger.warning("⚠️ Enhanced dashboard not found, serving basic version")
            return create_basic_dashboard(), 200, {'Content-Type': 'text/html; charset=utf-8'}
            
    except Exception as e:
        logger.error(f"❌ Error serving dashboard: {e}")
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/api/copilot/assets/<filename>')
def dashboard_assets(filename):
    """Serve dashboard assets"""
    try:
        # Try to find asset file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'src', filename),
            os.path.join(os.path.dirname(__file__), filename),
            f'src/{filename}',
            filename
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determine content type
                if filename.endswith('.js'):
                    content_type = 'text/javascript'
                elif filename.endswith('.css'):
                    content_type = 'text/css'
                else:
                    content_type = 'text/plain'
                
                return content, 200, {'Content-Type': content_type}
        
        return "Asset not found", 404
            
    except Exception as e:
        logger.error(f"❌ Error serving asset: {e}")
        return f"Error: {str(e)}", 500

@app.route('/api/flutterflow/mobile-dashboard')
def mobile_dashboard_redirect():
    """Redirect mobile dashboard to enhanced version"""
    enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
    days = request.args.get('days', '30')
    
    # Redirect to enhanced dashboard with parameters
    enhanced_url = f"/api/copilot/enhanced-dashboard?enterpriseId={enterprise_id}&days={days}"
    
    return f'''
    <script>
        window.location.href = "{enhanced_url}";
    </script>
    <p>Redirecionando para o dashboard melhorado...</p>
    <a href="{enhanced_url}">Clique aqui se não for redirecionado automaticamente</a>
    '''

def create_basic_dashboard():
    """Create basic dashboard if enhanced version not available"""
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fleet Copilot - BI Básico</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { background: #2c3e50; color: #ecf0f1; }
            .card { background: #34495e; border: none; }
            .btn-primary { background: #1abc9c; border-color: #1abc9c; }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3><i class="fas fa-truck"></i> Fleet Copilot - BI Básico</h3>
                        </div>
                        <div class="card-body">
                            <div class="alert alert-info">
                                <h5><i class="fas fa-info-circle"></i> Dashboard Básico</h5>
                                <p>O dashboard melhorado não foi encontrado. Esta é uma versão básica.</p>
                                <p>Para usar o dashboard completo, certifique-se de que todos os arquivos foram enviados corretamente.</p>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="card text-center">
                                        <div class="card-body">
                                            <h5>3</h5>
                                            <p>Verificações</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card text-center">
                                        <div class="card-body">
                                            <h5>100%</h5>
                                            <p>Conformidade</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card text-center">
                                        <div class="card-body">
                                            <h5>1</h5>
                                            <p>Veículos</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card text-center">
                                        <div class="card-body">
                                            <h5>1</h5>
                                            <p>Motoristas</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

# Original serve route with enhanced welcome page
@app.route('/', defaults={'path': ''} )
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
            # Enhanced welcome page
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Fleet Copilot Enhanced API</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                           margin: 0; padding: 20px; background: #2c3e50; color: #ecf0f1; }
                    .container { max-width: 900px; margin: 0 auto; background: #34495e; 
                                padding: 30px; border-radius: 10px; box-shadow: 0 2px 20px rgba(0,0,0,0.3); }
                    h1 { color: #1abc9c; margin-bottom: 20px; }
                    h2 { color: #3498db; margin-top: 30px; }
                    .endpoint { background: #2c3e50; padding: 15px; margin: 10px 0; 
                               border-left: 4px solid #1abc9c; border-radius: 5px; }
                    .method { background: #27ae60; color: white; padding: 3px 8px; 
                             border-radius: 3px; font-size: 12px; font-weight: bold; }
                    .method.post { background: #f39c12; }
                    .method.enhanced { background: #e74c3c; }
                    code { background: #2c3e50; color: #1abc9c; padding: 2px 6px; border-radius: 3px; }
                    .feature { background: #3498db; color: white; padding: 2px 6px; 
                              border-radius: 3px; font-size: 11px; margin-left: 5px; }
                    .new { background: #e74c3c; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚛 Fleet Copilot Enhanced API</h1>
                    <p>API do Copiloto Inteligente de Gestão de Frotas com BI Avançado - Pronta para integração!</p>
                    
                    <h2>🆕 Novos Endpoints (BI Melhorado):</h2>
                    
                    <div class="endpoint">
                        <span class="method enhanced">GET</span> <code>/api/copilot/enhanced-dashboard</code>
                        <span class="feature new">NOVO</span><br>
                        <small>Dashboard melhorado com filtros, gráficos avançados e DataTables</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method enhanced">GET</span> <code>/api/copilot/collections</code>
                        <span class="feature new">NOVO</span><br>
                        <small>Lista de collections disponíveis com IA dinâmica</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method enhanced">GET</span> <code>/api/copilot/assets/{filename}</code>
                        <span class="feature new">NOVO</span><br>
                        <small>Assets do dashboard (JS, CSS)</small>
                    </div>
                    
                    <h2>📋 Endpoints Originais:</h2>
                    
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
                    
                    <h2>🔗 URLs de Acesso:</h2>
                    <p><strong>Dashboard Melhorado:</strong><br>
                    <code>https://sua-app.onrender.com/api/copilot/enhanced-dashboard?enterpriseId=sA9EmrE3ymtnBqJKcYn7</code></p>
                    
                    <p><strong>Dashboard Mobile (FlutterFlow ):</strong><br>
                    <code>https://sua-app.onrender.com/api/flutterflow/mobile-dashboard?enterpriseId=sA9EmrE3ymtnBqJKcYn7</code></p>
                    
                    <h2>🎯 Funcionalidades do BI Melhorado:</h2>
                    <ul>
                        <li>🎨 <strong>Tema escuro</strong> com cores personalizadas</li>
                        <li>🔍 <strong>Filtros interativos</strong> com persistência</li>
                        <li>📊 <strong>Gráficos avançados</strong> com Chart.js</li>
                        <li>📋 <strong>DataTables</strong> com exportação Excel/PDF</li>
                        <li>🤖 <strong>IA dinâmica</strong> para múltiplas collections</li>
                        <li>📱 <strong>Responsivo</strong> para todos os dispositivos</li>
                    </ul>
                </div>
            </body>
            </html>
            ''', 200

# Register all blueprints
register_blueprints( )

# Database configuration (commented out as in original)
# uncomment if you need to use database
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Starting Enhanced Fleet Copilot API on port {port}")
    logger.info(f"🎯 Debug mode: {debug}")
    logger.info(f"🔗 Firebase API URL: {app.config['FIREBASE_API_URL']}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
