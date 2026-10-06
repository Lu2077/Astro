from fastapi import APIRouter, HTTPException
import subprocess
import sys
import os

router = APIRouter(prefix="/api/data", tags=["1. Ingesta de Datos TLE"])

# Detectar la raíz del proyecto para evitar rutas fijas/hardcodeadas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@router.post("/update-tles")
def ejecutar_flujo_ingesta():
    """
    Sincroniza el flujo secuencial original del laboratorio:
    1. Ejecuta celes_starlink.py (Descarga TLE de internet)
    2. Ejecuta celes_trak.py (Procesa e inyecta en la Base de Datos)
    """
    try:
        # Clonar el entorno de Python y asegurar que reconozca la raíz del repositorio
        env_laboratorio = os.environ.copy()
        env_laboratorio["PYTHONPATH"] = BASE_DIR + ":" + env_laboratorio.get("PYTHONPATH", "")

        # --- SUB-PASO 1: Descargar TLE ---
        script_descarga = os.path.join(BASE_DIR, "Astro", "src", "apis", "celes_starlink.py")
        result_descarga = subprocess.run([sys.executable, script_descarga], capture_output=True, text=True,
                                         env=env_laboratorio)

        if result_descarga.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Fallo en celes_starlink: {result_descarga.stderr}")

        # --- SUB-PASO 2: Inyectar en SQLite ---
        script_inyeccion = os.path.join(BASE_DIR, "Astro", "src", "apis", "celes_trak.py")
        result_inyeccion = subprocess.run([sys.executable, script_inyeccion], capture_output=True, text=True,
                                          env=env_laboratorio)

        if result_inyeccion.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Fallo en celes_trak: {result_inyeccion.stderr}")

        # Si ambos scripts nativos corrieron con éxito, devolvemos sus salidas exactas a la web
        return {
            "status": "success",
            "paso_1_celes_starlink": result_descarga.stdout.strip(),
            "paso_2_celes_trak": result_inyeccion.stdout.strip(),
            "message": "Flujo secuencial ejecutado correctamente en el hardware de la RPi5."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la automatización del flujo: {str(e)}")
