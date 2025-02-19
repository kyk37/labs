
import threading
import time

class Item:
    VALID_RARITIES =  {"common", "uncommon", "epic", "legendary"}
    ALL_ITEMS = [] #To track created items

    def __init__(self, name, owner='', rarity="common", description = ""):
        if name == "":
            raise ValueError(f"Invalid name: {self.name}. Cannot be blank")

        if rarity not in self.VALID_RARITIES:
            raise ValueError(f"Invalid rarity: {rarity}. Must be one of {self.VALID_RARITIES}")
        
        self.name = name
        self.description = description
        self.rarity = rarity
        self._ownership = owner

        #Trackevery item.
        Item.ALL_ITEMS.append(self)

    def pick_up(self, character:str) -> str:
        self._ownership = character
        print(f"{self.name} is now owned by {character}")
    
    def throw_away(self) -> str:
        self._ownership = ""
        print(f"{self.name} is thrown away")
    
    def use(self) -> str:
        if self._ownership:
            print(f"{self.name} is used.")
    
    def set_ownership(self, owner):
        self._ownership = owner
        
    def get_ownership(self):
        return self._ownership
    
    def set_description(self, description):
        self.description = description
    
    def get_description(self):
        return self.description
    
    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"
    
class Potion(Item):
    VALID_POTIONTYPES = {"attack", "defense", "hp"}
    def __init__(self, name, type, amount, duration, rarity="common", owner="", description=""):
        super().__init__(name, rarity=rarity, owner=owner, description=description)
        self.potion_type = type
        self.used_flag = False #simulate destroyed item
        self.amount = amount
        self.duration = duration
        if self.potion_type == "attack":
            self.set_description(f"{rarity} Attack potion +{self.amount} damage")
        elif self.potion_type == "defense":
            self.set_description(f"{rarity} Defense Potion +{self.amount} defense")
        elif self.potion_type == "hp":
            self.set_description(f"{rarity} Health potion heals +{self.amount} HP")
        else:
            raise ValueError("Invalid potion type, you must of made a stew")
            
    def get_type(self):
        return self.potion_type
    
    def use(self):
        owner = self.get_ownership()
        print(f"Owner: {owner}")
        if owner and self.used_flag == False:
            print(f"{owner} used {self.name}, and {self.potion_type} increased {self.amount} for {self.duration}s ")
            if self.potion_type == "attack":
                self.apply_weapon_boost()
            elif self.potion_type == "defense":
                self.apply_defense_boost()
            else:
                self.apply_healing()
            self.used_flag = True
    
    def apply_weapon_boost(self):
        print("Applying weapon boost")
        for item in Item.ALL_ITEMS:
            if isinstance(item, Weapon) and item.active:
                item.increase_damage_temporarily(amount = 50, duration= 3)
                
    @classmethod
    def from_ability(cls, name:str,  type:str,amount =50, duration=30 ,owner:str="", rarity:str="common", description:str=""):
        if owner == None or owner == "":
            raise ValueError(f"Invalid Owner, potions don't just appear out of thin air Mr. Potter")
        else:
            return cls(name, type, amount, duration, rarity, owner, description)

            
class Weapon(Item):
    # List is not all inclusive. Too many RPG weapons exist in RPG games x_x
    VALID_WEAPONTYPES = {"bow", "crossbow", "sword", "dagger", "axe", "flail", "polearm", "sling", "stave", "claw",
                          "mace", "spear", "battle axe", "scimitar", "scythe", "wand", "staff", "broadsword", "longsword",
                          "rapier", "katana", "halberd", "morningstar", "whip", "glaive", "warhammer", "trident", "chakram", "saber",
                          "gladius", "khopesh", "cutlass", "claymore", "shortsword", "machete", "club", "spiked club", "hammer", "hatchet",
                         "longspear", "sickle", "brandistock","tekkokagi", "hand crossbow", "repeating crossbow", "short bow", "long bow", "composite bow",
                         "dart", "harpoon", "glaive"}
    _instance = None
    def __init__(self, name, rarity, damage, weapon_type, description):
        super().__init__(name, rarity=rarity, description=description)
        self.damage = damage
        self.weapon_type = weapon_type
        self.active = False

        # Common, uncomin, epic = 1.0 | legendary = 1.15
        self.attack_modifier = 1.15 if rarity == "legendary" else 1.0

    def equip(self):
        self.active = True
        owner = self.get_ownership()
        if self.active:
            print(f"{self.name} is equipped by {owner}")

        
    def use(self) -> str:
        if self._ownership:
            damage_dealt = self.damage * self.attack_modifier
            print(f"{self.name} is used, dealing {damage_dealt} damage")

        
    def increase_damage_temporarily(self, amount, duration):
        self.damage += amount
        timer = threading.Timer(duration, self.reset_damage, [amount])
        timer.start()

    def reset_damage(self, amount):
        self.damage -= amount
    
    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"
    

class Shield(Item):
    VALID_SHIELDTYPE = {"small shield", " round shield", "shield", "crown shield", "buckler", "large shield",
                        "kite shield", "tower shield", "buckler"}

    def __init__(self, name, defense, broken=False, rarity='common', shield_type = "shield", description = ""):
        super().__init__(name, rarity=rarity, description=description)
        self.defense = defense
        self.shield_type = shield_type
        self.broken = broken
        self.active = False
        self.defense_modifier = 1.10 if rarity == "legendary" else 1.0
        self.broken_modifier = 0.5 if broken else 1.0
    
    def equip(self):
        self.active = True
        owner = self.get_ownership()
        print(f"{self.name} is equipped by {owner}")
    
    def unequip(self):
        self.active = False
        owner = self.get_ownership()
        print(f"{self.name} is unequipped by {owner}")

    def throw_away(self):
        self.active = False
        self.set_ownership("")
        print(f"{self.name} is thrown away")
    
    def use(self):
        if self.active and self.get_ownership() != "":
            defense_power = self.defense * self.defense_modifier * self.broken_modifier
            print(f"{self.name} is used, blocking {defense_power} damage")

    def increase_damage_temporarily(self, amount, duration):
        self.defense += amount
        timer = threading.Timer(duration, self.reset_defense, [amount])
        timer.start()

    def reset_defense(self, amount):
        self.defense -= amount
    

if __name__ == "__main__":
    long_bow = Weapon("Bethronding", "legendary", 5000, "bow", "Good for attacking enemies at a distance!")
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
    
    
    print("Test if longbows damage increased")
    long_bow.use()
    time.sleep(5)
    long_bow.use()