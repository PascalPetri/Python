#Gemaakt door Pascal Petri 
#Datum 29-1-2026

class Student:
    def __init__(self, naam, leeftijd, opleiding):
        self.naam = naam
        self.leeftijd = leeftijd
        self.opleiding = opleiding

    def begroet(self):
        print(f"Hallo, ik ben {self.naam}, ik ben {self.leeftijd} jaar en ik volg de opleiding {self.opleiding}")

student1 = Student("pascal", 19, "Software Development")
student2 = Student("kim", 20, "ICT Support")

student1.begroet()
student2.begroet()
