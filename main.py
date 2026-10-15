#TODO
"""
RE-ORGANIZE THIS!
satellites
"""


"""
* - IMPORTACIONES

** - CONFIG

*** - LOG. NEGOCIO/FUNCIONES

**** - APP FASTAPI

***** - RUTAS BASE
"""
#======================IMPORTS=========================

import sys
import os
import logging

from enum import Enum
from fastapi import Query

# 1. FORZAR LAS RUTAS DE PYTHON (antes de imports de src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

sub_astro = os.path.join(BASE_DIR, "Astro")
if os.path.exists(sub_astro) and sub_astro not in sys.path:
    sys.path.append(sub_astro)

# 2. IMPORTACIONES SEGURAS DE FASTAPI Y TU REPOSITORIO
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    from src.routers.track_router import router as track_router
    from src.routers.localization_router import router as localization_router
    from src.routers.mock_celestrak_router import router as mock_celestrak_router
except ModuleNotFoundError:
    from Astro.src.routers.track_router import router as track_router
    from Astro.src.routers.localization_router import router as localization_router
    from Astro.src.routers.mock_celestrak_router import router as mock_celestrak_router


from Astro.src.track.fov_checker import verificar_interferencia_fov
from Astro.src.track.track import charge_starlink_sats
#TODO - add ALL
from Astro.src.track.fov_localization import calcular_posiciones_satelites
from Astro.src.apis.alma import ask_schedule_alma
from Astro.src.apis.eso import (
    ask_schedule_la_silla,
    ask_schedule_paranal,
    ask_schedule_apex,
)
from Astro.src.config.observatories import OBSERVATORIES
"""
Normalization
"""



#======================IMPORTS=========================


#======================CONFIG..=========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("astro-api")

STATIC_DIR = os.path.join(
    BASE_DIR,
    "Astro",
    "frontend",
    "static",
)

TEMPLATE_PATH = os.path.join(
    BASE_DIR,
    "Astro",
    "frontend",
    "templates",
    "index.html",
)
#TODO - PUT HERE REAL SATS - THIS ARE FOR TESTING PURPOSES
#ALMA - DATA EXPOSURE STATE SUCCESS!! INTRUSO'' SAT SIMULATION - GIVES ALERT - STATE SUCCESS
ALMA_DEFAULT_START = "2026-10-11 22:00:00"
ALMA_DEFAULT_END = "2026-10-12 04:00:00"
#ESO - DATA EXPOSURE & TESTING
ESO_DEFAULT_START = "2026-10-09 22:00:00"
ESO_DEFAULT_END = "2026-10-11 22:00:00"

SATELITES_PREDICHOS = [
    {"name": "STARLINK-1043", "ra_deg": 53.120, "dec_deg": -27.840},
    {"name": "STARLINK-2241", "ra_deg": 120.45, "dec_deg": 15.32},
    {"name": "STARLINK-INTRUSO-CRITICO", "ra_deg": 336.6939, "dec_deg": 0.8698}
]

TODOS_LOS_SATELITES = charge_starlink_sats()



#======================CONFIG..=========================

