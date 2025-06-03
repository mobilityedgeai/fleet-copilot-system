"""
Dynamic BI Routes - Rotas para múltiplas collections
Fleet Copilot Enhanced API
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint para rotas dinâmicas
dynamic_bi_bp = Blueprint('dynamic_bi', __name__)

# Configuração da API Firebase
FIREBASE_API_URL = os.getenv('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')

class DynamicBIProcessor:
    """Processador dinâmico para múltiplas collections"""
    
    def __init__(self):
        self.firebase_url = FIREBASE_API_URL
        
    def fetch_collection_data(self, collection_name: str, enterprise_id: str = None, days: int = 30):
        """Busca dados de qualquer collection"""
        try:
            url = f"{self.firebase_url}/{collection_name}"
            params = {}
            
            if enterprise_id:
                params['enterpriseId'] = enterprise_id
            if days:
                params['days'] = days
                
            logger.info(f"🔗 Buscando dados de {collection_name}: {url}")
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Recebidos {len(data)} registros de /{collection_name}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro ao buscar {collection_name}: {e}")
            raise Exception(f"Erro na API externa: {str(e)}")
    
    def process_checklist_data(self, data, enterprise_id: str, days: int):
        """Processa dados de checklist"""
        if not data:
            return self._empty_checklist_response(enterprise_id, days)
            
        df = pd.DataFrame(data)
        
        # Filtrar por enterprise_id se especificado
        if enterprise_id and 'enterpriseId' in df.columns:
            df = df[df['enterpriseId'] == enterprise_id]
        
        # Filtrar por período
        if 'timestamp' in df.columns:
            cutoff_date = datetime.now() - timedelta(days=days)
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df[df['timestamp'] >= cutoff_date]
        
        total = len(df)
        
        # Calcular conformidade
        if 'noCompliant' in df.columns:
            non_compliant = len(df[df['noCompliant'] == True])
            compliant = total - non_compliant
        else:
            compliant = total
            non_compliant = 0
        
        compliance_rate = (compliant / total * 100) if total > 0 else 0
        
        # Contar veículos e motoristas únicos
        vehicles = df['vehiclePlate'].nunique() if 'vehiclePlate' in df.columns else 0
        drivers = df['driverName'].nunique() if 'driverName' in df.columns else 0
        
        return {
            "total": total,
            "compliant": compliant,
            "non_compliant": non_compliant,
            "compliance_rate": round(compliance_rate, 2),
            "vehicles": vehicles,
            "drivers": drivers,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": data[:50]  # Primeiros 50 registros para tabela
        }
    
    def process_trips_data(self, data, enterprise_id: str, days: int):
        """Processa dados de viagens"""
        if not data:
            return self._empty_trips_response(enterprise_id, days)
            
        df = pd.DataFrame(data)
        
        # Filtrar por enterprise_id se especificado
        if enterprise_id and 'enterpriseId' in df.columns:
            df = df[df['enterpriseId'] == enterprise_id]
        
        total_trips = len(df)
        total_distance = df['distance'].sum() if 'distance' in df.columns else 0
        total_time = df['duration'].sum() if 'duration' in df.columns else 0
        avg_speed = (total_distance / total_time) if total_time > 0 else 0
        
        drivers = df['driverName'].nunique() if 'driverName' in df.columns else 0
        vehicles = df['vehiclePlate'].nunique() if 'vehiclePlate' in df.columns else 0
        
        return {
            "total_trips": total_trips,
            "total_distance": round(total_distance, 2),
            "total_time": round(total_time, 2),
            "avg_speed": round(avg_speed, 2),
            "drivers": drivers,
            "vehicles": vehicles,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": data[:50]
        }
    
    def process_alerts_data(self, data, enterprise_id: str, days: int):
        """Processa dados de alertas"""
        if not data:
            return self._empty_alerts_response(enterprise_id, days)
            
        df = pd.DataFrame(data)
        
        # Filtrar por enterprise_id se especificado
        if enterprise_id and 'enterpriseId' in df.columns:
            df = df[df['enterpriseId'] == enterprise_id]
        
        total_alerts = len(df)
        active_alerts = len(df[df['status'] == 'Ativo']) if 'status' in df.columns else 0
        critical_alerts = len(df[df['priority'] == 'Alta']) if 'priority' in df.columns else 0
        resolved_alerts = len(df[df['status'] == 'Resolvido']) if 'status' in df.columns else 0
        
        resolution_rate = (resolved_alerts / total_alerts * 100) if total_alerts > 0 else 0
        avg_resolution_time = 24  # Placeholder
        
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts,
            "resolved_alerts": resolved_alerts,
            "resolution_rate": round(resolution_rate, 2),
            "avg_resolution_time": avg_resolution_time,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": data[:50]
        }
    
    def process_maintenance_data(self, data, enterprise_id: str, days: int):
        """Processa dados de manutenção"""
        if not data:
            return self._empty_maintenance_response(enterprise_id, days)
            
        df = pd.DataFrame(data)
        
        # Filtrar por enterprise_id se especificado
        if enterprise_id and 'enterpriseId' in df.columns:
            df = df[df['enterpriseId'] == enterprise_id]
        
        total_services = len(df)
        total_cost = df['cost'].sum() if 'cost' in df.columns else 0
        pending_services = len(df[df['status'] == 'Pendente']) if 'status' in df.columns else 0
        avg_service_time = df['duration'].mean() if 'duration' in df.columns else 0
        
        vehicles = df['vehiclePlate'].nunique() if 'vehiclePlate' in df.columns else 0
        
        return {
            "total_services": total_services,
            "total_cost": round(total_cost, 2),
            "pending_services": pending_services,
            "avg_service_time": round(avg_service_time, 2),
            "vehicles": vehicles,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": data[:50]
        }
    
    def _empty_checklist_response(self, enterprise_id: str, days: int):
        """Resposta vazia para checklist"""
        return {
            "total": 0,
            "compliant": 0,
            "non_compliant": 0,
            "compliance_rate": 0,
            "vehicles": 0,
            "drivers": 0,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": []
        }
    
    def _empty_trips_response(self, enterprise_id: str, days: int):
        """Resposta vazia para viagens"""
        return {
            "total_trips": 0,
            "total_distance": 0,
            "total_time": 0,
            "avg_speed": 0,
            "drivers": 0,
            "vehicles": 0,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": []
        }
    
    def _empty_alerts_response(self, enterprise_id: str, days: int):
        """Resposta vazia para alertas"""
        return {
            "total_alerts": 0,
            "active_alerts": 0,
            "critical_alerts": 0,
            "resolved_alerts": 0,
            "resolution_rate": 0,
            "avg_resolution_time": 0,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": []
        }
    
    def _empty_maintenance_response(self, enterprise_id: str, days: int):
        """Resposta vazia para manutenção"""
        return {
            "total_services": 0,
            "total_cost": 0,
            "pending_services": 0,
            "avg_service_time": 0,
            "vehicles": 0,
            "period_days": days,
            "enterprise_id": enterprise_id,
            "raw_data": []
        }

# Instância do processador
processor = DynamicBIProcessor()

@dynamic_bi_bp.route('/collections', methods=['GET'])
@cross_origin()
def get_collections():
    """Lista collections disponíveis"""
    try:
        collections = {
            "checklist": {
                "name": "Checklist de Veículos",
                "description": "Inspeções e verificações de conformidade",
                "icon": "fas fa-clipboard-check",
                "color": "#1abc9c",
                "available": True
            },
            "trips": {
                "name": "Viagens",
                "description": "Histórico de viagens e rotas",
                "icon": "fas fa-route",
                "color": "#3498db",
                "available": True
            },
            "alerts": {
                "name": "Alertas",
                "description": "Alertas e notificações do sistema",
                "icon": "fas fa-exclamation-triangle",
                "color": "#e74c3c",
                "available": True
            },
            "maintenance": {
                "name": "Manutenção",
                "description": "Serviços e manutenção de veículos",
                "icon": "fas fa-tools",
                "color": "#f39c12",
                "available": True
            }
        }
        
        return jsonify({
            'success': True,
            'data': collections
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar collections: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@dynamic_bi_bp.route('/checklist', methods=['GET'])
@cross_origin()
def get_checklist_data():
    """Dados de checklist"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        # Buscar dados reais da API
        raw_data = processor.fetch_collection_data('checklist', enterprise_id, days)
        
        # Processar dados
        processed_data = processor.process_checklist_data(raw_data, enterprise_id, days)
        
        return jsonify({
            'success': True,
            'data': processed_data
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados de checklist: {e}")
        return jsonify({
            'success': False,
            'message': str(e),
            'data': processor._empty_checklist_response(
                request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7'),
                int(request.args.get('days', 30))
            )
        }), 200  # Retorna 200 com dados vazios em caso de erro

@dynamic_bi_bp.route('/trips', methods=['GET'])
@cross_origin()
def get_trips_data():
    """Dados de viagens"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        # Buscar dados reais da API
        raw_data = processor.fetch_collection_data('trips', enterprise_id, days)
        
        # Processar dados
        processed_data = processor.process_trips_data(raw_data, enterprise_id, days)
        
        return jsonify({
            'success': True,
            'data': processed_data
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados de viagens: {e}")
        return jsonify({
            'success': False,
            'message': str(e),
            'data': processor._empty_trips_response(
                request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7'),
                int(request.args.get('days', 30))
            )
        }), 200

@dynamic_bi_bp.route('/alerts', methods=['GET'])
@cross_origin()
def get_alerts_data():
    """Dados de alertas"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        # Buscar dados reais da API
        raw_data = processor.fetch_collection_data('alerts', enterprise_id, days)
        
        # Processar dados
        processed_data = processor.process_alerts_data(raw_data, enterprise_id, days)
        
        return jsonify({
            'success': True,
            'data': processed_data
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados de alertas: {e}")
        return jsonify({
            'success': False,
            'message': str(e),
            'data': processor._empty_alerts_response(
                request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7'),
                int(request.args.get('days', 30))
            )
        }), 200

@dynamic_bi_bp.route('/maintenance', methods=['GET'])
@cross_origin()
def get_maintenance_data():
    """Dados de manutenção"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        # Buscar dados reais da API
        raw_data = processor.fetch_collection_data('maintenance', enterprise_id, days)
        
        # Processar dados
        processed_data = processor.process_maintenance_data(raw_data, enterprise_id, days)
        
        return jsonify({
            'success': True,
            'data': processed_data
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados de manutenção: {e}")
        return jsonify({
            'success': False,
            'message': str(e),
            'data': processor._empty_maintenance_response(
                request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7'),
                int(request.args.get('days', 30))
            )
        }), 200

# Endpoint genérico para qualquer collection
@dynamic_bi_bp.route('/<collection_name>', methods=['GET'])
@cross_origin()
def get_dynamic_collection_data(collection_name):
    """Endpoint genérico para qualquer collection"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        # Mapear collection para processador
        processors = {
            'checklist': processor.process_checklist_data,
            'trips': processor.process_trips_data,
            'alerts': processor.process_alerts_data,
            'maintenance': processor.process_maintenance_data
        }
        
        if collection_name not in processors:
            return jsonify({
                'success': False,
                'message': f'Collection {collection_name} não suportada'
            }), 404
        
        # Buscar dados reais da API
        raw_data = processor.fetch_collection_data(collection_name, enterprise_id, days)
        
        # Processar dados
        processed_data = processors[collection_name](raw_data, enterprise_id, days)
        
        return jsonify({
            'success': True,
            'data': processed_data
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar dados de {collection_name}: {e}")
        
        # Retornar dados vazios em caso de erro
        empty_responses = {
            'checklist': processor._empty_checklist_response,
            'trips': processor._empty_trips_response,
            'alerts': processor._empty_alerts_response,
            'maintenance': processor._empty_maintenance_response
        }
        
        empty_data = empty_responses.get(collection_name, processor._empty_checklist_response)(
            enterprise_id, days
        )
        
        return jsonify({
            'success': False,
            'message': str(e),
            'data': empty_data
        }), 200
