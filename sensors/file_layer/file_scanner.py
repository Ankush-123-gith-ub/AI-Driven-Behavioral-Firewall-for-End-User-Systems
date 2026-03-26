import os
import json

from sensors.file_layer.file_event import FileExecutionEvent
from sensors.file_layer.analyzers.hashing import calculate_sha256
from sensors.file_layer.analyzers.location import assess_location_risk
from sensors.file_layer.analyzers.file_age import calculate_file_age
from sensors.file_layer.analyzers.entropy import calculate_entropy
from sensors.file_layer.analyzers.signature import scan_signatures


class FileScanner:

    def __init__(self):
        self.seen_hashes = self._load_seen_hashes()

    # -------------------------------
    # Storage Handling
    # -------------------------------

    def _get_seen_hashes_path(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "storage", "seen_hashes.json")

    def _load_seen_hashes(self):
        path = self._get_seen_hashes_path()
        try:
            with open(path, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()

    def _save_seen_hashes(self):
        path = self._get_seen_hashes_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(list(self.seen_hashes), f)

    # -------------------------------
    # Main Scan Function
    # -------------------------------

    def scan(self, file_path, pid):

        if not os.path.exists(file_path):
            return None

        event = FileExecutionEvent()

        try:
            event.pid = pid
            event.file_path = file_path
            event.file_name = os.path.basename(file_path)
            event.file_size = os.path.getsize(file_path)

            # Location signal
            event.location_risk = assess_location_risk(file_path)

            # Temporal signal
            event.file_age_seconds = calculate_file_age(file_path)

            # Identity signal
            event.file_hash = calculate_sha256(file_path)

            # Novelty signal
            if event.file_hash not in self.seen_hashes:
                event.first_seen = True
                self.seen_hashes.add(event.file_hash)
                self._save_seen_hashes()
            else:
                event.first_seen = False

            # Content signal
            event.entropy = calculate_entropy(file_path)

            # Pattern signal
            event.signature_matches = scan_signatures(file_path)

            return event

        except Exception as e:
            print(f"[Scanner Error] {e}")
            return None