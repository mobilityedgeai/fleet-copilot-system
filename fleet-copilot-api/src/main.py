"""
Fleet Copilot API - Versão Reconstruída
Sistema robusto com dashboard reconstruído do zero
"""

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuração para produção
app.config["DEBUG"] = False

@app.route("/")
def home():
    """Página inicial da API"""
    return jsonify({
        "message": "Fleet Copilot API - Versão Reconstruída",
        "status": "online",
        "version": "3.0.0",
        "dashboard": "/api/copilot/enhanced-dashboard"
    })

@app.route("/health")
def health():
    """Health check para monitoramento"""
    return jsonify({"status": "healthy", "version": "3.0.0"})

@app.route("/api/copilot/enhanced-dashboard")
def enhanced_dashboard():
    """Dashboard BI reconstruído e robusto"""
    try:
        # Tentar carregar o dashboard reconstruído
        dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard_reconstruido.html")
        
        if os.path.exists(dashboard_path):
            with open(dashboard_path, "r", encoding="utf-8") as f:
                dashboard_content = f.read()
            return dashboard_content
        else:
            # Fallback 1: Tentar carregar o dashboard simplificado
            simplified_path = os.path.join(os.path.dirname(__file__), "dashboard_simplificado.html")
            if os.path.exists(simplified_path):
                with open(simplified_path, "r", encoding="utf-8") as f:
                    dashboard_content = f.read()
                return dashboard_content
            else:
                # Fallback 2: Dashboard inline básico
                return render_template_string(DASHBOARD_FALLBACK)
            
    except Exception as e:
        print(f"Erro ao carregar dashboard: {e}")
        return render_template_string(DASHBOARD_FALLBACK)

# Dashboard fallback inline (caso nenhum arquivo exista)
DASHBOARD_FALLBACK = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fleet Copilot - BI</title>
    <style>
        body { font-family: sans-serif; background: #2c3e50; color: #ecf0f1; padding: 20px; text-align: center; }
        h1 { color: #1abc9c; }
        .error { background: #e74c3c; color: white; padding: 15px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1><i class="fas fa-truck"></i> Fleet Copilot BI</h1>
    <div class="error">
        <h2>Erro Crítico</h2>
        <p>Não foi possível carregar o dashboard. Por favor, verifique os arquivos da aplicação.</p>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
