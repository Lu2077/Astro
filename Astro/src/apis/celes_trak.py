from skyfield.api import load
import requests
import os

ruta = os.path.dirname(os.path.abspath(__file__))
ruta_guardado = os.path.join(ruta, 'stations.tle')

max_days = 7.0         # download again once 7 days old
name = 'stations.tle'  # custom filename, not 'gp.php'

base = 'https://celestrak.org/NORAD/elements/gp.php'
url = base + '?GROUP=stations&FORMAT=tle'
response = requests.get(url)

print("descargando TLEs desde Celestrak...")

if response.status_code == 200:

    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Archivo descargado con éxito en: {ruta_guardado}")
else:
    print(f"Error al descargar: Código de estado {response.status_code}")

if not load.exists(name) or load.days_old(name) >= max_days:
    load.download(url, filename=name)