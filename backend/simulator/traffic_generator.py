import random
import uuid
from datetime import datetime


PROTOCOLS = ["TCP", "UDP", "HTTP", "HTTPS", "QUIC"]

APPLICATIONS = [
    "video_streaming",
    "iot",
    "telemedicine",
    "smart_city",
    "autonomous_vehicle",
    "cloud",
    "mobile_app"
]


def generate_ip():
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def generate_normal_traffic():
    packet_size = random.randint(64, 1500)
    duration = round(random.uniform(0.01, 5.0), 4)

    packets_sent = random.randint(1, 100)
    packets_received = random.randint(1, 100)

    bytes_sent = packet_size * packets_sent
    bytes_received = packet_size * packets_received

    return {
        "flow_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),

        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),

        "source_port": random.randint(1024, 65535),
        "destination_port": random.choice([
            80, 443, 53, 22, 8080, 5000
        ]),

        "protocol": random.choice(PROTOCOLS),
        "application": random.choice(APPLICATIONS),

        "packet_size": packet_size,
        "duration": duration,

        "packets_sent": packets_sent,
        "packets_received": packets_received,

        "bytes_sent": bytes_sent,
        "bytes_received": bytes_received,

        "connection_attempts": random.randint(1, 5),

        "label": "NORMAL"
    }