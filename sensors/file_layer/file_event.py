class FileExecutionEvent:
    def __init__(self):
        self.pid = None
        self.file_path = None
        self.file_name = None
        self.file_size = None
        self.file_hash = None
        self.first_seen = None
        self.location_risk = None
        self.file_age_seconds = None
        self.entropy = None
        self.signature_matches = []
        self.network_score = 0.0
        self.registry_flag = False
        self.process_cmdline = ""

    def pretty_print(self):
        print("\n========== FILE EVENT ==========")
        print(f"PID: {self.pid}")
        print(f"File: {self.file_name}")
        print(f"Path: {self.file_path}")
        print(f"Size: {self.file_size} bytes")
        print(f"Hash: {self.file_hash}")
        print(f"First Seen: {self.first_seen}")
        print(f"Location Risk: {self.location_risk}")
        print(f"File Age: {round(self.file_age_seconds, 2)} sec")
        print(f"Entropy: {round(self.entropy, 3)}")
        print(
            f"Signature Matches: "
            f"{self.signature_matches if self.signature_matches else 'None'}"
        )