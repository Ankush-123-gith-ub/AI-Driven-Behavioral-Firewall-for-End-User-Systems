# sensors/process_layer/process_monitor.py #

import psutil

class ProcessMonitor:

    def __init__(self):
        self.seen_pids = set()

    def poll(self):
        new_events = []

        for proc in psutil.process_iter(['pid', 'name', 'exe', 'ppid', 'cmdline']):
            try:
                if proc.info['pid'] not in self.seen_pids:

                    self.seen_pids.add(proc.info['pid'])

                    event = {
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "exe": proc.info['exe'],
                        "ppid": proc.info['ppid'],
                        "cmdline": " ".join(proc.info['cmdline']) if proc.info['cmdline'] else ""
                    }

                    new_events.append(event)

            except:
                continue

        return new_events

