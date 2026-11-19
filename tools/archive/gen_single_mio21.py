"""Single generator for mio_21_tire_flip.png"""
from pathlib import Path
import sys
import time
import shutil
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from evolve_pool import BASE_DIR, FIREFOX_EXE, PROFILE_DIR, SAME_AS_REF, ref_diff
from _browser import big_image_srcs, fetch_image, first_visible_css, wait_new_images

ART_DIR = Path(r"C:\Users\scmms\.gemini\antigravity\brain\acd72411-9330-4563-8940-20997c2e2063")
REPO_DIR = BASE_DIR / "image" / "90 repository"
target_file = BASE_DIR / "image" / "01 mio" / "mio_21_tire_flip.png"

def main():
    if target_file.exists() and target_file.stat().st_size > 50000:
        print("mio_21_tire_flip.png already exists!")
        return

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

    try:
        ref_paths = [REPO_DIR / "reference_mio" / "07_mio_official_standing.png", REPO_DIR / "mio" / "01_mio_track_rest.png"]
        ref_imgs = [Image.open(r) for r in ref_paths if r.exists()]
        driver.get("https://grok.com/imagine")
        time.sleep(3.5)

        prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
        box = first_visible_css(driver, prompt_css, 15)
        if not box:
            driver.get("https://grok.com")
            box = first_visible_css(driver, prompt_css, 20)

        for r in ref_paths:
            if not r.exists(): continue
            try:
                file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
                if not file_inputs: break
                target_input = next((i for i in file_inputs if i.get_attribute("multiple") is not None), file_inputs[0])
                target_input.send_keys(str(r.resolve()))
                time.sleep(2.5)
            except Exception as ex:
                break
        time.sleep(2.0)

        prompt = (
            "CRITICAL ART STYLE: Gakumas & Idolmaster Cinderella Girls official SSR anime CG illustration, "
            "vibrant cell-shaded anime art, low angle dynamic action shot, sunny outdoor turf lighting. "
            "CHARACTER (Honda Mio): 15yo cheerful idol girl, short caramel-brown layered bob with flipped ends, ahoge hair, honey-gold eyes. "
            "SCENE & POSE: Outdoor CrossFit turf, Mio bending deep with hands hooked under a giant heavy rubber tractor tire, "
            "explosively flipping it over with fierce energetic power, glistening sweat on collarbone, beaming triumphant roar: "
            "'One, two, HUP! You see that, Producer?! Pure idol strength!'. Athletic orange sports bra and compression shorts. "
            "Absolutely NO readable letters, NO brand logos."
        )

        before = set(big_image_srcs(driver))
        box = first_visible_css(driver, prompt_css, 10) or box
        box.click()
        time.sleep(0.3)
        box.send_keys(" ".join(prompt.split()))
        box.send_keys(Keys.ENTER)
        print("⏳ Grok CG rendering wait...")

        end_time = time.time() + 180
        while time.time() < end_time:
            new_srcs = wait_new_images(driver, before, timeout=40, settle=2.5)
            for src in new_srcs:
                cand = fetch_image(driver, src, "https://grok.com")
                diffs = [ref_diff(cand, r_im) for r_im in ref_imgs]
                min_diff = min(diffs) if diffs else 999.0
                if min_diff < SAME_AS_REF:
                    before.add(src)
                    continue

                target_file.parent.mkdir(parents=True, exist_ok=True)
                cand.save(target_file, format="PNG")
                print(f"✨ [SUCCESS] {target_file.name} saved! ({cand.size})")
                art_target = ART_DIR / target_file.name
                shutil.copy2(target_file, art_target)
                return
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
