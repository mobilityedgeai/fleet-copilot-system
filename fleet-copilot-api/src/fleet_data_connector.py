"""
Copiloto Inteligente de Gestão de Frotas
Módulo de Conexão e Processamento de Dados - Versão Corrigida
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import logging
from dataclasses import dataclass
from urllib.parse import urljoin
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FleetAPIConfig:
    """Configuração da API de gestão de frotas"""
    base_url: str = None
    timeout: int = 30
    max_retries: int = 3
    
    def __post_init__(self):
        if self.base_url is None:
            self.base_url = os.getenv('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')

class FleetDataConnector:
    """Conector para APIs de gestão de frotas"""
    
    def __init__(self, config: FleetAPIConfig = None):
        self.config = config or FleetAPIConfig()
        self.session = requests.Session()
        self.session.timeout = self.config.timeout
        
    def _make_request(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Faz requisição para a API com retry automático"""
        url = urljoin(self.config.base_url, endpoint)
        
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"Fazendo requisição para {url} (tentativa {attempt + 1})")
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"Recebidos {len(data)} registros de {endpoint}")
                return data
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Erro na tentativa {attempt + 1}: {e}")
                if attempt == self.config.max_retries - 1:
                    logger.error(f"Falha após {self.config.max_retries} tentativas: {e}")
                    return []
                    
        return []
    
    def get_checklist_data(self, enterprise_id: str = None, 
                          start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Obtém dados de checklist"""
        params = {}
        if enterprise_id:
            params['enterpriseId'] = enterprise_id
            
        data = self._make_request('/checklist', params)
        
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        
        if not df.empty:
            # Conversão de tipos com tratamento de erro
            try:
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                if 'issueOpenDate' in df.columns:
                    df['issueOpenDate'] = pd.to_datetime(df['issueOpenDate'], errors='coerce')
                
                # Filtros de data
                if start_date and 'timestamp' in df.columns:
                    start_dt = pd.to_datetime(start_date)
                    df = df[df['timestamp'] >= start_dt]
                if end_date and 'timestamp' in df.columns:
                    end_dt = pd.to_datetime(end_date)
                    df = df[df['timestamp'] <= end_dt]
                    
            except Exception as e:
                logger.warning(f"Erro na conversão de datas: {e}")
                
        return df
    
    def get_alerts_checkin_data(self, enterprise_id: str = None,
                               start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Obtém dados de alertas de check-in (telemática)"""
        params = {}
        if enterprise_id:
            params['enterpriseId'] = enterprise_id
            
        data = self._make_request('/alerts-checkin', params)
        
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        
        if not df.empty:
            try:
                # Conversão de tipos
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                
                # Extração de coordenadas se existir
                if 'location' in df.columns:
                    df['latitude'] = df['location'].apply(lambda x: x.get('latitude') if isinstance(x, dict) else None)
                    df['longitude'] = df['location'].apply(lambda x: x.get('longitude') if isinstance(x, dict) else None)
                
                # Filtros de data
                if start_date and 'timestamp' in df.columns:
                    start_dt = pd.to_datetime(start_date)
                    df = df[df['timestamp'] >= start_dt]
                if end_date and 'timestamp' in df.columns:
                    end_dt = pd.to_datetime(end_date)
                    df = df[df['timestamp'] <= end_dt]
                    
            except Exception as e:
                logger.warning(f"Erro no processamento de alertas: {e}")
                
        return df
    
    def get_driver_trips_data(self, enterprise_id: str = None,
                             start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Obtém dados de viagens de motoristas"""
        params = {}
        if enterprise_id:
            params['enterpriseId'] = enterprise_id
            
        data = self._make_request('/driver-trips', params)
        
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        
        if not df.empty:
            try:
                # Assumindo que existe campo de timestamp
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                        df = df[df['timestamp'] >= start_dt]
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                        df = df[df['timestamp'] <= end_dt]
                        
            except Exception as e:
                logger.warning(f"Erro no processamento de viagens: {e}")
                    
        return df

class FleetDataProcessor:
    """Processador de dados de frota para análises"""
    
    def __init__(self, connector: FleetDataConnector):
        self.connector = connector
        
    def get_checklist_summary(self, enterprise_id: str = None, days: int = 7) -> Dict[str, Any]:
        """Gera resumo de checklists"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            df = self.connector.get_checklist_data(
                enterprise_id=enterprise_id,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            
            if df.empty:
                return {
                    "total": 0, 
                    "compliant": 0, 
                    "non_compliant": 0, 
                    "compliance_rate": 0,
                    "period_days": days,
                    "vehicles": 0,
                    "drivers": 0
                }
            
            # Calcular métricas de conformidade baseado na estrutura real
            total = len(df)
            
            # Verificar diferentes campos de conformidade
            if 'noCompliant' in df.columns:
                # noCompliant: True = não conforme, False = conforme
                non_compliant = len(df[df['noCompliant'] == True])
                compliant = total - non_compliant
            elif 'compliant' in df.columns:
                # compliant: True = conforme, False = não conforme
                compliant = len(df[df['compliant'] == True])
                non_compliant = total - compliant
            else:
                # Se não há campo de conformidade, assumir todos conformes
                compliant = total
                non_compliant = 0
            
            compliance_rate = (compliant / total * 100) if total > 0 else 0
            
            # Contar veículos e motoristas únicos
            vehicles = df['vehiclePlate'].nunique() if 'vehiclePlate' in df.columns else 0
            drivers = df['driverName'].nunique() if 'driverName' in df.columns and df['driverName'].notna().any() else 0
            
            return {
                "total": total,
                "compliant": compliant,
                "non_compliant": non_compliant,
                "compliance_rate": round(compliance_rate, 2),
                "period_days": days,
                "vehicles": vehicles,
                "drivers": drivers
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo de checklist: {e}")
            return {
                "total": 0, 
                "compliant": 0, 
                "non_compliant": 0, 
                "compliance_rate": 0,
                "period_days": days,
                "vehicles": 0,
                "drivers": 0,
                "error": str(e)
            }
    
    def get_vehicle_performance(self, enterprise_id: str = None, days: int = 30) -> List[Dict[str, Any]]:
        """Análise de performance por veículo"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Dados de checklist
            checklist_df = self.connector.get_checklist_data(
                enterprise_id=enterprise_id,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            
            if checklist_df.empty:
                return []
            
            performance_data = []
            
            # Análise por veículo
            for vehicle in checklist_df['vehiclePlate'].unique():
                if pd.isna(vehicle):
                    continue
                    
                vehicle_data = checklist_df[checklist_df['vehiclePlate'] == vehicle]
                
                # Métricas de checklist
                total_checks = len(vehicle_data)
                
                # Calcular conformidade
                if 'noCompliant' in vehicle_data.columns:
                    compliant_checks = len(vehicle_data[vehicle_data['noCompliant'] == False])
                elif 'compliant' in vehicle_data.columns:
                    compliant_checks = len(vehicle_data[vehicle_data['compliant'] == True])
                else:
                    compliant_checks = total_checks
                
                compliance_rate = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
                
                # Última atividade
                last_check = vehicle_data['timestamp'].max() if 'timestamp' in vehicle_data.columns else None
                
                # Itens mais verificados
                top_items = []
                if 'itemName' in vehicle_data.columns:
                    item_counts = vehicle_data['itemName'].value_counts().head(3)
                    top_items = [{"item": item, "count": count} for item, count in item_counts.items()]
                
                performance_data.append({
                    'vehicle_plate': vehicle,
                    'total_checks': total_checks,
                    'compliance_rate': round(compliance_rate, 2),
                    'last_check': last_check.isoformat() if last_check and pd.notna(last_check) else None,
                    'top_items': top_items,
                    'status': 'active' if total_checks > 0 else 'inactive'
                })
            
            # Ordenar por taxa de conformidade
            performance_data.sort(key=lambda x: x['compliance_rate'], reverse=True)
            return performance_data
            
        except Exception as e:
            logger.error(f"Erro ao analisar performance de veículos: {e}")
            return []
    
    def get_driver_performance(self, enterprise_id: str = None, days: int = 30) -> List[Dict[str, Any]]:
        """Análise de performance por motorista"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            checklist_df = self.connector.get_checklist_data(
                enterprise_id=enterprise_id,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            
            if checklist_df.empty or 'driverName' not in checklist_df.columns:
                return []
            
            driver_performance = []
            
            for driver in checklist_df['driverName'].unique():
                if pd.isna(driver) or driver == "":
                    continue
                    
                driver_data = checklist_df[checklist_df['driverName'] == driver]
                
                total_checks = len(driver_data)
                
                # Calcular conformidade
                if 'noCompliant' in driver_data.columns:
                    compliant_checks = len(driver_data[driver_data['noCompliant'] == False])
                elif 'compliant' in driver_data.columns:
                    compliant_checks = len(driver_data[driver_data['compliant'] == True])
                else:
                    compliant_checks = total_checks
                
                compliance_rate = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
                
                vehicles_operated = driver_data['vehiclePlate'].nunique() if 'vehiclePlate' in driver_data.columns else 0
                last_activity = driver_data['timestamp'].max() if 'timestamp' in driver_data.columns else None
                
                driver_performance.append({
                    'driver_name': driver,
                    'total_checks': total_checks,
                    'compliance_rate': round(compliance_rate, 2),
                    'vehicles_operated': vehicles_operated,
                    'last_activity': last_activity.isoformat() if last_activity and pd.notna(last_activity) else None
                })
            
            # Ordenar por taxa de conformidade
            driver_performance.sort(key=lambda x: x['compliance_rate'], reverse=True)
            return driver_performance
            
        except Exception as e:
            logger.error(f"Erro ao analisar performance de motoristas: {e}")
            return []
    
    def get_maintenance_alerts(self, enterprise_id: str = None) -> List[Dict[str, Any]]:
        """Identifica alertas de manutenção baseados nos dados"""
        try:
            checklist_df = self.connector.get_checklist_data(enterprise_id=enterprise_id)
            
            if checklist_df.empty:
                return []
            
            alerts = []
            
            # Veículos com muitas não conformidades
            if 'noCompliant' in checklist_df.columns:
                non_compliant = checklist_df[checklist_df['noCompliant'] == True]
            elif 'compliant' in checklist_df.columns:
                non_compliant = checklist_df[checklist_df['compliant'] == False]
            else:
                non_compliant = pd.DataFrame()
            
            if not non_compliant.empty and 'vehiclePlate' in non_compliant.columns:
                vehicle_issues = non_compliant.groupby('vehiclePlate').size().sort_values(ascending=False)
                
                for vehicle, count in vehicle_issues.head(5).items():
                    if count >= 2:  # Threshold reduzido para alerta
                        priority = 'high' if count >= 3 else 'medium'
                        alerts.append({
                            'type': 'maintenance_required',
                            'vehicle': vehicle,
                            'issue_count': int(count),
                            'priority': priority,
                            'message': f'Veículo {vehicle} tem {count} não conformidades recentes'
                        })
            
            # Alertas de itens específicos
            if 'itemName' in checklist_df.columns and 'noCompliant' in checklist_df.columns:
                critical_items = checklist_df[checklist_df['noCompliant'] == True]['itemName'].value_counts()
                
                for item, count in critical_items.head(3).items():
                    if count >= 2:
                        alerts.append({
                            'type': 'item_alert',
                            'item': item,
                            'issue_count': int(count),
                            'priority': 'medium',
                            'message': f'Item "{item}" apresenta {count} não conformidades'
                        })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Erro ao gerar alertas de manutenção: {e}")
            return []

if __name__ == "__main__":
    # Teste básico do módulo
    connector = FleetDataConnector()
    processor = FleetDataProcessor(connector)
    
    # Teste de conexão
    try:
        test_enterprise_id = "sA9EmrE3ymtnBqJKcYn7"
        
        summary = processor.get_checklist_summary(enterprise_id=test_enterprise_id, days=30)
        print("Resumo de Checklists (últimos 30 dias):")
        print(json.dumps(summary, indent=2, default=str))
        
        vehicle_perf = processor.get_vehicle_performance(enterprise_id=test_enterprise_id, days=30)
        if vehicle_perf:
            print(f"\nPerformance de Veículos ({len(vehicle_perf)} veículos):")
            for vehicle in vehicle_perf[:3]:  # Top 3
                print(f"- {vehicle['vehicle_plate']}: {vehicle['compliance_rate']}% conformidade")
        
        alerts = processor.get_maintenance_alerts(enterprise_id=test_enterprise_id)
        if alerts:
            print(f"\nAlertas de Manutenção ({len(alerts)} alertas):")
            for alert in alerts:
                print(f"- {alert['message']} (Prioridade: {alert['priority']})")
        else:
            print("\nNenhum alerta de manutenção encontrado.")
                
    except Exception as e:
        logger.error(f"Erro no teste: {e}")

