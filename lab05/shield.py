from item import Item
from threading import Timer

class Shield(Item):
    VALID_SHIELDTYPE = {"small shield", " round shield", "shield", "crown shield", "buckler", "large shield",
                        "kite shield", "tower shield", "buckler", "wooden shield"}

    def __init__(self, name, defense, broken=False, rarity='common', shield_type = "shield", description = ""):
        super().__init__(name, rarity=rarity, description=description) 
        '''
            Create a shield instance
            Inputs:
                name: what is the shield's name
                defense: how much defensive stat does this item have
                broken: True/False. Is this item broken?
                rarity: How rare is this shield "common", "uncommon", "epic", "legendary"
                shield_type: What kind of shield is this?
                description: About shield/description
        '''
        self.defense = defense
        self.shield_type = shield_type
        self.broken = broken
        self.active = False
        self.defense_modifier = 1.10 if rarity == "legendary" else 1.0
        self.broken_modifier = 0.5 if broken else 1.0
        self.potion_name = ""
        self.timer = None

    def equip(self):
        # equip shield
        self.active = True
        owner = self.get_ownership()
        print(f"{self.name} is equipped by {owner}")
    
    def unequip(self):
        # unequip shield
        self.active = False
        owner = self.get_ownership()
        print(f"{self.name} is unequipped by {owner}")

    # def throw_away(self):
    #     self.active = False
    #     self.set_ownership("")
    #     print(f"{self.name} is thrown away")

    
    def use(self):
        # Use shield if it has an owner
        if self.active and self.get_ownership() != "":
            defense_power = self.defense * self.defense_modifier * self.broken_modifier
            print(f"{self.name} is used, blocking {defense_power} damage")

    def increase_defense_temporarily(self, pot_name, amount, duration):
        # create a timer for the potion
        if self.timer is not None:
            self.timer.cancel()
        self.potion_name = pot_name
        self.defense += amount
        self.timer = Timer(duration, self.reset_defense, [amount])
        self.timer.start()

    def reset_defense(self, amount):
        # reset the timer, and remove the buff
        print(f"{self.potion_name} has worn off!")
        self.defense -= amount
        self.potion_name = ""
        self.timer.cancel()