import sqlite3
import os


def inicializar_base_de_datos():
    # 1. Encontrar la ruta absoluta del archivo astro.sqlite3
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.abspath(os.path.join(base_dir, "..", "..", "data", "astro.sqlite3"))

    # Nos aseguramos de que exista el directorio data
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"Conectando de forma absoluta a: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 2. Borrar tablas viejas si existen para limpiar pruebas pasadas
    cursor.execute("DROP TABLE IF EXISTS observation_errors;")
    cursor.execute("DROP TABLE IF EXISTS satellite_observations;")
    cursor.execute("DROP TABLE IF EXISTS satellite_tles;")

    # 3. Crear la tabla histórica para procesar TLEs (Aquí vivirán starlink.tle y stations.tle)
    print("Creando tabla satellite_tles...")
    cursor.execute("""
                   CREATE TABLE satellite_tles
                   (
                       id         INTEGER PRIMARY KEY AUTOINCREMENT,
                       norad_id   INTEGER NOT NULL,
                       name       TEXT    NOT NULL,
                       epoch      TEXT    NOT NULL,
                       line1      TEXT    NOT NULL,
                       line2      TEXT    NOT NULL,
                       created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                       UNIQUE (norad_id, epoch)
                   );
                   """)

    # 4. Crear la tabla de observaciones del mundo real
    print("Creando tabla satellite_observations...")
    cursor.execute("""
                   CREATE TABLE satellite_observations
                   (
                       id            INTEGER PRIMARY KEY AUTOINCREMENT,
                       norad_id      INTEGER NOT NULL,
                       observed_at   TEXT    NOT NULL,
                       azimuth_deg   REAL,
                       elevation_deg REAL,
                       distance_km   REAL,
                       station_id    INTEGER
                   );
                   """)

    conn.commit()
    conn.close()
    print("¡Base de datos inicializada de forma segura y tablas creadas exitosamente!")


if __name__ == "__main__":
    inicializar_base_de_datos()
