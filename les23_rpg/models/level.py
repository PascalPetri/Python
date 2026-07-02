"""
Level class - Representeert een locatie/level in het spel
"""

from typing import List, Dict, Optional
from models.enemy import Enemy
from models.item import Item

class Level:
    """Klasse voor levels/locaties in de game"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enemies: List[Enemy] = []
        self.items: List[Item] = []
        self.exits: Dict[str, str] = {}  # richting -> level_name
        self.is_visited = False
    
    def add_enemy(self, enemy: Enemy) -> None:
        """Voeg een vijand toe aan het level"""
        self.enemies.append(enemy)
    
    def add_item(self, item: Item) -> None:
        """Voeg een item toe aan het level"""
        self.items.append(item)
    
    def add_exit(self, direction: str, level_name: str) -> None:
        """Voeg een uitgang toe naar een ander level"""
        self.exits[direction.lower()] = level_name
    
    def is_cleared(self) -> bool:
        """Check of alle vijanden in dit level verslagen zijn"""
        return all(not enemy.is_alive() for enemy in self.enemies) if self.enemies else True
    
    def get_enemies(self) -> List[Enemy]:
        """Geef alle levende vijanden"""
        return [e for e in self.enemies if e.is_alive()]
    
    def remove_item(self, item_name: str) -> Optional[Item]:
        """Verwijder en return een item uit het level"""
        for i, item in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None
    
    def get_exit(self, direction: str) -> Optional[str]:
        """Geef de level naam voor een richting"""
        return self.exits.get(direction.lower())
    
    def get_available_exits(self) -> List[str]:
        """Geef alle beschikbare uitgangen"""
        return list(self.exits.keys())
    
    def get_status(self) -> str:
        """Geef een status string voor weergave"""
        enemy_count = len([e for e in self.enemies if e.is_alive()])
        item_count = len(self.items)
        
        status = f"""
📍 {self.name}
📝 {self.description}
⚔️ Vijanden: {enemy_count} over
📦 Items: {item_count} beschikbaar
🚪 Uitgangen: {', '.join(self.get_available_exits()) or 'geen'}
"""
        return status
    
    def __str__(self) -> str:
        return f"{self.name} - {self.description[:50]}..."