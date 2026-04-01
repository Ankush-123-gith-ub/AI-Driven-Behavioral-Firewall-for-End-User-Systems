# sensors/persistence_layer/registry_monitor.py

import winreg


class RegistryMonitor:

    RUN_KEYS = [
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    ]

    def check(self):

        events = []

        for key_path in self.RUN_KEYS:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)

                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)

                        events.append({
                            "name": name,
                            "value": value,
                            "key": key_path
                        })

                        i += 1

                    except OSError:
                        break

            except Exception:
                continue

        return events