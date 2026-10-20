"""Grok 수렴진화(Convergent Evolution) 일러스트 생성 & 레퍼런스 풀(ref_pool) 관리 엔진

구조:
- `ref_pool/gemini/`        : 제미니 생존 일러스트 풀 (화풍 + 캐릭터 동시 참조)
- `ref_pool/mio/`           : 학원 아이돌마스터 화풍으로 진화 완료된 미오 생존 풀
- `ref_pool/reference_mio/` : 미오의 외형 특징(머리 모양, 머리색, 눈동자, 쾌활한 인상)만 따올 원본 참고 폴더
                              (절대 이 폴더의 옛날 셀 애니메이션 그림체를 따라 그리지 않고 특징만 추출!)
- `ref_pool/gakumas_style/` : 학원 아이돌마스터(Gakuen Idolmaster) 화풍·채색·빛 번짐·눈동자 묘사 기준 풀
"""
from __future__ import annotations

import argparse
import random
import shutil
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
POOL_DIR = BASE_DIR / "ref_pool"
GEMINI_POOL = POOL_DIR / "gemini"
MIO_POOL = POOL_DIR / "mio"
REF_MIO_FEATURE_POOL = POOL_DIR / "reference_mio"
STYLE_POOL = POOL_DIR / "gakumas_style"

FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
PROFILE_DIR = BASE_DIR / ".grok_profile"
SAME_AS_REF = 15.0  # 이 값 미만이면 Grok이 첨부 이미지를 그대로 화면에 표시한 것으로 판정해 무시함

SLOT_MAPPING = {
    "trainer_gemini.png": ("gemini", "01_gemini_main_studio.png"),
    "gemini_morning.png": ("gemini", "02_gemini_morning_sunlight.png"),
    "gemini_tea_matcha.png": ("gemini", "03_gemini_matcha_tea.png"),
    "gemini_evening.png": ("gemini", "04_gemini_evening_window.png"),
    "trainer_cafe.png": ("gemini", "05_gemini_home_cafe.png"),
    "trainer_mio.png": ("mio", "01_mio_gakumas_main.png"),
}

