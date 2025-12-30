import requests
from fastapi import HTTPException

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city_name: str):
    try:
        params = {"name": city_name, "count": 1, "language": "es", "format": "json"}
        response = requests.get(GEOCODING_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results"):
            return None, None
            
        result = data["results"][0]
        return result["latitude"], result["longitude"]
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def get_current_weather(lat: float, lon: float):
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }
        response = requests.get(WEATHER_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "current_weather" not in data:
            return None, None
            
        weather = data["current_weather"]
        return weather["temperature"], interpret_weather_code(weather["weathercode"])
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None, None

def interpret_weather_code(code: int) -> str:
    if code == 0: return "Despejado"
    if code in [1, 2, 3]: return "Nublado"
    if code in [45, 48]: return "Niebla"
    if code in [51, 53, 55, 56, 57]: return "Llovizna"
    if code in [61, 63, 65, 66, 67]: return "Lluvia"
    if code in [71, 73, 75, 77]: return "Nieve"
    if code in [80, 81, 82]: return "Lluvia fuerte"
    if code in [85, 86]: return "Nieve fuerte"
    if code >= 95: return "Tormenta"
    return "Desconocido"
