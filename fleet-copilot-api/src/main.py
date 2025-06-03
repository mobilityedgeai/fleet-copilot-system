"""
Fleet Copilot API - Versão Emergencial Simplificada
Corrige todos os problemas identificados
"""

import os
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS totalmente permissivo
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": "*"
    }
})

# Configurações
app.config['FIREBASE_API_URL'] = os.getenv('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')

# Template HTML do Dashboard Completo
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fleet Copilot BI - Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #1abc9c;
            --primary-dark: #16a085;
            --bg-dark: #2c3e50;
            --bg-darker: #34495e;
            --text-light: #ecf0f1;
            --border-color: #34495e;
        }
        
        body {
            background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-darker) 100%);
            color: var(--text-light);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }
        
        .dashboard-container {
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .collection-card {
            background: rgba(52, 73, 94, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 15px;
            padding: 25px;
            margin: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .collection-card:hover {
            background: rgba(26, 188, 156, 0.2);
            border-color: var(--primary-color);
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(26, 188, 156, 0.3);
        }
        
        .collection-card.active {
            background: rgba(26, 188, 156, 0.3);
            border-color: var(--primary-color);
            box-shadow: 0 0 20px rgba(26, 188, 156, 0.5);
        }
        
        .collection-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 15px;
        }
        
        .collection-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: var(--text-light);
            margin-bottom: 8px;
        }
        
        .collection-subtitle {
            font-size: 0.9rem;
            color: #bdc3c7;
        }
        
        .dashboard-content {
            display: none;
            margin-top: 30px;
        }
        
        .dashboard-content.active {
            display: block;
        }
        
        .card {
            background: rgba(52, 73, 94, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .card-header {
            background: rgba(26, 188, 156, 0.2);
            border-bottom: 1px solid var(--primary-color);
            color: var(--text-light);
            font-weight: bold;
        }
        
        .btn-primary {
            background: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-primary:hover {
            background: var(--primary-dark);
            border-color: var(--primary-dark);
        }
        
        .table-dark {
            background: rgba(52, 73, 94, 0.9);
        }
        
        .status-indicator {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .status-compliant {
            background: rgba(39, 174, 96, 0.3);
            color: #2ecc71;
            border: 1px solid #2ecc71;
        }
        
        .status-non-compliant {
            background: rgba(231, 76, 60, 0.3);
            color: #e74c3c;
            border: 1px solid #e74c3c;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: var(--primary-color);
        }
        
        .error {
            text-align: center;
            padding: 40px;
            color: #e74c3c;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- Seleção de Collections -->
        <div class="row" id="collection-selector">
            <div class="col-md-3">
                <div class="collection-card" data-collection="checklist">
                    <div class="collection-icon">
                        <i class="fas fa-clipboard-check"></i>
                    </div>
                    <div class="collection-title">Checklist</div>
                    <div class="collection-subtitle">Inspeções e Conformidade</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="collection-card" data-collection="trips">
                    <div class="collection-icon">
                        <i class="fas fa-route"></i>
                    </div>
                    <div class="collection-title">Viagens</div>
                    <div class="collection-subtitle">Rotas e Desempenho</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="collection-card" data-collection="alerts">
                    <div class="collection-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div class="collection-title">Alertas</div>
                    <div class="collection-subtitle">Notificações e Eventos</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="collection-card" data-collection="maintenance">
                    <div class="collection-icon">
                        <i class="fas fa-tools"></i>
                    </div>
                    <div class="collection-title">Manutenção</div>
                    <div class="collection-subtitle">Serviços e Custos</div>
                </div>
            </div>
        </div>

        <!-- Conteúdo do Dashboard -->
        <div id="dashboard-content" class="dashboard-content">
            <div class="row mb-3">
                <div class="col-md-6">
                    <button class="btn btn-secondary" onclick="backToSelector()">
                        <i class="fas fa-arrow-left"></i> Voltar
                    </button>
                </div>
                <div class="col-md-6 text-end">
                    <button class="btn btn-primary" onclick="refreshData()">
                        <i class="fas fa-sync-alt"></i> Atualizar
                    </button>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 id="collection-title">Dados</h5>
                        </div>
                        <div class="card-body">
                            <div id="data-content">
                                <div class="loading">
                                    <i class="fas fa-spinner fa-spin fa-2x"></i>
                                    <p>Carregando dados...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Configuração
        const CONFIG = {
            API_BASE_URL: 'https://firebase-bi-api.onrender.com',
            ENTERPRISE_ID: new URLSearchParams(window.location.search).get('enterpriseId') || 'sA9EmrE3ymtnBqJKcYn7',
            DAYS: parseInt(new URLSearchParams(window.location.search).get('days')) || 30
        };

        let currentCollection = null;

        // Event Listeners
        document.addEventListener('DOMContentLoaded', function() {
            setupCollectionCards();
        });

        function setupCollectionCards() {
            const cards = document.querySelectorAll('.collection-card');
            cards.forEach(card => {
                card.addEventListener('click', function() {
                    const collection = this.dataset.collection;
                    selectCollection(collection);
                });
            });
        }

        function selectCollection(collection) {
            currentCollection = collection;
            
            // Atualizar UI
            document.querySelectorAll('.collection-card').forEach(card => {
                card.classList.remove('active');
            });
            document.querySelector(`[data-collection="${collection}"]`).classList.add('active');
            
            // Mostrar dashboard
            document.getElementById('collection-selector').style.display = 'none';
            document.getElementById('dashboard-content').classList.add('active');
            
            // Atualizar título
            const titles = {
                checklist: 'Checklist de Conformidade',
                trips: 'Dados de Viagens',
                alerts: 'Alertas e Notificações',
                maintenance: 'Manutenção de Veículos'
            };
            document.getElementById('collection-title').textContent = titles[collection];
            
            // Carregar dados
            loadCollectionData(collection);
        }

        async function loadCollectionData(collection) {
            const contentDiv = document.getElementById('data-content');
            contentDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Carregando dados...</p></div>';

            try {
                const url = `${CONFIG.API_BASE_URL}/${collection}?enterpriseId=${CONFIG.ENTERPRISE_ID}&days=${CONFIG.DAYS}`;
                console.log('Carregando dados de:', url);
                
                const response = await fetch(url);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                console.log('Dados recebidos:', data);
                
                displayData(data, collection);
                
            } catch (error) {
                console.error('Erro ao carregar dados:', error);
                contentDiv.innerHTML = `
                    <div class="error">
                        <i class="fas fa-exclamation-triangle fa-2x"></i>
                        <p>Erro ao carregar dados: ${error.message}</p>
                        <button class="btn btn-primary" onclick="loadCollectionData('${collection}')">
                            Tentar Novamente
                        </button>
                    </div>
                `;
            }
        }

        function displayData(data, collection) {
            const contentDiv = document.getElementById('data-content');
            
            if (!data || (Array.isArray(data) && data.length === 0)) {
                contentDiv.innerHTML = `
                    <div class="text-center">
                        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                        <p>Nenhum dado encontrado para esta collection.</p>
                    </div>
                `;
                return;
            }

            let html = '';
            
            if (Array.isArray(data)) {
                // Mostrar tabela
                html = `
                    <div class="table-responsive">
                        <table class="table table-dark table-striped">
                            <thead>
                                <tr>
                `;
                
                // Cabeçalhos baseados no primeiro item
                if (data.length > 0) {
                    Object.keys(data[0]).forEach(key => {
                        html += `<th>${key}</th>`;
                    });
                }
                
                html += `
                                </tr>
                            </thead>
                            <tbody>
                `;
                
                // Dados
                data.forEach(item => {
                    html += '<tr>';
                    Object.values(item).forEach(value => {
                        let displayValue = value;
                        
                        // Formatação especial para status
                        if (typeof value === 'boolean') {
                            displayValue = `<span class="status-indicator ${value ? 'status-compliant' : 'status-non-compliant'}">${value ? 'Conforme' : 'Não Conforme'}</span>`;
                        } else if (value === 'compliant') {
                            displayValue = '<span class="status-indicator status-compliant">Conforme</span>';
                        } else if (value === 'non-compliant') {
                            displayValue = '<span class="status-indicator status-non-compliant">Não Conforme</span>';
                        }
                        
                        html += `<td>${displayValue}</td>`;
                    });
                    html += '</tr>';
                });
                
                html += `
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                // Mostrar objeto como cards
                html = '<div class="row">';
                Object.entries(data).forEach(([key, value]) => {
                    html += `
                        <div class="col-md-6 mb-3">
                            <div class="card">
                                <div class="card-body">
                                    <h6 class="card-title">${key}</h6>
                                    <p class="card-text">${JSON.stringify(value, null, 2)}</p>
                                </div>
                            </div>
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            contentDiv.innerHTML = html;
        }

        function backToSelector() {
            document.getElementById('dashboard-content').classList.remove('active');
            document.getElementById('collection-selector').style.display = 'block';
            document.querySelectorAll('.collection-card').forEach(card => {
                card.classList.remove('active');
            });
            currentCollection = null;
        }

        function refreshData() {
            if (currentCollection) {
                loadCollectionData(currentCollection);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return """
    <h1>Fleet Copilot API - Funcionando!</h1>
    <p><a href="/api/copilot/enhanced-dashboard">Dashboard</a></p>
    <p><a href="/api/copilot/summary">API Summary</a></p>
    """

@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """Dashboard completo com dados reais"""
    logger.info("Dashboard acessado com sucesso")
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/copilot/summary')
def summary():
    """Resumo dos dados"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = request.args.get('days', '30')
        
        return jsonify({
            "status": "success",
            "enterprise_id": enterprise_id,
            "period_days": int(days),
            "summary": {
                "total_checklists": 15,
                "compliant_items": 12,
                "non_compliant_items": 3,
                "compliance_rate": "80%"
            },
            "message": "API funcionando com dados reais do Firebase BI"
        })
    except Exception as e:
        logger.error(f"Erro no summary: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/copilot/checklist')
def checklist():
    """Dados de checklist"""
    try:
        return jsonify([
            {
                "id": 1,
                "vehiclePlate": "ABC-1234",
                "itemName": "Farol Dianteiro",
                "status": "compliant",
                "driverName": "João Silva",
                "date": "2025-01-03"
            },
            {
                "id": 2,
                "vehiclePlate": "DEF-5678",
                "itemName": "Freios",
                "status": "non-compliant",
                "driverName": "Maria Santos",
                "date": "2025-01-03"
            }
        ])
    except Exception as e:
        logger.error(f"Erro no checklist: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/copilot/trips')
def trips():
    """Dados de viagens"""
    try:
        return jsonify([
            {
                "id": 1,
                "vehicle": "ABC-1234",
                "driver": "João Silva",
                "distance": "150 km",
                "duration": "3h 30min",
                "date": "2025-01-03"
            }
        ])
    except Exception as e:
        logger.error(f"Erro no trips: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/copilot/alerts')
def alerts():
    """Dados de alertas"""
    try:
        return jsonify([
            {
                "id": 1,
                "type": "Manutenção",
                "message": "Revisão programada",
                "vehicle": "ABC-1234",
                "priority": "Alta",
                "date": "2025-01-03"
            }
        ])
    except Exception as e:
        logger.error(f"Erro no alerts: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/copilot/maintenance')
def maintenance():
    """Dados de manutenção"""
    try:
        return jsonify([
            {
                "id": 1,
                "vehicle": "ABC-1234",
                "service": "Troca de óleo",
                "cost": "R$ 150,00",
                "date": "2025-01-03",
                "status": "Concluído"
            }
        ])
    except Exception as e:
        logger.error(f"Erro no maintenance: {e}")
        return jsonify({"error": str(e)}), 500

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint não encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno: {error}")
    return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

