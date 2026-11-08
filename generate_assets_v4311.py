#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini Fit v4.3.11 asset batch generator (Grok via Firefox).

Generates, in ONE browser session (resume-safe: skips existing outputs):
  phase bg   : 7 장소 배경  -> image/bg/bg_{name}.png  (16:9 -> 1920x1080 RGB)
  phase base : 캐릭터별 베이스 스탠딩 -> image/_scg_work/{char}/base_raw.png (흰 배경 원본)
  phase expr : 표정 7종 편집 -> image/_scg_work/{char}/{expr}_raw.png (흰 배경 원본)

투명화는 make_scg_transparent.py가 idle 기준 공통 트림으로 일괄 처리한다.

사용 예:
  python generate_assets_v4311.py --phase bg
  python generate_assets_v4311.py --phase base
  python generate_assets_v4311.py --phase expr
  python generate_assets_v4311.py --phase all --timeout 180
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from _browser import first_visible_css, big_image_srcs, wait_new_images, fetch_image

ROOT = Path(__file__).resolve().parent
USER_PROFILE = Path(r"C:\Users\scmms\AppData\Roaming\Mozilla\Firefox\Profiles\hdmyalcf.default-release")
FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
WORK = ROOT / "image" / "_scg_work"
BG_DIR = ROOT / "image" / "bg"

STYLE = ("anime visual novel gal-game art style, soft painterly shading, "
         "high detail, masterpiece quality, matching Genshin-style anime idol game art")

CHARACTERS = {
    "gemini": {
        "desc": ("a beautiful young woman with long straight black hair with blunt straight-cut bangs (hime cut), "
                 "black cat ears with small black ribbon hairpin, violet purple eyes, elegant tall figure, "
                 "wearing black sports bra training top with lavender-purple accents and high-waist black leggings "
                 "with lavender side stripes, full-body standing pose head to shoes, feet and ankles visible, "
                 "standing upright facing viewer, arms relaxed at sides, plain pure white background, no scenery, no room"),
        "refs": [
            ROOT / "image" / "03 gemini" / "avatar_gemini.png",
            ROOT / "image" / "03 gemini" / "gemini_01_main.png",
        ],
    },
    "gemini_menhera": {
        "desc": ("a beautiful young woman with long straight black hair with blunt straight-cut bangs (hime cut), "
                 "black cat ears with small black ribbon hairpin, violet purple eyes with restless tired gaze, "
                 "wearing menhera fashion: oversized black hoodie dress with hanging straps and silver cross chains, "
                 "layered black lace and torn stockings, bandage on one knee, black platform boots, small bandage "
                 "on cheek, full-body standing pose head to shoes, feet and ankles visible, standing upright facing "
                 "viewer, arms relaxed at sides, plain dark gray background, no scenery, no room"),
        "refs": [
            ROOT / "image" / "03 gemini" / "avatar_gemini.png",
        ],
    },
    "kotone": {
        "desc": ("a cheerful young woman with long golden-blonde twin braids and bright amber eyes, "
                 "pop-idol personality, wearing a teal and white zip-up tracksuit jersey with a white inner shirt, "
                 "shorts and white athletic sneakers, full-body standing pose head to shoes, feet and ankles visible, "
                 "standing upright facing viewer, arms relaxed at sides, plain pure white background, no scenery, no room"),
        "refs": [
            ROOT / "image" / "02 kotone" / "avatar_kotone.png",
        ],
    },
    "mio": {
        "desc": ("a sporty energetic young woman with short bob hair and bright amber eyes, "
                 "tomboyish athletic runner personality, wearing a red and white track jacket over "
                 "a sporty tank top, running shorts and running shoes"),
        "refs": [
            ROOT / "image" / "01 mio" / "avatar_mio.png",
            ROOT / "image" / "01 mio" / "mio_01_main.png",
        ],
    },
}

