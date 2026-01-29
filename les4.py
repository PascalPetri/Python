#Gemaakt door Pascal Petri 
#Datum 29-1-2026

# Class Student = blauwdruk voor studenten
# Bevat naam, leeftijd en een begroet-methode
class Student:
    def __init__(self, naam, leeftijd):
        self.naam = naam
        self.leeftijd = leeftijd

    def begroet(self):
        print(f"Hallo, ik ben {self.naam}!")


# Lijst met meerdere Student-objecten
# Elk object heeft eigen naam en leeftijd
studenten = [
    Student("Pascal", 20),
    Student("Bob", 17),
    Student("Kim", 19),
    Student("Jeff",20),
]


# For-loop die door alle studenten gaat
# Roept per student de begroet()-methode aan
for s in studenten:
    s.begroet()


# Teller voor het aantal studenten van 18 jaar of ouder
aantal_18_plus = 0

for s in studenten:
    if s.leeftijd >= 18:
        aantal_18_plus += 1

print("Aantal studenten van 18 jaar of ouder:", aantal_18_plus)


# Berekenen van de gemiddelde leeftijd
totaal_leeftijd = 0

for s in studenten:
    totaal_leeftijd += s.leeftijd

gemiddelde = totaal_leeftijd / len(studenten)
print("Gemiddelde leeftijd:", gemiddelde)
