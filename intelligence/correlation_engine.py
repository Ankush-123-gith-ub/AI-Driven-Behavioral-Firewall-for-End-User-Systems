class CorrelationEngine:

    def correlate(self, rule, anomaly, threat, network, context, registry_flag, cmdline):

        score = (
            rule * 0.3 +
            anomaly * 0.2 +
            threat * 0.2 +
            network * 0.3
        )

        # 🔥 Registry persistence
        if registry_flag:
            score += 0.3

        # 🔥 Command-line attacks
        if cmdline:
            print("[DEBUG] CMDLINE DETECTED:", cmdline)

        if "powershell" in cmdline or "cmd.exe" in cmdline:
            score += 0.7   # 🔥 BIG BOOST FOR DEMO

        # 🔥 Context boosts
        if context.get("is_temp") and context.get("is_executable"):
            score += 0.6

        if context.get("is_script_engine") and network > 0.5:
            score += 0.3

        return min(score, 1.0)