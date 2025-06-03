"""
Copiloto Inteligente de Gestão de Frotas
Módulo de Conexão e Processamento de Dados - Versão Corrigida (Sem undefined)
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import json
import logging
from dataclasses import dataclass
from urllib.parse import urljoin
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_get(data: Union[Dict, pd.Series], key: str, default: Any = 0) -> Any:
    """Obtém valor de forma segura, retornando default se None ou inválido"""
    if isinstance(data, dict):
        value = data.get(key, default)
    elif isinstance(data, pd.Series):
        value = getattr(data, key, default) if hasattr(data, key) else default
    else:
        return default
    
    # Verificar se é NaN ou None
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    
    return value

def safe_number(value: Any, default: Union[int, float] = 0) -> Union[int, float]:
    """Converte valor para número de forma segura"""
    try:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return default
        
        # Tentar converter para número
        if isinstance(value, (int, float)):
            return value if not pd.isna(value) else default
        
        # Tentar converter string para número
        if isinstance(value, str):
            value = value.strip()
            if value == '' or value.lower() in ['nan', 'null', 'none']:
                return default
            return float(value)
        
        return default
    except (ValueError, TypeError):
        return default

def safe_string(value: Any, default: str = "N/A") -> str:
    """Converte valor para string de forma segura"""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    
    if isinstance(value, str) and value.strip() == '':
        return default
    
    return str(value)

def safe_bool(value: Any, default: bool = False) -> bool:
    """Converte valor para boolean de forma segura"""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        return value.lower() in ['true', '1', 'yes', 'sim']
    
    if isinstance(value, (int, float)):
        return bool(value)
    
    return default

def safe_percentage(numerator: Any, denominator: Any, decimals: int = 2) -> float:
    """Calcula percentual de forma segura"""
    num = safe_number(numerator, 0)
    den = safe_number(denominator, 0)
    
    if den == 0:
        return 0.0
    
    result = (num / den) * 100
    return round(result, decimals)

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
        """Gera resumo de checklists com validação robusta"""
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
                    "compliance_rate": 0.0,
                    "period_days": days,
                    "vehicles": 0,
                    "drivers": 0
                }
            
            # Calcular métricas de conformidade baseado na estrutura real
            total = len(df)
            
            # Verificar diferentes campos de conformidade com validação
            compliant = 0
            non_compliant = 0
            
            if 'noCompliant' in df.columns:
                # noCompliant: True = não conforme, False = conforme
                non_compliant_mask = df['noCompliant'].apply(lambda x: safe_bool(x, False))
                non_compliant = int(non_compliant_mask.sum())
                compliant = total - non_compliant
            elif 'compliant' in df.columns:
                # compliant: True = conforme, False = não conforme
                compliant_mask = df['compliant'].apply(lambda x: safe_bool(x, True))
                compliant = int(compliant_mask.sum())
                non_compliant = total - compliant
            else:
                # Se não há campo de conformidade, assumir todos conformes
                compliant = total
                non_compliant = 0
            
            # Calcular taxa de conformidade de forma segura
            compliance_rate = safe_percentage(compliant, total)
            
            # Contar veículos e motoristas únicos com validação
            vehicles = 0
            drivers = 0
            
            if 'vehiclePlate' in df.columns:
                valid_plates = df['vehiclePlate'].apply(lambda x: safe_string(x, "")).str.strip()
                valid_plates = valid_plates[valid_plates != ""]
                vehicles = len(valid_plates.unique()) if not valid_plates.empty else 0
            
            if 'driverName' in df.columns:
                valid_drivers = df['driverName'].apply(lambda x: safe_string(x, "")).str.strip()
                valid_drivers = valid_drivers[valid_drivers != ""]
                drivers = len(valid_drivers.unique()) if not valid_drivers.empty else 0
            
            result = {
                "total": int(total),
                "compliant": int(compliant),
                "non_compliant": int(non_compliant),
                "compliance_rate": float(compliance_rate),
                "period_days": int(days),
                "vehicles": int(vehicles),
                "drivers": int(drivers)
            }
            
            logger.info(f"Resumo calculado: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo de checklist: {e}")
            return {
                "total": 0, 
                "compliant": 0, 
                "non_compliant": 0, 
                "compliance_rate": 0.0,
                "period_days": int(days),
                "vehicles": 0,
                "drivers": 0,
                "error": str(e)
            }
    
    def get_vehicle_performance(self, enterprise_id: str = None, days: int = 30) -> List[Dict[str, Any]]:
        """Análise de performance por veículo com validação robusta"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Dados de checklist
            checklist_df = self.connector.get_checklist_data(
                enterprise_id=enterprise_id,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            
            if checklist_df.empty or 'vehiclePlate' not in checklist_df.columns:
                return []
            
            performance_data = []
            
            # Análise por veículo
            for vehicle in checklist_df['vehiclePlate'].unique():
                vehicle_str = safe_string(vehicle, "")
                if vehicle_str == "" or vehicle_str == "N/A":
                    continue
                    
                vehicle_data = checklist_df[checklist_df['vehiclePlate'] == vehicle]
                
                # Métricas de checklist
                total_checks = len(vehicle_data)
                
                # Calcular conformidade com validação
                compliant_checks = 0
                if 'noCompliant' in vehicle_data.columns:
                    compliant_mask = vehicle_data['noCompliant'].apply(lambda x: not safe_bool(x, False))
                    compliant_checks = int(compliant_mask.sum())
                elif 'compliant' in vehicle_data.columns:
                    compliant_mask = vehicle_data['compliant'].apply(lambda x: safe_bool(x, True))
                    compliant_checks = int(compliant_mask.sum())
                else:
                    compliant_checks = total_checks
                
                compliance_rate = safe_percentage(compliant_checks, total_checks)
                
                # Última atividade com validação
                last_check = None
                if 'timestamp' in vehicle_data.columns:
                    valid_timestamps = vehicle_data['timestamp'].dropna()
                    if not valid_timestamps.empty:
                        last_check = valid_timestamps.max()
                
                # Itens mais verificados com validação
                top_items = []
                if 'itemName' in vehicle_data.columns:
                    valid_items = vehicle_data['itemName'].apply(lambda x: safe_string(x, "")).str.strip()
                    valid_items = valid_items[valid_items != ""]
                    if not valid_items.empty:
                        item_counts = valid_items.value_counts().head(3)
                        top_items = [{"item": item, "count": int(count)} for item, count in item_counts.items()]
                
                performance_data.append({
                    'vehicle_plate': vehicle_str,
                    'total_checks': int(total_checks),
                    'compliance_rate': float(compliance_rate),
                    'last_check': last_check.isoformat() if last_check and pd.notna(last_check) else None,
                    'top_items': top_items,
                    'status': 'active' if total_checks > 0 else 'inactive'
                })
            
            # Ordenar por taxa de conformidade
            performance_data.sort(key=lambda x: safe_number(x['compliance_rate'], 0), reverse=True)
            return performance_data
            
        except Exception as e:
            logger.error(f"Erro ao analisar performance de veículos: {e}")
            return []
    
    def get_driver_performance(self, enterprise_id: str = None, days: int = 30) -> List[Dict[str, Any]]:
        """Análise de performance por motorista com validação robusta"""
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
                driver_str = safe_string(driver, "")
                if driver_str == "" or driver_str == "N/A":
                    continue
                    
                driver_data = checklist_df[checklist_df['driverName'] == driver]
                
                total_checks = len(driver_data)
                
                # Calcular conformidade com validação
                compliant_checks = 0
                if 'noCompliant' in driver_data.columns:
                    compliant_mask = driver_data['noCompliant'].apply(lambda x: not safe_bool(x, False))
                    compliant_checks = int(compliant_mask.sum())
                elif 'compliant' in driver_data.columns:
                    compliant_mask = driver_data['compliant'].apply(lambda x: safe_bool(x, True))
                    compliant_checks = int(compliant_mask.sum())
                else:
                    compliant_checks = total_checks
                
                compliance_rate = safe_percentage(compliant_checks, total_checks)
                
                # Veículos operados com validação
                vehicles_operated = 0
                if 'vehiclePlate' in driver_data.columns:
                    valid_plates = driver_data['vehiclePlate'].apply(lambda x: safe_string(x, "")).str.strip()
                    valid_plates = valid_plates[valid_plates != ""]
                    vehicles_operated = len(valid_plates.unique()) if not valid_plates.empty else 0
                
                # Última atividade com validação
                last_activity = None
                if 'timestamp' in driver_data.columns:
                    valid_timestamps = driver_data['timestamp'].dropna()
                    if not valid_timestamps.empty:
                        last_activity = valid_timestamps.max()
                
                driver_performance.append({
                    'driver_name': driver_str,
                    'total_checks': int(total_checks),
                    'compliance_rate': float(compliance_rate),
                    'vehicles_operated': int(vehicles_operated),
                    'last_activity': last_activity.isoformat() if last_activity and pd.notna(last_activity) else None
                })
            
            # Ordenar por taxa de conformidade
            driver_performance.sort(key=lambda x: safe_number(x['compliance_rate'], 0), reverse=True)
            return driver_performance
            
        except Exception as e:
            logger.error(f"Erro ao analisar performance de motoristas: {e}")
            return []
    
    def get_maintenance_alerts(self, enterprise_id: str = None) -> List[Dict[str, Any]]:
        """Identifica alertas de manutenção baseados nos dados com validação robusta"""
        try:
            checklist_df = self.connector.get_checklist_data(enterprise_id=enterprise_id)
            
            if checklist_df.empty:
                return []
            
            alerts = []
            
            # Veículos com muitas não conformidades
            non_compliant = pd.DataFrame()
            
            if 'noCompliant' in checklist_df.columns:
                non_compliant_mask = checklist_df['noCompliant'].apply(lambda x: safe_bool(x, False))
                non_compliant = checklist_df[non_compliant_mask]
            elif 'compliant' in checklist_df.columns:
                non_compliant_mask = checklist_df['compliant'].apply(lambda x: not safe_bool(x, True))
                non_compliant = checklist_df[non_compliant_mask]
            
            if not non_compliant.empty and 'vehiclePlate' in non_compliant.columns:
                # Filtrar veículos válidos
                valid_vehicles = non_compliant['vehiclePlate'].apply(lambda x: safe_string(x, "")).str.strip()
                valid_vehicles = valid_vehicles[valid_vehicles != ""]
                
                if not valid_vehicles.empty:
                    vehicle_issues = valid_vehicles.value_counts().head(5)
                    
                    for vehicle, count in vehicle_issues.items():
                        if count >= 2:  # Threshold reduzido para alerta
                            priority = 'high' if count >= 3 else 'medium'
                            alerts.append({
                                'type': 'maintenance_required',
                                'vehicle': safe_string(vehicle),
                                'issue_count': int(count),
                                'priority': priority,
                                'message': f'Veículo {safe_string(vehicle)} tem {int(count)} não conformidades recentes'
                            })
            
            # Alertas de itens específicos
            if 'itemName' in checklist_df.columns and not non_compliant.empty:
                valid_items = non_compliant['itemName'].apply(lambda x: safe_string(x, "")).str.strip()
                valid_items = valid_items[valid_items != ""]
                
                if not valid_items.empty:
                    critical_items = valid_items.value_counts().head(3)
                    
                    for item, count in critical_items.items():
                        if count >= 2:
                            alerts.append({
                                'type': 'item_alert',
                                'item': safe_string(item),
                                'issue_count': int(count),
                                'priority': 'medium',
                                'message': f'Item "{safe_string(item)}" apresenta {int(count)} não conformidades'
                            })
            
            # Se não há alertas, retornar lista vazia (não None)
            return alerts if alerts else []
            
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
        else:
            print("\nNenhum veículo encontrado.")
        
        driver_perf = processor.get_driver_performance(enterprise_id=test_enterprise_id, days=30)
        if driver_perf:
            print(f"\nPerformance de Motoristas ({len(driver_perf)} motoristas):")
            for driver in driver_perf[:3]:  # Top 3
                print(f"- {driver['driver_name']}: {driver['compliance_rate']}% conformidade")
        else:
            print("\nNenhum motorista encontrado.")
        
        alerts = processor.get_maintenance_alerts(enterprise_id=test_enterprise_id)
        if alerts:
            print(f"\nAlertas de Manutenção ({len(alerts)} alertas):")
            for alert in alerts:
                print(f"- {alert['message']} (Prioridade: {alert['priority']})")
        else:
            print("\nNenhum alerta de manutenção encontrado.")
                
    except Exception as e:
        logger.error(f"Erro no teste: {e}")
