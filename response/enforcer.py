# response/enforcer.py

from response.process_killer import ProcessKiller
from response.file_quarantine import FileQuarantine
from response.alert_manager import AlertManager
from response.response_policy import ResponsePolicy
from response.event_logger import EventLogger

class Enforcer:

    def __init__(self):
        self.killer = ProcessKiller()
        self.quarantine = FileQuarantine()
        self.alert = AlertManager()
        self.policy = ResponsePolicy()
        self.logger = EventLogger()

    def enforce(self, event, decision):

        # 🔥 ALWAYS LOG (even ALLOW)
        self.logger.log(event, decision)

        actions = self.policy.decide_action(decision.verdict)

        if not actions:
            return

        print("\n========== RESPONSE ==========")

        if event.file_path.startswith("C:\\Windows"):
            print("[Response] Skipping system file")
            return

        if "kill" in actions:
            self.killer.kill(event.pid)

        if "quarantine" in actions:
            self.quarantine.quarantine(event.file_path)

        if "alert" in actions:
            self.alert.alert(f"{event.file_name} marked as {decision.verdict}")

        print("================================\n")