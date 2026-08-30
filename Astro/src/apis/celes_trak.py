import os
from skyfield.api import load, EarthSatellite
from Astro.db.repositories.satellites import SatelliteRepository


def procesar_archivo_tle(nombre_archivo):
    ts = load.timescale()
    repo = SatelliteRepository()

    # Encontramos la ruta absoluta del archivo de texto .tle en tu proyecto
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(base_dir, nombre_archivo)

    if not os.path.exists(ruta_completa):
        print(f"Error: No se encontró el archivo en {ruta_completa}")
        return

    print(f"Procesando e inyectando datos de: {nombre_archivo}...")
    with open(ruta_completa, "r") as f:
        lineas = f.readlines()

    contador = 0
    for i in range(0, len(lineas) - 2, 3):
        name = lineas[i].strip()
        line1 = lineas[i + 1].strip()
        line2 = lineas[i + 2].strip()

        if not (line1.startswith("1 ") and line2.startswith("2 ")):
            continue

        try:
            sat_temporal = EarthSatellite(line1, line2, name, ts)
            norad_id = sat_temporal.model.satnum
            epoch_str = sat_temporal.epoch.utc_strftime('%Y-%m-%d %H:%M:%S')

            # Guardamos los elementos orbitales TLE dentro de la base de datos unificada
            repo.save_tle(norad_id, name, epoch_str, line1, line2)
            contador += 1
        except ValueError:
            continue

    print(f"Éxito: Se guardaron {contador} registros desde {nombre_archivo}")


if __name__ == "__main__":
    # Inyectamos de manera secuencial tus dos archivos fuente de datos
    procesar_archivo_tle("starlink.tle")
    procesar_archivo_tle("stations.tle")