#======================MODULES.=========================
"""
FOV
"""
def obtener_alertas_fov(
    start_date: str,
    end_date: str,
    observatorios: list[str],
    satellites: list[dict],
    eventos_muestra: int = 5,
) -> dict:
    eventos = []
    errores = {}

    for nombre in observatorios:
        nombre = nombre.lower().strip()
        config = OBSERVATORIES.get(nombre)

        if not config or not config.get("activo"):
            errores[nombre] = "Observatorio no configurado o inactivo"
            continue

        provider = config.get("tap_provider")

        try:
            if provider == "alma":
                eventos.extend(ask_schedule_alma(start_date, end_date))

            elif provider == "eso":
                funciones_eso = {
                    "la_silla": ask_schedule_la_silla,
                    "paranal": ask_schedule_paranal,
                    "apex": ask_schedule_apex,
                }

                funcion = funciones_eso.get(nombre)

                if funcion is None:
                    errores[nombre] = "No hay proveedor ESO configurado"
                else:
                    eventos.extend(funcion(start_date, end_date))

            else:
                errores[nombre] = f"Proveedor TAP desconocido: {provider}"

        except Exception as exc:
            errores[nombre] = f"{type(exc).__name__}: {exc}"

    alertas = []

    for evento in eventos:
        alertas.extend(
            verificar_interferencia_fov(
                satelites_en_orbita=satellites,
                evento_observatorio=evento,
            )
        )

    instrumentos = sorted({
        evento.get("instrument_name")
        or evento.get("instrumento")
        or evento.get("observatorio")
        for evento in eventos
        if evento
    })

    # Muestra acotada para validación sin saturar la respuesta
    muestra = [
        {
            "observatorio": evento.get("observatorio"),
            "objeto": evento.get("objeto"),
            "ra": evento.get("ra"),
            "dec": evento.get("dec"),
            "fov_deg": evento.get("fov_deg"),
            "instrument_name": evento.get("instrument_name"),
            "t_min": evento.get("t_min"),
            "t_max": evento.get("t_max"),
            "s_region": evento.get("s_region"),
        }
        for evento in eventos[:eventos_muestra]
    ]

    return {
        "status": "partial" if errores else "ok",
        "eventos_evaluados": len(eventos),
        "satelites_evaluados": len(satellites),
        "instrumentos_en_muestra": instrumentos,
        "eventos_muestra": muestra,
        "alertas": alertas,
        "errores": errores,
    }

#======================MODULES..=========================

#======================APP.FASTAPI=======================

