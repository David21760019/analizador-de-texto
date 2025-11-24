import sqlite3

conn = sqlite3.connect("fisica.db")
cursor = conn.cursor()

palabras_nuevas = [
    ("impulso", 8),
    ("momento", 9),
    ("momento angular", 10),
    ("elasticidad", 7),
    ("torsión", 7),
    ("presión", 8),
    ("densidad", 7),
    ("volumen", 6),
    ("frecuencia", 7),
    ("amplitud", 6),
    ("interferencia", 8),
    ("difracción", 8),
    ("reflexión", 7),
    ("refracción", 7),
    ("longitud de onda", 8),
    ("campo magnético", 10),
    ("campo eléctrico", 10),
    ("electrón", 8),
    ("protón", 8),
    ("neutrón", 8),
    ("fotón", 9),
    ("radioactividad", 10),
    ("radiación", 9),
    ("ion", 6),
    ("entropía", 10),
    ("fluido", 6),
    ("hidrodinámica", 9),
    ("hidrostática", 8),
    ("cosmología", 9),
    ("relatividad", 10)
]

    cursor.executemany(
    "INSERT INTO palabras_fisica (palabra, score) VALUES (?, ?)",
    nuevas_palabras
)

conn.commit()
conn.close()

print("✔ 30 palabras agregadas con éxito a fisica.db")
