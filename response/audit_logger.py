# response/audit_logger.py

import os
import json
from datetime import datetime

class AuditLogger:

    def __init__(self):
        self.log_path = os.path.join("response", "audit_log.json")

    def log(self, data):

        os.makedirs("response", exist_ok=True)

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }

        try:
            # Load existing logs safely
            if os.path.exists(self.log_path):
                try:
                    with open(self.log_path, "r") as f:
                        logs = json.load(f)
                except:
                    logs = []
            else:
                logs = []

            logs.append(record)

            with open(self.log_path, "w") as f:
                json.dump(logs, f, indent=4)

        except Exception as e:
            print("Audit log error:", e)