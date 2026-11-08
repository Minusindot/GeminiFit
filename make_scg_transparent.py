#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini Fit SCG transparentizer (v4.3.11)

Takes generated standing sprites shot on solid magenta (#FF00FF) backgrounds
in  image/_scg_work/{char}/{expr}.png
and produces true transparent PNGs at
  image/scg/{char}/{char}_default_{expr}.png

Key detail (VN spec): all 8 expressions of one character must share the SAME
canvas + bounding box so expressions cross-fade without shifting.
-> The 'idle' version defines the trim box; it is applied to all expressions.

Usage:
  python make_scg_transparent.py [--char gemini] [--expr smile]
"""
import argparse
import os
import sys

from PIL import Image
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(BASE_DIR, "image", "_scg_work")
OUT_DIR = os.path.join(BASE_DIR, "image", "scg")

EXPRESSIONS = ["idle", "smile", "sad", "angry", "shy", "shock", "dark", "joke"]
CHARS = ["gemini", "kotone", "mio"]

# canvas target per VN_ASSET_SPEC.md is ~1080x2560 portrait (ratio 1:2.37).
# Engine renders object-contain; we keep a tall canvas with identical layout.
CANVAS_W, CANVAS_H = 1080, 2560


def chroma_key_alpha(img: Image.Image) -> np.ndarray:
    """Return alpha mask where 1 = foreground (not magenta background)."""
    arr = np.asarray(img.convert("RGB")).astype(np.int32)
    h, w, _ = arr.shape
    # distance from pure magenta
    dist = np.sqrt((arr[..., 0] - 255) ** 2 + (arr[..., 1] - 0) ** 2 + (arr[..., 2] - 255) ** 2)
    # fuzzy edge: fully transparent < 60, fully opaque > 150, smooth in between
    alpha = np.clip((dist - 60) / 90.0, 0.0, 1.0)
    return alpha


def trim_box_from_alpha(alpha: np.ndarray, pad: int = 16):
    ys, xs = np.where(alpha > 0.5)
    if len(xs) == 0:
        return None
    x0, x1 = max(0, xs.min() - pad), min(alpha.shape[1] - 1, xs.max() + pad)
    y0, y1 = max(0, ys.min() - pad), min(alpha.shape[0] - 1, ys.max() + pad)
    return (x0, y0, x1 + 1, y1 + 1)


def process_character(char: str, only_expr: str | None = None):
    work = os.path.join(WORK_DIR, char)
    out = os.path.join(OUT_DIR, char)
    os.makedirs(out, exist_ok=True)

    # 1) chroma key every available expression, keep in memory
    rgba_by_expr = {}
    for expr in EXPRESSIONS:
        if only_expr and expr != only_expr and not (
            expr == "idle" or only_expr == "idle"
        ):
            # still need idle for the shared trim box
            if expr != "idle":
                continue
        src = os.path.join(work, f"{expr}.png")
        if not os.path.isfile(src):
            # also accept .jpg/.webp from the generator
            found = None
            for ext in (".jpg", ".jpeg", ".webp"):
                if os.path.isfile(os.path.join(work, f"{expr}{ext}")):
                    found = os.path.join(work, f"{expr}{ext}")
                    break
            if not found:
                print(f"  [skip] {char}/{expr}: source not found")
                continue
            src = found
        img = Image.open(src).convert("RGB")
        alpha = chroma_key_alpha(img)
        rgba = np.dstack([np.asarray(img), (alpha * 255).astype(np.uint8)])
        rgba_by_expr[expr] = rgba

    if not rgba_by_expr:
        print(f"  [{char}] no sources processed")
        return False

    # 2) shared trim box from idle (fallback: first available)
    ref = rgba_by_expr.get("idle") or next(iter(rgba_by_expr.values()))
    box = trim_box_from_alpha(ref[..., 3])
    if box is None:
        print(f"  [{char}] ERROR: empty foreground in reference")
        return False
    x0, y0, x1, y1 = box
    cw, ch = x1 - x0, y1 - y0
    print(f"  [{char}] trim box ({x0},{y0})-({x1},{y1}) size {cw}x{ch}")

    # 3) fit trimmed content onto the shared portrait canvas
    scale = min(CANVAS_W / cw, CANVAS_H / ch) if cw and ch else 1.0
    tw, th = max(1, round(cw * scale)), max(1, round(ch * scale))
    ox, oy = (CANVAS_W - tw) // 2, (CANVAS_H - th) // 2

    ok = True
    for expr, rgba in rgba_by_expr.items():
        cropped = Image.fromarray(rgba, mode="RGBA").crop(box)
        resized = cropped.resize((tw, th), Image.LANCZOS)
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        canvas.paste(resized, (ox, oy), resized)
        dst = os.path.join(out, f"{char}_default_{expr}.png")
        canvas.save(dst)
        print(f"  [ok] {dst} ({tw}x{th} on {CANVAS_W}x{CANVAS_H}, alpha={'%.1f%%' % (100 * (np.asarray(resized)[..., 3] > 10).mean())})")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--char", default=None)
    ap.add_argument("--expr", default=None)
    args = ap.parse_args()
    chars = [args.char] if args.char else CHARS
    all_ok = True
    for char in chars:
        print(f"== {char} ==")
        all_ok &= process_character(char, args.expr)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
