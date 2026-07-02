"""
ReserveringManager - Beheert alle reserveringen
Verantwoordelijk voor de logica van het reserveringssysteem
"""

from typing import List, Optional
from models.reservering import Reservering
from services.storage import ReserveringStorage

class ReserveringManager:
    """Manager die alle reserveringen beheert met validatie en opslag"""
    
    def __init__(self, storage: Optional[ReserveringStorage] = None):
        self.storage = storage or ReserveringStorage()
        self.reserveringen = self.storage.load()
    
    def voeg_toe(self, naam: str, datum: str, tijd: str, aantal_personen: int) -> bool:
        """
        Voeg een nieuwe reservering toe met validatie
        Returns: True als succesvol, False als validatie faalt
        """
        # Validatie
        if not self._is_valide(naam, datum, tijd, aantal_personen):
            return False
        
        # Maak nieuwe reservering
        reservering = Reservering(naam, datum, tijd, aantal_personen)
        self.reserveringen.append(reservering)
        
        # Opslaan
        self.storage.save(self.reserveringen)
        return True
    
    def _is_valide(self, naam: str, datum: str, tijd: str, aantal_personen: int) -> bool:
        """Valideer alle invoervelden"""
        if not naam or not naam.strip():
            return False
        
        if not datum or not datum.strip():
            return False
        
        if not tijd or not tijd.strip():
            return False
        
        if not isinstance(aantal_personen, int) or aantal_personen <= 0:
            return False
        
        return True
    
    def alles(self) -> List[Reservering]:
        """Geef alle reserveringen terug"""
        return self.reserveringen
    
    def verwijder(self, index: int) -> bool:
        """
        Verwijder een reservering op basis van index (0-based)
        Returns: True als succesvol, False als index ongeldig is
        """
        if 0 <= index < len(self.reserveringen):
            verwijderde = self.reserveringen.pop(index)
            self.storage.save(self.reserveringen)
            return True
        return False
    
    def zoek_op_naam(self, naam: str) -> List[Reservering]:
        """Zoek reserveringen op naam (case-insensitive, gedeeltelijke match)"""
        naam_lower = naam.lower().strip()
        return [r for r in self.reserveringen if naam_lower in r.naam.lower()]
    
    def filter_op_datum(self, datum: str) -> List[Reservering]:
        """Filter reserveringen op exacte datum"""
        return [r for r in self.reserveringen if r.datum == datum]
    
    def heeft_capaciteit(self, datum: str, tijd: str, max_personen: int = 30) -> bool:
        """
        Controleer of er nog capaciteit is voor een bepaald tijdslot
        """
        huidig_totaal = sum(
            r.aantal_personen 
            for r in self.reserveringen 
            if r.datum == datum and r.tijd == tijd
        )
        return huidig_totaal < max_personen
    
    def totaal_personen(self, datum: str, tijd: str) -> int:
        """Bereken totaal aantal personen voor een bepaald tijdslot"""
        return sum(
            r.aantal_personen 
            for r in self.reserveringen 
            if r.datum == datum and r.tijd == tijd
        )