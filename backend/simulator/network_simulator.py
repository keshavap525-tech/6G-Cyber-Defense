import random
import time

from .traffic_generator import generate_normal_traffic
from .attack_generator import generate_attack


class NetworkSimulator:

    def __init__(self):
        self.running = False
        self.total_packets = 0

    def generate_packet(self, attack_probability=0.20):
        """
        Generate one simulated 6G network flow.

        attack_probability:
            Probability that generated traffic is malicious.
        """

        self.total_packets += 1

        if random.random() < attack_probability:
            packet = generate_attack()
        else:
            packet = generate_normal_traffic()

        packet["packet_number"] = self.total_packets

        return packet

    def generate_batch(
        self,
        count=100,
        attack_probability=0.20
    ):

        traffic = []

        for _ in range(count):

            packet = self.generate_packet(
                attack_probability
            )

            traffic.append(packet)

        return traffic

    def stream(
        self,
        interval=1.0,
        attack_probability=0.20
    ):

        self.running = True

        while self.running:

            packet = self.generate_packet(
                attack_probability
            )

            yield packet

            time.sleep(interval)

    def stop(self):
        self.running = False


if __name__ == "__main__":

    simulator = NetworkSimulator()

    print("=" * 60)
    print("6G NETWORK TRAFFIC SIMULATOR")
    print("=" * 60)

    traffic = simulator.generate_batch(
        count=20,
        attack_probability=0.30
    )

    for packet in traffic:

        print(
            packet["packet_number"],
            packet["source_ip"],
            "->",
            packet["destination_ip"],
            "|",
            packet["label"]
        )

    print("=" * 60)
    print(f"Generated traffic: {len(traffic)}")
    print("=" * 60)