# intelligence/fusion_engine.py

class FusionEngine:

    def fuse(self, rule_score, anomaly_score, threat_score):

        final_score = (
            0.5 * rule_score +
            0.3 * anomaly_score +
            0.2 * threat_score
        )

        return min(final_score, 1.0)