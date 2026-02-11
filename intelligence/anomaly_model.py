# intelligence/anomaly_model.py

import pickle
from sklearn.ensemble import IsolationForest


class AnomalyModel:
    def __init__(self, model_path="storage/model.pkl"):
        self.model_path = model_path
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )
        self.trained = False
        self._load()

    def _load(self):
        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
                self.trained = True
        except FileNotFoundError:
            pass  # first run

    def train(self, feature_vectors):
        self.model.fit(feature_vectors)
        self.trained = True
        self._save()

    def _save(self):
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)

    def score(self, feature_vector):
        if not self.trained:
            return 0.0
        score = -self.model.decision_function([feature_vector])[0]
        return min(max(score, 0.0), 1.0)
 