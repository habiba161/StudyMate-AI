import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DATABASE"] = "studymate.db"

def get_connection():
    return sqlite3.connect(app.config["DATABASE"])

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""

    if request.method == "POST":
        user_input = request.form["topic"]
        response = f"AI Explanation for: {user_input}"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (topic, response) VALUES (?, ?)",
            (user_input, response)
        )
        conn.commit()
        conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic, response FROM history ORDER BY id DESC")
    history = cursor.fetchall()
    conn.close()

    return render_template("index.html", response=response, history=history)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)