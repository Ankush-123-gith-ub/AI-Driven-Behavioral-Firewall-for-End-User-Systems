# intelligence/rules_engine.py

class RulesEngine:

    def __init__(self):
        self.weights = {
            "entropy": 0.30,
            "signature": 0.30,
            "location": 0.15,
            "first_seen": 0.10,
            "young_file": 0.15
        }

    def evaluate(self, event):

        score = 0.0

        # Entropy rule
        if event.entropy is not None:
            if event.entropy > 7.5:
                score += self.weights["entropy"]
            elif event.entropy > 7.0:
                score += self.weights["entropy"] * 0.6
            elif event.entropy > 6.5:
                score += self.weights["entropy"] * 0.3

        # Signature rule
        if event.signature_matches:
            score += min(
                len(event.signature_matches) * 0.1,
                self.weights["signature"]
            )

        # Location rule
        if event.location_risk is not None:
            score += event.location_risk * self.weights["location"]

        # First seen
        if event.first_seen:
            score += self.weights["first_seen"]

        # Young file (<5 min)
        if event.file_age_seconds is not None and event.file_age_seconds < 300:
            score += self.weights["young_file"]

        return min(score, 1.0)
    