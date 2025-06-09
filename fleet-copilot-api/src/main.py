import os
import sys
import requests
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Configurar caminho para templates (um nível acima de src/)
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

# Criar app Flask com template_folder correto
app = Flask(__name__, template_folder=template_dir)

# Cache global para usuários (evita múltiplas consultas à API)
users_cache = {}
cache_timestamp = {}
CACHE_DURATION = 300  # 5 minutos

# Configurações da API
API_BASE_URL = "https://firebase-bi-api.onrender.com"

def get_users_mapping(enterprise_id):
    """
    Obter mapeamento de userID para nomes dos motoristas
    Implementa cache para otimizar performance
    """
    try:
        # Verificar se cache é válido
        cache_key = f"users_{enterprise_id}"
        now = datetime.now()
        
        if (cache_key in users_cache and 
            cache_key in cache_timestamp and 
            (now - cache_timestamp[cache_key]).seconds < CACHE_DURATION):
            print(f"[DE-PARA] Usando cache para {enterprise_id}")
            return users_cache[cache_key]
        
        # Buscar usuários da API
        print(f"[DE-PARA] Buscando usuários da API para {enterprise_id}")
        url = f"{API_BASE_URL}/users?enterpriseId={enterprise_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            users_data = data.get('data', [])
            
            # Criar mapeamento userID -> nome
            mapping = {}
            for user in users_data:
                user_id = user.get('uid') or user.get('id') or user.get('_doc_id')
                display_name = user.get('display_name', 'N/A')
                
                if user_id and display_name != 'N/A':
                    mapping[user_id] = display_name
                    print(f"[DE-PARA] Mapeado: {user_id[:10]}... -> {display_name}")
            
            # Atualizar cache
            users_cache[cache_key] = mapping
            cache_timestamp[cache_key] = now
            
            print(f"[DE-PARA] Cache atualizado: {len(mapping)} usuários")
            return mapping
            
        else:
            print(f"[DE-PARA] Erro na API users: {response.status_code}")
            return {}
            
    except Exception as e:
        print(f"[DE-PARA] Erro ao buscar usuários: {e}")
        return {}

def enrich_data_with_names(data, enterprise_id, user_fields=['UserString', 'userId', 'driverId', 'motorista']):
    """
    Enriquecer dados com nomes reais dos motoristas
    
    Args:
        data: Lista de registros ou registro único
        enterprise_id: ID da empresa
        user_fields: Lista de campos que podem conter userID
    
    Returns:
        Dados enriquecidos com nomes dos motoristas
    """
    try:
        # Obter mapeamento de usuários
        users_mapping = get_users_mapping(enterprise_id)
        
        if not users_mapping:
            print("[DE-PARA] Nenhum mapeamento disponível")
            return data
        
        def enrich_record(record):
            """Enriquecer um registro individual"""
            if not isinstance(record, dict):
                return record
            
            enriched = record.copy()
            
            # Procurar campos de usuário e adicionar nomes
            for field in user_fields:
                if field in record:
                    user_id = record[field]
                    if user_id in users_mapping:
                        # Adicionar campo com nome do motorista
                        name_field = f"{field}_name"
                        enriched[name_field] = users_mapping[user_id]
                        print(f"[DE-PARA] {field}: {user_id[:10]}... -> {users_mapping[user_id]}")
                    else:
                        # Adicionar campo indicando que não foi encontrado
                        name_field = f"{field}_name"
                        enriched[name_field] = f"Motorista {user_id[:8]}..." if user_id else "N/A"
            
            return enriched
        
        # Processar dados
        if isinstance(data, list):
            return [enrich_record(record) for record in data]
        else:
            return enrich_record(data)
            
    except Exception as e:
        print(f"[DE-PARA] Erro ao enriquecer dados: {e}")
        return data

