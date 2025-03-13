import time
import json
import random
import requests
from datetime import datetime

# Configuração do servidor
SERVER_URL = "http://localhost:8007/predict"  # Altere a URL conforme necessário


def generate_sensor_data():
    """Gera dados simulados de sensores"""
    return {
        "data": [[
            round(random.uniform(20.0, 100.0), 2),  # Temperatura (°C)
            round(random.uniform(0.1, 5.0), 2),  # Vibração (g)
            round(random.uniform(50.0, 500.0), 2),  # Consumo de energia (W)
        ]],
        "sensor_id": "test_sensor"
    }


def send_data():
    """Envia dados para o servidor"""
    while True:
        sensor_data = generate_sensor_data()
        try:
            response = requests.post(SERVER_URL, json=sensor_data)
            print(f"Enviado: {json.dumps(sensor_data)} | Resposta: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar dados: {e}")

        time.sleep(2)  # Envia dados a cada 2 segundos


if __name__ == "__main__":
    print("Iniciando sensor simulado...")
    send_data()