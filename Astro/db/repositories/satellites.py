import sqlite3
import os
from skyfield.api import EarthSatellite

class SatelliteRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            # 1. Encuentra la ruta absoluta de este archivo 'satellites.py'
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # 2. Sube tres niveles en el árbol de directorios para llegar a la raíz (Astro/)
            # de Astro/db/repositories/ -> Astro/db/ -> Astro/ -> Raíz del proyecto
            root_dir = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))
            # 3. Define la ruta absoluta final hacia la carpeta data
            self.db_path = os.path.join(root_dir, "data", "astro.sqlite3")
        else:
            self.db_path = db_path

# ==================================================================================
# 1. GESTION DE LOS TLEs (Datos del Espacio Exterior)
# ==================================================================================

    def save_tle(self, norad_id: int, name: str, epoch: str, line1: str, line2: str):
        """Guarda un TLE en la base de datos ignorando duplicados."""
        query = """
                INSERT \
                OR IGNORE INTO satellite_tles (norad_id, name, epoch, line1, line2)
            VALUES (?, ?, ?, ?, ?) \
                """
        # Aseguramos que la carpeta 'data' exista de forma absoluta antes de conectar
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, (norad_id, name, epoch, line1, line2))

    def get_tle_for_observation(self, norad_id: int, observation_time: str, timescale) -> EarthSatellite:
        """
        Busca el TLE histórico óptimo: el más cercano pero ANTERIOR
        al momento de tu observación real.
        """
        query = """
                SELECT name, line1, line2 \
                FROM satellite_tles
                WHERE norad_id = ? \
                  AND epoch <= ?
                ORDER BY epoch DESC LIMIT 1 \
                """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (norad_id, observation_time))
            row = cursor.fetchone()

        if row:
            name, line1, line2 = row
            return EarthSatellite(line1, line2, name, timescale)
        return None

# ==================================================================================
# 2. GESTIÓN DE OBSERVACIONES (Tus lecturas diarias en la Tierra)
# ==================================================================================

    def save_observation(self, norad_id: int, observed_at: str, az: float, el: float, dist: float = None):
        """
        Registra una lectura física de tu sensor.
        Permite múltiples lecturas diarias sin restricción UNIQUE.
        """
        query = """
                INSERT INTO satellite_observations (norad_id, observed_at, azimuth_deg, elevation_deg, distance_km)
                VALUES (?, ?, ?, ?, ?) \
                """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, (norad_id, observed_at, az, el, dist))

