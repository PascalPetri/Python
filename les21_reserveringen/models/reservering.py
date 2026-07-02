"""
Reservering model class
Verantwoordelijk voor de data-structuur van een reservering
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reservering:
    """Klasse die een restaurant reservering voorstelt"""
    naam: str
    datum: str  # formaat: "YYYY-MM-DD"
    tijd: str   # formaat: "HH:MM"
    aantal_personen: int
    
    def to_dict(self) -> dict:
        """Converteer reservering naar dictionary voor JSON opslag"""
        return {
            "naam": self.naam,
            "datum": self.datum,
            "tijd": self.tijd,
            "aantal_personen": self.aantal_personen
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reservering':
        """Maak een Reservering object van een dictionary"""
        return cls(
            naam=data["naam"],
            datum=data["datum"],
            tijd=data["tijd"],
            aantal_personen=data["aantal_personen"]
        )
    
    def __str__(self) -> str:
        """Mooie weergave van een reservering"""
        return f"{self.naam} - {self.datum} om {self.tijd} ({self.aantal_personen} personen)"