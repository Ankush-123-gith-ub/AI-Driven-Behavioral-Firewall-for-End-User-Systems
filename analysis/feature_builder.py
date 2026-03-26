# analysis/feature_builder.py

class FeatureBuilder:

    def build(self, event):

        return [
            event.entropy or 0.0,
            event.file_size or 0,
            event.location_risk or 0.0,
            1 if event.first_seen else 0,
            1 if event.file_age_seconds and event.file_age_seconds < 300 else 0,
            len(event.signature_matches)
        ]