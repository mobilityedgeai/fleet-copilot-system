"""
Enhanced Fleet Copilot API with Advanced BI
Sistema de BI melhorado com dashboards interativos, filtros dinâmicos e IA
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # App configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['FIREBASE_API_URL'] = os.environ.get('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')
    app.config['PORT'] = int(os.environ.get('PORT', 5000))
    
    # Register blueprints
    register_blueprints(app)
    
    # Add health check
    @app.route('/health')
    @app.route('/api/health')
    def health_check():
        return {
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
        }
    
    return app

def register_blueprints(app):
    """Register all application blueprints"""
    
    # Original copilot routes
    try:
        from routes.copilot import copilot_bp
        app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
        logger.info("✅ Registered copilot blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import copilot routes: {e}")
        # Create minimal copilot routes if not available
        create_minimal_copilot_routes(app)
    
    # FlutterFlow routes
    try:
        from routes.flutterflow import flutterflow_bp
        app.register_blueprint(flutterflow_bp, url_prefix='/api/flutterflow')
        logger.info("✅ Registered flutterflow blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import flutterflow routes: {e}")
    
    # Enhanced BI routes
    try:
        from dynamic_bi_routes import dynamic_bi_bp
        app.register_blueprint(dynamic_bi_bp, url_prefix='/api/copilot')
        logger.info("✅ Registered dynamic BI blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Could not import dynamic BI routes: {e}")
        # Create minimal BI routes if not available
        create_minimal_bi_routes(app)
    
    # Enhanced dashboard routes
    add_dashboard_routes(app)

def create_minimal_copilot_routes(app):
    """Create minimal copilot routes if main routes not available"""
    
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
                'enterprise_id': enterprise_id,
                'raw_data': [
                    {
                        'id': '1',
                        'vehiclePlate': '4564564',
                        'driverName': 'Motorista Teste',
                        'itemName': 'Farol',
                        'noCompliant': False,
                        'created_at': '2024-01-15T10:30:00Z'
                    }
                ]
            }
        })

def create_minimal_bi_routes(app):
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

def add_dashboard_routes(app):
    """Add enhanced dashboard routes"""
    
    @app.route('/api/copilot/enhanced-dashboard')
    def enhanced_dashboard():
        """Serve enhanced dashboard"""
        try:
            # Try to find dashboard file in current directory
            possible_paths = [
                'dashboard_melhorado.html',
                os.path.join(os.path.dirname(__file__), 'dashboard_melhorado.html'),
                os.path.join(os.getcwd(), 'dashboard_melhorado.html')
            ]
            
            dashboard_content = None
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        dashboard_content = f.read()
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
                # Return basic dashboard if enhanced not found
                return create_basic_dashboard(), 200, {'Content-Type': 'text/html; charset=utf-8'}
                
        except Exception as e:
            logger.error(f"Error serving dashboard: {e}")
            return f"Error loading dashboard: {str(e)}", 500
    
    @app.route('/api/copilot/assets/<filename>')
    def dashboard_assets(filename):
        """Serve dashboard assets"""
        try:
            # Try to find asset file
            possible_paths = [
                filename,
                os.path.join(os.path.dirname(__file__), filename),
                os.path.join(os.getcwd(), filename)
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
            logger.error(f"Error serving asset: {e}")
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

# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Starting Enhanced Fleet Copilot API on port {port}")
    logger.info(f"🎯 Debug mode: {debug}")
    logger.info(f"🔗 Firebase API URL: {app.config['FIREBASE_API_URL']}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

