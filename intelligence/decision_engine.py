from analysis.features import build_feature_vector
from analysis.baseline import store_feature_vector, load_baseline_vectors
from intelligence.anomaly_model import AnomalyModel

class DecisionEngine:
    def __init__(self):
        self.known_bad_hashes = {"bad123", "evil456"}
        self.anomaly_model = AnomalyModel()

        # Train once if baseline exists
        baseline = load_baseline_vectors()
        if baseline:
            self.anomaly_model.train(baseline)

    def decide(self, file_event):
        reasons = []

        # Known malware
        if file_event.file_hash_sha256 in self.known_bad_hashes:
            return "MALICIOUS", ["Known malware hash"]

        vector = build_feature_vector(file_event)

        # Store SAFE behavior as baseline
        store_feature_vector(vector)

        anomaly_score = self.anomaly_model.score(vector)

        if anomaly_score > 0.7:
            return "SUSPICIOUS", [f"Anomalous behavior ({anomaly_score:.2f})"]

        if file_event.first_seen and not file_event.signed:
            return "SUSPICIOUS", ["First-time unsigned execution"]

        return "SAFE", ["Normal behavior"]
