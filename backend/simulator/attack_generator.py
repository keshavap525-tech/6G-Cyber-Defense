import random
import uuid
from datetime import datetime

from .traffic_generator import generate_ip


ATTACK_TYPES = [
    "DDoS",
    "DoS",
    "PORT_SCAN",
    "BRUTE_FORCE",
    "BOTNET",
    "DATA_EXFILTRATION"
]


def generate_ddos():
    return {
        "flow_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),

        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),

        "source_port": random.randint(1024, 65535),
        "destination_port": random.choice([80, 443]),

        "protocol": "TCP",
        "application": "web",

        "packet_size": random.randint(64, 512),
        "duration": round(random.uniform(0.001, 0.2), 4),

        "packets_sent": random.randint(5000, 50000),
        "packets_received": random.randint(1, 20),

        "bytes_sent": random.randint(500000, 5000000),
        "bytes_received": random.randint(100, 5000),

        "connection_attempts": random.randint(1000, 10000),

        "label": "DDoS"
    }


def generate_dos():
    return {
        "flow_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),

        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),

        "source_port": random.randint(1024, 65535),
        "destination_port": random.choice([80, 443, 8080]),

        "protocol": random.choice(["TCP", "UDP"]),

        "application": "web",

        "packet_size": random.randint(64, 1024),
        "duration": round(random.uniform(0.01, 1.0), 4),

        "packets_sent": random.randint(1000, 10000),
        "packets_received": random.randint(0, 50),

        "bytes_sent": random.randint(100000, 1000000),
        "bytes_received": random.randint(100, 10000),

        "connection_attempts": random.randint(100, 2000),

        "label": "DoS"
    }


def generate_port_scan():
    return {
        "flow_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),

        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),

        "source_port": random.randint(1024, 65535),
        "destination_port": random.randint(1, 65535),

        "protocol": "TCP",
        "application": "network_scanner",

        "packet_size": random.randint(40, 100),
        "duration": round(random.uniform(0.001, 0.1), 4),

        "packets_sent": random.randint(100, 1000),
        "packets_received": random.randint(0, 10),

        "bytes_sent": random.randint(5000, 100000),
        "bytes_received": random.randint(0, 1000),

        "connection_attempts": random.randint(100, 5000),

        "label": "PORT_SCAN"
    }


def generate_brute_force():
    return {
        "flow_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),

        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),

        "source_port": random.randint(1024, 65535),
        "destination_port": random.choice([22, 21, 3389, 443]),

        "protocol": "TCP",
        "application": "authentication",

        "packet_size": random.randint(100, 1000),
        "duration": round(random.uniform(0.1, 2.0), 4),

        "packets_sent": random.randint(100, 2000),
        "packets_received": random.randint(1, 50),

        "bytes_sent": random.randint(10000, 500000),
        "bytes_received": random.randint(100, 10000),

        "connection_attempts": random.randint(50, 1000),

        "label": "BRUTE_FORCE"
    }


def generate_botnet():
    return {
        "flow_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),

        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),

        "source_port": random.randint(1024, 65535),
        "destination_port": random.choice([80, 443, 8080]),

        "protocol": random.choice(["TCP", "UDP"]),

        "application": "botnet",

        "packet_size": random.randint(100, 1500),
        "duration": round(random.uniform(0.1, 10), 4),

        "packets_sent": random.randint(500, 5000),
        "packets_received": random.randint(1, 100),

        "bytes_sent": random.randint(50000, 1000000),
        "bytes_received": random.randint(100, 10000),

        "connection_attempts": random.randint(20, 500),

        "label": "BOTNET"
    }


def generate_data_exfiltration():
    return {
        "flow_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),

        "source_ip": generate_ip(),
        "destination_ip": generate_ip(),

        "source_port": random.randint(1024, 65535),
        "destination_port": random.choice([443, 80]),

        "protocol": "HTTPS",
        "application": "data_transfer",

        "packet_size": random.randint(1000, 1500),
        "duration": round(random.uniform(5, 60), 4),

        "packets_sent": random.randint(5000, 50000),
        "packets_received": random.randint(100, 1000),

        "bytes_sent": random.randint(5000000, 50000000),
        "bytes_received": random.randint(1000, 100000),

        "connection_attempts": random.randint(1, 20),

        "label": "DATA_EXFILTRATION"
    }


def generate_attack(attack_type=None):

    if attack_type is None:
        attack_type = random.choice(ATTACK_TYPES)

    generators = {
        "DDoS": generate_ddos,
        "DoS": generate_dos,
        "PORT_SCAN": generate_port_scan,
        "BRUTE_FORCE": generate_brute_force,
        "BOTNET": generate_botnet,
        "DATA_EXFILTRATION": generate_data_exfiltration
    }

    if attack_type not in generators:
        raise ValueError(f"Unknown attack type: {attack_type}")

    return generators[attack_type]()