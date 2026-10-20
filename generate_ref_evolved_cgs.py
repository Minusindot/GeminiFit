"""Generate Evolved Fitness Trainer Art with Grok using Image-to-Image / Reference Upload
"""
import time
from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from _browser import first_visible_css, big_image_srcs, wait_new_images, fetch_image

FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
PROFILE_DIR = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\.grok_profile")
BASE_DIR = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health")

REF_MORNING = Path(r"C:\Users\scmms\.gemini\antigravity\brain\acd72411-9330-4563-8940-20997c2e2063\.user_uploaded\media_1792480804449_9f35246d.png")
REF_MIO = Path(r"C:\Users\scmms\.gemini\antigravity\brain\acd72411-9330-4563-8940-20997c2e2063\.user_uploaded\media_1792480708184_d363efaf.png")
REF_GAKUEN = Path(r"C:\Users\scmms\.gemini\antigravity\brain\acd72411-9330-4563-8940-20997c2e2063\.user_uploaded\media_1792480731356_e0f58139.png")

EVOLVE_JOBS = [
    (
        "trainer_gemini.png",
        REF_MORNING,
        "In the exact character design and soft warm lighting anime aesthetic of the reference image: Cute 19yo anime idol fitness trainer girl, identical soft blonde hair in twin braids, charming tsundere expression looking at camera, wearing stylish mint green and white athletic tracksuit, standing in an airy modern studio with warm golden sunlight pouring through large grid window, slender fit athletic waist, crisp clean anime cel shading, high quality 2D anime card illustration, upper body portrait, aspect ratio 9:16"
    ),
    (
        "trainer_mio.png",
        REF_MIO,
        "In the exact character design and anime art style of the reference image: Cute 19yo anime idol girl Honda Mio, identical short layered warm brown hair with cute side bangs, warm amber eyes, radiant beaming cheerful smile, wearing sporty yellow and orange track jacket with white accents, standing in sunny outdoor athletic park with green trees and dappled warm sunlight (komorebi), high quality anime card illustration, crisp clean anime lines, upper body portrait, aspect ratio 9:16"
    ),
    (
        "gemini_tea_matcha.png",
        REF_MORNING,
        "In the exact character design and soft warm lighting aesthetic of the reference image: The identical cute anime idol girl with soft blonde hair in twin braids, holding a traditional ceramic matcha tea bowl with delicate whisk froth, warm sweet gentle smile, sitting by a cozy sunlit cafe table, soft warm golden morning sunlight, airy pastel watercolor texture, high quality anime illustration, aspect ratio 9:16"
    )
]

def run():
    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    driver.set_script_timeout(150)
    
    try:
        for fname, ref_path, prompt in EVOLVE_JOBS:
            out_path = BASE_DIR / fname
            print(f"--- Starting {fname} with reference: {ref_path.name} ---")
            
            driver.get("https://grok.com/imagine")
            time.sleep(4)
            
            prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
            box = first_visible_css(driver, prompt_css, 15)
            if not box:
                driver.get("https://grok.com")
                box = first_visible_css(driver, prompt_css, 20)
            if not box:
                print("Could not find prompt box on grok.com")
                continue

            # Upload reference image
            file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            if file_inputs and ref_path.exists():
                print(f"Uploading reference image: {ref_path}")
                file_input = file_inputs[0]
                file_input.send_keys(str(ref_path.resolve()))
                time.sleep(5)  # wait for upload thumbnail to attach

            before = set(big_image_srcs(driver))
            box = first_visible_css(driver, prompt_css, 10) or box
            box.click()
            time.sleep(0.5)
            box.send_keys(prompt)
            box.send_keys(Keys.ENTER)
            print(f"Submitted prompt for {fname}, waiting for generation...")
            
            new_imgs = wait_new_images(driver, before, timeout=120, settle=3.0)
            if new_imgs:
                img = fetch_image(driver, new_imgs[0], "https://grok.com")
                img.save(out_path, format="PNG")
                print(f"Successfully generated and saved: {fname} ({img.size})")
            else:
                print(f"Timeout waiting for {fname}")
            time.sleep(4)
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
