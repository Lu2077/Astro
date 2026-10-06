from fastapi import APIRouter, HTTPException
import sys
import os

#router = APIRouter(prefix="/api/track", tags=["2. Motor de Localización Balística"])

# Encontrar la raíz del proyecto para resolver las importaciones
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importación absoluta y limpia respetando la jerarquía oficial de tu repositorio
try:
    from src.track.localization import closest_satellites, satellites
except ModuleNotFoundError:
    from Astro.src.track.localization import closest_satellites, satellites
router = APIRouter(prefix="/api/track", tags=["Localization"])

@router.get("/localization")
def calcular_coordenadas_satelitales(lat: float = -33.4569, lon: float = -70.6483, radio_km: float = 500.0):
    """
    PASO 3: Consume los TLEs cargados en SQLite para calcular altitudes orbitales,
    distancias proyectadas sobre el geoide y visibilidad en un radio específico.
    """
    try:
        # CORRECCIÓN ERROR A y B: Pasamos exactamente los 2 argumentos que tu función espera,
        # usando la lista 'satellites' importada que ya tiene cargados tus 10k TLEs locales.
        resultados_crudos = closest_satellites(satellites, max_distance_km=radio_km)

        # CORRECCIÓN PROBLEMA JSON: Limpiamos los datos antes de enviarlos a la web.
        # Eliminamos el objeto binario "sat" no-serializable para que FastAPI responda en verde.
        resultados_limpios = []
        for item in resultados_crudos:
            resultados_limpios.append({
                "nombre": str(item["nombre"]),
                "distancia_subpunto": round(item["distancia_subpunto"], 2),
                "altura_orbital": round(item["altura_orbital"], 2),
                "rango_real": round(item["rango_real"], 2),
                "lat": round(item["lat"], 4),
                "lon": round(item["lon"], 4)
            })

        return {
            "status": "success",
            "total_visibles": len(resultados_limpios),
            "satellites": resultados_limpios
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fallo en los hilos de cálculo de localization.py: {str(e)}"
        )

