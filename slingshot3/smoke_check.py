"""Basic SlingShot repository smoke checks.

This script is intentionally lightweight. It checks the repo layout, config,
and next-generation registry wiring without launching the GUI or importing the
legacy 4k+ line tool module.
"""
from __future__ import annotations

import json
import sys
from importlib.util import find_spec
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "slingshot3"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    APP_DIR / "slingshot.py",
    APP_DIR / "slingshot_next.py",
    APP_DIR / "tools.py",
    APP_DIR / "safe_tools.py",
    APP_DIR / "tool_registry.py",
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
    if not isinstance(favorites, list):
        problems.append("Config favorites must be a list.")
    elif any(item is None or item == "" for item in favorites):
        problems.append("Config favorites contains blank/null entries.")

    default_timeout = config.get("default_timeout")
    if not isinstance(default_timeout, int) or default_timeout < 1:
        problems.append("Config default_timeout must be an integer greater than zero.")

    return problems


def check_next_registry() -> list[str]:
    problems: list[str] = []
    try:
        from tool_registry import all_tools, categories
        from safe_tools import HANDLERS
    except Exception as exc:
        return [f"Failed to import next-gen registry modules: {type(exc).__name__}: {exc}"]

    tools = all_tools()
    if not tools:
        problems.append("Tool registry is empty.")

    seen_names: set[str] = set()
    for tool in tools:
        if tool.name in seen_names:
            problems.append(f"Duplicate tool name in registry: {tool.name}")
        seen_names.add(tool.name)
        if tool.handler_name not in HANDLERS:
            problems.append(f"Missing handler for {tool.name}: {tool.handler_name}")

    if not categories():
        problems.append("No categories returned by registry.")

    return problems


def main() -> int:
    checks = {
        "files": check_required_files(),
        "imports": check_core_imports(),
        "config": check_config(),
        "next_registry": check_next_registry(),
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
