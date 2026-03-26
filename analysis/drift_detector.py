# analysis/drift_detector.py

class DriftDetector:

    def detect(self, historical_avg, current_value, threshold=0.5):
        return abs(current_value - historical_avg) > threshold