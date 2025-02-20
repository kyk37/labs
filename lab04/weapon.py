from item import Item
from threading import Timer

class Weapon(Item):
    # List is not all inclusive. Too many RPG weapons exist in RPG games x_x
    VALID_WEAPONTYPES = {"bow", "crossbow", "sword", "dagger", "axe", "flail", "polearm", "sling", "stave", "claw",
                          "mace", "spear", "battle axe", "scimitar", "scythe", "wand", "staff", "broadsword", "longsword",
                          "rapier", "katana", "halberd", "morningstar", "whip", "glaive", "warhammer", "trident", "chakram", "saber",
                          "gladius", "khopesh", "cutlass", "claymore", "shortsword", "machete", "club", "spiked club", "hammer", "hatchet",
                         "longspear", "sickle", "brandistock","tekkokagi", "hand crossbow", "repeating crossbow", "short bow", "long bow", "composite bow",
                         "dart", "harpoon", "glaive", "spellbook"}
    _instance = None
    def __init__(self, name, rarity, damage, weapon_type, description):
        super().__init__(name, rarity=rarity, description=description)
        '''
            Creates a weapon instance
            Inputs:
                name: came of the weapon
                rarity: How rare the item is "common", "uncommon", "epic", "legendary"
                damage: How much damage does the weapon do
                weapon_type: What kind of weapon? see "VALID_WEAPONTYPES"
                description: Weapon description/about weapon
        '''
        self.damage = damage
        self.weapon_type = weapon_type
        self.active = False
        self.potion_name = ""
        self.timer = None
        # Common, uncomin, epic = 1.0 | legendary = 1.15
        self.attack_modifier = 1.15 if rarity == "legendary" else 1.0

    def equip(self):
        self.active = True
        owner = self.get_ownership()
        if self.active:
            print(f"{self.name} is equipped by {owner}")

    def unequip(self):
        self.active = False
        print(f"{self.name} is unequipped by {self.get_ownership()}")

    def use(self) -> str:
        if self.get_ownership() and self.active:
            damage_dealt = self.damage * self.attack_modifier
            print(f"{self.name} is used, dealing {damage_dealt} damage")
        elif self._ownership and self.active == False:
            pass
            #print(f"No weapon equipped!")
        
    def increase_damage_temporarily(self,pot_name, amount, duration):
        if self.timer is not None:
            self.timer.cancel()
        self.potion_name = pot_name
        self.damage += amount
        self.timer = Timer(duration, self.reset_damage, [amount])
        self.timer.start()

    def reset_damage(self, amount):
        print(f"{self.potion_name} has worn off!")
        self.damage -= amount
        self.potion_name = ""
        self.timer.cancel()
    
    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"