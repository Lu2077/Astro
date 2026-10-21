# 🛰️ Astro — Space Situational Awareness (SSA) SDK


[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Astro CI - Test Suite](https://github.com/Lu2077/Astro/actions/workflows/tests.yml/badge.svg)](https://github.com/Lu2077/Astro/actions/workflows/tests.yml)

**Astro** is an open-source Python SDK for Space Situational Awareness (SSA), satellite tracking, and observation planning.

Its goal is to act as an integration and validation layer between public orbital data sources, local astronomical datasets, and observation workflows. Rather than replacing propagation engines such as SGP4 or Skyfield, Astro focuses on combining their outputs with observatory context, field-of-view geometry, and reproducible data pipelines.

---

## 📚 Documentation

The documentation is organized by responsibility to keep technical references focused and maintainable:

- 📖 [**SDK & Core API Manual**](Astro/src/track/README.md) — Public interfaces, geometric engine contracts, and FastAPI endpoint specifications.
- 📐 [**Scientific Research Notes**](https://github.com/Lu2077/Astro/blob/main/docs/mvp_research_notes.md) — Orbital modeling, astrodynamics fundamentals, and the mathematical background behind the project.
- 🗄️ [**Data Layer Guide**](Astro/db/README.md) — SQLite schema, migrations, and static seed data for `astro.sqlite3`.

---

## 🧭 Project scope

Astro is designed to help answer practical questions such as:

- Where will a satellite be at a given time?
- What is its relative motion from a specific ground station?
- Could a satellite transit through a telescope’s field of view?
- Can TLE, observatory, and local observation data be integrated reproducibly?

The project is particularly interested in the interaction between LEO satellite constellations and ground-based astronomical facilities.

---

## 🛠️ Architecture

Astro is intended as an orchestration and integration layer, not as a new orbital-propagation engine.

```text
[ Observatory APIs ]        [ TLE ingestion (e.g. CelesTrak) ]
        │                              │
        └──────────► [ Astro SDK ] ◄───┘
                     (Orchestration layer)
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
[ Geometric engine ]                      [ Data pipeline ]
 FOV / ray-casting workflows               Ingestion, validation, SQLite
```

### Current MVP capabilities

- **LEO object tracking:** relative radial velocity and Doppler calculations from topocentric observer coordinates.
- **TLE data ingestion:** consumption, parsing, and local storage of structured TLE datasets.
- **Geometric backtracking:** reverse-time simulation workflows to compare recorded telemetry against field-of-view or exclusion polygons.

> Some observatory integrations and advanced orbital-refinement features are part of the project roadmap and are not yet fully implemented.

---

## 🚀 Local development

### Prerequisites

- Python 3.10 or later
- A virtual environment

### 1. Clone and install in editable mode

```bash
git clone [https://github.com/Lu2077/Astro.git](https://github.com/Lu2077/Astro.git)
cd Astro

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

Installing in editable mode links the local source code to your Python environment, allowing changes to the SDK to be available immediately during development.

### 2. Run the test suite

```bash
pytest tests/
```

### 3. Run the demonstration API

```bash
python Astro/main.py
```

The local API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 🛣️ Roadmap

- [x] Initial SDK architecture and Python packaging configuration (`pyproject.toml`).
- [x] Geometric backtracking workflow for validation experiments.
- [x] Earth-centered inertial (ECI) coordinate-system support.
- [x] Concurrent polling for live synchronization with observatory schedules.
- [ ] Uncertainty refinement using covariance information from historical observations.
- [ ] Stable public API, documentation, and package release.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).