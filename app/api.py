import requests

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