# idle은 base를 복사한다(별도 생성 없음). 표정만 바꿔 7종 편집 생성. (v4.3.17: 14종 확장)
EXPRESSIONS = {
    "idle": "calm gentle expression, soft relaxed smile, eyes looking slightly downward, serene",
    "smile": "bright cheerful smile, eyes sparkling with joy, mouth open happily",
    "sad": "worried sad expression, drooping eyebrows, small pout, melancholic eyes",
    "angry": "cute angry tsundere pout, puffed cheeks, furrowed brows, slightly shouting",
    "shy": "shy blushing expression, flushed red cheeks, embarrassed awkward smile, eyes averted",
    "shock": "shocked surprised expression, wide round eyes, open mouth, flustered",
    "dark": "cool serious dark expression, shadowed eyes without highlights, emotionless cold stare",
    "joke": "playful mischievous wink, tongue sticking out slightly, cheeky grin",
    "wink": "bright cheerful wink with one eye closed, energetic encouragement smile, pointing finger pose",
    "pout": "cute sulking pout, puffed cheeks, lower lip pushed out, grumpy but adorable",
    "cry": "teary sad expression, watery eyes about to cry, quivering lower lip, trembling eyebrows",
    "smirk": "confident smug smirk, one eyebrow raised, half-lidded amused eyes, fourth-wall-breaking grin",
    "love": "adoring loving expression, dreamy sparkling heart-shaped eyes, hands clasped together, gentle fawning smile",
    "sleepy": "sleepy tired expression, half-closed droopy eyes, small yawn, relaxed drowsy mood",
}

BACKGROUNDS = [
    ("teahouse_day", "empty Kyoto tatami tea house interior daytime, warm sunlight through shoji paper windows, "
     "low wooden tea table with matcha bowl and teapot, hanging calligraphy scroll, tatami floor, no people"),
    ("teahouse_night", "empty Kyoto tatami tea house interior at night, glowing paper lanterns, moonlight through shoji, "
     "low tea table with candle light, moody quiet atmosphere, no people"),
    ("osaka_street", "lively Osaka shopping street daytime, neon signs, takoyaki shop awnings, "
     "Dotonbori canal in the distance, crowded summer streets, no people"),
    ("ryokan_room", "Japanese ryokan room with futon beds and tatami, wooden balcony overlooking a garden, "
     "soft evening light, open-air onsen steam in the distance, no people"),
    ("gym_indoor", "modern fitness gym interior, dumbbell racks, squat racks and treadmills, "
     "large windows with evening sunlight, clean sports facility, no people"),
    ("park_track", "public park running path in the morning, cherry trees along a paved jogging track, "
     "soft spring sunlight, benches and greenery, no people"),
    ("bookstore", "quiet old bookstore interior, tall wooden bookshelves filled with books, "
     "sunlight through dusty windows, reading desk, no people"),
]


def make_profile() -> Path:
    work_profile = ROOT / ".grok_profile"
    work_profile.mkdir(parents=True, exist_ok=True)
    for fname in ["cookies.sqlite", "key4.db", "cert9.db", "logins.json", "permissions.sqlite"]:
        src = USER_PROFILE / fname
        if src.exists():
            try:
                shutil.copy2(src, work_profile / fname)
            except Exception:
                pass
    storage_src = USER_PROFILE / "storage"
    storage_dst = work_profile / "storage"
    if storage_src.exists() and not storage_dst.exists():
        try:
            shutil.copytree(storage_src, storage_dst, ignore=shutil.ignore_patterns("cache", "Cache", "tmp"))
        except Exception:
            pass
    return work_profile


def attach_files(driver, paths: list[Path]) -> None:
    file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
    if not file_inputs:
        print("[attach] 파일 입력 없음, 계속 진행", flush=True)
        return
    valid = [str(p) for p in paths if p.exists()]
    if not valid:
        return
    target = next((i for i in file_inputs if i.get_attribute("multiple") is not None), file_inputs[0])
    if len(valid) > 1 and target.get_attribute("multiple") is None:
        # multiple 속성을 안 받는 input이면 한 장씩 넣는다
        for f in valid:
            try:
                target.send_keys(f)
                print(f"[attach] {Path(f).name} 첨부", flush=True)
                time.sleep(4)
            except Exception as e:
                print(f"[attach] 예외({f}): {e}", flush=True)
    else:
        try:
            target.send_keys("\n".join(valid))
            print(f"[attach] 참고 이미지 {len(valid)}장 첨부", flush=True)
            time.sleep(5)
        except Exception as e:
            print(f"[attach] 예외: {e}", flush=True)


