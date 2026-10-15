def normalizar_evento_obscore(
    row: dict,
    observatorio: str,
) -> dict:
    return {
        "observatorio": observatorio,
        "objeto": row.get("target_name"),
        "ra": float(row["s_ra"]),
        "dec": float(row["s_dec"]),
        "fov_deg": float(row["s_fov"]),
        "t_min": row.get("t_min"),
        "t_max": row.get("t_max"),
        "instrument_name": row.get("instrument_name"),
        "s_region": row.get("s_region"),
        "dp_id": row.get("dp_id"),
    }



