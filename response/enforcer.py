# response/enforcer.py

from response.process_killer import ProcessKiller
from response.file_quarantine import FileQuarantine
from response.alert_manager import AlertManager
from response.response_policy import ResponsePolicy


class Enforcer:

    def __init__(self):
        self.killer = ProcessKiller()
        self.quarantine = FileQuarantine()
        self.alert = AlertManager()
        self.policy = ResponsePolicy()

    def enforce(self, event, decision):

        actions = self.policy.decide_action(decision.verdict)

        if not actions:
            return

        print("\n========== RESPONSE ==========")

        if "kill" in actions:
            self.killer.kill(event.pid)

        if "quarantine" in actions:
            self.quarantine.quarantine(event.file_path)

        if "alert" in actions:
            self.alert.alert(f"{event.file_name} marked as {decision.verdict}")

        print("================================\n")