# 🛰️ Astro - Sat Tracking for Astronomers

![Antenas ALMA](docs/Antenas-ALMA-105.jpg)

**Astro** is a project designed for astronomers that enables **real-time tracking and orbit prediction of artificial satellites**. Its primary objective is to assist in planning nighttime observations, preventing satellite passes from ruining astrophotography captures or scientific data.

---

##  Current state of the project

*   **Currently, Astro is in its initial functional version and is under active development.**

Prior to the implementation of machine learning models for orbit prediction, the modules are being developed separately.

The core modules allow the following tasks to be performed independently:

*   **Object Tracking on Low Earth Orbit (LEO):** 
Calculation of the relative radial velocity from a coordinated observation point to a captured satellite belonging to a satellite constellation. 
*   **Data ingestion and processing:** Download of TLE data—the global standard for packaging and sharing orbital data for any object in space. 
*   **Events ingestion:** Tracking of fixed and mobile events using astronomical coordinates and Astroquery. 
*   **Satellite radio localization:** determines the presence and number of satellites in a constellation based on the observer's radius 
*   **DataBases:** implementing Bata Bases

From chapter 4 - 4.2 - The role of the measurement model in introducing nonlinearity to the process was described. 
In the general orbit determination problem, both the dynamics and the measurements involve significant nonlinear relationships. For the general case, the governing relations involve the nonlinear expression.
$$
\dot{\mathbf{X}} = F(\mathbf{X}, t), \quad \mathbf{X}(t_k) \equiv \mathbf{X}_k \tag{4.2.1}
$$
$$
\mathbf{Y}_i = G(\mathbf{X}_i, t_i) + {\epsilon}_i; \quad i = 1, \dots, \ell \tag{4.2.2}
$$
where $\mathbf{X}_k$ is the unknown $n$-dimensional state vector at the time $t_k$, and
$\mathbf{Y}_i$ for $i = 1, \dots, \ell$, is a $p$-dimensional set of observations that are to be used to obtain a best estimate of the unknown value of $\mathbf{X}_k$ (i.e., $\hat{\mathbf{X}}_k$). 
In general, $p < n$ and $m = p \times \ell \gg n$. The formulation represented by Eqs. (4.2.1) and (4.2.2) is characterized by: (1) the inability to observe the state directly, (2) nonlinear relations between the observations and the state,
(3) fewer observations at any time epoch than there are state vector components ($p < n$), and (4) errors in the observations represented by ${\epsilon}_i$.
Then: our Data Base will provide $\mathbf{a})$ epochs or sets of observation, and
                                 $\mathbf{b})$ will provide observation errors ${\epsilon}_i$ to correct and get the trajectories of our captured satellites.


---

*   **Future features and Roadmap:**
*   **Automation:** Set the setup to bring the modules  
*   **Tests:** Improve test suite logic trough pytest fixture
*   **Trajectory calculation:** Reliably estimate orbital trajectories | refinement of orbital trajectory errors
*   **OD:** Improve the localization of captured objects using Earth-Centered Inertial (ECI) coordinates.
*   **OP:** Predict the object's location using Earth-Centered, Earth-Fixed (ECEF) coordinates (ITRF/WGS84)


---

## Installation and Requirements

This project requires **Python 3.8 or higher**. Follow these steps to set it up on your computer.

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/Lu2077/Astro
    cd Astro
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # En Linux/macOS
    # o usa: env\Scripts\activate  # En Windows
    ```

3.  **Install the necessary dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

##  Use cases and terminal output

**Examples of various modules in operation are shown below:**

<details>
<summary><b> Example 1: Space Station Scanning (ISS)</b></summary>

```text
Loaded 21 satellites
Primer satélite en la lista:  ISS (ZARYA)
Detectando tu ubicación actual...

 ¡Ubicación detectada!
Ciudad/Región: Santiago, Santiago Metropolitan, CL
Coordenadas: -33.4569, -70.6483

Escaneando... 21 satélites en un radio de 500 KM

 Resultados: se encontraron 0 satélites cerca de tí ahora mismo
SATELITE                       | DISTANCIA AL PUNTO | COORDENADAS         
---------------------------------------------------------------------------

Process finished with exit code 0
```
</details>

<details>
<summary><b> Example 2: Captured satellite constellation, including ID, geoid-projected and linear distances, orbital altitude, and projected coordinates</b></summary>

```text
Coordenadas: -33.4569, -70.6483

Escaneando... 10734 satélites en un radio de 500 KM

 Resultados: se encontraron 21 satélites cerca de tí ahora mismo
