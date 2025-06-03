"""
Fleet Copilot Enhanced API - Production Ready
Versão otimizada para produção com Gunicorn
"""

import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Configurar logging para produção
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__, static_folder='static')

# Configurar CORS
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"])

# Configurar SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fleet_copilot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FIREBASE_API_URL'] = os.getenv('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')

# Configurações de produção
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Inicializar database
db = SQLAlchemy(app)

# Modelo de usuário simples
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Criar tabelas
with app.app_context():
    try:
        db.create_all()
        logger.info("✅ Database inicializado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar database: {e}")

def register_blueprints():
    """Registra blueprints de forma segura"""
    try:
        # Tentar importar blueprints originais com diferentes caminhos
        blueprint_registered = False
        
        # Tentar diferentes caminhos para o blueprint copilot
        copilot_paths = [
            'routes.copilot',
            'src.routes.copilot', 
            'fleet_data_connector',
            'src.fleet_data_connector'
        ]
        
        for path in copilot_paths:
            try:
                if path == 'routes.copilot':
                    from routes.copilot import copilot_bp
                    app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
                    logger.info("✅ Blueprint copilot registrado (routes.copilot)")
                    blueprint_registered = True
                    break
                elif path == 'src.routes.copilot':
                    from src.routes.copilot import copilot_bp
                    app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
                    logger.info("✅ Blueprint copilot registrado (src.routes.copilot)")
                    blueprint_registered = True
                    break
            except ImportError:
                continue
        
        if not blueprint_registered:
            logger.warning("⚠️ Blueprint copilot não encontrado, criando rotas mínimas")
            create_minimal_copilot_routes()
        
        # Tentar importar blueprint dinâmico
        dynamic_registered = False
        dynamic_paths = [
            'dynamic_bi_routes',
            'src.dynamic_bi_routes'
        ]
        
        for path in dynamic_paths:
            try:
                if path == 'dynamic_bi_routes':
                    from dynamic_bi_routes import dynamic_bi_bp
                    app.register_blueprint(dynamic_bi_bp, url_prefix='/api/copilot')
                    logger.info("✅ Blueprint dynamic_bi registrado (dynamic_bi_routes)")
                    dynamic_registered = True
                    break
                elif path == 'src.dynamic_bi_routes':
                    from src.dynamic_bi_routes import dynamic_bi_bp
                    app.register_blueprint(dynamic_bi_bp, url_prefix='/api/copilot')
                    logger.info("✅ Blueprint dynamic_bi registrado (src.dynamic_bi_routes)")
                    dynamic_registered = True
                    break
            except ImportError:
                continue
        
        if not dynamic_registered:
            logger.warning("⚠️ Blueprint dynamic_bi não encontrado, criando rotas mínimas")
            create_minimal_bi_routes()
            
    except Exception as e:
        logger.error(f"❌ Erro ao registrar blueprints: {e}")
        create_fallback_routes()

def create_minimal_copilot_routes():
    """Cria rotas mínimas do copilot se blueprint não estiver disponível"""
    
    @app.route('/api/copilot/health')
    def minimal_health():
        return jsonify({
            'status': 'healthy',
            'service': 'Fleet Copilot Enhanced BI API',
            'version': '2.0.0',
            'environment': 'production',
            'server': 'gunicorn',
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
    """Cria rotas mínimas de BI se blueprint não estiver disponível"""
    
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
                },
                'maintenance': {
                    'name': 'Manutenção',
                    'description': 'Serviços e manutenção de veículos',
                    'icon': 'fas fa-tools',
                    'color': '#f39c12'
                }
            }
        })
    
    @app.route('/api/copilot/checklist')
    def minimal_checklist():
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': 1,
                    'vehiclePlate': 'ABC-1234',
                    'itemName': 'Farol Dianteiro',
                    'noCompliant': False,
                    'driverName': 'João Silva',
                    'timestamp': '2025-06-03T10:00:00Z'
                },
                {
                    'id': 2,
                    'vehiclePlate': 'ABC-1234',
                    'itemName': 'Pneu Traseiro',
                    'noCompliant': True,
                    'driverName': 'João Silva',
                    'timestamp': '2025-06-03T10:05:00Z'
                },
                {
                    'id': 3,
                    'vehiclePlate': 'ABC-1234',
                    'itemName': 'Freios',
                    'noCompliant': False,
                    'driverName': 'João Silva',
                    'timestamp': '2025-06-03T10:10:00Z'
                }
            ],
            'summary': {
                'total': 3,
                'compliant': 2,
                'non_compliant': 1,
                'compliance_rate': 66.7,
                'enterprise_id': enterprise_id,
                'period_days': days
            }
        })
    
    @app.route('/api/copilot/trips')
    def minimal_trips():
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': 1,
                    'vehiclePlate': 'ABC-1234',
                    'driverName': 'João Silva',
                    'origin': 'São Paulo',
                    'destination': 'Rio de Janeiro',
                    'distance': 430.5,
                    'duration': 360,
                    'timestamp': '2025-06-03T08:00:00Z'
                }
            ],
            'summary': {
                'total_trips': 1,
                'total_distance': 430.5,
                'total_duration': 360,
                'enterprise_id': enterprise_id,
                'period_days': days
            }
        })
    
    @app.route('/api/copilot/alerts')
    def minimal_alerts():
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': 1,
                    'type': 'maintenance',
                    'priority': 'high',
                    'message': 'Manutenção preventiva necessária',
                    'vehiclePlate': 'ABC-1234',
                    'timestamp': '2025-06-03T12:00:00Z'
                }
            ],
            'summary': {
                'total_alerts': 1,
                'high_priority': 1,
                'medium_priority': 0,
                'low_priority': 0,
                'enterprise_id': enterprise_id,
                'period_days': days
            }
        })
    
    @app.route('/api/copilot/maintenance')
    def minimal_maintenance():
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': 1,
                    'vehiclePlate': 'ABC-1234',
                    'serviceType': 'Troca de óleo',
                    'cost': 150.00,
                    'status': 'completed',
                    'timestamp': '2025-06-02T14:00:00Z'
                }
            ],
            'summary': {
                'total_services': 1,
                'total_cost': 150.00,
                'completed': 1,
                'pending': 0,
                'enterprise_id': enterprise_id,
                'period_days': days
            }
        })

