# intelligence/threat_intel.py

import json
import os


class ThreatIntel:

    def __init__(self):
        self.malicious_hashes = self._load_hashes()

    def _load_hashes(self):
        path = os.path.join("storage", "malicious_hashes.json")
        try:
            with open(path, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()

    def evaluate(self, file_hash):
        if file_hash in self.malicious_hashes:
            return 1.0
        return 0.0