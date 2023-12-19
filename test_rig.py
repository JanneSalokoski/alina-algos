""" test-rig.py - Test some algos"""

import applications
import random_order
import prefer_sparse
import graph_coloring

import os

def test_algo(algo, slot_amount, application_amount):
    slotspace = applications.SlotSpace(0, slot_amount)
    appls = applications.generate_applications(application_amount, slotspace)

    return algo(slotspace, appls)

def test_algos(algos, slot_amount, application_amount):
    results = []
    for algo in algos:
        results.append({
            "algo": algo.__name__,
            "not_distributed": test_algo(algo, slot_amount, application_amount)
        })

    os.system("clear")
    print(f"Testing with {slot_amount} slots and {application_amount} applications")

    for res in results:
        percentage = (res["not_distributed"] / 1000) * 100
        print(f"{res["algo"]}: {res["not_distributed"]} not distributed -> {percentage:.2f}%")


def main() -> None:
    algos = [
        random_order.random_order,
        prefer_sparse.prefer_sparse,
        graph_coloring.graph_coloring
    ]

    test_algos(algos, 30*5, 60)

if __name__ == "__main__":
    main()
