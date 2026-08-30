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