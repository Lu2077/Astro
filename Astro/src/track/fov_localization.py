from datetime import datetime, timezone

from skyfield.api import load, wgs84

from .track import charge_starlink_sats


def calcular_posiciones_satelites(
    fecha: str,
    lat_deg: float,
    lon_deg: float,
    alt_m: float = 0.0,
    constelacion: str = "starlink",
) -> list[dict]:
    ts = load.timescale()
    t = ts.from_datetime(
        datetime.fromisoformat(fecha).replace(tzinfo=timezone.utc)
    )

    observador = wgs84.latlon(lat_deg, lon_deg, elevation_m=alt_m)
    satelites = charge_starlink_sats()

    resultados = []

    for sat in satelites:
        try:
            diferencia = sat - observador
            topocentrico = diferencia.at(t)

            altitud, azimut, distancia = topocentrico.altaz()

            if altitud.degrees <= 0:
                continue

            ra, dec, _ = topocentrico.radec()

            resultados.append({
                "name": sat.name,
                "ra_deg": float(ra.hours * 15),
                "dec_deg": float(dec.degrees),
                "alt_deg": float(altitud.degrees),
                "az_deg": float(azimut.degrees),
                "distancia_km": float(distancia.km),
            })

        except Exception as exc:
            print(f"[Astro Localization Error] {sat.name}: {exc}")
            continue

    return resultados

if __name__ == "__main__":
    satelites = calcular_posiciones_satelites(
        fecha="2026-10-15T00:00:00",
        lat_deg=-29.2584,      # La Silla
        lon_deg=-70.7381,
        alt_m=2400,
        constelacion="starlink",
    )

    print(f"Satélites calculados: {len(satelites)}")

    for sat in satelites[:5]:
        print(sat)