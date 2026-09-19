from equipment import Item, Player, equip, unequip, total_power


def test_equip_надел():
    p = Player("A")
    sword = Item("Меч", "right_hand")
    p.inventory.append(sword)

    assert equip(p, sword) is True
    assert sword not in p.inventory
    assert p.slots["right_hand"] is sword


def test_equip_слот_занят():
    p = Player("A")
    old = Item("Старый", "right_hand")
    new = Item("Новый", "right_hand")
    p.slots["right_hand"] = old
    p.inventory.append(new)

    assert equip(p, new) is True
    assert p.slots["right_hand"] is new
    assert old in p.inventory


def test_equip_уровень_мал():
    p = Player("A", level=1)
    sword = Item("Меч", "right_hand", level_req=10)
    p.inventory.append(sword)

    assert equip(p, sword) is False


def test_equip_двуручное():
    p = Player("A")
    sword = Item("Двуручник", "right_hand", two_handed=True)
    p.inventory.append(sword)

    assert equip(p, sword) is True
    assert p.slots["right_hand"] is sword
    assert p.slots["left_hand"] is sword


def test_unequip_пусто():
    p = Player("A")
    assert unequip(p, "head") is False


def test_unequip_сломанная():
    p = Player("A")
    broken = Item("Сломанный", "head", durability=0)
    p.slots["head"] = broken

    assert unequip(p, "head") is True
    assert broken in p.inventory


def test_total_power():
    p = Player("A")
    p.slots["right_hand"] = Item("Меч", "right_hand", power=10)
    p.slots["body"] = Item("Броня", "body", power=5, durability=0)

    assert total_power(p) == 10