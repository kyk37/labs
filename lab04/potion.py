from item import Item
from weapon import Weapon
from shield import Shield

class Potion(Item):
    VALID_POTIONTYPES = {"attack", "defense", "hp"}
    def __init__(self, name, type, rarity="common", owner="", description=""):
        super().__init__(name, rarity=rarity, owner=owner, description=description)
        self.potion_type = type
        self.used_flag = False #simulate destroyed item
        self.amount = 50
        self.duration = 30
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
        #find weapon.
        for item in globals().values():
            print(item, Weapon)
            if isinstance(item, Weapon):# == False: ## Fails to enter this when True
                print("inside Instance") 
                for item in item:
                    Weapon.increase_damage_temporarily(50, 30)
                
    @classmethod
    def from_ability(cls, name:str,  type:str, owner:str="", rarity:str="common", description:str=""):
        if owner == None or owner == "":
            raise ValueError(f"Invalid Owner, potions don't just appear out of thin air Mr. Potter")
        else:
            return cls(name, type, rarity, owner, description)