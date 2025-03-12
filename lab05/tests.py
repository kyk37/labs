import time
from weapon import Weapon
from shield import Shield
from potion import Potion


def tests():

    print("____ Starting Personal Tests ______")
    print("Test case 1: Drinking attack potion")
    wand = Weapon(name = "Superior Wand", rarity="Common", damage=1000, weapon_type="wand", description="A well crafted wand")
    wand.pick_up("Echo")
    attack_potion = Potion.from_ability("Giants Strength Potion", owner='Echo', type= "attack")
    wand.equip()
    wand.use() # output
    attack_potion.use()
    wand.use() # output
    time.sleep(1) # add short delay for timer

    print("----------------------------")
    print("Test Case 2: Drinking defense potion")
    shield = Shield(name='Wooden Shield', shield_type="wooden shield", description="A shield made of wood, it's quite weak", defense=10, broken=False)
    defense_potion = Potion.from_ability("Sturdy Defense potion", owner='Echo', type= "defense")
    shield.pick_up("Echo")
    shield.equip()
    shield.use()
    defense_potion.use()
    time.sleep(1)
    shield.use()

    print("---------------------------")
    print("Test Case 3: Drinking health potion")
    print("Simulated healing as character class does not exist")
    healing_potion = Potion.from_ability("Basic Healing Potion", owner='Echo', type= "hp")
    healing_potion.use()


    print("---------------------------")
    print("Test Case 5: Unequipping weapon/shield")
    wand.unequip()
    shield.unequip()

    print("---------------------------")
    print("Test Case 6: Thrown Away")
    wand.throw_away()
    shield.throw_away()

    print("---------------------------")
    print("Test Case 7: Use thrown away item")
    print("Note: Section blank as items are not used. (No owner/inactive)")
    wand.use()
    shield.use()

    print("---------------------------")
    print("Test Case 8: Pick up thrown away item")
    print("Note: Fails when no character picks up item")
    wand.pick_up("Echo")
    shield.pick_up("Echo")

    print("---------------------------")
    print("Test Case 9: Equip and use picked up items")
    wand.equip()
    shield.equip()
    wand.use()
    shield.use()

    print("------- Waiting for Potions to wear off ----------")
    time.sleep(30)

    print("---------------------------")
    print("Test Case 10: Use items after potions wear off")
    wand.use()
    shield.use()
    
    # The below cause ValueErrors
    # test_atk_pot = Potion.from_ability("atk potion tmp", type= "attack")
    # test_stew = Potion.from_ability("Grand Pot", "grand", "Beleg")
    