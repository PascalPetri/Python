"""
Player class - Representeert de speler in het RPG
"""

from typing import List, Optional
from models.item import Item

class Player:
    """Klasse voor de speler"""
    
    def __init__(self, name: str, hp: int = 100, attack_power: int = 10):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack_power
        self.inventory: List[Item] = []
        self.level = 1
        self.experience = 0
    
    def is_alive(self) -> bool:
        """Check of de speler nog leeft"""
        return self.hp > 0
    
    def take_damage(self, amount: int) -> int:
        """
        Verminder HP met amount (niet onder 0)
        Returns: Werkelijke schade
        """
        actual_damage = min(amount, self.hp)
        self.hp -= actual_damage
        if self.hp < 0:
            self.hp = 0
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """
        Herstel HP (niet boven max_hp)
        Returns: Werkelijke genezing
        """
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        return self.hp - old_hp
    
    def attack(self, target) -> int:
        """
        Val een vijand aan
        Returns: Schade die is gedaan
        """
        if not target.is_alive():
            return 0
        
        import random
        damage = int(self.attack_power * (0.8 + 0.4 * random.random()))
        actual_damage = target.take_damage(damage)
        return actual_damage
    
    def add_item(self, item: Item) -> None:
        """Voeg item toe aan inventory"""
        self.inventory.append(item)
    
    def remove_item(self, item_name: str) -> Optional[Item]:
        """Verwijder en return een item uit inventory"""
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower():
                return self.inventory.pop(i)
        return None
    
    def use_item(self, item_name: str) -> str:
        """
        Gebruik een item uit inventory
        Returns: Resultaat van het gebruik
        """
        item = self.remove_item(item_name)
        if item:
            result = item.apply(self)
            return result
        return f"Je hebt geen {item_name} in je inventory."
    
    def get_inventory_names(self) -> List[str]:
        """Geef lijst van item namen in inventory"""
        return [item.name for item in self.inventory]
    
    def has_item(self, item_name: str) -> bool:
        """Check of een item in inventory zit"""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)
    
    def __str__(self) -> str:
        return f"{self.name} (HP: {self.hp}/{self.max_hp}, ATK: {self.attack_power})"
    
    def get_status(self) -> str:
        """Geef een status string voor weergave"""
        return f"""
╔══════════════════════════════════╗
║ {self.name:^30} ║
║ HP: {self.hp:>3}/{self.max_hp:<3}  ATK: {self.attack_power:<3} ║
║ Level: {self.level:<3}  XP: {self.experience:<3} ║
║ Items: {len(self.inventory)} ║
╚══════════════════════════════════╝
"""