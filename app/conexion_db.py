import mysql.connector
import os
import time

def conexion():
    """Conecta a MySQL con reintentos para manejar tiempos de espera."""
    intentos = 0
    while intentos < 3:
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except Exception as e:
            print(f"Error conectando a BD (intento {intentos+1}): {e}")
            intentos += 1
            time.sleep(2)
    raise Exception("No se pudo conectar a la base de datos después de 3 intentos")