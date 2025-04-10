import os
import numpy as np
import pandas as pd

base_path = "sensor-monitoring/data"

normal_path = os.path.join(base_path, "normal")
anomaly_path = os.path.join(base_path, "anomaly")

os.makedirs(normal_path, exist_ok=True)
os.makedirs(anomaly_path, exist_ok=True)

# Gera arquivos CSV com dados simulados
def gerar_csv(tipo: str, path: str, n_arquivos: int = 10, linhas: int = 50):
    for i in range(n_arquivos):
        if tipo == "normal":
            temperatura = np.random.normal(loc=25, scale=1, size=linhas)
            vibracao = np.random.normal(loc=1.2, scale=0.2, size=linhas)
            energia = np.random.normal(loc=110, scale=5, size=linhas)
        elif tipo == "anomaly":
            temperatura = np.random.normal(loc=60, scale=5, size=linhas)
            vibracao = np.random.normal(loc=3.5, scale=1.0, size=linhas)
            energia = np.random.normal(loc=250, scale=30, size=linhas)
        else:
            continue

        df = pd.DataFrame({
            "temperatura": temperatura,
            "vibracao": vibracao,
            "energia": energia
        })

        nome_arquivo = f"{tipo}_{i+1}.csv"
        df.to_csv(os.path.join(path, nome_arquivo), index=False)

# Geração
gerar_csv("normal", normal_path)
gerar_csv("anomaly", anomaly_path)

print("✅ Arquivos gerados em:")
print(f"📂 {normal_path}")
print(f"📂 {anomaly_path}")