"""
Unit tests voor het RPG systeem
"""

import unittest
from models.player import Player
from models.enemy import Enemy
from models.item import Item
from models.level import Level

class TestPlayer(unittest.TestCase):
    """Test de Player class"""
    
    def test_player_creation(self):
        player = Player("Test", 100, 15)
        self.assertEqual(player.name, "Test")
        self.assertEqual(player.hp, 100)
        self.assertEqual(player.max_hp, 100)
        self.assertEqual(player.attack_power, 15)
        self.assertTrue(player.is_alive())
    
    def test_player_take_damage(self):
        player = Player("Test", 100, 15)
        damage = player.take_damage(30)
        self.assertEqual(damage, 30)
        self.assertEqual(player.hp, 70)
        
        damage = player.take_damage(100)
        self.assertEqual(damage, 70)
        self.assertEqual(player.hp, 0)
        self.assertFalse(player.is_alive())
    
    def test_player_heal(self):
        player = Player("Test", 100, 15)
        player.take_damage(50)
        self.assertEqual(player.hp, 50)
        
        healed = player.heal(30)
        self.assertEqual(healed, 30)
        self.assertEqual(player.hp, 80)
        
        healed = player.heal(50)
        self.assertEqual(healed, 20)
        self.assertEqual(player.hp, 100)
    
    def test_player_attack(self):
        player = Player("Test", 100, 15)
        enemy = Enemy("Goblin", 30, 8, 10)
        
        damage = player.attack(enemy)
        self.assertGreater(damage, 0)
        self.assertLessEqual(damage, 15)
    
    def test_player_items(self):
        player = Player("Test", 100, 15)
        potion = Item("Health Potion", "heal", 30)
        
        player.add_item(potion)
        self.assertEqual(len(player.inventory), 1)
        self.assertEqual(player.inventory[0].name, "Health Potion")
        
        result = player.use_item("Health Potion")
        self.assertIn("herstelt", result)
        self.assertEqual(len(player.inventory), 0)

class TestEnemy(unittest.TestCase):
    """Test de Enemy class"""
    
    def test_enemy_creation(self):
        enemy = Enemy("Goblin", 30, 8, 15)
        self.assertEqual(enemy.name, "Goblin")
        self.assertEqual(enemy.hp, 30)
        self.assertEqual(enemy.attack_power, 8)
        self.assertTrue(enemy.is_alive())
    
    def test_enemy_take_damage(self):
        enemy = Enemy("Goblin", 30, 8, 15)
        damage = enemy.take_damage(20)
        self.assertEqual(damage, 20)
        self.assertEqual(enemy.hp, 10)
        self.assertTrue(enemy.is_alive())
        
        damage = enemy.take_damage(15)
        self.assertEqual(damage, 10)
        self.assertEqual(enemy.hp, 0)
        self.assertFalse(enemy.is_alive())

class TestItem(unittest.TestCase):
    """Test de Item class"""
    
    def test_item_creation(self):
        item = Item("Test Item", "heal", 20, "Test description")
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.type, "heal")
        self.assertEqual(item.value, 20)
    
    def test_item_apply_heal(self):
        player = Player("Test", 100, 15)
        player.take_damage(50)
        item = Item("Health Potion", "heal", 30)
        
        result = item.apply(player)
        self.assertIn("herstelt", result)
        self.assertEqual(player.hp, 80)
    
    def test_item_apply_attack_boost(self):
        player = Player("Test", 100, 15)
        item = Item("Strength Elixir", "attack_boost", 10)
        
        result = item.apply(player)
        self.assertIn("+10", result)
        self.assertEqual(player.attack_power, 25)

class TestLevel(unittest.TestCase):
    """Test de Level class"""
    
    def test_level_creation(self):
        level = Level("Test Level", "Test description")
        self.assertEqual(level.name, "Test Level")
        self.assertEqual(level.description, "Test description")
    
    def test_level_add_enemy(self):
        level = Level("Test Level", "Test")
        enemy = Enemy("Goblin", 30, 8, 15)
        level.add_enemy(enemy)
        
        self.assertEqual(len(level.enemies), 1)
        self.assertEqual(len(level.get_enemies()), 1)
        
        enemy.take_damage(30)
        self.assertEqual(len(level.get_enemies()), 0)
    
    def test_level_add_item(self):
        level = Level("Test Level", "Test")
        item = Item("Health Potion", "heal", 30)
        level.add_item(item)
        
        self.assertEqual(len(level.items), 1)
        
        removed = level.remove_item("Health Potion")
        self.assertIsNotNone(removed)
        self.assertEqual(len(level.items), 0)
    
    def test_level_exits(self):
        level = Level("Test Level", "Test")
        level.add_exit("east", "Forest")
        level.add_exit("north", "Cave")
        
        self.assertEqual(level.get_exit("east"), "Forest")
        self.assertEqual(level.get_exit("north"), "Cave")
        self.assertIsNone(level.get_exit("west"))
        
        self.assertEqual(set(level.get_available_exits()), {"east", "north"})

if __name__ == "__main__":
    unittest.main()