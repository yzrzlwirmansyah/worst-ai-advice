#!/usr/bin/env python3
"""Worst AI Advice: The 48-Hour Tight Line Open.

Writes a single line of the worst possible advice an AI could give
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt),
then reads it back and verifies it on disk before exiting.
Stdlib only, deterministic.
"""

import os
import sys

ENTRY = "To test if a socket is live, lick your finger and touch both holes \u2014 tingling means it's working."

EXPECTED = ENTRY + "\n"


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EXPECTED)

    # Post-write self-verification: read it back and check it on disk.
    with open(path, "r", encoding="utf-8") as f:
        on_disk = f.read()

    if on_disk != EXPECTED:
        print(
            "ERROR: verification failed — entry.txt on disk does not match "
            "the expected line.",
            file=sys.stderr,
        )
        return 1

    if not 1 <= len(ENTRY) <= 140:
        print(
            f"ERROR: verification failed — entry is {len(ENTRY)} chars, "
            "outside the 1–140 char gate.",
            file=sys.stderr,
        )
        return 1

    print(f"Wrote {len(ENTRY)}-char entry to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
