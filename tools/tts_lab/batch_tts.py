#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bake the kotonoha lesson lines into preset MP3s with the audition's picks.

Reads the spoken lines straight out of kotonoha_data.js (story steps + quiz
target words + lesson titles), cleans them with the *same* JS cleaner the app
uses, then synthesizes one MP3 per unique line with the chosen voice.

  # 1) dry run: show what would be generated, no network
  python tools/tts_lab/batch_tts.py --selection tts_selection.json --dry-run

  # 2) real run (VOICEVOX free tier: ~5s per line, so ~15 min for ~180 lines)
  python tools/tts_lab/batch_tts.py --selection tts_selection.json

  # 3) wire the result into the app
  #    -> tools/tts_lab/preset_map.json["js"] is a ready-to-paste object body
  python tools/tts_lab/batch_tts.py --emit-js

Voice selection file (copied from audition.html):
  {"roles": {"gemini": {"provider": "voicevox", "voiceId": "8"}, ...}}
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT_DIR = ROOT / "audio" / "kotonoha" / "auto"
MAP_FILE = HERE / "preset_map.json"

sys.path.insert(0, str(HERE))
from tts_lab import (  # noqa: E402
    SPEAK_DELAY,
    synth_fish,
    synth_gemini,
    synth_voicevox,
)

import requests  # noqa: E402

# Speakers that have their own voice, plus the narrator which rides on Gemini.
ROLE_FOR_SPEAKER = {
    "gemini": "gemini",
    "kotone": "kotone",
    "mio": "mio",
    "narrator": "gemini",
    # Guest cameos (100% female roster): voiced, appearing as mystery dialogue bubbles.
    "makima": "makima",
    "miko": "miko",
    "frieren": "frieren",
    "pekora": "pekora",
    "ryo": "ryo",
    "marine": "marine",
    "anya": "anya",
    "teio": "teio",
    "miku": "miku",
}
CORE_ROLES = ("gemini", "kotone", "mio")


# ---------------------------------------------------------------------------
# Extract spoken lines from kotonoha_data.js
# ---------------------------------------------------------------------------

NODE_EXTRACT = r"""
const fs = require('fs');
const src = fs.readFileSync(process.argv[1], 'utf8');
const w = {};
const run = new Function('window','self','globalThis',
  'var window=arguments[0];' + src + ';return window;');
const lessons = run(w, w, w).KOTONOHA_LESSONS || [];
const out = [];
function walk(o) {
  if (!o || typeof o !== 'object') return;
  if (Array.isArray(o)) { o.forEach(walk); return; }
  if (typeof o.jpPlain === 'string' && o.jpPlain.trim()) {
    out.push({ kind: 'story', speaker: o.speaker || 'gemini', raw: o.jpPlain, audio: o.audio || null });
  }
  if (typeof o.targetWord === 'string' && o.targetWord.trim()) {
    out.push({ kind: 'word', speaker: 'gemini', raw: o.targetWord, audio: null });
  }
  Object.values(o).forEach(walk);
}
walk(lessons);
lessons.forEach(l => {
  if (typeof l.titleJp === 'string' && l.titleJp.trim()) {
    out.push({ kind: 'title', speaker: 'gemini', raw: l.titleJp, audio: null });
  }
  (l.quizzes || []).forEach(q => {
    if (typeof q.geminiReactJp === 'string' && q.geminiReactJp.trim()) {
      out.push({ kind: 'react', speaker: 'gemini', raw: q.geminiReactJp, audio: null });
    }
  });
});
// The shared "wrong answer" encouragement line the engine speaks verbatim.
out.push({ kind: 'wrong', speaker: 'gemini',
  raw: 'おしい！もう<ruby>一度<rt>いちど</rt></ruby>確認しましょね🌸', audio: null });
process.stdout.write(JSON.stringify(out));
"""

# Reuse the app's own cleaner so preset keys match runtime cache keys exactly.
NODE_CLEAN = r"""
const fs = require('fs');
const eng = fs.readFileSync(process.argv[1], 'utf8');
const m = eng.match(/function cleanKotonohaTtsText\([\s\S]*?\n\s*\}/);
if (!m) { console.error('cleaner not found'); process.exit(1); }
const cleanKotonohaTtsText = eval('(' + m[0] + ')');
const texts = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
process.stdout.write(JSON.stringify(texts.map(t => cleanKotonohaTtsText(t))));
"""


def run_node(script: str, *args: str) -> str:
    proc = subprocess.run(
        ["node", "-e", script, *args],
        capture_output=True, text=True, encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "node failed")
    return proc.stdout


def load_lines() -> list[dict]:
    raw = json.loads(run_node(NODE_EXTRACT, str(ROOT / "kotonoha_data.js")))
    tmp = HERE / "_raw_lines.json"
    tmp.write_text(json.dumps([r["raw"] for r in raw], ensure_ascii=False), encoding="utf-8")
    try:
        cleaned = json.loads(run_node(NODE_CLEAN, str(ROOT / "kotonoha_engine.js"), str(tmp)))
    finally:
        tmp.unlink(missing_ok=True)

    for rec, clean in zip(raw, cleaned):
        rec["clean"] = clean
    return [r for r in raw if r["clean"]]


def dedupe(records: list[dict]) -> list[dict]:
    """One clip per unique cleaned text. First speaker wins (they own the line)."""
    seen: dict[str, dict] = {}
    for r in records:
        key = r["clean"]
        if key in seen:
            continue
        seen[key] = r
    return list(seen.values())


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------

