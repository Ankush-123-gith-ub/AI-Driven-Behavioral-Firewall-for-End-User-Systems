def is_suspicious_registry(value):

    value = value.lower()

    suspicious_keywords = [
        "powershell",
        "cmd.exe",
        "temp",
        "appdata",
        ".bat",
        ".ps1"
    ]

    return any(k in value for k in suspicious_keywords)