"""Direct clean generator for mio_21_tire_flip.png"""
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
        ref_path = REPO_DIR / "reference_mio" / "07_mio_official_standing.png"
        ref_img = Image.open(ref_path) if ref_path.exists() else None

        driver.get("https://grok.com")
        time.sleep(3.5)

        prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
        box = first_visible_css(driver, prompt_css, 20)
        if not box:
            raise RuntimeError("Grok input box not found")

        if ref_path.exists():
            try:
                file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
                if file_inputs:
                    target_input = next((i for i in file_inputs if i.get_attribute("multiple") is not None), file_inputs[0])
                    target_input.send_keys(str(ref_path.resolve()))
                    time.sleep(2.5)
            except Exception as ex:
                print("Attach error:", ex)

        prompt = (
            "CRITICAL ART STYLE: Gakumas & Cinderella Girls official SSR anime CG illustration, "
            "vibrant cell-shaded anime art, dynamic low angle sports action shot, sunny outdoor athletic turf. "
            "CHARACTER (Honda Mio): 15yo cheerful anime idol girl, short caramel-brown layered bob with flipped ends, "
            "bouncy ahoge hair, bright honey-gold eyes. "
            "SCENE & POSE: Outdoor sports turf, Mio standing triumphantly beside a giant heavy black workout tire, "
            "one hand on her hip and wiping sweat from her brow with an orange towel, radiant beaming idol smile: "
            "'Phew! 20 flips finished! You saw my idol strength, Producer?!'. Athletic sports bra and shorts. "
            "Clean vibrant colors. Absolutely NO readable letters, NO brand logos."
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
            new_srcs = wait_new_images(driver, before, timeout=30, settle=2.5)
            for src in new_srcs:
                cand = fetch_image(driver, src, "https://grok.com")
                if ref_img:
                    diff = ref_diff(cand, ref_img)
                    if diff < SAME_AS_REF:
                        print(f"Skipping ref image (diff={diff:.1f})")
                        before.add(src)
                        continue

                target_file.parent.mkdir(parents=True, exist_ok=True)
                cand.save(target_file, format="PNG")
                print(f"✨ [SUCCESS] {target_file.name} saved! ({cand.size})")
                art_target = ART_DIR / target_file.name
                shutil.copy2(target_file, art_target)
                return
        raise RuntimeError("Generation timeout")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
