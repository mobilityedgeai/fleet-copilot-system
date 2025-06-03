"""
Rotas da API do Copiloto Inteligente de Gestão de Frotas
Otimizado para integração com FlutterFlow
"""

import os
import json
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin

# Importar módulos do copiloto
from src.fleet_data_connector import FleetDataConnector, FleetDataProcessor
from src.fleet_visualization import FleetVisualizationEngine
from src.fleet_insights import FleetInsightsEngine
from src.fleet_reports import FleetReportGenerator

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
        
        connector = FleetDataConnector()
        processor = FleetDataProcessor(connector)
        viz_engine = FleetVisualizationEngine(processor)
        insights_engine = FleetInsightsEngine(processor)
        report_generator = FleetReportGenerator(processor, viz_engine, insights_engine)
        
        _copilot_components = {
            'connector': connector,
            'processor': processor,
            'viz_engine': viz_engine,
            'insights_engine': insights_engine,
            'report_generator': report_generator
        }
        
        logger.info("✓ Componentes do copiloto inicializados")
    
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
        
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter performance de veículos
        vehicle_perf = processor.get_vehicle_performance(enterprise_id, days)
        
        # Converter para lista de dicionários
        vehicles_list = []
        if not vehicle_perf.empty:
            for _, row in vehicle_perf.iterrows():
                vehicles_list.append({
                    'vehiclePlate': row['vehicle_plate'],
                    'totalChecks': int(row['total_checks']),
                    'complianceRate': round(row['compliance_rate'], 1),
                    'avgTemperature': round(row['avg_temperature'], 1) if row['avg_temperature'] else None,
                    'avgHumidity': round(row['avg_humidity'], 1) if row['avg_humidity'] else None,
                    'totalDistance': round(row['total_distance'], 1) if row['total_distance'] else None,
                    'lastActivity': row['last_activity'].isoformat() if row['last_activity'] else None
                })
        
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
        
        components = get_copilot_components()
        processor = components['processor']
        
        # Obter performance de motoristas
        driver_perf = processor.get_driver_performance(enterprise_id, days)
        
        # Converter para lista
        drivers_list = []
        if not driver_perf.empty:
            for _, row in driver_perf.iterrows():
                drivers_list.append({
                    'driverName': row['driver_name'],
                    'totalChecks': int(row['total_checks']),
                    'complianceRate': round(row['compliance_rate'], 1),
                    'vehiclesOperated': int(row['vehicles_operated']),
                    'lastActivity': row['last_activity'].isoformat() if row['last_activity'] else None
                })
        
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
        days = int(request.args.get('days', 30))
        priority = request.args.get('priority', 'all')  # all, high, medium, low
        
        components = get_copilot_components()
        insights_engine = components['insights_engine']
        
        # Gerar análise completa
        analysis = insights_engine.generate_comprehensive_analysis(enterprise_id, days)
        
        # Coletar todos os insights
        all_insights = []
        for category in ['summary', 'vehicle_insights', 'driver_insights', 'maintenance_insights', 'safety_insights']:
            if category in analysis and 'insights' in analysis[category]:
                for insight in analysis[category]['insights']:
                    insight['category'] = category
                    all_insights.append(insight)
        
        # Filtrar por prioridade se especificado
        if priority != 'all':
            all_insights = [i for i in all_insights if i['priority'] == priority]
        
        # Ordenar por prioridade (high, medium, low)
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        all_insights.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return jsonify({
            'success': True,
            'data': {
                'insights': all_insights,
                'alerts': analysis.get('alerts', []),
                'recommendations': analysis.get('recommendations', []),
                'summary': analysis.get('summary', {}),
                'totalInsights': len(all_insights),
                'highPriorityCount': len([i for i in all_insights if i['priority'] == 'high']),
                'mediumPriorityCount': len([i for i in all_insights if i['priority'] == 'medium']),
                'lowPriorityCount': len([i for i in all_insights if i['priority'] == 'low'])
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
        
        components = get_copilot_components()
        processor = components['processor']
        insights_engine = components['insights_engine']
        
        # Obter dados para contexto
        summary = processor.get_checklist_summary(enterprise_id, days)
        analysis = insights_engine.generate_comprehensive_analysis(enterprise_id, days)
        
        # Processar pergunta
        response = process_natural_language_question(question, summary, analysis)
        
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
        
        components = get_copilot_components()
        viz_engine = components['viz_engine']
        
        # Gerar dashboard HTML
        dashboard_file = viz_engine.create_interactive_dashboard(enterprise_id, days)
        
        # Ler conteúdo do arquivo
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Adicionar meta tags para mobile
        mobile_meta = '''
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <style>
            body { margin: 0; padding: 10px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
            .plotly-graph-div { width: 100% !important; height: auto !important; }
        </style>
        '''
        
        # Inserir meta tags no head
        html_content = html_content.replace('<head>', f'<head>{mobile_meta}')
        
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"Erro em dashboard_page: {e}")
        return f"<html><body><h1>Erro ao carregar dashboard</h1><p>{str(e)}</p></body></html>", 500

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def process_natural_language_question(question: str, summary: dict, analysis: dict) -> str:
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
               f"Cada veículo realizou em média {summary['total'] / summary['vehicles']:.1f} verificações " \
               f"no período analisado."
    
    # Perguntas sobre motoristas
    elif any(word in question_lower for word in ['motoristas', 'drivers', 'condutores']):
        return f"Há {summary['drivers']} motoristas ativos na frota. " \
               f"Cada motorista realizou em média {summary['total'] / summary['drivers']:.1f} verificações."
    
    # Perguntas sobre problemas/alertas
    elif any(word in question_lower for word in ['problemas', 'alertas', 'issues', 'falhas']):
        alerts_count = len(analysis.get('alerts', []))
        return f"Foram identificados {alerts_count} alertas ativos que requerem atenção. " \
               f"Há {summary['non_compliant']} não conformidades registradas no período."
    
    # Perguntas sobre insights
    elif any(word in question_lower for word in ['insights', 'recomendações', 'sugestões']):
        recommendations_count = len(analysis.get('recommendations', []))
        return f"O sistema gerou {recommendations_count} recomendações estratégicas para otimizar " \
               f"a operação da frota baseadas na análise dos dados."
    
    # Resposta genérica
    else:
        return f"Com base na análise dos últimos {summary['period_days']} dias: " \
               f"A frota tem {summary['vehicles']} veículos, {summary['drivers']} motoristas, " \
               f"realizou {summary['total']} verificações com {summary['compliance_rate']}% de conformidade."

