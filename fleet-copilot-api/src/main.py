"""
Fleet Copilot API - Versão Emergencial Simplificada
Todas as rotas funcionando com dados mock
"""

import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__, static_folder='.')

# Configurar CORS - MUITO PERMISSIVO
CORS(app, 
     origins="*", 
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Configurações
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

@app.after_request
def after_request(response):
    """Adicionar headers CORS manualmente"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ROTAS PRINCIPAIS
@app.route('/')
def home():
    return jsonify({
        'message': 'Fleet Copilot API - Versão Emergencial',
        'status': 'active',
        'version': '1.0.0-emergency'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando',
        'timestamp': '2025-06-03T16:00:00Z'
    })

# ROTAS DO COPILOT
@app.route('/api/copilot/summary')
def copilot_summary():
    enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
    days = int(request.args.get('days', 30))
    
    return jsonify({
        'success': True,
        'data': {
            'total': 15,
            'compliant': 12,
            'non_compliant': 3,
            'compliance_rate': 80.0,
            'vehicles': 5,
            'drivers': 8,
            'period_days': days,
            'enterprise_id': enterprise_id,
            'last_updated': '2025-06-03T16:00:00Z'
        }
    })

@app.route('/api/copilot/checklist')
def copilot_checklist():
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
                'timestamp': '2025-06-03T10:00:00Z',
                'status': 'OK'
            },
            {
                'id': 2,
                'vehiclePlate': 'ABC-1234',
                'itemName': 'Pneu Traseiro',
                'noCompliant': True,
                'driverName': 'João Silva',
                'timestamp': '2025-06-03T10:05:00Z',
                'status': 'NOK'
            },
            {
                'id': 3,
                'vehiclePlate': 'DEF-5678',
                'itemName': 'Freios',
                'noCompliant': False,
                'driverName': 'Maria Santos',
                'timestamp': '2025-06-03T10:10:00Z',
                'status': 'OK'
            },
            {
                'id': 4,
                'vehiclePlate': 'GHI-9012',
                'itemName': 'Cintos de Segurança',
                'noCompliant': False,
                'driverName': 'Pedro Costa',
                'timestamp': '2025-06-03T11:00:00Z',
                'status': 'OK'
            },
            {
                'id': 5,
                'vehiclePlate': 'GHI-9012',
                'itemName': 'Extintor',
                'noCompliant': True,
                'driverName': 'Pedro Costa',
                'timestamp': '2025-06-03T11:05:00Z',
                'status': 'NOK'
            }
        ],
        'summary': {
            'total': 5,
            'compliant': 3,
            'non_compliant': 2,
            'compliance_rate': 60.0,
            'enterprise_id': enterprise_id,
            'period_days': days
        }
    })

@app.route('/api/copilot/trips')
def copilot_trips():
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
            },
            {
                'id': 2,
                'vehiclePlate': 'DEF-5678',
                'driverName': 'Maria Santos',
                'origin': 'Belo Horizonte',
                'destination': 'Brasília',
                'distance': 741.2,
                'duration': 480,
                'timestamp': '2025-06-03T09:00:00Z'
            }
        ],
        'summary': {
            'total_trips': 2,
            'total_distance': 1171.7,
            'total_duration': 840,
            'enterprise_id': enterprise_id,
            'period_days': days
        }
    })

@app.route('/api/copilot/alerts')
def copilot_alerts():
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
            },
            {
                'id': 2,
                'type': 'safety',
                'priority': 'medium',
                'message': 'Verificar pneus',
                'vehiclePlate': 'DEF-5678',
                'timestamp': '2025-06-03T13:00:00Z'
            }
        ],
        'summary': {
            'total_alerts': 2,
            'high_priority': 1,
            'medium_priority': 1,
            'low_priority': 0,
            'enterprise_id': enterprise_id,
            'period_days': days
        }
    })

@app.route('/api/copilot/maintenance')
def copilot_maintenance():
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
            },
            {
                'id': 2,
                'vehiclePlate': 'DEF-5678',
                'serviceType': 'Revisão geral',
                'cost': 350.00,
                'status': 'pending',
                'timestamp': '2025-06-03T15:00:00Z'
            }
        ],
        'summary': {
            'total_services': 2,
            'total_cost': 500.00,
            'completed': 1,
            'pending': 1,
            'enterprise_id': enterprise_id,
            'period_days': days
        }
    })

@app.route('/api/copilot/collections')
def copilot_collections():
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

# DASHBOARD ROUTES
@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """Serve o dashboard melhorado"""
    try:
        # Procurar por dashboard corrigido primeiro
        dashboard_files = [
            'dashboard_corrigido_final.html',
            'dashboard_melhorado_corrigido.html', 
            'dashboard_melhorado.html'
        ]
        
        for filename in dashboard_files:
            if os.path.exists(filename):
                logger.info(f"✅ Dashboard encontrado: {filename}")
                return send_from_directory('.', filename)
        
        # Se não encontrar nenhum, retornar dashboard básico
        logger.warning("⚠️ Nenhum dashboard encontrado, retornando básico")
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fleet Copilot BI</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #2c3e50; color: white; }
                .container { max-width: 1200px; margin: 0 auto; }
                .card { background: #34495e; padding: 20px; margin: 10px; border-radius: 8px; }
                .btn { background: #1abc9c; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
                .btn:hover { background: #16a085; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Fleet Copilot BI - Dashboard Básico</h1>
                <div class="card">
                    <h3>Sistema Funcionando</h3>
                    <p>API ativa e respondendo corretamente.</p>
                    <button class="btn" onclick="window.location.reload()">Recarregar</button>
                </div>
                <div class="card">
                    <h3>APIs Disponíveis:</h3>
                    <ul>
                        <li>/api/copilot/summary</li>
                        <li>/api/copilot/checklist</li>
                        <li>/api/copilot/trips</li>
                        <li>/api/copilot/alerts</li>
                        <li>/api/copilot/maintenance</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        logger.error(f"❌ Erro ao servir dashboard: {e}")
        return jsonify({'error': 'Dashboard não disponível'}), 500

# USERS API (para compatibilidade)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([
        {'id': 1, 'username': 'admin', 'email': 'admin@fleet.com'},
        {'id': 2, 'username': 'user', 'email': 'user@fleet.com'}
    ])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify({
        'id': 3,
        'username': data.get('username', 'new_user'),
        'email': data.get('email', 'new@fleet.com'),
        'created': True
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({
        'id': user_id,
        'username': f'user_{user_id}',
        'email': f'user_{user_id}@fleet.com'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando Fleet Copilot API Emergencial na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
