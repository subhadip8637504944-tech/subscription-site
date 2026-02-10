from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

PASSWORD = "admin123"

def get_db():
    return sqlite3.connect("database.db")

with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            group_name TEXT
        )
    """)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        group = request.form["group"]
        with get_db() as db:
            db.execute(
                "INSERT INTO subscriptions (name, group_name) VALUES (?,?)",
                (name, group)
            )

    with get_db() as db:
        data = db.execute("SELECT * FROM subscriptions").fetchall()

    return render_template("dashboard.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)