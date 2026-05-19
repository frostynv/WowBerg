# API Reference Summary

- Primary docs: https://community.developer.battle.net/documentation/world-of-warcraft
- Guidance: use explicit base URL, namespace, locale, and auth token when building requests; keep API clients focused on retrieval and avoid embedding business logic.
- Example request template:

  GET {base_url}/data/wow/item/{item_id}?namespace={namespace}&locale={locale}&access_token={token}

Full doc: .github/api_reference.md