def load_selection(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    roles = data.get("roles", data)
    out = {}
    for role in CORE_ROLES:
        pick = roles.get(role)
        if not pick:
            raise SystemExit(f"selection is missing a voice for '{role}'")
        out[role] = pick
    # Optional guest voices (makima / miko). Only included when assigned, so the
    # three main characters never fall back to somebody else's voice.
    for role, pick in roles.items():
        if role not in out and pick:
            out[role] = pick
    return out


def slug(text: str, speaker: str) -> str:
    return f"{speaker}_{hashlib.sha1(text.encode('utf-8')).hexdigest()[:10]}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Bake kotonoha lines into preset MP3s")
    ap.add_argument("--selection", default=str(HERE / "tts_selection.json"))
    ap.add_argument("--voices", default="", help="gemini=8,kotone=2,mio=3 (alternative to --selection)")
    ap.add_argument("--provider", default="voicevox", choices=["voicevox", "fish"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--include-existing", action="store_true",
                    help="also regenerate lines that already ship a hand-made MP3")
    ap.add_argument("--emit-js", action="store_true", help="write the JS map body from preset_map.json")
    args = ap.parse_args(argv)

    if args.emit_js:
        return emit_js()

    if args.voices:
        picks = {}
        for part in args.voices.split(","):
            role, vid = part.split("=", 1)
            picks[role.strip()] = {"provider": args.provider, "voiceId": vid.strip()}
        selection = {k: picks[k] for k in ("gemini", "kotone", "mio")}
    else:
        selection = load_selection(Path(args.selection))

    records = load_lines()
    if not args.include_existing:
        records = [r for r in records if not r.get("audio")]
    unique = dedupe(records)
    if args.limit:
        unique = unique[: args.limit]

    by_role: dict[str, int] = {}
    for r in unique:
        role = ROLE_FOR_SPEAKER.get(r["speaker"], "gemini")
        by_role[role] = by_role.get(role, 0) + 1

    total_chars = sum(len(r["clean"]) for r in unique)
    print(f"lines to bake: {len(unique)}  {by_role}")
    print(f"total chars: {total_chars} · est. audio {total_chars / 6.5:.0f}s")
    print("voices:", {k: f"{v['provider']}:{v['voiceId']}" for k, v in selection.items()})

    if args.dry_run:
        for r in unique[:15]:
            print(f"  [{r['speaker']:8}] {r['clean']}")
        if len(unique) > 15:
            print(f"  ... +{len(unique) - 15} more")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "GeminiFit-TTS-Batch/1.0"})
    fish_key = ""
    if any(v["provider"] == "fish" for v in selection.values()):
        fish_key = os.environ.get("FISH_AUDIO_API_KEY", "")
        if not fish_key:
            raise SystemExit("FISH_AUDIO_API_KEY is not set (needed by a fish pick)")

    preset = {}
    remap = {}
    if MAP_FILE.exists():
        try:
            saved = json.loads(MAP_FILE.read_text(encoding="utf-8"))
            preset = saved.get("map", {})
            remap = saved.get("remap", {})
        except Exception:
            preset = {}

    made = skipped = failed = 0
    credit_start = ""
    if fish_key:
        from tts_lab import fish_credit
        credit_start = fish_credit(fish_key, session)
        print(f"fish credit before: {credit_start} (model=s2.1-pro-free)")
    for i, rec in enumerate(unique, 1):
        role = ROLE_FOR_SPEAKER.get(rec["speaker"], "gemini")
        pick = selection.get(role) or selection["gemini"]
        role = role if role in selection else "gemini"
        name = slug(rec["clean"], role)
        rel = f"./audio/kotonoha/auto/{name}.mp3"
        path = OUT_DIR / f"{name}.mp3"

        if path.exists() and not args.force:
            preset[rec["clean"]] = rel
            skipped += 1
            continue

        try:
            if pick["provider"] == "fish":
                audio, ext, _ = synth_fish(pick["voiceId"], rec["clean"], fish_key, session)
            else:
                audio, ext, _ = synth_voicevox(int(pick["voiceId"]), rec["clean"], session)
                import time
                time.sleep(SPEAK_DELAY)
        except Exception as exc:
            failed += 1
            print(f"  [{i}/{len(unique)}] FAILED {rec['clean'][:24]} :: {exc}")
            continue

        path.write_bytes(audio)
        preset[rec["clean"]] = rel
        made += 1

        # Remember which hand-made MP3 this line used to point at, so the data
        # file can be repointed at the freshly baked clip (keeps one voice).
        if rec.get("audio"):
            remap[rec["audio"]] = rel

        if fish_key:
            from tts_lab import fish_credit
            now = fish_credit(fish_key, session)
            try:
                if float(now) < float(credit_start):
                    print(f"ABORT: fish credit dropped {credit_start} -> {now}. Stopping to avoid charges.")
                    break
            except ValueError:
                pass

        if made % 10 == 0 or i == len(unique):
            MAP_FILE.write_text(
                json.dumps({"map": preset, "remap": remap, "voices": selection}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"  [{i}/{len(unique)}] ok · made {made} skipped {skipped} failed {failed}")

    MAP_FILE.write_text(
        json.dumps({"map": preset, "remap": remap, "voices": selection}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"done · made {made} skipped {skipped} failed {failed} · {MAP_FILE}")
    print("next: python tools/tts_lab/batch_tts.py --emit-js")
    return 0 if failed == 0 else 1


def emit_js() -> int:
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    mapping = data["map"]
    lines = [
        "// AUTO-GENERATED by tools/tts_lab/batch_tts.py — paste the entries below",
        "// inside KOTONOHA_PRESET_AUDIO in kotonoha_engine.js",
    ]
    for text, path in sorted(mapping.items()):
        key = text.replace("\\", "\\\\").replace("'", "\\'")
        lines.append(f"  '{key}': '{path}',")
    out = HERE / "preset_map_snippet.js"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(mapping)} entries -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
