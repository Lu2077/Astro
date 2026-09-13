import os
from unittest.mock import patch, MagicMock
from Astro.src.apis.celes_starlink import descargar_starlink_tle

@patch('Astro.src.apis.requests.get')
def test_descargar_starlink_tle_exito(mock_get, tmp_path):
    # 1. Simulamos una respuesta exitosa de la API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Linea 1\nLinea 2\nLinea 3\n" * 10  # Simula un TLE válido
    mock_get.return_value = mock_response

    # 2. Usamos una ruta temporal fija gracias a pytest (tmp_path)
    ruta_temporal = os.path.join(tmp_path, "test_starlink.tle")

    # 3. Ejecutamos la función
    resultado = descargar_starlink_tle(ruta_guardado=ruta_temporal)

    # 4. Asertamos que dio True y que el archivo se creó con contenido
    assert resultado is True
    assert os.path.exists(ruta_temporal)
    with open(ruta_temporal, 'r') as f:
        assert "Linea 1" in f.read()

@patch('Astro.src.apis.requests.get')
def test_descargar_starlink_tle_error_api(mock_get, tmp_path):
    # Simulamos un error 500 del servidor de Celestrak
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    ruta_temporal = os.path.join(tmp_path, "test_starlink.tle")
    resultado = descargar_starlink_tle(ruta_guardado=ruta_temporal)

    assert resultado is False
