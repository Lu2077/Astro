DROP TABLE IF EXISTS observation_errors;
DROP TABLE IF EXISTS satellite_observations;
DROP TABLE IF EXISTS satellite_tles;

CREATE TABLE satellite_tles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    norad_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    epoch TEXT NOT NULL,
    line1 TEXT NOT NULL,
    line2 TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(norad_id, epoch)
);

CREATE TABLE satellite_observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    norad_id INTEGER NOT NULL,
    observed_at TEXT NOT NULL,
    azimuth_deg REAL,
    elevation_deg REAL,
    distance_km REAL,
    station_id INTEGER
);

CREATE TABLE observation_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    observation_id INTEGER NOT NULL,
    tle_id INTEGER NOT NULL,
    error_azimuth REAL,
    error_elevation REAL,
    error_distance_km REAL,
    FOREIGN KEY(observation_id) REFERENCES satellite_observations(id),
    FOREIGN KEY(tle_id) REFERENCES satellite_tles(id)
);

-- SUGERENCIA -- LETS SHARP THIS!

CREATE TABLE IF NOT EXISTS ssa_calculated_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tle_id INTEGER,               -- Cambiado a tle_id para enganche correcto con la PK de satellite_tles
    norad_id INTEGER NOT NULL,
    sat_name TEXT,
    mjd_epoch REAL NOT NULL,      -- Sincronizado con ALMA/ESO (e.g., 61297.051977)
    ra_deg REAL NOT NULL,
    dec_deg REAL NOT NULL,
    alt_deg REAL,
    az_deg REAL,
    v_radial_kms REAL,           -- Tu script de efectos Doppler / Velocidad radial
    orbital_altitude_km REAL,
    distance_km REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(tle_id) REFERENCES satellite_tles(id)
);

-- SUGERENCIA -- BEST TRY -- LETS SHARP THIS PLEASE

CREATE TABLE IF NOT EXISTS backtracking_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- SATÉLITE UTILIZADO
    norad_id INTEGER NOT NULL,
    satellite_name TEXT,
    tle_epoch TEXT NOT NULL,      -- Época del TLE usado para calcular
    tle_age_days REAL,            -- Offset en días (para auditar si causó CRITICAL_ERROR)

    -- EVENTO DEL OBSERVATORIO / INSTRUMENTO
    observation_id TEXT,          -- ID o hash del evento científico en ALMA/MAST/ESO
    observatory TEXT NOT NULL,    -- E.g., 'ALMA', 'VLT'
    instrument_name TEXT,         -- E.g., 'GIRAFFE'
    t_min_mjd REAL NOT NULL,      -- Ventana de tiempo inicio
    t_max_mjd REAL NOT NULL,      -- Ventana de tiempo fin

    -- GEOMETRÍA DEL FOV (Mapeo dual: punto/radio o polígono)
    s_ra_deg REAL,                -- Centro RA (si aplica)
    s_dec_deg REAL,               -- Centro DEC (si aplica)
    s_fov_deg REAL,               -- Radio FOV (para la ESO)
    s_region TEXT,                -- ¡NUEVO! Almacena "Polygon ICRS ..." de ALMA tal cual llega

    -- RESULTADO DEL CONTRASTE GEOMÉTRICO
    closest_approach_mjd REAL,    -- MJD del máximo acercamiento o cruce
    min_separation_deg REAL,      -- Distancia angular mínima al centro o borde
    status TEXT NOT NULL,         -- 'DENTRO', 'CERCANO' (Sidelobes), 'DESCARTADO'

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (norad_id, observation_id, tle_epoch)
);


--INDEX - DO NOT TOUCH
CREATE INDEX idx_mjd ON ssa_calculated_states(mjd_epoch);
CREATE INDEX idx_spatial ON ssa_calculated_states(ra_deg, dec_deg);