# Configurações para CORS (necessário para scorecard preditivo)
@app.after_request
def after_request(response):
    """Adicionar headers CORS para compatibilidade com scorecard preditivo"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# NOVO ENDPOINT: Mapeamento de usuários
@app.route('/api/users-mapping')
def users_mapping_endpoint():
    """
    Endpoint para obter mapeamento de userID para nomes
    Usado pelos BIs para fazer DE-PARA no frontend
    """
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    
    try:
        mapping = get_users_mapping(enterprise_id)
        
        return jsonify({
            'status': 'success',
            'enterprise_id': enterprise_id,
            'mapping': mapping,
            'count': len(mapping),
            'cache_info': {
                'cached': f"users_{enterprise_id}" in users_cache,
                'timestamp': cache_timestamp.get(f"users_{enterprise_id}", {}).isoformat() if f"users_{enterprise_id}" in cache_timestamp else None
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'enterprise_id': enterprise_id,
            'timestamp': datetime.now().isoformat()
        }), 500

# NOVO ENDPOINT: Dados enriquecidos de trips
@app.route('/api/trips-enriched')
def trips_enriched():
    """
    Endpoint para obter dados de trips já enriquecidos com nomes dos motoristas
    """
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    
    try:
        # Buscar dados de trips da API original
        url = f"{API_BASE_URL}/trips?enterpriseId={enterprise_id}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            trips_data = response.json()
            original_data = trips_data.get('data', [])
            
            # Enriquecer dados com nomes
            enriched_data = enrich_data_with_names(original_data, enterprise_id)
            
            # Retornar dados enriquecidos
            result = trips_data.copy()
            result['data'] = enriched_data
            result['enriched'] = True
            result['enrichment_timestamp'] = datetime.now().isoformat()
            
            return jsonify(result)
            
        else:
            return jsonify({
                'status': 'error',
                'message': f'Erro na API trips: {response.status_code}',
                'enterprise_id': enterprise_id
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'enterprise_id': enterprise_id
        }), 500

# NOVO ENDPOINT: Limpar cache de usuários
@app.route('/api/clear-users-cache')
def clear_users_cache():
    """Limpar cache de usuários (útil para desenvolvimento)"""
    enterprise_id = request.args.get('enterpriseId')
    
    if enterprise_id:
        cache_key = f"users_{enterprise_id}"
        if cache_key in users_cache:
            del users_cache[cache_key]
        if cache_key in cache_timestamp:
            del cache_timestamp[cache_key]
        message = f"Cache limpo para {enterprise_id}"
    else:
        users_cache.clear()
        cache_timestamp.clear()
        message = "Cache global limpo"
    
    return jsonify({
        'status': 'success',
        'message': message,
        'timestamp': datetime.now().isoformat()
    })

# Rota principal - redireciona para o menu dos BIs
@app.route('/')
def index():
    """Página inicial - redireciona para menu dos BIs"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return redirect(url_for('dashboard_menu', enterpriseId=enterprise_id))

# Health check
@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'ok', 
        'message': 'Fleet Copilot BI Server is running',
        'features': {
            'users_mapping': True,
            'data_enrichment': True,
            'cache_system': True
        },
        'cache_stats': {
            'cached_enterprises': len(users_cache),
            'cache_keys': list(users_cache.keys())
        }
    }

# Menu principal dos BIs
@app.route('/api/copilot/dashboard')
def dashboard_menu():
    """Menu principal dos BIs"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('dashboard_menu.html', enterprise_id=enterprise_id)

# Compatibilidade com URL antiga
@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """Redireciona URL antiga para novo menu"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return redirect(url_for('dashboard_menu', enterpriseId=enterprise_id))

# BI Combustível
@app.route('/api/copilot/bi-combustivel')
def bi_combustivel():
    """BI de Combustível"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_combustivel.html', enterprise_id=enterprise_id)

# BI Checklist
@app.route('/api/copilot/bi-checklist')
def bi_checklist():
    """BI de Checklist"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_checklist.html', enterprise_id=enterprise_id)

# BI Frotas Agregadas/Spot
@app.route('/api/copilot/bi-frotas')
def bi_frotas():
    """BI de Frotas Agregadas/Spot"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_frotas.html', enterprise_id=enterprise_id)

# BI Viagens
@app.route('/api/copilot/bi-viagens')
def bi_viagens():
    """BI de Viagens"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_viagens.html', enterprise_id=enterprise_id)

# BI Trips - Análise de Viagens (Sentinel Insights)
@app.route('/api/copilot/bi-trips')
def bi_trips():
    """BI de Trips - Análise de Viagens com dados do Sentinel Insights"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_trips.html', enterprise_id=enterprise_id)

# BI Scorecard Preditivo de Risco
@app.route('/api/copilot/scorecard-preditivo')
def scorecard_preditivo():
    """Scorecard Preditivo de Risco - Análise Avançada de Segurança e Prevenção de Acidentes"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    
    # Log para debug do scorecard preditivo
    print(f"[SCORECARD] Acessando scorecard preditivo com enterpriseId: {enterprise_id}")
    
    return render_template('scorecard_preditivo.html', enterprise_id=enterprise_id)

# Endpoint específico para dados do scorecard preditivo (se necessário)
@app.route('/api/copilot/scorecard-preditivo/data')
def scorecard_preditivo_data():
    """Endpoint para dados específicos do scorecard preditivo (se necessário)"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    
    # Este endpoint pode ser usado para fornecer dados específicos do scorecard
    # se necessário no futuro, mas atualmente o scorecard busca dados diretamente
    # da API Firebase BI
    
    return jsonify({
        'status': 'success',
        'message': 'Scorecard preditivo configurado para buscar dados da API Firebase BI',
        'api_endpoints': {
            'trips': 'https://firebase-bi-api.onrender.com/trips',
            'users': 'https://firebase-bi-api.onrender.com/users',
            'trips_enriched': '/api/trips-enriched',
            'users_mapping': '/api/users-mapping'
        },
        'enterprise_id': enterprise_id
    })

# BI Manutenção
@app.route('/api/copilot/bi-manutencao')
def bi_manutencao():
    """BI de Manutenção (Preventiva e Corretiva)"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_manutencao.html', enterprise_id=enterprise_id)

