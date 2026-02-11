# response/enforcer.py

import os
import signal


class Enforcer:
    def enforce(self, verdict, file_event, reasons):
        """
        Enforce action based on verdict.
        """

        print("\n=== ENFORCEMENT ACTION ===")
        print(f"Verdict: {verdict}")
        print(f"Process ID: {file_event.pid}")
        print(f"File: {file_event.file_path}")
        print("Reasons:")
        for r in reasons:
            print(f" - {r}")

        if verdict == "MALICIOUS":
            self._kill_process(file_event.pid)

        elif verdict == "SUSPICIOUS":
            self._restrict_network(file_event.pid)

        elif verdict == "SAFE":
            self._allow(file_event.pid)

    def _kill_process(self, pid):
        """
        Kill malicious process.
        """
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[ACTION] Process {pid} terminated.")
        except Exception as e:
            print(f"[ERROR] Failed to kill process {pid}: {e}")

    def _restrict_network(self, pid):
        """
        Placeholder for firewall restriction.
        """
        print(f"[ACTION] Network access restricted for process {pid} (placeholder).")

    def _allow(self, pid):
        """
        Allow execution (no action).
        """
        print(f"[ACTION] Process {pid} allowed.")
