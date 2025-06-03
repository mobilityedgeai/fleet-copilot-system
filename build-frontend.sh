#!/bin/bash

# Script de Build para Deploy no Render
# Copiloto Inteligente de Gestão de Frotas

echo "🚀 Iniciando build para deploy no Render..."

# Configurar variáveis de ambiente para produção
export NODE_ENV=production
export VITE_API_BASE_URL=https://fleet-copilot-api.onrender.com/api/copilot

# Navegar para o diretório do frontend
cd fleet-copilot-web

echo "📦 Instalando dependências do frontend..."
npm install

echo "🔧 Construindo aplicação React..."
npm run build

echo "✅ Build concluído com sucesso!"
echo "📁 Arquivos estáticos gerados em: fleet-copilot-web/dist"

# Verificar se o build foi bem-sucedido
if [ -d "dist" ]; then
    echo "✅ Diretório dist criado com sucesso"
    echo "📊 Tamanho dos arquivos:"
    du -sh dist/*
else
    echo "❌ Erro: Diretório dist não foi criado"
    exit 1
fi

echo "🎯 Frontend pronto para deploy no Render!"

