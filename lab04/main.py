from item import Item
from potion import Potion
from shield import Shield
from weapon import Weapon



if __name__ == "__main__":
    long_bow = Weapon("Bethronding", "legendary", 5000, "long bow", "Good for attacking enemies at a distance!")
    long_bow.pick_up("Beleg")
    long_bow.equip()
    long_bow.use()
    print("No output here at use()")
    
    broken_pot_lid = Shield(name='wooden lid', description="A lid made of wood, useful in cooking. No one will choose it willingly for a shield", defense=5, broken=True)
    broken_pot_lid.pick_up("Beleg")
    broken_pot_lid.equip()
    broken_pot_lid.use()
    broken_pot_lid.throw_away()
    broken_pot_lid.use()
    print("No output here at use()")
    
    #

    attack_potion = Potion.from_ability("atk potion tmp", owner='Beleg', type= "attack")
    print("potion created")
    attack_potion.use()
    print("potion used")
    attack_potion.use()
    # test_atk_pot = Potion.from_ability("atk potion tmp", type= "attack")
    # test_stew = Potion.from_ability("Grand Pot", "grand", "Beleg")
    
    
    print(isinstance(long_bow, Item))
    print(isinstance(broken_pot_lid, Shield))
    print(isinstance(attack_potion, Weapon))
    
    
    print("Test longbows increased damage")
    long_bow.use()
    