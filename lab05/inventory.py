from weapon import Weapon
from shield import Shield
from potion import Potion

class Inventory:
    USER_INVENTORY = []
    def __init__(self, owner=None):
        # intialize variables
        self.name = "backpack"
        self.owner = owner
        self.items = []  # Stores all items
        Inventory.USER_INVENTORY.append(self)

    def add_item(self, item):
        """Adds an item to the inventory and updates its ownership."""
        if item not in self.items:
            self.items.append(item)
            item.set_ownership(self.owner)
            print(f"{item.name} has been added to {self.owner}'s backpack.")
        else:
            print(f"{item.name} is already in the backpack!")

    def drop_item(self, item):
        """Removes an item from the inventory and resets ownership."""
        if item in self.items:
            self.items.remove(item)
            item.set_ownership(None)  # Reset ownership when dropped
            print(f"{item.name} has been removed from {self.owner}'s backpack.")
        else:
            print(f"{item.name} is not in the backpack!")

    def view(self, type=None, item=None):
        """Displays individual items or a collection of items by type."""

        if item == None and type or type is None and item is None:
            # Convert string to class
            if isinstance(type, str):
                type_map = {
                    "weapon": Weapon,
                    "shield": Shield,
                    "potion": Potion,
                }
                type = type_map.get(type.lower(), None)
            if type: # Get a collection of items
                filtered_items = [item for item in self.items if isinstance(item, type)]
                if not filtered_items:
                    print(f"No items of type {type.__name__} in the backpack.")
                    return
                
                print(f"\n{self.owner}'s {type.__name__}s:")
                for idx,item in enumerate(filtered_items, start=1):
                    print(f"({idx}) {item}")  # This calls the __str__() method for each item
            else:
                print(f"\n{self.owner}'s Backpack Inventory:")
                if not self.items:
                    print("The backpack is empty.")
                for idx,item in enumerate(self.items, start=1):
                    print(f"({idx}) {item}")  # This ensures __str__() is called for each item
        else:
            print(item)

    def __iter__(self):
        """Allows iteration"""
        return iter(self.items)

    def __contains__(self, item):
        "Returns the items"
        return item in self.items

    def __str__(self):
        """Returns a summary of the inventory/bag"""
        return f"{self.owner}'s Inventory contains {len(self.items)} items."