from item import Item
from threading import Timer

class Shield(Item):
    VALID_SHIELDTYPE = {"small shield", " round shield", "shield", "crown shield", "buckler", "large shield",
                        "kite shield", "tower shield", "buckler", "wooden shield", "square shield"}

    TIMER = None
    BONUS = False
    DEFENSE_BUFF = 0
    def __init__(self, name, defense, broken=False, rarity='Common', shield_type = "shield", description = ""):
        super().__init__(name, rarity=rarity, description=description) 
        '''
            Create a shield instance
            Inputs:
                name: what is the shield's name
                defense: how much defensive stat does this item have
                broken: True/False. Is this item broken?
                rarity: How rare is this shield "Common", "Uncommon", "Epic", "Legendary"
                shield_type: What kind of shield is this?
                description: About shield/description
        '''
        self.defense = defense
        self.shield_type = shield_type
        self.broken = broken
        self.active = False
        self.defense_modifier = 1.10 if rarity == "Legendary" else 1.0
        self.broken_modifier = 0.5 if broken else 1.0
        self.potion_name = ""


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

    def throw_away(self):
        self.active = False
        self.set_ownership("")
        print(f"{self.name} is thrown away")

    def use(self):
        # Use shield if it has an owner
        if self.active and self.get_ownership() != "":
            defense_power = (self.defense + Shield.DEFENSE_BUFF) * self.defense_modifier * self.broken_modifier
            defense = self.COLORS.get("defense", self.COLORS["reset"])
            print(f"{self.name} is used, blocking {defense}{defense_power:0.2f}{self.COLORS["reset"]} damage")

    def increase_defense_temporarily(self, pot_name, amount, duration):
        # create a timer for the potion
        if self.TIMER is not None:
            self.TIMER.cancel()
            self.TIMER = None

        defense = self.COLORS.get("defense", self.COLORS["reset"])
        print(f"{defense}Defense boost applied{self.COLORS["reset"]}")
        self.potion_name = pot_name
        Shield.DEFENSE_BUFF = amount
        Shield.TIMER = Timer(duration, self.reset_defense, [amount])
        Shield.TIMER.start()

    def reset_defense(self, amount):
        # reset the timer, and remove the buff
        print(f"{self.potion_name} has worn off!")
        Shield.DEFENSE_BUFF -= amount
        self.potion_name = ""
        Shield.TIMER.cancel()
        Shield.TIMER = None
    
    def get_equipped(self):
        return self.active

    def __str__(self):
        """Override __str__ """
        base_str = super().__str__()
        defense = self.COLORS.get("defense", self.COLORS["reset"])
        type = self.COLORS.get("ownership", self.COLORS['reset'])
        if self.broken == True:
            broken = "Broken"
        else:
            broken = "Good Condition"
        
        shield_details =  f"{base_str}\nStatus: {broken}\n🛡️ {type}Type:{self.COLORS["reset"]} {self.shield_type} | Defense: {defense}{self.defense:0.2f}{self.COLORS["reset"]}\n"
        return shield_details


    def to_json(self):
        '''Returns an JSON-encodable object with the classes information and all items stored inside.
                Item class Data:
                "class" : "Item", 
                "name": "item name", 
                "owner": "item_owner", 
                "rarity":"rarity_level", 
                "description":"item_description" 

                Shield Class Data:
                "defense": "Defense stat amount",
                "shield_type": "Type of shield", 
                "broken":"Is the shield in a broken state",
                "active": self.active
            }  
            All other items get created and calculated from these items
        '''
        json_data = super().to_json()
        json_data.update({
            "defense": self.defense,
            "broken": self.broken,
            "shield_type": self.shield_type,
            "active": self.active 
        })
        return json_data
    
    @classmethod
    def from_json(cls, json_data):
        """Creates new instances using the data from JSON strings."""
        import json
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        # Extract Items
        name = data.get("name")
        defense = data.get("defense",0)
        broken = data.get("broken", False)
        rarity = data.get("rarity","Common")
        shield_type = data.get("shield_type", "")
        description = data.get("description", "")
        owner = data.get("owner", "")
        active = data.get("active", False)

        # Create Instance
        shield = cls(
            name=name, 
            defense=defense, 
            broken=broken, 
            rarity=rarity,
            shield_type = shield_type,
            description = description,
            )

        # Set ownership and equip state
        if owner:
            shield.set_ownership(owner)
        shield.active = active
        return shield