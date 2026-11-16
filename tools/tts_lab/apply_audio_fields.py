#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Give every story step that lacks an `audio` field one from preset_map.json.

Newly written lines (guest cameos, future episodes) start life without an
`audio` field. `speakJapanese` would still find the clip through the preset
map, but pinning the field makes the intent explicit and keeps the manga panel
and the preloader pointing at the same file.

Idempotent: steps that already have `audio` are left alone.

  python tools/tts_lab/apply_audio_fields.py --dry-run
  python tools/tts_lab/apply_audio_fields.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "kotonoha_data.js"
MAP_FILE = HERE / "preset_map.json"

sys.path.insert(0, str(HERE))
from batch_tts import NODE_CLEAN, run_node  # noqa: E402

JP_RUBY = re.compile(r'^(\s*)"jpRuby":')
JP_PLAIN = re.compile(r'^\s*"jpPlain":\s*"((?:[^"\\]|\\.)*)"')
AUDIO = re.compile(r'^\s*"audio":')


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))["map"]
    lines = DATA.read_text(encoding="utf-8").split("\n")

    # Pass 1: find steps without audio and grab the jpPlain that follows.
    targets = []  # (jpRuby index, indent, raw jpPlain)
    for i, line in enumerate(lines):
        m = JP_RUBY.match(line)
        if not m:
            continue
        if any(AUDIO.match(lines[j]) for j in range(max(0, i - 6), i)):
            continue
        for j in range(i + 1, min(i + 5, len(lines))):
            pm = JP_PLAIN.match(lines[j])
            if pm:
                targets.append((i, m.group(1), pm.group(1)))
                break

    if not targets:
        print("every story step already has an audio field")
        return 0

    # Pass 2: clean with the app's own cleaner so keys match the preset map.
    raw = [t[2] for t in targets]
    tmp = HERE / "_audio_fields.json"
    tmp.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    try:
        cleaned = json.loads(run_node(NODE_CLEAN, str(ROOT / "kotonoha_engine.js"), str(tmp)))
    finally:
        tmp.unlink(missing_ok=True)

    inserted = missing = 0
    out = list(lines)
    # Insert bottom-up so earlier indexes stay valid.
    for (idx, indent, raw_text), clean in sorted(zip(targets, cleaned), reverse=True):
        path = mapping.get(clean)
        if not path:
            missing += 1
            print(f"  no baked clip for: {raw_text}")
            continue
        out.insert(idx, f'{indent}"audio": "{path}",')
        inserted += 1

    print(f"story steps without audio: {len(targets)} · inserted: {inserted} · no clip: {missing}")
    if args.dry_run or not inserted:
        return 0
    DATA.write_text("\n".join(out), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
