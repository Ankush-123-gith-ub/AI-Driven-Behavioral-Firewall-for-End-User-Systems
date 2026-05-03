#----------------------------------------- file -----------------------------------------------
# from sensors.file_layer.file_scanner import FileScanner
# from intelligence.decision_engine import DecisionEngine
# from analysis.feature_builder import FeatureBuilder
# from analysis.baseline_manager import BaselineManager
# from response.enforcer import Enforcer

# def main():
#     enforcer = Enforcer()
#     scanner = FileScanner()
#     engine = DecisionEngine()
#     feature_builder = FeatureBuilder()
#     baseline_manager = BaselineManager()

#     file_path = r"C:\Users\Asus\Documents\WORK-SPACE\test_downloads\writeups.pdf"
#     pid = 1234  # fake PID

#     event = scanner.scan(file_path, pid)

#     if not event:
#         print("File scan failed.")
#         return

#     # ---------------------------------------
#     # Analysis Layer: Feature Extraction
#     # ---------------------------------------
#     feature_vector = feature_builder.build(event)

#     # Save to baseline storage
#     baseline_manager.save(feature_vector)

#     # ---------------------------------------
#     # Intelligence Layer: Decision
#     # ---------------------------------------
#     decision = engine.decide(event)

#     # ---------------------------------------
#     # Output
#     # ---------------------------------------
#     event.pretty_print()
#     decision.pretty_print()
#     enforcer.enforce(event, decision)
    

# if __name__ == "__main__":
#     main()







# #------------------------------------------------------------------ process --------------------------------------------------------------
# import time
# import psutil

# from sensors.file_layer.file_scanner import FileScanner
# from intelligence.decision_engine import DecisionEngine
# from response.enforcer import Enforcer


# def main():

#     scanner = FileScanner()
#     engine = DecisionEngine()
#     enforcer = Enforcer()

#     seen_pids = set()

#     print(" Monitoring ONLY PowerShell / CMD...\n")

#     while True:

#         for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
#             try:
#                 name = (proc.info['name'] or "").lower()

#                 # FILTER ONLY IMPORTANT PROCESSES
#                 if name not in ["powershell.exe", "cmd.exe"]:
#                     continue

#                 pid = proc.info['pid']

#                 # avoid duplicate scan
#                 if pid in seen_pids:
#                     continue
#                 seen_pids.add(pid)

#                 exe = proc.info['exe']
#                 cmdline = " ".join(proc.info['cmdline'] or []).lower()

#                 print(f"\n[ DETECTED PROCESS] {name} (PID: {pid})")
#                 print("[CMDLINE]:", cmdline)

#                 if not exe:
#                     continue

#                 # Scan file
#                 event = scanner.scan(exe, pid)

#                 if not event:
#                     continue

#                 # Attach cmdline
#                 event.process_cmdline = cmdline

#                 #  STRONG DETECTION CONDITION
#                 if "powershell" in cmdline and "bypass" in cmdline:
#                     print(" Suspicious PowerShell attack detected!")

#                     event.network_score = 0.6
#                     event.registry_flag = True

#                 # Decision
#                 decision = engine.decide(event)

#                 event.pretty_print()
#                 decision.pretty_print()

#                 enforcer.enforce(event, decision)

#             except Exception:
#                 continue

#         time.sleep(0.5)


# if __name__ == "__main__":
#     main()

#powershell -ExecutionPolicy Bypass -Command "Start-Sleep -Seconds 10"



# --------------------------------------------------- network -----------------------------------------------

# import time
# import psutil

# def main():

#     seen_connections = set()

#     print("\n Network Monitoring Started...")
#     print(" Watching for PowerShell / CMD network activity...\n")

#     while True:

#         connections = psutil.net_connections(kind='inet')

#         for conn in connections:
#             try:
#                 pid = conn.pid

#                 if not pid or not conn.raddr:
#                     continue

#                 # Unique connection key
#                 key = (pid, conn.raddr.ip, conn.raddr.port)

#                 if key in seen_connections:
#                     continue
#                 seen_connections.add(key)

#                 # Get process info
#                 proc = psutil.Process(pid)
#                 name = proc.name().lower()

#                 #  FILTER ONLY POWERSHELL / CMD
#                 if name not in ["powershell.exe", "cmd.exe"]:
#                     continue

#                 ip = conn.raddr.ip
#                 port = conn.raddr.port

#                 print("\n [NETWORK DETECTED]")
#                 print(f" Process: {name} (PID: {pid})")
#                 print(f" Remote IP: {ip}")
#                 print(f" Port: {port}")

#                 print(" [ALERT] External connection detected!\n")

#             except Exception:
#                 continue

#         time.sleep(0.5)


# if __name__ == "__main__":
#     main()

################################################## persistence layer ###############################################


# import time
# import winreg

# #  Startup registry path
# REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


# def read_registry():
#     entries = {}

#     try:
#         key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH)

#         i = 0
#         while True:
#             try:
#                 name, value, _ = winreg.EnumValue(key, i)
#                 entries[name] = value
#                 i += 1
#             except OSError:
#                 break

#     except Exception as e:
#         print("Error reading registry:", e)

#     return entries


# def main():

#     print("\n Persistence Monitoring Started...")
#     print(" Watching for startup registry changes...\n")

#     old_entries = read_registry()

#     while True:
#         time.sleep(2)

#         new_entries = read_registry()

#         # Compare old vs new
#         for name, value in new_entries.items():
#             if name not in old_entries:
#                 print("\n [PERSISTENCE DETECTED]")
#                 print(f" Name: {name}")
#                 print(f" Value: {value}")

