#!/usr/bin/env python3
"""One Word, One Username, One Reward.

Writes exactly one word - the entrant's own make.fun username - and
nothing else, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
"""

import os
import shutil
from pathlib import Path

USERNAME = "antiah-01"
OUTPUT_NAME = "entry.txt"


def clear_contents(directory: Path) -> None:
    """Remove only the contents of directory, never the directory itself."""
    for child in directory.iterdir():
        if child.is_symlink() or not child.is_dir():
            child.unlink()
        else:
            shutil.rmtree(child)


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    clear_contents(out_dir)
    target = out_dir / OUTPUT_NAME
    payload = USERNAME.encode("utf-8")
    target.write_bytes(payload)
    # Read the file back and verify it byte for byte before exiting, so a
    # silent write failure can never pass as a valid entry. Mirror the
    # competition gate here: 1-30 UTF-8 characters, one word, no padding.
    written = target.read_bytes()
    assert written == payload, "output mismatch on read-back"
    text = written.decode("utf-8")
    assert 1 <= len(text) <= 30, "output outside the 1-30 character gate"
    assert text == text.strip() and " " not in text, "output is not one word"


if __name__ == "__main__":
    main()
