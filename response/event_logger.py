import json
import os
from datetime import datetime

LOG_FILE = os.path.join("storage", "events_log.json")


class EventLogger:

    def log(self, event, decision):

        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "file": event.file_name,
            "pid": event.pid,
            "rule_score": round(decision.rule_score, 3),
            "anomaly_score": round(decision.anomaly_score, 3),
            "threat_score": round(decision.threat_score, 3),
            "final_score": round(decision.final_score, 3),
            "verdict": decision.verdict
        }

        try:
            if not os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w") as f:
                    json.dump([], f)

            with open(LOG_FILE, "r") as f:
                data = json.load(f)

            data.append(entry)

            with open(LOG_FILE, "w") as f:
                json.dump(data[-100:], f, indent=4)  # keep last 100 logs

        except Exception as e:
            print("[Logger Error]", e)