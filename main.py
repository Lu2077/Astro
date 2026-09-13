# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

"""
# Importas la lógica pura de tu backend (gracias a la estructura de tu proyecto)
from src.track.localization import obtener_coordenadas  # Ejemplo ficticio
from src.apis.celes_trak import escanear_satelites  # Ejemplo ficticio
"""

app = FastAPI(title="Astro - Sat Tracking Interface")

# Configuración de Frontend
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/")
async def dashboard(request: Request):
    # 1. Llamas a las funciones de tu backend de forma limpia
    # datos_satelites = escanear_satelites()

    # 2. Le inyectas los datos de tu backend a la plantilla de Bootstrap
    return templates.TemplateResponse("index.html", {
        "request": request,
        "satelites": []  # Aquí pasas tu lista de diccionarios/JSON
    })
