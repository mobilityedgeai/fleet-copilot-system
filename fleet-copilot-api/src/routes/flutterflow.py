"""
Rotas otimizadas para integração FlutterFlow
Páginas mobile-first e componentes específicos para WebView
"""

from flask import Blueprint, request, jsonify, render_template_string
from flask_cors import cross_origin
import json

# Blueprint para rotas FlutterFlow
flutterflow_bp = Blueprint('flutterflow', __name__)

# Template HTML mobile-first para WebView
MOBILE_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <title>Copiloto de Frotas</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            overflow-x: hidden;
        }
        
        .container {
            padding: 16px;
            max-width: 100%;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #2563eb;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header p {
            color: #6b7280;
            font-size: 14px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-card:active {
            transform: scale(0.98);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        
        .metric-label {
            font-size: 12px;
            color: #6b7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .compliance-high { color: #10b981; }
        .compliance-medium { color: #f59e0b; }
        .compliance-low { color: #ef4444; }
        
        .insights-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .insights-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #1f2937;
        }
        
        .insight-item {
            background: #f8fafc;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border-left: 4px solid #3b82f6;
        }
        
        .insight-item.high { border-left-color: #ef4444; }
        .insight-item.medium { border-left-color: #f59e0b; }
        .insight-item.low { border-left-color: #10b981; }
        
        .insight-title {
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 4px;
        }
        
        .insight-description {
            font-size: 13px;
            color: #6b7280;
            line-height: 1.4;
        }
        
        .vehicles-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .vehicle-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px;
            background: #f8fafc;
            border-radius: 12px;
            margin-bottom: 12px;
        }
        
        .vehicle-info h4 {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 4px;
        }
        
        .vehicle-info p {
            font-size: 12px;
            color: #6b7280;
        }
        
        .vehicle-compliance {
            font-weight: 700;
            font-size: 18px;
            padding: 8px 12px;
            border-radius: 8px;
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #6b7280;
        }
        
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 56px;
            height: 56px;
            background: #3b82f6;
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 20px;
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .refresh-btn:active {
            transform: scale(0.95);
        }
        
        @media (max-width: 480px) {
            .container { padding: 12px; }
            .metrics-grid { grid-template-columns: 1fr; }
            .metric-value { font-size: 28px; }
            .header h1 { font-size: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚛 Copiloto de Frotas</h1>
            <p>Gestão Inteligente em Tempo Real</p>
        </div>
        
        <div id="content" class="loading">
            <div style="font-size: 24px; margin-bottom: 16px;">⏳</div>
            <p>Carregando dados da frota...</p>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="loadData()">🔄</button>
    
    <script>
        const API_BASE = '{{ api_base_url }}';
        const ENTERPRISE_ID = '{{ enterprise_id }}';
        const DAYS = {{ days }};
        
        async function loadData() {
            try {
                document.getElementById('content').innerHTML = `
                    <div class="loading">
                        <div style="font-size: 24px; margin-bottom: 16px;">⏳</div>
                        <p>Atualizando dados...</p>
                    </div>
                `;
                
                // Carregar dados em paralelo
                const [summaryRes, vehiclesRes, insightsRes] = await Promise.all([
                    fetch(`${API_BASE}/summary?enterpriseId=${ENTERPRISE_ID}&days=${DAYS}`),
                    fetch(`${API_BASE}/vehicles?enterpriseId=${ENTERPRISE_ID}&days=${DAYS}`),
                    fetch(`${API_BASE}/insights?enterpriseId=${ENTERPRISE_ID}&days=${DAYS}&priority=high`)
                ]);
                
                const summary = await summaryRes.json();
                const vehicles = await vehiclesRes.json();
                const insights = await insightsRes.json();
                
                renderDashboard(summary.data, vehicles.data, insights.data);
                
            } catch (error) {
                document.getElementById('content').innerHTML = `
                    <div class="loading">
                        <div style="font-size: 24px; margin-bottom: 16px;">❌</div>
                        <p>Erro ao carregar dados</p>
                        <p style="font-size: 12px; margin-top: 8px;">${error.message}</p>
                    </div>
                `;
            }
        }
        
        function renderDashboard(summary, vehicles, insights) {
            const complianceClass = summary.complianceRate >= 90 ? 'compliance-high' : 
                                  summary.complianceRate >= 70 ? 'compliance-medium' : 'compliance-low';
            
            document.getElementById('content').innerHTML = `
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">${summary.totalChecks}</div>
                        <div class="metric-label">Verificações</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value ${complianceClass}">${summary.complianceRate}%</div>
                        <div class="metric-label">Conformidade</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${summary.totalVehicles}</div>
                        <div class="metric-label">Veículos</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${summary.totalDrivers}</div>
                        <div class="metric-label">Motoristas</div>
                    </div>
                </div>
                
                ${insights.insights.length > 0 ? `
                <div class="insights-section">
                    <div class="insights-title">⚠️ Alertas Importantes</div>
                    ${insights.insights.slice(0, 3).map(insight => `
                        <div class="insight-item ${insight.priority}">
                            <div class="insight-title">${insight.title}</div>
                            <div class="insight-description">${insight.description}</div>
                        </div>
                    `).join('')}
                </div>
                ` : ''}
                
                ${vehicles.length > 0 ? `
                <div class="vehicles-section">
                    <div class="insights-title">🚛 Veículos</div>
                    ${vehicles.slice(0, 5).map(vehicle => `
                        <div class="vehicle-item">
                            <div class="vehicle-info">
                                <h4>${vehicle.vehiclePlate}</h4>
                                <p>${vehicle.totalChecks} verificações</p>
                            </div>
                            <div class="vehicle-compliance ${vehicle.complianceRate >= 90 ? 'compliance-high' : 
                                                           vehicle.complianceRate >= 70 ? 'compliance-medium' : 'compliance-low'}">
                                ${vehicle.complianceRate}%
                            </div>
                        </div>
                    `).join('')}
                </div>
                ` : ''}
            `;
        }
        
        // Carregar dados iniciais
        loadData();
        
        // Auto-refresh a cada 5 minutos
        setInterval(loadData, 5 * 60 * 1000);
        
        // Comunicação com FlutterFlow (opcional)
        window.addEventListener('message', function(event) {
            if (event.data.action === 'refresh') {
                loadData();
            }
        });
        
        // Notificar FlutterFlow quando dados carregarem
        function notifyFlutterFlow(data) {
            if (window.parent !== window) {
                window.parent.postMessage({
                    type: 'fleetData',
                    data: data
                }, '*');
            }
        }
    </script>
</body>
</html>
'''

@flutterflow_bp.route('/mobile-dashboard', methods=['GET'])
@cross_origin()
def mobile_dashboard():
    """Dashboard mobile-first otimizado para WebView FlutterFlow"""
    enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
    days = int(request.args.get('days', 30))
    api_base_url = request.args.get('apiBase', '/api/copilot')
    
    return render_template_string(
        MOBILE_DASHBOARD_TEMPLATE,
        enterprise_id=enterprise_id,
        days=days,
        api_base_url=api_base_url
    )

@flutterflow_bp.route('/widget/<widget_type>', methods=['GET'])
@cross_origin()
def widget_endpoint(widget_type):
    """Widgets específicos para FlutterFlow"""
    enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
    days = int(request.args.get('days', 30))
    
    # Importar componentes do copiloto
    from src.routes.copilot import get_copilot_components
    
    try:
        components = get_copilot_components()
        processor = components['processor']
        
        if widget_type == 'summary-card':
            summary = processor.get_checklist_summary(enterprise_id, days)
            return jsonify({
                'success': True,
                'widget': 'summary-card',
                'data': {
                    'title': 'Resumo da Frota',
                    'metrics': [
                        {'label': 'Verificações', 'value': summary['total'], 'icon': '✅'},
                        {'label': 'Conformidade', 'value': f"{summary['compliance_rate']}%", 'icon': '📊'},
                        {'label': 'Veículos', 'value': summary['vehicles'], 'icon': '🚛'},
                        {'label': 'Motoristas', 'value': summary['drivers'], 'icon': '👨‍💼'}
                    ],
                    'status': 'success' if summary['compliance_rate'] >= 90 else 'warning' if summary['compliance_rate'] >= 70 else 'error'
                }
            })
            
        elif widget_type == 'alerts-list':
            insights_engine = components['insights_engine']
            analysis = insights_engine.generate_comprehensive_analysis(enterprise_id, days)
            
            alerts = []
            for category in ['summary', 'vehicle_insights', 'driver_insights']:
                if category in analysis and 'insights' in analysis[category]:
                    for insight in analysis[category]['insights']:
                        if insight['priority'] == 'high':
                            alerts.append({
                                'id': len(alerts) + 1,
                                'title': insight['title'],
                                'description': insight['description'],
                                'priority': insight['priority'],
                                'category': category,
                                'icon': '🚨' if insight['priority'] == 'high' else '⚠️'
                            })
            
            return jsonify({
                'success': True,
                'widget': 'alerts-list',
                'data': {
                    'title': 'Alertas Críticos',
                    'alerts': alerts[:5],  # Máximo 5 alertas
                    'totalAlerts': len(alerts)
                }
            })
            
        elif widget_type == 'compliance-gauge':
            summary = processor.get_checklist_summary(enterprise_id, days)
            return jsonify({
                'success': True,
                'widget': 'compliance-gauge',
                'data': {
                    'title': 'Taxa de Conformidade',
                    'value': summary['compliance_rate'],
                    'max': 100,
                    'unit': '%',
                    'color': '#10b981' if summary['compliance_rate'] >= 90 else '#f59e0b' if summary['compliance_rate'] >= 70 else '#ef4444',
                    'status': 'Excelente' if summary['compliance_rate'] >= 90 else 'Bom' if summary['compliance_rate'] >= 70 else 'Crítico'
                }
            })
            
        else:
            return jsonify({
                'success': False,
                'error': 'Widget type not found',
                'available_widgets': ['summary-card', 'alerts-list', 'compliance-gauge']
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'widget': widget_type
        }), 500

@flutterflow_bp.route('/config', methods=['GET'])
@cross_origin()
def flutterflow_config():
    """Configuração para integração FlutterFlow"""
    return jsonify({
        'success': True,
        'config': {
            'apiBaseUrl': '/api/copilot',
            'webviewUrl': '/api/flutterflow/mobile-dashboard',
            'defaultEnterpriseId': 'sA9EmrE3ymtnBqJKcYn7',
            'defaultDays': 30,
            'widgets': [
                {
                    'type': 'summary-card',
                    'name': 'Resumo da Frota',
                    'endpoint': '/api/flutterflow/widget/summary-card',
                    'refreshInterval': 300  # 5 minutos
                },
                {
                    'type': 'alerts-list',
                    'name': 'Alertas Críticos',
                    'endpoint': '/api/flutterflow/widget/alerts-list',
                    'refreshInterval': 60   # 1 minuto
                },
                {
                    'type': 'compliance-gauge',
                    'name': 'Taxa de Conformidade',
                    'endpoint': '/api/flutterflow/widget/compliance-gauge',
                    'refreshInterval': 300  # 5 minutos
                }
            ],
            'colors': {
                'primary': '#3b82f6',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'background': '#f8fafc'
            }
        }
    })

