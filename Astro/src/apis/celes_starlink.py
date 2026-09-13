"""
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
"""

# Astro/src/apis/celes_trak.py
import os
import requests

def descargar_starlink_tle(ruta_guardado: str = None) -> bool:
    base = 'https://celestrak.org/NORAD/elements/gp.php'
    url = f"{base}?GROUP=starlink&FORMAT=tle"

    # Si no se pasa una ruta, se usa la ruta por defecto del script original
    if ruta_guardado is None:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_guardado = os.path.join(ruta_actual, 'starlink.tle')

    print("Conectando con Celestrak para descargar la constelación de Starlink")
    
    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200 and len(response.text) > 100:
            with open(ruta_guardado, 'w', encoding='utf-8') as f:
                f.write(response.text)

            lineas = response.text.count('\n')
            print(f"Descarga exitosa! Archivo guardado en {ruta_guardado}")
            print(f"Se descargaron aproximadamente {lineas // 3} satélites Starlink.")
            return True
        
        print(f"Error en la api Celestrak. codigo {response.status_code}")
        return False

    except requests.RequestException as e:
        print(f"Error de red o conexión al conectar con Celestrak: {e}")
        return False

if __name__ == '__main__':
    descargar_starlink_tle()