from item import Item

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
    
    def throw_away(self):
        self.active = False
        self.set_ownership("")
        print(f"{self.name} is thrown away")
        
    
    def use(self):
        if self.active and self.get_ownership() != "":
            defense_power = self.defense * self.defense_modifier * self.broken_modifier
            print(f"{self.name} is used, blocking {defense_power} damage")
            