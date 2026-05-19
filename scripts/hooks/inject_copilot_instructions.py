import json

from _summary_tools import load_summary_message


def main() -> None:
    content = load_summary_message(
        summary_relative_path='.github/summaries/copilot_instructions_summary.md',
        fallback_message=(
            'Follow repository copilot instructions for global rules: organize code by technical responsibility, '
            'define interfaces before implementation, enforce inward dependency flow, and avoid utils/helpers files.'
        ),
    )
    print(json.dumps({"continue": True, "systemMessage": content}))


if __name__ == "__main__":
    main()
