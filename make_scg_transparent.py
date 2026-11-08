#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini Fit SCG transparentizer (v4.3.11)

Takes generated standing sprites shot on a plain pure white background
in  image/_scg_work/{char}/{expr}_raw.png
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

import numpy as np
from PIL import Image

from _common import remove_flat_background, alpha_bbox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(BASE_DIR, "image", "_scg_work")
OUT_DIR = os.path.join(BASE_DIR, "image", "scg")

EXPRESSIONS = ["idle", "smile", "sad", "angry", "shy", "shock", "dark", "joke"]
# char folder under _scg_work -> (output subdir under image/scg, file-name parts)
OUTFIT_TARGETS = {
    "gemini": ("gemini", "gemini_default_"),
    "gemini_menhera": ("gemini", "gemini_menhera_"),
    "kotone": ("kotone", "kotone_default_"),
    "mio": ("mio", "mio_default_"),
}
CHARS = ["gemini", "gemini_menhera", "kotone", "mio"]

# canvas target per VN_ASSET_SPEC.md is ~1080x2560 portrait (ratio 1:2.37).
# Engine renders object-contain; we keep a tall canvas with identical layout.
CANVAS_W, CANVAS_H = 1080, 2560


def raw_path(work: str, expr: str) -> str | None:
    names = [f"{expr}_raw.png", f"{expr}.png", f"{expr}.jpg", f"{expr}.jpeg", f"{expr}.webp"]
    if expr == "idle":
        names.insert(0, "base_raw.png")
    for name in names:
        p = os.path.join(work, name)
        if os.path.isfile(p):
            return p
    return None


def transparentize(img: Image.Image) -> Image.Image:
    """흰 배경 제거. 흰 옷을 살리려 threshold를 보수적으로 잡는다."""
    return remove_flat_background(img.convert("RGB"), threshold=24, feather=0.7)


def trim_box_from_alpha(alpha: np.ndarray, pad: int = 16):
    ys, xs = np.where(alpha > 0.5)
    if len(xs) == 0:
        return None
    x0, x1 = max(0, xs.min() - pad), min(alpha.shape[1] - 1, xs.max() + pad)
    y0, y1 = max(0, ys.min() - pad), min(alpha.shape[0] - 1, ys.max() + pad)
    return (x0, y0, x1 + 1, y1 + 1)


def process_character(char: str, only_expr: str | None = None):
    work = os.path.join(WORK_DIR, char)
    out_subdir, prefix = OUTFIT_TARGETS.get(char, (char, f"{char}_default_"))
    out = os.path.join(OUT_DIR, out_subdir)
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
        src = raw_path(work, expr)
        if src is None:
            print(f"  [skip] {char}/{expr}: source not found")
            continue
        img = Image.open(src)
        rgba_by_expr[expr] = transparentize(img)

    if not rgba_by_expr:
        print(f"  [{char}] no sources processed")
        return False

    # 2) shared trim box from idle (fallback: first available)
    ref = rgba_by_expr.get("idle") or next(iter(rgba_by_expr.values()))
    box = alpha_bbox(ref, min_alpha=16)
    if box is None:
        print(f"  [{char}] ERROR: empty foreground in reference")
        return False
    x0, y0, x1, y1 = box
    # padding
    pad = 16
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(ref.width, x1 + pad); y1 = min(ref.height, y1 + pad)
    box = (x0, y0, x1, y1)
    cw, ch = x1 - x0, y1 - y0
    print(f"  [{char}] trim box {box} size {cw}x{ch}")

    # 3) fit trimmed content onto the shared portrait canvas
    scale = min(CANVAS_W / cw, CANVAS_H / ch) if cw and ch else 1.0
    tw, th = max(1, round(cw * scale)), max(1, round(ch * scale))
    ox, oy = (CANVAS_W - tw) // 2, (CANVAS_H - th) // 2

    ok = True
    for expr, rgba_img in rgba_by_expr.items():
        cropped = rgba_img.crop(box)
        resized = cropped.resize((tw, th), Image.LANCZOS)
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        canvas.paste(resized, (ox, oy), resized)
        dst = os.path.join(out, f"{prefix}{expr}.png")
        canvas.save(dst)
        alpha_pct = 100 * (np.asarray(resized)[..., 3] > 10).mean()
        print(f"  [ok] {dst} ({tw}x{th} on {CANVAS_W}x{CANVAS_H}, alpha={alpha_pct:.1f}%)")
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
