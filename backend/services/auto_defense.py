import time
import threading
import requests

BASE_URL = "http://127.0.0.1:8000"

running = False
worker = None


def calculate_threat_score(detection):
    """
    Convert ML detection result into a 0-100 threat score.
    """

    confidence = float(detection.get("confidence", 0))

    attack_type = str(
        detection.get("attack_type", "NORMAL")
    ).upper()

    score = confidence * 100

    # Increase score for serious attack types
    if attack_type in ["DDOS", "DDoS".upper()]:
        score += 15

    elif attack_type in ["INTRUSION", "INTRUSION_DETECTION"]:
        score += 10

    elif attack_type in ["BOTNET", "MALWARE"]:
        score += 15

    return min(round(score, 2), 100)


def classify_severity(score):

    if score >= 80:
        return "CRITICAL"

    if score >= 60:
        return "HIGH"

    if score >= 40:
        return "MEDIUM"

    return "LOW"


def create_incident(detection, score, severity):

    payload = {
        "title": "Automated 6G Security Threat",
        "description": (
            f"Automatic ML detection identified "
            f"{detection.get('attack_type', 'UNKNOWN')} "
            f"traffic."
        ),
        "severity": severity,
        "threat_score": score,
        "attack_type": detection.get(
            "attack_type",
            "UNKNOWN"
        ),
        "confidence": detection.get(
            "confidence",
            0
        )
    }

    try:

        response = requests.post(
            f"{BASE_URL}/incidents/",
            json=payload,
            timeout=5
        )

        print(
            "Incident:",
            response.status_code,
            response.text
        )

        return response.json()

    except Exception as e:

        print("Incident creation error:", e)

        return None


def process_detection(detection):

    score = calculate_threat_score(detection)

    severity = classify_severity(score)

    print("--------------------------------")
    print("ATTACK TYPE :", detection.get("attack_type"))
    print("CONFIDENCE  :", detection.get("confidence"))
    print("THREAT SCORE:", score)
    print("SEVERITY    :", severity)
    print("--------------------------------")

    # Automatically create incident
    if score >= 40:

        create_incident(
            detection,
            score,
            severity
        )


def defense_loop():

    global running

    print("Automatic defense started")

    while running:

        try:

            # Get simulator status
            response = requests.get(
                f"{BASE_URL}/simulator/status",
                timeout=5
            )

            status = response.json()

            print("Simulator:", status)

            # Only process when simulator is running
            if status.get("running"):

                attack = status.get(
                    "current_attack",
                    "NONE"
                )

                if attack != "NONE":

                    # Temporary detection result.
                    # Replace this with your ML detector.
                    detection = {
                        "attack_type": attack,
                        "confidence": 0.90
                    }

                    process_detection(
                        detection
                    )

        except Exception as e:

            print(
                "Automatic defense error:",
                e
            )

        time.sleep(5)

    print("Automatic defense stopped")


def start_defense():

    global running
    global worker

    if running:
        return {
            "status": "already_running"
        }

    running = True

    worker = threading.Thread(
        target=defense_loop,
        daemon=True
    )

    worker.start()

    return {
        "status": "started"
    }


def stop_defense():

    global running

    running = False

    return {
        "status": "stopped"
    }