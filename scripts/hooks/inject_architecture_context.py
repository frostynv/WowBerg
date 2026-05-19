import json

from _summary_tools import load_summary_message


def main() -> None:
    content = load_summary_message(
        summary_relative_path='.github/summaries/architecture_summary.md',
        fallback_message=(
            'Use .github/full_stack_structure.md as the authoritative architecture law. '
            'Key rules: Separation of Concerns, Contract-First development, Inward dependency flow, '
            'ban utils.py/helpers.py, and use dependency injection.'
        ),
    )
    print(json.dumps({"continue": True, "systemMessage": content}))


if __name__ == "__main__":
    main()
