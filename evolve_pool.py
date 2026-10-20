"""Grok 수렴진화(Convergent Evolution) 일러스트 생성 & 레퍼런스 풀(ref_pool) 관리 엔진

원리:
1. 사용자가 `ref_pool/gemini/`, `ref_pool/mio/`, `ref_pool/gakumas_style/` 폴더에서
   마음에 안 드는 이미지를 탐색기에서 그냥 삭제(Delete)합니다.
2. 이 스크립트는 폴더에 **살아남은(생존한) 이미지들만** 스캔하여 Grok에 멀티 레퍼런스로 첨부합니다.
3. 새로 생성된 이미지는:
   - 첨부한 원본 레퍼런스와 픽셀 유사도(`_ref_diff < 15`)를 비교해 원본 재표시를 100% 걸러냅니다.
   - `ref_pool/<trainer>/` 폴더 안에 새 세대 파일로 저장되어 다음 진화의 부모 후보가 되며,
     마음에 안 들면 언제든 폴더에서 지워 도태시킬 수 있습니다.

사용법:
  python evolve_pool.py --status
    -> 현재 살아남은 레퍼런스 풀 목록 및 웹앱 연결 상태 확인
  python evolve_pool.py --sync
    -> 사용자가 ref_pool에서 삭제(도태)시킨 이미지가 있으면, 살아남은 최상위 이미지로 웹앱 슬롯 동기화
  python evolve_pool.py --trainer gemini --tag morning --prompt "stretching in sunlit room..." --out gemini_morning.png
    -> 살아남은 ref_pool/gemini + ref_pool/gakumas_style 이미지를 참조해 새 일러스트 진화 생성
"""
from __future__ import annotations

import argparse
import random
import shutil
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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

BASE_DIR = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health")
POOL_DIR = BASE_DIR / "ref_pool"
GEMINI_POOL = POOL_DIR / "gemini"
MIO_POOL = POOL_DIR / "mio"
STYLE_POOL = POOL_DIR / "gakumas_style"

FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
PROFILE_DIR = BASE_DIR / ".grok_profile"
SAME_AS_REF = 15.0  # 이 값 미만이면 Grok이 첨부 이미지를 그대로 화면에 표시한 것으로 판정해 무시함

# 웹앱(index.html) 슬롯과 ref_pool 초기 시드 매핑
SLOT_MAPPING = {
    "trainer_gemini.png": ("gemini", "01_gemini_mint_tracksuit.png"),
    "gemini_morning.png": ("gemini", "02_gemini_morning_sunlight.png"),
    "gemini_tea_matcha.png": ("gemini", "03_gemini_matcha_tea.png"),
    "gemini_evening.png": ("gemini", "04_gemini_evening_window.png"),
    "trainer_cafe.png": ("gemini", "05_gemini_home_cafe.png"),
    "trainer_mio.png": ("mio", "01_mio_sunlight_track.png"),
}

BASE_STYLE_PROMPT = {
    "gemini": (
        "Strictly follow the exact character design, face proportions, and Gakuen Idolmaster (학원 아이돌마스터) "
        "high-end anime illustration style of the attached reference images: "
        "19yo cute anime fitness trainer girl Gemini, soft warm blonde hair in twin braids, "
        "expressive golden-amber eyes, charming slightly tsundere yet caring expression, "
        "ultra-clean delicate lineart, luminous skin shading with soft coral blush, "
        "airy warm sunlight, slender athletic idol proportions, masterpiece 2D mobile game card art, aspect ratio 9:16."
    ),
    "mio": (
        "Strictly follow the exact character design, face proportions, and Gakuen Idolmaster (학원 아이돌마스터) "
        "high-end anime illustration style of the attached reference images: "
        "19yo cheerful anime fitness trainer girl Honda Mio, short layered warm caramel-brown hair with cute side bangs, "
        "bright amber eyes, radiant energetic smile, ultra-clean delicate lineart, "
        "luminous skin shading with warm sunlight (komorebi), masterpiece 2D mobile game card art, aspect ratio 9:16."
    ),
}


def list_survivors(folder: Path) -> list[Path]:
    """폴더 내에서 사용자가 삭제하지 않고 남겨둔(살아남은) 이미지 목록을 반환합니다."""
    if not folder.exists():
        return []
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts])


def ref_diff(img_a: Image.Image, img_b: Image.Image) -> float:
    """두 이미지의 블러 후 최대 픽셀 차이를 계산합니다 (원본 레퍼런스 재표시 필터링용)."""
    size = (504, 896) if img_a.height >= img_a.width else (896, 504)
    a = np.asarray(img_a.convert("L").resize(size), dtype=float)
    b = np.asarray(img_b.convert("L").resize(size), dtype=float)
    return float(ndimage.gaussian_filter(np.abs(a - b), 3).max())


