# Gemaakt door Pascal Petri
# Datum 12-2-2026

# zorgt voor de  datum & tijd
import datetime

#product klas zorgt voor namen en prijs
class Product:
    """Klasse voor producten in de webshop"""
    
    def __init__(self, naam, prijs, voorraad):
        self.naam = naam
        self.prijs = prijs
        self._voorraad = voorraad  # underscore = 'protected', niet direct wijzigen
    
    def toon_info(self):
        """Print productinformatie op een nette manier"""
        voorraad_status = self._voorraad if self._voorraad > 0 else "UITVERKOCHT"
        print(f"{self.naam} - €{self.prijs:.2f} (voorraad: {voorraad_status})")
    
    def is_op_voorraad(self, aantal=1):
        """Controleer of er genoeg voorraad is voor het gewenste aantal"""
        return self._voorraad >= aantal
    
    def verlaag_voorraad(self, aantal):
        """Verlaag voorraad als dat mogelijk is, retourneer True/False"""
        if aantal <= 0:
            print("❌ Aantal moet groter dan 0 zijn.")
            return False
        if not self.is_op_voorraad(aantal):
            print(f"❌ Niet genoeg voorraad. Nog {self._voorraad} beschikbaar.")
            return False
        
        self._voorraad -= aantal
        return True
    
    @property
    def voorraad(self):
        """Getter voor voorraad - read-only van buitenaf"""
        return self._voorraad


class Winkelmandje:
    """Klasse voor het winkelmandje van de klant"""
    
    def __init__(self):
        self.items = []  # Lijst van tuples: (product, aantal)
    
    def voeg_toe(self, product, aantal=1):
        """Voeg product met aantal toe aan winkelmandje"""
        if aantal <= 0:
            print("❌ Aantal moet groter dan 0 zijn.")
            return
        
        if not product.is_op_voorraad(aantal):
            print(f"❌ Sorry, er zijn maar {product.voorraad} stuks van {product.naam} beschikbaar.")
            return
        
        # Controleer of product al in mandje zit
        for i, (p, a) in enumerate(self.items):
            if p.naam == product.naam:
                # Product al aanwezig -> aantal verhogen
                self.items[i] = (p, a + aantal)
                print(f"✅ {aantal}x {product.naam} toegevoegd. Nu totaal {a + aantal} stuks.")
                return
        
        # Nieuw product toevoegen
        self.items.append((product, aantal))
        print(f"✅ {aantal}x {product.naam} toegevoegd aan winkelmandje.")
    
    def toon_mandje(self):
        """Toon alle items in het winkelmandje"""
        if not self.items:
            print("🛒 Winkelmandje is leeg.")
            return
        
        print("\n" + "=" * 50)
        print("🛍️  JE WINKELMANDJE")
        print("=" * 50)
        
        for i, (product, aantal) in enumerate(self.items, 1):
            subtotaal = product.prijs * aantal
            print(f"{i}. {product.naam} x{aantal} - €{product.prijs:.2f} p/st = €{subtotaal:.2f}")
        
        print("=" * 50)
    
    def totaal_prijs(self):
        """Bereken totaalprijs van alle items"""
        totaal = sum(product.prijs * aantal for product, aantal in self.items)
        return totaal
    
    def leegmaken(self):
        """Maak het mandje leeg"""
        self.items = []
        print("🧹 Winkelmandje is leeggemaakt.")


def toon_producten(producten):
    """Toon alle beschikbare producten met nummer"""
    print("\n" + "=" * 50)
    print("📦 BESCHIKBARE PRODUCTEN")
    print("=" * 50)
    for i, product in enumerate(producten, 1):
        print(f"{i}. ", end="")
        product.toon_info()


