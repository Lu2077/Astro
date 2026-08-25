import os
import geocoder
from skyfield.api import load, wgs84
from test_track import satellites

print("Detectando tu ubicación actual...")

g = geocoder.ip('me')

if g.ok:
    lat_observer, lon_observer = g.latlng
    print("\n ¡Ubicación detectada!")
    print(f"Ciudad/Región: {g.city}, {g.state}, {g.country}")
    print(f"Coordenadas: {lat_observer:.4f}, {lon_observer:.4f}")

else:
    print("No se pudo detectar localización. Usando coordenadas de respaldo.")
    lat_observer, lon_observer = -33.4489, -70.6693

ts = load.timescale()
ahora = ts.now()

def closest_satellites(satellites_list, max_distance_km=500):

    satelites_cerca = []

    position_observer = wgs84.latlon(lat_observer, lon_observer)

    observer_at_time = position_observer.at(ahora)

    print(f"\nEscaneando... {len(satellites_list)} satélites en un radio de {max_distance_km} KM")

    for sat in satellites_list:

        geocentric = sat.at(ahora)
        subpoint = wgs84.subpoint(geocentric)

        position_sat_earth = wgs84.latlon(subpoint.latitude.degrees, subpoint.longitude.degrees)

        sat_at_time = position_sat_earth.at(ahora)

        diferencia_vectores = sat_at_time - observer_at_time

        distancia_km = diferencia_vectores.distance().km

        if distancia_km <= max_distance_km:
            satelites_cerca.append({
                "sat": sat,
                "nombre": sat.name,
                "distancia": distancia_km,
                'lat': subpoint.latitude.degrees,
                'lon': subpoint.longitude.degrees
            })

    satelites_cerca.sort(key=lambda x: x["distancia"])
    return satelites_cerca

if __name__ == "__main__":
    if len(satellites) == 0:
        print("Error: no hay satélites cargados para analizar.")
    else:
        resultados = closest_satellites(satellites, max_distance_km=500)

        print(f"\n Resultados: se encontraron"
              f" {len(resultados)} satélites cerca de tí ahora mismo")
        print(f"{'SATELITE':<30} | {'DISTANCIA AL PUNTO':>18} | {'COORDENADAS':<20}")
        print("-" * 75)

        for s in resultados[:15]:
            print(f"{s['nombre']:<30} | {s['distancia']:>14.2f} km | {s['lat']:>7.3f}° , {s['lon']:>7.3f}° ")

