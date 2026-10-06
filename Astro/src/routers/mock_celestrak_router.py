# src/routers/mock_celestrak_router.py
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix="/api/mock/celestrak",
    tags=["Mocks & Testing"]
)

# Buscar dinámicamente la carpeta del proyecto para no usar rutas absolutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@router.get("/stations", response_class=PlainTextResponse)
def get_mock_stations():
    """
    Simula el endpoint de texto plano de Celestrak para estaciones espaciales (ISS).
    Entrega el archivo stations.tle local sin consumir ancho de banda real.
    """
    # Intentar resolver la ruta tanto si corres desde la raíz como desde la subcarpeta Astro
    posibles_rutas = [
        os.path.join(BASE_DIR, "Astro", "src", "apis", "stations.tle"),
        os.path.join(BASE_DIR, "src", "apis", "stations.tle"),
        os.path.join(BASE_DIR, "Astro", "stations.tle"),
        os.path.join(BASE_DIR, "stations.tle")
    ]

    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read()

    raise HTTPException(
        status_code=404,
        detail=f"Archivo stations.tle de simulación no encontrado en las rutas del clúster."
    )


@router.get("/starlink", response_class=PlainTextResponse)
def get_mock_starlink():
    """
    Simula el endpoint de texto plano de Celestrak para la constelación Starlink.
    """
    posibles_rutas = [
        os.path.join(BASE_DIR, "Astro", "src", "apis", "starlink.tle"),
        os.path.join(BASE_DIR, "src", "apis", "starlink.tle"),
        os.path.join(BASE_DIR, "Astro", "starlink.tle"),
        os.path.join(BASE_DIR, "starlink.tle")
    ]

    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read()

    raise HTTPException(
        status_code=404,
        detail="Archivo starlink.tle de simulación no encontrado en las rutas del clúster."
    )
