# monitor.py

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from sensors.file_layer.file_scanner import FileScanner
from intelligence.decision_engine import DecisionEngine
from response.enforcer import Enforcer
from sensors.process_layer.process_monitor import ProcessMonitor
from sensors.network_layer.network_monitor import NetworkMonitor
from intelligence.network_rules import network_score
from sensors.persistence_layer.registry_monitor import RegistryMonitor
from intelligence.persistence_rules import is_suspicious_registry

events_cache = {}
class FileMonitorHandler(FileSystemEventHandler):

    def __init__(self):
        self.scanner = FileScanner()
        self.engine = DecisionEngine()
        self.enforcer = Enforcer()
        self.seen_files = set()  # 🔥 avoid duplicate scans

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        # 🔥 Avoid duplicate scans
        if file_path in self.seen_files:
            return
        self.seen_files.add(file_path)

        # 🔥 Skip non-executable files
        if not file_path.lower().endswith((".exe", ".dll", ".bat", ".cmd", ".ps1")):
            return

        print(f"\n[Monitor] New file detected: {file_path}")

        # 🔥 Wait to ensure file is fully written
        time.sleep(0.5)

        self.process_file(file_path)

    def process_file(self, file_path):
        try:
            pid = 0

            event = self.scanner.scan(file_path, pid)

            if not event:
                print("[Monitor] Scan failed")
                return

            decision = self.engine.decide(event)

            event.pretty_print()
            decision.pretty_print()

            self.enforcer.enforce(event, decision)

        except Exception as e:
            print("[Monitor Error]", e)


def start_monitor(path_to_watch):

    event_handler = FileMonitorHandler()
    observer = Observer()
    registry_monitor = RegistryMonitor()
    network_monitor = NetworkMonitor()

    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    process_monitor = ProcessMonitor()
    seen_pids = set()  # avoid duplicate process scans

    print(f"[Monitor] Watching folder: {path_to_watch}")

    try:
        while True:
            time.sleep(0.5)


            # REGISTRY MONITORING

            entries = registry_monitor.check()

            for entry in entries:

                print(f"[Registry] {entry['name']} → {entry['value']}")

                if is_suspicious_registry(entry['value']):
                    print("[ALERT] Suspicious persistence detected!")

                    # ✅ APPLY TO ALL ACTIVE EVENTS
                    for event in events_cache.values():
                        event.registry_flag = True
                        print("[DEBUG] REGISTRY FLAG SET TRUE")
                        

            # NETWORK MONITORING (UPGRADED)

            connections = network_monitor.poll()

            for conn in connections:

                pid = conn['pid']
                ip = conn['remote_ip']
                port = conn['remote_port']

                print(f"[Network] PID {pid} → {ip}:{port}")

                try:
                    process_name = ""
                    if pid:
                        import psutil
                        process_name = psutil.Process(pid).name().lower()

                    score = network_score(ip, port, process_name)
                    print("[DEBUG] Network Score:", score)

                    # ✅ USE EXISTING EVENT
                    event = events_cache.get(pid)

                    if event:
                        event.network_score = score
                        print("[DEBUG] NETWORK ATTACHED:", score)

                except Exception as e:
                    print("[Network Error]", e)


            processes = process_monitor.poll()

            for proc in processes:

                if not proc['exe']:
                    continue

                pid = proc['pid']
                exe = proc['exe']
                cmdline = (proc.get("cmdline") or "").lower()

                print(f"[Process] New: {proc['name']} (PID: {pid})")

                try:
                    #  CREATE EVENT ONLY ONCE
                    event = event_handler.scanner.scan(exe, pid)

                    if not event:
                        continue

                    # ✅ STORE IN CACHE
                    events_cache[pid] = event

                    # ✅ ATTACH CMDLINE
                    event.process_cmdline = str(proc.get("cmdline", "")).lower()                    
                    print("[DEBUG] CMDLINE ATTACHED:", cmdline)

                    # 🔥 DECIDE
                    decision = event_handler.engine.decide(event)

                    event.pretty_print()
                    decision.pretty_print()

                    event_handler.enforcer.enforce(event, decision)

                except Exception as e:
                    print("[Process Error]", e)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    folder = r"C:\Users\Asus\Documents\WORK-SPACE\test_downloads"
    start_monitor(folder)