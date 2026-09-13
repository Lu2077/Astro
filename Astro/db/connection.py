import sqlite3

def get_connection():
    conn = sqlite3.connect("db/astro.sqlite3")
    # Activa el modo WAL para tolerar cortes de luz y mejorar lecturas/escrituras concurrentes
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn