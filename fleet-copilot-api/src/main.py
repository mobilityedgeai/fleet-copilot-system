"""
Fleet Copilot API - Dashboard Corporativo
Versão 5.0.0 - Design Enterprise

Características:
- Design corporativo profissional
- Paleta de cores enterprise (#7F57636C, #14181B)
- Ícones SVG profissionais
- Interface sem header/barra superior
- Funcionalidades avançadas mantidas
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuração
app.config['DEBUG'] = False

def load_dashboard_template():
    """Carrega o template do dashboard corporativo"""
    possible_paths = [
        '/opt/render/project/src/dashboard_corporativo.html',
        'dashboard_corporativo.html',
        'src/dashboard_corporativo.html',
        '/app/dashboard_corporativo.html',
        os.path.join(os.path.dirname(__file__), 'dashboard_corporativo.html'),
        os.path.join(os.path.dirname(__file__), '..', 'dashboard_corporativo.html')
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    logger.info(f"✅ Dashboard corporativo carregado: {path}")
                    return content
        except Exception as e:
            logger.warning(f"⚠️ Erro ao carregar {path}: {e}")
            continue
    
    logger.error("❌ Dashboard corporativo não encontrado")
    return None

# Carregar template na inicialização
DASHBOARD_TEMPLATE = load_dashboard_template()

@app.route('/')
def home():
    """Página inicial da API"""
    return jsonify({
        "service": "Fleet Copilot API",
        "version": "5.0.0",
        "status": "Enterprise Ready",
        "design": "Corporate Professional",
        "features": [
            "Dashboard corporativo",
            "Paleta enterprise",
            "Ícones profissionais",
            "Interface limpa",
            "Filtros avançados",
            "Exportação Excel/PDF"
        ],
        "endpoints": {
            "dashboard": "/api/copilot/corporate-dashboard",
            "enhanced": "/api/copilot/enhanced-dashboard"
        }
    })

@app.route('/api/copilot/corporate-dashboard')
def corporate_dashboard():
    """Dashboard corporativo principal"""
    if DASHBOARD_TEMPLATE:
        logger.info("🏢 Servindo dashboard corporativo")
        return DASHBOARD_TEMPLATE
    else:
        return jsonify({
            "error": "Dashboard corporativo não disponível",
            "message": "Template não encontrado no sistema",
            "status": "error"
        }), 404

@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """Alias para compatibilidade"""
    return corporate_dashboard()

@app.route('/health')
def health_check():
    """Health check para monitoramento"""
    dashboard_status = "available" if DASHBOARD_TEMPLATE else "unavailable"
    
    return jsonify({
        "status": "healthy",
        "version": "5.0.0",
        "design": "Corporate Enterprise",
        "dashboard": dashboard_status,
        "timestamp": "2025-01-04T19:00:00Z"
    })

@app.errorhandler(404)
def not_found(error):
    """Handler para 404"""
    return jsonify({
        "error": "Endpoint não encontrado",
        "message": "Verifique a documentação da API",
        "available_endpoints": [
            "/api/copilot/corporate-dashboard",
            "/api/copilot/enhanced-dashboard",
            "/health"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para 500"""
    logger.error(f"Erro interno: {error}")
    return jsonify({
        "error": "Erro interno do servidor",
        "message": "Entre em contato com o suporte técnico",
        "status": "error"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("🚀 Iniciando Fleet Copilot API - Corporate Edition")
    logger.info(f"🎨 Design: Enterprise Professional")
    logger.info(f"🔧 Porta: {port}")
    logger.info(f"📊 Dashboard: {'Disponível' if DASHBOARD_TEMPLATE else 'Indisponível'}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
