from conexion_db import conexion

def lista():
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, temperatura, clima FROM ciudades")
        filas = cursor.fetchall()

    print("Lista de ciudades")
    for nombre, temp, clima in filas:
        print(f"{nombre: <12} | {temp :> 5}°C | {clima}")
    
    return filas

def ciudad_existe(nombre):
    with conexion() as conn:
        cursor = conn.cursor()
        # MySQL usa %s
        cursor.execute("SELECT id FROM ciudades WHERE nombre = %s", (nombre,))

        return cursor.fetchone() is not None

def guardar_o_actualizar(nombre, lat, lon, temp, clima):
    with conexion() as conn:
        cursor = conn.cursor()

        if ciudad_existe(nombre):
            cursor.execute(""" 
                UPDATE ciudades
                SET latitud = %s, longitud = %s, temperatura = %s, clima = %s
                WHERE nombre = %s           
            """, (lat, lon, temp, clima, nombre))
            conn.commit()
            print (f"{nombre} Actualizada")
            return "actualizada"

        else:
            cursor.execute("""
                INSERT INTO ciudades (nombre, latitud, longitud, temperatura, clima)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, lat, lon, temp, clima))
            conn.commit()
            print(f"{nombre} guardada")
            return "creada"


def eliminar_ciudad(nombre):
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ciudades WHERE nombre = %s", (nombre,))
        conn.commit()

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
    
    return filas

# Refactorización de base de datos

# Obtenerlos a todos
def getAllCiudad():
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, temperatura, clima FROM ciudades")
        filas = cursor.fetchall()

    print("Lista de ciudades")
    for nombre, temp, clima in filas:
        print(f"{nombre: <12} | {temp :> 5}°C | {clima}")
    
    return filas


# Agregar 
def postCiudad(nombre, lat, lon, temp, clima):
    with conexion() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ciudades (nombre, latitud, longitud, temperatura, clima)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, lat, lon, temp, clima))
        conn.commit()
        print(f"{nombre} guardada")
        return "creada"
     
# Actualizar
def putCiudad(nombre, lat, lon, temp, clima):
    with conexion() as conn:
        cursor = conn.cursor()

        if ciudad_existe(nombre):
            cursor.execute(""" 
                UPDATE ciudades
                SET latitud = %s, longitud = %s, temperatura = %s, clima = %s
                WHERE nombre = %s           
            """, (lat, lon, temp, clima, nombre))
            conn.commit()
            print (f"{nombre} Actualizada")
            return "actualizada"
        else:
            return "No existe en la base de datos"
        
# Eliminar 
def deleteCiudad(nombre):
    with conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ciudades WHERE nombre = %s", (nombre,))
        conn.commit()

        if cursor.rowcount == 0:
            print("ciudad no encontrada")
            return "Ciudad no encontrada"
        else:
            print(f"{nombre} eliminada")
            return "eliminada"
