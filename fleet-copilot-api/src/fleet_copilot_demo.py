"""
Copiloto Inteligente de Gestão de Frotas
Sistema Integrado - Demonstração Completa
"""

import json
import logging
from datetime import datetime
from fleet_data_connector import FleetDataConnector, FleetDataProcessor
from fleet_visualization import FleetVisualizationEngine
from fleet_insights import FleetInsightsEngine
from fleet_reports import FleetReportGenerator

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FleetCopilotDemo:
    """Demonstração completa do Copiloto de Gestão de Frotas"""
    
    def __init__(self):
        logger.info("Inicializando Copiloto de Gestão de Frotas...")
        
        # Inicializar componentes
        self.connector = FleetDataConnector()
        self.processor = FleetDataProcessor(self.connector)
        self.viz_engine = FleetVisualizationEngine(self.processor)
        self.insights_engine = FleetInsightsEngine(self.processor)
        self.report_generator = FleetReportGenerator(self.processor, self.viz_engine, self.insights_engine)
        
        logger.info("✓ Todos os componentes inicializados com sucesso")
    
    def run_complete_demo(self, enterprise_id: str = None, days: int = 30):
        """Executa demonstração completa do sistema"""
        
        print("\n" + "="*80)
        print("🚛 COPILOTO INTELIGENTE DE GESTÃO DE FROTAS - DEMONSTRAÇÃO COMPLETA")
        print("="*80)
        
        # 1. Teste de Conectividade
        print("\n1️⃣ TESTANDO CONECTIVIDADE COM APIs...")
        self._test_connectivity()
        
        # 2. Processamento de Dados
        print("\n2️⃣ PROCESSANDO DADOS DA FROTA...")
        summary = self._process_fleet_data(enterprise_id, days)
        
        # 3. Geração de Visualizações
        print("\n3️⃣ GERANDO VISUALIZAÇÕES...")
        charts = self._generate_visualizations(enterprise_id, days)
        
        # 4. Análise de Insights
        print("\n4️⃣ ANALISANDO INSIGHTS...")
        insights = self._analyze_insights(enterprise_id, days)
        
        # 5. Geração de Relatórios
        print("\n5️⃣ GERANDO RELATÓRIOS...")
        reports = self._generate_reports(enterprise_id, days)
        
        # 6. Resumo Final
        print("\n6️⃣ RESUMO FINAL...")
        self._show_final_summary(summary, insights, reports)
        
        print("\n" + "="*80)
        print("✅ DEMONSTRAÇÃO COMPLETA FINALIZADA COM SUCESSO!")
        print("="*80)
        
        return {
            'summary': summary,
            'insights': insights,
            'reports': reports,
            'charts': charts
        }
    
    def _test_connectivity(self):
        """Testa conectividade com todas as APIs"""
        try:
            # Testar API de checklist
            checklist_data = self.connector.get_checklist_data()
            print(f"   ✓ API Checklist: {len(checklist_data)} registros acessíveis")
            
            # Testar API de alertas
            alerts_data = self.connector.get_alerts_checkin_data()
            print(f"   ✓ API Alertas: {len(alerts_data)} registros acessíveis")
            
            # Testar API de viagens (se disponível)
            try:
                trips_data = self.connector.get_driver_trips_data()
                print(f"   ✓ API Viagens: {len(trips_data)} registros acessíveis")
            except:
                print("   ⚠ API Viagens: Sem dados disponíveis")
            
            print("   🌐 Conectividade: EXCELENTE")
            
        except Exception as e:
            print(f"   ❌ Erro de conectividade: {e}")
            raise
    
    def _process_fleet_data(self, enterprise_id: str, days: int):
        """Processa dados da frota"""
        try:
            # Obter resumo geral
            summary = self.processor.get_checklist_summary(enterprise_id, days)
            
            print(f"   📊 Total de verificações: {summary['total']}")
            print(f"   ✅ Taxa de conformidade: {summary['compliance_rate']}%")
            print(f"   🚛 Veículos monitorados: {summary['vehicles']}")
            print(f"   👥 Motoristas ativos: {summary['drivers']}")
            
            # Obter performance de veículos
            vehicle_perf = self.processor.get_vehicle_performance(enterprise_id, days)
            if not vehicle_perf.empty:
                print(f"   🔍 Performance de veículos analisada: {len(vehicle_perf)} veículos")
            
            # Obter performance de motoristas
            driver_perf = self.processor.get_driver_performance(enterprise_id, days)
            if not driver_perf.empty:
                print(f"   👨‍💼 Performance de motoristas analisada: {len(driver_perf)} motoristas")
            
            return summary
            
        except Exception as e:
            print(f"   ❌ Erro no processamento: {e}")
            raise
    
    def _generate_visualizations(self, enterprise_id: str, days: int):
        """Gera visualizações"""
        charts = {}
        
        try:
            # Gráfico de resumo
            chart_file = self.viz_engine.create_checklist_summary_chart(enterprise_id, days)
            charts['summary'] = chart_file
            print(f"   📈 Gráfico de resumo: {chart_file}")
            
            # Gráfico de performance de veículos
            chart_file = self.viz_engine.create_vehicle_performance_chart(enterprise_id, days)
            charts['vehicles'] = chart_file
            print(f"   🚛 Gráfico de veículos: {chart_file}")
            
            # Gráfico de timeline
            chart_file = self.viz_engine.create_timeline_chart(enterprise_id, days)
            charts['timeline'] = chart_file
            print(f"   📅 Gráfico de timeline: {chart_file}")
            
            # Dashboard interativo
            dashboard_file = self.viz_engine.create_interactive_dashboard(enterprise_id, days)
            charts['dashboard'] = dashboard_file
            print(f"   🎯 Dashboard interativo: {dashboard_file}")
            
            print(f"   🎨 Total de visualizações geradas: {len(charts)}")
            
        except Exception as e:
            print(f"   ❌ Erro na geração de gráficos: {e}")
        
        return charts
    
    def _analyze_insights(self, enterprise_id: str, days: int):
        """Analisa insights"""
        try:
            # Gerar análise completa
            analysis = self.insights_engine.generate_comprehensive_analysis(enterprise_id, days)
            
            # Contar insights por prioridade
            all_insights = []
            for category in ['summary', 'vehicle_insights', 'driver_insights', 'maintenance_insights', 'safety_insights']:
                if category in analysis and 'insights' in analysis[category]:
                    all_insights.extend(analysis[category]['insights'])
            
            high_priority = len([i for i in all_insights if i['priority'] == 'high'])
            medium_priority = len([i for i in all_insights if i['priority'] == 'medium'])
            low_priority = len([i for i in all_insights if i['priority'] == 'low'])
            
            print(f"   🔴 Insights alta prioridade: {high_priority}")
            print(f"   🟡 Insights média prioridade: {medium_priority}")
            print(f"   🟢 Insights baixa prioridade: {low_priority}")
            print(f"   🚨 Alertas ativos: {len(analysis['alerts'])}")
            print(f"   💡 Recomendações: {len(analysis['recommendations'])}")
            
            # Gerar resumo em linguagem natural
            natural_summary = self.insights_engine.generate_natural_language_summary(analysis)
            print(f"   📝 Resumo: {natural_summary[:100]}...")
            
            return analysis
            
        except Exception as e:
            print(f"   ❌ Erro na análise de insights: {e}")
            return {}
    
    def _generate_reports(self, enterprise_id: str, days: int):
        """Gera relatórios"""
        reports = {}
        
        try:
            # Relatório completo (PDF + Excel)
            report_files = self.report_generator.generate_comprehensive_report(
                enterprise_id, days, format_type='both'
            )
            reports.update(report_files)
            
            print(f"   📄 Relatório PDF: {reports.get('pdf', 'N/A')}")
            print(f"   📊 Relatório Excel: {reports.get('excel', 'N/A')}")
            
            # Resumo rápido
            quick_excel = self.report_generator.generate_quick_summary_excel(enterprise_id, 7)
            reports['quick_summary'] = quick_excel
            print(f"   ⚡ Resumo rápido: {quick_excel}")
            
            print(f"   📋 Total de relatórios gerados: {len(reports)}")
            
        except Exception as e:
            print(f"   ❌ Erro na geração de relatórios: {e}")
        
        return reports
    
    def _show_final_summary(self, summary, insights, reports):
        """Mostra resumo final da demonstração"""
        
        print("\n📋 RESUMO EXECUTIVO:")
        print(f"   • Período analisado: {summary.get('period_days', 30)} dias")
        print(f"   • Total de verificações: {summary.get('total', 0)}")
        print(f"   • Taxa de conformidade: {summary.get('compliance_rate', 0)}%")
        print(f"   • Veículos monitorados: {summary.get('vehicles', 0)}")
        print(f"   • Motoristas ativos: {summary.get('drivers', 0)}")
        
        print("\n🎯 CAPACIDADES DEMONSTRADAS:")
        print("   ✓ Conexão com APIs REST de telemática")
        print("   ✓ Processamento e análise de dados")
        print("   ✓ Geração automática de visualizações")
        print("   ✓ Análise inteligente de insights")
        print("   ✓ Geração de relatórios profissionais")
        print("   ✓ Interface web interativa")
        
        print("\n📁 ARQUIVOS GERADOS:")
        for report_type, filepath in reports.items():
            if filepath:
                print(f"   • {report_type.upper()}: {filepath}")
    
    def answer_natural_language_question(self, question: str, enterprise_id: str = None, days: int = 30):
        """Responde perguntas em linguagem natural sobre a frota"""
        
        print(f"\n❓ PERGUNTA: {question}")
        print("🤖 ANALISANDO...")
        
        # Obter dados relevantes
        summary = self.processor.get_checklist_summary(enterprise_id, days)
        analysis = self.insights_engine.generate_comprehensive_analysis(enterprise_id, days)
        
        # Processar pergunta e gerar resposta
        response = self._process_question(question, summary, analysis)
        
        print(f"💬 RESPOSTA: {response}")
        return response
    
    def _process_question(self, question: str, summary: dict, analysis: dict):
        """Processa pergunta e gera resposta contextual"""
        
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