app = FastAPI(
    title="Astro API - Distributed Lab Cluster",
    description="Nodo de Cómputo Pesado y Balística Orbital en Raspberry Pi 5",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(track_router)
app.include_router(localization_router)
app.include_router(mock_celestrak_router)

#======================APP.FASTAPI=======================


#======================BASE_ROUTES=======================

@app.get("/")
async def serve_frontend():
    """Sirve el panel de control frontend."""
    return FileResponse(TEMPLATE_PATH)


@app.get("/health")
def health():
    """Endpoint liviano para verificar que el nodo está operativo."""
    return {
        "status": "ok",
        "service": "Astro API",
        "node": "RPi5",
    }


@app.get("/api/status")
def read_root():
    """Estado general del nodo y acceso al panel."""
    return {
        "message": "Nodo RPi5 Operativo. Ingesta de datos lista.",
        "panel_control_url": "http://192.168.1.10",
    }

#======================BASE_ROUTES=======================


#======================MENU$$$$$$$=======================
class Observatorio(str, Enum):
    alma = "alma"
    la_silla = "la_silla"
    paranal = "paranal"
    apex = "apex"
#======================MENU$$$$$$$=======================


#======================NEW_MODULES=======================

@app.get("/fov/alertas")
def get_alertas_fov(
    start: str = Query(
        "2026-09-14 00:00:00",
        description="Fecha inicio YYYY-MM-DD HH:MM:SS",
    ),
    end: str = Query(
        "2026-10-14 00:00:00",
        description="Fecha fin YYYY-MM-DD HH:MM:SS",
    ),
    observatorio: Observatorio = Query(
        Observatorio.alma,
        description="Selecciona el observatorio científico",
    ),

):
    # Enum -> string: "alma", "la_silla", etc.
    nombre_observatorio = observatorio.value

    # Configuración geográfica del observatorio
    config = OBSERVATORIES[nombre_observatorio]


    satellites = calcular_posiciones_satelites(
        fecha=start,
        lat_deg=config["lat_deg"],
        lon_deg=config["lon_deg"],
        alt_m=config["alt_m"],
        constelacion="starlink",
    )

    return obtener_alertas_fov(
        start_date=start,
        end_date=end,
        observatorios=[nombre_observatorio],
        satellites=satellites
        #instruments=instrument_name["instruments"]

    )


#======================NEW_MODULES=======================

#TODO - CHECK DEPRECATED MAIN
"""
# 1. FORZAR LAS RUTAS DE PYTHON (Debe ir en la línea 1 antes de los imports de src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Agregar también la subcarpeta Astro si la jerarquía del repositorio lo requiere
sub_astro = os.path.join(BASE_DIR, "Astro")
if os.path.exists(sub_astro) and sub_astro not in sys.path:
    sys.path.append(sub_astro)

# 2. AHORA SÍ, IMPORTACIONES SEGURAS DE FASTAPI Y TU REPOSITORIO
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
#------------------------------------------
from fastapi.middleware.cors import CORSMiddleware

try:
    from src.routers.track_router import router as track_router
    from src.routers.localization_router import router as localization_router
    from src.routers.mock_celestrak_router import router as mock_celestrak_router
except ModuleNotFoundError:
    from Astro.src.routers.track_router import router as track_router
    from Astro.src.routers.localization_router import router as localization_router
    from Astro.src.routers.mock_celestrak_router import router as mock_celestrak_router

"""
#-------------------------------------adding FOV logic
"""
from Astro.src.apis.alma import ask_schedule_alma
from Astro.src.track.fov_checker import verificar_interferencia_fov
agenda_alma = ask_schedule_alma("2026-10-11 22:00:00", "2026-10-12 04:00:00")
satelites_predichos = [
    {"name": "STARLINK-1043", "ra_deg": 53.120, "dec_deg": -27.840},
    {"name": "STARLINK-2241", "ra_deg": 120.45, "dec_deg": 15.32}
]
#validador - Geom
if agenda_alma:
    primer_evento = agenda_alma[0]
    alertas = verificar_interferencia_fov(satelites_predichos, primer_evento)
#Warns for DB & FrontEnd
    print(alertas)
"""

#endpoint para fov_checker.py

"""
@app.get("/api/v1/auditar-fov")
def auditar_fov(
    start_date: str = Query(..., description="Fecha de inicio ISO (YYYY-MM-DD HH:MM:SS)"),
    end_date: str = Query(..., description="Fecha de fin ISO (YYYY-MM-DD HH:MM:SS)")
):
    COMENT
    "
    Dynamic Endpoint fov_checker
    Orchestrating remote data ingest from ALMA
    Extracting orbits and gen. interferences alarms!
    "
    COMENT
    agenda_alma = ask_schedule_alma(start_date, end_date)

    if not agenda_alma:
        return {
            "status": "succes",
            "message": "scheduled obs. blocks not found",
            "alertas": []
        }

    COMENT
    "
    from spg4 propagator / local TLE
    let; Simulation data / Starlink!
    "
    COMENT
    satelites_predichos = [
        {"name": "STARLINK-1043", "ra_deg": 53.120, "dec_deg": -27.840},
        {"name": "STARLINK-2241", "ra_deg": 120.45, "dec_deg": 15.32}
    ]

    todas_las_alertas = []
    for evento in agenda_alma:
        #fov_checker function evaluates sats & comparing with M sats
        alertas_evento = verificar_interferencia_fov(satelites_predichos, evento)
        if alertas_evento:
            todas_las_alertas.extend(alertas_evento)

    return {
        "status": "success",
        "rango_evaluado": {"desde": start_date, "hasta": end_date},
        "total_eventos_alma": len(agenda_alma),
        "total_alertas_criticas": len(todas_las_alertas),
        "alertas": todas_las_alertas
    }
"""
#--------------------Swagger--------------------
#TODO - CHECK FASTAPI LOGIC & COMPARE
"""
app = FastAPI(
    title="Astro API - Distributed Lab Cluster",
    description="Nodo de Cómputo Pesado y Balística Orbital en Raspberry Pi 5",
    version="1.0.0"
)
STATIC_DIR = "/home/lucas2/proyecto-backend/Astro/Astro/frontend/static"
TEMPLATE_PATH = "/home/lucas2/proyecto-backend/Astro/Astro/frontend/templates/index.html"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_frontend():
    #Ruta index.html!!
    return FileResponse(TEMPLATE_PATH)

# Habilitar CORS para permitir futuras conexiones cableadas de la RPi4

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

#-----------------------------------------------------------------

#TODO - WARNING - THIS IS ROUTER FOR FASTAPI EXPOSURE;;

"""
# Registrar el router en el mapa general de FastAPI
app.include_router(track_router)
app.include_router(localization_router)

try:
    app.include_router(mock_celestrak_router)
    print("[MOCK] Simulation Router from Celestrak succesfully charged")
except Exception as e:
    print(f"WARNING [MOCK] we could not charge the simulation router: {e}")

@app.get("/")
def read_root():
    return {
        "message": "Nodo RPi5 Operativo. Ingesta de datos lista.",
        "panel_control_url": "http://192.168.1.10"
    }
"""

#----------------------------------
