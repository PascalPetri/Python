# gemaakt door: Pascal Petri 
# Datum: 4-6-2026

import json
import hashlib
from pathlib import Path


# hulpfunties &wachtwoorden

def hash_password(wachtwoord):
    """Maak een veilige hash van een wachtwoord"""
    return hashlib.sha256(wachtwoord.encode("utf-8")).hexdigest()

def check_password(wachtwoord, hash_waarde):
    """Controleer of wachtwoord klopt met de hash"""
    return hash_password(wachtwoord) == hash_waarde



# Bestandsfunties  & users

def laad_users():
    """Laad gebruikers uit users.json"""
    pad = Path("users.json")
    if not pad.exists():
        return []
    return json.loads(pad.read_text(encoding="utf-8"))

def bewaar_users(users):
    """Bewaar gebruikers in users.json"""
    Path("users.json").write_text(json.dumps(users, indent=2), encoding="utf-8")

def maak_standaard_users():
    """Maak standaard admin en user aan als bestand nog niet bestaat"""
    if Path("users.json").exists():
        return
    
    users = [
        {"username": "admin", "password_hash": hash_password("admin123"), "role": "admin"},
        {"username": "user",  "password_hash": hash_password("user123"),  "role": "user"}
    ]
    bewaar_users(users)
    print("✅ Standaard accounts aangemaakt!")


# inloggen

def login():
    """Vraag gebruikersnaam en wachtwoord, geef ingelogde gebruiker terug"""
    print("\n" + "=" * 40)
    print("           I N L O G G E N")
    print("=" * 40)
    
    gebruikersnaam = input("Gebruikersnaam: ").strip()
    wachtwoord = input("Wachtwoord: ").strip()
    
    users = laad_users()
    
    # Zoek gebruiker
    for user in users:
        if user["username"] == gebruikersnaam:
            if check_password(wachtwoord, user["password_hash"]):
                print(f"\n✅ Welkom {user['username']} (rol: {user['role']})")
                return user
            else:
                print("\n❌ Wachtwoord onjuist!")
                return None
    
    print("\n❌ Gebruiker niet gevonden!")
    return None



# Bestandsfunties 

def laad_taken():
    """Laad taken uit taken.json"""
    pad = Path("taken.json")
    if not pad.exists():
        return []
    return json.loads(pad.read_text(encoding="utf-8"))

def bewaar_taken(taken):
    """Bewaar taken in taken.json"""
    Path("taken.json").write_text(json.dumps(taken, indent=2), encoding="utf-8")



# taken filteren & tonen


def filter_taken_voor_user(taken, huidige_user):
    """Filter taken: admin ziet alles, user alleen eigen taken"""
    if huidige_user["role"] == "admin":
        return taken
    else:
        return [t for t in taken if t["owner"] == huidige_user["username"]]

def toon_taken(taken, huidige_user):
    """Toon taken op het scherm"""
    zichtbare_taken = filter_taken_voor_user(taken, huidige_user)
    
    print("\n" + "=" * 50)
    print("                    T A K E N")
    print("=" * 50)
    
    if not zichtbare_taken:
        print("   📭 Geen taken gevonden")
        return zichtbare_taken
    
    for i, taak in enumerate(zichtbare_taken, 1):
        vinkje = "✅" if taak["klaar"] else "⬜"
        eigenaar_info = f" [eigenaar: {taak['owner']}]" if huidige_user["role"] == "admin" else ""
        print(f"   {i}. {vinkje} {taak['titel']}{eigenaar_info}")
    
    return zichtbare_taken

# taken en bewerken

def voeg_taak_toe(taken, huidige_user):
    """Voeg een nieuwe taak toe voor de ingelogde gebruiker"""
    print("\n" + "=" * 40)
    print("        N I E U W E   T A A K")
    print("=" * 40)
    
    titel = input("Taak: ").strip()
    
    if not titel:
        print("❌ Taak mag niet leeg zijn!")
        return
    
    nieuwe_taak = {
        "titel": titel,
        "klaar": False,
        "owner": huidige_user["username"]
    }
    
    taken.append(nieuwe_taak)
    bewaar_taken(taken)
    print(f"✅ '{titel}' toegevoegd!")

def markeer_als_klaar(taken, huidige_user):
    """Markeer een taak als afgerond"""
    zichtbaar = toon_taken(taken, huidige_user)
    
    if not zichtbaar:
        return
    
    try:
        nummer = int(input("\nNummer om af te vinken: ")) - 1
        
        if 0 <= nummer < len(zichtbaar):
            taak = zichtbaar[nummer]
            
            # Zoek de echte taak in de volledige lijst
            for t in taken:
                if t["titel"] == taak["titel"] and t["owner"] == taak["owner"]:
                    t["klaar"] = True
                    break
            
            bewaar_taken(taken)
            print(f"✅ '{taak['titel']}' afgerond!")
        else:
            print("❌ Ongeldig nummer!")
    except ValueError:
        print("❌ Voer een geldig nummer in!")

def verwijder_taak(taken, huidige_user):
    """Verwijder een taak"""
    zichtbaar = toon_taken(taken, huidige_user)
    
    if not zichtbaar:
        return
    
    try:
        nummer = int(input("\nNummer om te verwijderen: ")) - 1
        
        if 0 <= nummer < len(zichtbaar):
            taak = zichtbaar[nummer]
            
            # Zoek en verwijder de echte taak
            for i, t in enumerate(taken):
                if t["titel"] == taak["titel"] and t["owner"] == taak["owner"]:
                    verwijderd = taken.pop(i)
                    break
            
            bewaar_taken(taken)
            print(f"🗑️ '{verwijderd['titel']}' verwijderd!")
        else:
            print("❌ Ongeldig nummer!")
    except ValueError:
        print("❌ Voer een geldig nummer in!")


#  menu & main

def toon_menu(huidige_user):
    """Toon het menu op basis van de rol"""
    print("\n" + "=" * 40)
    print(f"   M E N U   -   {huidige_user['role'].upper()}")
    print("=" * 40)
    print("   1. 📋 Toon alle taken")
    print("   2. ➕ Nieuwe taak")
    print("   3. ✅ Afvinken")
    print("   4. 🗑️  Verwijderen")
    print("   0. 🚪 Uitloggen")

def main():
    """Hoofdprogramma"""
    print("\n" + "=" * 40)
    print("    T A K E N B E H E E R")
    print("=" * 40)
    
    # Zorg dat er standaard accounts zijn
    maak_standaard_users()
    
    # Inloggen
    huidige_user = login()
    if not huidige_user:
        print("\nProgramma wordt afgesloten...")
        return
    
    # Laad taken
    taken = laad_taken()
    
    # Hoofdmenu loop
    while True:
        toon_menu(huidige_user)
        keuze = input("\nJouw keuze: ").strip()
        
        if keuze == "1":
            toon_taken(taken, huidige_user)
        
        elif keuze == "2":
            voeg_taak_toe(taken, huidige_user)
        
        elif keuze == "3":
            markeer_als_klaar(taken, huidige_user)
        
        elif keuze == "4":
            verwijder_taak(taken, huidige_user)
        
        elif keuze == "0":
            print(f"\n👋 Tot ziens, {huidige_user['username']}!")
            break
        
        else:
            print("❌ Ongeldige keuze!")



# start hier 

if __name__ == "__main__":
    main()