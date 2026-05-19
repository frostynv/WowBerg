from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_path(*parts: str) -> Path:
    return REPO_ROOT.joinpath(*parts)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding='utf-8')
    except OSError:
        return None


def load_summary_message(*, summary_relative_path: str, fallback_message: str) -> str:
    summary_path = repo_path(summary_relative_path)
    summary_text = read_text(summary_path)
    if summary_text:
        return summary_text.strip()

    return fallback_message