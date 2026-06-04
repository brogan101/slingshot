"""Basic SlingShot repository smoke checks.

This script is intentionally lightweight. It checks the repo layout and config
without launching the GUI or importing every tool dependency.
"""
from __future__ import annotations

import json
import sys
from importlib.util import find_spec
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "slingshot3"

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    APP_DIR / "slingshot.py",
    APP_DIR / "tools.py",
    APP_DIR / "custom_tools.py",
    APP_DIR / "config.json",
]

CORE_IMPORTS = [
    "customtkinter",
    "psutil",
    "cryptography",
    "pyotp",
    "dns",
    "requests",
    "PIL",
    "matplotlib",
    "numpy",
    "pypdf",
    "pyperclip",
    "qrcode",
]


def check_required_files() -> list[str]:
    problems: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            problems.append(f"Missing required file: {path.relative_to(ROOT)}")
    return problems


def check_core_imports() -> list[str]:
    problems: list[str] = []
    for module_name in CORE_IMPORTS:
        if find_spec(module_name) is None:
            problems.append(f"Missing Python package/module: {module_name}")
    return problems


def check_config() -> list[str]:
    problems: list[str] = []
    config_path = APP_DIR / "config.json"
    if not config_path.exists():
        return ["Missing config file: slingshot3/config.json"]

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in config: {exc}"]

    favorites = config.get("favorites", [])
    if any(item is None for item in favorites):
        problems.append("Config favorites contains null entries. Remove them or replace with valid tool names.")

    default_timeout = config.get("default_timeout")
    if not isinstance(default_timeout, int) or default_timeout < 1:
        problems.append("Config default_timeout must be an integer greater than zero.")

    return problems


def main() -> int:
    checks = {
        "files": check_required_files(),
        "imports": check_core_imports(),
        "config": check_config(),
    }

    failed = False
    print("SlingShot smoke check")
    print("=" * 22)
    for name, problems in checks.items():
        if problems:
            failed = True
            print(f"\n{name.upper()}: FAIL")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(f"\n{name.upper()}: OK")

    if failed:
        print("\nResult: FAIL")
        return 1

    print("\nResult: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
