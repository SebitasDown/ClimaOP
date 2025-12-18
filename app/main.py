from fastapi import FastAPI
from db import (
    guardar_o_actualizar,
    eliminar_ciudad,
    mostrar_ranking,
    lista
)
from config import CODIGOS

app = FastAPI(title= "API Clima")

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