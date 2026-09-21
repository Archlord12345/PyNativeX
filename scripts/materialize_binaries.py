#!/usr/bin/env python3
"""Rebuild binary assets GitHub cannot store via the text-only Contents API."""

from __future__ import annotations

import base64
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER_JAR = ROOT / "apps/photo_gallery/android/gradle/wrapper/gradle-wrapper.jar"
WRAPPER_URL = "https://github.com/gradle/gradle/raw/v8.13.0/gradle/wrapper/gradle-wrapper.jar"

BINARIES = [
    ROOT / "apps/photo_gallery/android/app/src/main/res/drawable-nodpi/limbe_beach.jpg",
    ROOT / "apps/photo_gallery/android/app/src/main/res/drawable-nodpi/mount_cameroon.jpg",
    ROOT / "apps/photo_gallery/android/app/src/main/res/drawable-nodpi/rainforest.jpg",
    ROOT / "assets/0c51bfea-9b69-4621-8ef6-4200a0f92073.png",
]


def stitch(dest: Path) -> bool:
    # Look for files like mount_cameroon.jpg.b64.*
    # Original file is mount_cameroon.jpg
    # Target name should be mount_cameroon.png
    
    # Generate the base name with dots replaced by underscores
    # mount_cameroon.jpg -> mount_cameroon_jpg
    base_name = dest.name.replace(".", "_")
    
    parts = sorted(dest.parent.glob(f"{dest.name}.b64.*"))
    if not parts:
        # Check if the renamed file already exists
        renamed = dest.parent / f"{base_name}.png"
        return renamed.is_file() and renamed.stat().st_size > 0
    
    dest.parent.mkdir(parents=True, exist_ok=True)
    # The actual image data is written to the file
    content = base64.b64decode("".join(part.read_text(encoding="ascii") for part in parts))
    
    # Save as .png as required by Android
    renamed = dest.parent / f"{base_name}.png"
    renamed.write_bytes(content)
    
    print(f"restored {renamed.relative_to(ROOT)} ({renamed.stat().st_size} bytes)")
    return True


def fetch_wrapper() -> None:
    if WRAPPER_JAR.is_file() and WRAPPER_JAR.stat().st_size > 20_000:
        print(f"kept {WRAPPER_JAR.relative_to(ROOT)}")
        return
    WRAPPER_JAR.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(WRAPPER_URL) as response:
        WRAPPER_JAR.write_bytes(response.read())
    print(f"downloaded {WRAPPER_JAR.relative_to(ROOT)} ({WRAPPER_JAR.stat().st_size} bytes)")


def main() -> int:
    fetch_wrapper()
    missing = [path for path in BINARIES if not stitch(path)]
    if missing:
        print("missing binaries:", file=sys.stderr)
        for path in missing:
            print(f"  {path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
