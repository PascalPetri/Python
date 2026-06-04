# Gemaakt door: Pascal Petri
# Datum: 4-6-2026

from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib
from pathlib import Path

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Hashing functies
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, password_hash):
    return hash_password(password) == password_hash

# Bestandspaden
USERS_FILE = "users.json"
TAKEN_FILE = "taken.json"

# Gebruikersbeheer
def ensure_users():
    if Path(USERS_FILE).exists():
        return
    
    users = [
        {"username": "admin", "password": hash_password("admin123"), "role": "admin"},
        {"username": "user", "password": hash_password("user123"), "role": "user"}
    ]
    Path(USERS_FILE).write_text(json.dumps(users, indent=2))

def load_users():
    if not Path(USERS_FILE).exists():
        return []
    return json.loads(Path(USERS_FILE).read_text())

# Takenbeheer
def load_taken():
    if not Path(TAKEN_FILE).exists():
        return []
    return json.loads(Path(TAKEN_FILE).read_text())

def save_taken(taken):
    Path(TAKEN_FILE).write_text(json.dumps(taken, indent=2))

# Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        users = load_users()
        for user in users:
            if user["username"] == username and check_password(password, user["password"]):
                session["user"] = user["username"]
                session["role"] = user["role"]
                return redirect(url_for("index"))
        
        return render_template("login.html", error="Foute login")
    
    return render_template("login.html")

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))  
    taken = load_taken()
    if session["role"] != "admin":
        taken = [t for t in taken if t.get("owner") == session["user"]]
    
    return render_template("index.html", taken=taken, user=session["user"], role=session["role"])

@app.post("/add")
def add():
    if "user" not in session:
        return redirect(url_for("login"))
    
    titel = request.form.get("titel", "").strip()
    if titel:
        taken = load_taken()
        taken.append({"titel": titel, "klaar": False, "owner": session["user"]})
        save_taken(taken)
    
    return redirect(url_for("index"))

@app.get("/done/<int:i>")
def done(i):
    if "user" not in session:
        return redirect(url_for("login"))
    
    taken = load_taken()
    if i < len(taken):
        if session["role"] == "admin" or taken[i].get("owner") == session["user"]:
            taken[i]["klaar"] = True
            save_taken(taken)
    
    return redirect(url_for("index"))

@app.get("/delete/<int:i>")
def delete(i):
    if "user" not in session:
        return redirect(url_for("login"))
    
    if session["role"] != "admin":
        return redirect(url_for("index"))
    
    taken = load_taken()
    if i < len(taken):
        taken.pop(i)
        save_taken(taken)
    
    return redirect(url_for("index"))

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    ensure_users()
    app.run(debug=True)