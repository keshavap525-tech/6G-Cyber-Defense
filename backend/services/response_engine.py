class ResponseEngine:

    def __init__(self):
        self.last_response = None

    def respond(
        self,
        prediction,
        threat_score,
        traffic
    ):
        """
        Simulated defensive response.

        This project does not modify the real network.
        The response is recorded as a simulated
        cybersecurity action.
        """

        prediction = str(prediction).upper()

        try:
            threat_score = float(threat_score)
        except (TypeError, ValueError):
            threat_score = 0.0

        # -----------------------------------------
        # Select defensive action
        # -----------------------------------------

        if prediction in ["NORMAL", "BENIGN"]:
            action = "MONITOR"

        elif threat_score >= 0.80:
            action = "BLOCK"

        elif threat_score >= 0.50:
            action = "QUARANTINE"

        else:
            action = "RATE_LIMIT"

        # -----------------------------------------
        # Create response
        # -----------------------------------------

        result = {
            "action": action,
            "status": "SIMULATED",
            "prediction": prediction,
            "threat_score": threat_score,
            "message": (
                f"Simulated defense action: {action}"
            ),
            "traffic": traffic
        }

        self.last_response = result

        print(
            f"[DEFENSE] {action} | "
            f"prediction={prediction} | "
            f"threat_score={threat_score}"
        )

        return result

    def get_last_response(self):
        return self.last_response