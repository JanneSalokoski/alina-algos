""" prefer-sparse.py - Distribute slots based on their sparsity"""

import applications

from time import perf_counter

def prefer_sparse(slotspace: applications.SlotSpace,
    appls: list[applications.Application]) -> int:
    """Distribute slots based on their sparsity"""

    print(f"Slotspace: {slotspace}")
    print(f"Applications: {len(appls)}")

    print("Start distributing slots")
    t1 = perf_counter()

    slot_counts = {}
    for appl in appls:
        for slot in appl.requested_slots:
            if slot not in slot_counts:
                slot_counts[slot] = []

            slot_counts[slot].append(appl)

    slot_counts = dict(sorted(slot_counts.items(), key=lambda x: len(x[1])))
    print("Got sorted counts of slot appearances")

    reserved = set()
    for slot in slot_counts:
        for reserver in slot_counts[slot]:
            if reserver.reserved == None and slot not in reserved:
                reserver.reserve(slot)
                reserved.add(slot)

    t2 = perf_counter()
    print(f"Finished distributing slots in {t2-t1:.4f}s")

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
    """Run `prefer_sparse` with some data"""

    slotspace = applications.SlotSpace(0, 1200)
    appls = applications.generate_applications(1000, slotspace)

    prefer_sparse(slotspace, appls)

if __name__ == "__main__":
    main()

