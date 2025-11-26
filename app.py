from flask import Flask, request, jsonify
import sqlite3
import re
import os
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fisica.db")

conectores = {
    "el","la","los","las","un","una","unos","unas",
    "de","del","al","a","en","por","para","con",
    "que","y","o","pero","si","no","se","su","sus",
    "es","son","como","más","menos","muy","ya",
    "lo","me","te","le","les","mi","tu","su",
    "esto","eso","esa","ese","aquel","aquella"
}

def cargar_palabras():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT palabra, score FROM palabras_fisica")
    data = cursor.fetchall()
    conn.close()

    print("PALABRAS CARGADAS DESDE BD:")
    for p, s in data:
        print(f" - {p}: {s}")

    return {palabra.lower(): score for palabra, score in data}


def analizar_texto(texto):

    texto = texto.lower()
    palabras_bd = cargar_palabras()

    
    
    separacion = re.findall(r"\b[a-záéíóúüñ]+\b", texto)


    separacion = [t for t in separacion if t not in conectores]

    print(f"🧹 Tokens SIN conectores ({len(separacion)}): {separacion}")

    if not separacion:
        return {"tema": "no detectado", "score": 0}

    frecuencia = {}
    for t in separacion:
        frecuencia[t] = frecuencia.get(t, 0) + 1

    for palabra, freq in frecuencia.items():
        print(f" - {palabra}: {freq}")

    score_total = 0
    coincidencias = 0

    for palabra, score in palabras_bd.items():
        if palabra in frecuencia:
            coincidencias += 1
            score_total += score


    if coincidencias == 0:
        porcentaje = 0
    else:
        porcentaje = min(100, round((score_total / (coincidencias * 10)) * 100, 2))



    return {
        "tema": "Fisica" if porcentaje > 10 else "No identificado",
        "score": porcentaje,
        "coincidencias": coincidencias
    }


@app.route("/analizador", methods=["POST"])
def analizador():
    try:
        data = request.get_json()
        texto = data.get("text", "")

        resultado = analizar_texto(texto)
        return jsonify(resultado)

    except Exception as e:
        print(f"ERROR EN LA API: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("API ejecutándose en http://localhost:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)
