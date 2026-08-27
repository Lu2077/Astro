import os
from skyfield.api import load
from skyfield.iokit import parse_tle_file

#from Astro.test.test_track import ruta_archivo


def charge_starlink_sats():
    ts = load.timescale()

    ruta_archivo = '/home/ros2/Desktop/proyecto-Astro/Astro/Astro/src/apis/starlink.tle'

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'rb') as f:
            sats = list(parse_tle_file(f,ts))
        return sats
    else:
        print(f"Error: no se encontro el archivo en {ruta_archivo}")
        return []

if __name__ == '__main__':
    lista_sat = charge_starlink_sats()
    print('Ejecución directa de prueba: Loaded', len(lista_sat), 'satellites')

"""
ts = load.timescale()

ruta = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(ruta,
                            '/home/ros2/Desktop/proyecto-Astro/Astro/Astro/src/apis/starlink.tle')

if os.path.exists(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        satellites = list(parse_tle_file(f,ts))
    print('Loaded',len(satellites), 'satellites')

    if satellites:
        print('Loaded', len(satellites), 'satellites')

    else:
        print(f"Error: no se encontró el archivo en {ruta_archivo}")
"""