import socket

SUSPICIOUS_PORTS = [4444, 1337, 6666, 8080]
HIGH_RISK_IP_PREFIXES = ["185.", "45.", "103."]


def resolve_domain(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "unknown"


def network_score(ip, port, process_name):

    score = 0.0

    # 🔥 Suspicious ports
    if port in SUSPICIOUS_PORTS:
        score += 0.4

    # 🔥 Suspicious IP ranges
    if any(ip.startswith(prefix) for prefix in HIGH_RISK_IP_PREFIXES):
        score += 0.4

    # 🔥 Unknown domain
    domain = resolve_domain(ip)
    if domain == "unknown":
        score += 0.2

    # 🔥 Process-based suspicion
    if process_name in ["powershell.exe", "cmd.exe"]:
        score += 0.5

    return min(score, 1.0)