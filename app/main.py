from api import obtener_coordenadas, obtener_clima
from db import (
    guardar_o_actualizar,
    eliminar_ciudad,
    mostrar_ranking,
    lista
)
from config import CODIGOS

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
    
