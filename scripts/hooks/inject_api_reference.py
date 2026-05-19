import json

from _summary_tools import load_summary_message


def main() -> None:
    content = load_summary_message(
        summary_relative_path='.github/summaries/api_reference_summary.md',
        fallback_message=(
            'Primary docs: https://community.developer.battle.net/documentation/world-of-warcraft. '
            'When implementing ingestion clients, prefer explicit base URL, namespace, locale, and auth token; '
            'keep API clients focused on retrieval and avoid embedding business logic in them.'
        ),
    )
    print(json.dumps({"continue": True, "systemMessage": content}))


if __name__ == "__main__":
    main()
