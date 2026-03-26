def assess_location_risk(file_path):
    try:
        path = file_path.lower()

        if "system32" in path or "program files" in path:
            return 0.0

        if "downloads" in path:
            return 0.3

        if "appdata" in path or "temp" in path:
            return 0.6

        return 0.1  # Unknown but not necessarily dangerous

    except Exception:
        return 0.0