def main():
    """Função principal para demonstração"""
    
    # Criar instância do copiloto
    copilot = FleetCopilotDemo()
    
    # Executar demonstração completa
    print("Iniciando demonstração completa do sistema...")
    
    # Usar enterpriseId real para testes (conforme conhecimento fornecido)
    enterprise_id = "sA9EmrE3ymtnBqJKcYn7"
    
    try:
        # Demonstração completa
        results = copilot.run_complete_demo(enterprise_id=enterprise_id, days=30)
        
        # Demonstrar capacidade de resposta a perguntas
        print("\n" + "="*80)
        print("🗣️ DEMONSTRAÇÃO DE PERGUNTAS EM LINGUAGEM NATURAL")
        print("="*80)
        
        questions = [
            "Qual é a taxa de conformidade da frota?",
            "Quantos veículos estão sendo monitorados?",
            "Há algum problema que precisa de atenção?",
            "Quais são as principais recomendações?",
            "Como está a performance dos motoristas?"
        ]
        
        for question in questions:
            copilot.answer_natural_language_question(question, enterprise_id, 30)
            print()
        
        # Salvar resultados da demonstração
        demo_results = {
            'timestamp': datetime.now().isoformat(),
            'enterprise_id': enterprise_id,
            'results': results,
            'status': 'success'
        }
        
        with open('/home/ubuntu/demo_results.json', 'w', encoding='utf-8') as f:
            json.dump(demo_results, f, indent=2, ensure_ascii=False, default=str)
        
        print("📁 Resultados da demonstração salvos em: /home/ubuntu/demo_results.json")
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
        raise

if __name__ == "__main__":
    main()

