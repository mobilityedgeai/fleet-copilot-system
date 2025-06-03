"""
Rotas da API do Copiloto Inteligente de Gestão de Frotas
Otimizado para integração com FlutterFlow - Versão Corrigida (Sem undefined)
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

def safe_get(data, key, default=0):
    """Obtém valor de forma segura, retornando default se None ou inválido"""
    if not isinstance(data, dict):
        return default
    
    value = data.get(key, default)
    if value is None or (isinstance(value, float) and (value != value)):  # Check for NaN
        return default
    return value

def safe_format_number(value, decimals=1):
    """Formata número de forma segura"""
    try:
        if value is None or (isinstance(value, float) and (value != value)):
            return "0.0"
        return f"{float(value):.{decimals}f}"
    except (ValueError, TypeError):
        return "0.0"

def safe_format_message(template, **kwargs):
    """Formata mensagem de forma segura, substituindo valores None por padrões"""
    safe_kwargs = {}
    for key, value in kwargs.items():
        if value is None:
            safe_kwargs[key] = "N/A"
        elif isinstance(value, (int, float)):
            safe_kwargs[key] = safe_format_number(value)
        else:
            safe_kwargs[key] = str(value)
    
    try:
        return template.format(**safe_kwargs)
    except (KeyError, ValueError) as e:
        logger.warning(f"Erro ao formatar mensagem: {e}")
        return "Informação não disponível"

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
        
        # Validar e formatar dados com segurança
        response = {
            'success': True,
            'data': {
                'totalChecks': safe_get(summary, 'total', 0),
                'complianceRate': float(safe_format_number(safe_get(summary, 'compliance_rate', 0))),
                'compliantChecks': safe_get(summary, 'compliant', 0),
                'nonCompliantChecks': safe_get(summary, 'non_compliant', 0),
                'totalVehicles': safe_get(summary, 'vehicles', 0),
                'totalDrivers': safe_get(summary, 'drivers', 0),
                'periodDays': safe_get(summary, 'period_days', days),
                'lastUpdate': datetime.now().isoformat()
            }
        }
        
        logger.info(f"Resumo gerado com sucesso: {response['data']}")
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
        
        # Formatar para FlutterFlow com validação
        vehicles_list = []
        for vehicle in vehicle_perf:
            vehicles_list.append({
                'vehiclePlate': vehicle.get('vehicle_plate', 'N/A'),
                'totalChecks': int(safe_get(vehicle, 'total_checks', 0)),
                'complianceRate': float(safe_format_number(safe_get(vehicle, 'compliance_rate', 0))),
                'lastActivity': vehicle.get('last_check') or 'N/A',
                'status': vehicle.get('status', 'unknown'),
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
        
        # Formatar para FlutterFlow com validação
        drivers_list = []
        for driver in driver_perf:
            drivers_list.append({
                'driverName': driver.get('driver_name', 'N/A'),
                'totalChecks': int(safe_get(driver, 'total_checks', 0)),
                'complianceRate': float(safe_format_number(safe_get(driver, 'compliance_rate', 0))),
                'vehiclesOperated': int(safe_get(driver, 'vehicles_operated', 0)),
                'lastActivity': driver.get('last_activity') or 'N/A'
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
        
        # Obter dados básicos
        summary = processor.get_checklist_summary(enterprise_id, 30)
        alerts = processor.get_maintenance_alerts(enterprise_id)
        
        insights = []
        
        # Validar se há dados suficientes
        total_checks = safe_get(summary, 'total', 0)
        compliance_rate = safe_get(summary, 'compliance_rate', 0)
        
        if total_checks == 0:
            insights.append({
                'type': 'no_data',
                'priority': 'medium',
                'title': 'Sem Dados Recentes',
                'message': 'Nenhuma verificação registrada no período analisado',
                'category': 'operational'
            })
        else:
            # Insight de conformidade (apenas se há dados)
            if compliance_rate < 80:
                insights.append({
                    'type': 'compliance_warning',
                    'priority': 'high',
                    'title': 'Taxa de Conformidade Baixa',
                    'message': safe_format_message(
                        'Taxa de conformidade de {rate}% está abaixo do ideal (80%)',
                        rate=compliance_rate
                    ),
                    'category': 'safety'
                })
            elif compliance_rate >= 95:
                insights.append({
                    'type': 'compliance_excellent',
                    'priority': 'low',
                    'title': 'Excelente Conformidade',
                    'message': safe_format_message(
                        'Taxa de conformidade de {rate}% está excelente!',
                        rate=compliance_rate
                    ),
                    'category': 'safety'
                })
            else:
                insights.append({
                    'type': 'compliance_good',
                    'priority': 'low',
                    'title': 'Conformidade Adequada',
                    'message': safe_format_message(
                        'Taxa de conformidade de {rate}% está dentro do esperado',
                        rate=compliance_rate
                    ),
                    'category': 'safety'
                })
        
        # Converter alertas para insights com validação
        for alert in alerts:
            if isinstance(alert, dict) and alert.get('message'):
                insights.append({
                    'type': alert.get('type', 'maintenance'),
                    'priority': alert.get('priority', 'medium'),
                    'title': 'Alerta de Manutenção',
                    'message': str(alert.get('message', 'Alerta sem descrição')),
                    'category': 'maintenance'
                })
        
        # Se não há insights, adicionar mensagem padrão
        if not insights:
            insights.append({
                'type': 'all_good',
                'priority': 'low',
                'title': 'Tudo em Ordem',
                'message': 'Nenhum alerta ou problema identificado no momento',
                'category': 'operational'
            })
        
        # Filtrar por prioridade se especificado
        if priority != 'all':
            insights = [i for i in insights if i.get('priority') == priority]
        
        # Ordenar por prioridade
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        insights.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
        
        logger.info(f"Gerados {len(insights)} insights")
        
        return jsonify({
            'success': True,
            'data': {
                'insights': insights,
                'alerts': alerts,
                'summary': summary,
                'totalInsights': len(insights),
                'highPriorityCount': len([i for i in insights if i.get('priority') == 'high']),
                'mediumPriorityCount': len([i for i in insights if i.get('priority') == 'medium']),
                'lowPriorityCount': len([i for i in insights if i.get('priority') == 'low'])
            }
        })
        
    except Exception as e:
        logger.error(f"Erro em get_insights: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erro ao obter insights',
            'data': {
                'insights': [{
                    'type': 'error',
                    'priority': 'high',
                    'title': 'Erro no Sistema',
                    'message': 'Não foi possível carregar os insights no momento',
                    'category': 'system'
                }],
                'alerts': [],
                'summary': {},
                'totalInsights': 1,
                'highPriorityCount': 1,
                'mediumPriorityCount': 0,
                'lowPriorityCount': 0
            }
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
    
    # Validar dados do summary
    total = safe_get(summary, 'total', 0)
    compliance_rate = safe_get(summary, 'compliance_rate', 0)
    compliant = safe_get(summary, 'compliant', 0)
    non_compliant = safe_get(summary, 'non_compliant', 0)
    vehicles = safe_get(summary, 'vehicles', 0)
    drivers = safe_get(summary, 'drivers', 0)
    period_days = safe_get(summary, 'period_days', 30)
    
    # Perguntas sobre conformidade
    if any(word in question_lower for word in ['conformidade', 'compliance', 'taxa']):
        return safe_format_message(
            "A taxa de conformidade atual da frota é de {rate}%. "
            "Foram realizadas {total} verificações, sendo {compliant} conformes "
            "e {non_compliant} não conformes.",
            rate=compliance_rate, total=total, compliant=compliant, non_compliant=non_compliant
        )
    
    # Perguntas sobre veículos
    elif any(word in question_lower for word in ['veículos', 'veiculos', 'carros', 'frota']):
        return safe_format_message(
            "A frota possui {vehicles} veículos monitorados ativamente. "
            "Foram realizadas {total} verificações no período analisado.",
            vehicles=vehicles, total=total
        )
    
    # Perguntas sobre motoristas
    elif any(word in question_lower for word in ['motoristas', 'drivers', 'condutores']):
        if drivers > 0:
            return safe_format_message(
                "Há {drivers} motoristas ativos na frota. "
                "Cada motorista realizou verificações durante o período.",
                drivers=drivers
            )
        else:
            return "Não foram encontrados motoristas ativos no período analisado."
    
    # Perguntas sobre problemas/alertas
    elif any(word in question_lower for word in ['problemas', 'alertas', 'issues', 'falhas']):
        return safe_format_message(
            "Há {non_compliant} não conformidades registradas no período. "
            "Recomenda-se atenção especial aos itens com falhas.",
            non_compliant=non_compliant
        )
    
    # Resposta genérica
    else:
        return safe_format_message(
            "Com base na análise dos últimos {period_days} dias: "
            "A frota tem {vehicles} veículos, {drivers} motoristas, "
            "realizou {total} verificações com {rate}% de conformidade.",
            period_days=period_days, vehicles=vehicles, drivers=drivers, 
            total=total, rate=compliance_rate
        )

def generate_dashboard_html(summary, vehicles, drivers, alerts, enterprise_id):
    """Gera HTML do dashboard com validação de dados"""
    
    # Validar e calcular estatísticas com segurança
    total_vehicles = len(vehicles) if vehicles else 0
    total_drivers = len(drivers) if drivers else 0
    avg_compliance = safe_format_number(safe_get(summary, 'compliance_rate', 0))
    total_checks = safe_get(summary, 'total', 0)
    compliant_checks = safe_get(summary, 'compliant', 0)
    non_compliant_checks = safe_get(summary, 'non_compliant', 0)
    period_days = safe_get(summary, 'period_days', 30)
    
    # Gerar lista de veículos com validação
    vehicles_html = ""
    if vehicles and len(vehicles) > 0:
        for vehicle in vehicles[:5]:  # Top 5
            plate = vehicle.get('vehicle_plate', 'N/A')
            compliance = safe_format_number(safe_get(vehicle, 'compliance_rate', 0))
            checks = safe_get(vehicle, 'total_checks', 0)
            
            vehicles_html += f"""
            <div class="vehicle-card">
                <h4>{plate}</h4>
                <p>Conformidade: {compliance}%</p>
                <p>Verificações: {checks}</p>
            </div>
            """
    else:
        vehicles_html = '<p>Nenhum veículo encontrado no período</p>'
    
    # Gerar lista de alertas com validação
    alerts_html = ""
    if alerts and len(alerts) > 0:
        for alert in alerts[:3]:  # Top 3
            if isinstance(alert, dict) and alert.get('message'):
                priority = alert.get('priority', 'medium')
                priority_color = {'high': '#ff4444', 'medium': '#ffaa00', 'low': '#44ff44'}.get(priority, '#666')
                message = str(alert.get('message', 'Alerta sem descrição'))
                
                alerts_html += f"""
                <div class="alert-card" style="border-left: 4px solid {priority_color};">
                    <p><strong>{message}</strong></p>
                    <small>Prioridade: {priority}</small>
                </div>
                """
    
    if not alerts_html:
        alerts_html = '<p>✅ Nenhum alerta ativo no momento</p>'
    
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
            .no-data {{
                text-align: center;
                color: #666;
                font-style: italic;
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
                    <div class="stat-value">{total_checks}</div>
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
                {vehicles_html}
            </div>
            
            <div class="section">
                <h3>⚠️ Alertas Importantes</h3>
                {alerts_html}
            </div>
            
            <div class="section">
                <h3>📊 Resumo do Período</h3>
                <p><strong>Período:</strong> Últimos {period_days} dias</p>
                <p><strong>Conformes:</strong> {compliant_checks} verificações</p>
                <p><strong>Não Conformes:</strong> {non_compliant_checks} verificações</p>
                <p><strong>Última Atualização:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
        </div>
        
        <script>
            // Auto-refresh a cada 5 minutos
            setTimeout(function() {{
                location.reload();
            }}, 300000);
            
            // Log para debug
            console.log('Dashboard carregado:', {{
                totalChecks: {total_checks},
                compliance: '{avg_compliance}%',
                vehicles: {total_vehicles},
                drivers: {total_drivers}
            }});
        </script>
    </body>
    </html>
    """
    
    return html_template
