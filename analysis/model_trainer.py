from sklearn.ensemble import IsolationForest
import joblib
import os


class ModelTrainer:

    def __init__(self):
        self.model_path = os.path.join("analysis", "model_store", "anomaly_model.pkl")

    def train(self, feature_data):

        if not feature_data or len(feature_data) < 10:
            print("Not enough data to train model.")
            return

        model = IsolationForest(contamination=0.05)
        model.fit(feature_data)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(model, self.model_path)

        print("Model trained successfully.")