import os
from skyfield.api import load
from skyfield.iokit import parse_tle_file

ts = load.timescale()

ruta_test = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(ruta_test, 'stations.tle')

if os.path.exists(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        satellites = list(parse_tle_file(f,ts))
    print('Loaded',len(satellites), 'satellites')

    if satellites:
        print('Loaded', len(satellites), 'satellites')

    else:
        print(f"Error: no se encontró el archivo en {ruta_archivo}")