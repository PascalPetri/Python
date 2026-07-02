"""
Game Engine - Beheert de game loop en alle game logica
"""

import sys
from typing import Dict, Optional, List
from models.player import Player
from models.enemy import Enemy
from models.item import Item
from models.level import Level

class Game:
    """Hoofd game engine"""
    
    def __init__(self, player: Player, start_level: str):
        self.player = player
        self.levels: Dict[str, Level] = {}
        self.current_level_name = start_level
        self.running = True
        self.turn_count = 0
        self.game_over = False
    
    def add_level(self, level: Level) -> None:
        """Voeg een level toe aan de game"""
        self.levels[level.name] = level
    
    def get_current_level(self) -> Level:
        """Geef het huidige level"""
        return self.levels[self.current_level_name]
    
    def show_status(self) -> None:
        """Toon de huidige status"""
        print("\n" + "="*60)
        print(self.player.get_status())
        print("\n" + self.get_current_level().get_status())
        print("="*60)
        
        if self.player.inventory:
            print("🎒 Inventory:", ", ".join([item.name for item in self.player.inventory]))
        else:
            print("🎒 Inventory: leeg")
        
        print("="*60)
    
    def show_menu(self) -> None:
        """Toon het actie menu"""
        print("\n📋 Acties:")
        print("  look        - Bekijk het level")
        print("  fight [n]   - Vecht tegen vijand n (1-{})".format(len(self.get_current_level().get_enemies())))
        print("  take [item] - Pak een item op")
        print("  use [item]  - Gebruik een item uit inventory")
        print("  go [dir]    - Ga naar een andere locatie")
        print("  inventory   - Bekijk je inventory")
        print("  status      - Toon status")
        print("  quit        - Stop het spel")
        print("-"*40)
    
    def handle_command(self, command: str) -> str:
        """
        Verwerk een command
        Returns: Resultaat string
        """
        if not command or not command.strip():
            return "Voer een commando in."
        
        parts = command.strip().lower().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == "quit":
            self.running = False
            return "Je verlaat het spel. Tot ziens!"
        
        if cmd in ["status", "s"]:
            self.show_status()
            return "Status getoond."
        
        if cmd in ["look", "l"]:
            return self._handle_look()
        
        if cmd in ["inventory", "inv", "i"]:
            return self._handle_inventory()
        
        if cmd in ["fight", "f", "attack", "a"]:
            return self._handle_fight(args)
        
        if cmd in ["take", "t", "pickup", "p"]:
            return self._handle_take(args)
        
        if cmd in ["use", "u"]:
            return self._handle_use(args)
        
        if cmd in ["go", "g", "move", "m"]:
            return self._handle_go(args)
        
        if cmd in ["help", "h", "?"]:
            return self._handle_help()
        
        return f"Onbekend commando: {cmd}. Typ 'help' voor alle commando's."
    
    def _handle_look(self) -> str:
        """Bekijk het huidige level"""
        level = self.get_current_level()
        result = f"\n📍 {level.name}\n"
        result += f"{level.description}\n\n"
        
        enemies = level.get_enemies()
        if enemies:
            result += "⚔️ Vijanden aanwezig:\n"
            for i, enemy in enumerate(enemies, 1):
                result += f"  {i}. {enemy.get_status()}\n"
        else:
            result += "✅ Geen vijanden hier.\n"
        
        if level.items:
            result += f"\n📦 Items hier: {', '.join([item.name for item in level.items])}\n"
        else:
            result += "\n📦 Geen items hier.\n"
        
        exits = level.get_available_exits()
        if exits:
            result += f"\n🚪 Uitgangen: {', '.join(exits)}\n"
        
        return result
    
    def _handle_inventory(self) -> str:
        """Bekijk inventory"""
        if not self.player.inventory:
            return "🎒 Je inventory is leeg."
        
        result = "🎒 Je inventory:\n"
        for i, item in enumerate(self.player.inventory, 1):
            result += f"  {i}. {item.name} ({item.type}) - {item.description}\n"
        return result
    
    def _handle_fight(self, args: List[str]) -> str:
        """Vecht tegen een vijand"""
        level = self.get_current_level()
        enemies = level.get_enemies()
        
        if not enemies:
            return "Er zijn geen vijanden om tegen te vechten."
        
        if not args:
            enemy = enemies[0]
        else:
            try:
                idx = int(args[0]) - 1
                if idx < 0 or idx >= len(enemies):
                    return f"Ongeldig nummer. Kies 1-{len(enemies)}."
                enemy = enemies[idx]
            except ValueError:
                return "Voer een geldig nummer in."
        
        damage = self.player.attack(enemy)
        result = f"💥 Je valt {enemy.name} aan en doet {damage} schade!\n"
        
        if not enemy.is_alive():
            result += f"🎉 {enemy.name} is verslagen!\n"
            self.player.experience += enemy.experience_value
            result += f"✨ Je krijgt {enemy.experience_value} XP!\n"
            
            if self.player.experience >= 50:
                self.player.level += 1
                self.player.max_hp += 20
                self.player.hp = self.player.max_hp
                self.player.attack_power += 5
                result += f"🎊 LEVEL UP! Je bent nu level {self.player.level}!\n"
                self.player.experience = 0
        else:
            enemy_damage = enemy.attack(self.player)
            result += f"💢 {enemy.name} valt terug en doet {enemy_damage} schade!\n"
            
            if not self.player.is_alive():
                result += "💀 Je bent verslagen! Game Over!"
                self.running = False
                self.game_over = True
        
        return result
    
    def _handle_take(self, args: List[str]) -> str:
        """Pak een item op"""
        if not args:
            return "Wat wil je oppakken? Gebruik: take [item]"
        
        item_name = args[0]
        level = self.get_current_level()
        item = level.remove_item(item_name)
        
        if item:
            self.player.add_item(item)
            return f"✅ Je pakt {item.name} op."
        else:
            return f"❌ {item_name} is hier niet te vinden."
    
    def _handle_use(self, args: List[str]) -> str:
        """Gebruik een item"""
        if not args:
            return "Wat wil je gebruiken? Gebruik: use [item]"
        
        item_name = args[0]
        return self.player.use_item(item_name)
    
    def _handle_go(self, args: List[str]) -> str:
        """Ga naar een ander level"""
        if not args:
            return "Waar wil je heen? Gebruik: go [direction]"
        
        direction = args[0]
        level = self.get_current_level()
        next_level_name = level.get_exit(direction)
        
        if not next_level_name:
            return f"❌ Je kunt niet naar {direction} gaan. Uitgangen: {', '.join(level.get_available_exits())}"
        
        if next_level_name not in self.levels:
            return f"❌ Level {next_level_name} bestaat niet."
        
        self.current_level_name = next_level_name
        level = self.levels[next_level_name]
        level.is_visited = True
        
        return f"🚶 Je gaat naar {next_level_name}.\n{level.description}"
    
    def _handle_help(self) -> str:
        """Toon help"""
        return """
📖 COMMANDO'S:
  look / l      - Bekijk het level
  fight / f [n] - Vecht tegen vijand n
  take / t [i]  - Pak item op
  use / u [i]   - Gebruik item uit inventory
  go / g [dir]  - Ga naar een richting
  inventory / i - Bekijk inventory
  status / s    - Toon status
  help / h      - Toon deze help
  quit          - Stop het spel
"""
    
    def run(self) -> None:
        """Start de game loop"""
        print("="*60)
        print("🎮 WELKOM BIJ HET TEXT-BASED RPG! 🎮")
        print("="*60)
        print(f"Hallo {self.player.name}! Je avontuur begint in {self.current_level_name}.")
        print("Typ 'help' voor alle commando's.\n")
        
        while self.running:
            try:
                self.show_status()
                command = input("\n> ").strip()
                result = self.handle_command(command)
                print("\n" + result + "\n")
                
                if self._check_win():
                    print("\n🎉 GEFELICITEERD! Je hebt het spel voltooid! 🎉")
                    self.running = False
                    break
                
                if self.game_over or not self.player.is_alive():
                    print("\n💀 GAME OVER! 💀")
                    print(f"Je hebt {self.turn_count} beurten overleefd.")
                    self.running = False
                    break
                
                self.turn_count += 1
                
            except KeyboardInterrupt:
                print("\n\n👋 Tot ziens!")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Er is een fout opgetreden: {e}")
        
        print("\nBedankt voor het spelen!")
    
    def _check_win(self) -> bool:
        """Check of de speler heeft gewonnen (alle levels cleared)"""
        return all(level.is_cleared() for level in self.levels.values())