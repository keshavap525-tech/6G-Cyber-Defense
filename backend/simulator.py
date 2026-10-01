import random
import threading
import time

from backend.ml.predict import IntrusionDetector


class Simulator:

    def __init__(self):
        self.running = False
        self.current_attack = "NONE"

        self.total_packets = 0
        self.total_threats = 0
        self.total_incidents = 0

        self.last_event = None
        self.last_analysis = None
        self.threat_score = 0

        self.detector = IntrusionDetector()

        self.thread = None

    def start(self):
        if self.running:
            return {
                "message": "Simulator already running"
            }

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

        return {
            "message": "6G simulator started",
            "running": True
        }

    def stop(self):
        self.running = False

        return {
            "message": "6G simulator stopped",
            "running": False
        }

    def set_attack(self, attack_type):
        self.current_attack = attack_type.upper()

        return {
            "message": "Attack configured",
            "attack": self.current_attack
        }

    def get_status(self):

        return {
            "running": self.running,
            "total_packets": self.total_packets,
            "total_threats": self.total_threats,
            "total_incidents": self.total_incidents,
            "current_attack": self.current_attack,
            "last_event": self.last_event,
            "last_analysis": self.last_analysis,
            "threat_score": self.threat_score
        }

    def _run(self):

        while self.running:

            traffic = self._generate_traffic()

            self.total_packets += traffic["packet_count"]

            try:

                result = self.detector.predict(traffic)

                self.last_analysis = result

                self.threat_score = result.get(
                    "threat_score",
                    0
                )

                prediction = result.get(
                    "prediction",
                    "NORMAL"
                )

                if prediction.upper() != "NORMAL":

                    self.total_threats += 1
                    self.total_incidents += 1

                    self.last_event = {
                        "type": prediction,
                        "attack": self.current_attack,
                        "traffic": traffic
                    }

                else:

                    self.last_event = {
                        "type": "NORMAL",
                        "attack": self.current_attack,
                        "traffic": traffic
                    }

            except Exception as e:

                self.last_analysis = {
                    "error": str(e)
                }

            time.sleep(2)

    def _generate_traffic(self):

        # Normal traffic
        packet_count = random.randint(50, 200)
        packet_size = random.randint(256, 1200)
        duration = random.uniform(5, 20)
        bytes_sent = random.randint(10000, 100000)
        bytes_received = random.randint(10000, 100000)

        # Simulated attacks
        if self.current_attack == "DOS":

            packet_count = random.randint(
                1500,
                5000
            )

            packet_size = random.randint(
                1500,
                2500
            )

            duration = random.uniform(
                0.1,
                1
            )

            bytes_sent = random.randint(
                1000000,
                5000000
            )

            bytes_received = random.randint(
                1000000,
                5000000
            )

        elif self.current_attack == "DDOS":

            packet_count = random.randint(
                3000,
                10000
            )

            packet_size = random.randint(
                1500,
                3000
            )

            duration = random.uniform(
                0.05,
                0.5
            )

            bytes_sent = random.randint(
                5000000,
                15000000
            )

            bytes_received = random.randint(
                5000000,
                15000000
            )

        elif self.current_attack == "PORT_SCAN":

            packet_count = random.randint(
                1000,
                3000
            )

            packet_size = random.randint(
                64,
                300
            )

            duration = random.uniform(
                0.1,
                2
            )

        return {
            "packet_count": packet_count,
            "packet_size": packet_size,
            "duration": duration,
            "bytes_sent": bytes_sent,
            "bytes_received": bytes_received
        }


# Global simulator instance

simulator = Simulator()