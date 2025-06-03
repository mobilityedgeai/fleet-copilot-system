"""
Rotas da API do Copiloto Inteligente de Gestão de Frotas
Otimizado para integração com FlutterFlow - Versão Corrigida
"""

import os
import json
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin

# Importar módulos do copiloto
from src.fleet_data_connector import FleetDataConnector, FleetDataProcessor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar blueprint
copilot_bp = Blueprint('copilot', __name__)

# Inicializar componentes do copiloto (singleton)
_copilot_components = None

def get_copilot_components():
    """Inicializa componentes do copiloto (singleton pattern)"""
    global _copilot_components
    
    if _copilot_components is None:
        logger.info("Inicializando componentes do copiloto...")
        
        try:
            connector = FleetDataConnector()
            processor = FleetDataProcessor(connector)
            
            _copilot_components = {
                'connector': connector,
                'processor': processor
            }
            
            logger.info("✓ Componentes do copiloto inicializados")
        except Exception as e:
            logger.error(f"Erro ao inicializar componentes: {e}")
            raise
    
    return _copilot_components

# ============================================================================
# ROTAS PARA FLUTTERFLOW - API CALLS
# ============================================================================

@copilot_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check para verificar se a API está funcionando"""
    return jsonify({
        'status': 'healthy',
        'service': 'Fleet Copilot API',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

@copilot_bp.route('/summary', methods=['GET'])
@cross_origin()
def get_fleet_summary():
    """Obter resumo da frota - Ideal para cards no FlutterFlow"""
    try:
        # Parâmetros
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        logger.info(f"Obtendo resumo para enterprise_id: {enterprise_id}, days: {days}")
        
        # Obter componentes
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter dados
        summary = processor.get_checklist_summary(enterprise_id, days)
        
        # Formatar para FlutterFlow
        response = {
            'success': True,
            'data': {
                'totalChecks': summary['total'],
                'complianceRate': round(summary['compliance_rate'], 1),
                'compliantChecks': summary['compliant'],
                'nonCompliantChecks': summary['non_compliant'],
                'totalVehicles': summary['vehicles'],
                'totalDrivers': summary['drivers'],
                'periodDays': summary['period_days'],
                'lastUpdate': datetime.now().isoformat()
            }
        }
        
        logger.info(f"Resumo gerado com sucesso: {summary}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erro em get_fleet_summary: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao obter resumo da frota'
        }), 500

@copilot_bp.route('/vehicles', methods=['GET'])
@cross_origin()
def get_vehicles_performance():
    """Obter performance de veículos - Para lista no FlutterFlow"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        logger.info(f"Obtendo performance de veículos para enterprise_id: {enterprise_id}")
        
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter performance de veículos (retorna lista)
        vehicle_perf = processor.get_vehicle_performance(enterprise_id, days)
        
        # Formatar para FlutterFlow
        vehicles_list = []
        for vehicle in vehicle_perf:
            vehicles_list.append({
                'vehiclePlate': vehicle['vehicle_plate'],
                'totalChecks': int(vehicle['total_checks']),
                'complianceRate': round(vehicle['compliance_rate'], 1),
                'lastActivity': vehicle['last_check'],
                'status': vehicle['status'],
                'topItems': vehicle.get('top_items', [])
            })
        
        logger.info(f"Performance de {len(vehicles_list)} veículos obtida")
        
        return jsonify({
            'success': True,
            'data': vehicles_list,
            'count': len(vehicles_list)
        })
        
    except Exception as e:
        logger.error(f"Erro em get_vehicles_performance: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao obter performance de veículos'
        }), 500