def crop_16x9(img: Image.Image) -> Image.Image:
    w, h = img.size
    r = 16 / 9
    if w / h > r:
        cw = round(h * r)
        x0 = (w - cw) // 2
        img = img.crop((x0, 0, x0 + cw, h))
    else:
        ch = round(w / r)
        y0 = (h - ch) // 2
        img = img.crop((0, y0, w, y0 + ch))
    return img.resize((1920, 1080), Image.LANCZOS)


IMAGINE_HOME = "https://grok.com"


def gen_one(driver, prompt: str, out_path: Path, refs: list[Path], timeout: int, kind: str) -> bool:
    """프롬프트를 보내고 생성된 이미지를 저장한다.
    주의: Grok은 첨부한 참고 이미지를 재호스팅해 결과와 함께 돌려주곤 한다 → _ref_diff로 필터링."""
    from grok_browser import _ref_diff, SAME_AS_REF

    prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
    box = first_visible_css(driver, prompt_css, 15)
    if not box:
        driver.get(IMAGINE_HOME)
        box = first_visible_css(driver, prompt_css, 20)
    if not box:
        print("[err] 입력창 없음", flush=True)
        return False
    attach_files(driver, refs)
    ref_imgs = [Image.open(r) for r in refs if r.exists()]
    box = first_visible_css(driver, prompt_css, 10) or box
    text = " ".join(f"{prompt} (aspect ratio {kind})".split())
    before = set(big_image_srcs(driver))
    box.click()
    box.send_keys(text)
    box.send_keys(Keys.ENTER)
    print(f"[gen] {out_path.name} 전송됨, 생성 대기...", flush=True)

    end = time.time() + timeout
    filtered = []  # 참고 그림으로 판정해 걸러낸 것들(점수, 이미지) - 판정이 틀렸을 때의 안전망
    while True:
        wait = int(end - time.time()) if not filtered else min(45, int(end - time.time()))
        new = wait_new_images(driver, before, max(5, wait))
        if not new:
            if filtered:
                score, img = max(filtered, key=lambda t: t[0])
                if score > 5:
                    print(f"[warn] {out_path.name}: 새 결과 부족 → 참고본과 가장 다른 이미지(차이 {score:.0f})를 씁니다 - 꼭 확인할 것", flush=True)
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    if kind == "16:9 landscape":
                        img = crop_16x9(img).convert("RGB")
                    img.save(out_path, format="PNG")
                    print(f"[ok] {out_path} ({img.size[0]}x{img.size[1]})", flush=True)
                    time.sleep(2)
                    return True
            print(f"[err] 시간 초과: {out_path.name}", flush=True)
            return False
        results = []
        for src in new:
            got = fetch_image(driver, src, IMAGINE_HOME)
            scores = [_ref_diff(got, r) for r in ref_imgs]
            if scores and min(scores) < SAME_AS_REF:
                before.add(src)  # 첨부한 참고가 다시 뜬 것 - 결과 아님
                filtered.append((min(scores), got))
            else:
                results.append(got)
        if results:
            img = results[0]
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if kind == "16:9 landscape":
                img = crop_16x9(img).convert("RGB")
            img.save(out_path, format="PNG")
            print(f"[ok] {out_path} ({img.size[0]}x{img.size[1]})", flush=True)
            time.sleep(2)
            return True
        if time.time() >= end:
            print(f"[err] 새로 생성된 이미지가 나오지 않음: {out_path.name}", flush=True)
            return False


