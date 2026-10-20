"""Generate Gemini CG expansion:
1. gemini_21_cable_row.png: Seated cable row, back line, focused look
2. gemini_22_plank_challenge.png: 2-minute elbow plank, intense eye-contact & sweat
3. gemini_23_night_rooftop_hoodie.png: Post-night-run windy rooftop, sporty zip hoodie & warm canned tea
4. gemini_24_kettlebell_swing.png: Kettlebell swing hip hinge, dynamic athletic posture
5. gemini_25_post_workout_smoothie.png: Juice bar tall stool, blueberry smoothie, bashful tsundere gaze
6. sd_gemini_03_plank_shiver.png: Morikinoko 2-head-tall SD plank vibration comedy meltdown
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
REPO_DIR = BASE_DIR / "image" / "90 repository"
SD_POOL = REPO_DIR / "morikinoko_sd"

JOBS = [
    # 1. Gemini 21: Cable Row Back Line
    (
        "gemini_21_cable_row.png",
        "image/03 gemini/gemini_21_cable_row.png",
        [REPO_DIR / "reference_gemini" / "06_black_hair_ref.png", REPO_DIR / "gemini" / "06_gemini_mirror_stretch.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "vibrant cell-shaded anime visual novel CG, cinematic gym studio rim lighting, clean delicate lineart. "
            "CHARACTER (Gemini): 19-year-old Japanese anime girl, glossy raven-black long hair tied in low side bunches, "
            "cute black cat ears with soft inner fur, striking crimson-amber eyes, straight bangs, tsundere personality. "
            "SCENE & POSE: Seated cable row machine in modern fitness gym, camera viewed from three-quarter back angle showcasing "
            "her beautifully toned scapula and back muscles pulling the V-bar cable tight to her abdomen, "
            "turning head back over shoulder with a confident, fierce tsundere smirk: 'Watch closely, Producer! This is how you build a toned posture!'. "
            "Wearing sleek black-and-purple sports bra and high-waisted tights. Absolutely NO text, NO brand logos, NO tongue out."
        )
    ),
    # 2. Gemini 22: Plank Challenge
    (
        "gemini_22_plank_challenge.png",
        "image/03 gemini/gemini_22_plank_challenge.png",
        [REPO_DIR / "reference_gemini" / "06_black_hair_ref.png", REPO_DIR / "gemini" / "01_gemini_main.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "vibrant cell-shaded anime art, low-angle dynamic POV, gorgeous atmospheric gym floor lighting. "
            "CHARACTER (Gemini): Raven-black hair, black cat ears, amber eyes. "
            "SCENE & POSE: Face-to-face elbow plank challenge on a black gym mat! Low camera looking directly into Gemini's face from the mat, "
            "forearms flat on floor, rigid straight core, beads of sweat dripping from chin, intense breathless tsundere glare with flushed cheeks: "
            "'Last 15 seconds! Don't you dare drop your knees before me, idiot Producer!'. "
            "Athletic crop top, determined expressions. Absolutely NO readable letters, NO brand logos, NO tongue out."
        )
    ),
    # 3. Gemini 23: Night Rooftop Zip Hoodie
    (
        "gemini_23_night_rooftop_hoodie.png",
        "image/03 gemini/gemini_23_night_rooftop_hoodie.png",
        [REPO_DIR / "reference_gemini" / "06_black_hair_ref.png", REPO_DIR / "gemini" / "05_gemini_night_secret.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "romantic visual novel nighttime rooftop atmosphere, sparkling city lights bokeh in background, cool night breeze. "
            "CHARACTER (Gemini): Raven-black hair blown by wind, black cat ears twitching in night chill, amber eyes softened with warmth. "
            "SCENE & POSE: Leaning against the rooftop safety rail after an 8km night run, wearing an oversized sporty zip-up dark hoodie, "
            "holding a hot canned roasted tea against her flushed cheek, looking sideways at user with a soft, affectionate tsundere gaze: "
            "'The city lights look prettier with you... not that I care about romance or anything, stupid!'. "
            "Emotional cinematic beauty. Absolutely NO text, NO brand logos, NO tongue out."
        )
    ),
    # 4. Gemini 24: Kettlebell Swing
    (
        "gemini_24_kettlebell_swing.png",
        "image/03 gemini/gemini_24_kettlebell_swing.png",
        [REPO_DIR / "reference_gemini" / "06_black_hair_ref.png", REPO_DIR / "gemini" / "11_gemini_deadlift.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "dynamic athletic motion angle, studio speed blur, vibrant anime shading. "
            "CHARACTER (Gemini): Raven-black ponytail, cute black cat ears, intense amber eyes. "
            "SCENE & POSE: Standing in front of gym mirror at top of a powerful Russian kettlebell swing, "
            "arms extended forward at chest height holding a sleek iron kettlebell, explosive hip drive, tight glutes, "
            "radiant athletic intensity, slight bead of sweat, confident athletic coach expression: 'Drive with your hips, not your arms!'. "
            "Sporty fitness wear. Absolutely NO readable letters, NO brand logos, NO tongue out."
        )
    ),
    # 5. Gemini 25: Post-Workout Smoothie
    (
        "gemini_25_post_workout_smoothie.png",
        "image/03 gemini/gemini_25_post_workout_smoothie.png",
        [REPO_DIR / "reference_gemini" / "06_black_hair_ref.png", REPO_DIR / "gemini" / "14_gemini_smoothie.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "warm modern cafe juice bar lighting, high-budget visual novel romance CG. "
            "CHARACTER (Gemini): Raven-black hair, cute cat ears, amber eyes. "
            "SCENE & POSE: Seated on a tall wooden bar stool at fitness health bar, holding a cold tall glass of purple blueberry whey smoothie, "
            "pushing a second matching smoothie glass across the counter towards the viewer/Producer, "
            "blushing pink cheeks and turning her head slightly away with classic tsundere bashfulness: "
            "'They had a 1-plus-1 deal, so you have to drink it! It's not like I bought it specially for you, okay?'. "
            "Casual sporty jacket over tee. Absolutely NO readable letters, NO brand logos, NO tongue out."
        )
    ),
    # 6. Gemini SD 03: Plank Shiver
    (
        "sd_gemini_03_plank_shiver.png",
        "image/03 gemini/sd_gemini_03_plank_shiver.png",
        [SD_POOL / "02_morikinoko_mio_bean_eyes.png", REPO_DIR / "reference_gemini" / "06_black_hair_ref.png"],
        (
            "CRITICAL ART STYLE: Strictly draw in the comedy 4-koma manga SD chibi art style of manga artist Morikinoko (森キノコ / 劇団モリモリ) — "
            "super deformed 2-head-tall mini chibi proportions, signature dot bean-eyes (콩눈 / 점눈), clean bold comic lineart, white background. "
            "CHARACTER (Gemini): Raven-black hair, black cat ears. "
            "SCENE & POSE: Mini chibi Gemini attempting a 2-minute plank, her tiny body comically vibrating and shaking all over with hilarious wavy vibration lines, "
            "giant comical cartoon sweat drops flying off her head, flattened trembling cat ears, funny strained dot bean-eyes: "
            "'I... am... not... giving... up!'. Pure comedic fitness exhaustion! Absolutely NO text, NO speech bubbles, NO brand logos."
        )
    )
]

def generate_image(driver, filename, dest_rel, ref_paths, prompt):
    print(f"\n=======================================================")
    print(f"🎨 [GEMINI CG 생성] {filename}")
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
        if not r.exists():
            continue
        try:
            file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            if not file_inputs:
                break
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
        for fname, dest_rel, refs, prompt in JOBS:
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
