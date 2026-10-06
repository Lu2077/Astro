import sys
import os

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
from fastapi.middleware.cors import CORSMiddleware

try:
    from src.routers.track_router import router as track_router
    from src.routers.localization_router import router as localization_router
    from src.routers.mock_celestrak_router import router as mock_celestrak_router
except ModuleNotFoundError:
    from Astro.src.routers.track_router import router as track_router
    from Astro.src.routers.localization_router import router as localization_router
    from Astro.src.routers.mock_celestrak_router import router as mock_celestrak_router

app = FastAPI(
    title="Astro API - Distributed Lab Cluster",
    description="Nodo de Cómputo Pesado y Balística Orbital en Raspberry Pi 5",
    version="1.0.0"
)

# Habilitar CORS para permitir futuras conexiones cableadas de la RPi4

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#-----------------------------------------------------------------

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

