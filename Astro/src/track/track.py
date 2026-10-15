#TODO - IMPORT FROM DATABASE NO LOCAL TLE (DELAY)



"""
import os
from skyfield.api import load
from skyfield.iokit import parse_tle_file

def charge_starlink_sats():
    ts = load.timescale()

    # 1. Obtiene la carpeta exacta donde está parado ESTE script (Astro/src/track/)
    ruta_actual = os.path.dirname(os.path.abspath(__file__))

    # 2. Subimos un nivel a 'src/' y entramos a 'apis/starlink.tle' de forma dinámica
    ruta_archivo = os.path.abspath(os.path.join(ruta_actual, "..", "apis", "starlink.tle"))

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'rb') as f:
            sats = list(parse_tle_file(f, ts))
        return sats
    else:
        print(f"Error: no se encontro el archivo en {ruta_archivo}")
        return []

if __name__ == '__main__':
    lista_sat = charge_starlink_sats()
    print('Ejecución directa de prueba: Loaded', len(lista_sat), 'satellites')
"""
import sqlite3
from pathlib import Path

from skyfield.api import EarthSatellite, load

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "data" / "astro.sqlite3"


def charge_starlink_sats(db_path: Path = DB_PATH):
    ts = load.timescale()
    satellites = []

    query = """
        SELECT norad_id, name, epoch, line1, line2
        FROM satellite_tles
        WHERE id IN (
            SELECT id
            FROM (
                SELECT id,
                       ROW_NUMBER() OVER (
                           PARTITION BY norad_id
                           ORDER BY epoch DESC, created_at DESC, id DESC
                       ) AS rn
                FROM satellite_tles
                WHERE name LIKE 'STARLINK%'
            )
            WHERE rn = 1
        )
        ORDER BY name;
    """

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row

        total = conn.execute("SELECT COUNT(*) FROM satellite_tles").fetchone()[0]
        print(f"Total de TLEs en satellite_tles: {total}")

        rows = conn.execute(query).fetchall()
        print(f"Filas devueltas por la consulta de últimos TLEs: {len(rows)}")

        if rows:
            print("Primer registro:")
            print(dict(rows[0]))

        for row in rows:
            try:
                sat = EarthSatellite(row["line1"], row["line2"], row["name"], ts)
                satellites.append(sat)
            except Exception as exc:
                print(f"Error creando satélite {row['norad_id']}: {exc}")

    return satellites


if __name__ == "__main__":
    lista_sat = charge_starlink_sats()
    print(f"Loaded {len(lista_sat)} satellites from database")