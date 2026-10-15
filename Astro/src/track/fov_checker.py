import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from Astro.src.apis.alma import ask_schedule_alma
from Astro.src.apis.eso import (
    ask_schedule_la_silla,
    ask_schedule_paranal,
    ask_schedule_apex,
)



def verificar_interferencia_fov(satelites_en_orbita: list, evento_observatorio: dict) -> list:
    """
    let's make a comparison between
    pos satelites against fov real from observatories
    data from ESO/ALMA using spherical trigonometric from Astropy.

    :param satelites_en_orbita: Lista de dicts con ['name', 'ra_deg', 'dec_deg']
    :param evento_observatorio: Dicionario con el evento de observacion
    :return: sat Lists intercepted by de vision cone (Alerts gen)
    """
    alertas_generadas = []

    #let's define central coord's from telescope to ephemeride
    coordenada_telescopio = SkyCoord(
        ra=evento_observatorio["ra"] * u.deg,
        dec=evento_observatorio["dec"] * u.deg,
        frame = "icrs"
    )

    #exclusion radio FOV diamm/2 from the sensor
    radio_fov = evento_observatorio["fov_deg"] / 2.0

    #let's iterate over the sat's predictions - localizaton.py
    for sat in satelites_en_orbita:
        try:
            coordenadas_satelite = SkyCoord(
                ra=sat["ra_deg"] * u.deg,
                dec=sat["dec_deg"] * u.deg,
                frame = "icrs"
            )

            distancia_angular = coordenada_telescopio.separation(coordenadas_satelite).degree

            #Interception WARNING
            if distancia_angular <= radio_fov:
                alertas_generadas.append({
                    "observatorio": evento_observatorio.get("observatorio", "desconocido"),
                    "satelite_name": sat.get("name"),
                    "sat_ra_deg": float(sat["ra_deg"]),
                    "sat_dec_deg": float(sat["dec_deg"]),
                    "impacto_objeto": evento_observatorio.get("objeto"),
                    "instrumento_afectado": evento_observatorio.get("instrument_name"),
                    "distancia_al_centro_deg": float(distancia_angular),
                    "radio_fov_deg": radio_fov,
                    "alerta_status": "CRITICAL_BLOCK",
                })

        except (KeyError, TypeError, ValueError) as exc:
            print(
                f"[Astro Geometry Error] Satellite"
                f"{sat.get('name','unknown')}: {exc}"
            )
            continue

    return alertas_generadas


