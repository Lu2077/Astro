# Astro/test/test_track.py
import pytest
# Importamos directamente la función desde tu script matemático original
from src.track.localization import closest_satellites

def test_closest_satellites_empty_list():
    """
    Verifica que la función matemática maneje correctamente listas vacías
    respetando que toma un máximo de 2 argumentos posicionales.
    """
    # Pasamos una lista vacía y el radio en KM (los 2 parámetros que tu código espera)
    resultados = closest_satellites([], max_distance_km=500.0)
    assert isinstance(resultados, list)
    assert len(resultados) == 0

def test_closest_satellites_structure():
    """
    Verifica que la función retorne una lista limpia si no se le inyectan satélites.
    """
    # Ejecutamos la función usando el radio por defecto (1 argumento posicional)
    resultados = closest_satellites([])
    assert resultados == []

