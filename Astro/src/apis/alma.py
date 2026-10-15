import warnings
from erfa import ErfaWarning
from astropy.time import Time
from pyvo.dal import TAPService  # ¡SOL!

# Silenciamos el ErfaWarning molesto de Astropy
warnings.filterwarnings("ignore", category=ErfaWarning)


def transformar_a_mjd(fecha_iso: str) -> float:
    """Convierte formato estándar YYYY-MM-DD a Julian date (MJD) usando Astropy."""
    try:
        t = Time(fecha_iso, format='iso', scale='utc')
        return float(t.mjd)
    except Exception as e:
        print(f"[Astro SDK] ERROR al convertir fecha {fecha_iso} a MJD: {e}")
        return 61324.0


def ask_schedule_alma(start_date: str, end_date: str) -> list:
    """
    Consulta las planificaciones de ALMA utilizando el cliente oficial TAP de la IVOA.
    """
    # Endpoint oficial del servicio TAP de ALMA
    url_tap = "https://almascience.eso.org/tap"

    mjd_start = transformar_a_mjd(start_date)
    mjd_end = transformar_a_mjd(end_date)

    # Tu consulta ADQL original bajo el modelo ObsCore
    query_adql = f"""
    SELECT TOP 10
        target_name, s_ra, s_dec, s_fov, t_min, t_max, instrument_name
    FROM
        ivoa.obscore
    WHERE
        t_min >= {mjd_start} AND
        t_max <= {mjd_end}
    ORDER BY
        t_min ASC
    """

    try:
        print(f"[Astro SDK] Conectando de forma segura a ALMA TAP vía PyVO...")
        # Conectamos al servicio usando el protocolo estandarizado
        service = TAPService(url_tap)

        # Ejecutamos la consulta ADQL. PyVO se encarga de pedir VOTable y parsearlo
        resultados = service.search(query_adql)

        # Convertimos los resultados a la lista de diccionarios estándar de tu SDK
        eventos_programados = []
        for fila in resultados:
            eventos_programados.append({
                "observatorio": "ALMA",
                "objeto": str(fila["target_name"]),
                "ra": float(fila["s_ra"]),
                "dec": float(fila["s_dec"]),
                "fov_deg": float(fila["s_fov"]) if fila["s_fov"] is not None else 1.0,
                "t_start": float(fila["t_min"]),
                "t_end": float(fila["t_max"]),
                "instrument_name": str(fila["instrument_name"])
            })

        return eventos_programados

    except Exception as e:
        print(f"[Astro API Error] FALLO crítico al consultar ALMA vía PyVO: {e}")
        return []

#TODO - THIS IS FOR TESTING SUIT - PYTEST/GITHUBACTIONS
"""
def _obtener_datos_simulados(mjd_start: float, mjd_end: float) -> list:
    #Función interna para generar respuestas estables con la misma firma de datos.
    print(f"[MOCK] Generando eventos de simulación estables para el rango MJD [{mjd_start} - {mjd_end}]")
    return [
        {
            "observatorio": "ALMA",
            "objeto": "Orion Nebula (M42)",
            "ra": 83.8221,
            "dec": -5.3911,
            "fov_deg": 0.5,
            "t_start": mjd_start,
            "t_end": mjd_start + 0.1,
            "instrument_name": "ALMA_Band6"
        },
        {
            "observatorio": "ALMA",
            "objeto": "Sagittarius A*",
            "ra": 266.4168,
            "dec": -29.0078,
            "fov_deg": 0.2,
            "t_start": mjd_start + 0.05,
            "t_end": mjd_end,
            "instrument_name": "ALMA_Band7"
        }
    ]
"""



