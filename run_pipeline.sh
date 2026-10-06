#!/bin/bash

# ==============================================================
# ASTRO PIPELINE - CONTROL DE INGESTA / INPUT DATA CONTROL
# AVOIDING BLOCKED IP DUE TO EXCESS OF REQUESTS - CELESTRAK
# =============================================================

PROJECT_ROOT="/home/lucas2/proyecto-backend/Astro"
PYTHON_BIN="$PROJECT_ROOT/env/bin/python3"
TLE_FILE="$PROJECT_ROOT/Astro/src/apis/starlink.tle"

echo "🛰️ [$(date '+%Y-%m-%d %H:%M:%S')] Iniciando ciclo de actualización Astro..."

# verified  - network (petition 24hrs limits or else)
if [ -f "$TLE_FILE" ] && [ -n "$(find "$TLE_FILE" -mmin -1440 2>/dev/null)" ]; then
    echo "🛡️ [CONTROL DE RED] Los TLEs locales se descargaron hace menos de 24 horas."
    echo "➡️ Saltando descarga web de Celestrak para proteger cuota de IP."
else
    echo "📡 [CONTROL DE RED] Los TLEs locales expiraron o no existen."
    echo "📥 Ejecutando actualización segura vía celes_starlink.py..."

	#execute download script - routes
    PYTHONPATH=$PROJECT_ROOT $PYTHON_BIN $PROJECT_ROOT/Astro/src/apis/celes_starlink.py

    sleep 3

fi

echo "[SQlite data input] procesing orbital data - astro.sqlite..."

PYTHONPATH=$PROJECT_ROOT $PYTHON_BIN $PROJECT_ROOT/Astro/src/apis/celes_trak.py

echo "✅ [PIPELINE COMPLETED] SYNCRONIZED DB - Ready for data extraction - orbital calculations . . . "
echo "=========================================================================="
