"""
Copiloto Inteligente de Gestão de Frotas
Módulo de Conexão e Processamento de Dados
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

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FleetAPIConfig:
    """Configuração da API de gestão de frotas"""
    base_url: str = "https://firebase-bi-api.onrender.com"
    timeout: int = 30
    max_retries: int = 3

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
                    raise
                    
        return []
    
    def get_checklist_data(self, enterprise_id: str = None, 
                          start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Obtém dados de checklist"""
        params = {}
        if enterprise_id:
            params['enterpriseId'] = enterprise_id
            
        data = self._make_request('/checklist', params)
        df = pd.DataFrame(data)
        
        if not df.empty:
            # Conversão de tipos
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['issueOpenDate'] = pd.to_datetime(df['issueOpenDate'])
            
            # Filtros de data
            if start_date:
                df = df[df['timestamp'] >= start_date]
            if end_date:
                df = df[df['timestamp'] <= end_date]
                
        return df
    
    def get_alerts_checkin_data(self, enterprise_id: str = None,
                               start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Obtém dados de alertas de check-in (telemática)"""
        params = {}
        if enterprise_id:
            params['enterpriseId'] = enterprise_id
            
        data = self._make_request('/alerts-checkin', params)
        df = pd.DataFrame(data)
        
        if not df.empty:
            # Conversão de tipos
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Extração de coordenadas
            if 'location' in df.columns:
                df['latitude'] = df['location'].apply(lambda x: x.get('latitude') if isinstance(x, dict) else None)
                df['longitude'] = df['location'].apply(lambda x: x.get('longitude') if isinstance(x, dict) else None)
            
            # Filtros de data
            if start_date:
                df = df[df['timestamp'] >= start_date]
            if end_date:
                df = df[df['timestamp'] <= end_date]
                
        return df
    
    def get_driver_trips_data(self, enterprise_id: str = None,
                             start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Obtém dados de viagens de motoristas"""
        params = {}
        if enterprise_id:
            params['enterpriseId'] = enterprise_id
            
        data = self._make_request('/driver-trips', params)
        df = pd.DataFrame(data)
        
        if not df.empty and start_date:
            # Assumindo que existe campo de timestamp
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                if start_date:
                    df = df[df['timestamp'] >= start_date]
                if end_date:
                    df = df[df['timestamp'] <= end_date]
                    
        return df
    
    def get_incidents_data(self, enterprise_id: str = None,
                          start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Obtém dados de incidentes"""
        params = {}
        if enterprise_id:
            params['enterpriseId'] = enterprise_id
            
        data = self._make_request('/incidents', params)
        df = pd.DataFrame(data)
        
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filtros de data
            if start_date:
                df = df[df['timestamp'] >= start_date]
            if end_date:
                df = df[df['timestamp'] <= end_date]
                
        return df

class FleetDataProcessor:
    """Processador de dados de frota para análises"""
    
    def __init__(self, connector: FleetDataConnector):
        self.connector = connector
        
    def get_checklist_summary(self, enterprise_id: str = None, days: int = 7) -> Dict[str, Any]:
        """Gera resumo de checklists"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        df = self.connector.get_checklist_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if df.empty:
            return {"total": 0, "compliant": 0, "non_compliant": 0, "compliance_rate": 0}
        
        # Calcular métricas de conformidade
        if 'noCompliant' in df.columns:
            # Usar a coluna noCompliant (True = não conforme, False = conforme)
            compliant = len(df[df['noCompliant'] == False])
            non_compliant = len(df[df['noCompliant'] == True])
        else:
            # Fallback se não houver coluna de conformidade
            compliant = len(df)
            non_compliant = 0
        
        total = len(df)
        compliance_rate = (compliant / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "compliant": compliant,
            "non_compliant": non_compliant,
            "compliance_rate": round(compliance_rate, 2),
            "period_days": days,
            "vehicles": df['vehiclePlate'].nunique() if 'vehiclePlate' in df.columns else 0,
            "drivers": df['driverName'].nunique() if 'driverName' in df.columns else 0
        }
    
    def get_vehicle_performance(self, enterprise_id: str = None, days: int = 30) -> pd.DataFrame:
        """Análise de performance por veículo"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Dados de checklist
        checklist_df = self.connector.get_checklist_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        # Dados de telemática
        telemetry_df = self.connector.get_alerts_checkin_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        performance_data = []
        
        if not checklist_df.empty:
            # Análise por veículo
            for vehicle in checklist_df['vehiclePlate'].unique():
                vehicle_data = checklist_df[checklist_df['vehiclePlate'] == vehicle]
                
                # Métricas de checklist
                total_checks = len(vehicle_data)
                compliant_checks = len(vehicle_data[vehicle_data['noCompliant'] == False]) if 'noCompliant' in vehicle_data.columns else len(vehicle_data)
                compliance_rate = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
                
                # Dados de telemática para o veículo
                vehicle_telemetry = telemetry_df[telemetry_df['vehiclePlate'] == vehicle] if not telemetry_df.empty else pd.DataFrame()
                
                avg_temp = vehicle_telemetry['temperature'].mean() if not vehicle_telemetry.empty and 'temperature' in vehicle_telemetry.columns else None
                avg_humidity = vehicle_telemetry['humidity'].mean() if not vehicle_telemetry.empty and 'humidity' in vehicle_telemetry.columns else None
                total_distance = vehicle_telemetry['distance'].sum() if not vehicle_telemetry.empty and 'distance' in vehicle_telemetry.columns else None
                
                performance_data.append({
                    'vehicle_plate': vehicle,
                    'total_checks': total_checks,
                    'compliance_rate': round(compliance_rate, 2),
                    'avg_temperature': round(avg_temp, 2) if avg_temp else None,
                    'avg_humidity': round(avg_humidity, 2) if avg_humidity else None,
                    'total_distance': total_distance,
                    'last_check': vehicle_data['timestamp'].max()
                })
        
        return pd.DataFrame(performance_data)
    
    def get_driver_performance(self, enterprise_id: str = None, days: int = 30) -> pd.DataFrame:
        """Análise de performance por motorista"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        checklist_df = self.connector.get_checklist_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if checklist_df.empty:
            return pd.DataFrame()
        
        driver_performance = []
        
        for driver in checklist_df['driverName'].unique():
            driver_data = checklist_df[checklist_df['driverName'] == driver]
            
            total_checks = len(driver_data)
            compliant_checks = len(driver_data[driver_data['noCompliant'] == False]) if 'noCompliant' in driver_data.columns else len(driver_data)
            compliance_rate = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
            
            vehicles_operated = driver_data['vehiclePlate'].nunique()
            
            driver_performance.append({
                'driver_name': driver,
                'total_checks': total_checks,
                'compliance_rate': round(compliance_rate, 2),
                'vehicles_operated': vehicles_operated,
                'last_activity': driver_data['timestamp'].max()
            })
        
        return pd.DataFrame(driver_performance).sort_values('compliance_rate', ascending=False)
    
    def get_maintenance_alerts(self, enterprise_id: str = None) -> List[Dict[str, Any]]:
        """Identifica alertas de manutenção baseados nos dados"""
        checklist_df = self.connector.get_checklist_data(enterprise_id=enterprise_id)
        
        if checklist_df.empty:
            return []
        
        alerts = []
        
        # Veículos com muitas não conformidades
        non_compliant = checklist_df[checklist_df['compliant'] == False]
        
        if not non_compliant.empty:
            vehicle_issues = non_compliant.groupby('vehiclePlate').size().sort_values(ascending=False)
            
            for vehicle, count in vehicle_issues.head(5).items():
                if count >= 3:  # Threshold para alerta
                    alerts.append({
                        'type': 'maintenance_required',
                        'vehicle': vehicle,
                        'issue_count': count,
                        'priority': 'high' if count >= 5 else 'medium',
                        'message': f'Veículo {vehicle} tem {count} não conformidades recentes'
                    })
        
        return alerts

if __name__ == "__main__":
    # Teste básico do módulo
    connector = FleetDataConnector()
    processor = FleetDataProcessor(connector)
    
    # Teste de conexão
    try:
        summary = processor.get_checklist_summary(days=30)
        print("Resumo de Checklists (últimos 30 dias):")
        print(json.dumps(summary, indent=2, default=str))
        
        vehicle_perf = processor.get_vehicle_performance(days=30)
        if not vehicle_perf.empty:
            print("\nTop 5 Veículos por Performance:")
            print(vehicle_perf.head().to_string(index=False))
        
        alerts = processor.get_maintenance_alerts()
        if alerts:
            print("\nAlertas de Manutenção:")
            for alert in alerts:
                print(f"- {alert['message']} (Prioridade: {alert['priority']})")
                
    except Exception as e:
        logger.error(f"Erro no teste: {e}")

