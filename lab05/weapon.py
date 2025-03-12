from item import Item
from threading import Timer

class Weapon(Item):
    # List is not all inclusive. Too many RPG weapons exist in RPG games x_x
    # Later on upon revision of different weapon types, utilize ABC, and abstract methodology
    WEAPON_CATEGORIES = {
        "single-handed": {
            "sword", "dagger", "axe", "mace", "scimitar", "rapier", "whip", "saber",  "hammer", "wand", "claw",
            "gladius", "khopesh", "cutlass", "shortsword", "machete", "club", "spiked club", "hatchet", "sickle", "tekkokagi"
        },
        "double-handed": {
            "broadsword", "longsword", "battle axe", "halberd", "morningstar", "warhammer", "claymore", "brandistock", "staff", "stave"
        },
        "pike": {
            "spear", "longspear", "trident", "harpoon", "glaive", "pike"
        },
        "ranged": {
            "bow", "crossbow", "hand crossbow", "repeating crossbow", "short bow", "long bow", "composite bow", 
            "dart", "chakram", "sling"
        }, 
    }
    TIMER = None
    BONUS = False
    BONUS_DAMAGE = 0
    
    def __init__(self, name, rarity, damage, weapon_type, description):
        super().__init__(name, rarity=rarity, description=description)
        '''
            Creates a weapon instance
            Inputs:
                name: came of the weapon
                rarity: How rare the item is "Common", "Uncommon", "Epic", "Legendary"
                damage: How much damage does the weapon do
                weapon_type: What kind of weapon? see "VALID_WEAPONS"
                description: Weapon description/about weapon
        '''
        self.damage = damage
        self.weapon_type = self.assign_weapontype(weapon_type)
        self.active = False
        self.potion_name = ""


        # Common, uncomin, epic = 1.0 | legendary = 1.15
        self.attack_modifier = 1.15 if rarity == "Legendary" else 1.0

    def assign_weapontype(self, name):
        """Assigns the correct weapon type based on the weapon name."""
        name = name.lower()  # Ensure case insensitivity
        for weapon_type, weapons in Weapon.WEAPON_CATEGORIES.items():
            if name in (weapon.lower() for weapon in weapons):  # Ensure case insensitivity for weapon names
                return weapon_type  # Return the category it belongs to
        return "unknown"  # Default if weapon isn't found

    def get_equipped(self):
        return self.active
    
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
            self.attack_move()
            damage_dealt = (self.damage + self.BONUS_DAMAGE) * self.attack_modifier
            damage = self.COLORS.get("damage", self.COLORS["reset"])
            print(f"{self.name} is used, dealing {damage}{damage_dealt:0.2f}{self.COLORS["reset"]} damage")
        elif self._ownership and self.active == False:
            pass
            #print(f"No weapon equipped!")

    # Future implentation        
    # def attack_move(self):
    #     ''' Overwritten by subclasses'''
    #     raise NotImplementedError("Each weapon has it's own special attack")
    
    def attack_move(self):
        if self.weapon_type == "single-handed":
            print(self._slash())
        elif self.weapon_type == "double-handed":
            print(self._spin())
        elif self.weapon_type == "pike":
            print(self._thrust())
        elif self.weapon_type == "ranged":
            print(self._shoot())
        else:
            raise ValueError("Not a proper weapon_type: {self.weapon_type}")

    def _slash(self):
        return f"{self.get_ownership()} slashes swiftly with {self.name}!"

    def _spin(self):
        return f"{self.get_ownership()} spins mightily and strikes with {self.name}!"

    def _thrust(self):
        return f"{self.get_ownership()} thrusts forward with {self.name}, piercing enemies!"

    def _shoot(self):
        return f"{self.get_ownership()} takes aim and releases a volley with {self.name}!"

    def increase_damage_temporarily(self,pot_name, amount, duration):
        '''Adds the bonus damage, and timer to all weapons'''
        if self.TIMER is not None:
            self.TIMER.cancel()
            self.TIMER = None
        damage = self.COLORS.get("damage", self.COLORS["reset"])
        print(f"{damage}Damage boost applied{self.COLORS["reset"]}")
        self.potion_name = pot_name
        Weapon.BONUS_DAMAGE += amount
        Weapon.TIMER = Timer(duration, self.reset_damage, [amount])
        Weapon.TIMER.start()
        Weapon.BONUS = True

    def reset_damage(self, amount):
        '''Sets bonus damage to 0 and resets timers'''
        print(f"{self.potion_name} has worn off!")
        Weapon.BONUS_DAMAGE -= amount
        self.potion_name = ""
        Weapon.TIMER.cancel()
        Weapon.TIMER = None

    def __str__(self):
        """Override __str__"""
        base_str = super().__str__()
        damage = self.COLORS.get("damage", self.COLORS["reset"])
        type = self.COLORS.get("ownership", self.COLORS['reset'])
        if self.weapon_type == "single-handed":
            weapon_details =  f"{base_str}\n⚔️  {type}Type:{self.COLORS["reset"]} {self.weapon_type} | Damage: {damage}{self.damage:0.2f}{self.COLORS["reset"]}\n"
        elif self.weapon_type == "double-handed":
            weapon_details = f"{base_str}\n🗡️ {type}Type:{self.COLORS["reset"]} {self.weapon_type} | Damage: {damage}{self.damage:0.2f}{self.COLORS["reset"]}\n"
        elif self.weapon_type == "pike":
            weapon_details = f"{base_str}\n🔱 {type}Type:{self.COLORS["reset"]} {self.weapon_type} | Damage: {damage}{self.damage:0.2f}{self.COLORS["reset"]}\n"
        elif self.weapon_type == "ranged":
            weapon_details = f"{base_str}\n🏹 {type}Type:{self.COLORS["reset"]} {self.weapon_type} | Damage: {damage}{self.damage:0.2f}{self.COLORS["reset"]}\n"
        else:
            raise Exception(f"Invalid Weapon Type: {self.weapon_type}\n")
        return weapon_details


###
#   For future implentation of classes
#   Just make "attack_move(), and _spin(), _slash(), _thrust(), _shoot() functions"
#   Mybe later on edit the below with colored text
###
# class singlehandedWeapon(Weapon):
#     def __init__(self, name, rarity, damage, description, owner=""):
#         super().__init__(name, rarity, damage, description, owner)
#         self.weapon_type = "single-handed"

#     def attack_move(self):
#         return f"{self.get_ownership()} slashes swiftly with {self.name}!"


# class doublehandedWeapon(Weapon):
#     def __init__(self, name, rarity, damage, description, owner=""):
#         super().__init__(name, rarity, damage, description, owner)
#         self.weapon_type = "double-handed"

#     def attack_move(self):
#         return f"{self.get_ownership()} spins mightily and strikes with {self.name}!"


# class pikeWeapon(Weapon):
#     def __init__(self, name, rarity, damage, description, owner=""):
#         super().__init__(name, rarity, damage, description, owner)
#         self.weapon_type = "pike"

#     def attack_move(self):
#         return f"{self.get_ownership()} thrusts forward with {self.name}, piercing enemies!"


# class rangedWeapon(Weapon):
#     def __init__(self, name, rarity, damage, description, owner=""):
#         super().__init__(name, rarity, damage, description, owner)
#         self.weapon_type = "ranged"

#     def attack_move(self):
#         return f"{self.get_ownership()} takes aim and shoots with {self.name}!"