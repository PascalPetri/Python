"""
Main entry point voor het Text-based RPG
"""

from models.player import Player
from models.enemy import Enemy
from models.item import Item
from models.level import Level
from game import Game

def create_game():
    """Maak de game met levels, enemies, items en player"""
    
    player = Player("Helden", hp=100, attack_power=15)
    
    # Levels
    forest = Level("Forest", 
                   "Een dichtbegroeid bos met hoge bomen. Vogels fluiten in de verte.")
    cave = Level("Cave", 
                 "Een donkere, vochtige grot. Water druppelt van de plafonds.")
    boss_room = Level("Boss Room", 
                      "Een grote, dreigende kamer. Hier wacht de eindbaas!")
    village = Level("Village", 
                    "Een vredig dorpje. De bewoners kijken je nieuwsgierig aan.")
    
    # Enemies
    goblin = Enemy("Goblin", hp=30, attack_power=8, experience_value=15)
    wolf = Enemy("Wolf", hp=25, attack_power=12, experience_value=12)
    orc = Enemy("Orc", hp=50, attack_power=15, experience_value=25)
    boss = Enemy("Shadow Dragon", hp=100, attack_power=20, experience_value=50)
    rat = Enemy("Giant Rat", hp=15, attack_power=5, experience_value=8)
    
    # Items
    health_potion = Item("Health Potion", "heal", 30, "Herstelt 30 HP")
    health_potion2 = Item("Health Potion", "heal", 20, "Herstelt 20 HP")
    strength_elixir = Item("Strength Elixir", "attack_boost", 10, "Verhoogt aanvalskracht met 10")
    magic_scroll = Item("Magic Scroll", "special", 0, "Een mysterieuze magische scroll")
    key = Item("Gold Key", "key", 0, "Een gouden sleutel, misschien opent het iets")
    
    # Voeg enemies en items toe aan levels
    forest.add_enemy(goblin)
    forest.add_enemy(wolf)
    forest.add_enemy(rat)
    forest.add_item(health_potion)
    forest.add_item(strength_elixir)
    forest.add_item(key)
    
    cave.add_enemy(orc)
    cave.add_enemy(rat)
    cave.add_item(health_potion2)
    cave.add_item(magic_scroll)
    
    boss_room.add_enemy(boss)
    boss_room.add_item(health_potion)
    boss_room.add_item(strength_elixir)
    
    village.add_item(health_potion)
    village.add_item(magic_scroll)
    
    # Verbind levels
    forest.add_exit("east", "Cave")
    forest.add_exit("south", "Village")
    forest.add_exit("west", "Village")
    
    cave.add_exit("west", "Forest")
    cave.add_exit("north", "Boss Room")
    
    boss_room.add_exit("south", "Cave")
    
    village.add_exit("north", "Forest")
    village.add_exit("east", "Forest")
    
    # Creëer game
    game = Game(player, "Village")
    game.add_level(forest)
    game.add_level(cave)
    game.add_level(boss_room)
    game.add_level(village)
    
    return game

def main():
    """Start de game"""
    print("="*60)
    print("🎮 TEXT-BASED RPG 🎮")
    print("="*60)
    print("Welkom bij het avontuur!")
    print("Type 'help' voor een lijst van commando's.")
    print("="*60)
    
    game = create_game()
    game.run()

if __name__ == "__main__":
    main()