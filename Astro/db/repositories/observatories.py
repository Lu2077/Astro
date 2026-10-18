from skyfield.api import wgs84

def observatories_repo(observatories):

    observatories = {
        "alma": {
            "nombre": "ALMA",
            "lat_deg": -23.0292,
            "lon_deg": -67.7549,
            "alt_m": 5058,
            "tap_provider": "alma",
            "activo": True,
        },
        "la_silla": {
            "nombre": "La Silla",
            "lat_deg": -29.2584,
            "lon_deg": -70.7381,
            "alt_m": 2400,
            "tap_provider": "eso",
            "activo": True,
        },
        "paranal": {
            "nombre": "Paranal",
            "lat_deg": -24.6275,
            "lon_deg": -70.4044,
            "alt_m": 2635,
            "tap_provider": "eso",
            "activo": True,
        },
        "apex": {
            "nombre": "APEX",
            "lat_deg": -23.0058,
            "lon_deg": -67.7549,
            "alt_m": 5100,
            "tap_provider": "eso",
            "activo": True,
        },
    }