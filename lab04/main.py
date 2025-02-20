import time
from item import Item
from potion import Potion
from shield import Shield
from weapon import Weapon
from tests import tests

if __name__ == "__main__":
    print("Kyle Kessler")
    print("Intermediate Python Programming")
    print("Lab 04")
    print("----------------------------------")
    long_bow = Weapon("Bethronding", "legendary", 5000, "bow", "Good for attacking enemies at a distance!")
    long_bow.pick_up("Beleg")
    long_bow.equip()
    long_bow.use()
    print('\n')

    broken_pot_lid = Shield(name='wooden lid', description="A lid made of wood, useful in cooking. No one will choose it willingly for a shield", defense=5, broken=True)
    broken_pot_lid.pick_up("Beleg")
    broken_pot_lid.equip()
    broken_pot_lid.use()
    broken_pot_lid.throw_away()
    broken_pot_lid.use()
    print('\n')

    attack_potion = Potion.from_ability("atk potion tmp", owner='Beleg', type= "attack") # Remove duration to make it 30 seconds
    attack_potion.use()
    attack_potion.use()
    print('\n')

    print(isinstance(long_bow, Item))
    print(isinstance(broken_pot_lid, Shield))
    print(isinstance(attack_potion, Weapon))
    print('\n')

    time.sleep(1)
    print("_____ Document test cases over _____________")
    print("----------------------------")
    tests()