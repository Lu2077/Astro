import sqlite3
from pathlib import Path
import numpy as np
from skyfield.api import EarthSatellite, load
from astropy.time import Time

# pathlib
BASE_DIR = Path(__file__).resolve().parents[3]  # Astro/src/sdk/
DEFAULT_DB_PATH = BASE_DIR / "data" / "astro.sqlite3"

#TODO - BUILD BACKTRACKING VALIDATOR

class OrbitalValidatorSDK:

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.ts = load.timescale()

    def obtain_available_norad_ids(self, name_pattern: str = "STARLINK%") -> list[dict]:
        """
        Devuelve los satélites disponibles que tienen al menos 2 TLEs,
        agrupados por NORAD ID extraído de la línea 1 del TLE.
        """
        query = """
                SELECT substr(line1, 3, 5) AS norad_id, \
                       name, \
                       COUNT(*)            AS tle_count, \
                       MIN(epoch)          AS first_epoch, \
                       MAX(epoch)          AS last_epoch
                FROM satellite_tles
                WHERE name LIKE ?
                GROUP BY norad_id, name
                HAVING COUNT(*) >= 2
                ORDER BY tle_count DESC, last_epoch DESC; \
                """

        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found at: {self.db_path}")

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, (name_pattern,)).fetchall()

        return [dict(row) for row in rows]

    def obtain_historical_tles(self, norad_id: str, limit: int = 5) -> list:
        query = """
                SELECT name, line1, line2, epoch
                FROM satellite_tles
                WHERE substr(line1, 3, 5) = ?
                ORDER BY epoch DESC, created_at DESC, id DESC LIMIT ?; \
                """

        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found at: {self.db_path}")

        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                query,
                (norad_id.zfill(5), limit),
            ).fetchall()


        if len(rows) < 2:
            raise ValueError(
                f"NORAD {norad_id} has fewer than 2 TLEs; cannot validate"
            )

        return rows

    def calculate_angular_distance(self, ra1, dec1, ra2, dec2):
        """
        Astrodynamic - angular ortodrómica
        SSA - Degrees Error Calculation
        """
        r1, d1 = np.radians(ra1), np.radians(dec1)
        r2, d2 = np.radians(ra2), np.radians(dec2)

        # Fórmula matemática correcta de la distancia angular ortodrómica
        cos_dist = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(r1 - r2)

        # Clip to avoid float precision errors outside [-1, 1]
        cos_dist = np.clip(cos_dist, -1.0, 1.0)
        return np.degrees(np.arccos(cos_dist))

    def validate_starlink_constellation(self, limit_per_satellite: int = 5, max_satellites: int = 10) -> list[dict]:
        """
        Procesa un lote controlado (batch) de satélites para evitar congelar la CPU/Disk I/O.
        """
        satellites = self.obtain_available_norad_ids("STARLINK%")
        results = []

        # Limitamos el bucle al número máximo de satélites solicitado para el lote
        sampled_satellites = satellites[:max_satellites]
        print(f"[Astro SDK] Batch configuration: Processing {len(sampled_satellites)} of {len(satellites)} total satellites...")

        for satellite in sampled_satellites:
            try:
                result = self.validate_orbital(
                    norad_id=satellite["norad_id"],
                    limit=limit_per_satellite,
                )
                results.append(result)
            except (ValueError, FileNotFoundError) as e:
                results.append({
                    "norad_id": satellite["norad_id"],
                    "satellite_name": satellite["name"],
                    "data_quality_status": "SKIPPED",
                    "message": str(e),
                })

        return results

    def validate_orbital(self, norad_id: str, limit: int = 5) -> dict:
        historical = self.obtain_historical_tles(norad_id, limit=limit)

        if len(historical) < 2:
            return {
                "status": "DATA_INSUFFICIENT",
                "message": "At least 2 historical TLEs are required",
            }

        tle_newest = historical[0]
        tle_oldest = historical[-1]

        sat_new = EarthSatellite(tle_newest[1], tle_newest[2], tle_newest[0], self.ts)
        sat_old = EarthSatellite(tle_oldest[1], tle_oldest[2], tle_oldest[0], self.ts)

        if str(sat_new.model.satnum) != str(sat_old.model.satnum):
            raise ValueError(
                f"TLE mismatch: {sat_new.model.satnum} vs {sat_old.model.satnum}"
            )

        if sat_new.epoch == sat_old.epoch:
            return {
                "status": "DATA_INSUFFICIENT",
                "message": "Selected TLEs have identical epochs; cannot measure propagation error",
            }

        time_target = sat_new.epoch

        pos_new = sat_new.at(time_target)
        pos_old = sat_old.at(time_target)

        ra_n, dec_n, _ = pos_new.radec()
        ra_v, dec_v, _ = pos_old.radec()

        grad_error = self.calculate_angular_distance(
            ra_n.hours * 15.0, dec_n.degrees,
            ra_v.hours * 15.0, dec_v.degrees,
        )

        status = "VALID" if grad_error < 0.2 else "INVALID"
        if grad_error > 1.0:
            status = "CRITICAL_ERROR"

        days_offset = float(time_target - sat_old.epoch)
        hours_offset = days_offset * 24.0
        minutes_offset = days_offset * 60.0

        return {
            "norad_id": norad_id,
            "satellite_name": tle_newest[0],
            "days_offset": days_offset,
            "hours_offset": hours_offset,
            "minutes_offset": minutes_offset,
            "angular_error_degrees": float(grad_error),
            "data_quality_status": status,
            "metrics": {
                "reference_epoch": time_target.utc_iso(),
                "propagated_epoch": sat_old.epoch.utc_iso(),
            },
        }


if __name__ == "__main__":
    print("[Astro SDK] Running validation module...")

    validator = OrbitalValidatorSDK()

    try:
        available = validator.obtain_available_norad_ids("STARLINK%")

        if not available:
            raise ValueError("No STARLINK satellites with at least 2 TLEs were found")

        print(f"[Astro SDK] Found {len(available)} STARLINK satellites eligible for validation.")

        # Solicitamos un lote rápido de 5 satélites para validar la matemática en frío sin saturar la Pi
        print("\n[Astro SDK] Activating Batch Processing via validate_starlink_constellation()...")
        constellation_results = validator.validate_starlink_constellation(
            limit_per_satellite=5,
            max_satellites=5
        )

        print(f"\n[Astro SDK] Batch Analysis Results ({len(constellation_results)} processed):")
        print("-" * 80)
        for sample in constellation_results:
            print(f"-> NORAD {sample.get('norad_id')} ({sample.get('satellite_name')}):")
            print(
                f"   Status: {sample.get('data_quality_status')} | Error Angular: {sample.get('angular_error_degrees', 0):.4f}°")
            print(f"   Offset: {sample.get('days_offset', 0):.4f} days ({sample.get('hours_offset', 0):.2f} hours)")
            print("-" * 80)

    except Exception as e:
        print(f"\n[Astro SDK] Validation pipeline failed: {e}")


