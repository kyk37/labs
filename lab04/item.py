

class Item:
    VALID_RARITIES =  {"common", "uncommon", "epic", "legendary"}
    ALL_ITEMS = [] # list of all items ever created (Note no items are removed from this list)

    def __init__(self, name, owner='', rarity="common", description = ""):
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
        #Returns everything about the item class
        return f"{self.name} a {self.rarity} item owned by {self._ownership}: {self.description}"