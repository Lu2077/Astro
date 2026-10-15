#TODO agregar ESO data http://archive.eso.org/tap_obs

import warnings
from erfa import ErfaWarning
from astropy.time import Time
from pyvo.dal import TAPService
from Astro.src.apis.normalization import normalizar_evento_obscore

warnings.filterwarnings("ignore", category=ErfaWarning)

#TODO IF IT APPLIES ;


def transformar_a_mjd(fecha_iso: str) -> float:
    "Convierte formato estándar YYYY-MM-DD a Julian date (MJD) usando Astropy."
    try:
        t = Time(fecha_iso, format='iso', scale='utc')
        return float(t.mjd)
    except Exception as e:
        print(f"[Astro SDK] ERROR al convertir fecha {fecha_iso} a MJD: {e}")
        return 61324.0


ESO_TAP_URL = "https://archive.eso.org/tap_obs"


ESO_INSTRUMENTS = {
    "la_silla": ["HARPS"],
    "paranal": ["GIRAFFE"],
}

def ask_schedule_eso(
    start_date: str,
    end_date: str,
    instruments: list[str],
    limit: int = 10,
):

    mjd_start = transformar_a_mjd(start_date)
    mjd_end = transformar_a_mjd(end_date)

    placeholders = ", ".join(f"'{i}'" for i in instruments)

    query_adql = f"""
        SELECT TOP {limit}
            dp_id,
            target_name,
            s_ra,
            s_dec,
            s_fov,
            s_region,
            t_min,
            t_max,
            instrument_name,
            facility_name,
            dataproduct_type
        FROM ivoa.ObsCore
        WHERE
            t_min <= {mjd_end}
            AND t_max >= {mjd_start}
            AND s_fov IS NOT NULL
            AND instrument_name IN ({placeholders})
        ORDER BY t_min ASC
    """.strip()

    service = TAPService(ESO_TAP_URL)
    result = service.run_async(query_adql)



    eventos = []

    for row in result:
        fila = dict(row)

        if fila.get("s_ra") is None or fila.get("s_dec") is None or fila.get("s_fov") is None:
            continue

        eventos.append(
            normalizar_evento_obscore(
                row=fila,
                observatorio=fila.get("instrument_name", "ESO"),
            )
        )

    return eventos

def ask_schedule_la_silla(start_date: str, end_date: str) -> list[dict]:
    return ask_schedule_eso(start_date, end_date, ESO_INSTRUMENTS["la_silla"])

def ask_schedule_paranal(start_date: str, end_date: str) -> list[dict]:
    return ask_schedule_eso(start_date, end_date, ESO_INSTRUMENTS["paranal"])

def ask_schedule_apex(start_date: str, end_date: str) -> list[dict]:
    return ask_schedule_eso(start_date, end_date, ESO_INSTRUMENTS["apex"])