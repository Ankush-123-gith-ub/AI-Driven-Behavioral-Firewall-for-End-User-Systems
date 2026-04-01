# sensors/network_layer/network_monitor.py

import psutil


class NetworkMonitor:

    def __init__(self):
        self.seen_connections = set()

    def poll(self):
        events = []

        connections = psutil.net_connections(kind='inet')

        for conn in connections:
            try:
                if not conn.raddr:
                    continue

                key = (conn.pid, conn.raddr.ip, conn.raddr.port)

                if key in self.seen_connections:
                    continue

                self.seen_connections.add(key)

                event = {
                    "pid": conn.pid,
                    "remote_ip": conn.raddr.ip,
                    "remote_port": conn.raddr.port,
                    "status": conn.status
                }

                events.append(event)

            except:
                continue

        return events