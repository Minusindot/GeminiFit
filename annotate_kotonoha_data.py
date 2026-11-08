#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kotonoha data annotator (v4.3.11): add expr/bg to story steps so SCG mode activates.

- bg: derived per lesson from bgImage filename keywords (VN_ASSET_SPEC.md 7 BGs).
- expr: conservative cue-based mapping on the Korean translation; strong cues only,
  everything else -> idle. Only gemini/kotone/mio steps are annotated (narrator stays ECG).
- sceneImg is kept as ECG fallback (resolver prefers SCG when expr present).

Usage:
  python annotate_kotonoha_data.py --dry-run   # print decisions, no write
  python annotate_kotonoha_data.py             # apply
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "kotonoha_data.js"

BG_RULES = [
    ("teahouse_night", ("night", "밤")),
    ("bookstore", ("bookstore", "kanji", "book", "library")),
    ("osaka_street", ("osaka", "takoyaki", "street", "subway", "train", "city")),
    ("ryokan_room", ("ryokan", "yukata", "onsen", "lantern")),
    ("park_track", ("park", "track", "jog", "cherry", "spring_wind", "walk", "run", "stretch")),
    ("gym_indoor", ("gym", "rehab", "massage", "tape_measure", "locker", "reformer", "squat", "pool", "machine")),
    ("teahouse_day", ("teahouse", "matcha", "wagashi", "cafe", "kitchen", "cooking", "apron", "toast", "kyoto_tea", "tea_")),
]

# Strong-cue emotion markers (Korean text / shared variants). First match wins.
EXPR_RULES = [
    ("shy", ("///", "부끄", "수줍", "얼굴이 빨개", "빨개졌", "빤히")),
    ("joke", ("헤헤", "윙크", "장난", "농담", "혀를 내밀", "능글")),
    ("angry", ("잔소리", "왜이래", "바보 같", "고집", "쯧", "콕콕")),
    ("shock", ("헐", "어머", "충격", "멘붕", "어떡해", "무서")),
    ("sad", ("아쉽", "미안", "걱정", "하나같이", "슬퍼", "미안해")),
    ("dark", ("단식 어렸", "단식 깨", "무시", "정색", "차가")),
    ("smile", ("최고", "멋지", "신나", "좋아", "행복", "기분 좋")),
]


def lesson_bg(bg_image: str) -> str:
    name = (bg_image or "").lower()
    for bg, keys in BG_RULES:
        if any(k in name for k in keys):
            return bg
    return "teahouse_day"


def step_expr(step: dict) -> str:
    if step.get("speaker") not in ("gemini", "kotone", "mio"):
        return None
    ko = step.get("ko") or ""
    for expr, keys in EXPR_RULES:
        if any(k in ko for k in keys):
            return expr
    return "idle"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raw = DATA.read_text(encoding="utf-8")
    start = raw.index("window.KOTONOHA_LESSONS = [") + len("window.KOTONOHA_LESSONS = ")
    end = raw.rindex("];") + 1
    lessons = json.loads(raw[start:end])

    annotated = 0
    for lesson in lessons:
        bg = lesson_bg(lesson.get("bgImage", ""))
        for step in lesson.get("story", []):
            expr = step_expr(step)
            if expr is None:
                continue
            annotated += 1
            ko = (step.get("ko") or "")[:34]
            print("  %s ep%s #%s -> expr=%s bg=%s | %s" % (lesson.get("id"), lesson.get("episode"), step.get("speaker"), expr, bg, ko))
            if not args.dry_run:
                step["expr"] = expr
                step["bg"] = bg

    print(f"annotated steps: {annotated}")
    if args.dry_run:
        return
    new_body = json.dumps(lessons, ensure_ascii=False, indent=2)
    out = raw[:start] + new_body + raw[end:]
    DATA.write_text(out, encoding="utf-8")
    print("written.")


if __name__ == "__main__":
    main()
