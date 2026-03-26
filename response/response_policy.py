# response/response_policy.py

class ResponsePolicy:

    def decide_action(self, verdict):

        if verdict == "BLOCK":
            return ["kill", "quarantine", "alert"]

        if verdict == "SUSPICIOUS":
            return ["alert"]

        return []