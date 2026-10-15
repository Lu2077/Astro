import sqlite3
from datetime import datetime
from skyfield.api import load, wgs84, EarthSatellite
from astropy.time import Time
from Astro.src.track.fov_checker import verificar_interferencia_fov


def obtener_ultimo_tle_db(norad_id: str, db_path: str = "data/astro.sqlite3") -> tuple:
    """
    Paso 1: Busca en tu tabla SQLite el TLE más reciente para un satélite.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Consulta optimizada: solo la última fila de ese dispositivo
    cursor.execute("""
                   SELECT name, tle_line1, tle_line2
                   FROM satellites
                   WHERE norad_id = ?
                   ORDER BY epoch_timestamp DESC LIMIT 1
                   """, (norad_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"No se encontraron TLEs en la DB para el NORAD ID {norad_id}")
    return row[0], row[1], row[2]


def predecir_posicion_satelital_real(norad_id: str, tiempo_mjd: float, lat_obs: float, lon_obs: float,
                                     ele_obs: float) -> dict:
    """
    Paso 2: Parsea el TLE a SGP4 usando Skyfield y calcula las coordenadas
    celestes (RA/DEC) reales vistas desde la ubicación del telescopio.
    """
    # 1. Extraemos la data de tu SQLite
    name, line1, line2 = obtener_ultimo_tle_db(norad_id)

    # 2. Skyfield inicializa el motor SGP4 interno al instanciar EarthSatellite
    ts = load.timescale()
    sat_sgp4 = EarthSatellite(line1, line2, name, ts)

    # 3. Convertimos el tiempo MJD del evento a tiempo de Skyfield
    t_astropy = Time(tiempo_mjd, format='mjd')
    t_skyfield = ts.from_astropy(t_astropy)

    # 4. Definimos la posición geográfica del observatorio (WGS84)
    observatorio = wgs84.latlon(lat_obs, lon_obs, elevation_m=ele_obs)

    # 5. Calculamos la posición topocéntrica (el bache geométrico que te faltaba)
    diferencia = sat_sgp4 - observatorio
    topocéntrico = diferencia.at(t_skyfield)

    # 6. Extraemos la Ascensión Recta y Declinación astronómicas aparente en el cielo
    ra, dec, distance = topocéntrico.radec()

    return {
        "name": name,
        "ra_deg": float(ra.hours * 15.0),  # Skyfield entrega RA en horas, multiplicamos por 15 para grados
        "dec_deg": float(dec.degrees)
    }


# --- ORQUESTACIÓN EN CALIENTE ---

# 1. Obtenemos la agenda real de ALMA de la noche (vía tu script ask_schedule_alma)
# Supongamos que nos devuelve un evento apuntando a RA=53.0, DEC=-27.0 en un tiempo t_mjd
evento_alma = {
    "observatorio": "ALMA",
    "objeto": "Galaxia de Prueba",
    "ra": 53.123,
    "dec": -27.844,
    "fov_deg": 0.5,
    "t_start_mjd": 61324.15,  # Tiempo en el que el telescopio va a mirar
    "instrument_name": "Band 7 Receiver"
}

# Coordenadas geográficas de ALMA (Llano de Chajnantor)
LAT_ALMA = -23.029
LON_ALMA = -67.755
ELEV_ALMA = 5000.0

# 2. Calculamos la posición SGP4 real del satélite para ese segundo exacto
# Reemplaza '99999' por un código NORAD real de Starlink que tengas en tu SQLite
try:
    satelite_calculado = predecir_posicion_satelital_real(
        norad_id="99999",
        tiempo_mjd=evento_alma["t_start_mjd"],
        lat_obs=LAT_ALMA, lon_obs=LON_ALMA, ele_obs=ELEV_ALMA
    )

    # 3. Mandamos el cálculo real al FOV checker (¡Adiós Mocks!)
    satelites_a_verificar = [satelite_calculado]
    alertas_reales = verificar_interferencia_fov(satelites_a_verificar, evento_alma)

    print("[Astro Real-Time Logs] Alertas generadas en producción:")
    print(alertas_reales)

except Exception as e:
    print(f"Error en la cadena de ejecución: {e}")

