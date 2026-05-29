---
name: fullstack-coding
description: Coding skill for the Fullstack Agent. Use when the task needs software design or implementation guidance, including module boundaries, contract-first design, dependency flow, and testable code.
---

Use this skill for coding-focused tasks.

Rules
- Name the module boundary and contract before implementation.
- Prefer the smallest slice that proves the change.
- Add tests when behavior changes.
- Ask concise, actionable questions when blocked.
- Separate modules by responsibility: interfaces, core math, services, IO adapters.
- Keep dependencies inward: interfaces/core -> services -> IO adapters.
- Do not let service or analytics code import infrastructure adapters.
- Define Protocol or abstract contract before implementation logic.
- Make type contracts explicit and behavior-focused.
- Keep ingestion clients focused on retrieval only.
- Do not create files named `utils.py` or `helpers.py`.
- Prefer dependency injection for HTTP clients, database gateways, and filesystem adapters.
