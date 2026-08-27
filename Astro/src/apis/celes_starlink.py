import os
import requests

base = 'https://celestrak.org/NORAD/elements/gp.php'
url = f"{base}?GROUP=starlink&FORMAT=tle"

ruta_actual = os.path.dirname(os.path.abspath(__file__))

ruta_guardado = os.path.join(ruta_actual, 'starlink.tle')

print("Conectando con Celestrak para descargar la constelación de Starlink")
response = requests.get(url, timeout=15)

if response.status_code == 200 and len(response.text) > 100:
    with open(ruta_guardado, 'w', encoding='utf-8') as f:
        f.write(response.text)

    lineas = response.text.count('\n')
    print(f"Descarga exitosa! Archivo guardado en {ruta_guardado}")
    print(f" Se descargaron aproximadamente {lineas // 3} satélites Starlink.")
else:
    print(f"Error en la api Celestrak. codio {response.status_code}")