"""
Gemaakt door: Pascal Petri
Datum: 23 maart 2026
Doel: Product class voor beheren productgegevens
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
        self._voorraad = voorraad
    
    def toon_info(self):
        """Toon productinformatie."""
        return f"{self.naam} - €{self.prijs:.2f} - Voorraad: {self._voorraad}"
    
    def is_op_voorraad(self, aantal=1):
        """
        Controleer of product op voorraad is.
        
        Args:
            aantal (int): Gevraagd aantal
            
        Returns:
            bool: True als op voorraad, anders False
        """
        return self._voorraad >= aantal
    
    def verlaag_voorraad(self, aantal):
        """
        Verlaag de voorraad met een bepaald aantal.
        
        Args:
            aantal (int): Aantal om te verlagen
            
        Returns:
            bool: True als gelukt, False als niet genoeg voorraad
        """
        if self.is_op_voorraad(aantal):
            self._voorraad -= aantal
            return True
        return False
    
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