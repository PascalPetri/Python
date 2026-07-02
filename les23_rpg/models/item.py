"""
Item class - Representeert items die spelers kunnen vinden en gebruiken
"""

from typing import Optional

class Item:
    """Klasse voor items in de game"""
    
    def __init__(self, name: str, item_type: str, value: int, description: str = ""):
        """
        Args:
            name: Naam van het item
            item_type: "heal", "attack_boost", "key", "special"
            value: Hoeveelheid heal/boost of effect waarde
            description: Beschrijving van het item
        """
        self.name = name
        self.type = item_type
        self.value = value
        self.description = description or f"Een {name}"
    
    def apply(self, player) -> str:
        """
        Pas het item toe op een speler
        Returns: Beschrijving van wat er gebeurde
        """
        if self.type == "heal":
            healed = player.heal(self.value)
            return f"Je gebruikt {self.name} en herstelt {healed} HP!"
        
        elif self.type == "attack_boost":
            player.attack_power += self.value
            return f"Je gebruikt {self.name} en krijgt +{self.value} aanvalskracht!"
        
        elif self.type == "key":
            return f"Je hebt de {self.name}! Deze opent misschien een deur..."
        
        elif self.type == "special":
            if self.name.lower() == "magic scroll":
                return f"Je leest de {self.name} en voelt magische energie!"
            return f"Je gebruikt {self.name}, maar er gebeurt niets speciaals."
        
        return f"Je kunt {self.name} niet gebruiken."
    
    def __str__(self) -> str:
        return f"{self.name} ({self.type}) - {self.description}"
    
    def __repr__(self) -> str:
        return f"Item('{self.name}', '{self.type}', {self.value})"