BASE_STYLE_PROMPT = {
    "gemini": (
        "Strictly follow the exact character design, face proportions, and Gakuen Idolmaster (학원 아이돌마스터) "
        "high-end anime illustration style of the attached reference images: "
        "19yo cute anime fitness trainer girl Gemini, soft warm blonde hair in twin braids, "
        "expressive golden-amber jewel-like eyes, charming slightly tsundere yet sweet expression, "
        "ultra-clean delicate fine lineart, luminous skin shading with soft coral blush, "
        "airy warm golden sunlight, masterpiece 2D mobile game card art, aspect ratio 9:16."
    ),
    "mio": (
        "CRITICAL STYLE INSTRUCTION: Draw strictly in the Gakuen Idolmaster (학원 아이돌마스터) high-end mobile game "
        "illustration art style of the attached style reference images — ultra-delicate fine brown/tinted lineart, "
        "soft luminous skin rendering with warm coral cheek blush, detailed jewel-like amber eyes with fine eyelashes, "
        "silky hair strands catching warm golden sunlight, airy depth of field. "
        "DO NOT copy the flat TV anime cel-shading or thick outlines of the character sheet! "
        "CHARACTER TRAITS ONLY from Honda Mio reference: 19yo cheerful idol trainer girl, short layered warm caramel-brown "
        "hair with cute playful side-swept bangs and fluffy outward-flipped hair tips, bright golden-amber eyes, "
        "radiant energetic sweet smile, wearing stylish yellow, white, and pastel-orange sporty track jacket, aspect ratio 9:16."
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
    """트레이너별 참조 이미지 조합을 선택합니다.
    - gemini: ref_pool/gemini 생존본 2장 + ref_pool/gakumas_style 1장
    - mio:
      * ref_pool/mio에 진화된 학원마스풍 미오가 있으면 그 생존본 우선 사용 + gakumas_style
      * ref_pool/mio가 비어 있으면 gakumas_style 2장(화풍 강제 고정) + reference_mio 1장(캐릭터 특징만 참조)
    """
    style_survivors = list_survivors(STYLE_POOL)
    if trainer == "gemini":
        survivors = list_survivors(GEMINI_POOL)
        if not survivors:
            raise RuntimeError(f"ref_pool/gemini 에 살아남은 이미지가 없습니다!")
        chosen = survivors[:2] if len(survivors) <= 2 else [survivors[0], random.choice(survivors[1:])]
        if style_survivors:
            chosen.append(style_survivors[0])
        return chosen

    # trainer == "mio"
    mio_survivors = list_survivors(MIO_POOL)
    feature_refs = list_survivors(REF_MIO_FEATURE_POOL)
    chosen: list[Path] = []

    if mio_survivors:
        # 이미 학원마스 화풍으로 진화해 살아남은 미오가 있을 때
        chosen.extend(mio_survivors[:2])
        if style_survivors:
            chosen.append(style_survivors[0])
    else:
        # 화풍은 gakumas_style에서 강하게 고정하고, reference_mio에서는 원본 캐릭터 시트(02_mio_original_ref) 1장만 특징용으로 첨부
        if style_survivors:
            chosen.extend(style_survivors[:2])
        gemini_survivors = list_survivors(GEMINI_POOL)
        if gemini_survivors and len(chosen) < 2:
            chosen.append(gemini_survivors[0])
        if feature_refs:
            # 02_mio_original_ref.png (또는 가장 마지막 원본 특징 이미지) 선택
            orig_pref = [p for p in feature_refs if "original" in p.name.lower() or "02" in p.name]
            chosen.append(orig_pref[0] if orig_pref else feature_refs[-1])

    if not chosen:
        raise RuntimeError("미오 생성을 위한 레퍼런스 이미지가 없습니다.")
    return chosen


def show_status() -> None:
    print("=" * 72)
    print("🧬 [Gemini Fit] 수렴진화 레퍼런스 풀 (ref_pool) 생존 현황")
    print("=" * 72)
    for label, folder in [
        ("제미니 생존 풀 (ref_pool/gemini)", GEMINI_POOL),
        ("미오 생존 풀   (ref_pool/mio - 학원마스 화풍 진화본)", MIO_POOL),
        ("미오 특징 참고 (ref_pool/reference_mio - 외형 특징만 추출)", REF_MIO_FEATURE_POOL),
        ("학원마스 화풍  (ref_pool/gakumas_style - 그림체/채색 기준)", STYLE_POOL),
    ]:
        files = list_survivors(folder)
        print(f"\n📂 {label} — {len(files)}장:")
        for f in files:
            with Image.open(f) as im:
                print(f"   ✅ {f.name:<38} ({im.size[0]}x{im.size[1]}, {f.stat().st_size // 1024}KB)")

    print("\n" + "-" * 72)
    print("🔗 웹앱(index.html) 슬롯 연결 상태:")
    for web_file, (trainer, pool_name) in SLOT_MAPPING.items():
        pool_folder = GEMINI_POOL if trainer == "gemini" else MIO_POOL
        pool_file = pool_folder / pool_name
        status = "🟢 정상 유지됨" if pool_file.exists() else "🔴 비어있음/도태됨 (새로 진화 생성 필요)"
        print(f"   • {web_file:<24} <- {pool_name:<34} : {status}")
    print("=" * 72)


def evolve_generate(trainer: str, tag: str, situation_prompt: str, out_web_file: str | None = None, pool_filename: str | None = None) -> Path:
    refs = pick_evolution_refs(trainer)
    ref_imgs = [Image.open(r) for r in refs]
    full_prompt = f"{BASE_STYLE_PROMPT[trainer]} Scene & Pose: {situation_prompt}"

    print(f"🧬 [{trainer.upper()}] 수렴진화 생성 시작 (참조 이미지 {len(refs)}장):")
    for r in refs:
        print(f"   📎 {r.relative_to(BASE_DIR)}")

    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    driver.set_script_timeout(150)

    try:
        driver.get("https://grok.com/imagine")
        time.sleep(4)
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
                target_input.send_keys(str(r.resolve()))
                time.sleep(3.5)
            except Exception as ex:
                print(f"   [첨부 참고] 추가 파일 첨부 생략: {ex}")
                break
        time.sleep(3)

        before = set(big_image_srcs(driver))
        box = first_visible_css(driver, prompt_css, 10) or box
        box.click()
        time.sleep(0.4)
        box.send_keys(" ".join(full_prompt.split()))
        box.send_keys(Keys.ENTER)
        print("⏳ Grok 생성 대기 중 (첨부 원본 에코 자동 필터링 활성)...")

        end_time = time.time() + 150
        while time.time() < end_time:
            new_srcs = wait_new_images(driver, before, timeout=30, settle=2.5)
            for src in new_srcs:
                cand = fetch_image(driver, src, "https://grok.com")
                diffs = [ref_diff(cand, r_im) for r_im in ref_imgs]
                min_diff = min(diffs) if diffs else 999.0
                if min_diff < SAME_AS_REF:
                    print(f"   [필터] 첨부 레퍼런스 재표시 이미지 건너뜀 (diff={min_diff:.1f})")
                    before.add(src)
                    continue

                ts = datetime.now().strftime("%m%d_%H%M%S")
                try:
                    driver.save_screenshot(str(BASE_DIR / "grok_live_proof.png"))
                except Exception:
                    pass
                pool_folder = GEMINI_POOL if trainer == "gemini" else MIO_POOL
                pool_folder.mkdir(parents=True, exist_ok=True)
                fname = pool_filename if pool_filename else f"gen_{ts}_{tag}.png"
                new_pool_path = pool_folder / fname
                cand.save(new_pool_path, format="PNG")
                print(f"✨ [진화 성공] 레퍼런스 풀 저장 완료: {new_pool_path.relative_to(BASE_DIR)} ({cand.size})")

                if out_web_file:
                    web_target = BASE_DIR / out_web_file
                    cand.save(web_target, format="PNG")
                    print(f"🚀 웹앱 슬롯 즉시 반영 완료: {web_target.name}")
                return new_pool_path

        raise RuntimeError("제한 시간 내에 새로운 진화 이미지를 받지 못했습니다.")
    finally:
        driver.quit()


def main() -> None:
    ap = argparse.ArgumentParser(description="Grok 수렴진화 레퍼런스 풀 관리 및 생성기")
    ap.add_argument("--status", action="store_true", help="현재 살아남은 레퍼런스 풀 현황 출력")
    ap.add_argument("--trainer", choices=["gemini", "mio"], help="진화 생성할 트레이너 선택")
    ap.add_argument("--tag", default="event", help="새로 생성될 풀 파일 태그")
    ap.add_argument("--pool-name", help="ref_pool 내에 저장할 지정 파일명")
    ap.add_argument("--prompt", help="상황/포즈 프롬프트")
    ap.add_argument("--out", help="웹앱에 바로 덮어쓸 파일명")
    args = ap.parse_args()

    if args.status:
        show_status()
        return
    if args.trainer and args.prompt:
        evolve_generate(args.trainer, args.tag, args.prompt, args.out, args.pool_name)
        return
    show_status()


if __name__ == "__main__":
    main()
