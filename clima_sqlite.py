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

# Inyeccion de datos a SQLite

conn = sqlite3.connect("clima.db")
cursor = conn.cursor()

cursor.executemany("""
INSERT INTO ciudades(nombre, latitud, longitud, temperatura, clima)
VALUES(?,?,?,?,?)""", [
("Bogota", 4.61, -74.08, 18, "Nublado ☁️"), 
("Medellin", 4.61, -74.08, 18, "Nublado ☁️")
])

conn.commit()
conn.close()

print("Ciudades insertadas")


# Consulta sql para observar todas las ciudades
conn = sqlite3.connect("clima.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM ciudades")
ciudades = cursor.fetchall()

for ciudad in ciudades:
    print("- ", ciudad)

conn.close()