# BI Gestão de Veículos
@app.route('/api/copilot/bi-gestao-veiculos')
def bi_gestao_veiculos():
    """BI de Gestão de Veículos da Frota"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_gestao_veiculos.html', enterprise_id=enterprise_id)

# BI Motoristas
@app.route('/api/copilot/bi-motoristas')
def bi_motoristas():
    """BI de Motoristas"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_motoristas.html', enterprise_id=enterprise_id)

# BI Financeiro
@app.route('/api/copilot/bi-financeiro')
def bi_financeiro():
    """BI Financeiro"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_financeiro.html', enterprise_id=enterprise_id)

# API para listar BIs disponíveis
@app.route('/api/copilot/bis')
def list_bis():
    """Lista todos os BIs disponíveis"""
    bis = [
        {
            'id': 'combustivel',
            'name': 'Combustível',
            'description': 'Gestão e análise de abastecimento',
            'status': 'available',
            'url': '/api/copilot/bi-combustivel'
        },
        {
            'id': 'checklist',
            'name': 'Checklist',
            'description': 'Inspeções e verificações de conformidade',
            'status': 'available',
            'url': '/api/copilot/bi-checklist'
        },
        {
            'id': 'frotas',
            'name': 'Frotas Agregadas/Spot',
            'description': 'Gestão de frotas terceirizadas e spot',
            'status': 'available',
            'url': '/api/copilot/bi-frotas'
        },
        {
            'id': 'viagens',
            'name': 'Viagens',
            'description': 'Rotas e deslocamentos da frota',
            'status': 'coming_soon',
            'url': '/api/copilot/bi-viagens'
        },
        {
            'id': 'trips',
            'name': 'Trips - Análise de Viagens',
            'description': 'Performance, custos, segurança e emissões das viagens (Sentinel Insights)',
            'status': 'available',
            'url': '/api/copilot/bi-trips'
        },
        {
            'id': 'scorecard-preditivo',
            'name': 'Scorecard Preditivo de Risco',
            'description': 'Análise avançada de segurança e prevenção de acidentes com algoritmo preditivo',
            'status': 'available',
            'url': '/api/copilot/scorecard-preditivo',
            'features': [
                'Algoritmo preditivo de risco',
                'Análise de comportamento de motoristas',
                'Scores baseados em dados reais',
                'Gráficos informativos e insights',
                'Visual enterprise profissional',
                'DE-PARA automático de nomes'
            ]
        },
        {
            'id': 'manutencao',
            'name': 'Manutenção',
            'description': 'Gestão de manutenção preventiva e corretiva',
            'status': 'available',
            'url': '/api/copilot/bi-manutencao'
        },
        {
            'id': 'gestao-veiculos',
            'name': 'Gestão de Veículos',
            'description': 'Composição, valor, utilização, manutenção e conformidade da frota',
            'status': 'available',
            'url': '/api/copilot/bi-gestao-veiculos'
        },
        {
            'id': 'motoristas',
            'name': 'Motoristas',
            'description': 'Performance e comportamento dos condutores',
            'status': 'coming_soon',
            'url': '/api/copilot/bi-motoristas'
        },
        {
            'id': 'financeiro',
            'name': 'Financeiro',
            'description': 'Análise financeira completa',
            'status': 'coming_soon',
            'url': '/api/copilot/bi-financeiro'
        }
    ]
    return jsonify(bis)

# Endpoint para configurações do scorecard preditivo
@app.route('/api/copilot/scorecard-preditivo/config')
def scorecard_config():
    """Configurações específicas do scorecard preditivo"""
    return jsonify({
        'scorecard_version': '2.1',
        'algorithm_version': 'v1.3',
        'data_sources': {
            'trips_api': 'https://firebase-bi-api.onrender.com/trips',
            'users_api': 'https://firebase-bi-api.onrender.com/users',
            'trips_enriched': '/api/trips-enriched',
            'users_mapping': '/api/users-mapping'
        },
        'features': {
            'real_data_processing': True,
            'predictive_scoring': True,
            'enterprise_visual': True,
            'advanced_charts': True,
            'fallback_system': True,
            'automatic_name_mapping': True,
            'data_enrichment': True
        },
        'risk_calculation': {
            'behavior_score_weight': 0.4,
            'events_per_trip_weight': 0.3,
            'speed_events_weight': 0.2,
            'trip_frequency_weight': 0.1
        },
        'thresholds': {
            'low_risk': 40,
            'medium_risk': 70,
            'high_risk': 100
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"[FLEET COPILOT] Iniciando servidor na porta {port}")
    print(f"[FLEET COPILOT] Modo debug: {debug}")
    print(f"[FLEET COPILOT] Template directory: {template_dir}")
    print(f"[SCORECARD] Scorecard Preditivo disponível em: /api/copilot/scorecard-preditivo")
    print(f"[DE-PARA] Sistema de mapeamento de usuários ativo")
    print(f"[DE-PARA] Endpoints disponíveis:")
    print(f"[DE-PARA]   - /api/users-mapping")
    print(f"[DE-PARA]   - /api/trips-enriched")
    print(f"[DE-PARA]   - /api/clear-users-cache")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
