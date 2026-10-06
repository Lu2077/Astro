# Astro/test/test_track.py
import pytest
from src.track.localization import closest_satellites

def test_closest_satellites_empty_list():
    """Verifica que la función matemática maneje correctamente listas vacías."""
    resultados = closest_satellites([], lat_observer=-33.4569, lon_observer=-70.6483, max_distance_km=500)
    assert isinstance(resultados, list)
    assert len(resultados) == 0

def test_closest_satellites_structure():
    """Verifica que si la función no encuentra satélites, retorne una lista limpia."""
    # Test rápido simulando comportamiento aislado sin inicializar Skyfield masivo
    assert closest_satellites([], 0, 0) == []
