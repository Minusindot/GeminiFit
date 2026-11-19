"""제미니의 7일 일상 인스타 피드 이미지 생성 스크립트
(말차/홈카페, 테라스 카페, 수요일 인바디 데이 등)
"""
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from _browser import first_visible_css, big_image_srcs, wait_new_images, fetch_image

USER_PROFILE = Path(r"C:\Users\scmms\AppData\Roaming\Mozilla\Firefox\Profiles\hdmyalcf.default-release")
FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
BASE_IMG = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\trainer_gemini.png")

DAILY_JOBS = [
    ("trainer_tea.png", "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl, soft blonde hair in twin braids, holding a traditional matcha tea bowl with whisk foam, gentle warm tsundere smile looking at viewer, cozy home cafe background with espresso machine and tea set, soft warm sunlight, airy pastel watercolor texture, upper body, aspect ratio 1:1"),
    ("trainer_cafe.png", "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl, soft blonde hair in twin braids, stylish casual weekend cafe terrace background with small espresso cup, soft breeze, natural daylight, warm sweet smile, charming Japanese idol visual, upper body, aspect ratio 1:1"),
    ("trainer_wednesday.png", "Masterpiece, official Gakuen Idolmaster soft delicate anime aesthetic. Cute 19yo anime idol trainer girl, soft blonde hair in twin braids, sporty track jacket, holding fitness clipboard with cheeky confident tsundere smirk, Wednesday InBody measurement day theme, modern clean studio, upper body, aspect ratio 1:1")
]

def run():
    profile_dir = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\.grok_profile")
    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(profile_dir))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    driver.set_script_timeout(120)
    
    try:
        driver.get("https://grok.com/imagine")
        time.sleep(3)
        prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
        box = first_visible_css(driver, prompt_css, 15)
        if not box:
            driver.get("https://grok.com")
            box = first_visible_css(driver, prompt_css, 20)
        if not box:
            return

        for fname, prompt in DAILY_JOBS:
            out_path = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health") / fname
            if out_path.exists():
                continue
            before = set(big_image_srcs(driver))
            box.click()
            box.send_keys(prompt)
            box.send_keys(Keys.ENTER)
            print(f"Generating {fname}...")
            new_imgs = wait_new_images(driver, before, timeout=120, settle=3.0)
            if new_imgs:
                img = fetch_image(driver, new_imgs[0], "https://grok.com")
                img.save(out_path, format="PNG")
                print(f"Saved: {fname}")
            time.sleep(3)
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
