"""
Enemy class - Representeert vijanden in het RPG
"""

import random

class Enemy:
    """Klasse voor vijanden"""
    
    def __init__(self, name: str, hp: int, attack_power: int, 
                 experience_value: int = 10, description: str = ""):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack_power
        self.experience_value = experience_value
        self.description = description or f"Een {name}"
        self.is_defeated = False
    
    def is_alive(self) -> bool:
        """Check of de vijand nog leeft"""
        return self.hp > 0 and not self.is_defeated
    
    def take_damage(self, amount: int) -> int:
        """Verminder HP met amount (niet onder 0)"""
        actual_damage = min(amount, self.hp)
        self.hp -= actual_damage
        if self.hp <= 0:
            self.hp = 0
            self.is_defeated = True
        return actual_damage
    
    def attack(self, player) -> int:
        """Val de speler aan"""
        if not player.is_alive():
            return 0
        
        import random
        damage = int(self.attack_power * (0.8 + 0.4 * random.random()))
        actual_damage = player.take_damage(damage)
        return actual_damage
    
    def __str__(self) -> str:
        status = "💀" if not self.is_alive() else "⚔️"
        return f"{status} {self.name} (HP: {self.hp}/{self.max_hp})"
    
    def get_status(self) -> str:
        """Geef een status string voor weergave"""
        return f"{self.name} [HP: {self.hp}/{self.max_hp}]"