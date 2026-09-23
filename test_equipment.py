from equipment import Item, Player, equip, unequip, total_power


def test_equip():
    sword = Item("Меч", "right_hand", power=10)
    player = Player("Игрок", inventory=[sword])

    before = len(player.inventory)

    for slot in player.slots:
        if player.slots[slot] is not None:
            before += 1

    assert equip(player, sword) is True
    assert player.slots["right_hand"] is sword
    assert sword not in player.inventory

    after = len(player.inventory)

    for slot in player.slots:
        if player.slots[slot] is not None:
            after += 1

    assert before == after


test_equip()
print("Тест пройден")

def test_replace():
    old_sword = Item("Старый меч", "right_hand", power=5)
    new_sword = Item("Новый меч", "right_hand", power=10)

    player = Player("Игрок", inventory=[old_sword, new_sword])

    before = len(player.inventory)

    for slot in player.slots:
        if player.slots[slot] is not None:
            before += 1

    equip(player, old_sword)

    assert equip(player, new_sword) is True
    assert player.slots["right_hand"] is new_sword
    assert old_sword in player.inventory
    assert new_sword not in player.inventory

    after = len(player.inventory)

    for slot in player.slots:
        if player.slots[slot] is not None:
            after += 1

    assert before == after


test_replace()
print("Замена предмета: тест пройден")

def test_two_handed():
    sword = Item("Двуручный меч", "right_hand", power=20, two_handed=True)
    shield = Item("Щит", "left_hand", power=5)
    player = Player("Игрок", inventory=[sword, shield])

    equip(player, shield)
    equip(player, sword)

    assert player.slots["right_hand"] is sword
    assert player.slots["left_hand"] is None
    assert shield in player.inventory
    assert sword not in player.inventory

    total = len(player.inventory)

    for slot in player.slots:
        if player.slots[slot] is not None:
            total += 1

    assert total == 2


test_two_handed()
print("Двуручное оружие: тест пройден")

def test_unequip():
    sword = Item("Меч", "right_hand", power=10)
    player = Player("Игрок", inventory=[sword])

    equip(player, sword)

    assert unequip(player, "right_hand") is True
    assert player.slots["right_hand"] is None
    assert sword in player.inventory


test_unequip()
print("Снятие предмета: тест пройден")

def test_total_power():
    sword = Item("Меч", "right_hand", power=20)
    helmet = Item("Шлем", "head", power=10, durability=0)
    player = Player("Игрок", inventory=[sword, helmet])
    equip(player, sword)
    equip(player, helmet)
    assert total_power(player) == 20


test_total_power()
print("Подсчёт силы: тест пройден")

def test_level():
    sword = Item("Сильный меч", "right_hand", power=50, level_req=5)
    player = Player("Игрок", level=1, inventory=[sword])
    assert equip(player, sword) is False
    assert sword in player.inventory
    assert player.slots["right_hand"] is None

test_level()
print("Проверка уровня: тест пройден")

def test_invalid_slot():
    item = Item("Странный предмет", "foot", power=10)
    player = Player("Игрок", inventory=[item])
    assert equip(player, item) is False
    assert item in player.inventory

test_invalid_slot()
print("Неправильный слот: тест пройден")

def test_one_handed_with_two_handed():
    sword = Item("Двуручный меч", "right_hand", power=20, two_handed=True)
    shield = Item("Щит", "left_hand", power=5)
    player = Player("Игрок", inventory=[sword, shield])
    assert equip(player, sword) is True
    assert equip(player, shield) is True
    assert player.slots["left_hand"] is shield
    assert sword in player.inventory
    assert shield not in player.inventory


test_one_handed_with_two_handed()
print("Замена двуручного оружия: тест пройден")

def test_capacity():
    sword = Item("Двуручный меч", "right_hand", power=20, two_handed=True)
    shield = Item("Щит", "left_hand", power=5)

    player = Player(
        "Игрок",
        inventory=[sword, shield],
        capacity=0
    )

    assert equip(player, shield) is True
    assert equip(player, sword) is False

    assert shield in player.slots.values()
    assert sword in player.inventory


test_capacity()
print("Проверка вместимости: тест пройден")