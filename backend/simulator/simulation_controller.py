import random
import threading
import time
from datetime import datetime


class SimulationController:

    def __init__(self):

        # ========================================================
        # SIMULATOR STATE
        # ========================================================

        self.running = False

        self.total_packets = 0
        self.total_threats = 0
        self.total_incidents = 0

        self.current_attack = "NONE"

        self.last_event = None
        self.last_analysis = None

        self.lock = threading.Lock()

        self.simulation_thread = None

    # ============================================================
    # START SIMULATOR
    # ============================================================

    def start(self):

        with self.lock:

            if self.running:

                return {
                    "success": True,
                    "message": "6G simulator is already running",
                    "running": True
                }

            self.running = True

        self.simulation_thread = threading.Thread(
            target=self._simulation_loop,
            daemon=True
        )

        self.simulation_thread.start()

        return {
            "success": True,
            "message": "6G simulator started",
            "running": True
        }

    # ============================================================
    # STOP SIMULATOR
    # ============================================================

    def stop(self):

        with self.lock:

            self.running = False

        return {
            "success": True,
            "message": "6G simulator stopped",
            "running": False
        }

    # ============================================================
    # MAIN SIMULATION LOOP
    # ============================================================

    def _simulation_loop(self):

        print("[6G SIMULATOR] Simulation loop started")

        while True:

            # ----------------------------------------------------
            # CHECK WHETHER SIMULATOR IS RUNNING
            # ----------------------------------------------------

            with self.lock:

                if not self.running:
                    break

                attack_type = self.current_attack

            # ----------------------------------------------------
            # GENERATE NETWORK TRAFFIC
            # ----------------------------------------------------

            event = self._generate_traffic(
                attack_type
            )

            # ----------------------------------------------------
            # UPDATE TRAFFIC STATISTICS
            # ----------------------------------------------------

            with self.lock:

                self.total_packets += event[
                    "packet_count"
                ]

                self.last_event = event

            print(
                "[6G TRAFFIC]",
                attack_type,
                "| packets=",
                event["packet_count"]
            )

            # ----------------------------------------------------
            # SEND EVENT TO DETECTION SERVICE
            # ----------------------------------------------------

            try:

                from backend.services.detection_service import (
                    DetectionService
                )

                detector = DetectionService()

                analysis = detector.analyze(
                    event
                )

                # ------------------------------------------------
                # SAVE DETECTION RESULT
                # ------------------------------------------------

                with self.lock:

                    self.last_analysis = analysis

                    # Count detected attacks
                    if analysis.get(
                        "is_attack",
                        False
                    ):

                        self.total_threats += 1

                    # Count created incidents
                    if analysis.get(
                        "incident_id"
                    ):

                        self.total_incidents += 1

                print(
                    "[DETECTION]",
                    analysis.get(
                        "prediction"
                    ),
                    "| score=",
                    analysis.get(
                        "threat_score",
                        0
                    ),
                    "| incident=",
                    analysis.get(
                        "incident_id"
                    )
                )

            except Exception as e:

                print(
                    "[SIMULATION ERROR]",
                    str(e)
                )

                with self.lock:

                    self.last_analysis = {

                        "prediction": "ERROR",

                        "confidence": 0.0,

                        "threat_score": 0.0,

                        "is_attack": False,

                        "incident_id": None,

                        "error": str(e)
                    }

            # ----------------------------------------------------
            # WAIT BEFORE NEXT EVENT
            # ----------------------------------------------------

            time.sleep(1)

        print("[6G SIMULATOR] Simulation loop stopped")

    # ============================================================
    # GENERATE 6G NETWORK TRAFFIC
    # ============================================================

    def _generate_traffic(
        self,
        attack_type
    ):

        timestamp = datetime.now().isoformat()

        # --------------------------------------------------------
        # IP ADDRESSES
        # --------------------------------------------------------

        src_ip = (
            f"10.0.0.{random.randint(1, 254)}"
        )

        dst_ip = (
            f"10.0.1.{random.randint(1, 254)}"
        )

        # --------------------------------------------------------
        # PORTS
        # --------------------------------------------------------

        src_port = random.randint(
            1024,
            65535
        )

        dst_port = random.choice(
            [
                22,
                53,
                80,
                443,
                8080
            ]
        )

        # --------------------------------------------------------
        # PROTOCOL
        # --------------------------------------------------------

        protocol = random.choice(
            [
                "TCP",
                "UDP"
            ]
        )

        # ========================================================
        # NORMAL TRAFFIC
        # ========================================================

        if attack_type == "NONE":

            packet_count = random.randint(
                50,
                500
            )

            bytes_count = (
                packet_count
                * random.randint(
                    500,
                    1500
                )
            )

            duration = round(
                random.uniform(
                    0.5,
                    5.0
                ),
                2
            )

            attack_label = "NORMAL"

        # ========================================================
        # DDOS ATTACK
        # ========================================================

        elif attack_type == "DDOS":

            packet_count = random.randint(
                3000,
                8000
            )

            bytes_count = (
                packet_count
                * random.randint(
                    800,
                    1500
                )
            )

            duration = round(
                random.uniform(
                    0.1,
                    1.0
                ),
                2
            )

            attack_label = "DDOS"

        # ========================================================
        # PORT SCAN ATTACK
        # ========================================================

        elif attack_type == "PORT_SCAN":

            packet_count = random.randint(
                500,
                1500
            )

            bytes_count = (
                packet_count
                * random.randint(
                    40,
                    150
                )
            )

            duration = round(
                random.uniform(
                    0.1,
                    1.5
                ),
                2
            )

            attack_label = "PORT_SCAN"

        # ========================================================
        # BOTNET ATTACK
        # ========================================================

        elif attack_type == "BOTNET":

            packet_count = random.randint(
                1000,
                4000
            )

            bytes_count = (
                packet_count
                * random.randint(
                    300,
                    1000
                )
            )

            duration = round(
                random.uniform(
                    0.2,
                    2.0
                ),
                2
            )

            attack_label = "BOTNET"

        # ========================================================
        # UNKNOWN ATTACK TYPE
        # ========================================================

        else:

            packet_count = random.randint(
                50,
                500
            )

            bytes_count = (
                packet_count
                * random.randint(
                    500,
                    1500
                )
            )

            duration = round(
                random.uniform(
                    0.5,
                    5.0
                ),
                2
            )

            attack_label = "NORMAL"

        # ========================================================
        # TRAFFIC EVENT
        # ========================================================

        return {

            "timestamp": timestamp,

            "src_ip": src_ip,

            "dst_ip": dst_ip,

            "src_port": src_port,

            "dst_port": dst_port,

            "protocol": protocol,

            "packet_count": packet_count,

            "bytes": bytes_count,

            "duration": duration,

            "attack_type": attack_label
        }

    # ============================================================
    # CHANGE ATTACK TYPE
    # ============================================================

    def set_attack(
        self,
        attack_type
    ):

        allowed_attacks = [
            "NONE",
            "DDOS",
            "PORT_SCAN",
            "BOTNET"
        ]

        attack_type = str(
            attack_type
        ).upper()

        if attack_type not in allowed_attacks:

            return {

                "success": False,

                "message": "Unknown attack type",

                "allowed": allowed_attacks
            }

        with self.lock:

            self.current_attack = attack_type

        print(
            "[6G SIMULATOR] Attack changed to:",
            attack_type
        )

        return {

            "success": True,

            "message": (
                "Attack type changed to "
                + attack_type
            ),

            "attack": attack_type
        }

    # ============================================================
    # GET SIMULATOR STATUS
    # ============================================================

    def status(self):

        with self.lock:

            threat_score = 0

            if isinstance(
                self.last_analysis,
                dict
            ):

                threat_score = (
                    self.last_analysis.get(
                        "threat_score",
                        0
                    )
                )

            return {

                "running": self.running,

                "total_packets": (
                    self.total_packets
                ),

                "total_threats": (
                    self.total_threats
                ),

                "total_incidents": (
                    self.total_incidents
                ),

                "current_attack": (
                    self.current_attack
                ),

                "last_event": (
                    self.last_event
                ),

                "last_analysis": (
                    self.last_analysis
                ),

                "threat_score": (
                    threat_score
                )
            }


# ================================================================
# GLOBAL SIMULATOR INSTANCE
# ================================================================

simulation_controller = SimulationController()
