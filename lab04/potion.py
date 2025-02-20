from item import Item
from weapon import Weapon
from shield import Shield

class Potion(Item):
    VALID_POTIONTYPES = {"attack", "defense", "hp"}
    def __init__(self, name, type, amount, duration, rarity="common", owner="", description=""):
        super().__init__(name, rarity=rarity, owner=owner, description=description)
        '''
            Creates a potion instance
            Input:
                name: Potion's Nmae
                type: What kind of potion (attack/defense/hp)
                amount: How much does it boost; ie.. 50hp, 30 damage
                duration: How long the potion lasts for
                rarity: How common the potion is "common", "uncommon", "epic", "legendary"
                owner: Who the potion is owned by
                description: What does this item do/about item
        '''
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
        # Returns potion type
        return self.potion_type

    def use(self):
        # Use the potion and apply boosts

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
        # Boost the weapon damage for specified amount
        for item in Item.ALL_ITEMS:
            if isinstance(item, Weapon) and item._ownership == self.get_ownership():
                item.increase_damage_temporarily(self.name, amount = self.amount, duration= self.duration)

    def apply_defense_boost(self):
        # Boost defense for specified amount
        for item in Item.ALL_ITEMS:
            if isinstance(item, Shield) and item._ownership == self.get_ownership():
                item.increase_defense_temporarily(self.name, amount = self.amount, duration= self.duration)

    def apply_healing(self):
        # Simulate player getting healed
        print(f"{self.get_ownership()} healed for {self.amount}")
                
    @classmethod
    def from_ability(cls, name:str,  type:str, owner:str="", description:str=""):
        # All user created potions are +50 stat, 30seconds duration and commoon rarity
        if owner == None or owner == "":
            raise ValueError(f"Invalid Owner, potions don't just appear out of thin air Mr. Potter")
        else:
            amount = 50
            duration = 30
            rarity = "common"
            return cls(name, type, amount, duration, rarity, owner, description)