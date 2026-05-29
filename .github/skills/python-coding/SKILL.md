---
name: python-coding
description: Use when the task is Python-only, including scripts, modules, refactors, tests, type hints, packaging, and CLI entry points.
---

Use this skill for Python-only work.

Rules
- Keep the scope to Python files and Python tooling.
- Define the module boundary and contract before implementation.
- Prefer small, testable functions and explicit type hints.
- Put a Python `main()` entry point near the top of CLI files, after imports and constants and before helper functions.
- Add or update tests when behavior changes.
- Use Google-style docstrings for public functions and classes.
- Keep dependency flow inward and avoid mixing Python logic with unrelated platform code.
- Do not create files named `utils.py` or `helpers.py`.
- Prefer dependency injection for external systems such as HTTP clients, databases, and filesystems.