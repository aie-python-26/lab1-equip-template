"""Экипировка. Здесь ты пишешь новую систему.

Классы Item и Player трогать не надо: их держит остальной сервер, и менять
поля нельзя. Твоя работа — три функции внизу.
"""

SLOTS = ("head", "body", "right_hand", "left_hand", "ring_1", "ring_2")
# Не отдельное хранилище: просто два ключа из SLOTS, чтобы не писать их руками.
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
    if item.slot not in SLOTS:
        return False
    before = len(player.inventory)
    for slot in player.slots:
        if player.slots[slot] is not None:
            before += 1

    if item not in player.inventory:
        return False

    if player.level < item.level_req:
        return False
    if not item.two_handed:
        old = player.slots[item.slot]

        if item.slot in HANDS:
            if player.slots["right_hand"] is not None:
                if player.slots["right_hand"].two_handed:
                    old = player.slots["right_hand"]
                    player.slots["right_hand"] = None

        player.inventory.remove(item)

        if old is not None:
            player.inventory.append(old)

        player.slots[item.slot] = item
    else:
        right = player.slots["right_hand"]
        left = player.slots["left_hand"]

        free = player.capacity - len(player.inventory)
        need = 0
        if right is not None:
            need += 1
        if left is not None:
            need += 1
        if len(player.inventory) - 1 + need > player.capacity:
            return False
        if right is not None:
            player.inventory.append(right)
        if left is not None:
            player.inventory.append(left)
        player.inventory.remove(item)
        player.slots["right_hand"] = item
        player.slots["left_hand"] = None
    after = len(player.inventory)
    for slot in player.slots:
        if player.slots[slot] is not None:
            after += 1

    assert before == after
    return True


def unequip(player, slot):
    if slot not in SLOTS:
        return False

    before = len(player.inventory)

    for slot_name in player.slots:
        if player.slots[slot_name] is not None:
            before += 1

    item = player.slots[slot]

    if item is None:
        return False

    player.inventory.append(item)
    player.slots[slot] = None

    if item.two_handed:
        player.slots["left_hand"] = None

    after = len(player.inventory)

    for slot_name in player.slots:
        if player.slots[slot_name] is not None:
            after += 1

    assert before == after

    return True

def total_power(player):
    power = 0

    for slot in player.slots:
        item = player.slots[slot]
        if item is not None and item.durability > 0:
            power += item.power

    return power