""" applications.py - Provide utility classes for handling applications"""

import uuid
import random

def generate_id(length: int) -> str:
    """Generate a random uuid and return last `length` characters from it"""
    return str(uuid.uuid4())[:length]

class Slot: 
    """Implementation of a slot: an item that can only be reserved once"""
    def __init__(self, value: int) -> None:
        self.value = value

class SlotSpace:
    """Defines a range of possible slots"""
    def __init__(self, lo_bound: int, hi_bound: int) -> None:
        self.lo_bound = lo_bound
        self.hi_bound = hi_bound

        self.range = hi_bound - lo_bound
        self.coeff = 360 / self.range

    def pull(self) -> Slot:
        """Get a random Slot from this SlotSpace"""
        return Slot(random.randint(self.lo_bound, self.hi_bound))

    def color(self, slot: Slot) -> str:
        if slot.value >= self.lo_bound and slot.value <= self.hi_bound:
            degree = self.coeff * (slot.value - self.lo_bound)
            return f"hsv({degree}, 100, 100)"

        raise ValueError(f"Slot {slot} not in range [{self.lo_bound},{self.hi_bound}]")

class Application:
    """Implementation of a random application with an id and `amount` of slots"""
    def __init__(self, amount: int, slotspace: SlotSpace) -> None:
        self.id = generate_id(6)
        self.slotspace = slotspace
        self.requested_slots = self.get_slots(amount)

    def get_slots(self, amount: int) -> list[Slot]:
        slots = []
        for _ in range(amount):
            slots.append(self.slotspace.pull())

        return slots