def pick_evolution_refs(trainer: str, max_char_refs: int = 2, include_style: bool = True) -> list[Path]:
    """살아남은 캐릭터 레퍼런스 풀 + 학원 아이돌마스터 화풍 풀에서 최적의 참조 이미지를 선택합니다."""
    char_folder = GEMINI_POOL if trainer == "gemini" else MIO_POOL
    survivors = list_survivors(char_folder)
    if not survivors:
        raise RuntimeError(f"[{trainer}] 레퍼런스 풀({char_folder})에 살아남은 이미지가 없습니다! 최소 1장을 남겨주세요.")

    # 01_, 02_ 등 번호가 앞선 핵심 시드 1장 + 나머지 생존자 중 1장 조합으로 일관성과 진화 다양성을 동시에 확보
    if len(survivors) <= max_char_refs:
        chosen = list(survivors)
    else:
        anchor = survivors[0]
        others = random.sample(survivors[1:], k=max_char_refs - 1)
        chosen = [anchor] + others

    if include_style:
        style_survivors = list_survivors(STYLE_POOL)
        if style_survivors:
            chosen.append(random.choice(style_survivors))

    return chosen


def show_status() -> None:
    print("=" * 68)
    print("🧬 [Gemini Fit] 수렴진화 레퍼런스 풀 (ref_pool) 생존 현황")
    print("=" * 68)
    for label, folder in [
        ("제미니 (ref_pool/gemini)", GEMINI_POOL),
        ("미오   (ref_pool/mio)", MIO_POOL),
        ("화풍   (ref_pool/gakumas_style)", STYLE_POOL),
    ]:
        files = list_survivors(folder)
        print(f"\n📂 {label} — 생존 이미지 {len(files)}장:")
        for f in files:
            with Image.open(f) as im:
                print(f"   ✅ {f.name:<38} ({im.size[0]}x{im.size[1]}, {f.stat().st_size // 1024}KB)")

    print("\n" + "-" * 68)
    print("🔗 웹앱(index.html) 슬롯 연결 상태:")
    for web_file, (trainer, pool_name) in SLOT_MAPPING.items():
        pool_folder = GEMINI_POOL if trainer == "gemini" else MIO_POOL
        pool_file = pool_folder / pool_name
        status = "🟢 정상 유지됨" if pool_file.exists() else "🔴 사용자가 삭제함 (--sync 실행 시 대체됨)"
        print(f"   • {web_file:<24} <- {pool_name:<34} : {status}")
    print("=" * 68)


def sync_from_pool() -> None:
    """사용자가 ref_pool에서 삭제(도태)시킨 이미지가 있으면 살아남은 최상위 이미지로 웹앱 슬롯을 자동 대체합니다."""
    changed = False
    for web_file, (trainer, pool_name) in SLOT_MAPPING.items():
        pool_folder = GEMINI_POOL if trainer == "gemini" else MIO_POOL
        pool_file = pool_folder / pool_name
        target_path = BASE_DIR / web_file
        if pool_file.exists():
            continue
        survivors = list_survivors(pool_folder)
        if not survivors:
            print(f"⚠️ [{trainer}] 폴더에 남은 이미지가 없어 {web_file} 대체 불가")
            continue
        replacement = survivors[0]
        shutil.copy2(replacement, target_path)
        print(f"♻️ [도태 감지] 삭제된 '{pool_name}' 대신 생존 1순위 '{replacement.name}' -> '{web_file}' 적용 완료!")
        changed = True
    if not changed:
        print("✅ 모든 웹앱 슬롯 이미지가 ref_pool 내에서 정상 생존 중입니다.")


def evolve_generate(trainer: str, tag: str, situation_prompt: str, out_web_file: str | None = None) -> Path:
    """살아남은 레퍼런스 풀 이미지를 Grok에 첨부하여 진화된 새 일러스트를 생성하고 풀에 추가합니다."""
    refs = pick_evolution_refs(trainer, max_char_refs=2, include_style=True)
    ref_imgs = [Image.open(r) for r in refs]
    full_prompt = f"{BASE_STYLE_PROMPT[trainer]} Scene & Action: {situation_prompt}"

    print(f"🧬 [{trainer.upper()}] 수렴진화 생성 시작 (참조 생존 이미지 {len(refs)}장):")
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

                # 진짜 새로 진화 생성된 이미지 저장!
                ts = datetime.now().strftime("%m%d_%H%M%S")
                try:
                    driver.save_screenshot(str(BASE_DIR / "grok_live_proof.png"))
                except Exception:
                    pass
                pool_folder = GEMINI_POOL if trainer == "gemini" else MIO_POOL
                new_pool_path = pool_folder / f"gen_{ts}_{tag}.png"
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
    ap.add_argument("--sync", action="store_true", help="폴더에서 삭제된 이미지를 감지해 생존 이미지로 웹앱 동기화")
    ap.add_argument("--trainer", choices=["gemini", "mio"], help="진화 생성할 트레이너 선택")
    ap.add_argument("--tag", default="event", help="새로 생성될 풀 파일 태그 (예: morning, workout, cafe)")
    ap.add_argument("--prompt", help="상황/포즈 프롬프트 (화풍 및 캐릭터 고정 프롬프트는 자동 결합됨)")
    ap.add_argument("--out", help="웹앱에 바로 덮어쓸 파일명 (예: gemini_morning.png)")
    args = ap.parse_args()

    if args.status:
        show_status()
        return
    if args.sync:
        sync_from_pool()
        return
    if args.trainer and args.prompt:
        evolve_generate(args.trainer, args.tag, args.prompt, args.out)
        return
    show_status()


if __name__ == "__main__":
    main()
