# analysis/features.py

def build_feature_vector(file_event):
    """
    Convert event → numeric feature vector
    """

    return [
        1 if file_event.first_seen else 0,
        0 if file_event.signed else 1,
        file_event.file_size / 1024,  # KB
        file_event.timestamp % 86400  # seconds in day
    ]