@copilot_bp.route('/drivers', methods=['GET'])
@cross_origin()
def get_drivers_performance():
    """Obter performance de motoristas - Para lista no FlutterFlow"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        logger.info(f"Obtendo performance de motoristas para enterprise_id: {enterprise_id}")
        
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter performance de motoristas (retorna lista)
        driver_perf = processor.get_driver_performance(enterprise_id, days)
        
        # Formatar para FlutterFlow
        drivers_list = []
        for driver in driver_perf:
            drivers_list.append({
                'driverName': driver['driver_name'],
                'totalChecks': int(driver['total_checks']),
                'complianceRate': round(driver['compliance_rate'], 1),
                'vehiclesOperated': int(driver['vehicles_operated']),
                'lastActivity': driver['last_activity']
            })
        
        logger.info(f"Performance de {len(drivers_list)} motoristas obtida")
        
        return jsonify({
            'success': True,
            'data': drivers_list,
            'count': len(drivers_list)
        })
        
    except Exception as e:
        logger.error(f"Erro em get_drivers_performance: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao obter performance de motoristas'
        }), 500

@copilot_bp.route('/insights', methods=['GET'])
@cross_origin()
def get_insights():
    """Obter insights e alertas - Para notificações no FlutterFlow"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        priority = request.args.get('priority', 'all')  # all, high, medium, low
        
        logger.info(f"Obtendo insights para enterprise_id: {enterprise_id}")
        
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter alertas de manutenção
        alerts = processor.get_maintenance_alerts(enterprise_id)
        
        # Gerar insights básicos
        summary = processor.get_checklist_summary(enterprise_id, 30)
        
        insights = []
        
        # Insight de conformidade
        if summary['compliance_rate'] < 80:
            insights.append({
                'type': 'compliance_warning',
                'priority': 'high',
                'title': 'Taxa de Conformidade Baixa',
                'message': f'Taxa de conformidade de {summary["compliance_rate"]}% está abaixo do ideal (80%)',
                'category': 'safety'
            })
        elif summary['compliance_rate'] >= 95:
            insights.append({
                'type': 'compliance_excellent',
                'priority': 'low',
                'title': 'Excelente Conformidade',
                'message': f'Taxa de conformidade de {summary["compliance_rate"]}% está excelente!',
                'category': 'safety'
            })
        
        # Insight de atividade
        if summary['total'] == 0:
            insights.append({
                'type': 'no_activity',
                'priority': 'high',
                'title': 'Sem Atividade Recente',
                'message': 'Nenhuma verificação registrada no período',
                'category': 'operational'
            })
        
        # Converter alertas para insights
        for alert in alerts:
            insights.append({
                'type': alert['type'],
                'priority': alert['priority'],
                'title': 'Alerta de Manutenção',
                'message': alert['message'],
                'category': 'maintenance'
            })
        
        # Filtrar por prioridade se especificado
        if priority != 'all':
            insights = [i for i in insights if i['priority'] == priority]
        
        # Ordenar por prioridade
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        insights.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        logger.info(f"Gerados {len(insights)} insights")
        
        return jsonify({
            'success': True,
            'data': {
                'insights': insights,
                'alerts': alerts,
                'summary': summary,
                'totalInsights': len(insights),
                'highPriorityCount': len([i for i in insights if i['priority'] == 'high']),
                'mediumPriorityCount': len([i for i in insights if i['priority'] == 'medium']),
                'lowPriorityCount': len([i for i in insights if i['priority'] == 'low'])
            }
        })
        
    except Exception as e:
        logger.error(f"Erro em get_insights: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao obter insights'
        }), 500

@copilot_bp.route('/question', methods=['POST'])
@cross_origin()
def answer_question():
    """Responder pergunta em linguagem natural - Para chat no FlutterFlow"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        enterprise_id = data.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(data.get('days', 30))
        
        if not question:
            return jsonify({
                'success': False,
                'message': 'Pergunta é obrigatória'
            }), 400
        
        logger.info(f"Processando pergunta: {question}")
        
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter dados para contexto
        summary = processor.get_checklist_summary(enterprise_id, days)
        
        # Processar pergunta
        response = process_natural_language_question(question, summary)
        
        return jsonify({
            'success': True,
            'data': {
                'question': question,
                'answer': response,
                'timestamp': datetime.now().isoformat(),
                'context': {
                    'enterpriseId': enterprise_id,
                    'days': days
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Erro em answer_question: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao processar pergunta'
        }), 500

# ============================================================================
# ROTAS PARA WEBVIEW - PÁGINAS HTML
# ============================================================================

@copilot_bp.route('/dashboard', methods=['GET'])
@cross_origin()
def dashboard_page():
    """Página de dashboard para WebView no FlutterFlow"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        logger.info(f"Gerando dashboard para enterprise_id: {enterprise_id}")
        
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter dados
        summary = processor.get_checklist_summary(enterprise_id, days)
        vehicles = processor.get_vehicle_performance(enterprise_id, days)
        drivers = processor.get_driver_performance(enterprise_id, days)
        alerts = processor.get_maintenance_alerts(enterprise_id)
        
        # Gerar HTML do dashboard
        html_content = generate_dashboard_html(summary, vehicles, drivers, alerts, enterprise_id)
        
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"Erro em dashboard_page: {e}")
        return f"<html><body><h1>Erro ao carregar dashboard</h1><p>{str(e)}</p></body></html>", 500

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def process_natural_language_question(question: str, summary: dict) -> str:
    """Processa pergunta em linguagem natural e gera resposta contextual"""
    
    question_lower = question.lower()
    
    # Perguntas sobre conformidade
    if any(word in question_lower for word in ['conformidade', 'compliance', 'taxa']):
        return f"A taxa de conformidade atual da frota é de {summary['compliance_rate']}%. " \
               f"Foram realizadas {summary['total']} verificações, sendo {summary['compliant']} conformes " \
               f"e {summary['non_compliant']} não conformes."
    
    # Perguntas sobre veículos
    elif any(word in question_lower for word in ['veículos', 'veiculos', 'carros', 'frota']):
        return f"A frota possui {summary['vehicles']} veículos monitorados ativamente. " \
               f"Foram realizadas {summary['total']} verificações no período analisado."
    
    # Perguntas sobre motoristas
    elif any(word in question_lower for word in ['motoristas', 'drivers', 'condutores']):
        return f"Há {summary['drivers']} motoristas ativos na frota. " \
               f"Cada motorista realizou verificações durante o período."
    
    # Perguntas sobre problemas/alertas
    elif any(word in question_lower for word in ['problemas', 'alertas', 'issues', 'falhas']):
        return f"Há {summary['non_compliant']} não conformidades registradas no período. " \
               f"Recomenda-se atenção especial aos itens com falhas."
    
    # Resposta genérica
    else:
        return f"Com base na análise dos últimos {summary['period_days']} dias: " \
               f"A frota tem {summary['vehicles']} veículos, {summary['drivers']} motoristas, " \
               f"realizou {summary['total']} verificações com {summary['compliance_rate']}% de conformidade."

