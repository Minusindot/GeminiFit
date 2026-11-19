"""Grok 수렴진화(Convergent Evolution) 3인 히로인(코토네 / 미오 / 제미니) 레퍼런스 풀 & 배치 생성 엔진

폴더 구조:
- `ref_pool/kotone/`           : 코토네(금발 양갈래, 학원마스 후지타 코토네) 생존 풀
- `ref_pool/mio/`              : 미오(캐러멜 브라운 단발, 혼다 미오) 학원마스 화풍 생존 풀
- `ref_pool/gemini/`           : 제미니(신규 오리지널: 애쉬 밀크티 단발+화이트 앞머리 브릿지+네코미미+덧니) 학원마스 화풍 생존 풀
- `ref_pool/reference_mio/`    : 미오 외형 특징만 추출하는 참고 폴더
- `ref_pool/reference_gemini/` : 신규 제미니 외형 특징만 추출하는 참고 폴더
- `ref_pool/gakumas_style/`    : 학원 아이돌마스터(Gakuen Idolmaster) 화풍·채색·빛 번짐·눈동자 밀도 기준 풀
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from datetime import datetime
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from _browser import big_image_srcs, fetch_image, first_visible_css, wait_new_images

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health")
POOL_DIR = BASE_DIR / "image" / "90 repository"
KOTONE_POOL = POOL_DIR / "kotone"
MIO_POOL = POOL_DIR / "mio"
GEMINI_POOL = POOL_DIR / "gemini"
REF_MIO_FEATURE_POOL = POOL_DIR / "reference_mio"
REF_GEMINI_FEATURE_POOL = POOL_DIR / "reference_gemini"
STYLE_POOL = POOL_DIR / "gakumas_style"
SHINY_STYLE_POOL = POOL_DIR / "shiny_style"
SD_CHIBI_POOL = POOL_DIR / "sd_chibi_style"
MORIKINOKO_SD_POOL = POOL_DIR / "morikinoko_sd"
MENT_STYLE_POOL = POOL_DIR / "ment_style"

FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
PROFILE_DIR = BASE_DIR / ".grok_profile"
SAME_AS_REF = 15.0

GLOBAL_NEGATIVE_RULES = (
    "STRICT NEGATIVE CONSTRAINTS (MANDATORY): "
    "ABSOLUTELY NO text, NO letters, NO words, NO typography, NO readable characters, NO subtitles, NO captions, "
    "NO watermarks, NO signatures, NO artist tags, "
    "NO brand logos, NO trademarked emblems, NO corporate insignias (strictly NO Nike swoosh, NO Adidas stripes, NO brand names, NO store signage text). "
    "All clothing, equipment, and background objects must be completely clean, generic, original, and free of any readable writing or brand identity."
)

BASE_STYLE_PROMPT = {
    "kotone": (
        "Strictly follow the exact character design, face proportions, and Gakuen Idolmaster (학원 아이돌마스터) "
        "high-end mobile game illustration style of the attached reference images: "
        "19yo cute anime idol trainer girl Fujita Kotone, soft warm blonde hair in twin braids, "
        "expressive golden-amber jewel-like eyes, cute lively expression with warm coral cheek blush, "
        "ultra-clean delicate fine lineart, luminous soft sunlight rendering, masterpiece 2D bishoujo game event CG, aspect ratio 9:16."
    ),
    "mio": (
        "CRITICAL CHARACTER & STYLE RULE: Strictly maintain the exact official character identity, face structure, "
        "and signature hairstyle of Honda Mio (혼다 미오) from the attached official reference images (07_mio_official_standing & official SSR cards), "
        "rendered in the Gakuen Idolmaster (학원 아이돌마스터) high-end mobile game illustration art style — "
        "ultra-delicate tinted fine lineart, luminous soft porcelain skin with natural peach-coral blush, "
        "detailed multi-tonal honey-amber jewel eyes catching sunlight, airy dynamic lighting and depth of field. "
        "EXACT HONDA MIO CHARACTER TRAITS: 19yo sunshine idol trainer girl, "
        "signature warm caramel-brown short layered bob haircut with distinct outward-flipped feathery hair ends around her neck and ears, "
        "soft textured bangs parted over forehead, delicate ahoge cowlick curl on top of head, "
        "large expressive round golden-amber eyes full of warmth and vitality, radiant infectious smile, "
        "tomboyish yet incredibly charming idol aura, slender toned athletic curves, masterpiece 2D bishoujo game event CG, aspect ratio 9:16."
    ),

    "gemini": (
        "CRITICAL STYLE RULE: Draw strictly in the Gakuen Idolmaster (학원 아이돌마스터) high-end mobile game "
        "illustration art style of the attached style reference images — ultra-delicate fine tinted lineart, "
        "soft luminous porcelain skin rendering with warm coral cheek blush, detailed jewel-like eyes with rich eyelashes, "
        "silky hair strands catching warm golden light, airy depth of field. DO NOT use flat cel-shading! "
        "CHARACTER DESIGN (Gemini): 19yo personal fitness & intermittent fasting coach girl, "
        "very long waist-length silky raven-black hair (흑발 롱헤어), straight blunt-cut bangs (hime cut bangs) "
        "with straight cheek-length sidelocks framing her face, a cute little ahoge strand on top, "
        "and cute fluffy black cat ears (nekomimi) with a tiny ribbon pin. "
        "Slender glamorous idol proportions, masterpiece 2D bishoujo game event CG, aspect ratio 9:16. "
        "CRITICAL NEGATIVE RESTRICTION: ABSOLUTELY DO NOT stick tongue out! Keep mouth naturally closed or smiling/speaking, "
        "and avoid repetitive frontal head tilts. Expressions and camera angles must vary dynamically per scene!"
    ),
}


def list_survivors(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts])


def ref_diff(img_a: Image.Image, img_b: Image.Image) -> float:
    size = (504, 896) if img_a.height >= img_a.width else (896, 504)
    a = np.asarray(img_a.convert("L").resize(size), dtype=float)
    b = np.asarray(img_b.convert("L").resize(size), dtype=float)
    return float(ndimage.gaussian_filter(np.abs(a - b), 3).max())


def pick_evolution_refs(trainer: str) -> list[Path]:
    style_survivors = list_survivors(STYLE_POOL)
    kotone_survivors = list_survivors(KOTONE_POOL)

    if trainer == "kotone":
        if not kotone_survivors:
            raise RuntimeError("ref_pool/kotone 에 살아남은 이미지가 없습니다!")
        chosen = kotone_survivors[:2]
        if style_survivors:
            chosen.append(style_survivors[0])
        return chosen

    if trainer == "mio":
        feature_refs = list_survivors(REF_MIO_FEATURE_POOL)
        standing_ref = [p for p in feature_refs if "07_mio_official_standing" in p.name]
        ssr_refs = [
            p for p in feature_refs
            if "03_mio_ssr" in p.name
            or "04_mio_ssr" in p.name
            or "05_mio_ssr" in p.name
            or "06_mio_ssr" in p.name
            or "10_mio_shine" in p.name
        ]
        chosen: list[Path] = []
        # Always attach official Honda Mio standing sprite for exact facial proportions & hair flips
        if standing_ref:
            chosen.append(standing_ref[0])
        elif feature_refs:
            chosen.append(feature_refs[0])
        # Attach official high-end SSR card for expression & vibrant lighting
        if ssr_refs:
            chosen.append(random.choice(ssr_refs))
        # Attach Gakumas style survivor for mobile game illustration rendering
        if style_survivors:
            chosen.append(style_survivors[0])
        return chosen



    # trainer == "gemini" (신규 흑발 롱헤어 제미니)
    gem_survivors = list_survivors(GEMINI_POOL)
    gem_features = list_survivors(REF_GEMINI_FEATURE_POOL)
    black_ref = [p for p in gem_features if "06_black_hair" in p.name]
    chosen = []
    # Pick clean reference sheet first, avoiding fixed tongue-out poses
    if black_ref:
        chosen.append(black_ref[0])
    if style_survivors:
        chosen.append(style_survivors[0])
    if gem_survivors and len(chosen) < 3:
        # Pick latest non-first survivor or clean pose
        chosen.append(gem_survivors[-1])
    if not chosen:
        if black_ref:
            chosen.append(black_ref[0])
        if style_survivors:
            chosen.append(style_survivors[0])
        if kotone_survivors:
            chosen.append(kotone_survivors[0])
    return chosen


def generate_single_on_driver(driver, trainer: str, tag: str, situation_prompt: str, out_web_file: str | None = None, pool_filename: str | None = None) -> Path:
    refs = pick_evolution_refs(trainer)
    ref_imgs = [Image.open(r) for r in refs]
    full_prompt = f"{BASE_STYLE_PROMPT[trainer]} Scene, Outfit & Pose: {situation_prompt} {GLOBAL_NEGATIVE_RULES}"

    print(f"\n🧬 [{trainer.upper()} | {tag}] 수렴진화 생성 시작 (참조 {len(refs)}장):")
    for r in refs:
        print(f"   📎 {r.relative_to(BASE_DIR)}")

    driver.get("https://grok.com/imagine")
    time.sleep(3.5)
    prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
    box = first_visible_css(driver, prompt_css, 15)
    if not box:
        driver.get("https://grok.com")
        box = first_visible_css(driver, prompt_css, 20)
    if not box:
        raise RuntimeError("Grok 입력창을 찾지 못했습니다.")

    for r in refs:
        try:
            file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            if not file_inputs:
                break
            target_input = next((i for i in file_inputs if i.get_attribute("multiple") is not None), file_inputs[0])
            # webp 등인 경우 png 변환본 사용
            upload_path = r
            if r.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                tmp_png = BASE_DIR / f".tmp_ref_{r.stem}.png"
                Image.open(r).convert("RGB").save(tmp_png)
                upload_path = tmp_png
            target_input.send_keys(str(upload_path.resolve()))
            time.sleep(3.0)
        except Exception as ex:
            print(f"   [첨부 참고] 추가 파일 첨부 생략: {ex}")
            break
    time.sleep(2.5)

    before = set(big_image_srcs(driver))
    box = first_visible_css(driver, prompt_css, 10) or box
    box.click()
    time.sleep(0.3)
    box.send_keys(" ".join(full_prompt.split()))
    box.send_keys(Keys.ENTER)
    print("⏳ Grok 렌더링 대기 중...")

    end_time = time.time() + 150
    while time.time() < end_time:
        new_srcs = wait_new_images(driver, before, timeout=30, settle=2.5)
        for src in new_srcs:
            cand = fetch_image(driver, src, "https://grok.com")
            diffs = [ref_diff(cand, r_im) for r_im in ref_imgs]
            min_diff = min(diffs) if diffs else 999.0
            if min_diff < SAME_AS_REF:
                print(f"   [필터] 첨부 레퍼런스 재표시 건너뜀 (diff={min_diff:.1f})")
                before.add(src)
                continue

            ts = datetime.now().strftime("%m%d_%H%M%S")
            try:
                driver.save_screenshot(str(BASE_DIR / "grok_live_proof.png"))
            except Exception:
                pass
            pool_map = {"kotone": KOTONE_POOL, "mio": MIO_POOL, "gemini": GEMINI_POOL}
            pool_folder = pool_map[trainer]
            pool_folder.mkdir(parents=True, exist_ok=True)
            fname = pool_filename if pool_filename else f"gen_{ts}_{tag}.png"
            new_pool_path = pool_folder / fname
            cand.save(new_pool_path, format="PNG")
            print(f"✨ [진화 완료] {new_pool_path.relative_to(BASE_DIR)} ({cand.size})")

            if out_web_file:
                web_target = BASE_DIR / out_web_file
                cand.save(web_target, format="PNG")
                print(f"🚀 웹앱 파일 저장: {web_target.name}")
            return new_pool_path

    raise RuntimeError(f"[{trainer}:{tag}] 제한 시간 내 이미지 생성 실패")


def run_batch(jobs: list[tuple[str, str, str, str, str]]) -> None:
    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    driver.set_script_timeout(150)
    try:
        for trainer, tag, pool_name, web_out, prompt in jobs:
            try:
                generate_single_on_driver(driver, trainer, tag, prompt, web_out, pool_name)
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ [{trainer}:{tag}] 오류 발생 (다음 작업 계속): {e}")
    finally:
        driver.quit()


def show_status() -> None:
    print("=" * 72)
    print("🧬 [Gemini Fit] 3인 히로인 수렴진화 레퍼런스 풀 현황")
    print("=" * 72)
    for label, folder in [
        ("코토네 생존 풀 (ref_pool/kotone)", KOTONE_POOL),
        ("미오 생존 풀   (ref_pool/mio)", MIO_POOL),
        ("제미니 생존 풀 (ref_pool/gemini - 신규 오리지널)", GEMINI_POOL),
        ("미오 특징 참고 (ref_pool/reference_mio)", REF_MIO_FEATURE_POOL),
        ("제미니 특징 참고 (ref_pool/reference_gemini)", REF_GEMINI_FEATURE_POOL),
        ("학원마스 화풍  (ref_pool/gakumas_style)", STYLE_POOL),
        ("샤니마스 미소녀 (ref_pool/shiny_style)", SHINY_STYLE_POOL),
        ("SD 치비 캐릭터  (ref_pool/sd_chibi_style)", SD_CHIBI_POOL),
        ("모리키노코 SD    (ref_pool/morikinoko_sd)", MORIKINOKO_SD_POOL),
        ("ment 미소녀 화풍 (ref_pool/ment_style)", MENT_STYLE_POOL),
    ]:
        files = list_survivors(folder)
        print(f"\n📂 {label} — {len(files)}장:")
        for f in files:
            with Image.open(f) as im:
                print(f"   ✅ {f.name:<38} ({im.size[0]}x{im.size[1]}, {f.stat().st_size // 1024}KB)")
    print("=" * 72)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--trainer", choices=["kotone", "mio", "gemini"])
    ap.add_argument("--tag", default="event")
    ap.add_argument("--pool-name")
    ap.add_argument("--prompt")
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.status:
        show_status()
        return
    if args.trainer and args.prompt:
        run_batch([(args.trainer, args.tag, args.pool_name, args.out, args.prompt)])
        return
    show_status()


if __name__ == "__main__":
    main()
