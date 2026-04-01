# analysis/feature_builder.py

import os


class FeatureBuilder:

    def build(self, event):

        # -------- File Extension --------
        file_extension = ""
        if event.file_name and "." in event.file_name:
            file_extension = event.file_name.split('.')[-1].lower()

        # -------- Executable Detection --------
        is_executable = 1 if file_extension in ["exe", "dll", "bat", "cmd", "ps1"] else 0

        # -------- Suspicious Location --------
        is_temp_location = 1 if event.file_path and any(x in event.file_path.lower() for x in ["temp", "downloads"]) else 0

        # -------- Young File --------
        is_young = 1 if event.file_age_seconds and event.file_age_seconds < 300 else 0

        return [
            event.entropy or 0.0,                      # randomness
            event.file_size or 0,                      # size
            event.location_risk or 0.0,                # risky path
            1 if event.first_seen else 0,              # new file
            is_young,                                 # recently created
            len(event.signature_matches),             # suspicious patterns
            is_executable,                            #  important
            is_temp_location                          #  important
        ]