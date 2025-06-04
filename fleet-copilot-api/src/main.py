#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fleet Copilot BI - Dashboard Corporativo com Filtros Corrigidos
Versão: 5.0.0
Data: 2025-06-04

Funcionalidades:
- Filtros dinâmicos baseados em dados reais da API Firebase BI
- Paginação completa sem limitação de registros
- Exportação Excel e PDF
- Interface corporativa profissional
- Suporte a múltiplos enterpriseId via URL
"""

import os
import logging
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do Flask
app = Flask(__name__)
CORS(app)

# Configurações
app.config['DEBUG'] = False
app.config['TESTING'] = False

def find_dashboard_file():
    """
    Busca o arquivo do dashboard em diferentes localizações possíveis
    """
    possible_paths = [
        'dashboard_filtros_corrigidos.html',
        './dashboard_filtros_corrigidos.html',
        '/app/dashboard_filtros_corrigidos.html',
        'dashboard_corporativo.html',
        './dashboard_corporativo.html',
        '/app/dashboard_corporativo.html',
        'dashboard_avancado.html',
        './dashboard_avancado.html',
        '/app/dashboard_avancado.html'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"✅ Dashboard encontrado em: {path}")
            return path
    
    logger.error("❌ Nenhum arquivo de dashboard encontrado")
    return None

def load_dashboard_content():
    """
    Carrega o conteúdo do dashboard HTML
    """
    dashboard_path = find_dashboard_file()
    
    if not dashboard_path:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fleet Copilot BI - Erro</title>
            <style>
                body { font-family: Arial, sans-serif; background: #14181B; color: white; padding: 50px; text-align: center; }
                .error { background: #ef4444; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }
            </style>
        </head>
        <body>
            <h1>Fleet Copilot BI</h1>
            <div class="error">
                <h2>❌ Erro: Dashboard não encontrado</h2>
                <p>O arquivo do dashboard não foi encontrado no servidor.</p>
                <p>Verifique se o arquivo dashboard_filtros_corrigidos.html está presente.</p>
            </div>
        </body>
        </html>
        """
    
    try:
        with open(dashboard_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logger.info(f"✅ Dashboard carregado com sucesso: {len(content)} caracteres")
            return content
    except Exception as e:
        logger.error(f"❌ Erro ao ler dashboard: {str(e)}")
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fleet Copilot BI - Erro</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #14181B; color: white; padding: 50px; text-align: center; }}
                .error {{ background: #ef4444; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }}
            </style>
        </head>
        <body>
            <h1>Fleet Copilot BI</h1>
            <div class="error">
                <h2>❌ Erro ao carregar dashboard</h2>
                <p>Erro: {str(e)}</p>
            </div>
        </body>
        </html>
        """

@app.route('/')
def index():
    """
    Página inicial - redireciona para o dashboard
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fleet Copilot BI</title>
        <meta http-equiv="refresh" content="0; url=/api/copilot/enhanced-dashboard">
        <style>
            body { font-family: Arial, sans-serif; background: #14181B; color: white; padding: 50px; text-align: center; }
            .loading { background: #3c444c; padding: 30px; border-radius: 12px; margin: 50px auto; max-width: 400px; }
        </style>
    </head>
    <body>
        <div class="loading">
            <h2>🚀 Fleet Copilot BI</h2>
            <p>Redirecionando para o dashboard...</p>
            <p><a href="/api/copilot/enhanced-dashboard" style="color: #14b8a6;">Clique aqui se não for redirecionado</a></p>
        </div>
    </body>
    </html>
    """

@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """
    Dashboard principal com filtros corrigidos e paginação
    """
    try:
        # Parâmetros da URL
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = request.args.get('days', '30')
        
        logger.info(f"📊 Dashboard solicitado - Enterprise: {enterprise_id}, Dias: {days}")
        
        # Carregar conteúdo do dashboard
        dashboard_content = load_dashboard_content()
        
        # Log de sucesso
        logger.info(f"✅ Dashboard servido com sucesso para enterprise: {enterprise_id}")
        
        return dashboard_content
        
    except Exception as e:
        logger.error(f"❌ Erro no dashboard: {str(e)}")
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fleet Copilot BI - Erro</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #14181B; color: white; padding: 50px; text-align: center; }}
                .error {{ background: #ef4444; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }}
            </style>
        </head>
        <body>
            <h1>Fleet Copilot BI</h1>
            <div class="error">
                <h2>❌ Erro interno do servidor</h2>
                <p>Erro: {str(e)}</p>
                <p>Tente novamente em alguns instantes.</p>
            </div>
        </body>
        </html>
        """

@app.route('/api/copilot/corporate-dashboard')
def corporate_dashboard():
    """
    Alias para o dashboard corporativo
    """
    return enhanced_dashboard()

@app.route('/health')
def health_check():
    """
    Endpoint de verificação de saúde
    """
    dashboard_path = find_dashboard_file()
    
    return jsonify({
        'status': 'healthy' if dashboard_path else 'error',
        'version': '5.0.0',
        'dashboard_found': dashboard_path is not None,
        'dashboard_path': dashboard_path,
        'features': [
            'Filtros dinâmicos baseados em dados reais',
            'Paginação completa sem limitações',
            'Exportação Excel e PDF',
            'Interface corporativa profissional',
            'Suporte a múltiplos enterpriseId'
        ]
    })

@app.route('/api/info')
def api_info():
    """
    Informações da API
    """
    return jsonify({
        'name': 'Fleet Copilot BI',
        'version': '5.0.0',
        'description': 'Dashboard corporativo com filtros corrigidos e paginação',
        'endpoints': {
            '/': 'Página inicial',
            '/api/copilot/enhanced-dashboard': 'Dashboard principal',
            '/api/copilot/corporate-dashboard': 'Dashboard corporativo (alias)',
            '/health': 'Verificação de saúde',
            '/api/info': 'Informações da API'
        },
        'parameters': {
            'enterpriseId': 'ID da empresa (opcional)',
            'days': 'Número de dias para análise (opcional, padrão: 30)'
        },
        'corrections_applied': [
            'Filtros baseados em campos reais da API Firebase BI',
            'Responsável: userRespForRegistration',
            'Placa: vehiclePlate (dropdown)',
            'Tipo de Ativo: planName',
            'Motorista: driverName',
            'Paginação: 50 itens por página',
            'Exportação: Excel e PDF funcionais'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    """
    Página de erro 404
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fleet Copilot BI - Página não encontrada</title>
        <style>
            body { font-family: Arial, sans-serif; background: #14181B; color: white; padding: 50px; text-align: center; }
            .error { background: #f59e0b; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }
            .links { margin-top: 30px; }
            .links a { color: #14b8a6; text-decoration: none; margin: 0 15px; }
        </style>
    </head>
    <body>
        <h1>Fleet Copilot BI</h1>
        <div class="error">
            <h2>⚠️ Página não encontrada</h2>
            <p>A página solicitada não existe.</p>
        </div>
        <div class="links">
            <a href="/">Página Inicial</a>
            <a href="/api/copilot/enhanced-dashboard">Dashboard</a>
            <a href="/health">Status</a>
        </div>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    """
    Página de erro 500
    """
    logger.error(f"❌ Erro interno: {str(error)}")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fleet Copilot BI - Erro interno</title>
        <style>
            body { font-family: Arial, sans-serif; background: #14181B; color: white; padding: 50px; text-align: center; }
            .error { background: #ef4444; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 600px; }
        </style>
    </head>
    <body>
        <h1>Fleet Copilot BI</h1>
        <div class="error">
            <h2>❌ Erro interno do servidor</h2>
            <p>Ocorreu um erro interno. Tente novamente em alguns instantes.</p>
        </div>
    </body>
    </html>
    """, 500

if __name__ == '__main__':
    # Configuração para desenvolvimento
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("🚀 Iniciando Fleet Copilot BI v5.0.0")
    logger.info(f"📊 Funcionalidades: Filtros corrigidos, Paginação, Exportação")
    logger.info(f"🌐 Porta: {port}")
    
    # Verificar se dashboard existe
    dashboard_path = find_dashboard_file()
    if dashboard_path:
        logger.info(f"✅ Dashboard pronto: {dashboard_path}")
    else:
        logger.warning("⚠️ Dashboard não encontrado - será exibida mensagem de erro")
    
    app.run(host='0.0.0.0', port=port, debug=False)
