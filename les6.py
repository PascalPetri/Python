# Gemaakt door Pascal Petri
# Datum 12-2-2026

#klas persoon 
class Persoon:
    """Parent class voor alle personen"""
    
    def __init__(self, naam):
        self.naam = naam
    
    def voorstel(self):
        print(f"Ik ben {self.naam}.")

# klas student ende persoon leeftijd naam opleiding ect 
class Student(Persoon):
    """Child class Student erft van Persoon"""
    
    def __init__(self, naam, leeftijd, opleiding):
        # Roep __init__ van Persoon aan voor naam
        super().__init__(naam)
        # Extra attributen specifiek voor Student
        self.leeftijd = leeftijd
        self.opleiding = opleiding
    
    def voorstel(self):
        # Overschrijf (override) de methode van Persoon
        print(f"Ik ben {self.naam}, {self.leeftijd} jaar, opleiding: {self.opleiding}.")


class Docent(Persoon):
    """Child class Docent erft van Persoon"""
    
    def __init__(self, naam, vak):
        # Roep __init__ van Persoon aan voor naam
        super().__init__(naam)
        # Extra attribuut specifiek voor Docent
        self.vak = vak
    
    def voorstel(self):
        # Overschrijf (override) de methode van Persoon
        print(f"Ik ben {self.naam} en ik geef {self.vak}.")


# Testcode - maak objecten en roep voorstel() aan
if __name__ == "__main__":
    # Maak een student
    s1 = Student("Sara", 20, "Software Development")
    
    # Maak een docent
    d1 = Docent("Ali", "Python")
    
    # Roep voorstel() aan op beide objecten
    s1.voorstel()   # Gebruikt Student.voorstel()
    d1.voorstel()   # Gebruikt Docent.voorstel()
    
    # Extra test: als we een Persoon-object maken
    p1 = Persoon("Jan")
    p1.voorstel()   # Gebruikt Persoon.voorstel()