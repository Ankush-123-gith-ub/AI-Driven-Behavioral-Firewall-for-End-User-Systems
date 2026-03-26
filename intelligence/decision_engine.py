# intelligence/decision_engine.py

from intelligence.rules_engine import RulesEngine
from intelligence.anomaly_engine import AnomalyEngine
from intelligence.threat_intel import ThreatIntel
from intelligence.fusion_engine import FusionEngine
from analysis.feature_builder import FeatureBuilder

class DecisionResult:
    def __init__(self):
        self.rule_score = 0.0
        self.anomaly_score = 0.0
        self.threat_score = 0.0
        self.final_score = 0.0
        self.verdict = "ALLOW"

    def pretty_print(self):
        print("\n========== DECISION ==========")
        print(f"Rule Score: {round(self.rule_score, 3)}")
        print(f"Anomaly Score: {round(self.anomaly_score, 3)}")
        print(f"Threat Score: {round(self.threat_score, 3)}")
        print(f"Final Score: {round(self.final_score, 3)}")
        print(f"Verdict: {self.verdict}")
        print("================================\n")


class DecisionEngine:

    def __init__(self):
        self.rules = RulesEngine()
        self.anomaly = AnomalyEngine()
        self.threat = ThreatIntel()
        self.fusion = FusionEngine()
        self.feature_builder = FeatureBuilder()

    def decide(self, event):

        result = DecisionResult()

        # Rule score
        result.rule_score = self.rules.evaluate(event)

        # Build feature vector
        feature_vector = self.feature_builder.build(event)

        # Anomaly score
        result.anomaly_score = self.anomaly.evaluate(feature_vector)

        # Threat score
        result.threat_score = self.threat.evaluate(event.file_hash)

        # 🚨 IMMEDIATE BLOCK IF KNOWN MALICIOUS
        if result.threat_score == 1.0:
            result.final_score = 1.0
            result.verdict = "BLOCK"
            return result

        # Normal fusion if not malicious
        result.final_score = self.fusion.fuse(
            result.rule_score,
            result.anomaly_score,
            result.threat_score
        )

        if result.final_score >= 0.75:
            result.verdict = "BLOCK"
        elif result.final_score >= 0.50:
            result.verdict = "SUSPICIOUS"
        else:
            result.verdict = "ALLOW"

        return result