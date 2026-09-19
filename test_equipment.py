from equipment import Item, Player, equip, unequip, total_power
#дипсик писал тесты

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





def test_unequip_обычная():
    p = Player("A")
    меч = Item("Меч", "right_hand")
    p.slots["right_hand"] = меч

    assert unequip(p, "right_hand") is True
    assert p.slots["right_hand"] is None
    assert меч in p.inventory


def test_unequip_пустой_слот():
    p = Player("A")

    assert unequip(p, "head") is False
    assert p.slots["head"] is None
    assert p.inventory == []


def test_unequip_сломанная_вещь():
    p = Player("A")
    broken = Item("Сломанный", "head", durability=0)
    p.slots["head"] = broken

    assert unequip(p, "head") is True
    assert p.slots["head"] is None
    assert broken in p.inventory


def test_unequip_двуручное_освобождает_обе_руки():
    p = Player("A")
    двуручник = Item("Двуручник", "right_hand", two_handed=True)
    p.slots["right_hand"] = двуручник
    p.slots["left_hand"] = двуручник

    assert unequip(p, "right_hand") is True
    assert p.slots["right_hand"] is None
    assert p.slots["left_hand"] is None
    assert двуручник in p.inventory


def test_unequip_инвариант():
    def count(p):
        return len(p.inventory) + sum(1 for v in p.slots.values() if v is not None)

    p = Player("A")
    меч = Item("Меч", "right_hand")
    p.slots["right_hand"] = меч

    before = count(p)
    unequip(p, "right_hand")
    assert count(p) == before


if __name__ == "__main__":
    test_equip_надел()
    test_equip_слот_занят()
    test_equip_уровень_мал()
    test_equip_двуручное()
    test_unequip_обычная()
    test_unequip_пустой_слот()
    test_unequip_сломанная_вещь()
    test_unequip_двуручное_освобождает_обе_руки()
    test_unequip_инвариант()
    print("OK")
