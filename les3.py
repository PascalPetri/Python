#gemaakt door Pascal Petri 
#datum 29-1-2026

#het Maken hoe oud iemand is met true or false al
class Student:
    def __init__(self, naam, leeftijd):
        self.naam = naam
        self.leeftijd = leeftijd

#check of iemand 18 is 
    def is_volwassen(self):
        return self.leeftijd >= 18

#lijst studenten 
s1 = Student("Pascal", 20)
s2 = Student("Bob", 17)
s3 = Student("Kim", 19)
s4 = Student("joep", 16)
studenten = [s1, s2, s3, s4]

aantal_volwassen = 0

#telt of er iemand volwassen is
for student in studenten:
    print(student.naam, student.leeftijd, student.is_volwassen())

    if student.is_volwassen():
        aantal_volwassen += 1

print("Aantal studenten van 18 jaar of ouder:", aantal_volwassen)
