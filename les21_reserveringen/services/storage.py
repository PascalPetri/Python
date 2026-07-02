"""
Storage service voor JSON opslag
Verantwoordelijk voor lezen en schrijven van reserveringen naar bestand
"""

import json
import os
from typing import List
from models.reservering import Reservering

class ReserveringStorage:
    """Klasse voor het opslaan en laden van reserveringen in JSON formaat"""
    
    def __init__(self, bestandspad: str = "reserveringen.json"):
        self.bestandspad = bestandspad
    
    def load(self) -> List[Reservering]:
        """Laad reserveringen uit JSON bestand"""
        if not os.path.exists(self.bestandspad):
            return []
        
        try:
            with open(self.bestandspad, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Reservering.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            # Als het bestand corrupt is of niet bestaat, begin met lege lijst
            return []
    
    def save(self, reserveringen: List[Reservering]) -> None:
        """Sla reserveringen op naar JSON bestand"""
        data = [r.to_dict() for r in reserveringen]
        with open(self.bestandspad, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)