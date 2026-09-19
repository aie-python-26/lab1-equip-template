"""Экипировка. Здесь ты пишешь новую систему.

Классы Item и Player трогать не надо: их держит остальной сервер, и менять
поля нельзя. Твоя работа — три функции внизу.
"""

SLOTS = ("head", "body", "right_hand", "left_hand", "ring_1", "ring_2")
HANDS = ("right_hand", "left_hand")


class Item:
    """Вещь. Класс достался от старой системы."""

    def __init__(self, name, slot, power=0, durability=100, level_req=1,
                 two_handed=False):
        self.name = name
        self.slot = slot
        self.power = power
        self.durability = durability
        self.level_req = level_req
        self.two_handed = two_handed

    def __bool__(self):
        # Валера: «удобно же — if item: значит вещь целая»
        return self.durability > 0

    def __repr__(self):
        return f"<{self.name} {self.slot} dur={self.durability}>"


class Player:
    def __init__(self, name, level=1, inventory=None, capacity=20):
        self.name = name
        self.level = level
        self.inventory = list(inventory) if inventory else []
        self.capacity = capacity
        self.slots = {slot: None for slot in SLOTS}

    def __repr__(self):
        return f"<{self.name} lvl={self.level} inv={len(self.inventory)}>"

def equip(player, item):
    if player.level < item.level_req:
        return False
    if item.two_handed:
        slots = ["right_hand", "left_hand"]
    else:
        slots = [item.slot]

    old_slots = [player.slots[x] for x in slots if player.slots[x] is not None]

    if len(player.inventory) - 1 + len(old_slots) > player.capacity:
        return False

    player.inventory.remove(item)

    for slot in slots:
        if player.slots[slot] is not None:
            player.inventory.append(player.slots[slot])
        player.slots[slot] = item

    return True


def unequip(player, slot):
    if player.slots[slot] is None:
        return False

    item = player.slots[slot]

    if item.two_handed:
        player.slots["right_hand"] = None
        player.slots["left_hand"] = None
    else:
        player.slots[slot] = None

    player.inventory.append(item)

    return True




def total_power(player):
    total = 0
    for slot in SLOTS:
        item = player.slots[slot]
        if item is None:
            continue
        if item.durability > 0:
            total += item.power
    return total
