"""
using tap protocol to communicate
ALMA/ESO Servers
"""

import requests
import logging
from io import BytesIO
from astropy.table import Table

logger = logging.getLogger("Astro.tap_client")

class TAPClient:
    """
    orchestrating TAP requests (table access protocol)
    avoiding failures / otherwise / format parsing could crash the whole flow
    """

    def __init__(self, base_url: str, timeout: int = 15):
        self.base_url = base_url
        slef.timeout = timeout

    # Mock mode
    def fetch_data(self, query_adql: str) -> list:
        if self.mock_mode:
            print(f"[MOCK] Generando datos simulados estables para el Servidor TAP...")
            return [
                {
                    "target_name": "Orion Nebula",
                    "s_ra": 83.8221,
                    "s_dec": -5.3911,
                    "s_fov": 0.5,
                    "t_min": 61324.0,
                    "t_max": 61324.1,
                    "instrument_name": "ALMA_Band6"
                },
                {
                    "target_name": "Sagittarius A*",
                    "s_ra": 266.4168,
                    "s_dec": -29.0078,
                    "s_fov": 0.2,
                    "t_min": 61324.05,
                    "t_max": 61324.15,
                    "instrument_name": "ALMA_Band7"
                }
            ]

    #Production mode
    def send_query(self, query_adql: str) -> list:
        """
        send requests and handles format errors

        """
        payload = {
            "REQUEST": "doQuery",
            "LANG": "ADQL",
            "FORMAT": "votable",
            "QUERY": query_adql
        }
        try:
            response = requests.post(self.base_url, data=payload, timeout=self.timeout)
            response.raise_for_status()
            tabla_astropy = Table.read(BytesIO(response.content), format="votable")

            return [{str(col): fila[col] for col in tabla_astropy.colnames} for fila in tabla_astropy]
        except Exception as e:
            print(f"[TAP Client Error] Fallo crítico real en {self.base_url}: {e}")
            return []