"""Refine Event CGs using the exact proven aesthetic prompt from gemini_morning
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

AESTHETIC_JOBS = [
    (
        "gemini_tea_matcha.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl with soft blonde hair in twin braids, holding a traditional ceramic matcha tea bowl with fine green foam, gentle warm tsundere smile looking at viewer, sitting beside a sunlit cafe window with tea utensils, soft warm golden sunlight pouring in, airy pastel watercolor texture, slender toned waist, high quality anime illustration, aspect ratio 9:16"
    ),
    (
        "mio_sunlight_run.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol girl Honda Mio, short layered warm brown hair with cute side bangs, bright warm amber eyes, wearing sporty yellow and white fitness top, stretching or jogging pose on sunny outdoor track with green trees and dappled sunlight (komorebi), beaming radiant energetic smile, soft warm morning lighting, high quality anime card illustration, aspect ratio 9:16"
    ),
    (
        "gemini_workout_clean.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl with soft blonde hair in twin braids, sporty mint and white fitness outfit, holding small 2kg pink dumbbell demonstrating safe wrist rehab exercise, focused caring confident gaze, sunlit bright modern fitness studio, airy soft lighting, slender fit waist, high quality anime illustration, aspect ratio 9:16"
    ),
    (
        "gemini_evening.png",
        "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl with soft blonde hair in twin braids, cozy oversized pastel hoodie, holding warm mug of herbal tea, relaxed gentle soothing smile, cozy warm indoor ambient lamp lighting, cozy evening rest after fasting shutdown, high quality anime illustration, aspect ratio 9:16"
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

        for fname, prompt in AESTHETIC_JOBS:
            out_path = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health") / fname
            if out_path.exists():
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
