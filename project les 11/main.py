"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Hoofdprogramma voor producten en winkelmandje
"""

import json
from pathlib import Path
from shop.product import Product
from shop.mandje import Winkelmandje


def save_producten(producten, filename):
    """Sla producten op in een JSON-bestand."""
    data = [p.to_dict() for p in producten]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Producten opgeslagen in {filename}")


def load_producten(filename):
    """Laad producten uit een JSON-bestand."""
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
    """Vraag een integer aan de gebruiker met foutafhandeling."""
    while True:
        try:
            waarde = int(input(prompt))
            if waarde < 0:
                print("❌ Voer een positief getal in.")
                continue
            return waarde
        except ValueError:
            print("❌ Ongeldige invoer. Voer een geheel getal in.")


def vraag_float(prompt):
    """Vraag een float aan de gebruiker met foutafhandeling."""
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
    """Toon alle producten op het scherm."""
    if not producten:
        print("📦 Geen producten gevonden.")
        return
    
    print("\n" + "=" * 60)
    print("📋 OVERZICHT PRODUCTEN")
    print("=" * 60)
    print(f"{'#':<3} {'Product':<20} {'Prijs':<10} {'Voorraad':<10}")
    print("-" * 60)
    for i, product in enumerate(producten, 1):
        print(f"{i:<3} {product.naam:<20} €{product.prijs:<9.2f} {product._voorraad:<10}")
    print("=" * 60 + "\n")


def voeg_standaard_producten_toe(producten):
    """Voeg standaard testproducten toe als er geen producten zijn."""
    print("📦 Geen opgeslagen producten gevonden. Starten met testproducten.")
    
    test_producten = [
        Product("Gaming Laptop", 899.00, 5),
        Product("Office Laptop", 599.00, 8),
        Product("Gaming Muis", 45.00, 15),
        Product("Draadloze Muis", 25.00, 20),
        Product("Mechanisch Toetsenbord", 89.00, 10),
        Product("Standaard Toetsenbord", 35.00, 12),
        Product("27 inch Monitor", 249.00, 4),
        Product("24 inch Monitor", 179.00, 6),
        Product("iPad Tablet", 499.00, 3),
        Product("Samsung Tablet", 399.00, 5),
        Product("USB-C HUB", 45.00, 15),
        Product("Externe SSD 1TB", 120.00, 7),
        Product("Webcam HD", 65.00, 9),
        Product("Hoofdtelefoon", 85.00, 12),
        Product("Laptop Stand", 35.00, 20),
        Product("Laptop Tas", 55.00, 8),
        Product("HDMI Kabel", 12.50, 30),
        Product("Stroomadapter", 45.00, 10),
        Product("Printer", 199.00, 3),
        Product("Scanner", 149.00, 2)
    ]
    
    producten.extend(test_producten)
    print(f"✅ {len(test_producten)} testproducten toegevoegd!")
    return producten


def main():
    """Hoofdfunctie van het programma."""
    filename = "producten.json"
    
    # Laad bestaande producten of start met lege lijst
    producten = load_producten(filename)
    
    # Als er geen producten zijn, voeg testproducten toe
    if not producten:
        producten = voeg_standaard_producten_toe(producten)
        # Sla testproducten direct op
        save_producten(producten, filename)
    
    # Maak een nieuw winkelmandje
    mandje = Winkelmandje()
    
    while True:
        print("\n" + "=" * 50)
        print("🛒 PRODUCTEN BEHEER - SHOP SYSTEEM")
        print("=" * 50)
        print("1. 📋 Toon alle producten")
        print("2. ➕ Nieuw product toevoegen")
        print("3. 🛍️ Toon winkelmandje")
        print("4. 🛒 Product toevoegen aan mandje")
        print("5. 💾 Opslaan")
        print("6. 🔄 Testproducten resetten")
        print("0. 🚪 Stoppen")
        print("=" * 50)
        
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
            mandje.toon()
        
        elif keuze == "4":
            if not producten:
                print("📦 Geen producten beschikbaar.")
                continue
            
            toon_producten(producten)
            nummer = vraag_int("Productnummer: ") - 1
            
            if 0 <= nummer < len(producten):
                product = producten[nummer]
                print(f"\n📦 {product.naam}")
                print(f"   Prijs: €{product.prijs:.2f}")
                print(f"   Beschikbaar: {product._voorraad}")
                aantal = vraag_int(f"Aantal: ")
                
                if aantal > 0:
                    mandje.voeg_toe(product, aantal)
                else:
                    print("❌ Aantal moet groter zijn dan 0.")
            else:
                print("❌ Ongeldig productnummer.")
        
        elif keuze == "5":
            save_producten(producten, filename)
        
        elif keuze == "6":
            print("\n🔄 Testproducten resetten...")
            bevestiging = input("Weet je zeker dat je alle producten wilt resetten? (j/n): ")
            if bevestiging.lower() == "j":
                producten = []
                producten = voeg_standaard_producten_toe(producten)
                save_producten(producten, filename)
                mandje.leeg()
                print("✅ Producten gereset naar testproducten!")
            else:
                print("❌ Reset geannuleerd.")
        
        elif keuze == "0":
            print("\n💾 Opslaan voor het afsluiten...")
            save_producten(producten, filename)
            print("👋 Programma afgesloten. Tot ziens!")
            break
        
        else:
            print("❌ Ongeldige keuze. Kies 1, 2, 3, 4, 5, 6 of 0.")


if __name__ == "__main__":
    main()