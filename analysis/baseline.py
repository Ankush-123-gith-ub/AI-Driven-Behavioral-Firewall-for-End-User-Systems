# analysis/baseline.py

import csv
import os


BASELINE_PATH = "storage/baseline_features.csv"


def store_feature_vector(vector):
    os.makedirs("storage", exist_ok=True)
    with open(BASELINE_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(vector)


def load_baseline_vectors():
    if not os.path.exists(BASELINE_PATH):
        return []

    with open(BASELINE_PATH, "r") as f:
        reader = csv.reader(f)
        return [[float(x) for x in row] for row in reader]
