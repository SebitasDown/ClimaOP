import sqlite3

# Conexion a la base de datos (sqlite)
def conexion():
    return sqlite3.connect("clima.db")