# Copilot Instructions for WowBerg

## Non-Negotiable Rules
- Define interfaces/contracts before implementation logic when adding new module boundaries.
- Keep dependency flow inward.
- Do not create catch-all files named `utils.py` or `helpers.py`.
- Use explicit dependency injection for external systems.

## Response and Code Style
- Prefer small, testable functions and clear module boundaries.
- Add comments only where behavior is not obvious.
- Keep examples practical and concise.