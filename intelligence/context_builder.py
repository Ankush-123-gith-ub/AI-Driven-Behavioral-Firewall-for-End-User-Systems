# intelligence/context_builder.py

class ContextBuilder:

    def build(self, event):

        context = {}

        # FILE CONTEXT
        file_name = (event.file_name or "").lower()
        file_path = (event.file_path or "").lower()

        context["is_executable"] = file_name.endswith((".exe", ".bat", ".ps1", ".cmd"))
        context["is_temp"] = "temp" in file_path
        context["is_download"] = "download" in file_path

        # ⚙️ PROCESS CONTEXT
        context["is_script_engine"] = file_name in ["powershell.exe", "cmd.exe"]

        # 🌐 NETWORK CONTEXT
        context["has_network_activity"] = getattr(event, "network_score", 0.0) > 0
        context["high_network_risk"] = getattr(event, "network_score", 0.0) >= 0.7

        # 🧬 REGISTRY CONTEXT
        context["has_persistence"] = getattr(event, "registry_flag", False)

        # BEHAVIOR FLAGS
        context["is_new_file"] = event.first_seen
        context["is_high_entropy"] = (event.entropy or 0) > 7

        return context