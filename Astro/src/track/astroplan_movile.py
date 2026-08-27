from astropy.time import Time
from astropy.coordinates import EarthLocation, get_body

t = Time("2026-08-26 23:48:00")
observatorio = EarthLocation.from_geodetic(
    lon=-70.403,
    lat=-24.625,
    height=2635
)

posicion_marte = get_body("mars", t, location=observatorio)

print(posicion_marte)