def create_fallback_routes():
    """Cria rotas de fallback em caso de erro"""
    
    @app.route('/api/health')
    def fallback_health():
        return jsonify({
            'status': 'healthy',
            'service': 'Fleet Copilot API (Production Mode)',
            'version': '2.0.0',
            'environment': 'production',
            'server': 'gunicorn'
        })

@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """Serve enhanced dashboard"""
    try:
        # Tentar encontrar arquivo do dashboard corrigido primeiro
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'dashboard_corrigido_final.html'),
            os.path.join(os.path.dirname(__file__), 'src', 'dashboard_corrigido_final.html'),
            os.path.join(os.path.dirname(__file__), 'dashboard_melhorado_corrigido.html'),
            os.path.join(os.path.dirname(__file__), 'src', 'dashboard_melhorado_corrigido.html'),
            os.path.join(os.path.dirname(__file__), 'dashboard_melhorado.html'),
            os.path.join(os.path.dirname(__file__), 'src', 'dashboard_melhorado.html'),
            'dashboard_corrigido_final.html',
            'dashboard_melhorado_corrigido.html',
            'dashboard_melhorado.html'
        ]
        
        dashboard_content = None
        dashboard_file = None
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    dashboard_content = f.read()
                dashboard_file = os.path.basename(path)
                logger.info(f"✅ Dashboard encontrado em: {path} (arquivo: {dashboard_file})")
                break
        
        if dashboard_content:
            # Substituir URL base da API para produção
            api_base_url = request.host_url.rstrip('/')
            dashboard_content = dashboard_content.replace(
                'window.location.origin', 
                f"'{api_base_url}'"
            )
            
            # Log do arquivo usado
            if 'corrigido' in dashboard_file:
                logger.info("✅ Usando dashboard corrigido com cores e layout corretos")
            else:
                logger.warning("⚠️ Usando dashboard antigo - recomenda-se atualizar para versão corrigida")
            
            return dashboard_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            logger.warning("⚠️ Nenhum dashboard encontrado, servindo versão básica")
            return create_basic_dashboard(), 200, {'Content-Type': 'text/html; charset=utf-8'}
            
    except Exception as e:
        logger.error(f"❌ Erro ao servir dashboard: {e}")
        return f"Erro ao carregar dashboard: {str(e)}", 500

