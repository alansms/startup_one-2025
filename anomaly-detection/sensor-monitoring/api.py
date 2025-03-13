import numpy as np
from scipy import stats as scipy_stats
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import logging
import os
import math

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class AnomalyDetector:
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            logger.error("Modelo não encontrado: %s", model_path)
            raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

        model = np.load(model_path)
        self.mu = model["mu"]
        self.cov = model["cov"]
        self.threshold = model["threshold"]
        self.last_predictions = [False, False, False]
        self.recent_distances = []  # Armazena distâncias recentes para estabilidade

        logger.info("Modelo carregado com threshold: %.2f", self.threshold)

    def preprocess(self, data, remove_dc=True):
        if remove_dc:
            data = data - np.mean(data, axis=0)
        return data

    def extract_features(self, sample):
        """Extrai um conjunto reduzido de características estatísticas do sample"""
        features = []
        for axis_idx in range(sample.shape[1]):
            axis_data = sample[:, axis_idx]

            # Características no domínio do tempo
            features.extend(
                [
                    np.std(axis_data),
                    scipy_stats.kurtosis(axis_data),
                    np.max(np.abs(axis_data)),
                    np.sqrt(np.mean(np.square(axis_data))),
                    np.max(axis_data) - np.min(axis_data),
                ]
            )

        return np.array(features)

    def mahalanobis_distance(self, x):
        if np.linalg.det(self.cov) == 0:
            logger.warning("Matriz de covariância singular, retornando distância infinita.")
            return np.inf

        x_mu = x - self.mu
        epsilon = 1e-6
        cov_reg = self.cov + epsilon * np.eye(self.cov.shape[0])

        try:
            scale = np.median(np.diag(cov_reg))
            cov_scaled = cov_reg / scale
            inv_covmat = np.linalg.inv(cov_scaled) / scale

            if x_mu.ndim == 1:
                mahal = np.sqrt(np.dot(np.dot(x_mu, inv_covmat), x_mu))
            else:
                mahal = np.sqrt(np.sum(np.dot(x_mu, inv_covmat) * x_mu, axis=1))
            return mahal
        except np.linalg.LinAlgError:
            return np.inf

    def calculate_confidence(self, distance):
        """Calcula confiança com bandas adaptativas de threshold"""
        self.recent_distances.append(distance)
        self.recent_distances = self.recent_distances[-20:]

        threshold_magnitude = np.log10(self.threshold)
        lower_band_factor = np.exp(-threshold_magnitude / 2)
        upper_band_factor = np.exp(threshold_magnitude / 2)

        lower_bound = self.threshold * lower_band_factor
        upper_bound = self.threshold * upper_band_factor

        if distance < lower_bound:
            base_confidence = 0.95
        elif distance > upper_bound:
            base_confidence = 0.90
        else:
            x = (distance - lower_bound) / (upper_bound - lower_bound)
            base_confidence = 0.9 / (1 + np.exp((x - 0.5) * 10))

        if len(self.recent_distances) > 5:
            recent_mean = np.mean(self.recent_distances[-5:])
            recent_std = np.std(self.recent_distances[-5:])

            trend_stability = np.exp(-abs(distance - recent_mean) / (recent_std + 1e-6))
            variation_coefficient = recent_std / (recent_mean + 1e-6)
            variation_stability = np.exp(-variation_coefficient)

            stability_factor = (trend_stability + variation_stability) / 2
            history_weight = min(len(self.recent_distances) / 20, 1.0)

            final_confidence = (
                base_confidence * (1 - history_weight)
                + (base_confidence + stability_factor) / 2 * history_weight
            )
        else:
            final_confidence = base_confidence

        return float(np.clip(final_confidence, 0.0, 1.0))

    def predict(self, data):
        processed_data = self.preprocess(data)
        features = self.extract_features(processed_data)
        distance = float(self.mahalanobis_distance(features))

        if math.isnan(distance):
            logger.error("Distância calculada é NaN, retornando erro.")
            return {"error": "Distância NaN detectada"}

        is_anomaly = distance > self.threshold
        self.last_predictions.pop(0)
        self.last_predictions.append(is_anomaly)
        stable_anomaly = sum(self.last_predictions) >= 2

        confidence = self.calculate_confidence(distance)

        feature_names = ["std", "kurtosis", "peak_amplitude", "rms", "peak_to_peak"]
        feature_stats = {}
        n_features_per_axis = len(feature_names)
        n_axes = len(features) // n_features_per_axis

        for axis_idx in range(n_axes):
            start_idx = axis_idx * n_features_per_axis
            axis_features = features[start_idx : start_idx + n_features_per_axis]
            feature_stats[f"axis_{axis_idx}"] = {
                name: float(value) for name, value in zip(feature_names, axis_features)
            }

        result = {
            "is_anomaly": bool(stable_anomaly),
            "confidence": float(confidence),
            "distance": float(distance),
            "threshold": float(self.threshold),
            "feature_values": feature_stats,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info("=" * 50)
        logger.info("Prediction Details:")
        logger.info("Timestamp: %s", result["timestamp"])
        logger.info("Is Anomaly: %s", result["is_anomaly"])
        logger.info("Confidence: %.3f", result["confidence"])
        logger.info("Distance: %.3f (threshold: %.3f)", result["distance"], result["threshold"])

        return result


class AccelerometerData(BaseModel):
    data: List[List[float]]
    sensor_id: str = "default"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    detector = AnomalyDetector("models/mahalanobis_model.npz")
except FileNotFoundError:
    detector = None  # Se o modelo não existir, a API não irá processar requests


def clean_json(data):
    return {k: (0 if math.isnan(v) else v) if isinstance(v, float) else v for k, v in data.items()}


@app.post("/predict")
async def predict_anomaly(data: AccelerometerData):
    if detector is None:
        return {"error": "Modelo não carregado", "timestamp": datetime.now().isoformat()}

    try:
        array_data = np.array(data.data)
        logger.info("Received data shape: %s from sensor %s", array_data.shape, data.sensor_id)

        result = detector.predict(array_data)
        result = clean_json(result)

        return result
    except Exception as e:
        logger.error("Erro durante a predição: %s", str(e))
        return {"error": str(e), "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)