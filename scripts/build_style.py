"""Compile style.less into asset/style.css using lessc (via npx)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESS_FILE = ROOT / "style.less"
CSS_FILE = ROOT / "asset" / "style.css"


def build_style() -> int:
    if not LESS_FILE.is_file():
        print(f"Error: {LESS_FILE} not found.", file=sys.stderr)
        return 1

    CSS_FILE.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["npx", "--yes", "less", str(LESS_FILE), str(CSS_FILE)]
    print(f"Compiling {LESS_FILE.name} -> {CSS_FILE.relative_to(ROOT)}...")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(ROOT),
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as exc:
        print(f"Compilation failed with exit code {exc.returncode}:", file=sys.stderr)
        if exc.stdout:
            print(exc.stdout, file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        return exc.returncode
    except Exception as exc:
        print(f"Failed to run npx less: {exc}", file=sys.stderr)
        return 1

    if CSS_FILE.is_file():
        size_kb = CSS_FILE.stat().st_size / 1024
        print(f"Successfully compiled {CSS_FILE.relative_to(ROOT)} ({size_kb:.1f} KB).")
        return 0

    print("Error: Output CSS file was not generated.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(build_style())