def reken_af(mandje, producten):
    """Reken af met korting en bonnetje"""
    if not mandje.items:
        print("🛒 Je mandje is leeg. Voeg eerst producten toe.")
        return
    
    print("\n" + "=" * 50)
    print("💳 AFREKENEN")
    print("=" * 50)
    
    # Check voorraad voor alle items
    for product, aantal in mandje.items:
        if not product.is_op_voorraad(aantal):
            print(f"❌ {product.naam}: nog maar {product.voorraad} op voorraad, jij wilt {aantal}.")
            print("   Afrekenen geannuleerd.")
            return
    
    # Voorraad verlagen
    for product, aantal in mandje.items:
        if product.verlaag_voorraad(aantal):
            print(f"✅ {aantal}x {product.naam} gekocht. Nieuwe voorraad: {product.voorraad}")
    
    # Bereken totaal
    subtotaal = mandje.totaal_prijs()
    korting = 0
    
    # Opdracht 2: 10% korting boven €500
    if subtotaal > 500:
        korting = subtotaal * 0.10
        print(f"🎉 Korting (10%): -€{korting:.2f}")
    
    totaal = subtotaal - korting
    
    print(f"\n💰 Subtotaal: €{subtotaal:.2f}")
    print(f"💰 Te betalen: €{totaal:.2f}")
    
    # Opdracht 3: Bonnetje opslaan
    maak_bonnetje(mandje, subtotaal, korting, totaal)
    
    print("\n✅ Afrekenen gelukt! Bedankt voor je aankoop.")
    mandje.leegmaken()


def maak_bonnetje(mandje, subtotaal, korting, totaal):
    """Opdracht 3: Sla bonnetje op in tekstbestand"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bestandsnaam = f"bonnetje_{timestamp}.txt"
    
    with open(bestandsnaam, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("🛍️  BONNETJE\n")
        f.write(f"Datum: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
        f.write("=" * 50 + "\n\n")
        
        for product, aantal in mandje.items:
            subtotaal_item = product.prijs * aantal
            f.write(f"{product.naam} x{aantal:2d}  €{product.prijs:.2f}  =  €{subtotaal_item:.2f}\n")
        
        f.write("\n" + "-" * 50 + "\n")
        f.write(f"Subtotaal:          €{subtotaal:.2f}\n")
        
        if korting > 0:
            f.write(f"Korting (10%):     -€{korting:.2f}\n")
        
        f.write(f"TOTAAL:            €{totaal:.2f}\n")
        f.write("=" * 50 + "\n")
        f.write("Bedankt voor je aankoop!\n")
    
    print(f"🧾 Bonnetje opgeslagen als: {bestandsnaam}")


def main():
    """Hoofdprogramma met menu-loop"""
    # Startproducten
    producten = [
        Product("Laptop", 899.00, 3),
        Product("Muis", 25.50, 10),
        Product("Toetsenbord", 59.95, 5),
        Product("Monitor", 249.00, 2),
        Product("Webcam", 79.99, 4)
    ]
    
    mandje = Winkelmandje()
    
    print("\n" + "=" * 50)
    print("🏪 WELKOM BIJ DE MINI-WEBSHOP")
    print("=" * 50)
    
    while True:
        print("\n" + "-" * 50)
        print("📋 MENU")
        print("-" * 50)
        print("1. 📦 Producten bekijken")
        print("2. ➕ Product toevoegen aan mandje")
        print("3. 🛒 Winkelmandje bekijken")
        print("4. 💳 Afrekenen")
        print("0. 🚪 Stoppen")
        print("-" * 50)
        
        keuze = input("Kies een optie: ").strip()
        
        if keuze == "1":
            toon_producten(producten)
            
        elif keuze == "2":
            toon_producten(producten)
            
            try:
                product_nr = int(input("\nKies productnummer: ")) - 1
                if 0 <= product_nr < len(producten):
                    product = producten[product_nr]
                    
                    # Opdracht 1: Vraag om aantal
                    aantal = input(f"Aantal {product.naam} (Enter = 1): ").strip()
                    if aantal == "":
                        aantal = 1
                    else:
                        aantal = int(aantal)
                    
                    mandje.voeg_toe(product, aantal)
                else:
                    print("❌ Ongeldig productnummer.")
            except ValueError:
                print("❌ Voer een geldig nummer in.")
            
        elif keuze == "3":
            mandje.toon_mandje()
            if mandje.items:
                print(f"💰 Totaal: €{mandje.totaal_prijs():.2f}")
            
        elif keuze == "4":
            reken_af(mandje, producten)
            
        elif keuze == "0":
            print("👋 Bedankt voor je bezoek! Tot ziens.")
            break
            
        else:
            print("❌ Ongeldige keuze. Probeer opnieuw.")


if __name__ == "__main__":
    main()