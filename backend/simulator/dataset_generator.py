import csv
import os

from .network_simulator import NetworkSimulator


OUTPUT_FILE = "dataset/raw/6g_network_traffic.csv"


def generate_dataset(
    number_of_records=10000,
    attack_probability=0.25
):

    simulator = NetworkSimulator()

    traffic = simulator.generate_batch(
        count=number_of_records,
        attack_probability=attack_probability
    )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    if not traffic:
        print("No traffic generated.")
        return

    fieldnames = traffic[0].keys()

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(traffic)

    print("=" * 60)
    print("DATASET GENERATION COMPLETE")
    print("=" * 60)
    print(f"Records generated : {len(traffic)}")
    print(f"Output file       : {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":

    generate_dataset(
        number_of_records=10000,
        attack_probability=0.25
    )