"""
Copiloto Inteligente de Gestão de Frotas
Sistema de Exportação de Relatórios
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import logging
import base64
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from openpyxl.drawing.image import Image as OpenpyxlImage
import tempfile
import os

logger = logging.getLogger(__name__)

class FleetReportGenerator:
    """Gerador de relatórios para gestão de frotas"""
    
    def __init__(self, data_processor, visualization_engine, insights_engine):
        self.data_processor = data_processor
        self.visualization_engine = visualization_engine
        self.insights_engine = insights_engine
        
        # Estilos para Excel
        self.excel_styles = {
            'header': Font(bold=True, color='FFFFFF'),
            'header_fill': PatternFill(start_color='2E86AB', end_color='2E86AB', fill_type='solid'),
            'subheader': Font(bold=True, color='2E86AB'),
            'normal': Font(color='000000'),
            'warning': Font(color='C73E1D'),
            'success': Font(color='28A745'),
            'center': Alignment(horizontal='center', vertical='center'),
            'border': Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
        }
    
    def generate_comprehensive_report(self, enterprise_id: str = None, days: int = 30, 
                                    format_type: str = 'both') -> Dict[str, str]:
        """Gera relatório abrangente em PDF e/ou Excel"""
        logger.info(f"Gerando relatório abrangente para os últimos {days} dias")
        
        # Obter dados e análises
        analysis = self.insights_engine.generate_comprehensive_analysis(enterprise_id, days)
        summary = self.data_processor.get_checklist_summary(enterprise_id, days)
        vehicle_perf = self.data_processor.get_vehicle_performance(enterprise_id, days)
        driver_perf = self.data_processor.get_driver_performance(enterprise_id, days)
        
        # Gerar visualizações
        charts = self._generate_report_charts(enterprise_id, days)
        
        report_files = {}
        
        if format_type in ['pdf', 'both']:
            pdf_file = self._generate_pdf_report(analysis, summary, vehicle_perf, driver_perf, charts, days)
            report_files['pdf'] = pdf_file
        
        if format_type in ['excel', 'both']:
            excel_file = self._generate_excel_report(analysis, summary, vehicle_perf, driver_perf, charts, days)
            report_files['excel'] = excel_file
        
        return report_files
    
    def _generate_report_charts(self, enterprise_id: str, days: int) -> Dict[str, str]:
        """Gera gráficos para o relatório"""
        charts = {}
        
        try:
            # Gráfico de resumo
            charts['summary'] = self.visualization_engine.create_checklist_summary_chart(enterprise_id, days)
            
            # Gráfico de performance de veículos
            charts['vehicles'] = self.visualization_engine.create_vehicle_performance_chart(enterprise_id, days)
            
            # Gráfico de performance de motoristas
            charts['drivers'] = self.visualization_engine.create_driver_performance_chart(enterprise_id, days)
            
            # Gráfico de timeline
            charts['timeline'] = self.visualization_engine.create_timeline_chart(enterprise_id, days)
            
        except Exception as e:
            logger.warning(f"Erro ao gerar gráficos: {e}")
        
        return charts
    
    def _generate_pdf_report(self, analysis: Dict, summary: Dict, vehicle_perf: pd.DataFrame, 
                           driver_perf: pd.DataFrame, charts: Dict, days: int) -> str:
        """Gera relatório em PDF usando Markdown"""
        
        # Criar conteúdo Markdown
        markdown_content = self._create_markdown_report(analysis, summary, vehicle_perf, driver_perf, charts, days)
        
        # Salvar arquivo Markdown
        md_file = f"/home/ubuntu/fleet_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Converter para PDF usando utilitário
        pdf_file = md_file.replace('.md', '.pdf')
        
        try:
            import subprocess
            result = subprocess.run(['manus-md-to-pdf', md_file, pdf_file], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Relatório PDF gerado: {pdf_file}")
                return pdf_file
            else:
                logger.error(f"Erro ao converter para PDF: {result.stderr}")
                return md_file  # Retorna o Markdown se não conseguir converter
        except Exception as e:
            logger.error(f"Erro ao executar conversão para PDF: {e}")
            return md_file
    
    def _create_markdown_report(self, analysis: Dict, summary: Dict, vehicle_perf: pd.DataFrame, 
                              driver_perf: pd.DataFrame, charts: Dict, days: int) -> str:
        """Cria conteúdo do relatório em Markdown"""
        
        content = []
        
        # Cabeçalho
        content.append("# Relatório de Gestão de Frotas")
        content.append(f"**Período:** {days} dias")
        content.append(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
        content.append("---")
        content.append("")
        
        # Resumo Executivo
        content.append("## Resumo Executivo")
        content.append("")
        natural_summary = self.insights_engine.generate_natural_language_summary(analysis)
        content.append(natural_summary)
        content.append("")
        
        # Métricas Principais
        content.append("## Métricas Principais")
        content.append("")
        content.append("| Métrica | Valor |")
        content.append("|---------|-------|")
        content.append(f"| Total de Verificações | {summary['total']} |")
        content.append(f"| Taxa de Conformidade | {summary['compliance_rate']}% |")
        content.append(f"| Veículos Monitorados | {summary['vehicles']} |")
        content.append(f"| Motoristas Ativos | {summary['drivers']} |")
        content.append(f"| Verificações Conformes | {summary['compliant']} |")
        content.append(f"| Não Conformidades | {summary['non_compliant']} |")
        content.append("")
        
        # Insights Principais
        content.append("## Insights Principais")
        content.append("")
        
        # Agrupar insights por prioridade
        all_insights = []
        for category in ['summary', 'vehicle_insights', 'driver_insights', 'maintenance_insights', 'safety_insights']:
            if category in analysis and 'insights' in analysis[category]:
                all_insights.extend(analysis[category]['insights'])
        
        high_priority = [i for i in all_insights if i['priority'] == 'high']
        medium_priority = [i for i in all_insights if i['priority'] == 'medium']
        
        if high_priority:
            content.append("### 🔴 Alta Prioridade")
            for insight in high_priority:
                content.append(f"- **{insight['title']}**: {insight['description']}")
                content.append(f"  - *Recomendação*: {insight['recommendation']}")
            content.append("")
        
        if medium_priority:
            content.append("### 🟡 Média Prioridade")
            for insight in medium_priority:
                content.append(f"- **{insight['title']}**: {insight['description']}")
                content.append(f"  - *Recomendação*: {insight['recommendation']}")
            content.append("")
        
        # Performance de Veículos
        content.append("## Performance de Veículos")
        content.append("")
        
        if not vehicle_perf.empty:
            content.append("### Top 5 Veículos por Conformidade")
            content.append("")
            content.append("| Veículo | Taxa de Conformidade | Total de Verificações | Última Verificação |")
            content.append("|---------|---------------------|----------------------|-------------------|")
            
            for _, row in vehicle_perf.head(5).iterrows():
                last_check = pd.to_datetime(row['last_check']).strftime('%d/%m/%Y')
                content.append(f"| {row['vehicle_plate']} | {row['compliance_rate']}% | {row['total_checks']} | {last_check} |")
            content.append("")
        
        # Performance de Motoristas
        content.append("## Performance de Motoristas")
        content.append("")
        
        if not driver_perf.empty:
            content.append("### Top 5 Motoristas por Conformidade")
            content.append("")
            content.append("| Motorista | Taxa de Conformidade | Total de Verificações | Veículos Operados |")
            content.append("|-----------|---------------------|----------------------|------------------|")
            
            for _, row in driver_perf.head(5).iterrows():
                content.append(f"| {row['driver_name']} | {row['compliance_rate']}% | {row['total_checks']} | {row['vehicles_operated']} |")
            content.append("")
        
        # Alertas
        if analysis['alerts']:
            content.append("## Alertas Ativos")
            content.append("")
            for alert in analysis['alerts']:
                severity_icon = "🔴" if alert['severity'] == 'critical' else "🟡"
                content.append(f"{severity_icon} **{alert['title']}**: {alert['message']}")
            content.append("")
        
        # Recomendações
        if analysis['recommendations']:
            content.append("## Recomendações Estratégicas")
            content.append("")
            for i, rec in enumerate(analysis['recommendations'], 1):
                priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                content.append(f"{i}. {priority_icon} **{rec['title']}**")
                content.append(f"   - {rec['description']}")
                content.append(f"   - *Impacto Estimado*: {rec['estimated_impact']}")
                content.append(f"   - *Prazo*: {rec['timeline']}")
                content.append("")
        
        # Tendências
        if analysis['trends']['trends']:
            content.append("## Análise de Tendências")
            content.append("")
            for trend in analysis['trends']['trends']:
                direction_icon = "📈" if trend['direction'] == "melhorando" else "📉"
                content.append(f"{direction_icon} **{trend['metric']}**: {trend['description']}")
            content.append("")
        
        # Rodapé
        content.append("---")
        content.append("*Relatório gerado automaticamente pelo Copiloto Inteligente de Gestão de Frotas*")
        
        return "\n".join(content)
    
    def _generate_excel_report(self, analysis: Dict, summary: Dict, vehicle_perf: pd.DataFrame, 
                             driver_perf: pd.DataFrame, charts: Dict, days: int) -> str:
        """Gera relatório em Excel"""
        
        excel_file = f"/home/ubuntu/fleet_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            
            # Aba 1: Resumo
            self._create_summary_sheet(writer, analysis, summary, days)
            
            # Aba 2: Performance de Veículos
            if not vehicle_perf.empty:
                self._create_vehicles_sheet(writer, vehicle_perf)
            
            # Aba 3: Performance de Motoristas
            if not driver_perf.empty:
                self._create_drivers_sheet(writer, driver_perf)
            
            # Aba 4: Insights e Alertas
            self._create_insights_sheet(writer, analysis)
            
            # Aba 5: Dados Brutos
            self._create_raw_data_sheet(writer, analysis, summary, days)
        
        logger.info(f"Relatório Excel gerado: {excel_file}")
        return excel_file
    
    def _create_summary_sheet(self, writer, analysis: Dict, summary: Dict, days: int):
        """Cria aba de resumo no Excel"""
        
        # Criar DataFrame com métricas principais
        metrics_data = [
            ['Métrica', 'Valor'],
            ['Período Analisado', f'{days} dias'],
            ['Total de Verificações', summary['total']],
            ['Taxa de Conformidade', f"{summary['compliance_rate']}%"],
            ['Veículos Monitorados', summary['vehicles']],
            ['Motoristas Ativos', summary['drivers']],
            ['Verificações Conformes', summary['compliant']],
            ['Não Conformidades', summary['non_compliant']],
            ['Data de Geração', datetime.now().strftime('%d/%m/%Y %H:%M')]
        ]
        
        df_metrics = pd.DataFrame(metrics_data[1:], columns=metrics_data[0])
        df_metrics.to_excel(writer, sheet_name='Resumo', index=False, startrow=2)
        
        # Aplicar formatação
        worksheet = writer.sheets['Resumo']
        
        # Título
        worksheet['A1'] = 'Relatório de Gestão de Frotas'
        worksheet['A1'].font = Font(size=16, bold=True, color='2E86AB')
        
        # Formatar cabeçalhos
        for col in ['A', 'B']:
            cell = worksheet[f'{col}3']
            cell.font = self.excel_styles['header']
            cell.fill = self.excel_styles['header_fill']
            cell.alignment = self.excel_styles['center']
        
        # Ajustar largura das colunas
        worksheet.column_dimensions['A'].width = 25
        worksheet.column_dimensions['B'].width = 20
    
    def _create_vehicles_sheet(self, writer, vehicle_perf: pd.DataFrame):
        """Cria aba de performance de veículos"""
        
        # Renomear colunas para português e tratar timezone
        vehicle_perf_pt = vehicle_perf.copy()
        
        # Remover timezone se existir
        if 'last_check' in vehicle_perf_pt.columns:
            vehicle_perf_pt['last_check'] = pd.to_datetime(vehicle_perf_pt['last_check']).dt.tz_localize(None)
        
        vehicle_perf_pt.columns = [
            'Placa do Veículo', 'Total de Verificações', 'Taxa de Conformidade (%)',
            'Temperatura Média (°C)', 'Umidade Média (%)', 'Distância Total (m)',
            'Última Verificação'
        ]
        
        vehicle_perf_pt.to_excel(writer, sheet_name='Veículos', index=False, startrow=1)
        
        worksheet = writer.sheets['Veículos']
        
        # Título
        worksheet['A1'] = 'Performance de Veículos'
        worksheet['A1'].font = Font(size=14, bold=True, color='2E86AB')
        
        # Formatar cabeçalhos
        for col_num, col_letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 1):
            cell = worksheet[f'{col_letter}2']
            cell.font = self.excel_styles['header']
            cell.fill = self.excel_styles['header_fill']
            cell.alignment = self.excel_styles['center']
        
        # Ajustar largura das colunas
        column_widths = [15, 20, 25, 20, 18, 18, 20]
        for i, width in enumerate(column_widths):
            worksheet.column_dimensions[chr(65 + i)].width = width
    
    def _create_drivers_sheet(self, writer, driver_perf: pd.DataFrame):
        """Cria aba de performance de motoristas"""
        
        # Renomear colunas para português e tratar timezone
        driver_perf_pt = driver_perf.copy()
        
        # Remover timezone se existir
        if 'last_activity' in driver_perf_pt.columns:
            driver_perf_pt['last_activity'] = pd.to_datetime(driver_perf_pt['last_activity']).dt.tz_localize(None)
        
        driver_perf_pt.columns = [
            'Nome do Motorista', 'Total de Verificações', 'Taxa de Conformidade (%)',
            'Veículos Operados', 'Última Atividade'
        ]
        
        driver_perf_pt.to_excel(writer, sheet_name='Motoristas', index=False, startrow=1)
        
        worksheet = writer.sheets['Motoristas']
        
        # Título
        worksheet['A1'] = 'Performance de Motoristas'
        worksheet['A1'].font = Font(size=14, bold=True, color='2E86AB')
        
        # Formatar cabeçalhos
        for col_letter in ['A', 'B', 'C', 'D', 'E']:
            cell = worksheet[f'{col_letter}2']
            cell.font = self.excel_styles['header']
            cell.fill = self.excel_styles['header_fill']
            cell.alignment = self.excel_styles['center']
        
        # Ajustar largura das colunas
        column_widths = [25, 20, 25, 18, 20]
        for i, width in enumerate(column_widths):
            worksheet.column_dimensions[chr(65 + i)].width = width
    
    def _create_insights_sheet(self, writer, analysis: Dict):
        """Cria aba de insights e alertas"""
        
        insights_data = []
        
        # Coletar todos os insights
        all_insights = []
        for category in ['summary', 'vehicle_insights', 'driver_insights', 'maintenance_insights', 'safety_insights']:
            if category in analysis and 'insights' in analysis[category]:
                all_insights.extend(analysis[category]['insights'])
        
        # Preparar dados para Excel
        for insight in all_insights:
            priority_icon = "🔴" if insight['priority'] == 'high' else "🟡" if insight['priority'] == 'medium' else "🟢"
            impact_icon = "✅" if insight['impact'] == 'positive' else "❌" if insight['impact'] == 'negative' else "➖"
            
            insights_data.append([
                f"{priority_icon} {insight['priority'].upper()}",
                insight['category'].title(),
                insight['title'],
                insight['description'],
                insight['recommendation'],
                f"{impact_icon} {insight['impact'].title()}"
            ])
        
        if insights_data:
            df_insights = pd.DataFrame(insights_data, columns=[
                'Prioridade', 'Categoria', 'Título', 'Descrição', 'Recomendação', 'Impacto'
            ])
            df_insights.to_excel(writer, sheet_name='Insights', index=False, startrow=1)
            
            worksheet = writer.sheets['Insights']
            
            # Título
            worksheet['A1'] = 'Insights e Recomendações'
            worksheet['A1'].font = Font(size=14, bold=True, color='2E86AB')
            
            # Formatar cabeçalhos
            for col_letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                cell = worksheet[f'{col_letter}2']
                cell.font = self.excel_styles['header']
                cell.fill = self.excel_styles['header_fill']
                cell.alignment = self.excel_styles['center']
            
            # Ajustar largura das colunas
            column_widths = [15, 15, 25, 40, 40, 15]
            for i, width in enumerate(column_widths):
                worksheet.column_dimensions[chr(65 + i)].width = width
    
    def _create_raw_data_sheet(self, writer, analysis: Dict, summary: Dict, days: int):
        """Cria aba com dados brutos em JSON"""
        
        # Converter análise para formato tabular
        raw_data = [
            ['Seção', 'Dados JSON'],
            ['Resumo', json.dumps(summary, indent=2, ensure_ascii=False)],
            ['Análise Completa', json.dumps(analysis, indent=2, ensure_ascii=False, default=str)]
        ]
        
        df_raw = pd.DataFrame(raw_data[1:], columns=raw_data[0])
        df_raw.to_excel(writer, sheet_name='Dados Brutos', index=False, startrow=1)
        
        worksheet = writer.sheets['Dados Brutos']
        
        # Título
        worksheet['A1'] = 'Dados Brutos (JSON)'
        worksheet['A1'].font = Font(size=14, bold=True, color='2E86AB')
        
        # Ajustar largura das colunas
        worksheet.column_dimensions['A'].width = 20
        worksheet.column_dimensions['B'].width = 100
    
    def generate_quick_summary_excel(self, enterprise_id: str = None, days: int = 7) -> str:
        """Gera planilha Excel com resumo rápido"""
        
        summary = self.data_processor.get_checklist_summary(enterprise_id, days)
        vehicle_perf = self.data_processor.get_vehicle_performance(enterprise_id, days)
        
        excel_file = f"/home/ubuntu/fleet_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            
            # Resumo rápido
            summary_data = pd.DataFrame([
                ['Total de Verificações', summary['total']],
                ['Taxa de Conformidade', f"{summary['compliance_rate']}%"],
                ['Veículos', summary['vehicles']],
                ['Motoristas', summary['drivers']]
            ], columns=['Métrica', 'Valor'])
            
            summary_data.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Performance de veículos (se disponível)
            if not vehicle_perf.empty:
                vehicle_perf.to_excel(writer, sheet_name='Veículos', index=False)
        
        logger.info(f"Resumo Excel gerado: {excel_file}")
        return excel_file

if __name__ == "__main__":
    # Teste do sistema de relatórios
    from fleet_data_connector import FleetDataConnector, FleetDataProcessor
    from fleet_visualization import FleetVisualizationEngine
    from fleet_insights import FleetInsightsEngine
    
    connector = FleetDataConnector()
    processor = FleetDataProcessor(connector)
    viz_engine = FleetVisualizationEngine(processor)
    insights_engine = FleetInsightsEngine(processor)
    report_generator = FleetReportGenerator(processor, viz_engine, insights_engine)
    
    print("Gerando relatórios de teste...")
    
    try:
        # Gerar relatório completo
        reports = report_generator.generate_comprehensive_report(days=30, format_type='both')
        
        print("✓ Relatórios gerados:")
        for format_type, filepath in reports.items():
            print(f"  - {format_type.upper()}: {filepath}")
        
        # Gerar resumo rápido
        quick_excel = report_generator.generate_quick_summary_excel(days=7)
        print(f"✓ Resumo rápido: {quick_excel}")
        
    except Exception as e:
        print(f"Erro ao gerar relatórios: {e}")

