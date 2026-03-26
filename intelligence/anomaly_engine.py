# intelligence/anomaly_engine.py

import os
import joblib


class AnomalyEngine:

    def __init__(self):
        self.model_path = os.path.join("analysis", "model_store", "anomaly_model.pkl")

    def evaluate(self, feature_vector):

        # If no trained model yet → no anomaly
        if not os.path.exists(self.model_path):
            return 0.0

        try:
            model = joblib.load(self.model_path)

            # IsolationForest decision_function:
            # Higher = normal, Lower = anomaly
            raw_score = model.decision_function([feature_vector])[0]

            # Convert to 0–1 anomaly scale
            anomaly_score = max(0.0, min(1.0, -raw_score))

            return anomaly_score

        except Exception:
            return 0.0