#                 print(" [ALERT] New startup entry added!\n")

#         old_entries = new_entries


# if __name__ == "__main__":
#     main()

#####################################################################################################################3
# import time
# import psutil
# import winreg
# import os

# from sensors.file_layer.file_scanner import FileScanner
# from intelligence.decision_engine import DecisionEngine
# from response.enforcer import Enforcer


# # -------------------------
# # CONFIG
# # -------------------------
# WATCH_FOLDER = r"C:\Users\Asus\Documents\WORK-SPACE\test_downloads"
# REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


# # -------------------------
# # HELPERS
# # -------------------------
# def read_registry():
#     entries = {}
#     try:
#         key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH)
#         i = 0
#         while True:
#             try:
#                 name, value, _ = winreg.EnumValue(key, i)
#                 entries[name] = value
#                 i += 1
#             except OSError:
#                 break
#     except:
#         pass
#     return entries


# def print_file_block(file_path):
#     print("\n===== FILE THREAT DETECTED =====")
#     print("Reason: Malicious or suspicious file detected")
#     print(f"File: {file_path}")
#     print("Action: File blocked / quarantined")
#     print("================================\n")


# def print_process_block():
#     print("\n===== PROCESS THREAT DETECTED =====")
#     print("Reason: Suspicious command-line execution")
#     print("Indicator: PowerShell with ExecutionPolicy Bypass")
#     print("Action: Process blocked and terminated")
#     print("===================================\n")


# def print_network_block(ip, port):
#     print("\n===== NETWORK THREAT DETECTED =====")
#     print("Reason: Suspicious outbound connection")
#     print(f"Destination: {ip}:{port}")
#     print("Action: Connection flagged and process blocked")
#     print("===================================\n")


# def print_persistence_block(name, value):
#     print("\n===== PERSISTENCE THREAT DETECTED =====")
#     print("Reason: Unauthorized startup entry detected")
#     print(f"Registry Entry: {name}")
#     print(f"Value: {value}")
#     print("Action: Persistence attempt blocked")
#     print("=======================================\n")


# # -------------------------
# # MAIN
# # -------------------------
# def main():

#     scanner = FileScanner()
#     engine = DecisionEngine()
#     enforcer = Enforcer()

#     seen_files = set()
#     seen_pids = set()
#     seen_connections = set()
#     old_registry = read_registry()

#     print("\nAI Behavioral Firewall Demo Started")
#     print("Monitoring File, Process, Network, and Persistence Layers\n")

#     while True:

#         print("Scanning system activity...\n")

#         # -------------------------
#         # FILE LAYER
#         # -------------------------
#         for file_name in os.listdir(WATCH_FOLDER):
#             file_path = os.path.join(WATCH_FOLDER, file_name)

#             if file_path in seen_files:
#                 continue
#             seen_files.add(file_path)

#             print(f"File Detected: {file_path}")

#             event = scanner.scan(file_path, 0)
#             if not event:
#                 continue

#             decision = engine.decide(event)

#             # FILE BLOCK
#             if decision.verdict == "BLOCK":
#                 print_file_block(file_path)
#                 enforcer.enforce(event, decision)

#         # -------------------------
#         # PROCESS + NETWORK
#         # -------------------------
#         for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
#             try:
#                 name = (proc.info['name'] or "").lower()

#                 if name not in ["powershell.exe", "cmd.exe"]:
#                     continue

#                 pid = proc.info['pid']

#                 if pid in seen_pids:
#                     continue
#                 seen_pids.add(pid)

#                 exe = proc.info['exe']
#                 cmdline = " ".join(proc.info['cmdline'] or []).lower()

#                 print(f"Process Detected: {name} (PID: {pid})")
#                 print("Command Line:", cmdline)

#                 if not exe:
#                     continue

#                 event = scanner.scan(exe, pid)
#                 if not event:
#                     continue

#                 event.process_cmdline = cmdline

#                 # -------------------------
#                 # PROCESS BLOCK
#                 # -------------------------
#                 if "powershell" in cmdline and "bypass" in cmdline:
#                     print_process_block()

#                     decision = engine.decide(event)
#                     decision.verdict = "BLOCK"

#                     enforcer.enforce(event, decision)
#                     continue

#                 # -------------------------
#                 # NETWORK BLOCK
#                 # -------------------------
#                 time.sleep(1)

#                 for conn in psutil.net_connections(kind='inet'):
#                     if conn.pid == pid and conn.raddr:

#                         key = (pid, conn.raddr.ip, conn.raddr.port)
#                         if key in seen_connections:
#                             continue
#                         seen_connections.add(key)

#                         ip = conn.raddr.ip
#                         port = conn.raddr.port

#                         print(f"Network Detected: {ip}:{port}")

#                         event.network_score = 0.9

#                         print_network_block(ip, port)

#                         decision = engine.decide(event)
#                         decision.verdict = "BLOCK"

#                         enforcer.enforce(event, decision)

#             except:
#                 continue

#         # -------------------------
#         # PERSISTENCE
#         # -------------------------
#         new_registry = read_registry()

#         for name, value in new_registry.items():
#             if name not in old_registry:

#                 print("New registry entry detected")

#                 print_persistence_block(name, value)

#                 event = scanner.scan(value, 0)
#                 if event:
#                     event.registry_flag = True

#                     decision = engine.decide(event)
#                     decision.verdict = "BLOCK"

#                     enforcer.enforce(event, decision)

#         old_registry = new_registry

#         time.sleep(1)


# if __name__ == "__main__":
#     main()