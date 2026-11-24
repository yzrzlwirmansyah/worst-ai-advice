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
    # 1. Raw bytes: exact UTF-8 encoding, no BOM, no extra trailing data.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != EXPECTED.encode("utf-8"):
        print(
            "ERROR: verification failed — entry.txt bytes do not match "
            "the expected UTF-8 encoding.",
            file=sys.stderr,
        )
        return 1
    if raw.startswith(b"\xef\xbb\xbf"):
        print(
            "ERROR: verification failed — entry.txt starts with a UTF-8 BOM.",
            file=sys.stderr,
        )
        return 1

    # 2. Decoded text: must be valid UTF-8 and exactly the chosen line + "\n".
    with open(path, "r", encoding="utf-8") as f:
        on_disk = f.read()

    if on_disk != EXPECTED:
        print(
            "ERROR: verification failed — entry.txt on disk does not match "
            "the expected line.",
            file=sys.stderr,
        )
        return 1

    # 3. Single line: exactly one "\n", at the very end, no other newlines.
    if on_disk.count("\n") != 1 or not on_disk.endswith("\n"):
        print(
            "ERROR: verification failed — entry.txt must be exactly one "
            "line ending with a single newline.",
            file=sys.stderr,
        )
        return 1
    if "\r" in on_disk:
        print(
            "ERROR: verification failed — entry.txt contains a carriage "
            "return.",
            file=sys.stderr,
        )
        return 1

    # 4. Length gate: 1–140 chars, measured on the line without the newline.
    line = on_disk.rstrip("\n")
    if not 1 <= len(line) <= 140:
        print(
            f"ERROR: verification failed — entry is {len(line)} chars, "
            "outside the 1–140 char gate.",
            file=sys.stderr,
        )
        return 1

    # 5. No stray whitespace or trailing/leading space on the line.
    if line != line.strip():
        print(
            "ERROR: verification failed — entry line has leading or "
            "trailing whitespace.",
            file=sys.stderr,
        )
        return 1

    print(f"Wrote {len(ENTRY)}-char entry to {path} (verified: {len(raw)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
