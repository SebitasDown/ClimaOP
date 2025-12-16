import sqlite3

conn = sqlite3.connect("clima.db")

cursor = conn.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS ciudades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    latitud REAL,
    longitud REAL,
    temperatura REAL,
    clima TEXT
)
""")

conn.commit()
conn.close()

print("Base de datos creada con exito")