from __future__ import annotations

import argparse
import importlib
import json
import platform
import shutil
import sys
from pathlib import Path

from .protocol import Reconciler

APP_TEMPLATE = '''import pynativex as pn

app = pn.App(
    title="{display_name}",
    home=pn.Scaffold(
        app_bar=pn.AppBar(pn.Text("{display_name}")),
        body=pn.Center(pn.Text("Built with PyNativeX")),
    ),
)
'''

PYPROJECT_TEMPLATE = '''[project]
name = "{package_name}"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pynativex>=0.1.0a1"]

[tool.pynativex]
app_id = "dev.pynativex.{module_name}"
name = "{display_name}"
entry = "{module_name}.main:app"

[tool.pynativex.android]
min_sdk = 24
target_sdk = 36
abis = ["arm64-v8a"]
'''


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pynativex",
        description="PyNativeX project and native build tooling.",
    )
    parser.add_argument("--version", action="version", version="PyNativeX 0.1.0a1")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a minimal application.")
    create.add_argument("name", help="Project directory and package name.")
    create.add_argument("--directory", type=Path, default=Path.cwd())
    create.add_argument(
        "--force",
        action="store_true",
        help="Write into an existing empty directory.",
    )

    subparsers.add_parser("doctor", help="Check the local Android toolchain.")

    inspect = subparsers.add_parser("inspect", help="Render an example UI protocol batch.")
    inspect.add_argument("--entry", help="Application entry point, for example package.main:app.")
    inspect.add_argument("--output", type=Path, help="Write the protocol batch to a file.")
    inspect.add_argument("--pretty", action="store_true")

    build = subparsers.add_parser("build", help="Validate a native build request.")
    build.add_argument("platform", choices=["android"])
    build.add_argument("--release", action="store_true")
    build.add_argument("--dry-run", action="store_true")
    return parser


def _emit(payload: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")


def _create(args: argparse.Namespace, as_json: bool) -> int:
    package_name = args.name.lower().replace("-", "_")
    target = args.directory / args.name
    if target.exists() and any(target.iterdir()):
        _emit({"error": f"{target} is not empty"}, as_json)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    module = target / package_name
    module.mkdir(exist_ok=True)
    (module / "__init__.py").write_text("", encoding="utf-8")
    values = {
        "package_name": package_name,
        "module_name": package_name,
        "display_name": args.name.replace("-", " ").title(),
    }
    (module / "main.py").write_text(APP_TEMPLATE.format(**values), encoding="utf-8")
    (target / "pyproject.toml").write_text(PYPROJECT_TEMPLATE.format(**values), encoding="utf-8")
    _emit({"created": str(target), "entry": f"{package_name}.main:app"}, as_json)
    return 0


def _doctor(as_json: bool) -> int:
    checks = {
        "python": platform.python_version(),
        "java": shutil.which("java"),
        "adb": shutil.which("adb"),
        "cmake": shutil.which("cmake"),
        "android_sdk": bool(Path.home().joinpath("Android", "Sdk").exists()),
    }
    ready = all(checks[name] for name in ("java", "adb", "cmake")) and checks["android_sdk"]
    _emit({"ready": ready, "checks": checks}, as_json)
    return 0 if ready else 1


def _load_app(entry: str) -> object:
    try:
        module_name, attribute = entry.split(":", 1)
    except ValueError as exc:
        raise ValueError("entry must use the form package.module:attribute") from exc
    module = importlib.import_module(module_name)
    try:
        return getattr(module, attribute)
    except AttributeError as exc:
        raise ValueError(f"{entry} does not exist") from exc


def _inspect(entry: str | None, pretty: bool, output: Path | None) -> int:
    from .widgets import App, Center, Scaffold, Text, Widget

    root: Widget = Scaffold(Center(Text("PyNativeX")))
    if entry:
        loaded = _load_app(entry)
        if not isinstance(loaded, App):
            raise ValueError(f"{entry} is not a PyNativeX App")
        root = loaded.home
    operations = Reconciler().mount(root)
    indent = 2 if pretty else None
    payload = [{"code": op.code, "id": op.node_id, **(op.payload or {})} for op in operations]
    rendered = json.dumps(payload, indent=indent, ensure_ascii=False)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(f"{rendered}\n", encoding="utf-8")
        print(output)
    else:
        print(rendered)
    return 0


def _build(args: argparse.Namespace, as_json: bool) -> int:
    if not Path("pyproject.toml").exists():
        _emit({"error": "pyproject.toml was not found"}, as_json)
        return 2
    if not args.dry_run:
        _emit(
            {
                "error": (
                    "The alpha validates build inputs only; "
                    "Android engine artifacts are not published yet."
                ),
                "hint": "Use --dry-run or follow docs/roadmap.md.",
            },
            as_json,
        )
        return 3
    _emit(
        {
            "platform": args.platform,
            "mode": "release" if args.release else "debug",
            "validated": True,
        },
        as_json,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "create":
        return _create(args, args.json)
    if args.command == "doctor":
        return _doctor(args.json)
    if args.command == "inspect":
        try:
            return _inspect(args.entry, args.pretty, args.output)
        except (ModuleNotFoundError, ValueError) as exc:
            _emit({"error": str(exc)}, args.json)
            return 2
    if args.command == "build":
        return _build(args, args.json)
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    sys.exit(main())
