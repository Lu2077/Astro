import time

from astroplan import observer
from skyfield.api import load, wgs84
from skyfield.elementslib import longitude_of_ascending_node

from track import charge_starlink_sats
import geocoder

satellites = charge_starlink_sats()

ts = load.timescale()

g = geocoder.ip('me')

lat_observer = g.lat
lon_observer = g.lng

print(f"lugar observer: {lat_observer}, {lon_observer}")

observer = wgs84.latlon(lat_observer, lon_observer)

print(f"configuracion observación exitosa: {observer}")

if g.lat and g.lng:
    lat_observer = g.lat
    lon_observer = g.lng
else:
    print("Warning: IP-not detected coordinates")
    lat_observer = input("ingrese la latitud: ...")
    lon_observer = input("ingrese la longitud: ...")

observer = wgs84.latlon(lat_observer, lon_observer)

def muestra(max_distance_km=200):
    ahora = ts.now()
    observer_at_time = observer.at(ahora)
    muestra = {}

    for sat in satellites:
        geocentric = sat.at(ahora)
        subpoint = wgs84.subpoint(geocentric)

        punto_subpunto = wgs84.latlon(
            subpoint.latitude.degrees,
            subpoint.longitude.degrees,
        ).at(ahora)

        distancia_subpunto_km = (
            punto_subpunto - observer_at_time
        ).distance().km

        if distancia_subpunto_km > max_distance_km:
            continue

        rango_real_km = (
            geocentric - observer_at_time
        ).distance().km

        topocentric = (sat - observer).at(ahora)
        alt, az, _ = topocentric.altaz()

        norad_id = sat.model.satnum

        muestra[norad_id] = {
            "nombre": sat.name,
            "hora": ahora.utc_datetime(),
            "rango": rango_real_km,
            "distancia_subpunto": distancia_subpunto_km,
            "elevation_deg": alt.degrees,
            "azimuth_deg": az.degrees,
        }

    return muestra

primera = muestra(max_distance_km=200)
print(f"primera muestra: {len(primera)} satélites")
time.sleep(10)

segunda = muestra(max_distance_km=200)
print(f"Segunda muestra: {len(segunda)} satélites\n")

for norad_id, actual in segunda.items():
    anterior = primera.get(norad_id)

    if anterior is None:
        continue

    segundos_transcurridos = (
        actual["hora"] - anterior["hora"]
    ).total_seconds()

    vel_rad_km_s = (
        actual["rango"] - anterior["rango"]
    ) / segundos_transcurridos

    state = (
        "acercandose"
        if vel_rad_km_s < 0
        else "alejandose"
    )

    print(
        f"{actual['nombre']:<30} | "
        f"rango: {actual['rango']:7.2f} km | "
        f"{state}: {abs(vel_rad_km_s):.3f} km/s | "
        f"elevación: {actual['elevation_deg']:.2f} degree | "
    )
