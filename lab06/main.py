import time
import json
from item import Item
from potion import Potion
from shield import Shield
from weapon import *
from inventory import Inventory
from colorama import Fore, Style, init
init(autoreset=True)  # Resets colors automatically



if __name__ == "__main__":
    print("Kyle Kessler")
    print("Intermediate Python Programming")
    print("Lab 05")
    print("----------------------------------")
    print("_____________ Lab 05 test Beginning _____________")

    print ("_____ Creating Items _____")
    beleg_backpack = Inventory(owner="Beleg")
    belthronding = Weapon("Belthronding", "Legendary", 500, "bow", "A mighty bow made of black yew-wood")
    master_sword = Weapon("Master Sword", "Legendary", 300,  "sword", "A sword deserving of only the most skilled swordsman")
    broken_pot_lid = Shield(name='wooden lid', description="A lid made of wood, useful in cooking. No one will choose it willingly for a shield", defense=5, broken=True)
    round_shield = Shield(name="Round Shield", description="A sturdy shield", defense=15, broken=False)
    tower_shield = Shield(name="tower shield", description="A rectangular shield", defense=15, broken=False)
    muramasa = Weapon("Muramasa", "Legendary", 580,  "battle axe", "A cursed axe with dark aura eminating from it's head")
    gungnir = Weapon("Gungnir", "Legendary", 290,  "spear", "I wonder how Odin lost this...")
    claw = Weapon("Enchanted Claws", "Epic", 300,  "claw", "They say cat scratches hurt the soul")
    wand = Weapon("Magic Wand", "Uncommon", 150,  "wand", "This wand chose you")
    hp_potion = Potion.from_ability("health potion", owner='Beleg', type= "hp") # Remove duration to make it 30 seconds
    attack_potion = Potion.from_ability("attack potion", owner='Beleg', type= "attack") # Remove duration to make it 30 seconds
    defense_potion = Potion.from_ability("defense potion", owner='Beleg', type= "defense") # Remove duration to make it 30 seconds
    
    print("Items Created")

    print("_____ Adding items to backpack _____")
    beleg_backpack.add_item(belthronding)
    beleg_backpack.add_item(master_sword)
    beleg_backpack.add_item(hp_potion)
    beleg_backpack.add_item(broken_pot_lid)
    beleg_backpack.add_item(muramasa)
    beleg_backpack.add_item(gungnir)
    beleg_backpack.add_item(round_shield)

    print("_____ Starting Tests _____")
    print("--- View Shields ---")
    beleg_backpack.view(type='shield')

    print("--- View All Items ---")
    beleg_backpack.view()

    print("--- Drop broken Lid ---")
    beleg_backpack.drop_item(broken_pot_lid)
    # Equipping and using weapons

    print("\n--- Use Weapon ---")
    if master_sword in beleg_backpack:
        master_sword.equip()
        print(master_sword)
        master_sword.use()
        master_sword.unequip()

    print("\n--- item check ---")
    for item in beleg_backpack:
        if isinstance(item, Weapon):
            beleg_backpack.view(item = item)


    print("_____________ Document test cases over _____________")
    print("----------------------------")
    print("_____________ User test cases started _____________")
    print("\nTesting if broken lid was dropped")
    beleg_backpack.view(type="shield")

    beleg_backpack.add_item(attack_potion)
    beleg_backpack.add_item(defense_potion)
    beleg_backpack.add_item(claw)
    beleg_backpack.add_item(wand)
    beleg_backpack.add_item(tower_shield)

    print("\nUsing potions")

    # time.sleep(1)
    # if defense_potion in beleg_backpack:
    #     defense_potion.use()

    for item in beleg_backpack:
        if isinstance(item, Potion):
            beleg_backpack.view(item=item)


    print('\n-- Testing Health Potion --')
    if hp_potion in beleg_backpack:
        hp_potion.use()

    print('\n-- Testing weapon buffs --')
    if claw in beleg_backpack:
        claw.equip()
        attack_potion.use()
        print(claw)
        claw.use()
        claw.unequip()

    if gungnir in beleg_backpack:
        gungnir.equip()
        print(gungnir)
        gungnir.use()

    print('\n-- Testing shield buffs --')
    if round_shield in beleg_backpack:
        round_shield.equip()
        defense_potion.use()
        print(round_shield)
        round_shield.use()

    if tower_shield in beleg_backpack:
        tower_shield.equip()
        print(tower_shield)
        tower_shield.use()
    
    # Create json string
    temp_item = Item(name ="my_name", rarity="Epic", owner="Kyle", description="Insert description")
    temp = temp_item.to_json()
    print("\nSerialized Item (JSON): ")
    print(json.dumps(temp, indent=4))
    temp_json_string = json.dumps(temp)
    
    # Rebuild item
    new_temp = Item.from_json(json_data=temp_json_string)

    print(new_temp)
    
    print("\nYou may close terminal. This will run for 30 seconds.")