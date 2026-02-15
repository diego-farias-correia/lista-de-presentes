from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("presente.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

# API LISTAR
@app.route("/api/presentes")
def listar_presentes():
    conn = get_db()
    presentes = conn.execute("SELECT * FROM lista_presentes").fetchall()
    conn.close()

    return jsonify([dict(p) for p in presentes])

# API PRESENTEAR
@app.route("/api/presentear", methods=["POST"])
def presentear():
    data = request.get_json()
    nome = data["nome"]
    id_presente = data["id"]

    conn = get_db()

    # PROTEÇÃO SQL INJECTION (query parametrizada)
    conn.execute("""
        UPDATE lista_presentes
        SET convidado = ?, status = 1
        WHERE id = ?
    """, (nome, id_presente))

    conn.commit()
    conn.close()

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
