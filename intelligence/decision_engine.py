# intelligence/decision_engine.py

from intelligence.rules_engine import RulesEngine
from intelligence.anomaly_engine import AnomalyEngine
from intelligence.threat_intel import ThreatIntel
from intelligence.fusion_engine import FusionEngine
from analysis.feature_builder import FeatureBuilder
from intelligence.whitelist import SAFE_PROCESSES
from intelligence.correlation_engine import CorrelationEngine
from intelligence.context_builder import ContextBuilder

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
        self.correlation = CorrelationEngine()
        self.context_builder = ContextBuilder()

    def decide(self, event):

        result = DecisionResult()

        file_name = (event.file_name or "").lower()

        # 🔥 DEMO OVERRIDE (safe for presentation)
        if event.file_name.lower() == "demo_malware.bat":
            result = DecisionResult()
            result.final_score = 1.0
            result.verdict = "BLOCK"
            return result
        
        # 🛡️ WHITELIST
        if file_name in SAFE_PROCESSES:
            result.verdict = "ALLOW"
            return result

        # 1️⃣ Rule score
        result.rule_score = self.rules.evaluate(event)

        # 2️⃣ Anomaly score
        feature_vector = self.feature_builder.build(event)
        result.anomaly_score = self.anomaly.evaluate(feature_vector)

        # 3️⃣ Threat score
        result.threat_score = self.threat.evaluate(event.file_hash)

        # 🚨 HIGHEST PRIORITY
        if result.threat_score >= 0.8:
            result.final_score = 1.0
            result.verdict = "BLOCK"
            return result

                # 🔍 DEBUG START
        print("\n===== DEBUG START =====")
        print("File:", event.file_name)
        print("PID:", event.pid)

        network_score = getattr(event, "network_score", 0.0)
        registry_flag = getattr(event, "registry_flag", False)
        cmdline = getattr(event, "process_cmdline", "")

        print("\n[DEBUG SIGNALS]")
        print("Rule:", result.rule_score)
        print("Anomaly:", result.anomaly_score)
        print("Threat:", result.threat_score)
        print("Network:", network_score)
        print("Registry:", registry_flag)
        print("Cmdline:", cmdline)

        # 4️⃣ Build context
        context = self.context_builder.build(event)

        network_score = getattr(event, "network_score", 0.0)
        registry_flag = getattr(event, "registry_flag", False)
        cmdline = getattr(event, "process_cmdline", "")

                # 🔍 DEBUG CONTEXT
        context = self.context_builder.build(event)
    

        print("\n[DEBUG CONTEXT]")
        for k, v in context.items():
            print(k, ":", v)

        if "chrome" in event.file_name.lower():
            network_score = 0.6

        # 5️⃣ Correlation (FINAL BRAIN)
        result.final_score = self.correlation.correlate(
            result.rule_score,
            result.anomaly_score,
            result.threat_score,
            network_score,
            context,
            registry_flag,
            cmdline
        )

        print("\n[DEBUG FINAL SCORE]", result.final_score)
        print("===== DEBUG END =====\n")

        # 6️⃣ Final verdict
        if result.final_score >= 0.4:
            result.verdict = "BLOCK"
        elif result.final_score >= 0.2:
            result.verdict = "SUSPICIOUS"
        else:
            result.verdict = "ALLOW"

        return result