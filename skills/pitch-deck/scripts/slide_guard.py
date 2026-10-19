#!/usr/bin/env python3
"""Prove that an edit touched only the slides you meant to touch.

Usage:
    python3 slide_guard.py snapshot DECK.pptx SNAP.json
    python3 slide_guard.py compare  DECK.pptx SNAP.json --changed 13 [--changed 14 ...]

`snapshot` stores one fingerprint per slide (XML, notes, charts, images).
`compare` re-reads the deck and checks that every slide NOT listed in --changed
(1-based, as numbered in the deck) is identical, and that the slide count is
unchanged. Exit 0 = guard passed, 1 = something else changed. For an edit that adds
or removes slides, pass --expect-count N and --changed for the new/moved positions
(slides after an insertion shift, so compare by position only when counts match).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deck_lib import slide_fingerprints  # noqa: E402
from pptx import Presentation  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["snapshot", "compare"])
    ap.add_argument("deck")
    ap.add_argument("snap")
    ap.add_argument("--changed", type=int, action="append", default=[])
    ap.add_argument("--expect-count", type=int)
    a = ap.parse_args()
    fp = slide_fingerprints(Presentation(a.deck))
    if a.mode == "snapshot":
        Path(a.snap).write_text(json.dumps(fp))
        print(f"snapshot of {len(fp)} slides saved to {a.snap}")
        return 0
    before = json.loads(Path(a.snap).read_text())
    want = a.expect_count if a.expect_count is not None else len(before)
    bad = []
    if len(fp) != want:
        bad.append(f"slide count is {len(fp)}, expected {want}")
    if len(fp) == len(before):
        for i, (x, y) in enumerate(zip(before, fp), 1):
            if x != y and i not in a.changed:
                bad.append(f"slide {i} changed but was not expected to")
    for i in a.changed:
        if len(fp) == len(before) and i <= len(fp) and before[i - 1] == fp[i - 1]:
            print(f"note: slide {i} was listed as changed but is identical")
    if bad:
        print("GUARD FAILED:\n  " + "\n  ".join(bad))
        return 1
    print(f"guard passed: {len(fp)} slides, only {sorted(a.changed) or 'nothing'} changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
