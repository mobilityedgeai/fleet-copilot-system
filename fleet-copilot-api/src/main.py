import os
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Configurar caminho para templates (um nível acima de src/)
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

# Criar app Flask com template_folder correto
app = Flask(__name__, template_folder=template_dir)

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
    return {'status': 'ok', 'message': 'Fleet Copilot BI Server is running'}

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

# BI Viagens
@app.route('/api/copilot/bi-viagens')
def bi_viagens():
    """BI de Viagens"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_viagens.html', enterprise_id=enterprise_id)

# BI Manutenção
@app.route('/api/copilot/bi-manutencao')
def bi_manutencao():
    """BI de Manutenção"""
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('bi_manutencao.html', enterprise_id=enterprise_id)

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
            'status': 'coming_soon',
            'url': '/api/copilot/bi-checklist'
        },
        {
            'id': 'viagens',
            'name': 'Viagens',
            'description': 'Rotas e deslocamentos da frota',
            'status': 'coming_soon',
            'url': '/api/copilot/bi-viagens'
        },
        {
            'id': 'manutencao',
            'name': 'Manutenção',
            'description': 'Serviços e reparos da frota',
            'status': 'coming_soon',
            'url': '/api/copilot/bi-manutencao'
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
