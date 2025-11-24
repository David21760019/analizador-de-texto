from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

DB_PATH = "fisica.db"

# --------------------------------------------
# LISTA DE CONECTORES A ELIMINAR (STOPWORDS)
# --------------------------------------------
STOPWORDS = {
    "el","la","los","las","un","una","unos","unas",
    "de","del","al","a","en","por","para","con",
    "que","y","o","pero","si","no","se","su","sus",
    "es","son","como","más","menos","muy","ya",
    "lo","me","te","le","les","mi","tu","su",
    "esto","eso","esa","ese","aquel","aquella"
}

# -----------------------------------------------------------------------------------
# Función para cargar palabras desde BD
# -----------------------------------------------------------------------------------
def cargar_palabras():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT palabra, score FROM palabras_fisica")
    data = cursor.fetchall()
    conn.close()

    print("\n📌 PALABRAS CARGADAS DESDE BD:")
    for p, s in data:
        print(f" - {p}: {s}")

    return {palabra.lower(): score for palabra, score in data}


# -----------------------------------------------------------------------------------
# Analizar texto
# -----------------------------------------------------------------------------------
def analizar_texto(texto):
    print("\n===============================")
    print("🔍 ANALIZANDO TEXTO...")
    print("===============================")
    print(f"Texto recibido:\n{texto}\n")

    texto = texto.lower()
    palabras_bd = cargar_palabras()

    # Tokenizar el texto
    tokens = re.findall(r"\b[a-záéíóúüñ]+\b", texto)
    print(f"📝 Tokens detectados ({len(tokens)}): {tokens}")

    # 🔥 QUITAR CONECTORES
    tokens = [t for t in tokens if t not in STOPWORDS]

    print(f"🧹 Tokens SIN conectores ({len(tokens)}): {tokens}")

    if not tokens:
        print("❌ No quedan palabras clave tras limpiar conectores.")
        return {"tema": "no detectado", "score": 0}

    # Contar frecuencia
    frecuencia = {}
    for t in tokens:
        frecuencia[t] = frecuencia.get(t, 0) + 1

    print("\n📊 Frecuencia de palabras filtradas:")
    for palabra, freq in frecuencia.items():
        print(f" - {palabra}: {freq}")

    score_total = 0
    coincidencias = 0

    # Revisar palabras clave
    print("\n📌 Revisando palabras clave de física:")
    for palabra, score in palabras_bd.items():
        if palabra in frecuencia:
            coincidencias += 1
            score_total += score

            print(f" ✔ Coincidencia: '{palabra}' → +{score}")

    # --------------------------------------------
    # NUEVA FÓRMULA PARA PORCENTAJE
    # Basado SOLO en coincidencias ENCONTRADAS
    # --------------------------------------------
    if coincidencias == 0:
        porcentaje = 0
    else:
        # normalizar entre 0 y 100
        porcentaje = min(100, round((score_total / (coincidencias * 10)) * 100, 2))

    print(f"\n Score total acumulado: {score_total}")
    print(f" Coincidencias detectadas: {coincidencias}")
    print(f" Porcentaje final: {porcentaje}%")
    print("===============================\n")

    return {
        "tema": "Fisica" if porcentaje > 10 else "No identificado",
        "score": porcentaje,
        "coincidencias": coincidencias
    }


# -----------------------------------------------------------------------------------
# ENDPOINT
# -----------------------------------------------------------------------------------
@app.route("/analizador", methods=["POST"])
def analizador():
    try:
        data = request.get_json()
        texto = data.get("text", "")

        resultado = analizar_texto(texto)
        return jsonify(resultado)

    except Exception as e:
        print(f"❌ ERROR EN LA API: {e}")
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 API ejecutándose en http://localhost:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)
