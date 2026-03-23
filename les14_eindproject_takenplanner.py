"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Takenplanner - taken toevoegen, bekijken, afvinken en verwijderen met JSON-opslag
"""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class Taak:
    """Een taak met titel en status."""
    titel: str
    klaar: bool = False
    
    def markeer_klaar(self):
        self.klaar = True
    
    def to_dict(self):
        return {"titel": self.titel, "klaar": self.klaar}
    
    @staticmethod
    def from_dict(data):
        return Taak(titel=data["titel"], klaar=data["klaar"])


class Takenlijst:
    """Beheert een lijst van taken."""
    
    def __init__(self, filename="taken.json"):
        self.taken: List[Taak] = []
        self.filename = filename
    
    def voeg_toe(self, titel):
        """Voeg een nieuwe taak toe."""
        if not titel or titel.strip() == "":
            print("❌ Titel mag niet leeg zijn!")
            return False
        
        self.taken.append(Taak(titel.strip()))
        print(f"✅ Taak '{titel}' toegevoegd!")
        return True
    
    def toon(self):
        """Toon alle taken met nummer en status."""
        if not self.taken:
            print("\n📭 Geen taken gevonden.\n")
            return
        
        print("\n" + "=" * 50)
        print("📋 MIJN TAKEN")
        print("=" * 50)
        
        for i, taak in enumerate(self.taken, 1):
            status = "✅" if taak.klaar else "⬜"
            print(f"{i}. {status} {taak.titel}")
        
        print("=" * 50 + "\n")
    
    def markeer_klaar(self, index):
        """Markeer een taak als klaar."""
        if not self._check_index(index):
            return False
        
        if self.taken[index].klaar:
            print(f"⚠️ Taak is al klaar!")
            return False
        
        self.taken[index].markeer_klaar()
        print(f"✅ Taak gemarkeerd als klaar!")
        return True
    
    def verwijder(self, index):
        """Verwijder een taak."""
        if not self._check_index(index):
            return False
        
        verwijderde = self.taken.pop(index)
        print(f"🗑️ Taak '{verwijderde.titel}' verwijderd!")
        return True
    
    def _check_index(self, index):
        """Controleer of index geldig is."""
        if 0 <= index < len(self.taken):
            return True
        print(f"❌ Ongeldig nummer! Kies 1 t/m {len(self.taken)}")
        return False
    
    def save(self):
        """Sla taken op in JSON."""
        try:
            data = [t.to_dict() for t in self.taken]
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Opgeslagen in {self.filename}")
            return True
        except Exception as e:
            print(f"❌ Fout bij opslaan: {e}")
            return False
    
    def load(self):
        """Laad taken uit JSON."""
        if not Path(self.filename).exists():
            print("📄 Geen bestand gevonden. Starten met lege lijst.")
            return False
        
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.taken = [Taak.from_dict(item) for item in data]
            print(f"📂 {len(self.taken)} taken geladen")
            return True
        except Exception as e:
            print(f"❌ Fout bij laden: {e}")
            return False


def main():
    """Hoofdfunctie met menu."""
    print("\n" + "=" * 50)
    print("🎯 TAKENPLANNER")
    print("=" * 50)
    
    planner = Takenlijst()
    planner.load()
    
    while True:
        print("\n" + "-" * 30)
        print("1. 📋 Toon taken")
        print("2. ➕ Taak toevoegen")
        print("3. ✅ Markeer als klaar")
        print("4. 🗑️ Verwijder taak")
        print("0. 💾 Opslaan en stoppen")
        print("-" * 30)
        
        keuze = input("Kies een optie: ")
        
        if keuze == "1":
            planner.toon()
        
        elif keuze == "2":
            titel = input("Titel: ").strip()
            planner.voeg_toe(titel)
        
        elif keuze == "3":
            if not planner.taken:
                print("📭 Geen taken om af te vinken.")
                continue
            
            planner.toon()
            try:
                nummer = int(input("Nummer van taak: "))
                planner.markeer_klaar(nummer - 1)
            except ValueError:
                print("❌ Voer een geldig nummer in.")
        
        elif keuze == "4":
            if not planner.taken:
                print("📭 Geen taken om te verwijderen.")
                continue
            
            planner.toon()
            try:
                nummer = int(input("Nummer van taak: "))
                planner.verwijder(nummer - 1)
            except ValueError:
                print("❌ Voer een geldig nummer in.")
        
        elif keuze == "0":
            planner.save()
            print("👋 Tot ziens!")
            break
        
        else:
            print("❌ Ongeldige keuze. Kies 0, 1, 2, 3 of 4.")


if __name__ == "__main__":
    main()