from conexion_db import conexion

def lista():
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, temperatura, clima FROM ciudades")
        filas = cursor.fetchall()


    print("Lista de ciudades")
    for nombre, temp, clima in filas:
        print(f"{nombre: <12} | {temp :> 5}°C | {clima}")

def ciudad_existe(nombre):
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ciudades WHERE nombre = ?", (nombre,))

        return cursor.fetchone() is not None

# Funcion para guardar en la base de datos o actualizar
def guardar_o_actualizar (nombre, lat, lon, temp, clima):
    with conexion() as conn:
        cursor = conn.cursor()

        if ciudad_existe(nombre):
            cursor.execute(""" 
                UPDATE ciudades
                SET latitud = ?, longitud = ?, temperatura = ?, clima = ?
                WHERE nombre = ?           
            """, (lat, lon, temp, clima, nombre))
            print (f"{nombre} Actualizada")

        else:
            cursor.execute("""
                INSERT INTO ciudades (nombre, latitud, longitud, temperatura, clima)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, lat, lon, temp, clima))
            print(f"{nombre} guardada")


def eliminar_ciudad(nombre):
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ciudades WHERE nombre = ?", (nombre,))

        if cursor.rowcount == 0:
            print("ciudad no encontrada")
        else:
            print(f"{nombre} eliminada")

def mostrar_ranking():
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre, temperatura, clima
            FROM ciudades
            ORDER BY temperatura DESC
        """)
        filas = cursor.fetchall()

    print("\n🌡️ Ranking de temperaturas:")
    for i, (nombre, temp, clima) in enumerate( filas, start=1):
        print(f"{i}. {nombre: <12} | {temp:>5}°C | {clima}")
