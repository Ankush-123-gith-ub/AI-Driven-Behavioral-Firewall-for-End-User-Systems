# intelligence/threat_intel.py

import json
import os
import requests


class ThreatIntel:

    def __init__(self):
        self.malicious_hashes = self._load_hashes()
        self.api_key = os.getenv("VT_API_KEY")  # safer than hardcoding

    # ---------------------------
    # Load local malicious hashes
    # ---------------------------
    def _load_hashes(self):
        path = os.path.join("storage", "malicious_hashes.json")
        try:
            with open(path, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()

    # ---------------------------
    # Main evaluation function
    # ---------------------------
    def evaluate(self, file_hash):

        # 1️⃣ LOCAL CHECK (FAST)
        if file_hash in self.malicious_hashes:
            print("[ThreatIntel] Local DB hit")
            return 1.0

        # 2️⃣ CLOUD CHECK (VirusTotal)
        vt_score = self._check_virustotal(file_hash)

        return vt_score

    # ---------------------------
    # VirusTotal lookup
    # ---------------------------
    def _check_virustotal(self, file_hash):

        # If API key not set → skip
        if not self.api_key:
            return 0.0

        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

        headers = {
            "x-apikey": self.api_key
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)

            # ✅ Success
            if response.status_code == 200:
                data = response.json()

                stats = data["data"]["attributes"]["last_analysis_stats"]

                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                total = sum(stats.values())

                if total == 0:
                    return 0.0

                score = (malicious + suspicious) / total

                print(f"[ThreatIntel] VT score: {round(score, 3)}")

                return min(score, 1.0)

            # ❌ Hash not found
            elif response.status_code == 404:
                print("[ThreatIntel] Not found in VirusTotal")
                return 0.0

            # ⚠️ Other API issues
            else:
                print("[ThreatIntel] API error:", response.status_code)
                return 0.0

        except Exception as e:
            print("[ThreatIntel] API failed:", e)
            return 0.0
