"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Logica voor producten en winkelmandje (te testen met unittest)
"""

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
        self.voorraad = voorraad
    
    def verlaag_voorraad(self, aantal):
        """
        Verlaag de voorraad met een bepaald aantal.
        
        Args:
            aantal (int): Aantal om te verlagen
            
        Returns:
            bool: True als gelukt, False als niet genoeg voorraad of ongeldig aantal
        """
        # Controleer of aantal geldig is (positief en niet groter dan voorraad)
        if aantal <= 0:
            return False
        if aantal > self.voorraad:
            return False
        
        # Verlaag voorraad
        self.voorraad -= aantal
        return True
    
    def is_op_voorraad(self, aantal=1):
        """
        Controleer of product op voorraad is.
        
        Args:
            aantal (int): Gevraagd aantal
            
        Returns:
            bool: True als op voorraad, anders False
        """
        return self.voorraad >= aantal and aantal > 0
    
    def toon_info(self):
        """Toon productinformatie."""
        return f"{self.naam} - €{self.prijs:.2f} - Voorraad: {self.voorraad}"
    
    def __str__(self):
        """Maak een leesbare weergave van het product."""
        return f"{self.naam} - €{self.prijs:.2f} - Voorraad: {self.voorraad}"


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
            
        Returns:
            bool: True als toevoegen gelukt is, anders False
        """
        # Controleer of aantal geldig is
        if aantal <= 0:
            return False
        
        # Controleer of product op voorraad is
        if not product.is_op_voorraad(aantal):
            return False
        
        # Check of product al in mandje zit
        for i, (p, a) in enumerate(self.items):
            if p.naam == product.naam:
                self.items[i] = (p, a + aantal)
                return True
        
        # Nieuw product toevoegen
        self.items.append((product, aantal))
        return True
    
    def totaal_prijs(self):
        """
        Bereken de totale prijs van het winkelmandje.
        
        Returns:
            float: Totale prijs
        """
        totaal = sum(product.prijs * aantal for product, aantal in self.items)
        return totaal
    
    def verwijder_product(self, product_naam, aantal=None):
        """
        Verwijder (een deel van) een product uit het mandje.
        
        Args:
            product_naam (str): Naam van het product
            aantal (int, optional): Aantal om te verwijderen. None = helemaal verwijderen.
            
        Returns:
            bool: True als gelukt, anders False
        """
        for i, (product, huidig_aantal) in enumerate(self.items):
            if product.naam == product_naam:
                if aantal is None or aantal >= huidig_aantal:
                    # Verwijder helemaal
                    del self.items[i]
                else:
                    # Verwijder gedeeltelijk
                    self.items[i] = (product, huidig_aantal - aantal)
                return True
        return False
    
    def aantal_items(self):
        """
        Bereken het totaal aantal items in het mandje.
        
        Returns:
            int: Totaal aantal items
        """
        return sum(aantal for _, aantal in self.items)
    
    def leeg_mandje(self):
        """Leeg het winkelmandje."""
        self.items = []
    
    def __len__(self):
        """Aantal verschillende producten in mandje."""
        return len(self.items)
    
    def __str__(self):
        """String representatie van het winkelmandje."""
        if not self.items:
            return "Winkelmandje is leeg"
        
        result = "Winkelmandje:\n"
        for product, aantal in self.items:
            result += f"  {product.naam} x{aantal} = €{product.prijs * aantal:.2f}\n"
        result += f"Totaal: €{self.totaal_prijs():.2f}"
        return result