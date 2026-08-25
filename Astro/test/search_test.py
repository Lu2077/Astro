from test_track import satellites


def search_satellites(satellites_list):
    search = input("\nIntroduce el nombre del satélite a buscar (ej. ISS): ")
    search_clean = search.strip().lower()

    if not search_clean:
        return None

    for sat in satellites_list:
        if search_clean in sat.name.lower():
            print(f"¡Satélite encontrado!: {sat.name}")
            return sat

    print(f"Error: no se encontró ningún satélite con el nombre '{search}'")
    return None

if __name__ == "__main__":
    if len(satellites) == 0:
        print("Adertencia: La lista de satélites está vacía. "
              "Verifíca que stations.tle existe")
    else:
        print(f"Buscando en una base de datos de {len(satellites)} satélites")
        satelite_encontrado = search_satellites(satellites)