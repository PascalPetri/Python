"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Winkelmandje class voor beheren winkelwagen
"""

from .product import Product

class Winkelmandje:
    """Een winkelmandje voor het verzamelen van producten."""
    
    def __init__(self):
        """Initialiseer een leeg winkelmandje."""
        self.items = []  # Lijst met tuples (product, aantal)
    
    def voeg_toe(self, product, aantal):
        """
        Voeg een product toe aan het winkelmandje.
        
        Args:
            product (Product): Het product om toe te voegen
            aantal (int): Het aantal
        """
        if not product.is_op_voorraad(aantal):
            print(f"❌ Niet genoeg voorraad van {product.naam}")
            return False
        
        # Check of product al in mandje zit
        for i, (p, a) in enumerate(self.items):
            if p.naam == product.naam:
                self.items[i] = (p, a + aantal)
                print(f"✅ {aantal}x {product.naam} toegevoegd (totaal: {a + aantal})")
                return True
        
        # Nieuw product toevoegen
        self.items.append((product, aantal))
        print(f"✅ {aantal}x {product.naam} toegevoegd")
        return True
    
    def totaal_prijs(self):
        """
        Bereken de totale prijs van het winkelmandje.
        
        Returns:
            float: Totale prijs
        """
        totaal = sum(product.prijs * aantal for product, aantal in self.items)
        return totaal
    
    def toon(self):
        """Toon de inhoud van het winkelmandje."""
        if not self.items:
            print("🛒 Winkelmandje is leeg.")
            return
        
        print("\n" + "=" * 50)
        print("🛒 INHOUD WINKELMANDJE")
        print("=" * 50)
        for i, (product, aantal) in enumerate(self.items, 1):
            subtotaal = product.prijs * aantal
            print(f"{i}. {product.naam} x{aantal} = €{subtotaal:.2f}")
        print("-" * 50)
        print(f"Totaal: €{self.totaal_prijs():.2f}")
        print("=" * 50 + "\n")
    
    def leeg(self):
        """Leeg het winkelmandje."""
        self.items = []
        print("🛒 Winkelmandje is geleegd.")
    
    def __len__(self):
        """Aantal verschillende producten in mandje."""
        return len(self.items)