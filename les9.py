# Gemaakt door Pascal Petri
# Datum: 05-03-2026
# Les 9 - Exceptions en Validatie

# Vraag om een geldig geheel getal
def vraag_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ongeldige invoer, probeer opnieuw")


# Delen functie met eigen fout
def delen(a, b):
    if b == 0:
        raise ZeroDivisionError("Delen door 0 mag niet")
    return a / b


# Hoofdmenu
while True:
    print("\nMenu")
    print("1. Optellen")
    print("2. Delen")
    print("0. Stoppen")

    keuze = vraag_int("Kies: ")

    try:
        if keuze == 0:
            print("Programma gestopt")
            break

        elif keuze == 1:
            a = vraag_int("Getal 1: ")
            b = vraag_int("Getal 2: ")
            print("Uitkomst:", a + b)

        elif keuze == 2:
            a = vraag_int("Getal 1: ")
            b = vraag_int("Getal 2: ")
            print("Uitkomst:", delen(a, b))

        else:
            print("Ongeldige keuze")

    except ZeroDivisionError as e:
        print("Fout:", e)

    finally:
        print("Terug naar menu...")