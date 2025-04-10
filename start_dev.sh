#!/bin/bash

echo "🔁 Ativando ambiente virtual..."
source venv/bin/activate || { echo "❌ Ambiente virtual não encontrado. Crie com: python3 -m venv venv"; exit 1; }

echo "📦 Instalando dependências (se necessário)..."
pip install -r anomaly-detection/requirements.txt

echo "📊 Gerando dados simulados..."
python anomaly-detection/sensor-monitoring/data/generate_data.py || { echo "❌ Erro ao gerar dados"; exit 1; }

echo "🔍 Verificando arquivos..."
NORMAL_COUNT=$(find anomaly-detection/sensor-monitoring/data/normal -type f -name "*.csv" | wc -l)
ANOMALY_COUNT=$(find anomaly-detection/sensor-monitoring/data/anomaly -type f -name "*.csv" | wc -l)

echo "✅       $NORMAL_COUNT arquivos normais encontrados."
echo "✅       $ANOMALY_COUNT arquivos com anomalias encontrados."

if [[ $NORMAL_COUNT -eq 0 || $ANOMALY_COUNT -eq 0 ]]; then
  echo "❌ Nenhum dado encontrado para treinamento!"
  exit 1
fi

echo "🧠 Treinando modelo..."
python anomaly-detection/sensor-monitoring/training.py || { echo "❌ Falha no treinamento."; exit 1; }

echo "🚀 Tudo pronto! Modelo treinado com sucesso."