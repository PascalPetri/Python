"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Unit tests voor les12_logic.py (10 tests)
"""

import unittest
from les12_logic import Product, Winkelmandje


class TestProduct(unittest.TestCase):
    """Testklasse voor de Product class."""
    
    # Test 1: voorraad verlaagt bij geldig aantal
    def test_verlaag_voorraad_geldig(self):
        """Test dat voorraad correct verlaagd wordt bij geldig aantal."""
        p = Product("Muis", 25, 10)
        
        resultaat = p.verlaag_voorraad(3)
        
        self.assertTrue(resultaat)
        self.assertEqual(p.voorraad, 7)
    
    # Test 2: voorraad mag niet negatief worden
    def test_verlaag_voorraad_teveel(self):
        """Test dat voorraad niet verlaagd wordt als aantal te groot is."""
        p = Product("Muis", 25, 2)
        
        resultaat = p.verlaag_voorraad(5)
        
        self.assertFalse(resultaat)
        self.assertEqual(p.voorraad, 2)
    
    # Test 3: negatief aantal mag niet
    def test_verlaag_voorraad_negatief(self):
        """Test dat voorraad niet verlaagd wordt bij negatief aantal."""
        p = Product("Muis", 25, 5)
        
        resultaat = p.verlaag_voorraad(-1)
        
        self.assertFalse(resultaat)
        self.assertEqual(p.voorraad, 5)
    
    # Test 4: nul aantal mag niet
    def test_verlaag_voorraad_nul(self):
        """Test dat voorraad niet verlaagd wordt bij nul aantal."""
        p = Product("Muis", 25, 10)
        
        resultaat = p.verlaag_voorraad(0)
        
        self.assertFalse(resultaat)
        self.assertEqual(p.voorraad, 10)
    
    # Test 5: is_op_voorraad werkt correct
    def test_is_op_voorraad(self):
        """Test de is_op_voorraad methode."""
        p = Product("Laptop", 899, 3)
        
        self.assertTrue(p.is_op_voorraad(1))
        self.assertTrue(p.is_op_voorraad(3))
        self.assertFalse(p.is_op_voorraad(4))
        self.assertFalse(p.is_op_voorraad(0))
        self.assertFalse(p.is_op_voorraad(-1))


class TestWinkelmandje(unittest.TestCase):
    """Testklasse voor de Winkelmandje class."""
    
    def setUp(self):
        """Maak standaard testproducten voor elke test."""
        self.p1 = Product("Muis", 25, 10)
        self.p2 = Product("Toetsenbord", 59, 5)
        self.p3 = Product("Laptop", 899, 1)
        self.mandje = Winkelmandje()
    
    # Test 6: totaalprijs klopt bij meerdere items
    def test_totaal_prijs_meerdere_items(self):
        """Test dat totaalprijs correct berekend wordt."""
        self.mandje.voeg_toe(self.p1, 2)   # 2 x 25 = 50
        self.mandje.voeg_toe(self.p2, 1)   # 1 x 59 = 59
        
        self.assertEqual(self.mandje.totaal_prijs(), 109)
    
    # Test 7: toevoegen mislukt bij te weinig voorraad
    def test_voeg_toe_teveel_voorraad(self):
        """Test dat toevoegen mislukt als aantal groter is dan voorraad."""
        resultaat = self.mandje.voeg_toe(self.p3, 3)
        
        self.assertFalse(resultaat)
        self.assertEqual(self.mandje.totaal_prijs(), 0)
        self.assertEqual(len(self.mandje.items), 0)
    
    # Test 8: zelfde product meerdere keren toevoegen
    def test_voeg_toe_zelfde_product(self):
        """Test dat toevoegen vanzelfde product de hoeveelheid optelt."""
        self.mandje.voeg_toe(self.p1, 2)
        self.mandje.voeg_toe(self.p1, 3)
        
        self.assertEqual(len(self.mandje.items), 1)
        self.assertEqual(self.mandje.items[0][1], 5)
        self.assertEqual(self.mandje.totaal_prijs(), 125)  # 5 x 25 = 125
    
    # Test 9: totaalprijs leeg mandje is 0
    def test_totaal_prijs_leeg_mandje(self):
        """Test dat totaalprijs van leeg mandje 0 is."""
        self.assertEqual(self.mandje.totaal_prijs(), 0)
    
    # Test 10: leeg_mandje werkt correct
    def test_leeg_mandje(self):
        """Test dat leeg_mandje alle items verwijdert."""
        self.mandje.voeg_toe(self.p1, 2)
        self.mandje.voeg_toe(self.p2, 3)
        
        self.mandje.leeg_mandje()
        
        self.assertEqual(len(self.mandje.items), 0)
        self.assertEqual(self.mandje.totaal_prijs(), 0)


if __name__ == "__main__":
    unittest.main()