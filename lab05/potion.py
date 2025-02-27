from item import Item
from weapon import Weapon
from shield import Shield

class Potion(Item):
    VALID_POTIONTYPES = {"attack", "defense", "hp", "empty_vial"}
    def __init__(self, name, type, amount, duration, rarity="Common", owner="", description=""):
        super().__init__(name, rarity=rarity, owner=owner, description=description)
        '''
            Creates a potion instance
            Input:
                name: Potion's Nmae
                type: What kind of potion (attack/defense/hp)
                amount: How much does it boost; ie.. 50hp, 30 damage
                duration: How long the potion lasts for
                rarity: How common the potion is "Common", "Uncommon", "Epic", "Legendary"
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
        inventory = self.get_inventory()
        if owner and self.used_flag == False:
            if self.potion_type == "attack":
                print(f"{owner} used {self.name}, and {self.potion_type} increased {self.amount} for {self.duration}s ")
                self.apply_weapon_boost(inventory)
                self.name = self.name + " used"
            elif self.potion_type == "defense":
                print(f"{owner} used {self.name}, and {self.potion_type} increased {self.amount} for {self.duration}s ")
                self.apply_defense_boost(inventory)
                self.name = self.name + " used"
            else:
                self.apply_healing()
                self.name = self.name + " used"
            self.used_flag = True
        else:
            print(f"{self.name} has already been used and is empty!")

    def get_inventory(self):
        """Finds and returns the inventory of the potion's owner."""
        from inventory import Inventory
        for inventory in Inventory.USER_INVENTORY:  # Assuming a global registry of inventories
            if inventory.owner == self.get_ownership():
                return inventory
        return None  # No matching inventory found
    
    def apply_weapon_boost(self, inventory):
        # Boost the weapon damage for specified amount
        weapon = next(
            (item for item in inventory.items if isinstance(item, Weapon) and item.get_ownership() == self.get_ownership()), 
            None)
        if weapon:
            weapon.increase_damage_temporarily(self.name, amount = self.amount, duration= self.duration)
        else:
            print("No matching weapon found to apply the boost.")

    def apply_defense_boost(self, inventory):
        # Boost defense for specified amount
        shield = next(
            (item for item in inventory.items if isinstance(item, Shield) and item.get_ownership() == self.get_ownership()), 
            None)
        if shield:
            shield.increase_defense_temporarily(self.name, amount = self.amount, duration= self.duration)
        else:
            print("No matching shield found to apply the boost.")

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
            rarity = "Common"
            return cls(name, type, amount, duration, rarity, owner, description)
        
    def __str__(self):
        """Override item __str__ """
        base_str = super().__str__()
        amount = self.COLORS.get("defense", self.COLORS["reset"])
        type = self.COLORS.get("ownership", self.COLORS['reset'])
        potion_details =  f"{base_str}\n🧪{type}Type:{self.COLORS["reset"]} {self.potion_type} | Amount: {amount}{self.amount:0.2f}{self.COLORS["reset"]}\n"
        return potion_details