# response/file_quarantine.py

import os
import shutil


class FileQuarantine:

    def __init__(self):
        self.quarantine_dir = "quarantine"

    def quarantine(self, file_path):

        if not os.path.exists(file_path):
            return

        os.makedirs(self.quarantine_dir, exist_ok=True)

        filename = os.path.basename(file_path)
        destination = os.path.join(self.quarantine_dir, filename)

        shutil.move(file_path, destination)

        print(f"[ACTION] File moved to quarantine: {destination}")