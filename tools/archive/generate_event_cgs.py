"""Generate Event CGs and High-Res Trainer Images using Grok with Gakuen Idolmaster Aesthetic
"""
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from _browser import first_visible_css, big_image_srcs, wait_new_images, fetch_image

FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
PROFILE_DIR = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\.grok_profile")

JOBS = [
    (
        "trainer_mio.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol girl, Honda Mio inspired, bright warm amber eyes, warm brown short layered hair with cute side bangs, bright cheerful beaming smile, wearing sporty yellow and orange track jacket with white accents, idol trainer, soft pastel daylight, clean studio background, high quality anime visual, upper body portrait, aspect ratio 1:1",
        True # force overwrite
    ),
    (
        "gemini_morning.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl, soft blonde hair in twin braids, gentle morning stretch pose near sunny window, soft airy pastels, drinking glass of fresh water, serene charming expression, cozy morning fitness atmosphere, upper body, aspect ratio 1:1",
        False
    ),
    (
        "gemini_workout.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl, soft blonde hair in twin braids, sporty mint-white track jacket, holding 2kg dumbbell doing wrist exercise demonstration, focused caring confident gaze, clean modern gym studio background, soft lighting, upper body, aspect ratio 1:1",
        False
    ),
    (
        "mio_running.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol girl Honda Mio, short brown layered hair, energetic running pose on outdoor athletic track, sports windbreaker, sunny park background, cheering enthusiastically at viewer, dynamic charming idol scene, upper body, aspect ratio 1:1",
        False
    ),
    (
        "dual_inbody.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Two cute anime idol trainer girls standing together side by side: one with soft blonde twin braids in mint jacket and one with short brown hair in yellow sporty jacket, holding InBody fitness report chart together, smiling brightly at viewer, celebratory golden sparkle atmosphere, charming duo, horizontal aspect ratio 16:9",
        False
    )
]

def run():
    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    driver.set_script_timeout(120)
    
    try:
        driver.get("https://grok.com/imagine")
        time.sleep(4)
        prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
        box = first_visible_css(driver, prompt_css, 15)
        if not box:
            driver.get("https://grok.com")
            box = first_visible_css(driver, prompt_css, 20)
        if not box:
            print("Could not find prompt box on grok.com")
            return

        for fname, prompt, force in JOBS:
            out_path = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health") / fname
            if out_path.exists() and not force:
                print(f"Skipping {fname} (already exists)")
                continue
            
            print(f"Generating {fname}...")
            before = set(big_image_srcs(driver))
            box.click()
            time.sleep(0.5)
            box.send_keys(prompt)
            box.send_keys(Keys.ENTER)
            
            new_imgs = wait_new_images(driver, before, timeout=120, settle=3.0)
            if new_imgs:
                img = fetch_image(driver, new_imgs[0], "https://grok.com")
                img.save(out_path, format="PNG")
                print(f"Saved: {fname}")
            else:
                print(f"Timeout waiting for image: {fname}")
            time.sleep(3)
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
