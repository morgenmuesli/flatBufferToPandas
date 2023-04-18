# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import flatbuffers
from MyGame.Sample.Monster import Monster
import MyGame.Sample.Color
import MyGame.Sample.Equipment
import MyGame.Sample.Monster
import MyGame.Sample.Vec3
import MyGame.Sample.Weapon
import json
import os
MINIMUM_BUFFER_SIZE = 1024


def create_weapon(builder, name, damage):
    # Create the name.
    name_offset = builder.CreateString(name)
    # Create the weapon.
    MyGame.Sample.Weapon.WeaponStart(builder)
    MyGame.Sample.Weapon.WeaponAddName(builder, name_offset)
    MyGame.Sample.Weapon.WeaponAddDamage(builder, damage)
    return MyGame.Sample.Weapon.WeaponEnd(builder)


def create_inventory(builder, size: int):
    # Create the inventory.
    MyGame.Sample.Monster.StartInventoryVector(builder, size)
    for i in range(size):
        builder.PrependByte(i)
    return builder.EndVector()


def insert_weapons(builder, weapons):
    # Create the weapons.
    MyGame.Sample.Monster.StartWeaponsVector(builder, len(weapons))
    for weapon in weapons:
        builder.PrependUOffsetTRelative(weapon)
    return builder.EndVector()


def create_path(builder, path):
    # Create the path.
    MyGame.Sample.Monster.StartPathVector(builder, len(path))
    for point in path:
        assert len(point) == 3  # x, y, z
        MyGame.Sample.Vec3.CreateVec3(builder, *point)
    return builder.EndVector()


def create_monster(builder: flatbuffers.Builder, name: str, hp: int, pos, color, weapons, inventory, path, equipped_weapon):
    name = builder.CreateString(name)
    # Create our monster by using `Monster.Start()` and `Monster.End()`.
    MyGame.Sample.Monster.Start(builder)
    MyGame.Sample.Monster.AddPos(builder,
                                 MyGame.Sample.Vec3.CreateVec3(builder, *pos))
    MyGame.Sample.Monster.AddHp(builder, hp)
    MyGame.Sample.Monster.AddName(builder, name)
    MyGame.Sample.Monster.AddInventory(builder, inventory)
    MyGame.Sample.Monster.AddColor(builder,
                                   color)
    MyGame.Sample.Monster.AddWeapons(builder, weapons)  #
    MyGame.Sample.Monster.AddEquippedType(
        builder, MyGame.Sample.Equipment.Equipment().Weapon)  # Union type
    MyGame.Sample.Monster.AddEquipped(builder, equipped_weapon)  # Union data
    MyGame.Sample.Monster.AddPath(builder, path)
    orc = MyGame.Sample.Monster.End(builder)
    return orc


def create_sample_game():
    # create the builder
    builder = flatbuffers.Builder(MINIMUM_BUFFER_SIZE)
    # create the weapons
    sword = create_weapon(builder, "Sword", 3)
    axe = create_weapon(builder, "Axe", 5)
    # insert the weapons
    weapons = insert_weapons(builder, [axe, sword])
    # create the inventory
    inventory = create_inventory(builder, 10)
    # create the path
    path = create_path(builder, [[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
    # create the monster
    monster = create_monster(builder, "Orc", 300, [1., 2., 3.], MyGame.Sample.Color.Color().Red, weapons, inventory, path, axe)

    # finish the buffer
    builder.Finish(monster)

    return builder


def write_sample_game(builder, path: str = "monster.bin"):
    # Finish the buffer.
    buffer = builder.Output()
    # Write the buffer to disk.
    with open(path, "wb") as f:
        f.write(buffer)


def read_sample_game(path: str):
    # read the buffer from disk as bytes
    with open(path, "rb") as f:
        buffer = f.read()
    # read the monster from the buffer
    monster = Monster.GetRootAsMonster(buffer, 0)
    return monster


def print_monster(monster):
    # access the primitive fields
    hp = monster.Hp()
    mana = monster.Mana()
    name = monster.Name()

    # access the nested struct
    pos = monster.Pos()
    x = pos.X()
    y = pos.Y()
    z = pos.Z()

    # access the inventory as a list
    inv_len = monster.InventoryLength()
    third_item = monster.Inventory(2)

    # accessing nested tables
    weapons_length = monster.WeaponsLength()
    equipped_weapons_string = ""
    for i in range(weapons_length):
        weapon = monster.Weapons(i)
        weapon_name = weapon.Name()
        weapon_damage = weapon.Damage()
        equipped_weapons_string += f"{weapon_name}({weapon_damage}), "

    # accessing unions
    union_type = monster.EquippedType()
    if union_type == MyGame.Sample.Equipment.Equipment().Weapon:
        # `monster.Equipped()` returns a `flatbuffers.Table`, which can be used to
        # initialize a `MyGame.Sample.Weapon.Weapon()`.
        union_weapon = MyGame.Sample.Weapon.Weapon()
        union_weapon.Init(monster.Equipped().Bytes, monster.Equipped().Pos)



    print(
        f"hp: {hp}, mana: {mana}, name: {name}, pos: {x}, {y}, {z}, inv_len: {inv_len}, weapons: {equipped_weapons_string}, union_type: {union_type}, union_weapon: {union_weapon.Name()}({union_weapon.Damage()})")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    builder = create_sample_game()
    write_sample_game(builder)
    monster = read_sample_game("monster.bin")
    print_monster(monster)










