"""
Copiloto Inteligente de Gestão de Frotas
Sistema de Visualização de Dados e Gráficos
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import base64
import io
import warnings

# Configurações de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
warnings.filterwarnings('ignore')

# Configuração para português
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

class FleetVisualizationEngine:
    """Motor de visualização para dados de gestão de frotas"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'warning': '#C73E1D',
            'info': '#5D737E',
            'compliant': '#28a745',
            'non_compliant': '#dc3545'
        }
    
    def create_checklist_summary_chart(self, enterprise_id: str = None, days: int = 7) -> str:
        """Cria gráfico de resumo de checklists"""
        summary = self.data_processor.get_checklist_summary(enterprise_id, days)
        
        # Gráfico de pizza para conformidade
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Pizza de conformidade
        labels = ['Conformes', 'Não Conformes']
        sizes = [summary['compliant'], summary['non_compliant']]
        colors = [self.colors['compliant'], self.colors['non_compliant']]
        
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title(f'Conformidade de Checklists\n(Últimos {days} dias)', fontsize=14, fontweight='bold')
        
        # Gráfico de barras com métricas
        metrics = ['Total', 'Conformes', 'Não Conformes', 'Veículos', 'Motoristas']
        values = [summary['total'], summary['compliant'], summary['non_compliant'], 
                 summary['vehicles'], summary['drivers']]
        
        bars = ax2.bar(metrics, values, color=[self.colors['info'], self.colors['compliant'], 
                                              self.colors['non_compliant'], self.colors['primary'], 
                                              self.colors['secondary']])
        
        ax2.set_title('Métricas Gerais', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Quantidade')
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_vehicle_performance_chart(self, enterprise_id: str = None, days: int = 30) -> str:
        """Cria gráfico de performance de veículos"""
        df = self.data_processor.get_vehicle_performance(enterprise_id, days)
        
        if df.empty:
            return self._create_no_data_chart("Nenhum dado de performance de veículos encontrado")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Gráfico de barras - Taxa de conformidade por veículo
        vehicles = df['vehicle_plate'].tolist()
        compliance_rates = df['compliance_rate'].tolist()
        
        bars1 = ax1.bar(vehicles, compliance_rates, color=self.colors['primary'])
        ax1.set_title('Taxa de Conformidade por Veículo (%)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Taxa de Conformidade (%)')
        ax1.set_ylim(0, 100)
        ax1.tick_params(axis='x', rotation=45)
        
        # Adicionar valores nas barras
        for bar, rate in zip(bars1, compliance_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate}%', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de barras - Total de verificações por veículo
        total_checks = df['total_checks'].tolist()
        bars2 = ax2.bar(vehicles, total_checks, color=self.colors['secondary'])
        ax2.set_title('Total de Verificações por Veículo', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Número de Verificações')
        ax2.set_xlabel('Veículos')
        ax2.tick_params(axis='x', rotation=45)
        
        # Adicionar valores nas barras
        for bar, checks in zip(bars2, total_checks):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{checks}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_driver_performance_chart(self, enterprise_id: str = None, days: int = 30) -> str:
        """Cria gráfico de performance de motoristas"""
        df = self.data_processor.get_driver_performance(enterprise_id, days)
        
        if df.empty:
            return self._create_no_data_chart("Nenhum dado de performance de motoristas encontrado")
        
        # Limitar aos top 10 motoristas
        df_top = df.head(10)
        
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Gráfico de barras horizontais
        drivers = df_top['driver_name'].tolist()
        compliance_rates = df_top['compliance_rate'].tolist()
        total_checks = df_top['total_checks'].tolist()
        
        # Criar cores baseadas na taxa de conformidade
        colors = []
        for rate in compliance_rates:
            if rate >= 95:
                colors.append(self.colors['compliant'])
            elif rate >= 80:
                colors.append(self.colors['warning'])
            else:
                colors.append(self.colors['non_compliant'])
        
        bars = ax.barh(drivers, compliance_rates, color=colors)
        ax.set_title('Top 10 Motoristas - Taxa de Conformidade (%)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Taxa de Conformidade (%)')
        ax.set_xlim(0, 100)
        
        # Adicionar valores nas barras e número de verificações
        for i, (bar, rate, checks) in enumerate(zip(bars, compliance_rates, total_checks)):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2.,
                    f'{rate}% ({checks} checks)', ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_timeline_chart(self, enterprise_id: str = None, days: int = 30) -> str:
        """Cria gráfico de linha temporal de atividades"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Obter dados de checklist
        checklist_df = self.data_processor.connector.get_checklist_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if checklist_df.empty:
            return self._create_no_data_chart("Nenhum dado temporal encontrado")
        
        # Agrupar por data
        checklist_df['date'] = checklist_df['timestamp'].dt.date
        daily_stats = checklist_df.groupby('date').agg({
            'compliant': ['count', 'sum'],
            'vehiclePlate': 'nunique'
        }).reset_index()
        
        daily_stats.columns = ['date', 'total_checks', 'compliant_checks', 'unique_vehicles']
        daily_stats['non_compliant_checks'] = daily_stats['total_checks'] - daily_stats['compliant_checks']
        daily_stats['compliance_rate'] = (daily_stats['compliant_checks'] / daily_stats['total_checks'] * 100).round(2)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Gráfico de linha - Taxa de conformidade ao longo do tempo
        ax1.plot(daily_stats['date'], daily_stats['compliance_rate'], 
                marker='o', linewidth=2, markersize=6, color=self.colors['primary'])
        ax1.set_title('Taxa de Conformidade ao Longo do Tempo', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Taxa de Conformidade (%)')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de barras empilhadas - Verificações por dia
        ax2.bar(daily_stats['date'], daily_stats['compliant_checks'], 
               label='Conformes', color=self.colors['compliant'])
        ax2.bar(daily_stats['date'], daily_stats['non_compliant_checks'], 
               bottom=daily_stats['compliant_checks'], label='Não Conformes', 
               color=self.colors['non_compliant'])
        
        ax2.set_title('Verificações Diárias', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Número de Verificações')
        ax2.set_xlabel('Data')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Formatar datas no eixo x
        for ax in [ax1, ax2]:
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_temperature_humidity_chart(self, enterprise_id: str = None, days: int = 7) -> str:
        """Cria gráfico de temperatura e umidade dos veículos"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Obter dados de telemática
        telemetry_df = self.data_processor.connector.get_alerts_checkin_data(
            enterprise_id=enterprise_id,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        if telemetry_df.empty or 'temperature' not in telemetry_df.columns:
            return self._create_no_data_chart("Nenhum dado de temperatura/umidade encontrado")
        
        # Agrupar por hora para reduzir ruído
        telemetry_df['hour'] = telemetry_df['timestamp'].dt.floor('H')
        hourly_stats = telemetry_df.groupby('hour').agg({
            'temperature': 'mean',
            'humidity': 'mean'
        }).reset_index()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Gráfico de temperatura
        ax1.plot(hourly_stats['hour'], hourly_stats['temperature'], 
                marker='o', linewidth=2, markersize=4, color=self.colors['warning'])
        ax1.set_title('Temperatura Média dos Veículos', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Temperatura (°C)')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de umidade
        ax2.plot(hourly_stats['hour'], hourly_stats['humidity'], 
                marker='s', linewidth=2, markersize=4, color=self.colors['info'])
        ax2.set_title('Umidade Média dos Veículos', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Umidade (%)')
        ax2.set_xlabel('Data/Hora')
        ax2.grid(True, alpha=0.3)
        
        # Formatar datas
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_interactive_dashboard(self, enterprise_id: str = None) -> str:
        """Cria dashboard interativo com Plotly"""
        # Obter dados
        summary = self.data_processor.get_checklist_summary(enterprise_id, days=30)
        vehicle_perf = self.data_processor.get_vehicle_performance(enterprise_id, days=30)
        driver_perf = self.data_processor.get_driver_performance(enterprise_id, days=30)
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Resumo de Conformidade', 'Performance de Veículos', 
                          'Top 5 Motoristas', 'Métricas Gerais'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Gráfico de pizza - Conformidade
        fig.add_trace(
            go.Pie(labels=['Conformes', 'Não Conformes'],
                   values=[summary['compliant'], summary['non_compliant']],
                   marker_colors=[self.colors['compliant'], self.colors['non_compliant']]),
            row=1, col=1
        )
        
        # Gráfico de barras - Performance de veículos
        if not vehicle_perf.empty:
            fig.add_trace(
                go.Bar(x=vehicle_perf['vehicle_plate'][:10], 
                       y=vehicle_perf['compliance_rate'][:10],
                       marker_color=self.colors['primary'],
                       name='Taxa de Conformidade'),
                row=1, col=2
            )
        
        # Gráfico de barras - Top motoristas
        if not driver_perf.empty:
            fig.add_trace(
                go.Bar(x=driver_perf['driver_name'][:5], 
                       y=driver_perf['compliance_rate'][:5],
                       marker_color=self.colors['secondary'],
                       name='Taxa de Conformidade'),
                row=2, col=1
            )
        
        # Gráfico de barras - Métricas gerais
        metrics = ['Total', 'Conformes', 'Não Conformes', 'Veículos', 'Motoristas']
        values = [summary['total'], summary['compliant'], summary['non_compliant'], 
                 summary['vehicles'], summary['drivers']]
        
        fig.add_trace(
            go.Bar(x=metrics, y=values,
                   marker_color=[self.colors['info'], self.colors['compliant'], 
                               self.colors['non_compliant'], self.colors['primary'], 
                               self.colors['secondary']],
                   name='Quantidade'),
            row=2, col=2
        )
        
        # Atualizar layout
        fig.update_layout(
            title_text="Dashboard de Gestão de Frotas",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        # Salvar como HTML
        html_str = fig.to_html(include_plotlyjs='cdn')
        
        return html_str
    
    def _create_no_data_chart(self, message: str) -> str:
        """Cria gráfico indicando ausência de dados"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, message, ha='center', va='center', 
                fontsize=16, fontweight='bold', color=self.colors['info'])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def save_chart_to_file(self, chart_base64: str, filename: str) -> str:
        """Salva gráfico em arquivo"""
        image_data = base64.b64decode(chart_base64)
        filepath = f"/home/ubuntu/{filename}"
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return filepath

if __name__ == "__main__":
    # Teste do sistema de visualização
    from fleet_data_connector import FleetDataConnector, FleetDataProcessor
    
    connector = FleetDataConnector()
    processor = FleetDataProcessor(connector)
    viz_engine = FleetVisualizationEngine(processor)
    
    print("Gerando visualizações de teste...")
    
    # Gerar gráficos
    try:
        # Resumo de checklists
        chart1 = viz_engine.create_checklist_summary_chart(days=30)
        viz_engine.save_chart_to_file(chart1, "checklist_summary.png")
        print("✓ Gráfico de resumo de checklists criado")
        
        # Performance de veículos
        chart2 = viz_engine.create_vehicle_performance_chart(days=30)
        viz_engine.save_chart_to_file(chart2, "vehicle_performance.png")
        print("✓ Gráfico de performance de veículos criado")
        
        # Performance de motoristas
        chart3 = viz_engine.create_driver_performance_chart(days=30)
        viz_engine.save_chart_to_file(chart3, "driver_performance.png")
        print("✓ Gráfico de performance de motoristas criado")
        
        # Timeline
        chart4 = viz_engine.create_timeline_chart(days=30)
        viz_engine.save_chart_to_file(chart4, "timeline_chart.png")
        print("✓ Gráfico de timeline criado")
        
        # Dashboard interativo
        dashboard_html = viz_engine.create_interactive_dashboard()
        with open("/home/ubuntu/dashboard.html", "w", encoding="utf-8") as f:
            f.write(dashboard_html)
        print("✓ Dashboard interativo criado")
        
        print("\nTodos os gráficos foram gerados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao gerar visualizações: {e}")

