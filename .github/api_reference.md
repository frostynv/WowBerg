# Blizzard World of Warcraft API Reference

Primary docs: https://community.developer.battle.net/documentation/world-of-warcraft

Guidance:
- Use explicit base URL, namespace, locale, and auth token when building requests.
- Keep ingestion clients focused on retrieval; do not embed business logic in API clients.
- Prefer small, testable request wrappers and inject HTTP clients for testability.

Example request template:

GET {base_url}/data/wow/item/{item_id}?namespace={namespace}&locale={locale}&access_token={token}

