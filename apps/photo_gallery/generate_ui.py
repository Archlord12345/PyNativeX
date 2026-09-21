from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "sdk" / "python"))

import pynativex as pn  # noqa: E402
from gallery_app import app  # noqa: E402


def generate(output: Path) -> None:
    operations = pn.Reconciler().mount(app.home)
    document = {
        "framework": "PyNativeX",
        "protocol_version": pn.PROTOCOL_VERSION,
        "application": {"title": app.title, "entry": "gallery_app:app"},
        "operations": json.loads(pn.Reconciler.encode(operations)),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the Python gallery UI for Android.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("android/app/src/main/assets/gallery_ui.json"),
    )
    args = parser.parse_args()
    generate(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
