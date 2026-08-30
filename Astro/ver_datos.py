import sqlite3
import os

# Buscamos la ruta absoluta de la base de datos de manera dinámica
base_dir = os.path.dirname(os.path.abspath(__file__))
# Viajamos desde Astro/ a la carpeta raíz y luego a data/astro.sqlite3
db_path = os.path.abspath(os.path.join(base_dir, "..", "data", "astro.sqlite3"))

if not os.path.exists(db_path):
    print(f"Error: El archivo de la base de datos no existe en la ruta calculada: {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("--- DETECTANDO TABLAS PRESENTES EN TU BASE DE DATOS ---")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    print(f"Tablas encontradas: {tablas}\n")

    print("--- CONTENIDO DE LA TABLA SATELLITE_TLES (Primeros 5 registros) ---")
    try:
        cursor.execute("SELECT id, norad_id, name, epoch FROM satellite_tles LIMIT 5;")
        filas = cursor.fetchall()
        for fila in filas:
            print(f"Reg ID: {fila[0]} | NORAD ID: {fila[1]} | Nombre: {fila[2]:<20} | Época Órbita: {fila[3]}")
    except sqlite3.OperationalError as e:
        print(f"Error al consultar la tabla: {e}")

    conn.close()