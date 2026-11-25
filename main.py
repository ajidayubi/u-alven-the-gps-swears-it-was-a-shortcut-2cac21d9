#!/usr/bin/env python3
"""The GPS Swears It Was a Shortcut — make.fun program/v1 entry.

Writes one line of plain text, the GPS's own excuse for sending the driver
down the wrong road, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The gate: the file must be UTF-8 text of 1 to 200 characters, not only
whitespace, exactly one line. The program checks the gate on the line before
writing and re-checks it on what is actually on disk, and refuses to finish
unless the round-trip is byte for byte identical.
"""

import os
import sys

LINE = (
    "The map said that lake was a road, and I don't argue with the map "
    "\u2014 I just repeat it louder. Ask the fish: they heard me coming."
)

MAX_CHARS = 200


def check_gate(text):
    """Mirror the sealed gate: 1-200 chars, one line, not only whitespace."""
    if not isinstance(text, str):
        return False, "not text"
    if len(text) < 1 or len(text) > MAX_CHARS:
        return False, "length %d outside 1-%d" % (len(text), MAX_CHARS)
    if text.strip() == "":
        return False, "only whitespace"
    if "\n" in text or "\r" in text:
        return False, "more than one line"
    text.encode("utf-8")  # raises if not encodable
    return True, "ok"


def main():
    ok, why = check_gate(LINE)
    if not ok:
        print("gate failed: %s" % why, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    with open(path, "rb") as f:
        raw = f.read()
    on_disk = raw.decode("utf-8")
    if on_disk != LINE:
        print("round-trip mismatch", file=sys.stderr)
        return 1
    ok, why = check_gate(on_disk)
    if not ok:
        print("gate failed on disk: %s" % why, file=sys.stderr)
        return 1

    print(LINE)
    print("chars: %d" % len(LINE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
