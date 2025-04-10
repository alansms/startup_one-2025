#!/bin/bash

echo "🔁 Ativando ambiente virtual..."
source ../venv/bin/activate

echo "⚙️ Gerando dados simulados..."
python3 sensor-monitoring/data/generate_data.py