---
description: "Use when writing or refactoring backend Python ingestion, processing, quant, storage, and API modules. Enforces contract-first boundaries and inward dependency flow."
name: "Backend Python Architecture Rules"
applyTo:
  - "backend/**/*.py"
  - "**/*.py"
---
# Backend Python Rules

Apply these rules when touching Python code in this repository.

## Layering
- Separate modules by technical responsibility: interfaces, models/core math, services, and IO adapters.
- Keep dependencies inward: core/interfaces -> services -> IO adapters.
- Do not let service or analytics code import infrastructure adapters directly.

## Contract-First
- Define Protocol or abstract contract before implementation logic for new boundaries.
- Type contracts should be explicit and focused on behavior, not concrete adapters.

## API and IO
- Build Blizzard API requests with explicit base URL, namespace, locale, and auth token.
- Keep ingestion clients focused on retrieval only.

## Code Hygiene
- Do not create files named `utils.py` or `helpers.py`.
- Prefer dependency injection for HTTP clients, database gateways, and filesystem adapters.
- Favor small testable functions and modules.
