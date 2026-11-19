"""Generate Kotone CG expansion:
1. kotone_07_smoothie_bench.png: Gym bench with fruit smoothie
2. kotone_21_jump_rope.png: Speed jump rope in dance studio, mid-air leap
3. kotone_22_hip_thrust.png: Barbell hip thrust with pad, focused idol determination
4. kotone_23_sports_drink_towel.png: Seated in dance room leaning back, towel, refreshing sip
5. kotone_24_pilates_ladder.png: Pilates ladder barrel graceful stretch
6. kotone_25_night_convenience_chat.png: Night convenience store plastic chair, warm sweet potato
7. sd_kotone_03_scale_shock.png: Morikinoko 2-head-tall bathroom scale shock comedy
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
    # 1. Kotone 07: Smoothie Bench
    (
        "kotone_07_smoothie_bench.png",
        "image/02 kotone/kotone_07_smoothie_bench.png",
        [REPO_DIR / "kotone" / "01_kotone_studio.png", REPO_DIR / "kotone" / "03_kotone_cafe.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "vibrant cell-shaded anime art, delicate lineart, sunny studio lighting. "
            "CHARACTER (Fujita Kotone): 16yo blonde anime girl with twin braids tied with yellow ribbons, amber eyes. "
            "SCENE & POSE: Kotone sitting on a polished gym bench holding an icy berry smoothie cup with a striped straw, "
            "tilting her head with an adorable affectionate idol smile: 'Phew! Taking a breather with you is the sweetest part of training, Producer!'. "
            "Yellow and white athletic outfit. Modern fitness studio background. Absolutely NO text, NO brand logos."
        )
    ),
    # 2. Kotone 21: Jump Rope
    (
        "kotone_21_jump_rope.png",
        "image/02 kotone/kotone_21_jump_rope.png",
        [REPO_DIR / "kotone" / "01_kotone_studio.png", REPO_DIR / "kotone" / "14_morning_jog.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "dynamic mid-air freeze frame, bright stage studio lighting, sparkling anime sweat effects. "
            "CHARACTER (Fujita Kotone): Blonde anime girl with twin braids flying in the air, amber eyes. "
            "SCENE & POSE: Mid-air leap doing high-speed jump rope in dance studio, knees tucked lightly, rope blurred under her sneakers, "
            "sparkling bright smile full of idol energy: '100 jumps done! 200 jumps next! Cardio for the center idol position!'. "
            "Energetic idol workout wear. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 3. Kotone 22: Barbell Hip Thrust
    (
        "kotone_22_hip_thrust.png",
        "image/02 kotone/kotone_22_hip_thrust.png",
        [REPO_DIR / "kotone" / "01_kotone_studio.png", REPO_DIR / "kotone" / "10_beach_volleyball.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "vibrant cell-shaded anime art, clean lineart, focused gym atmosphere. "
            "CHARACTER (Fujita Kotone): Blonde anime girl with twin braids, amber eyes. "
            "SCENE & POSE: Kotone at the bench performing a barbell hip thrust with a pink foam barbell pad, "
            "upper back braced against the bench, hips fully extended at top lockout, focused determined expression with flushed cheeks: "
            "'To have the most breathtaking dance lines on stage, glute drive is essential! Look Producer, form is perfect, right?'. "
            "Modern gym weight room background. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 4. Kotone 23: Sports Drink & Towel
    (
        "kotone_23_sports_drink_towel.png",
        "image/02 kotone/kotone_23_sports_drink_towel.png",
        [REPO_DIR / "kotone" / "01_kotone_studio.png", REPO_DIR / "kotone" / "13_cool_down.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "warm relaxing lighting, delicate lineart, charming romance atmosphere. "
            "CHARACTER (Fujita Kotone): Blonde hair with twin braids, amber eyes shining with gratitude. "
            "SCENE & POSE: Seated on the wooden dance studio floor leaning back on her left hand, fluffy white sports towel draped around her neck, "
            "holding a chilled sports bottle in her right hand after taking a refreshing sip, soft blushing gaze at user: "
            "'Ahhh~! When Producer hands me cold water, it tastes a hundred times more refreshing!'. "
            "Casual idol tee and track shorts. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 5. Kotone 24: Pilates Ladder Barrel
    (
        "kotone_24_pilates_ladder.png",
        "image/02 kotone/kotone_24_pilates_ladder.png",
        [REPO_DIR / "kotone" / "01_kotone_studio.png", REPO_DIR / "kotone" / "11_balance_ball.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "elegant studio lighting, beautiful arching posture, clean cell shading. "
            "CHARACTER (Fujita Kotone): Blonde anime girl with twin braids, amber eyes. "
            "SCENE & POSE: Elegant side stretch on a wooden Pilates ladder barrel, one arm arching gracefully overhead, "
            "giggling playfully as she looks at user: 'Look Producer, flexible like a ribbon! My posture is getting more idol-like every day!'. "
            "Pastel yellow Pilates tights. Boutique fitness room background. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 6. Kotone 25: Night Convenience Chat
    (
        "kotone_25_night_convenience_chat.png",
        "image/02 kotone/kotone_25_night_convenience_chat.png",
        [REPO_DIR / "kotone" / "01_kotone_studio.png", REPO_DIR / "kotone" / "20_sunset_bench.png"],
        (
            "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) official SSR anime game CG illustration, "
            "warm street lamp glow, night convenience store romantic mood, emotional visual novel illustration. "
            "CHARACTER (Fujita Kotone): Blonde hair with twin braids, amber eyes with affectionate gaze. "
            "SCENE & POSE: Sitting on a green plastic chair outside a 24h convenience store at night after training, "
            "breaking a warm roasted sweet potato in half and offering the bigger piece to Producer with a radiant sweet smile: "
            "'You worked so hard coaching me today! Half for you, half for Kotone! Let's reach 52kg together!'. "
            "Night city ambiance. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 7. Kotone SD 03: Scale Shock
    (
        "sd_kotone_03_scale_shock.png",
        "image/02 kotone/sd_kotone_03_scale_shock.png",
        [SD_POOL / "02_morikinoko_mio_bean_eyes.png", REPO_DIR / "kotone" / "01_kotone_studio.png"],
        (
            "CRITICAL ART STYLE: Strictly draw in the comedy 4-koma manga SD chibi art style of manga artist Morikinoko (森キノコ / 劇団モリモリ) — "
            "super deformed 2-head-tall mini chibi proportions, signature dot bean-eyes, clean comic lineart, white background. "
            "CHARACTER (Fujita Kotone): Blonde hair with twin braids. "
            "SCENE & POSE: Mini chibi Kotone standing on a tiny bathroom scale, clutching her cheeks in comical sheer horror with giant dot eyes "
            "and funny wavy cartoon scream lines: '+0.2kg?! Did that cup of water weigh 200 grams?! Waaaah!'. "
            "Hilarious idol diet panic comedy! Absolutely NO text, NO speech bubbles, NO brand logos."
        )
    )
]

def generate_image(driver, filename, dest_rel, ref_paths, prompt):
    print(f"\n=======================================================")
    print(f"🎨 [KOTONE CG 생성] {filename}")
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
