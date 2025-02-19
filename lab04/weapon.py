from item import Item
import threading

class Weapon(Item):
    # List is not all inclusive. Too many RPG weapons exist in RPG games x_x
    VALID_WEAPONTYPES = {"bow", "crossbow", "sword", "dagger", "axe", "flail", "polearm", "sling", "stave", "claw",
                          "mace", "spear", "battle axe", "scimitar", "scythe", "wand", "staff", "broadsword", "longsword",
                          "rapier", "katana", "halberd", "morningstar", "whip", "glaive", "warhammer", "trident", "chakram", "saber",
                          "gladius", "khopesh", "cutlass", "claymore", "shortsword", "machete", "club", "spiked club", "hammer", "hatchet",
                         "longspear", "sickle", "brandistock","tekkokagi", "hand crossbow", "repeating crossbow", "short bow", "long bow", "composite bow",
                         "dart", "harpoon", "glaive"}
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
        else:
            return ""
        
    def increase_damage_temporarily(self, amount, duration):
        self.damage += amount
        timer = threading.Timer(duration, self.reset_damage, [amount])
        timer.start()
        
    def reset_damage(self, amount):
        self.damage -= amount
    
    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"
    