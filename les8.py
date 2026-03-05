# Gemaakt door Pascal Petri
# Datum: 05-03-2026
# Polymorfisme voorbeeld met abstracte class

from abc import ABC, abstractmethod

# Basisclass voor betaalmethodes
class Betaalmethode(ABC):

    def __init__(self, naam):
        self.naam = naam

    @abstractmethod
    def betaal(self, bedrag):
        pass


# Pin betaling
class PinBetaling(Betaalmethode):

    def __init__(self):
        super().__init__("Pin")

    def betaal(self, bedrag):
        return f"💳 Betaling van €{bedrag:.2f} gepind via betaalautomaat."


# Contante betaling
class ContantBetaling(Betaalmethode):

    def __init__(self):
        super().__init__("Contant")

    def betaal(self, bedrag):
        return f"💵 Contante betaling ontvangen: €{bedrag:.2f}."


# Online betaling
class OnlineBetaling(Betaalmethode):

    def __init__(self):
        super().__init__("Online")

    def betaal(self, bedrag):
        return f"🌐 Online betaling van €{bedrag:.2f} succesvol verwerkt."


# Test polymorfisme
print("Test van verschillende betaalmethodes\n")

methodes = [PinBetaling(), ContantBetaling(), OnlineBetaling()]

for methode in methodes:
    print(methode.betaal(49.95))