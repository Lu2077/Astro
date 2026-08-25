import os
import geocoder
from skyfield.api import load, wgs84

# 1. Configurar ubicación por IP (Caerá automáticamente en Santiago, CL)
print(" Detectando coordenadas del telescopio...")
g = geocoder.ip('me')
lat_obs, lon_obs = (g.latlng) if (g.ok and g.latlng) else (-33.4569, -70.6483)

ts = load.timescale()
ahora = ts.now()

# 2. Cargar los datos desde el archivo físico local 'starlink.tle'
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_tle = os.path.join(ruta_actual, 'starlink.tle')

if not os.path.exists(ruta_tle):
    print("❌ Error: No se encuentra 'starlink.tle'. Ejecuta primero test_Starlink.py")
    exit()

print(" Leyendo base de datos local de Starlink...")
satellites_dict = load.tle_file(ruta_tle)
starlinks = list(satellites_dict.values())
print(f" {len(starlinks)} satélites cargados en memoria.")


def find_interfering_satellites(satellites_list, horizon_limit_degrees=15):
    """Filtra y encuentra qué satélites están sobre el horizonte visible."""
    observatorio = wgs84.latlon(lat_obs, lon_obs)
    en_cielo = []

    print(f"🛰️ Escaneando el firmamento en tiempo real...")
    for sat in satellites_list:
        # Relación topocéntrica (Satélite visto desde el observatorio)
        diferencia = sat - observatorio
        topocentric = diferencia.at(ahora)
        alt, az, distance = topocentric.altaz()

        # Si el satélite está por encima del límite del horizonte del telescopio
        if alt.degrees >= horizon_limit_degrees:
            en_cielo.append({
                "name": sat.name,
                "id": sat.model.satnum,
                "alt": alt.degrees,
                "az": az.degrees,
                "dist": distance.km
            })

    # Ordenar por el que está más alto en el cenit (máximo peligro para la foto)
    en_cielo.sort(key=lambda x: x["alt"], reverse=True)
    return en_cielo


if __name__ == "__main__":
    # Filtramos satélites que estén a más de 15 grados del suelo
    contaminantes = find_interfering_satellites(starlinks, horizon_limit_degrees=15)

    print(f"\n [ALERTA OBSERVATORIO] ")
    print(f"Se detectaron {len(contaminantes)} satélites Starlink interfiriendo tu cielo AHORA:")
    print(f"{'SATÉLITE':<25} | {'NORAD ID':<8} | {'ELEVACIÓN':<10} | {'AZIMUT':<10}")
    print("-" * 65)

    for s in contaminantes[:15]:  # Mostramos el top 15 de los más altos
        print(f"{s['name']:<25} | {s['id']:<8} | {s['alt']:>8.2f}° | {s['az']:>8.2f}°")
