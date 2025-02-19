import threading

class Item:
    VALID_RARITIES =  {"common", "uncommon", "epic", "legendary"}
    def __init__(self, name, owner='', rarity="common", description = ""):
        if name == "":
            raise ValueError(f"Invalid name: {self.name}. Cannot be blank")
        self.name = name
        self.description = description
        if rarity not in self.VALID_RARITIES:
            raise ValueError(f"Invalid rarity: {rarity}. Must be one of {self.VALID_RARITIES}")
        self.rarity = rarity
        self._ownership = owner
        
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
    
    def get_description(self, description):
        return self.description
    
    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"
    