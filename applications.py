""" applications.py - Provide utility classes for handling applications"""

import uuid
import random
import pandas as pd
import functools

def generate_id(length: int) -> str:
    """Generate a random uuid and return last `length` characters from it"""
    return str(uuid.uuid4())[:length]

@functools.total_ordering
class Slot: 
    """Implementation of a slot: an item that can only be reserved once"""
    def __init__(self, value: int) -> None:
        self.value = value

    def __repr__(self):
        return f"Slot {self.value}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other) -> bool:
        if hasattr(other, "value"):
            return self.value == other.value
        
        return self.value == other

    def __lt__(self, other) -> bool:
        if hasattr(other, "value"):
            return self.value < other.value

        return self.value < other

    def __hash__(self):
        return hash(self.__repr__())

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
        if slot is not None and slot.value >= self.lo_bound and slot.value <= self.hi_bound:
            degree = self.coeff * (slot.value - self.lo_bound)
            return f"hsv({degree}, 100, 100)"

        return "hsv(0, 0, 0)"

    def __repr__(self):
        return f"[{self.lo_bound}-{self.hi_bound}]" 

    def __str__(self):
        return self.__repr__()

class Application:
    """Implementation of a random application with an id and `amount` of slots"""
    def __init__(self, amount: int, slotspace: SlotSpace) -> None:
        self.id = generate_id(6)
        self.slotspace = slotspace
        self.requested_slots = self.get_slots(amount)

        self.reserved = None

    def get_slots(self, amount: int) -> list[Slot]:
        slots = []
        for _ in range(amount):
            slots.append(self.slotspace.pull())

        return slots

    def reserve(self, slot: Slot) -> None:
        self.reserved = slot

    def __repr__(self):
        return f"{self.id}: {self.requested_slots}" 

    def __str__(self):
        return self.__repr__()

def generate_applications(amount: int, slotspace: SlotSpace) -> list[Application]:
    applications = []
    for _ in range(amount):
        applications.append(Application(amount=3, slotspace=slotspace))

    return applications

def generate_dataframe(applications: list[Application]) -> pd.DataFrame:
    data = []
    for application in applications:
        data.append({
            "id": application.id,
            "request_1": application.requested_slots[0],
            "request_2": application.requested_slots[1],
            "request_3": application.requested_slots[2],
            "reserved": application.reserved
        })

    return pd.DataFrame(data)


