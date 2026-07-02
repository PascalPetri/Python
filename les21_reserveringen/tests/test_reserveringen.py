"""
Unit tests voor het Restaurant Reserveringssysteem
Minimaal 5 tests zoals vereist
"""

import unittest
import os
import json
from models.reservering import Reservering
from services.manager import ReserveringManager
from services.storage import ReserveringStorage

class TestReservering(unittest.TestCase):
    """Test de Reservering class"""
    
    def test_reservering_aanmaken(self):
        """Test of een reservering correct wordt aangemaakt"""
        res = Reservering("Jan", "2026-02-06", "18:30", 4)
        self.assertEqual(res.naam, "Jan")
        self.assertEqual(res.datum, "2026-02-06")
        self.assertEqual(res.tijd, "18:30")
        self.assertEqual(res.aantal_personen, 4)
    
    def test_to_dict(self):
        """Test of to_dict correct werkt"""
        res = Reservering("Piet", "2026-02-07", "19:00", 2)
        expected = {
            "naam": "Piet",
            "datum": "2026-02-07",
            "tijd": "19:00",
            "aantal_personen": 2
        }
        self.assertEqual(res.to_dict(), expected)
    
    def test_from_dict(self):
        """Test of from_dict correct werkt"""
        data = {
            "naam": "Klaas",
            "datum": "2026-02-08",
            "tijd": "20:00",
            "aantal_personen": 6
        }
        res = Reservering.from_dict(data)
        self.assertEqual(res.naam, "Klaas")
        self.assertEqual(res.datum, "2026-02-08")
        self.assertEqual(res.tijd, "20:00")
        self.assertEqual(res.aantal_personen, 6)

class TestReserveringManager(unittest.TestCase):
    """Test de ReserveringManager class"""
    
    def setUp(self):
        """Maak een schone manager voor elke test"""
        self.manager = ReserveringManager()
    
    def test_voeg_toe_geldig(self):
        """Test 1: Geldig toevoegen → True + lijst groeit"""
        result = self.manager.voeg_toe("Anna", "2026-02-06", "18:30", 2)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.alles()), 1)
    
    def test_voeg_toe_lege_naam(self):
        """Test 2: Toevoegen met lege naam → False"""
        result = self.manager.voeg_toe("", "2026-02-06", "18:30", 2)
        self.assertFalse(result)
        self.assertEqual(len(self.manager.alles()), 0)
    
    def test_voeg_toe_aantal_0(self):
        """Test 3: Toevoegen met aantal 0 → False"""
        result = self.manager.voeg_toe("Bob", "2026-02-06", "18:30", 0)
        self.assertFalse(result)
        self.assertEqual(len(self.manager.alles()), 0)
    
    def test_verwijder_geldig(self):
        """Test 4: Verwijderen geldige index → True"""
        self.manager.voeg_toe("Test", "2026-02-06", "18:30", 2)
        self.assertEqual(len(self.manager.alles()), 1)
        result = self.manager.verwijder(0)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.alles()), 0)
    
    def test_verwijder_ongeldig(self):
        """Test 5: Verwijderen foute index → False"""
        self.manager.voeg_toe("Test", "2026-02-06", "18:30", 2)
        result = self.manager.verwijder(5)  # Index bestaat niet
        self.assertFalse(result)
        self.assertEqual(len(self.manager.alles()), 1)
    
    def test_zoek_op_naam(self):
        """Extra test: Zoeken op naam werkt correct"""
        self.manager.voeg_toe("Jan Jansen", "2026-02-06", "18:30", 2)
        self.manager.voeg_toe("Piet Pieters", "2026-02-06", "19:00", 4)
        self.manager.voeg_toe("Jan de Vries", "2026-02-07", "18:30", 3)
        
        resultaten = self.manager.zoek_op_naam("Jan")
        self.assertEqual(len(resultaten), 2)
        
        resultaten = self.manager.zoek_op_naam("Piet")
        self.assertEqual(len(resultaten), 1)
    
    def test_filter_op_datum(self):
        """Extra test: Filteren op datum werkt correct"""
        self.manager.voeg_toe("Jan", "2026-02-06", "18:30", 2)
        self.manager.voeg_toe("Piet", "2026-02-06", "19:00", 4)
        self.manager.voeg_toe("Klaas", "2026-02-07", "18:30", 3)
        
        resultaten = self.manager.filter_op_datum("2026-02-06")
        self.assertEqual(len(resultaten), 2)
        
        resultaten = self.manager.filter_op_datum("2026-02-07")
        self.assertEqual(len(resultaten), 1)
    
    def test_capaciteit(self):
        """Extra test: Capaciteit controle werkt correct"""
        self.manager.voeg_toe("Jan", "2026-02-06", "18:30", 10)
        self.manager.voeg_toe("Piet", "2026-02-06", "18:30", 15)
        
        # Totaal 25 personen, nog 5 beschikbaar (max 30)
        self.assertTrue(self.manager.heeft_capaciteit("2026-02-06", "18:30"))
        
        self.manager.voeg_toe("Klaas", "2026-02-06", "18:30", 10)
        # Totaal 35 personen, over de max
        self.assertFalse(self.manager.heeft_capaciteit("2026-02-06", "18:30"))

class TestReserveringStorage(unittest.TestCase):
    """Test de Storage class"""
    
    def setUp(self):
        """Maak een test bestand"""
        self.test_bestand = "test_reserveringen.json"
        self.storage = ReserveringStorage(self.test_bestand)
    
    def tearDown(self):
        """Verwijder test bestand na tests"""
        if os.path.exists(self.test_bestand):
            os.remove(self.test_bestand)
    
    def test_save_en_load(self):
        """Test of opslaan en laden werkt"""
        reserveringen = [
            Reservering("Jan", "2026-02-06", "18:30", 2),
            Reservering("Piet", "2026-02-07", "19:00", 4)
        ]
        
        self.storage.save(reserveringen)
        geladen = self.storage.load()
        
        self.assertEqual(len(geladen), 2)
        self.assertEqual(geladen[0].naam, "Jan")
        self.assertEqual(geladen[1].naam, "Piet")
    
    def test_load_bestand_bestaat_niet(self):
        """Test of load een lege lijst geeft als bestand niet bestaat"""
        if os.path.exists(self.test_bestand):
            os.remove(self.test_bestand)
        
        geladen = self.storage.load()
        self.assertEqual(geladen, [])

if __name__ == "__main__":
    unittest.main()