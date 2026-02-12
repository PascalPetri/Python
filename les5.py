#Gemaakt door Pascal Petri
# Datum 12-2-2026

#klas student met leeftijd en naam 
class Student:
    def __init__(self, naam, leeftijd):
        self.naam = naam
        self._leeftijd = leeftijd
    
    # Leeftijd Ophalen
    def get_leeftijd(self):
        return self._leeftijd
    
    # Leeftijd ZETTEN met checks
    def set_leeftijd(self, nieuwe_leeftijd):
        if nieuwe_leeftijd < 0:
            print(f"FOUT bij {self.naam}: Leeftijd kan niet negatief zijn!")
            return
        if nieuwe_leeftijd > 130:
            print(f"FOUT bij {self.naam}: Leeftijd kan niet boven 130 zijn!")
            return
        self._leeftijd = nieuwe_leeftijd
        print(f"{self.naam} is nu {nieuwe_leeftijd} jaar")
    
    # Verjaardag
    def verjaar(self):
        self.set_leeftijd(self.get_leeftijd() + 1)
    
    # Info tonen
    def toon_info(self):
        print(f"  {self.naam} -> {self._leeftijd} jaar")


# =========== 3 STUDENTEN MAKEN ===========
print("=== 3 STUDENTEN ===")

student1 = Student("Pascal", 19)
student2 = Student("Bob", 22)
student3 = Student("Ahmed", 129)

# Info tonen
print("\n📋 START:")
student1.toon_info()
student2.toon_info()
student3.toon_info()

# =========== TESTEN ===========
print("\n--- Pascal wordt 20 ---")
student1.set_leeftijd(20)

print("\n--- BOB verjaart ---")
student2.verjaar()

print("\n--- Ahmed verjaart (129 -> 130) ---")
student3.verjaar()
print("--- Ahmed nog een keer (130 -> 131 mag niet!) ---")
student3.verjaar()

print("\n--- Foute leeftijden testen ---")
student1.set_leeftijd(-10)
student2.set_leeftijd(200)

# =========== EINDRESULTAAT ===========
print("\n📊 EINDSTAND:")
student1.toon_info()
student2.toon_info()
student3.toon_info()

print("\n✅ KLAAR! 3 studenten met encapsulation!")