SATELITE             | ORBITAL ALTITUDE | ACTUAL DISTANCE | GROUND DISTANCE   | COORDENADAS         
-------------------------------------------------------------------------------------------------
STARLINK-31415       | 491.48 km        | 495.49 km       | 60.62 km          | -32.937° , -70.448° 
STARLINK-3306        | 343.57 km        | 356.75 km       | 93.58 km          | -33.707° , -69.686° 
STARLINK-35014       | 474.12 km        | 489.32 km       | 116.74 km         | -34.279° , -71.436° 
STARLINK-35714       | 472.13 km        | 500.04 km       | 158.91 km         | -32.027° , -70.756° 
STARLINK-11343 [DTC] | 368.30 km        | 410.79 km       | 176.90 km         | -32.024° , -71.478° 
STARLINK-32092       | 492.38 km        | 531.47 km       | 192.76 km         | -34.995° , -71.621° 
STARLINK-1191        | 440.04 km        | 496.07 km       | 221.51 km         | -34.321° , -72.807° 
STARLINK-33620       | 492.42 km        | 552.78 km       | 242.01 km         | -34.735° , -68.522° 
STARLINK-1357        | 346.38 km        | 429.78 km       | 247.79 km         | -34.113° , -73.206° 
STARLINK-37451       | 474.70 km        | 582.28 km       | 325.30 km         | -35.795° , -68.507° 
STARLINK-35999       | 473.87 km        | 593.14 km       | 344.20 km         | -33.569° , -66.945° 
STARLINK-35934       | 477.82 km        | 598.97 km       | 348.35 km         | -31.082° , -68.228° 
STARLINK-31802       | 492.44 km        | 620.16 km       | 363.20 km         | -35.510° , -73.729° 
STARLINK-33923       | 490.91 km        | 621.25 km       | 366.83 km         | -30.342° , -69.341° 
STARLINK-35712       | 472.13 km        | 609.01 km       | 371.16 km         | -30.149° , -70.046° 

```
</details>


<details>

<summary><b> Example 3: Relative Radial Velocity</b></summary>

```text
lugar observer: -33.4569, -70.6483
configuracion observación exitosa: WGS84 latitude -33.4569 N longitude -70.6483 E elevation 0.0 m
primera muestra: 3 satélites
Segunda muestra: 2 satélites

STARLINK-36407                 | rango:  485.27 km | alejandose: 0.595 km/s | elevación: 80.20 degree | 
STARLINK-36614                 | rango:  493.25 km | acercandose: 0.297 km/s | elevación: 84.86 degree | 
```
</details>

---

##  Project Structure

<details>
<summary><b> Tree | directories, scripts & archives </b></summary>

```text
ros2@lucas-H410M-H:~/Desktop/proyecto-Astro/Astro$ tree -I 'env'
.
├── Astro
│   ├── db
│   │   ├── connection.py
│   │   ├── init_db.py
│   │   ├── migrations
│   │   │   └── README.md
│   │   ├── models.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   ├── observatories.py
│   │   │   ├── satellites.py
│   │   │   └── stations.py
│   │   ├── schema.sql
│   │   └── seeds
│   │       ├── __init__.py
│   │       └── seed.sql
│   ├── deploy
│   ├── Dockerfile
│   ├── info
│   ├── __init__.py
│   ├── requirements.txt
│   ├── src
│   │   ├── apis
│   │   │   ├── apis.yaml
│   │   │   ├── astroplan.py
│   │   │   ├── astroquery_api.py
│   │   │   ├── celes_starlink.py
│   │   │   ├── celes_trak.py
│   │   │   ├── starlink.tle
│   │   │   └── stations.tle
│   │   ├── __init__.py
│   │   └── track
│   │       ├── astroplan_fixed.py
│   │       ├── astroplan_movile.py
│   │       ├── astro_validate.py
│   │       ├── events.py
│   │       ├── FOV.py
│   │       ├── __init__.py
│   │       ├── localization.py
│   │       ├── track.py
│   │       ├── trajectories.py
│   │       ├── vel_sat.py
│   │       └── warns.py
│   └── test
│       ├── __init__.py
│       ├── localization_test.py
│       ├── pulses_test.py
│       ├── __pycache__
│       │   └── test_track.cpython-310.pyc
│       ├── search_test.py
│       ├── setup.py
│       ├── starlink.tle
│       ├── stations.tle
│       ├── test_celes_trak.py
│       ├── test_track.py
│       └── visibility_test.py
├── Astro.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── data
│   └── astro.sqlite3
├── docs
│   └── Antenas-ALMA-105.jpg
├── __init__.py
├── pre-commit-config.yaml
├── README.md
├── requirements.txt
└── setup.py

15 directories, 55 files

```
</details>

---

##  Contributions

Contributions are welcome | Lets share ideas. Use the links on my profile to contact with me.


---

##  Licence

This project is licensed under the **MIT** License.
