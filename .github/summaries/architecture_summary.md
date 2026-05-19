# Architecture Summary

- Separation of Concerns: organize code by technical responsibility (models, ingestion, analytics, API), not by feature.
- Contract-First: define interfaces/Protocols in `src/interfaces/` before implementation so teams can work against contracts.
- Inward dependency flow: core/interfaces → services → IO adapters; outer layers must not be imported by inner layers.
- Phases: Ingestion (async scrapers), Processing & Storage (workers + Postgres/TimescaleDB), Quant Engine & API (FastAPI).
- Client boundaries: Electron main handles caching, filesystem & SavedVariables export; renderer handles UI and IPC; Lua addon consumes precomputed SavedVariables only.
- Coding rules: ban `utils.py`/`helpers.py`; use explicit dependency injection and write fast, offline unit tests.

Full doc: .github/full_stack_structure.md