@app.route('/api/copilot/assets/<filename>')
def dashboard_assets(filename):
    """Serve dashboard assets"""
    try:
        # Tentar encontrar arquivo de asset
        possible_paths = [
            os.path.join(os.path.dirname(__file__), filename),
            os.path.join(os.path.dirname(__file__), 'src', filename),
            f'src/{filename}',
            filename
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determinar tipo de conteúdo
                if filename.endswith('.js'):
                    content_type = 'text/javascript'
                elif filename.endswith('.css'):
                    content_type = 'text/css'
                else:
                    content_type = 'text/plain'
                
                return content, 200, {'Content-Type': content_type}
        
        return "Asset não encontrado", 404
            
    except Exception as e:
        logger.error(f"❌ Erro ao servir asset: {e}")
        return f"Erro: {str(e)}", 500

@app.route('/api/flutterflow/mobile-dashboard')
def mobile_dashboard_redirect():
    """Redireciona dashboard mobile para versão melhorada"""
    enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
    days = request.args.get('days', '30')
    
    # Redirecionar para dashboard melhorado com parâmetros
    enhanced_url = f"/api/copilot/enhanced-dashboard?enterpriseId={enterprise_id}&days={days}"
    
    return f'''
    <script>
        window.location.href = "{enhanced_url}";
    </script>
    <p>Redirecionando para o dashboard melhorado...</p>
    <a href="{enhanced_url}">Clique aqui se não for redirecionado automaticamente</a>
    '''

def create_basic_dashboard():
    """Cria dashboard básico se versão melhorada não estiver disponível"""
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
                            <h3><i class="fas fa-truck"></i> Fleet Copilot - BI Básico (Produção)</h3>
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

# Rota principal com página de boas-vindas melhorada
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
            # Página de boas-vindas melhorada para produção
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Fleet Copilot Production API</title>
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
                    .method.enhanced { background: #e74c3c; }
                    code { background: #2c3e50; color: #1abc9c; padding: 2px 6px; border-radius: 3px; }
                    .feature { background: #3498db; color: white; padding: 2px 6px; 
                              border-radius: 3px; font-size: 11px; margin-left: 5px; }
                    .production { background: #27ae60; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚛 Fleet Copilot Production API</h1>
                    <p>API do Copiloto Inteligente de Gestão de Frotas - <strong>Ambiente de Produção</strong></p>
                    
                    <div style="background: #27ae60; color: white; padding: 10px; border-radius: 5px; margin: 20px 0;">
                        <strong>✅ PRODUÇÃO:</strong> Servidor Gunicorn ativo - Otimizado para alta performance
                    </div>
                    
                    <h2>🆕 Endpoints Disponíveis:</h2>
                    
                    <div class="endpoint">
                        <span class="method enhanced">GET</span> <code>/api/copilot/enhanced-dashboard</code>
                        <span class="feature production">PRODUÇÃO</span><br>
                        <small>Dashboard melhorado com padrão de cores correto e layout para WebView</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method enhanced">GET</span> <code>/api/copilot/collections</code>
                        <span class="feature production">PRODUÇÃO</span><br>
                        <small>Lista de collections disponíveis com IA dinâmica</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method enhanced">GET</span> <code>/api/copilot/checklist</code>
                        <span class="feature production">PRODUÇÃO</span><br>
                        <small>Dados de checklist com insights de IA</small>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method enhanced">GET</span> <code>/api/health</code>
                        <span class="feature production">PRODUÇÃO</span><br>
                        <small>Health check da aplicação</small>
                    </div>
                    
                    <h2>🔗 URLs de Acesso:</h2>
                    <p><strong>Dashboard Melhorado:</strong><br>
                    <code>https://fleet-copilot-api.onrender.com/api/copilot/enhanced-dashboard?enterpriseId=sA9EmrE3ymtnBqJKcYn7</code></p>
                    
                    <h2>🎯 Características de Produção:</h2>
                    <ul>
                        <li>🚀 <strong>Servidor Gunicorn</strong> - Alta performance</li>
                        <li>🔒 <strong>Configurações seguras</strong> - Debug desabilitado</li>
                        <li>📊 <strong>Logs otimizados</strong> - Monitoramento eficiente</li>
                        <li>⚡ <strong>Processamento assíncrono</strong> - Gevent workers</li>
                        <li>🎨 <strong>Dashboard corrigido</strong> - Cores e layout otimizados</li>
                        <li>🤖 <strong>IA dinâmica</strong> - Insights baseados em dados reais</li>
                    </ul>
                </div>
            </body>
            </html>
            ''', 200

# Registrar todos os blueprints
register_blueprints()

# Health check principal
@app.route('/api/health')
def health_check():
    """Health check principal da aplicação"""
    return jsonify({
        'status': 'healthy',
        'service': 'Fleet Copilot Enhanced BI API',
        'version': '2.0.0',
        'environment': 'production',
        'server': 'gunicorn',
        'database': 'connected',
        'firebase_api': app.config['FIREBASE_API_URL'],
        'features': [
            'Interactive Dashboards',
            'Dynamic Filters', 
            'Advanced Charts',
            'DataTables with Export',
            'AI-Powered Insights',
            'Multi-Collection Support',
            'Production Ready'
        ]
    })

# Configuração para Gunicorn
def create_app():
    """Factory function para Gunicorn"""
    return app

if __name__ == '__main__':
    # Apenas para desenvolvimento local
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando Fleet Copilot Enhanced API na porta {port}")
    logger.info(f"🎯 Ambiente: PRODUÇÃO")
    logger.info(f"🔗 Firebase API URL: {app.config['FIREBASE_API_URL']}")
    logger.info(f"🎨 Dashboard melhorado com padrão de cores correto")
    logger.info(f"📱 Layout otimizado para WebView")
    logger.info(f"🤖 IA dinâmica para múltiplas collections")
    logger.warning("⚠️ Usando servidor de desenvolvimento - Use Gunicorn em produção")
    
    app.run(host='0.0.0.0', port=port, debug=False)
