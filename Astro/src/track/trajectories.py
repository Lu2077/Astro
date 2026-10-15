import sqlite3
from pathlib import Path

from astropy.time import Time
from skyfield.api import EarthSatellite, load, wgs84

from Astro.src.track.fov_checker import verificar_interferencia_fov


BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "data" / "astro.sqlite3"


def obtener_ultimo_tle_db(norad_id: int, db_path: Path = DB_PATH) -> tuple[str, str, str]:
    """Devuelve (name, line1, line2) del TLE más reciente para un NORAD ID."""

    query = """
        SELECT name, line1, line2
        FROM satellite_tles
        WHERE name LIKE 'STARLINK%'
        ORDER BY epoch DESC, created_at DESC, id DESC LIMIT ?; \
        """

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(query, (norad_id,)).fetchone()

    if not row:
        raise ValueError(
            f"No se encontraron TLEs en la DB para el NORAD ID {norad_id}"
        )

    return row[0], row[1], row[2]


def predecir_posicion_satelital_real(
    norad_id: int,
    tiempo_mjd: float,
    lat_obs: float,
    lon_obs: float,
    ele_obs: float,
) -> dict:
    """Calcula RA/Dec aparentes del satélite vistos desde el observatorio."""

    name, line1, line2 = obtener_ultimo_tle_db(norad_id)

    ts = load.timescale()
    sat = EarthSatellite(line1, line2, name, ts)

    t_astropy = Time(tiempo_mjd, format="mjd")
    t_skyfield = ts.from_astropy(t_astropy)

    observatorio = wgs84.latlon(lat_obs, lon_obs, elevation_m=ele_obs)

    diferencia = sat - observatorio
    topocentrico = diferencia.at(t_skyfield)

    ra, dec, distance = topocentrico.radec()

    return {
        "name": name,
        "norad_id": norad_id,
        "ra_deg": float(ra.hours * 15.0),
        "dec_deg": float(dec.degrees),
        "distance_km": float(distance.km),
    }

if __name__ == "__main__":
    print(">>> Iniciando trajectories.py")

    evento_alma = {
        "observatorio": "ALMA",
        "objeto": "Galaxia de Prueba",
        "ra": 53.123,
        "dec": -27.844,
        "fov_deg": 0.5,
        "t_start_mjd": 61324.15,
        "instrument_name": "Band 7 Receiver",
    }

    LAT_ALMA = -23.029
    LON_ALMA = -67.755
    ELEV_ALMA = 5000.0

    try:
        satelite = predecir_posicion_satelital_real(
            norad_id=67796,
            tiempo_mjd=evento_alma["t_start_mjd"],
            lat_obs=LAT_ALMA,
            lon_obs=LON_ALMA,
            ele_obs=ELEV_ALMA,
        )

        print(">>> Posición calculada:")
        print(satelite)

        alertas = verificar_interferencia_fov([satelite], evento_alma)

        print(">>> Alertas generadas:")
        print(alertas)

    except Exception as exc:
        print(f">>> Error en la cadena: {type(exc).__name__}: {exc}")