from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = Path("sensor-monitoring/data")
NORMAL_PATH = DATA_PATH / "normal"
ANOMALY_PATH = DATA_PATH / "anomaly"
MODEL_PATH = Path("models/mahalanobis_model.npz")

def load_csv_files(path):
    files = list(path.glob("*.csv"))
    data = []
    for f in files:
        try:
            df = pd.read_csv(f)
            if {"temperatura", "vibracao", "energia"}.issubset(df.columns):
                # Extração de features simples: média de cada coluna
                features = df[["temperatura", "vibracao", "energia"]].mean().values
                data.append(features)
            else:
                print(f"⚠️  Ignorando arquivo inválido: {f}")
        except Exception as e:
            print(f"⚠️  Erro ao ler {f}: {e}")
    return np.array(data)

def train_model():
    print("🧠 Iniciando treino com CSVs no formato temperatura/vibracao/energia")

    normal_data = load_csv_files(NORMAL_PATH)
    anomaly_data = load_csv_files(ANOMALY_PATH)

    print(f"📁 Arquivos válidos: {len(normal_data)} normais, {len(anomaly_data)} anômalos")

    if len(normal_data) < 2 or len(anomaly_data) < 2:
        print("❌ Dados insuficientes ou com falhas.")
        return

    X = np.vstack([normal_data, anomaly_data])
    y = np.array([0] * len(normal_data) + [1] * len(anomaly_data))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    # Treina modelo baseado em Mahalanobis
    mu = np.mean(X_train[y_train == 0], axis=0)
    cov = np.cov(X_train[y_train == 0].T)
    inv_cov = np.linalg.inv(cov + 1e-6 * np.eye(cov.shape[0]))

    def mahalanobis(x): return np.sqrt(np.sum((x - mu) @ inv_cov * (x - mu), axis=1))

    dist_test = mahalanobis(X_test)
    threshold = np.percentile(dist_test[y_test == 0], 95)

    y_pred = (dist_test > threshold).astype(int)

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Anomaly"]))
    print(f"AUC Score: {roc_auc_score(y_test, dist_test):.4f}")

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal", "Anomaly"], yticklabels=["Normal", "Anomaly"])
    plt.title("Matriz de Confusão")
    plt.xlabel("Predito")
    plt.ylabel("Real")
    plt.show()

    MODEL_PATH.parent.mkdir(exist_ok=True)
    np.savez(MODEL_PATH, mu=mu, cov=cov, threshold=threshold, scaler=scaler)
    print(f"\n✅ Modelo salvo em {MODEL_PATH}")

if __name__ == "__main__":
    train_model()