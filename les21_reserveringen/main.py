"""
Hoofdprogramma voor Restaurant Reserveringssysteem
CLI interface met menu
"""

from services.manager import ReserveringManager
from services.storage import ReserveringStorage
from datetime import datetime

def vraag_int(prompt: str, min_waarde: int = 1) -> int:
    """Vraag een integer met validatie"""
    while True:
        try:
            waarde = int(input(prompt))
            if waarde >= min_waarde:
                return waarde
            print(f"Waarde moet minimaal {min_waarde} zijn.")
        except ValueError:
            print("Voer een geldig getal in.")

def vraag_datum(prompt: str = "Voer datum (YYYY-MM-DD): ") -> str:
    """Vraag een datum met validatie"""
    while True:
        datum = input(prompt).strip()
        if not datum:
            print("Datum mag niet leeg zijn.")
            continue
        
        try:
            # Probeer de datum te parsen
            datetime.strptime(datum, "%Y-%m-%d")
            return datum
        except ValueError:
            print("Ongeldig datumformaat. Gebruik YYYY-MM-DD (bv. 2026-02-06)")

def vraag_tijd(prompt: str = "Voer tijd (HH:MM): ") -> str:
    """Vraag een tijd met validatie"""
    while True:
        tijd = input(prompt).strip()
        if not tijd:
            print("Tijd mag niet leeg zijn.")
            continue
        
        try:
            datetime.strptime(tijd, "%H:%M")
            return tijd
        except ValueError:
            print("Ongeldig tijdformaat. Gebruik HH:MM (bv. 18:30)")

def toon_menu():
    """Toon het hoofdmenu"""
    print("\n" + "="*50)
    print("    RESTAURANT RESERVERINGSSYSTEEM")
    print("="*50)
    print("1. Alle reserveringen bekijken")
    print("2. Nieuwe reservering toevoegen")
    print("3. Reservering verwijderen")
    print("4. Zoeken op naam")
    print("5. Filteren op datum")
    print("6. Capaciteit bekijken")
    print("7. Stoppen")
    print("="*50)

def toon_reserveringen(manager: ReserveringManager):
    """Toon alle reserveringen met nummering"""
    reserveringen = manager.alles()
    if not reserveringen:
        print("\n📭 Geen reserveringen gevonden.")
        return
    
    print(f"\n📋 Alle reserveringen ({len(reserveringen)}):")
    print("-" * 60)
    for i, res in enumerate(reserveringen):
        print(f"{i+1:2d}. {res}")
    print("-" * 60)

def voeg_reservering_toe(manager: ReserveringManager):
    """Voeg een nieuwe reservering toe met validatie"""
    print("\n➕ Nieuwe reservering toevoegen")
    print("-" * 40)
    
    naam = input("Naam: ").strip()
    if not naam:
        print("❌ Naam mag niet leeg zijn.")
        return
    
    datum = vraag_datum()
    tijd = vraag_tijd()
    aantal = vraag_int("Aantal personen: ", 1)
    
    # Check capaciteit (optionele extra feature)
    if not manager.heeft_capaciteit(datum, tijd):
        huidig = manager.totaal_personen(datum, tijd)
        print(f"❌ Geen capaciteit meer voor {datum} om {tijd}.")
        print(f"   Huidig: {huidig} personen, Max: 30 personen")
        return
    
    if manager.voeg_toe(naam, datum, tijd, aantal):
        print(f"✅ Reservering toegevoegd voor {naam}!")
    else:
        print("❌ Kon reservering niet toevoegen. Controleer de invoer.")

def verwijder_reservering(manager: ReserveringManager):
    """Verwijder een reservering op basis van nummer"""
    toon_reserveringen(manager)
    reserveringen = manager.alles()
    if not reserveringen:
        return
    
    try:
        nummer = int(input("\nVoer het nummer van de te verwijderen reservering: "))
        index = nummer - 1
        if manager.verwijder(index):
            print(f"✅ Reservering {nummer} verwijderd!")
        else:
            print("❌ Ongeldig nummer.")
    except ValueError:
        print("❌ Voer een geldig nummer in.")

def zoek_op_naam(manager: ReserveringManager):
    """Zoek reserveringen op naam"""
    naam = input("\n🔍 Voer naam (of deel van naam) om te zoeken: ").strip()
    if not naam:
        print("❌ Voer een naam in om te zoeken.")
        return
    
    resultaten = manager.zoek_op_naam(naam)
    if not resultaten:
        print(f"📭 Geen reserveringen gevonden voor '{naam}'")
        return
    
    print(f"\n📋 Reserveringen voor '{naam}' ({len(resultaten)}):")
    print("-" * 50)
    for i, res in enumerate(resultaten, 1):
        print(f"{i}. {res}")
    print("-" * 50)

def filter_op_datum(manager: ReserveringManager):
    """Filter reserveringen op datum"""
    datum = vraag_datum("📅 Voer datum om te filteren (YYYY-MM-DD): ")
    resultaten = manager.filter_op_datum(datum)
    
    if not resultaten:
        print(f"📭 Geen reserveringen gevonden voor {datum}")
        return
    
    print(f"\n📋 Reserveringen op {datum} ({len(resultaten)}):")
    print("-" * 50)
    for i, res in enumerate(resultaten, 1):
        print(f"{i}. {res}")
    print("-" * 50)

def toon_capaciteit(manager: ReserveringManager):
    """Toon de capaciteit voor een datum/tijd"""
    print("\n📊 Capaciteit bekijken")
    print("-" * 40)
    datum = vraag_datum()
    tijd = vraag_tijd()
    
    huidig = manager.totaal_personen(datum, tijd)
    max_personen = 30
    beschikbaar = max_personen - huidig
    
    print(f"\n📅 {datum} om {tijd}")
    print(f"👥 Huidig: {huidig} personen")
    print(f"📊 Beschikbaar: {beschikbaar} personen")
    print(f"🔢 Maximaal: {max_personen} personen")
    
    if beschikbaar <= 0:
        print("⚠️  VOL! Geen capaciteit meer beschikbaar.")
    elif beschikbaar < 5:
        print(f"⚠️  Nog maar {beschikbaar} plaatsen beschikbaar!")

def main():
    """Hoofdprogramma loop"""
    # Initialiseer storage en manager
    storage = ReserveringStorage("reserveringen.json")
    manager = ReserveringManager(storage)
    
    print("🔄 Bestaande reserveringen geladen...")
    
    while True:
        toon_menu()
        keuze = input("\nKies een optie (1-7): ").strip()
        
        if keuze == "1":
            toon_reserveringen(manager)
        elif keuze == "2":
            voeg_reservering_toe(manager)
        elif keuze == "3":
            verwijder_reservering(manager)
        elif keuze == "4":
            zoek_op_naam(manager)
        elif keuze == "5":
            filter_op_datum(manager)
        elif keuze == "6":
            toon_capaciteit(manager)
        elif keuze == "7":
            print("\n👋 Tot ziens! Bedankt voor het gebruik van het reserveringssysteem.")
            break
        else:
            print("❌ Ongeldige keuze. Kies een nummer van 1 tot 7.")
        
        input("\nDruk op Enter om door te gaan...")

if __name__ == "__main__":
    main()