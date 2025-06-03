"""
Fleet Copilot API - Dashboard Avançado
Sistema completo com filtros, múltiplas visualizações e exportação
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
        "message": "Fleet Copilot API - Dashboard Avançado",
        "status": "online",
        "version": "4.0.0",
        "features": [
            "Filtros dinâmicos",
            "Múltiplas visualizações",
            "Exportação Excel/PDF",
            "Gráficos interativos"
        ],
        "dashboard": "/api/copilot/enhanced-dashboard"
    })

@app.route("/health")
def health():
    """Health check para monitoramento"""
    return jsonify({
        "status": "healthy", 
        "version": "4.0.0",
        "features": "advanced"
    })

@app.route("/api/copilot/enhanced-dashboard")
def enhanced_dashboard():
    """Dashboard BI Avançado com todas as funcionalidades"""
    try:
        # Tentar carregar o dashboard avançado
        dashboard_path = os.path.join(os.path.dirname(__file__), "..", "dashboard_avancado.html")
        
        if os.path.exists(dashboard_path):
            with open(dashboard_path, "r", encoding="utf-8") as f:
                dashboard_content = f.read()
            return dashboard_content
        else:
            # Fallback para dashboard na raiz
            root_path = os.path.join(os.path.dirname(__file__), "..", "..", "dashboard_avancado.html")
            if os.path.exists(root_path):
                with open(root_path, "r", encoding="utf-8") as f:
                    dashboard_content = f.read()
                return dashboard_content
            else:
                # Fallback final
                return render_template_string(DASHBOARD_FALLBACK)
            
    except Exception as e:
        print(f"Erro ao carregar dashboard avançado: {e}")
        return render_template_string(DASHBOARD_FALLBACK)

# Dashboard fallback inline
DASHBOARD_FALLBACK = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fleet Copilot - BI Avançado</title>
    <style>
        body { 
            font-family: sans-serif; 
            background: linear-gradient(135deg, #2c3e50, #34495e); 
            color: #ecf0f1; 
            padding: 40px 20px; 
            text-align: center; 
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .container {
            max-width: 600px;
            background: rgba(52, 73, 94, 0.8);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 { 
            color: #1abc9c; 
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        .icon { 
            font-size: 4rem; 
            margin-bottom: 20px; 
        }
        .error { 
            background: linear-gradient(135deg, #e74c3c, #c0392b); 
            color: white; 
            padding: 20px; 
            border-radius: 10px; 
            margin-top: 20px;
        }
        .features {
            text-align: left;
            margin: 20px 0;
            padding: 20px;
            background: rgba(26, 188, 156, 0.1);
            border-radius: 10px;
            border-left: 4px solid #1abc9c;
        }
        .features h3 {
            color: #1abc9c;
            margin-bottom: 10px;
        }
        .features ul {
            list-style: none;
            padding: 0;
        }
        .features li {
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
        }
        .features li:before {
            content: "✅";
            position: absolute;
            left: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🚛</div>
        <h1>Fleet Copilot BI</h1>
        <div class="features">
            <h3>Dashboard Avançado</h3>
            <ul>
                <li>Filtros dinâmicos por data, garagem, filial</li>
                <li>Múltiplas visualizações em abas</li>
                <li>Exportação para Excel e PDF</li>
                <li>Gráficos interativos</li>
                <li>Dados reais da API Firebase</li>
            </ul>
        </div>
        <div class="error">
            <h2>⚠️ Dashboard Avançado Carregando...</h2>
            <p>Se esta mensagem persistir, verifique se o arquivo dashboard_avancado.html está na raiz do projeto.</p>
            <p><strong>Versão:</strong> 4.0.0 - Dashboard Avançado</p>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
