"""Generate Mio CG expansion:
1. mio_21_tire_flip.png: Tire flip on outdoor turf, fierce energetic idol grit
2. mio_22_battle_ropes.png: Battle ropes slam, dynamic waves & laughter
3. mio_23_stair_sprint.png: Outdoor stadium stairs sprint, looking back reaching hand
4. mio_24_lat_pulldown.png: Wide grip lat pulldown machine, muscular back posture
5. mio_25_night_stargazing.png: Lying on track grass gazing at starry night sky
6. sd_mio_03_burpee_bounce.png: Morikinoko 2-head-tall burpee bouncing ball comedy
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
    # 1. Mio 21: Tire Flip
    (
        "mio_21_tire_flip.png",
        "image/01 mio/mio_21_tire_flip.png",
        [REPO_DIR / "reference_mio" / "07_mio_official_standing.png", REPO_DIR / "mio" / "01_mio_main.png"],
        (
            "CRITICAL ART STYLE: Gakumas & Idolmaster Cinderella Girls official SSR anime CG illustration, "
            "vibrant cell-shaded anime art, low angle dynamic action shot, sunny outdoor turf lighting. "
            "CHARACTER (Honda Mio): 15yo cheerful idol girl, short caramel-brown layered bob with flipped ends, ahoge hair, honey-gold eyes. "
            "SCENE & POSE: Outdoor CrossFit turf, Mio bending deep with hands hooked under a giant heavy rubber tractor tire, "
            "explosively flipping it over with fierce energetic power, glistening sweat on collarbone, beaming triumphant roar: "
            "'One, two, HUP! You see that, Producer?! Pure idol strength!'. Athletic orange sports bra and compression shorts. "
            "Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 2. Mio 22: Battle Ropes
    (
        "mio_22_battle_ropes.png",
        "image/01 mio/mio_22_battle_ropes.png",
        [REPO_DIR / "reference_mio" / "07_mio_official_standing.png", REPO_DIR / "mio" / "09_mio_boxing_sparring.png"],
        (
            "CRITICAL ART STYLE: Gakumas & Cinderella Girls official SSR anime CG illustration, "
            "vibrant cell-shaded anime art, high-speed motion blur waves, dramatic fitness studio lighting. "
            "CHARACTER (Honda Mio): Short caramel-brown hair with bouncing ahoge, honey-gold eyes. "
            "SCENE & POSE: Gripping heavy black battle ropes with both hands in a athletic half-squat, slamming them rhythmically to create "
            "huge undulating wave ripples on the floor, sweat beads flying, laughing with exhilaration: "
            "'Wave after wave! Upper body HIIT cardio is unbeatable! Let's burn every extra calorie!'. "
            "Dynamic sports wear. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 3. Mio 23: Stair Sprint
    (
        "mio_23_stair_sprint.png",
        "image/01 mio/mio_23_stair_sprint.png",
        [REPO_DIR / "reference_mio" / "01_mio_sunlight_track.png", REPO_DIR / "mio" / "02_mio_park_run.png"],
        (
            "CRITICAL ART STYLE: Gakumas & Cinderella Girls official SSR anime CG illustration, "
            "golden sunset lighting, dynamic upward perspective on stadium concrete stairs. "
            "CHARACTER (Honda Mio): Short caramel-brown hair catching golden sunlight, honey-gold eyes. "
            "SCENE & POSE: Sprinting up the final steps of a grand outdoor stadium staircase, pausing at the landing and reaching her hand down toward Producer, "
            "breathless but smiling with dazzling idol warmth: 'Almost at the top! Take my hand Producer, let's watch the sunset from the highest step together!'. "
            "Bright athletic runner outfit. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 4. Mio 24: Lat Pulldown
    (
        "mio_24_lat_pulldown.png",
        "image/01 mio/mio_24_lat_pulldown.png",
        [REPO_DIR / "reference_mio" / "07_mio_official_standing.png", REPO_DIR / "mio" / "18_squat_rack.png"],
        (
            "CRITICAL ART STYLE: Gakumas & Cinderella Girls official SSR anime CG illustration, "
            "vibrant cell-shaded anime art, mirror reflection angle, high-energy gym setting. "
            "CHARACTER (Honda Mio): Short caramel-brown hair, honey-gold eyes. "
            "SCENE & POSE: Seated at lat pulldown machine, pulling wide angled bar smoothly down to her upper chest, "
            "arching chest proudly, beautifully defined back taper and shoulder line, focused grin catching eye-contact in the front mirror: "
            "'20 reps x 4 sets, set number three! Don't let your elbows flare out, that's what Producer taught me!'. "
            "Sporty tank top. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 5. Mio 25: Night Stargazing
    (
        "mio_25_night_stargazing.png",
        "image/01 mio/mio_25_night_stargazing.png",
        [REPO_DIR / "reference_mio" / "08_mio_zenith_rest.png", REPO_DIR / "mio" / "01_mio_main.png"],
        (
            "CRITICAL ART STYLE: Gakumas & Cinderella Girls official SSR anime CG illustration, "
            "cool night breeze atmosphere, deep blue night sky sprinkled with stars, soft track floodlight glow. "
            "CHARACTER (Honda Mio): Short caramel-brown hair spread on grass, honey-gold eyes reflecting starlight. "
            "SCENE & POSE: Lying side-by-side with Producer on the infield grass of the stadium track after a 10km run, "
            "turning her head to the side to look directly at Producer with a gentle, tender, heart-fluttering smile: "
            "'Running under the starry sky with you... is my happiest place in the world. Thank you for always being by my side, Producer.'. "
            "Emotional romantic bond. Absolutely NO readable letters, NO brand logos."
        )
    ),
    # 6. Mio SD 03: Burpee Bounce
    (
        "sd_mio_03_burpee_bounce.png",
        "image/01 mio/sd_mio_03_burpee_bounce.png",
        [SD_POOL / "04_morikinoko_mio_cover_smug.png", SD_POOL / "02_morikinoko_mio_bean_eyes.png"],
        (
            "CRITICAL ART STYLE: Strictly draw in the legendary official Morikinoko (森キノコ / 劇団モリモリ) Honda Mio 4-koma manga SD chibi art style — "
            "super deformed 2-head-tall mini chibi proportions, signature Morikinoko dot bean-eyes (콩눈), clean comic lineart, white background. "
            "CHARACTER (Honda Mio): Short caramel-brown hair with bouncy ahoge. "
            "SCENE & POSE: Mini chibi Mio doing rapid-fire burpees like a bouncing rubber ball, bouncing high in the air with comical spring coil effects under her feet, "
            "hilarious open-mouthed bean-eyed grin: 'Boing! Boing! 50 burpees in 1 minute! Mio-chan is invincible!'. "
            "Hilarious cartoon comedy action! Absolutely NO text, NO speech bubbles, NO brand logos."
        )
    )
]

def generate_image(driver, filename, dest_rel, ref_paths, prompt):
    print(f"\n=======================================================")
    print(f"🎨 [MIO CG 생성] {filename}")
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
