from fastapi import FastAPI, HTTPException, status
from schemas import Ciudad
from db import (
 getAllCiudad,
 postCiudad,
 putCiudad,
 deleteCiudad,
 mostrar_ranking
)
from cors import setup_cors

app = FastAPI(title= "API Clima")

setup_cors(app)

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
def crear_ciudad(ciudad:Ciudad):
    estado = postCiudad(
        ciudad.nombre,
        ciudad.latitud,
        ciudad.longitud,
        ciudad.temperatura,
        ciudad.clima
    )
    return {"mensaje": f"Ciudad {estado}"}


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
@app.delete("/ciudad/{nombre}")
def borrar_ciudad(nombre:str):
   filas  = deleteCiudad(nombre)
   if filas == 0:
       raise HTTPException(
           status_code = 404,
           detail = "Ciudad no encontrada"
       )
   return {"mensaje": "Ciudad eliminada"}