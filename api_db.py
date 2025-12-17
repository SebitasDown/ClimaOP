import requests
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


# Consumo de Api externa (con request)
def obtener_coordenadas(ciudad):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    parametros = {"name": ciudad, "count": 1, "language": "es"}

    try:
        resp = requests.get(geo_url, params=parametros, timeout=10)
        data = resp.json()
        
        if resp.status_code == 200  and data.get("results"):
            datos = resp.json()["results"][0]
            return datos["latitude"], datos["longitude"], datos["name"]
        else:
            print("No se encontro la ciudad")
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error en la conexion: {e}")        


def obtener_clima(lat, lon):
    clima_url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude" : lat,
        "longitude" : lon,
        "current_weather": True
    }
    try:
        resp = requests.get(clima_url, params=parametros, timeout=10)

        if resp.status_code == 200:
            return resp.json().get("current_weather", None)
        else:
            print("Error al obtener el clima")
            return None    
    except requests.exceptions.RequestException as e:
        print(f"Error en la conexion: {e}")        


CODIGOS = {
    0: "Despejado ☀️",
    1: "Mayormente despejado 🌤️",
    2: "Parcialmente nublado ⛅",
    3: "Nublado ☁️",
    45: "Niebla 🌫️",
    48: "Niebla con escarcha 🌫️❄️",
    51: "Llovizna ligera 🌦️",
    61: "Lluvia 🌧️",
    71: "Nieve ❄️",
    95: "Tormenta eléctrica ⛈️"
}
# Bucle para pedir ciudad a usuario

while True:
    print("""
1. Agregar / Actualizar ciudad
2. Mostrar ranking
3. Eliminar ciudad
4. Mostrar todas las ciudades
5. Salir
""")
    opcion = input("Elige: ")

    if opcion == "1":
        ciudad = input("Ciudad: ")
        lat, lon, nombre = obtener_coordenadas(ciudad)
        if lat:
            clima = obtener_clima(lat, lon)
            # Validacion por si api no funciona
            if clima is None:
                print("No se pudo obtener el clima")
                continue
            temp = clima["temperature"]
            codigo = clima["weathercode"]
            desc = CODIGOS.get(codigo, "Desconocido")
            guardar_o_actualizar(nombre, lat, lon, temp, desc)
        else:
            print("No se pudo obtener el clima")

    elif opcion == "2":
        mostrar_ranking()

    elif opcion == "3":
        nombre = input("Ciudad a eliminar: ")
        eliminar_ciudad(nombre)
    
    elif opcion == "4":
        lista()

    elif opcion == "5":
        print("Saliendo")
        break

    else:
        print("opcion no valida")  
    
