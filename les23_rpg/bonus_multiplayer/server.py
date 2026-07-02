"""
Multiplayer Server - Beheert de game state voor meerdere clients
"""

import socket
import threading
import json
from typing import Dict, List, Optional
from models.player import Player
from models.enemy import Enemy
from models.item import Item
from models.level import Level

class MultiplayerGame:
    """Game state voor multiplayer"""
    
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.current_turn = 0
        self.game_state = "waiting"
        self.levels = self._create_levels()
        self.current_level = "Village"
    
    def _create_levels(self) -> Dict[str, Level]:
        """Maak de levels voor multiplayer"""
        forest = Level("Forest", "Een dichtbegroeid bos met hoge bomen.")
        cave = Level("Cave", "Een donkere, vochtige grot.")
        boss_room = Level("Boss Room", "Een grote, dreigende kamer.")
        village = Level("Village", "Een vredig dorpje.")
        
        goblin = Enemy("Goblin", 30, 8, 15)
        wolf = Enemy("Wolf", 25, 12, 12)
        orc = Enemy("Orc", 50, 15, 25)
        boss = Enemy("Shadow Dragon", 100, 20, 50)
        
        forest.add_enemy(goblin)
        forest.add_enemy(wolf)
        cave.add_enemy(orc)
        boss_room.add_enemy(boss)
        
        forest.add_item(Item("Health Potion", "heal", 30))
        forest.add_item(Item("Strength Elixir", "attack_boost", 10))
        cave.add_item(Item("Health Potion", "heal", 20))
        cave.add_item(Item("Magic Scroll", "special", 0))
        boss_room.add_item(Item("Health Potion", "heal", 30))
        
        forest.add_exit("east", "Cave")
        forest.add_exit("south", "Village")
        cave.add_exit("west", "Forest")
        cave.add_exit("north", "Boss Room")
        boss_room.add_exit("south", "Cave")
        village.add_exit("north", "Forest")
        village.add_exit("east", "Forest")
        
        return {
            "Forest": forest,
            "Cave": cave,
            "Boss Room": boss_room,
            "Village": village
        }
    
    def add_player(self, name: str) -> bool:
        """Voeg een speler toe aan de game"""
        if name in self.players:
            return False
        
        self.players[name] = Player(name, hp=100, attack_power=15)
        
        if len(self.players) == 2:
            self.game_state = "playing"
        
        return True
    
    def get_game_state(self, player_name: str) -> str:
        """Geef de game state voor een specifieke speler"""
        if player_name not in self.players:
            return "ERROR: Speler niet gevonden"
        
        player = self.players[player_name]
        level = self.levels[self.current_level]
        
        state = {
            "player": {
                "name": player.name,
                "hp": player.hp,
                "max_hp": player.max_hp,
                "attack_power": player.attack_power,
                "inventory": [item.name for item in player.inventory]
            },
            "level": {
                "name": level.name,
                "description": level.description,
                "enemies": [{"name": e.name, "hp": e.hp, "max_hp": e.max_hp} 
                           for e in level.get_enemies()],
                "items": [item.name for item in level.items],
                "exits": level.get_available_exits()
            },
            "game_state": self.game_state,
            "current_turn": self.current_turn,
            "players": list(self.players.keys())
        }
        
        return json.dumps(state)
    
    def process_action(self, player_name: str, action: str) -> str:
        """Verwerk een actie van een speler"""
        if player_name not in self.players:
            return "ERROR: Speler niet gevonden"
        
        if self.game_state != "playing":
            return "ERROR: Game is niet actief"
        
        if action.startswith("look"):
            return self.get_game_state(player_name)
        
        if action.startswith("fight"):
            return self._handle_fight(player_name)
        
        if action.startswith("status"):
            return self.get_game_state(player_name)
        
        return f"Onbekende actie: {action}"
    
    def _handle_fight(self, player_name: str) -> str:
        """Vecht logica"""
        player = self.players[player_name]
        level = self.levels[self.current_level]
        enemies = level.get_enemies()
        
        if not enemies:
            return "Geen vijanden hier!"
        
        enemy = enemies[0]
        damage = player.attack(enemy)
        result = f"{player_name} valt {enemy.name} aan en doet {damage} schade!\n"
        
        if not enemy.is_alive():
            result += f"{enemy.name} is verslagen!\n"
        else:
            enemy_damage = enemy.attack(player)
            result += f"{enemy.name} valt terug en doet {enemy_damage} schade!\n"
        
        return result

class GameServer:
    """Server die multiplayer games host"""
    
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.game = MultiplayerGame()
        self.clients: Dict[str, socket.socket] = {}
        self.running = False
    
    def start(self):
        """Start de server"""
        self.running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(2)
        
        print(f"🖥️  Server gestart op {self.host}:{self.port}")
        print("⏳ Wachten op spelers...")
        
        try:
            while self.running and len(self.clients) < 2:
                client_socket, address = server_socket.accept()
                print(f"📡 Verbinding van {address}")
                
                client_socket.send(b"Vul je naam in: ")
                name = client_socket.recv(1024).decode().strip()
                
                if self.game.add_player(name):
                    self.clients[name] = client_socket
                    client_socket.send(f"Welkom {name}!".encode())
                    
                    if len(self.clients) == 2:
                        print("🎮 Beide spelers verbonden! Start spel...")
                        self._broadcast("Spel begint! Alle spelers verbonden.")
                else:
                    client_socket.send("Naam bestaat al!".encode())
                    client_socket.close()
            
            if len(self.clients) == 2:
                self._game_loop()
                
        except Exception as e:
            print(f"❌ Server fout: {e}")
        finally:
            self._cleanup()
    
    def _game_loop(self):
        """Hoofd game loop voor multiplayer"""
        while self.running:
            player_names = list(self.clients.keys())
            current_player = player_names[self.game.current_turn % len(player_names)]
            
            self._broadcast(f"🎯 {current_player} is aan de beurt!")
            
            client_socket = self.clients[current_player]
            client_socket.send("Je bent aan de beurt! Voer actie in: ".encode())
            
            try:
                action = client_socket.recv(1024).decode().strip()
                result = self.game.process_action(current_player, action)
                self._broadcast(f"📢 {current_player}: {action}\n{result}")
                
                self.game.current_turn += 1
                
                if self.game.game_state == "game_over":
                    self._broadcast("💀 GAME OVER!")
                    break
                    
            except Exception as e:
                print(f"❌ Fout met {current_player}: {e}")
                break
    
    def _broadcast(self, message: str):
        """Stuur bericht naar alle clients"""
        for client in self.clients.values():
            try:
                client.send(f"{message}\n".encode())
            except:
                pass
    
    def _cleanup(self):
        """Opruimen bij stoppen"""
        for client in self.clients.values():
            client.close()
        self.running = False
        print("🛑 Server gestopt.")

if __name__ == "__main__":
    server = GameServer()
    server.start()