"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Producten opslaan en laden met JSON
"""

import json
from pathlib import Path


class Product:
    """Een productklasse voor het opslaan van productinformatie."""
    
    def __init__(self, naam, prijs, voorraad):
        """
        Initialiseer een nieuw product.
        
        Args:
            naam (str): De naam van het product
            prijs (float): De prijs van het product
            voorraad (int): De beschikbare voorraad
        """
        self.naam = naam
        self.prijs = prijs
        self._voorraad = voorraad
    
    def to_dict(self):
        """
        Converteer product naar dictionary voor JSON-opslag.
        
        Returns:
            dict: Een dictionary met productgegevens
        """
        return {
            "naam": self.naam,
            "prijs": self.prijs,
            "voorraad": self._voorraad
        }
    
    @staticmethod
    def from_dict(data):
        """
        Maak een Product-object van een dictionary.
        
        Args:
            data (dict): Dictionary met productgegevens
            
        Returns:
            Product: Een nieuw Product-object
        """
        return Product(
            data["naam"],
            data["prijs"],
            data["voorraad"]
        )
    
    def __str__(self):
        """Maak een leesbare weergave van het product."""
        return f"{self.naam} - €{self.prijs:.2f} - Voorraad: {self._voorraad}"


def save_producten(producten, filename):
    """
    Sla producten op in een JSON-bestand.
    
    Args:
        producten (list): Lijst met Product-objecten
        filename (str): Naam van het bestand om op te slaan
    """
    data = [p.to_dict() for p in producten]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Producten opgeslagen in {filename}")


def load_producten(filename):
    """
    Laad producten uit een JSON-bestand.
    
    Args:
        filename (str): Naam van het bestand om te laden
        
    Returns:
        list: Lijst met Product-objecten
    """
    if not Path(filename).exists():
        return []
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Product.from_dict(d) for d in data]
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ Bestand kon niet worden geladen, starten met lege lijst.")
        return []


def vraag_int(prompt):
    """
    Vraag een integer aan de gebruiker met foutafhandeling.
    
    Args:
        prompt (str): De vraag die aan de gebruiker getoond wordt
        
    Returns:
        int: Het ingevoerde gehele getal
    """
    while True:
        try:
            waarde = int(input(prompt))
            return waarde
        except ValueError:
            print("❌ Ongeldige invoer. Voer een geheel getal in.")


def vraag_float(prompt):
    """
    Vraag een float aan de gebruiker met foutafhandeling.
    
    Args:
        prompt (str): De vraag die aan de gebruiker getoond wordt
        
    Returns:
        float: Het ingevoerde getal met decimalen
    """
    while True:
        try:
            waarde = float(input(prompt))
            if waarde < 0:
                print("❌ Prijs kan niet negatief zijn.")
                continue
            return waarde
        except ValueError:
            print("❌ Ongeldige invoer. Voer een getal in (gebruik . voor decimalen).")


def toon_producten(producten):
    """
    Toon alle producten op het scherm.
    
    Args:
        producten (list): Lijst met Product-objecten
    """
    if not producten:
        print("📦 Geen producten gevonden.")
        return
    
    print("\n" + "=" * 50)
    print("📋 OVERZICHT PRODUCTEN")
    print("=" * 50)
    for i, product in enumerate(producten, 1):
        print(f"{i}. {product}")
    print("=" * 50 + "\n")


def main():
    """Hoofdfunctie van het programma."""
    filename = "producten.json"
    
    # Laad bestaande producten of start met lege lijst
    producten = load_producten(filename)
    
    # Als er geen producten zijn, voeg standaardproducten toe
    if not producten:
        print("📦 Geen opgeslagen producten gevonden. Starten met standaardproducten.")
        producten = [
            Product("Muis", 25.00, 10),
            Product("Toetsenbord", 45.50, 5),
            Product("Monitor", 199.99, 3)
        ]
    
    while True:
        print("\n" + "=" * 40)
        print("🛒 PRODUCTEN BEHEER")
        print("=" * 40)
        print("1. Toon producten")
        print("2. Product toevoegen")
        print("3. Opslaan")
        print("0. Stoppen")
        print("=" * 40)
        
        keuze = input("Kies een optie: ")
        
        if keuze == "1":
            toon_producten(producten)
        
        elif keuze == "2":
            print("\n➕ Nieuw product toevoegen")
            naam = input("Productnaam: ")
            prijs = vraag_float("Prijs (€): ")
            voorraad = vraag_int("Voorraad: ")
            
            product = Product(naam, prijs, voorraad)
            producten.append(product)
            print(f"✅ Product '{naam}' toegevoegd!")
        
        elif keuze == "3":
            save_producten(producten, filename)
        
        elif keuze == "0":
            print("\n💾 Opslaan voor het afsluiten...")
            save_producten(producten, filename)
            print("👋 Programma afgesloten. Tot ziens!")
            break
        
        else:
            print("❌ Ongeldige keuze. Kies 1, 2, 3 of 0.")


if __name__ == "__main__":
    main()