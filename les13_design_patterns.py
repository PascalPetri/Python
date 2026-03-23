"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Design Patterns - Factory en Strategy
"""

# ============================================
#   Product class
# ============================================

class Product:
    """Een eenvoudige productklasse."""
    
    def __init__(self, naam, prijs):
        """
        Initialiseer een nieuw product.
        
        Args:
            naam (str): De naam van het product
            prijs (float): De prijs van het product
        """
        self.naam = naam
        self.prijs = prijs
    
    def __str__(self):
        """Leesbare weergave van product."""
        return f"{self.naam} - €{self.prijs:.2f}"


# ============================================
# ProductFactory (Factory Pattern)
# ============================================

class ProductFactory:
    """
    Factory voor het maken van producten.
    Centrale plek waar producten worden aangemaakt.
    """
    
    def maak_product(self, soort):
        """
        Maak een product op basis van de soort.
        
        Args:
            soort (str): Het type product ('laptop', 'muis', 'toetsenbord', etc.)
            
        Returns:
            Product: Een nieuw product-object
            
        Raises:
            ValueError: Als de soort onbekend is
        """
        soort = soort.lower()
        
        if soort == "laptop":
            return Product("Laptop", 899.00)
        elif soort == "gaming laptop":
            return Product("Gaming Laptop", 1299.00)
        elif soort == "office laptop":
            return Product("Office Laptop", 599.00)
        elif soort == "muis":
            return Product("Muis", 25.00)
        elif soort == "gaming muis":
            return Product("Gaming Muis", 45.00)
        elif soort == "draadloze muis":
            return Product("Draadloze Muis", 35.00)
        elif soort == "toetsenbord":
            return Product("Toetsenbord", 59.00)
        elif soort == "mechanisch toetsenbord":
            return Product("Mechanisch Toetsenbord", 89.00)
        elif soort == "monitor":
            return Product("Monitor", 199.99)
        elif soort == "27 inch monitor":
            return Product("27 inch Monitor", 249.00)
        elif soort == "tablet":
            return Product("Tablet", 399.00)
        elif soort == "hoofdtelefoon":
            return Product("Hoofdtelefoon", 85.00)
        elif soort == "webcam":
            return Product("Webcam", 65.00)
        elif soort == "externe ssd":
            return Product("Externe SSD", 120.00)
        else:
            # Ongeldige soort - foutmelding geven
            raise ValueError(f"Onbekende productsoort: '{soort}'. Beschikbaar: laptop, muis, toetsenbord, monitor, tablet, etc.")


# ============================================
#  KortingRegel (Strategy Pattern)
# ============================================

class KortingRegel:
    """
    Interface voor kortingsregels (Strategy).
    Elke kortingsregel moet een pas_toe() methode hebben.
    """
    
    def pas_toe(self, totaal):
        """
        Bereken de korting op basis van het totaalbedrag.
        
        Args:
            totaal (float): Het subtotaal van de kassa
            
        Returns:
            float: Het kortingsbedrag
        """
        raise NotImplementedError("Elke kortingsregel moet pas_toe() implementeren")


class GeenKorting(KortingRegel):
    """Geen korting (altijd €0 korting)."""
    
    def pas_toe(self, totaal):
        """Geef altijd €0 korting."""
        return 0.00


class TienProcentBoven500(KortingRegel):
    """10% korting als totaal boven €500 is."""
    
    def pas_toe(self, totaal):
        """Geef 10% korting bij bedragen boven €500."""
        if totaal > 500:
            return totaal * 0.10
        return 0.00


class VijfProcentBoven100(KortingRegel):
    """5% korting als totaal boven €100 is."""
    
    def pas_toe(self, totaal):
        """Geef 5% korting bij bedragen boven €100."""
        if totaal > 100:
            return totaal * 0.05
        return 0.00


class TwintigProcentKorting(KortingRegel):
    """20% korting op alles."""
    
    def pas_toe(self, totaal):
        """Geef altijd 20% korting."""
        return totaal * 0.20


class Studentenkorting(KortingRegel):
    """15% korting, maximaal €50."""
    
    def pas_toe(self, totaal):
        """Geef 15% korting met maximum van €50."""
        korting = totaal * 0.15
        return min(korting, 50.00)


# ============================================
# Kassa class
# ============================================

class Kassa:
    """
    Kassa class die producten verzamelt en eindbedrag berekent.
    Gebruikt een kortingsregel (Strategy) voor de korting.
    """
    
    def __init__(self, korting_regel):
        """
        Initialiseer een nieuwe kassa.
        
        Args:
            korting_regel (KortingRegel): De kortingsregel die wordt toegepast
        """
        self.producten = []
        self.korting_regel = korting_regel
    
    def voeg_toe(self, product):
        """
        Voeg een product toe aan de kassa.
        
        Args:
            product (Product): Het product om toe te voegen
        """
        self.producten.append(product)
        print(f"➕ Toegevoegd: {product}")
    
    def totaal(self):
        """
        Bereken het subtotaal van alle producten.
        
        Returns:
            float: Som van alle productprijzen
        """
        return sum(product.prijs for product in self.producten)
    
    def korting(self):
        """
        Bereken de korting met de ingestelde kortingsregel.
        
        Returns:
            float: Het kortingsbedrag
        """
        return self.korting_regel.pas_toe(self.totaal())
    
    def eindbedrag(self):
        """
        Bereken het eindbedrag (totaal - korting).
        
        Returns:
            float: Het te betalen bedrag
        """
        return self.totaal() - self.korting()
    
    def toon_bon(self):
        """
        Toon een bon met alle producten en bedragen.
        """
        print("\n" + "=" * 50)
        print("🛍️  BON")
        print("=" * 50)
        
        if not self.producten:
            print("Geen producten in kassa.")
            return
        
        for i, product in enumerate(self.producten, 1):
            print(f"{i}. {product}")
        
        print("-" * 50)
        print(f"Subtotaal: €{self.totaal():.2f}")
        print(f"Korting:   -€{self.korting():.2f}")
        print(f"Eindbedrag: €{self.eindbedrag():.2f}")
        print("=" * 50)
        print(f"Kortingregel: {self.korting_regel.__class__.__name__}")
        print("=" * 50 + "\n")
    
    def reset(self):
        """Leeg de kassa."""
        self.producten = []
        print("🔄 Kassa geleegd.")


# ============================================
# STAP 6: Demo / Test
# ============================================

def demo():
    """Demo van Factory en Strategy patterns."""
    
    print("\n" + "=" * 60)
    print("🏭 DESIGN PATTERNS DEMO - Factory & Strategy")
    print("=" * 60)
    
    # Maak de factory aan
    factory = ProductFactory()
    
    print("\n📦 Producten gemaakt via Factory:")
    print("-" * 40)
    
    # Maak producten via de factory
    try:
        laptop = factory.maak_product("laptop")
        print(f"✓ Gemaakt: {laptop}")
        
        muis = factory.maak_product("muis")
        print(f"✓ Gemaakt: {muis}")
        
        toetsenbord = factory.maak_product("toetsenbord")
        print(f"✓ Gemaakt: {toetsenbord}")
        
        gaming_muis = factory.maak_product("gaming muis")
        print(f"✓ Gemaakt: {gaming_muis}")
        
        monitor = factory.maak_product("monitor")
        print(f"✓ Gemaakt: {monitor}")
        
        # Probeer een onbekend product (gaat een fout geven)
        # onbekend = factory.maak_product("fiets")  # Uncomment om te testen
        
    except ValueError as e:
        print(f"❌ Fout: {e}")
    
    # ============================================
    # DEMO 1: Geen korting
    # ============================================
    print("\n" + "=" * 60)
    print("💰 DEMO 1: Kassa met GEEN KORTING")
    print("=" * 60)
    
    kassa1 = Kassa(GeenKorting())
    kassa1.voeg_toe(laptop)
    kassa1.voeg_toe(muis)
    kassa1.voeg_toe(toetsenbord)
    kassa1.toon_bon()
    
    # ============================================
    # DEMO 2: 10% korting boven €500
    # ============================================
    print("\n" + "=" * 60)
    print("💰 DEMO 2: Kassa met 10% KORTING BOVEN €500")
    print("=" * 60)
    
    kassa2 = Kassa(TienProcentBoven500())
    kassa2.voeg_toe(laptop)           # €899
    kassa2.voeg_toe(gaming_muis)      # €45
    kassa2.voeg_toe(monitor)          # €200
    kassa2.toon_bon()
    
    # ============================================
    # DEMO 3: 5% korting boven €100
    # ============================================
    print("\n" + "=" * 60)
    print("💰 DEMO 3: Kassa met 5% KORTING BOVEN €100")
    print("=" * 60)
    
    kassa3 = Kassa(VijfProcentBoven100())
    kassa3.voeg_toe(toetsenbord)      # €59
    kassa3.voeg_toe(gaming_muis)      # €45
    kassa3.voeg_toe(muis)             # €25
    kassa3.toon_bon()                 # Totaal €129 -> 5% korting
    
    # ============================================
    # DEM0 4: 20% korting op alles
    # ============================================
    print("\n" + "=" * 60)
    print("💰 DEMO 4: Kassa met 20% KORTING OP ALLES")
    print("=" * 60)
    
    kassa4 = Kassa(TwintigProcentKorting())
    kassa4.voeg_toe(laptop)           # €899
    kassa4.voeg_toe(monitor)          # €200
    kassa4.toon_bon()                 # Totaal €1099 -> 20% korting = €219.80
    
    # ============================================
    # DEMO 5: Studentenkorting (max €50)
    # ============================================
    print("\n" + "=" * 60)
    print("💰 DEMO 5: Kassa met STUDENTENKORTING (max €50)")
    print("=" * 60)
    
    kassa5 = Kassa(Studentenkorting())
    kassa5.voeg_toe(laptop)           # €899
    kassa5.voeg_toe(toetsenbord)      # €59
    kassa5.voeg_toe(gaming_muis)      # €45
    kassa5.toon_bon()                 # Totaal €1003 -> 15% = €150.45 maar max €50
    
    # ============================================
    # DEMO 6: Kortingregel wisselen tijdens gebruik
    # ============================================
    print("\n" + "=" * 60)
    print("💰 DEMO 6: KORTINGREGEL WISSELEN (Strategy in actie)")
    print("=" * 60)
    
    kassa6 = Kassa(GeenKorting())
    
    print("\n📦 Producten toevoegen:")
    kassa6.voeg_toe(laptop)           # €899
    kassa6.voeg_toe(monitor)          # €200
    
    print(f"\n📊 Subtotaal: €{kassa6.totaal():.2f}")
    
    print("\n🔄 Wissel naar 20% korting:")
    kassa6.korting_regel = TwintigProcentKorting()
    print(f"   Korting: €{kassa6.korting():.2f}")
    print(f"   Eindbedrag: €{kassa6.eindbedrag():.2f}")
    
    print("\n🔄 Wissel naar studentenkorting:")
    kassa6.korting_regel = Studentenkorting()
    print(f"   Korting: €{kassa6.korting():.2f}")
    print(f"   Eindbedrag: €{kassa6.eindbedrag():.2f}")
    
    print("\n🔄 Wissel naar geen korting:")
    kassa6.korting_regel = GeenKorting()
    print(f"   Korting: €{kassa6.korting():.2f}")
    print(f"   Eindbedrag: €{kassa6.eindbedrag():.2f}")
    
    # ============================================
    # SAMENVATTING
    # ============================================
    print("\n" + "=" * 60)
    print("📚 SAMENVATTING DESIGN PATTERNS")
    print("=" * 60)
    print("\n🏭 FACTORY PATTERN:")
    print("   - ProductFactory maakt alle producten centraal aan")
    print("   - Eén plek om producten te maken en aan te passen")
    print("   - Makkelijk nieuwe producten toevoegen")
    
    print("\n🎯 STRATEGY PATTERN:")
    print("   - KortingRegel is de interface (Strategy)")
    print("   - Verschillende kortingsregels: GeenKorting, 10% boven €500, etc.")
    print("   - Kassa kan kortingregel eenvoudig wisselen")
    print("   - Nieuwe kortingregels toevoegen zonder Kassa aan te passen")
    
    print("\n✅ Voordelen:")
    print("   - Code is overzichtelijk en gestructureerd")
    print("   - Makkelijk uitbreidbaar met nieuwe producten en kortingen")
    print("   - Geen herhaling van code (DRY - Don't Repeat Yourself)")
    print("=" * 60)


# ============================================
# START PUNT
# ============================================

if __name__ == "__main__":
    demo()