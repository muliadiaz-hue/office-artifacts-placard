#!/usr/bin/env python3
"""Office Artifacts: The One-Line Placard Contest.

Writes a one-line museum placard for an ordinary office object — a
charging cable, recast as an ancient artifact — to the harness output
file ``entry.txt`` inside ``$MAKEFUN_OUTPUT_DIR`` (falling back to
``/output/entry.txt`` when the variable is unset).

The placard text lives in ``entry.txt`` next to this script and is
copied byte for byte, so the program itself carries no wording of its
own; it only moves the bytes from the repo to the output directory.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FALLBACK_OUTPUT = Path("/output/entry.txt")


def output_path() -> Path:
    """Resolve where the harness expects the entry file."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return Path(chosen) / "entry.txt"
    return FALLBACK_OUTPUT


def main() -> int:
    source = HERE / "entry.txt"
    placard = source.read_bytes()
    # Gate guard: the entry must be one UTF-8 line of 1-180 characters.
    text = placard.decode("utf-8")
    if not 1 <= len(text) <= 180:
        print(f"entry is {len(text)} chars, outside the 1-180 gate", file=sys.stderr)
        return 1
    if "\n" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(placard)
    print(f"wrote {len(placard)} bytes to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
