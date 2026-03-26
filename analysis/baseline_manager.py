# analysis/baseline_manager.py

import csv
import os

class BaselineManager:

    def __init__(self):
        self.path = os.path.join("storage", "baseline_features.csv")

    def save(self, feature_vector):
        os.makedirs("storage", exist_ok=True)
        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(feature_vector)

    def load(self):
        data = []
        try:
            with open(self.path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append([float(x) for x in row])
        except:
            pass
        return data