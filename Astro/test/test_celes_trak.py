# Astro/test/test_celes_trak.py
import os
from unittest.mock import patch, mock_open
from src.apis.celes_trak import descargar_starlink_tle


@patch('requests.get')
def test_descargar_starlink_tle_exitoso(mock_get):
    """Prueba que si Celestrak responde 200, la función retorna True y guarda."""
    # 1. Simulamos que Celestrak responde con éxito y nos da un TLE falso de Starlink
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "STARLINK-36048\n1 67547U...\n2 67547..."

    # 2. Ejecutamos la función apuntando a un archivo temporal simulado
    with patch("builtins.open", mock_open()) as mocked_file:
        resultado = descargar_starlink_tle("fake_path/starlink.tle")

        # 3. Verificaciones de Pytest (Asserts)
        assert resultado is True
        mocked_file.assert_called_once_with("fake_path/starlink.tle", 'w', encoding='utf-8')
