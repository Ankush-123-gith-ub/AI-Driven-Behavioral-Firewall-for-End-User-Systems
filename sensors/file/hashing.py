import hashlib
def calculate_sha256(file_path):
    """
    Calculate SHA-256 hash of a file.

    Args:
        file_path (str): Full path to file

    Returns:
        str: SHA-256 hex digest
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()
