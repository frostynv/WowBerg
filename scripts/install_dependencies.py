"""Install the project dependencies into the local virtual environment.

This script creates the project-local virtual environment when needed and then
installs the project in editable mode so the host-side environment matches the
dependencies declared in pyproject.toml.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VENV_DIR = PROJECT_ROOT / ".venv"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create or update the local virtual environment from pyproject.toml."
    )
    parser.add_argument(
        "--venv",
        type=Path,
        default=DEFAULT_VENV_DIR,
        help="Path to the local virtual environment to create or update.",
    )
    return parser.parse_args()


def venv_python(venv_dir: Path) -> Path:
    """Return the Python executable path for a virtual environment.

    Args:
        venv_dir (Path): Virtual environment directory.

    Returns:
        Path: Platform-specific Python executable inside the virtual environment.
    """
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"

    return venv_dir / "bin" / "python"


def run_command(command: list[str]) -> None:
    """Run a subprocess command.

    Args:
        command (list[str]): Command and arguments to execute.

    Returns:
        None: This function raises on failure.
    """
    subprocess.run(command, check=True)


def ensure_virtualenv(venv_dir: Path) -> None:
    """Create the local virtual environment if it does not exist.

    Args:
        venv_dir (Path): Target virtual environment directory.

    Returns:
        None: This function creates the environment in place when needed.
    """
    python_executable = venv_python(venv_dir)
    if python_executable.exists():
        return

    run_command([sys.executable, "-m", "venv", str(venv_dir)])


def install_dependencies(project_root: Path, venv_dir: Path) -> None:
    """Create the virtual environment and install the project in editable mode.

    Args:
        project_root (Path): Path to the repository root containing pyproject.toml.
        venv_dir (Path): Target virtual environment directory.

    Raises:
        FileNotFoundError: Raised when pyproject.toml does not exist.
        subprocess.CalledProcessError: Raised when pip or venv creation fails.
    """
    project_file = project_root / "pyproject.toml"
    if not project_file.exists():
        raise FileNotFoundError(f"Project metadata file not found: {project_file}")

    ensure_virtualenv(venv_dir)

    python_executable = venv_python(venv_dir)
    run_command([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])
    run_command([str(python_executable), "-m", "pip", "install", "--upgrade", "-e", str(project_root)])


def main() -> int:
    """Run the dependency installation workflow.

    Returns:
        int: Zero on success, non-zero on failure.
    """
    arguments = parse_args()

    try:
        install_dependencies(PROJECT_ROOT, arguments.venv)
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"Dependency installation failed: {error}", file=sys.stderr)
        return 1

    print(f"Installed {PROJECT_ROOT} into {arguments.venv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())