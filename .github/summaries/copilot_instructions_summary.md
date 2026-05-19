# Copilot Instructions Summary

- Organize code by technical responsibility; avoid feature folders that mix concerns.
- Define interfaces/contracts before writing implementation (Contract-First development).
- Enforce inward dependency flow: core/interfaces → services → IO adapters.
- Do not create `utils.py` or `helpers.py` — keep files focused and cohesive.
- Use explicit dependency injection for HTTP clients, DB gateways, and filesystem adapters.
- API/IO guidance: build requests with explicit base URL, namespace, locale, and auth token; keep ingestion clients retrieval-only.

Full doc: .github/copilot-instructions.md
