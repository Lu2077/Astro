#TODO - THIS IS FOR VALIDATIION PURPOSES$%!

def extract_poligon_vertices(polygon_str: str) -> list:
    """
    Extrae los vértices RA/Dec de un string STC-S:
    'Polygon ICRS RA1 DEC1 RA2 DEC2 ...'

    Retorna:
        [(ra1, dec1), (ra2, dec2), ...]

    Lanza ValueError si no hay al menos 3 vértices.
    """
    if not polygon_str:
        raise ValueError("s_region vacío")

    partes = polygon_str.strip().split()

    numeros = []

    for parte in partes:
        try:
            numeros.append(float(parte))
        except ValueError:
            # Ignora 'Polygon', 'ICRS', etc.
            continue

    if len(numeros) < 6 or len(numeros) % 2 != 0:
        raise ValueError(
            f"s_region no contiene un polígono válido: {polygon_str!r}"
        )

    vertices = []

    for i in range(0, len(numeros), 2):
        vertices.append((numeros[i], numeros[i + 1]))

    return vertices

def is_point_on_polygon(ra: float, dec: float, vertices: list) -> bool:
    """
    Determina si un punto RA/Dec está dentro de un polígono.
    Usa ray casting en coordenadas planas; suficiente para FOVs pequeños.
    """
    dentro = False
    n = len(vertices)

    j = n - 1

    for i in range(n):
        ra_i, dec_i = vertices[i]
        ra_j, dec_j = vertices[j]

        if (
            (dec_i > dec) != (dec_j > dec)
            and ra < (ra_j - ra_i) * (dec - dec_i) / (dec_j - dec_i) + ra_i
        ):
            dentro = not dentro

        j = i

    return dentro

#TODO - TESTING PURPOSES ONLY

#---------------------------WE LEFT IT HERE!!!


def obtain_bounding_box(vertices: list) -> dict:
        """
        Calcula los límites máximos y mínimos de una lista de vértices [(ra, dec), ...].
        Actúa como el simplificador primario para la Raspberry Pi 5.
        """
        if not vertices:
            return {}

        # Extraemos todas las RAs (primer elemento de cada tupla)
        ras = [v[0] for v in vertices]
        # Extraemos todas las Decs (segundo elemento de cada tupla)
        decs = [v[1] for v in vertices]

        return {
                "min_ra": min(ras),
                "max_ra": max(ras),
                "min_dec": min(decs),
                "max_dec": max(decs)
            }

if __name__ == "__main__":
    s_region = (
        "Polygon ICRS "
        "261.172568 -38.923861 "
        "261.172796 -38.926670 "
        "261.171678 -38.929347 "
        "261.169372 -38.931515 "
        "261.167870 -38.932310 "
        "261.165620 -38.933003 "
        "261.162009 -38.933179 "
        "261.160236 -38.932871 "
        "261.158046 -38.932070 "
        "261.155409 -38.930143 "
        "261.153869 -38.927596 "
        "261.153642 -38.924787 "
        "261.154760 -38.922111 "
        "261.157066 -38.919943 "
        "261.158569 -38.919148 "
        "261.160818 -38.918455 "
        "261.164428 -38.918279 "
        "261.166772 -38.918747 "
        "261.168391 -38.919388 "
        "261.171028 -38.921315"
    )

    vertices = extract_poligon_vertices(s_region)

    print("Número de vértices:", len(vertices))
    print("Primero:", vertices[0])
    print("Último:", vertices[-1])

    punto_prueba = (261.163, -38.925)

    print("¿Dentro?:", is_point_on_polygon(
        punto_prueba[0],
        punto_prueba[1],
        vertices,
    ))

    #validation test - -

    bbox = obtain_bounding_box(vertices)
    print("Caja Delimitadora (Bounding Box):")
    print(f"  RA  rango: {bbox['min_ra']} a {bbox['max_ra']}")
    print(f"  DEC rango: {bbox['min_dec']} a {bbox['max_dec']}")

    punto_prueba = (261.163, -38.925)

    #EXAMPLE Out of the Bounding Box
    #punto_fuera = (262.0, -38.0)

    # El Filtro de Dos Capas que usará tu orquestador back_tracking.py:
    esta_en_caja = (bbox["min_ra"] <= punto_prueba[0] <= bbox["max_ra"] and
                    bbox["min_dec"] <= punto_prueba[1] <= bbox["max_dec"])

    print("¿Pasó el filtro rápido del Bounding Box?:", esta_en_caja)

    if esta_en_caja:
        print("¿Dentro del polígono final (Ray-Casting)?:", is_point_on_polygon(
            punto_prueba[0], punto_prueba[1], vertices
        ))

#---------------------------WE LEFT IT HERE!!!