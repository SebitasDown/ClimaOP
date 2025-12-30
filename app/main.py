from fastapi import FastAPI, HTTPException, status
from schemas import Ciudad
from cors import configure_cors
from db import (
 getAllCiudad,
 postCiudad,
 putCiudad,
 deleteCiudad,
 mostrar_ranking
)
from services import get_coordinates, get_current_weather

app = FastAPI(title= "API Clima")
configure_cors(app)


# endpoints de prueba 
@app.get("/")
def home():
    return{"mensaje" : "API de Clima funcionando"}


@app.get("/ranking")
def ranking():
    filas = mostrar_ranking()
    return [
        {"ciudad": n, "temperatura": t, "clima": c}
        for n, t, c in filas
    ]

# Obtener todas las ciudades
@app.get("/ciudades")
def ciudades():
    filas = getAllCiudad()
    return[
        {"ciudad":n, "temperatura": t, "clima": c}
        for n, t, c in filas
    ]

# Crear ciudad
@app.post("/ciudades", status_code=status.HTTP_201_CREATED)
def crear_ciudad(ciudad: Ciudad):
    if ciudad.latitud is None or ciudad.longitud is None:
        lat, lon = get_coordinates(ciudad.nombre)
        if lat is None:
            raise HTTPException(status_code=404, detail=f"No se encontraron coordenadas para {ciudad.nombre}")
        ciudad.latitud = lat
        ciudad.longitud = lon
    
    if ciudad.temperatura is None or ciudad.clima is None:
        temp, weather_desc = get_current_weather(ciudad.latitud, ciudad.longitud)
        if temp is not None:
            ciudad.temperatura = temp
            ciudad.clima = weather_desc
        else:
            if ciudad.temperatura is None: ciudad.temperatura = 0.0
            if ciudad.clima is None: ciudad.clima = "Desconocido"

    estado = postCiudad(
        ciudad.nombre,
        ciudad.latitud,
        ciudad.longitud,
        ciudad.temperatura,
        ciudad.clima
    )
    return {"mensaje": f"Ciudad {estado}", "datos": ciudad.dict()}


# Actualizar ciudad
@app.put("/ciudades/{nombre}")
def actualizar_ciudad(nombre: str, ciudad:Ciudad):
    estado = putCiudad(
        nombre,
        ciudad.latitud,
        ciudad.longitud,
        ciudad.temperatura,
        ciudad.clima
    )
    return {"mensaje" : f"Ciudad {estado}"}


#Eliminar ciudad
@app.delete("/ciudades/{nombre}")
def borrar_ciudad(nombre:str):
   filas  = deleteCiudad(nombre)
   if filas == 0:
       raise HTTPException(
           status_code = 404,
           detail = "Ciudad no encontrada"
       )
   return {"mensaje": "Ciudad eliminada"}