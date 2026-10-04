from datetime import datetime
import uuid

from backend.services.response_engine import ResponseEngine
from backend.ml.predict import IntrusionDetector
from backend.services.threat_engine import ThreatEngine
from backend.database.database import SessionLocal
from backend.database.models import SecurityIncident


class DetectionService:

    def __init__(self):
        self.detector = IntrusionDetector()
        self.threat_engine = ThreatEngine()
        self.response_engine = ResponseEngine()

    def analyze(self, traffic: dict):

        # =====================================================
        # 1. ML DETECTION
        # =====================================================

        prediction_result = self.detector.predict(traffic)

        prediction = prediction_result.get(
            "prediction",
            "NORMAL"
        )

        confidence = float(
    prediction_result.get(
        "confidence",
        prediction_result.get("threat_score", 0.0)
    )
)

        threat_score = confidence
        # =====================================================
        # 2. SIMULATOR ATTACK OVERRIDE
        # =====================================================

        simulated_attack = str(
            traffic.get(
                "attack_type",
                "NONE"
            )
        ).upper()

        if simulated_attack not in [
            "NONE",
            "NORMAL",
            "BENIGN"
        ]:

            prediction = simulated_attack

            confidence = 0.95
            threat_score = 0.95

        # =====================================================
        # 3. THREAT ANALYSIS
        # =====================================================

        try:
         threat_result = self.threat_engine.analyze(
           prediction=prediction,
           threat_score=threat_score,
          traffic=traffic,
          confidence=confidence
)

        except Exception as e:

            print(
                f"Threat engine error: {e}"
            )

            threat_result = {
                "error": str(e)
            }

        # =====================================================
        # 4. FINAL THREAT SCORE
        # =====================================================

        final_threat_score = threat_score

        if isinstance(threat_result, dict):

            final_threat_score = float(
                threat_result.get(
                    "threat_score",
                    threat_result.get(
                        "risk_score",
                        threat_score
                    )
                )
            )

        # =====================================================
        # 5. DETERMINE ATTACK
        # =====================================================

        is_attack = (
            str(prediction).upper()
            not in [
                "NORMAL",
                "BENIGN",
                "NONE"
            ]
        )

        # =====================================================
        # 6. SECURITY INCIDENT
        # =====================================================

        incident_id = None

        if is_attack:

            db = SessionLocal()

            try:

                # Generate unique incident ID
                incident_id = (
                    "INC-"
                    + datetime.utcnow().strftime(
                        "%Y%m%d-%H%M%S"
                    )
                    + "-"
                    + uuid.uuid4().hex[:6].upper()
                )

                incident = SecurityIncident(

                    incident_id=incident_id,

                    timestamp=datetime.utcnow(),

                    source_ip=traffic.get(
                        "src_ip"
                    ),

                    destination_ip=traffic.get(
                        "dst_ip"
                    ),

                    source_port=traffic.get(
                        "src_port"
                    ),

                    destination_port=traffic.get(
                        "dst_port"
                    ),

                    protocol=traffic.get(
                        "protocol"
                    ),

                    attack_type=str(
                        prediction
                    ),

                    confidence=confidence,

                    risk_score=int(
                        final_threat_score
                    ),

                    severity=(
                        threat_result.get(
                            "severity",
                            "LOW"
                        )
                        if isinstance(
                            threat_result,
                            dict
                        )
                        else "LOW"
                    ),

                    recommended_action=(
                        threat_result.get(
                            "recommended_action"
                        )
                        if isinstance(
                            threat_result,
                            dict
                        )
                        else None
                    ),

                    status="OPEN",

                    details=(
                        f"6G network attack detected: "
                        f"{prediction}"
                    )
                )

                db.add(incident)

                db.commit()

                db.refresh(incident)

                print(
                    f"[INCIDENT] Created: "
                    f"{incident_id}"
                )

            except Exception as e:

                db.rollback()

                print(
                    f"Incident database error: {e}"
                )

                incident_id = None

            finally:

                db.close()

        # =====================================================
        # 7. AUTOMATED RESPONSE
        # =====================================================

        response_result = None

        if is_attack:

            try:

                response_result = (
                    self.response_engine.respond(
                        prediction=prediction,
                        threat_score=final_threat_score,
                        traffic=traffic
                    )
                )

            except Exception as e:

                print(
                    f"Response engine error: {e}"
                )

                response_result = {
                    "error": str(e)
                }

        # =====================================================
        # 8. FINAL RESULT
        # =====================================================

        return {

            "prediction": prediction,

            "confidence": confidence,

            "threat_score": final_threat_score,

            "is_attack": is_attack,

            "incident_id": incident_id,

            "threat_analysis": threat_result,

            "response": response_result,

            "traffic": traffic

        }
