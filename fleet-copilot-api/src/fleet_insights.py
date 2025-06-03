"""
Copiloto Inteligente de Gestão de Frotas
Sistema de Geração de Insights e Análises Automáticas
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import logging
from dataclasses import dataclass
from collections import defaultdict
import statistics

logger = logging.getLogger(__name__)

@dataclass
class Insight:
    """Estrutura para representar um insight"""
    title: str
    description: str
    category: str
    priority: str  # 'high', 'medium', 'low'
    impact: str    # 'positive', 'negative', 'neutral'
    recommendation: str
    data: Dict[str, Any]
    timestamp: datetime

@dataclass
class Alert:
    """Estrutura para representar um alerta"""
    title: str
    message: str
    severity: str  # 'critical', 'warning', 'info'
    category: str
    affected_items: List[str]
    timestamp: datetime
    action_required: bool

class FleetInsightsEngine:
    """Motor de insights para gestão de frotas"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.insights_history = []
        self.alerts_history = []
        
        # Thresholds configuráveis
        self.thresholds = {
            'compliance_rate_warning': 85.0,
            'compliance_rate_critical': 70.0,
            'max_days_without_check': 7,
            'temperature_warning': 35.0,
            'temperature_critical': 40.0,
            'humidity_warning': 80.0,
            'min_checks_per_vehicle': 2,
            'performance_decline_threshold': 10.0
        }
    
    def generate_comprehensive_analysis(self, enterprise_id: str = None, days: int = 30) -> Dict[str, Any]:
        """Gera análise abrangente da frota"""
        logger.info(f"Gerando análise abrangente para os últimos {days} dias")
        
        analysis = {
            'summary': self._generate_summary_insights(enterprise_id, days),
            'vehicle_insights': self._analyze_vehicle_performance(enterprise_id, days),
            'driver_insights': self._analyze_driver_performance(enterprise_id, days),
            'maintenance_insights': self._analyze_maintenance_patterns(enterprise_id, days),
            'safety_insights': self._analyze_safety_metrics(enterprise_id, days),
            'operational_insights': self._analyze_operational_efficiency(enterprise_id, days),
            'alerts': self._generate_alerts(enterprise_id, days),
            'recommendations': self._generate_recommendations(enterprise_id, days),
            'trends': self._analyze_trends(enterprise_id, days),
            'generated_at': datetime.now().isoformat()
        }
        
        return analysis
    
    def _generate_summary_insights(self, enterprise_id: str, days: int) -> Dict[str, Any]:
        """Gera insights de resumo geral"""
        summary = self.data_processor.get_checklist_summary(enterprise_id, days)
        
        insights = []
        
        # Insight sobre taxa de conformidade geral
        compliance_rate = summary['compliance_rate']
        if compliance_rate >= 95:
            insights.append(Insight(
                title="Excelente Conformidade",
                description=f"A frota mantém uma taxa de conformidade de {compliance_rate}%, indicando excelente gestão de manutenção.",
                category="performance",
                priority="low",
                impact="positive",
                recommendation="Manter os procedimentos atuais e considerar compartilhar as melhores práticas.",
                data={"compliance_rate": compliance_rate},
                timestamp=datetime.now()
            ))
        elif compliance_rate >= 85:
            insights.append(Insight(
                title="Boa Conformidade",
                description=f"A frota apresenta taxa de conformidade de {compliance_rate}%, dentro do padrão aceitável.",
                category="performance",
                priority="medium",
                impact="positive",
                recommendation="Identificar e corrigir as principais causas de não conformidade para melhorar ainda mais.",
                data={"compliance_rate": compliance_rate},
                timestamp=datetime.now()
            ))
        else:
            insights.append(Insight(
                title="Conformidade Abaixo do Esperado",
                description=f"A taxa de conformidade de {compliance_rate}% está abaixo do ideal e requer atenção imediata.",
                category="performance",
                priority="high",
                impact="negative",
                recommendation="Implementar programa intensivo de treinamento e revisão dos procedimentos de checklist.",
                data={"compliance_rate": compliance_rate},
                timestamp=datetime.now()
            ))
        
        # Insight sobre atividade da frota
        total_checks = summary['total']
        vehicles = summary['vehicles']
        drivers = summary['drivers']
        
        if vehicles > 0:
            checks_per_vehicle = total_checks / vehicles
            if checks_per_vehicle < self.thresholds['min_checks_per_vehicle']:
                insights.append(Insight(
                    title="Baixa Frequência de Verificações",
                    description=f"Média de {checks_per_vehicle:.1f} verificações por veículo nos últimos {days} dias.",
                    category="operational",
                    priority="medium",
                    impact="negative",
                    recommendation="Aumentar a frequência de verificações para garantir melhor monitoramento da frota.",
                    data={"checks_per_vehicle": checks_per_vehicle, "total_vehicles": vehicles},
                    timestamp=datetime.now()
                ))
        
        return {
            'insights': [insight.__dict__ for insight in insights],
            'metrics': summary
        }
    
    def _analyze_vehicle_performance(self, enterprise_id: str, days: int) -> Dict[str, Any]:
        """Analisa performance individual dos veículos"""
        vehicle_perf = self.data_processor.get_vehicle_performance(enterprise_id, days)
        
        if vehicle_perf.empty:
            return {'insights': [], 'top_performers': [], 'attention_needed': []}
        
        insights = []
        
        # Identificar top performers
        top_performers = vehicle_perf.nlargest(3, 'compliance_rate')
        
        # Identificar veículos que precisam de atenção
        attention_needed = vehicle_perf[
            vehicle_perf['compliance_rate'] < self.thresholds['compliance_rate_warning']
        ].sort_values('compliance_rate')
        
        # Insight sobre dispersão de performance
        compliance_std = vehicle_perf['compliance_rate'].std()
        if compliance_std > 15:
            insights.append(Insight(
                title="Alta Variabilidade na Performance",
                description=f"Há grande variação na performance entre veículos (desvio padrão: {compliance_std:.1f}%).",
                category="performance",
                priority="medium",
                impact="negative",
                recommendation="Padronizar procedimentos e treinar motoristas dos veículos com menor performance.",
                data={"std_deviation": compliance_std},
                timestamp=datetime.now()
            ))
        
        # Insight sobre veículos problemáticos
        if not attention_needed.empty:
            worst_vehicle = attention_needed.iloc[0]
            insights.append(Insight(
                title="Veículo Requer Atenção Urgente",
                description=f"Veículo {worst_vehicle['vehicle_plate']} tem taxa de conformidade de apenas {worst_vehicle['compliance_rate']}%.",
                category="maintenance",
                priority="high",
                impact="negative",
                recommendation="Realizar inspeção detalhada e manutenção preventiva no veículo.",
                data={"vehicle": worst_vehicle['vehicle_plate'], "compliance_rate": worst_vehicle['compliance_rate']},
                timestamp=datetime.now()
            ))
        
        return {
            'insights': [insight.__dict__ for insight in insights],
            'top_performers': top_performers.to_dict('records'),
            'attention_needed': attention_needed.to_dict('records'),
            'average_compliance': vehicle_perf['compliance_rate'].mean(),
            'total_vehicles_analyzed': len(vehicle_perf)
        }
    
    def _analyze_driver_performance(self, enterprise_id: str, days: int) -> Dict[str, Any]:
        """Analisa performance dos motoristas"""
        driver_perf = self.data_processor.get_driver_performance(enterprise_id, days)
        
        if driver_perf.empty:
            return {'insights': [], 'top_performers': [], 'training_needed': []}
        
        insights = []
        
        # Top performers
        top_performers = driver_perf.nlargest(3, 'compliance_rate')
        
        # Motoristas que precisam de treinamento
        training_needed = driver_perf[
            driver_perf['compliance_rate'] < self.thresholds['compliance_rate_warning']
        ].sort_values('compliance_rate')
        
        # Insight sobre consistência dos motoristas
        avg_compliance = driver_perf['compliance_rate'].mean()
        if avg_compliance >= 90:
            insights.append(Insight(
                title="Equipe de Motoristas Bem Treinada",
                description=f"Taxa média de conformidade dos motoristas é de {avg_compliance:.1f}%.",
                category="performance",
                priority="low",
                impact="positive",
                recommendation="Reconhecer e recompensar os motoristas com melhor performance.",
                data={"average_compliance": avg_compliance},
                timestamp=datetime.now()
            ))
        
        # Insight sobre necessidade de treinamento
        if not training_needed.empty:
            insights.append(Insight(
                title="Motoristas Precisam de Treinamento",
                description=f"{len(training_needed)} motorista(s) apresentam performance abaixo do esperado.",
                category="training",
                priority="medium",
                impact="negative",
                recommendation="Implementar programa de treinamento focado em procedimentos de segurança.",
                data={"drivers_count": len(training_needed)},
                timestamp=datetime.now()
            ))
        
        return {
            'insights': [insight.__dict__ for insight in insights],
            'top_performers': top_performers.to_dict('records'),
            'training_needed': training_needed.to_dict('records'),
            'average_compliance': avg_compliance,
            'total_drivers_analyzed': len(driver_perf)
        }
    
    def _analyze_maintenance_patterns(self, enterprise_id: str, days: int) -> Dict[str, Any]:
        """Analisa padrões de manutenção"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        checklist_df = self.data_processor.connector.get_checklist_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if checklist_df.empty:
            return {'insights': [], 'common_issues': [], 'maintenance_schedule': []}
        
        insights = []
        
        # Análise de itens mais problemáticos
        non_compliant = checklist_df[checklist_df['compliant'] == False]
        if not non_compliant.empty:
            common_issues = non_compliant['itemName'].value_counts().head(5)
            
            most_common_issue = common_issues.index[0]
            issue_count = common_issues.iloc[0]
            
            insights.append(Insight(
                title="Item de Manutenção Mais Problemático",
                description=f"'{most_common_issue}' apresentou {issue_count} não conformidades.",
                category="maintenance",
                priority="high",
                impact="negative",
                recommendation="Revisar procedimentos de manutenção preventiva para este item específico.",
                data={"item": most_common_issue, "count": issue_count},
                timestamp=datetime.now()
            ))
        
        # Análise temporal de manutenção
        checklist_df['date'] = checklist_df['timestamp'].dt.date
        daily_issues = checklist_df[checklist_df['compliant'] == False].groupby('date').size()
        
        if len(daily_issues) > 0:
            avg_daily_issues = daily_issues.mean()
            if avg_daily_issues > 2:
                insights.append(Insight(
                    title="Alta Frequência de Problemas",
                    description=f"Média de {avg_daily_issues:.1f} problemas por dia detectados.",
                    category="maintenance",
                    priority="medium",
                    impact="negative",
                    recommendation="Intensificar manutenção preventiva para reduzir problemas recorrentes.",
                    data={"avg_daily_issues": avg_daily_issues},
                    timestamp=datetime.now()
                ))
        
        return {
            'insights': [insight.__dict__ for insight in insights],
            'common_issues': common_issues.to_dict() if not non_compliant.empty else {},
            'total_issues': len(non_compliant),
            'issues_trend': {str(k): v for k, v in daily_issues.to_dict().items()} if len(daily_issues) > 0 else {}
        }
    
    def _analyze_safety_metrics(self, enterprise_id: str, days: int) -> Dict[str, Any]:
        """Analisa métricas de segurança"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Dados de telemática para análise de segurança
        telemetry_df = self.data_processor.connector.get_alerts_checkin_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        insights = []
        
        if not telemetry_df.empty and 'temperature' in telemetry_df.columns:
            # Análise de temperatura
            avg_temp = telemetry_df['temperature'].mean()
            max_temp = telemetry_df['temperature'].max()
            
            if max_temp > self.thresholds['temperature_critical']:
                insights.append(Insight(
                    title="Temperatura Crítica Detectada",
                    description=f"Temperatura máxima de {max_temp}°C registrada, acima do limite crítico.",
                    category="safety",
                    priority="high",
                    impact="negative",
                    recommendation="Verificar sistema de refrigeração e condições de operação dos veículos.",
                    data={"max_temperature": max_temp, "avg_temperature": avg_temp},
                    timestamp=datetime.now()
                ))
            elif max_temp > self.thresholds['temperature_warning']:
                insights.append(Insight(
                    title="Temperatura Elevada",
                    description=f"Temperatura máxima de {max_temp}°C próxima do limite de atenção.",
                    category="safety",
                    priority="medium",
                    impact="negative",
                    recommendation="Monitorar condições de temperatura e considerar manutenção preventiva.",
                    data={"max_temperature": max_temp, "avg_temperature": avg_temp},
                    timestamp=datetime.now()
                ))
        
        # Análise de bateria baixa
        if not telemetry_df.empty and 'lowBattery' in telemetry_df.columns:
            low_battery_count = telemetry_df['lowBattery'].sum()
            if low_battery_count > 0:
                insights.append(Insight(
                    title="Alertas de Bateria Baixa",
                    description=f"{low_battery_count} alertas de bateria baixa registrados.",
                    category="safety",
                    priority="medium",
                    impact="negative",
                    recommendation="Verificar e substituir baterias dos dispositivos de monitoramento.",
                    data={"low_battery_alerts": low_battery_count},
                    timestamp=datetime.now()
                ))
        
        return {
            'insights': [insight.__dict__ for insight in insights],
            'temperature_stats': {
                'avg': telemetry_df['temperature'].mean() if not telemetry_df.empty and 'temperature' in telemetry_df.columns else None,
                'max': telemetry_df['temperature'].max() if not telemetry_df.empty and 'temperature' in telemetry_df.columns else None,
                'min': telemetry_df['temperature'].min() if not telemetry_df.empty and 'temperature' in telemetry_df.columns else None
            },
            'battery_alerts': telemetry_df['lowBattery'].sum() if not telemetry_df.empty and 'lowBattery' in telemetry_df.columns else 0
        }
    
    def _analyze_operational_efficiency(self, enterprise_id: str, days: int) -> Dict[str, Any]:
        """Analisa eficiência operacional"""
        summary = self.data_processor.get_checklist_summary(enterprise_id, days)
        vehicle_perf = self.data_processor.get_vehicle_performance(enterprise_id, days)
        
        insights = []
        
        # Análise de utilização da frota
        if summary['vehicles'] > 0 and summary['total'] > 0:
            checks_per_vehicle = summary['total'] / summary['vehicles']
            
            if checks_per_vehicle > 10:
                insights.append(Insight(
                    title="Alta Utilização da Frota",
                    description=f"Média de {checks_per_vehicle:.1f} verificações por veículo indica alta atividade.",
                    category="operational",
                    priority="low",
                    impact="positive",
                    recommendation="Manter o nível atual de utilização e monitorar desgaste dos veículos.",
                    data={"checks_per_vehicle": checks_per_vehicle},
                    timestamp=datetime.now()
                ))
            elif checks_per_vehicle < 3:
                insights.append(Insight(
                    title="Baixa Utilização da Frota",
                    description=f"Média de apenas {checks_per_vehicle:.1f} verificações por veículo.",
                    category="operational",
                    priority="medium",
                    impact="negative",
                    recommendation="Avaliar necessidade de otimização da frota ou aumento da utilização.",
                    data={"checks_per_vehicle": checks_per_vehicle},
                    timestamp=datetime.now()
                ))
        
        # Análise de eficiência de motoristas
        if summary['drivers'] > 0:
            checks_per_driver = summary['total'] / summary['drivers']
            insights.append(Insight(
                title="Produtividade dos Motoristas",
                description=f"Média de {checks_per_driver:.1f} verificações por motorista.",
                category="operational",
                priority="low",
                impact="neutral",
                recommendation="Monitorar produtividade e balancear carga de trabalho entre motoristas.",
                data={"checks_per_driver": checks_per_driver},
                timestamp=datetime.now()
            ))
        
        return {
            'insights': [insight.__dict__ for insight in insights],
            'utilization_metrics': {
                'checks_per_vehicle': summary['total'] / summary['vehicles'] if summary['vehicles'] > 0 else 0,
                'checks_per_driver': summary['total'] / summary['drivers'] if summary['drivers'] > 0 else 0,
                'total_vehicles': summary['vehicles'],
                'total_drivers': summary['drivers']
            }
        }
    
    def _generate_alerts(self, enterprise_id: str, days: int) -> List[Dict[str, Any]]:
        """Gera alertas baseados nos dados atuais"""
        alerts = []
        
        # Usar o sistema de alertas existente
        maintenance_alerts = self.data_processor.get_maintenance_alerts(enterprise_id)
        
        for alert in maintenance_alerts:
            alerts.append(Alert(
                title=alert.get('type', 'Alerta de Manutenção'),
                message=alert.get('message', ''),
                severity='critical' if alert.get('priority') == 'high' else 'warning',
                category='maintenance',
                affected_items=[alert.get('vehicle', '')],
                timestamp=datetime.now(),
                action_required=True
            ).__dict__)
        
        return alerts
    
    def _generate_recommendations(self, enterprise_id: str, days: int) -> List[Dict[str, Any]]:
        """Gera recomendações estratégicas"""
        summary = self.data_processor.get_checklist_summary(enterprise_id, days)
        
        recommendations = []
        
        # Recomendações baseadas na taxa de conformidade
        if summary['compliance_rate'] < 90:
            recommendations.append({
                'title': 'Melhorar Procedimentos de Checklist',
                'description': 'Implementar treinamento adicional para aumentar taxa de conformidade',
                'priority': 'high',
                'estimated_impact': 'Aumento de 10-15% na conformidade',
                'timeline': '2-4 semanas'
            })
        
        # Recomendações baseadas no volume de verificações
        if summary['total'] < summary['vehicles'] * 5:  # Menos de 5 checks por veículo
            recommendations.append({
                'title': 'Aumentar Frequência de Verificações',
                'description': 'Estabelecer cronograma mais rigoroso de inspeções',
                'priority': 'medium',
                'estimated_impact': 'Detecção precoce de 20-30% mais problemas',
                'timeline': '1-2 semanas'
            })
        
        return recommendations
    
    def _analyze_trends(self, enterprise_id: str, days: int) -> Dict[str, Any]:
        """Analisa tendências temporais"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        checklist_df = self.data_processor.connector.get_checklist_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if checklist_df.empty:
            return {'trends': [], 'forecast': {}}
        
        # Análise de tendência semanal
        checklist_df['week'] = checklist_df['timestamp'].dt.isocalendar().week
        weekly_compliance = checklist_df.groupby('week')['compliant'].mean() * 100
        
        trends = []
        
        if len(weekly_compliance) >= 2:
            # Calcular tendência
            recent_avg = weekly_compliance.tail(2).mean()
            older_avg = weekly_compliance.head(2).mean() if len(weekly_compliance) >= 4 else weekly_compliance.mean()
            
            trend_direction = "melhorando" if recent_avg > older_avg else "piorando"
            trend_magnitude = abs(recent_avg - older_avg)
            
            trends.append({
                'metric': 'Taxa de Conformidade',
                'direction': trend_direction,
                'magnitude': round(trend_magnitude, 2),
                'description': f'Taxa de conformidade está {trend_direction} em {trend_magnitude:.1f}% nas últimas semanas'
            })
        
        return {
            'trends': trends,
            'weekly_compliance': {str(k): v for k, v in weekly_compliance.to_dict().items()},
            'forecast': {
                'next_week_compliance': weekly_compliance.mean() if len(weekly_compliance) > 0 else 0
            }
        }
    
    def generate_natural_language_summary(self, analysis: Dict[str, Any]) -> str:
        """Gera resumo em linguagem natural da análise"""
        summary_parts = []
        
        # Resumo geral
        metrics = analysis['summary']['metrics']
        summary_parts.append(f"Nos últimos dias, sua frota realizou {metrics['total']} verificações em {metrics['vehicles']} veículos, "
                            f"com uma taxa de conformidade de {metrics['compliance_rate']}%.")
        
        # Insights principais
        all_insights = []
        for category in ['summary', 'vehicle_insights', 'driver_insights', 'maintenance_insights', 'safety_insights']:
            if category in analysis and 'insights' in analysis[category]:
                all_insights.extend(analysis[category]['insights'])
        
        high_priority_insights = [i for i in all_insights if i['priority'] == 'high']
        if high_priority_insights:
            summary_parts.append(f"Foram identificados {len(high_priority_insights)} pontos que requerem atenção imediata.")
        
        # Alertas
        if analysis['alerts']:
            summary_parts.append(f"Há {len(analysis['alerts'])} alertas ativos que precisam de ação.")
        
        # Recomendações
        if analysis['recommendations']:
            summary_parts.append(f"O sistema gerou {len(analysis['recommendations'])} recomendações para melhorar a operação.")
        
        return " ".join(summary_parts)

if __name__ == "__main__":
    # Teste do sistema de insights
    from fleet_data_connector import FleetDataConnector, FleetDataProcessor
    
    connector = FleetDataConnector()
    processor = FleetDataProcessor(connector)
    insights_engine = FleetInsightsEngine(processor)
    
    print("Gerando análise abrangente...")
    
    try:
        analysis = insights_engine.generate_comprehensive_analysis(days=30)
        
        # Salvar análise completa
        with open("/home/ubuntu/fleet_analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        # Gerar resumo em linguagem natural
        summary = insights_engine.generate_natural_language_summary(analysis)
        
        print("✓ Análise abrangente gerada")
        print(f"\nResumo: {summary}")
        
        # Mostrar alguns insights
        print(f"\nInsights encontrados:")
        for category, data in analysis.items():
            if isinstance(data, dict) and 'insights' in data:
                for insight in data['insights']:
                    print(f"- [{insight['priority'].upper()}] {insight['title']}: {insight['description']}")
        
        print(f"\nAlertas: {len(analysis['alerts'])}")
        print(f"Recomendações: {len(analysis['recommendations'])}")
        
    except Exception as e:
        print(f"Erro ao gerar insights: {e}")

