""" random-order.py - Random order base distribution of slots"""

import random
import applications

from time import perf_counter

def random_order(slotspace: applications.SlotSpace,
    appls: list[applications.Application]) -> int:
    """Random order based distribution of slots"""

    print(f"Slotspace: {slotspace}")
    print(f"Applications: {len(appls)}")

    random.shuffle(appls)
    print("\nShuffled applications\n")


    print("Started reserving slots")
    t1 = perf_counter()

    reserved = []
    for appl in appls:
        for slot in appl.requested_slots:
            if slot not in reserved:
                reserved.append(slot)
                appl.reserve(slot)
                break

    t2 = perf_counter()
    print(f"Finished reserving slots in {t2-t1:.4f}s")

    df = applications.generate_dataframe(appls)
    df = df.sort_values(by=["reserved"])
    print(f"\nReserved slots:\n{df}\n")

    counts = df["reserved"].value_counts(dropna=False)

    none_amount = 0
    try:
        none_amount = counts[None]
    except Exception:
        print(f"All applications have a reserved slot!")

    percent = none_amount / len(appls)

    print(f"Applications without a reserved slot: {none_amount} -> {percent*100:.2f}%")

    return int(none_amount)

def main():
    """Run `random_order` with some data"""

    slotspace = applications.SlotSpace(0, 1200)
    appls = applications.generate_applications(1000, slotspace)

    random_order(slotspace, appls)

if __name__ == "__main__":
    main()

