from typing import Dict, Any


class ThreatEngine:
    """
    Threat intelligence and risk scoring engine.

    Combines:
    - ML prediction
    - ML confidence
    - Attack severity
    - Traffic characteristics
    """

    ATTACK_SEVERITY = {
        "NORMAL": 0,
        "PORT_SCAN": 35,
        "BRUTE_FORCE": 55,
        "BOTNET": 65,
        "DOS": 75,
        "DDOS": 90,
        "DATA_EXFILTRATION": 95,
    }

    def analyze(
        self,
        prediction="NORMAL",
        confidence=0.0,
        traffic=None,
        **kwargs
    ):
        """
        Main method used by DetectionService.
        """

        if traffic is None:
            traffic = {}

        # Allow alternate parameter names
        if "score" in kwargs and confidence == 0:
            confidence = kwargs["score"]

        # Convert prediction to uppercase
        prediction = str(prediction).upper()

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.0

        # Confidence may sometimes arrive as 0-100
        if confidence > 1:
            confidence = confidence / 100.0

        confidence = max(0.0, min(1.0, confidence))

        result = self.calculate_risk(
            prediction=prediction,
            confidence=confidence,
            traffic=traffic
        )

        return result

    def calculate_risk(
        self,
        prediction: str,
        confidence: float,
        traffic: Dict[str, Any]
    ) -> Dict[str, Any]:

        prediction = str(prediction).upper()

        # ------------------------------------------------
        # Base threat score
        # ------------------------------------------------

        base_score = self.ATTACK_SEVERITY.get(
            prediction,
            50
        )

        # ------------------------------------------------
        # ML confidence contribution
        # ------------------------------------------------

        confidence_score = confidence * 20

        # ------------------------------------------------
        # Traffic behavior contribution
        # ------------------------------------------------

        behavior_score = 0

        # Support both simulator and ML feature names
        packets_sent = float(
            traffic.get(
                "packets_sent",
                traffic.get(
                    "packet_count",
                    0
                )
            )
        )

        connection_attempts = float(
            traffic.get(
                "connection_attempts",
                traffic.get(
                    "packet_count",
                    0
                )
            )
        )

        bytes_sent = float(
            traffic.get(
                "bytes_sent",
                traffic.get(
                    "bytes",
                    0
                )
            )
        )

        # ------------------------------------------------
        # High packet volume
        # ------------------------------------------------

        if packets_sent > 5000:
            behavior_score += 10

        elif packets_sent > 1000:
            behavior_score += 5

        # ------------------------------------------------
        # High connection attempts
        # ------------------------------------------------

        if connection_attempts > 5000:
            behavior_score += 10

        elif connection_attempts > 1000:
            behavior_score += 5

        # ------------------------------------------------
        # Large data transfer
        # ------------------------------------------------

        if bytes_sent > 10_000_000:
            behavior_score += 10

        elif bytes_sent > 1_000_000:
            behavior_score += 5

        # ------------------------------------------------
        # Calculate final score
        # ------------------------------------------------

        if prediction == "NORMAL":

            risk_score = 0

        else:

            risk_score = (
                base_score * 0.65
                + confidence_score
                + behavior_score
            )

        risk_score = min(
            100,
            max(
                0,
                round(risk_score)
            )
        )

        # ------------------------------------------------
        # Determine severity
        # ------------------------------------------------

        if risk_score >= 85:

            severity = "CRITICAL"

        elif risk_score >= 65:

            severity = "HIGH"

        elif risk_score >= 35:

            severity = "MEDIUM"

        else:

            severity = "LOW"

        # ------------------------------------------------
        # Recommended response
        # ------------------------------------------------

        if severity == "CRITICAL":

            recommended_action = "ISOLATE_SOURCE"

        elif severity == "HIGH":

            recommended_action = "BLOCK_SOURCE"

        elif severity == "MEDIUM":

            recommended_action = "MONITOR_AND_ALERT"

        else:

            recommended_action = "ALLOW"

        # ------------------------------------------------
        # Final result
        # ------------------------------------------------

        return {
            "risk_score": risk_score,
            "threat_score": risk_score,
            "severity": severity,
            "threat_level": severity,
            "recommended_action": recommended_action,

            "threat_details": {
                "attack_type": prediction,
                "ml_confidence": round(
                    confidence,
                    4
                ),
                "base_severity": base_score,
                "behavior_score": behavior_score
            }
        }