"Gemaakt door pascal petri "  
"Datum 18-5-2026"

import sqlite3

def connect_db():
    """Maakt verbinding met de database (maakt taken.db aan indien nodig)"""
    return sqlite3.connect("taken.db")

def init_db():
    """Initialiseert de database en maakt de tabel 'taken' aan als die nog niet bestaat"""
    conn = connect_db()
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS taken (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT NOT NULL,
            klaar INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    conn.close()

def add_taak(titel):
    """Voegt een nieuwe taak toe aan de database"""
    conn = connect_db()
    conn.execute("INSERT INTO taken (titel, klaar) VALUES (?, 0)", (titel,))
    conn.commit()
    conn.close()

def get_taken():
    """Haalt alle taken op uit de database"""
    conn = connect_db()
    rows = conn.execute("SELECT id, titel, klaar FROM taken").fetchall()
    conn.close()
    return rows

def markeer_klaar(taak_id):
    """Markeert een taak als klaar (1 = klaar)"""
    conn = connect_db()
    conn.execute("UPDATE taken SET klaar = 1 WHERE id = ?", (taak_id,))
    conn.commit()
    conn.close()

def verwijder_taak(taak_id):
    """Verwijdert een taak uit de database"""
    conn = connect_db()
    conn.execute("DELETE FROM taken WHERE id = ?", (taak_id,))
    conn.commit()
    conn.close()

def toon_taken():
    """Toont alle taken op een nette manier met status icoontjes"""
    taken = get_taken()
    
    if not taken:
        print("\n(Geen taken)")
        return
    
    print("\n📋 Overzicht van taken:")
    for taak_id, titel, klaar in taken:
        status = "✅" if klaar == 1 else "⬜"
        print(f"  {taak_id}. {status} {titel}")

def main():
    """Hoofdprogramma - de takenplanner interface"""
    # Initialiseer de database (maakt taken.db en tabel aan)
    init_db()
    
    print("🎯 Welkom bij de Takenplanner met Database!")
    
    while True:
        print("\n=== TAKENPLANNER (SQLITE) ===")
        print("1) 📋 Toon taken")
        print("2) ➕ Voeg taak toe")
        print("3) ✅ Markeer taak als klaar")
        print("4) 🗑️ Verwijder taak")
        print("0) 🚪 Stoppen")
        
        keuze = input("\nKies een optie: ").strip()
        
        if keuze == "1":
            toon_taken()
        
        elif keuze == "2":
            titel = input("Wat is de taak? ").strip()
            if titel == "":
                print("❌ Titel mag niet leeg zijn.")
            else:
                add_taak(titel)
                print(f"✅ Taak '{titel}' toegevoegd!")
        
        elif keuze == "3":
            toon_taken()
            taak_id = input("Welk ID wil je als klaar markeren? ").strip()
            if taak_id.isdigit():
                markeer_klaar(int(taak_id))
                print("🎉 Taak gemarkeerd als klaar!")
            else:
                print("❌ Ongeldig ID. Vul een nummer in.")
        
        elif keuze == "4":
            toon_taken()
            taak_id = input("Welk ID wil je verwijderen? ").strip()
            if taak_id.isdigit():
                verwijder_taak(int(taak_id))
                print("🗑️ Taak verwijderd!")
            else:
                print("❌ Ongeldig ID. Vul een nummer in.")
        
        elif keuze == "0":
            print("\n👋 Tot ziens! Je taken zijn opgeslagen in taken.db")
            break
        
        else:
            print("❌ Ongeldige keuze. Kies 0, 1, 2, 3 of 4.")

# Startpunt van het programma
if __name__ == "__main__":
    main()