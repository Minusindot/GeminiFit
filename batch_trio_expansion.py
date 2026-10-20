"""Generate 2 additional 3-Heroine Joint Special CGs:
1. trio_05_cooking_mealprep.png: Kitchen shared mealprep, chicken breast & sweet potato & avocado
2. trio_06_fireworks_summer.png: Summer night festival, holding sparklers together, glowing smiles
"""
from __future__ import annotations
import sys
import time
import shutil
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from evolve_pool import (
    BASE_DIR,
    FIREFOX_EXE,
    PROFILE_DIR,
    SAME_AS_REF,
    ref_diff,
)
from _browser import big_image_srcs, fetch_image, first_visible_css, wait_new_images

ART_DIR = Path(r"C:\Users\scmms\.gemini\antigravity\brain\acd72411-9330-4563-8940-20997c2e2063")
COMMON_DIR = BASE_DIR / "image" / "00 common"

TRIO_JOBS = [
    # 1. Kitchen Meal Prep
    (
        "trio_05_cooking_mealprep.png",
        "image/00 common/trio_05_cooking_mealprep.png",
        [COMMON_DIR / "dual_inbody.png", COMMON_DIR / "trio_02_cafe_cheer.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "vibrant cell-shaded anime visual novel CG, bright sunny kitchen lighting, cheerful romance slice-of-life atmosphere. "
            "CHARACTERS (Three anime girls together in home kitchen): "
            "1) Gemini (center-left): Raven-black hair with cat ears, wearing a cute pink apron over sporty tee, "
            "holding a spatula grilling golden seasoned chicken breast cubes, tsundere blush. "
            "2) Fujita Kotone (center): Blonde anime girl with twin braids, packing boiled sweet potato slices into a bento lunchbox with a bright beaming smile. "
            "3) Honda Mio (right): Short caramel-brown hair with ahoge, slicing fresh ripe green avocados on a wooden board, laughing playfully: "
            "'Healthy meal prep for our Producer's 52kg diet is ready!'. "
            "Cozy modern bright kitchen, clean wooden counters, square composition. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 2. Summer Fireworks Festival
    (
        "trio_06_fireworks_summer.png",
        "image/00 common/trio_06_fireworks_summer.png",
        [COMMON_DIR / "dual_inbody.png", COMMON_DIR / "trio_04_sunset_victory.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "emotional nighttime festival atmosphere, sparkling handheld sparkler fireworks glowing warm golden light onto faces. "
            "CHARACTERS (Three anime girls standing shoulder-to-shoulder under summer night sky): "
            "1) Gemini: Black hair, cat ears, dark blue floral summer yukata, holding a sparkling sparkler, soft bashful smile looking at viewer. "
            "2) Fujita Kotone: Blonde twin braids, yellow sunflower yukata, holding a glowing lantern, radiant affectionate gaze. "
            "3) Honda Mio: Caramel-brown layered hair, bright orange festival haori, waving her sparkler with a dazzling triumphant smile. "
            "SCENE: Celebrating together on a breezy hilltop overlooking the city summer fireworks, looking at viewer/Producer with deep affection: "
            "'Thank you for training with us all season, Producer! We love you!'. Square composition. Absolutely NO readable letters, NO brand logos."
        )
    )
]

def generate_image(driver, filename, dest_rel, ref_paths, prompt):
    print(f"\n=======================================================")
    print(f"🌟 [합동 CG 생성] {filename}")
    print(f"=======================================================")

    ref_imgs = [Image.open(r) for r in ref_paths if r.exists()]
    driver.get("https://grok.com/imagine")
    time.sleep(3.5)

    prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
    box = first_visible_css(driver, prompt_css, 15)
    if not box:
        driver.get("https://grok.com")
        box = first_visible_css(driver, prompt_css, 20)
    if not box:
        raise RuntimeError("Grok input box not found")

    for r in ref_paths:
        if not r.exists(): continue
        try:
            file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            if not file_inputs: break
            target_input = next((i for i in file_inputs if i.get_attribute("multiple") is not None), file_inputs[0])
            target_input.send_keys(str(r.resolve()))
            time.sleep(2.5)
        except Exception as ex:
            print("Attachment note:", ex)
            break
    time.sleep(2.0)

    before = set(big_image_srcs(driver))
    box = first_visible_css(driver, prompt_css, 10) or box
    box.click()
    time.sleep(0.3)
    box.send_keys(" ".join(prompt.split()))
    box.send_keys(Keys.ENTER)
    print("⏳ Grok CG 렌더링 대기 중...")

    end_time = time.time() + 160
    while time.time() < end_time:
        new_srcs = wait_new_images(driver, before, timeout=35, settle=2.5)
        for src in new_srcs:
            cand = fetch_image(driver, src, "https://grok.com")
            diffs = [ref_diff(cand, r_im) for r_im in ref_imgs]
            min_diff = min(diffs) if diffs else 999.0
            if min_diff < SAME_AS_REF:
                print(f"   [필터] 레퍼런스 재표시 건너뜀 (diff={min_diff:.1f})")
                before.add(src)
                continue

            target_path = BASE_DIR / dest_rel
            target_path.parent.mkdir(parents=True, exist_ok=True)
            cand.save(target_path, format="PNG")
            print(f"✨ [생성 완료] {target_path.relative_to(BASE_DIR)} ({cand.size})")

            art_target = ART_DIR / target_path.name
            shutil.copy2(target_path, art_target)
            return target_path

    raise RuntimeError(f"[{filename}] 생성 타임아웃")

def main():
    lock_file = PROFILE_DIR / "parent.lock"
    if lock_file.exists():
        try: lock_file.unlink()
        except Exception: pass

    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    driver.set_script_timeout(180)

    try:
        for fname, dest_rel, refs, prompt in TRIO_JOBS:
            target_file = BASE_DIR / dest_rel
            if target_file.exists() and target_file.stat().st_size > 50000:
                print(f"Skipping already existing {target_file.name}")
                continue
            try:
                generate_image(driver, fname, dest_rel, refs, prompt)
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Error on {fname}: {e}")
                time.sleep(3)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
