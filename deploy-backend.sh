#!/bin/bash

# Script de Deploy para Backend Flask no Render
# Copiloto Inteligente de Gestão de Frotas

echo "🚀 Preparando backend Flask para deploy no Render..."

# Navegar para o diretório do backend
cd fleet-copilot-api

echo "📦 Verificando requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt encontrado"
    echo "📋 Dependências:"
    head -10 requirements.txt
else
    echo "❌ Erro: requirements.txt não encontrado"
    exit 1
fi

echo "🔧 Verificando estrutura do projeto..."
if [ -f "src/main.py" ]; then
    echo "✅ main.py encontrado"
else
    echo "❌ Erro: src/main.py não encontrado"
    exit 1
fi

echo "🧪 Testando importações..."
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from src.routes.copilot import copilot_bp
    print('✅ Rotas do copiloto importadas com sucesso')
except ImportError as e:
    print(f'❌ Erro ao importar rotas: {e}')
    sys.exit(1)
"

echo "🌐 Configurando para produção..."
# Criar arquivo de configuração para produção
cat > src/config.py << EOF
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fleet-copilot-secret-key-prod'
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
EOF

echo "✅ Backend pronto para deploy no Render!"
echo "🔗 Endpoints disponíveis:"
echo "   - /api/copilot/health"
echo "   - /api/copilot/summary"
echo "   - /api/copilot/vehicles"
echo "   - /api/copilot/drivers"
echo "   - /api/copilot/insights"
echo "   - /api/copilot/question"
echo "   - /api/copilot/dashboard"

