SUSPICIOUS_PATTERNS = [
    b"powershell",
    b"cmd.exe",
    b"CreateRemoteThread",
    b"VirtualAlloc",
    b"WriteProcessMemory",
    b"base64",
    b"eval(",
    b"socket",
    b"http://",
    b"https://"
]

def scan_signatures(file_path, chunk_size=8192):
    try:
        matches = []

        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                chunk_lower = chunk.lower()

                for pattern in SUSPICIOUS_PATTERNS:
                    if pattern.lower() in chunk_lower:
                        matches.append(pattern.decode(errors="ignore"))

        return matches

    except Exception:
        return []