def generate_dashboard_html(summary, vehicles, drivers, alerts, enterprise_id):
    """Gera HTML do dashboard"""
    
    # Calcular estatísticas
    total_vehicles = len(vehicles)
    total_drivers = len(drivers)
    avg_compliance = summary['compliance_rate']
    
    # Gerar lista de veículos
    vehicles_html = ""
    for vehicle in vehicles[:5]:  # Top 5
        vehicles_html += f"""
        <div class="vehicle-card">
            <h4>{vehicle['vehicle_plate']}</h4>
            <p>Conformidade: {vehicle['compliance_rate']}%</p>
            <p>Verificações: {vehicle['total_checks']}</p>
        </div>
        """
    
    # Gerar lista de alertas
    alerts_html = ""
    for alert in alerts[:3]:  # Top 3
        priority_color = {'high': '#ff4444', 'medium': '#ffaa00', 'low': '#44ff44'}.get(alert['priority'], '#666')
        alerts_html += f"""
        <div class="alert-card" style="border-left: 4px solid {priority_color};">
            <p><strong>{alert['message']}</strong></p>
            <small>Prioridade: {alert['priority']}</small>
        </div>
        """
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Copiloto de Frotas - Dashboard</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }}
            .stat-label {{
                color: #666;
                margin-top: 5px;
            }}
            .section {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .vehicle-card, .alert-card {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 10px;
            }}
            .refresh-btn {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 50px;
                cursor: pointer;
                font-size: 18px;
            }}
            @media (max-width: 768px) {{
                .stats-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                body {{
                    padding: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <button class="refresh-btn" onclick="location.reload()">🔄</button>
        
        <div class="container">
            <div class="header">
                <h1>🚛 Copiloto de Frotas</h1>
                <p>Gestão Inteligente em Tempo Real</p>
                <small>Enterprise ID: {enterprise_id}</small>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{summary['total']}</div>
                    <div class="stat-label">Verificações</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{avg_compliance}%</div>
                    <div class="stat-label">Conformidade</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_vehicles}</div>
                    <div class="stat-label">Veículos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_drivers}</div>
                    <div class="stat-label">Motoristas</div>
                </div>
            </div>
            
            <div class="section">
                <h3>🚗 Top Veículos</h3>
                {vehicles_html if vehicles_html else '<p>Nenhum veículo encontrado</p>'}
            </div>
            
            <div class="section">
                <h3>⚠️ Alertas Ativos</h3>
                {alerts_html if alerts_html else '<p>Nenhum alerta ativo</p>'}
            </div>
            
            <div class="section">
                <h3>📊 Resumo do Período</h3>
                <p><strong>Período:</strong> Últimos {summary['period_days']} dias</p>
                <p><strong>Conformes:</strong> {summary['compliant']} verificações</p>
                <p><strong>Não Conformes:</strong> {summary['non_compliant']} verificações</p>
                <p><strong>Última Atualização:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
        </div>
        
        <script>
            // Auto-refresh a cada 5 minutos
            setTimeout(function() {{
                location.reload();
            }}, 300000);
        </script>
    </body>
    </html>
    """
    
    return html_template