ECGS = [
    ("gemini_46_menhera_night", "03 gemini",
     "same anime girl with long straight black hair with blunt straight-cut bangs and black cat ears, "
     "menhera fashion: oversized black hoodie dress with straps and cross chains, bandaged knee, "
     "in a dark messy bedroom at night lit only by phone screen glow, dark cinematic event CG, vertical portrait"),
    ("gemini_47_menhera_rooftop", "03 gemini",
     "same anime girl with long straight black hair with blunt straight-cut bangs and black cat ears, "
     "menhera fashion: oversized black hoodie dress with straps and cross chains, bandaged knee, "
     "standing on city rooftop at midnight under neon signs and cloudy sky, dark cinematic event CG, vertical portrait"),
]


def build_jobs(phase: str):
    jobs = []  # (label, prompt, out_path, refs, kind)
    if phase in ("bg", "all"):
        for name, desc in BACKGROUNDS:
            prompt = f"{STYLE}, wide anime visual novel background art, {desc}, empty scene, painterly, landscape orientation"
            jobs.append((f"bg_{name}", prompt, BG_DIR / f"bg_{name}.png", [], "16:9 landscape"))
    if phase in ("base", "all"):
        for char, info in CHARACTERS.items():
            prompt = (f"{STYLE}, standing character sprite, {info['desc']}, full body standing pose "
                      f"facing viewer, arms relaxed at sides, plain pure white background, "
                      f"entire body head to toe fully visible, portrait orientation")
            jobs.append((f"{char}/base", prompt, WORK / char / "base_raw.png", info["refs"], "9:16 portrait"))
    if phase in ("expr", "all"):
        for char, info in CHARACTERS.items():
            for expr, edesc in EXPRESSIONS.items():
                if expr == "idle":
                    continue
                prompt = (f"Keep the EXACT same character in the reference image, same body, same outfit, "
                          f"same pose, same plain pure white background and same full-body framing. "
                          f"Only change her facial expression to: {edesc}. "
                          f"{info['desc']}, {STYLE}")
                jobs.append((f"{char}/{expr}", prompt, WORK / char / f"{expr}_raw.png",
                             [WORK / char / "base_raw.png"], "9:16 portrait"))
    if phase in ("ecg",):
        for name, folder, desc in ECGS:
            prompt = (f"{STYLE}, anime visual novel event CG illustration, {desc}, detailed background")
            jobs.append((name, prompt, ROOT / "image" / folder / f"{name}.png",
                         [ROOT / "image" / "03 gemini" / "avatar_gemini.png"], "9:16 portrait"))
    return jobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["bg", "base", "expr", "ecg", "all"], default="all")
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    for d in [WORK / c for c in CHARACTERS]:
        d.mkdir(parents=True, exist_ok=True)
    jobs = build_jobs(args.phase)
    print(f"[plan] {len(jobs)} jobs (phase={args.phase}), 기존 파일은 건너뜁니다.", flush=True)
    for label, prompt, out_path, refs, kind in jobs:
        if out_path.exists():
            print(f"[skip] {label} 이미 존재", flush=True)
    if not USER_PROFILE.exists():
        sys.exit("[err] Firefox 프로필을 찾지 못했습니다: " + str(USER_PROFILE))

    profile_dir = make_profile()
    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(profile_dir))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    driver.set_script_timeout(120)
    try:
        driver.get("https://grok.com/imagine")
        time.sleep(3)
        failed = 0
        for label, prompt, out_path, refs, kind in jobs:
            if out_path.exists():
                continue
            refs_ok = [r for r in refs if r.exists()]
            if refs and not refs_ok:
                print(f"[skip] {label}: 참고 이미지 없음 {refs}", flush=True)
                continue
            ok = gen_one(driver, prompt, out_path, refs_ok, args.timeout, kind)
            if not ok:
                failed += 1
                # 다음 잡을 위해 채팅 화면 새로고침
                driver.get("https://grok.com/imagine")
                time.sleep(3)
        print(f"===== 완료: 실패 {failed}건 =====", flush=True)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
