import os
import time

def calculate_file_age(file_path):
    try:
        creation_time = os.path.getctime(file_path)
        return time.time() - creation_time
    except Exception:
        return None