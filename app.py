from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/")
def index():
    return render_template("index.html")

# LISTAR PRESENTES
@app.route("/api/presentes")
def listar_presentes():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT * FROM lista_presentes ORDER BY id;")
    presentes = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(presentes)

# DAR PRESENTE
@app.route("/api/presentear", methods=["POST"])
def presentear():
    data = request.get_json()
    nome = data["nome"]
    id_presente = data["id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lista_presentes
        SET convidado = %s, status = 1
        WHERE id = %s
    """, (nome, id_presente))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"ok": True})

# ADMIN
@app.route("/admin")
def admin():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("""
        SELECT item, convidado
        FROM lista_presentes
        WHERE convidado IS NOT NULL
        ORDER BY id;
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(dados)

if __name__ == "__main__":
    app.run()