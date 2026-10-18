
import math
import time
from pathlib import Path

#from astroplan import Observer
from skyfield.api import load

#from Astro.src.track.vel_sat import muestra
#from Astro.src.sdk.math.geometry import extract_poligon_vertices
from Astro.src.apis.alma import ask_schedule_alma
#--------------------NOT CALLABLE FUNCTION------------------------?#$%!
#from Astro.src.config.observatories import observatories_repo

#==========================SALIERI=GOT=IN=TO=THE=COURT=FIRST=THAN=MOZART============================

from Astro.src.sdk.math.geometry import (
    extract_poligon_vertices,
    obtain_bounding_box,
    is_point_on_polygon
)


ts = load.timescale()

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "data" / "astro.sqlite3"

import math

def intervalos_mjd_gen(t_start: float, t_end: float, step_hrs: float = 1.0) -> list:
    """Genera pasos temporales en MJD evitando colapsar la Raspberry Pi."""
    pasos = []
    paso_mjd = step_hrs / 24.0
    actual = t_start
    # Tolerancia de punto flotante para no perder el último segundo
    while actual <= t_end + 1e-9:
        pasos.append(actual)
        actual += paso_mjd
    return pasos

def calc_magnitudes_sat(sat, t_mjd: float, observador) -> dict:
    """
    MOCK ACUTADO: Emula a vel_sat devolviendo un diccionario limpio.
    Sustituye los NaN por None para que el Response Body sea profesional.
    """
    # Aquí simulas el paso de tu script real
    # Si el satélite no es visible en ese MJD, distance_km o alt_deg deben ser None
    return {
        "tle_id": getattr(sat, 'id', 1),
        "norad_id": getattr(sat, 'norad_id', 44714),
        "sat_name": getattr(sat, 'name', "STARLINK-1008"),
        "mjd_epoch": t_mjd,
        "ra": 261.163,          # Forzamos coordenadas dentro de tu test de ALMA
        "dec": -38.925,         # Forzamos coordenadas dentro de tu test de ALMA
        "alt_deg": 75.87,       # Datos limpios de tu terminal
        "az_deg": 142.12,
        "v_radial_kms": -1.905, # Negativo acercándose
        "orbital_altitude_km": 487.13,
        "distance_km": 502.49   # Si fuera invisible, pones None aquí
    }

def verify_nan(calc_state: dict) -> bool:
    """Tu escudo directo contra datos corruptos en el Response Body."""
    if calc_state["distance_km"] is None or calc_state["alt_deg"] is None:
        return True
    # Tolerancia si por alguna razón SGP4 llegó a escupir un NaN flotante real
    if math.isnan(calc_state["ra"]) or math.isnan(calc_state["dec"]):
        return True
    return False

#==========================UPPER=TESTING=PURPOSES=========================================

def back_track_fov(
        evento_alma: dict,
        db_path: Path = DB_PATH,
        step_hrs: float = 1.0,
) -> list:

    #TODO - LETS VERIFY TIME FRAME


    t_start_mjd = evento_alma["t_min"]
    t_end_mjd = evento_alma["t_max"]

    #s_region reported by ALMA/ObsCore.
    polygon_str = evento_alma["s_region"]


    #Parser
    #vertices_alma = extract_poligon_vertices(polygon_str)

    try:
        vertices_alma = extract_poligon_vertices(polygon_str)
    except ValueError as e:
        print(f"[FOV inválido] {e}")
        return []

    #Bounding box:
    bbox = obtain_bounding_box(vertices_alma)

    time_steps = intervalos_mjd_gen(
        t_start_mjd,
        t_end_mjd,
        step_hrs=step_hrs,
    )

    alertas_evento = []
    observador_alma = None
    """
    lets make - main loop (linear)
    """
    #TODO - THIS IS A MOCK FOR MVP - IT SHOULD BRING THE SAMPLES FROM 'satellite_tles'
    satellites_sample = [type('Sat', (object,), {'id': 1, 'norad_id': 44714, 'name': 'STARLINK-1008'})()]

    for t_mjd in time_steps:

        for sat in satellites_sample:
            try:
                # Propaga el satélite y calcula magnitudes: RA, Dec, rango, velocidad, etc.
                calc_state = calc_magnitudes_sat(
                    sat,
                    t_mjd,
                    observador_alma,
                )

                # Descarta estados numéricamente inválidos.
                if (
                        math.isnan(calc_state["distance_km"])
                        or math.isnan(calc_state["alt_deg"])
                ):
                    continue

                # Persiste el estado calculado para auditoría posterior.
                save_refined_state_db(calc_state, db_path)

                # Comprueba si la posición aparente cae dentro del polígono ALMA.
                if is_point_on_polygon(
                        calc_state["ra"],
                        calc_state["dec"],
                        vertices_alma,
                ):
                    alerta_warn = gen_warn_structure(
                        sat,
                        t_mjd,
                        calc_state,
                    )
                    alertas_evento.append(alerta_warn)

            except Exception as e:
                #SGP4 failure - will not let the function stops
                print(
                    f"[Error] Satélite {sat.norad_id} "
                    f"en MJD {t_mjd}: {e}"
                )
                continue

    #add event - persistend result
    save_backtracking_results(
        alertas_evento,
        evento_alma,
        db_path,
    )

    return alertas_evento

def save_refined_state_db(calc_state: dict, db_path: Path):
    """Mock de escritura para ssa_calculated_states. Evita delay en el frontend."""
    pass

def gen_warn_structure(sat, t_mjd: float, calc_state: dict) -> dict:
    """Estructura el JSON final que tu frontend va a renderizar en la tabla de alertas."""
    return {
        "satelite": calc_state["sat_name"],
        "norad_id": calc_state["norad_id"],
        "mjd": t_mjd,
        "velocidad_radial": f"{calc_state['v_radial_kms']} km/s",
        "estado": "CRUZA_FOV_ALMA",
        "impacto": "CRÍTICO"
    }

def save_backtracking_results(alertas, evento, db_path):
    """Mock de escritura para backtracking_results."""
    pass


if __name__ == "__main__":
    # Prueba en frío: usa un evento ALMA sintético o previamente guardado,
    # sin llamar a ask_schedule_alma() ni escribir necesariamente en la BD.
    evento_prueba = {
        "t_min": 61324.0,  # MJD inicial
        "t_max": 61324.5,  # MJD final
        "s_region": "Polygon ICRS "
        "261.172568 -38.923861 "
        "261.172796 -38.926670 "
        "261.171678 -38.929347 "
        "261.169372 -38.931515 "
        "261.167870 -38.932310 "
        "261.165620 -38.933003 "
        "261.162009 -38.933179 "
        "261.160236 -38.932871 "
        "261.158046 -38.932070 "
        "261.155409 -38.930143 "
        "261.153869 -38.927596 "
        "261.153642 -38.924787 "
        "261.154760 -38.922111 "
        "261.157066 -38.919943 "
        "261.158569 -38.919148 "
        "261.160818 -38.918455 "
        "261.164428 -38.918279 "
        "261.166772 -38.918747 "
        "261.168391 -38.919388 "
        "261.171028 -38.921315"
    }

    alertas = back_track_fov(
        evento_alma=evento_prueba,
        db_path=DB_PATH,
        step_hrs=1.0,
    )

    print(f"Alertas detectadas: {len(alertas)}")
    for alerta in alertas:
        print(alerta)