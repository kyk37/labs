from colorama import Fore, Style, init
init(autoreset=True)  # Resets colors automatically

class Item:
    VALID_RARITIES =  {"Common", "Uncommon", "Epic", "Legendary"}
    ALL_ITEMS = [] # list of all items ever created (Note no items are removed from this list)
    COLORS = {
        "Common": "\033[0;37m",    # White
        "Uncommon": "\033[0;32m",  # Green
        "Epic": "\033[0;35m",      # Purple
        "Legendary": "\033[0;33m", # Yellow
        "ownership": "\033[0;34m",  #  Blue
        "defense": "\033[0;36m",   # Cyan
        "damage": "\033[0;31m",    # Red
        "reset": "\033[0m"         # Resets color
    }

    def __init__(self, name, owner='', rarity="Common", description = ""):
        '''
            Creates an item and adds it to the list of existing items
            Inputs:
                name: the Name of the item
                rarity: How rare the item is "common", "uncommon", "epic", "legendary"
                description: A short description of the item
                owner: Character who owns the item
        '''
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
        # Pick up the item
        self._ownership = character
        print(f"{self.name} is now owned by {character}")
    
    def throw_away(self) -> str:
        # throw the item out (still exists in list)
        self._ownership = ""
        print(f"{self.name} is thrown away")
    
    def use(self) -> str:
        # Use this item if it is own'ed by someone
        if self._ownership:
            print(f"{self.name} is used.")
    
    def set_ownership(self, owner):
        # Set the owner
        self._ownership = owner
        
    def get_ownership(self):
        # Return the owner
        return self._ownership
    
    def set_description(self, description):
        # Set the items description
        self.description = description
    
    def get_description(self):
        # Get the item description
        return self.description
    
    def __str__(self):
        '''Returns basic item information'''
        if self.rarity == "Legendary":
            rarity = Item.COLORS.get(self.rarity, Item.COLORS["reset"])
            ownership = Item.COLORS.get("ownership", Item.COLORS["reset"])
            return f"{self.name}\nRarity: {rarity}✨✨ {self.rarity} Item ✨✨{Item.COLORS["reset"]}\n{self.description} \n{ownership}Owned by:{Item.COLORS["reset"]} {self._ownership}"
        elif self.rarity =="Epic":
            rarity = Item.COLORS.get(self.rarity, Item.COLORS["reset"])
            ownership = Item.COLORS.get("ownership", Item.COLORS["reset"])
            return f"{rarity}✨ Epic Item ✨{Item.COLORS["reset"]}\n{self.name}\nRarity: {rarity}✨ {self.rarity} Item ✨{Item.COLORS["reset"]}\n{self.description} \n{ownership}Owned by:{Item.COLORS["reset"]} {self._ownership}"
        else:
            rarity = Item.COLORS.get(self.rarity, Item.COLORS["reset"])
            ownership = Item.COLORS.get("ownership", Item.COLORS["reset"])
            return f"{self.name}\nRarity: {rarity}{self.rarity} Item{Item.COLORS["reset"]}\n{self.description} \n{ownership}Owned by:{Item.COLORS["reset"]} {self._ownership}"
