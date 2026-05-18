"Gemaakt door Pascal Petri"
"Datum: 18-5-2026"

import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

"class voor taken "
class Taak:
    def __init__(self, titel, klaar=False):
        self.titel = titel
        self.klaar = klaar

    def to_dict(self):
        return {"titel": self.titel, "klaar": self.klaar}

    @staticmethod
    def from_dict(data):
        return Taak(data["titel"], data["klaar"])

"class voor de takenlijst zelf"
class Takenlijst:
    def __init__(self):
        self.taken = []
        self.filename = "taken_gui.json"

    def voeg_toe(self, titel):
        taak = Taak(titel)
        self.taken.append(taak)

    def markeer_klaar(self, index):
        if 0 <= index < len(self.taken):
            self.taken[index].klaar = not self.taken[index].klaar

    def verwijder(self, index):
        if 0 <= index < len(self.taken):
            self.taken.pop(index)

    def save(self):
        data = [taak.to_dict() for taak in self.taken]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self):
        pad = Path(self.filename)
        if pad.exists():
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.taken = [Taak.from_dict(item) for item in data]

"class is voor het venster"
class TakenApp:
    def __init__(self):
        # Maak het hoofdvenster
        self.root = tk.Tk()
        self.root.title("Takenplanner")
        self.root.geometry("500x450")

        # Laad de takenlijst
        self.lijst = Takenlijst()
        self.lijst.load()

        # Maak de widgets
        self._create_widgets()

        # Ververs de lijst bij het opstarten
        self.refresh_listbox()

    def _create_widgets(self):
        """Maak alle GUI widgets aan"""
        
        # Entry voor nieuwe taken
        self.entry = tk.Entry(self.root, width=40, font=("Arial", 11))
        self.entry.pack(padx=10, pady=(10, 5))
        self.entry.bind("<Return>", lambda event: self.on_add())

        # Frame voor de knoppen
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        # Knoppen
        self.btn_add = tk.Button(
            btn_frame, 
            text="➕ Toevoegen", 
            command=self.on_add,
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5
        )
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_done = tk.Button(
            btn_frame, 
            text="✅ Klaar", 
            command=self.on_done,
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5
        )
        self.btn_done.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(
            btn_frame, 
            text="🗑️ Verwijderen", 
            command=self.on_delete,
            bg="#f44336",
            fg="white",
            padx=10,
            pady=5
        )
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_save = tk.Button(
            btn_frame, 
            text="💾 Opslaan", 
            command=self.on_save,
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=5
        )
        self.btn_save.grid(row=0, column=3, padx=5)

        # Listbox voor taken
        self.listbox = tk.Listbox(
            self.root, 
            width=60, 
            height=12,
            font=("Arial", 10),
            selectmode=tk.SINGLE
        )
        self.listbox.pack(padx=10, pady=5)

        # Label met instructie
        self.label = tk.Label(
            self.root, 
            text="Tip: Dubbelklik op een taak om deze als klaar te markeren",
            font=("Arial", 9),
            fg="gray"
        )
        self.label.pack(pady=5)

        # Bind dubbelklik aan klaar markeren
        self.listbox.bind("<Double-Button-1>", lambda event: self.on_done())

    def refresh_listbox(self):
        """Ververs de Listbox met de huidige taken"""
        self.listbox.delete(0, tk.END)

        for taak in self.lijst.taken:
            status = "✅" if taak.klaar else "⬜"
            self.listbox.insert(tk.END, f"{status} {taak.titel}")

    def get_selected_index(self):
        """Haal de index op van de geselecteerde taak"""
        selectie = self.listbox.curselection()
        if not selectie:
            return None
        return selectie[0]

    def on_add(self):
        """Voeg een nieuwe taak toe"""
        titel = self.entry.get().strip()

        if titel == "":
            messagebox.showwarning("Fout", "Titel mag niet leeg zijn.")
            return

        self.lijst.voeg_toe(titel)
        self.entry.delete(0, tk.END)
        self.refresh_listbox()

    def on_done(self):
        """Markeer een taak als klaar/niet klaar"""
        idx = self.get_selected_index()
        
        if idx is None:
            messagebox.showinfo("Info", "Selecteer eerst een taak.")
            return

        self.lijst.markeer_klaar(idx)
        self.refresh_listbox()

    def on_delete(self):
        """Verwijder een taak"""
        idx = self.get_selected_index()

        if idx is None:
            messagebox.showinfo("Info", "Selecteer eerst een taak.")
            return

        # Vraag bevestiging voor verwijderen
        if messagebox.askyesno("Bevestigen", "Weet je zeker dat je deze taak wilt verwijderen?"):
            self.lijst.verwijder(idx)
            self.refresh_listbox()

    def on_save(self):
        """Sla alle taken op"""
        self.lijst.save()
        messagebox.showinfo("Opgeslagen", "Taken zijn succesvol opgeslagen!")

    def run(self):
        """Start de applicatie"""
        self.root.mainloop()


if __name__ == "__main__":
    app = TakenApp()
    app.run()