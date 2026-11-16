#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Point every `audio:` field in kotonoha_data.js at its own freshly baked clip.

The lesson data is quirky: 34 story steps share only 7 `audio` paths, so eight
different lines used to play the exact same MP3. String-replacing the path
would preserve that bug, so instead each `audio` field is matched to the
`jpPlain` of its own object and repointed at the clip baked for *that* line.

  python tools/tts_lab/apply_remap.py --dry-run
  python tools/tts_lab/apply_remap.py
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
from batch_tts import run_node, NODE_CLEAN  # noqa: E402

AUDIO_RE = re.compile(r'"audio"\s*:\s*"([^"]+)"')
JP_PLAIN_RE = re.compile(r'"jpPlain"\s*:\s*"((?:[^"\\]|\\.)*)"')


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))["map"]
    src = DATA.read_text(encoding="utf-8")

    # Pair each audio field with the jpPlain that follows it inside the same object.
    pairs = []
    for m in AUDIO_RE.finditer(src):
        tail = src[m.end(): m.end() + 600]
        jp = JP_PLAIN_RE.search(tail)
        pairs.append((m, jp.group(1) if jp else None))

    raws = [p[1] for p in pairs if p[1]]
    tmp = HERE / "_remap_lines.json"
    tmp.write_text(json.dumps(raws, ensure_ascii=False), encoding="utf-8")
    try:
        cleaned = json.loads(run_node(NODE_CLEAN, str(ROOT / "kotonoha_engine.js"), str(tmp)))
    finally:
        tmp.unlink(missing_ok=True)

    out, cursor, changed, missing = [], 0, 0, 0
    ci = 0
    for m, jp in pairs:
        if jp is None:
            continue
        clean = cleaned[ci]
        ci += 1
        new = mapping.get(clean)
        if not new:
            missing += 1
            continue
        out.append(src[cursor:m.start(1)])
        out.append(new)
        cursor = m.end(1)
        changed += 1
    out.append(src[cursor:])
    result = "".join(out)

    print(f"audio fields: {len(pairs)} · repointed: {changed} · no baked clip: {missing}")
    if args.dry_run:
        return 0
    DATA.write_text(result, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
