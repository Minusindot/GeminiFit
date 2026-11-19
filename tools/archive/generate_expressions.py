"""트레이너 표정 바리에이션 생성 (Happy, Angry)
"""
import time
from pathlib import Path
from PIL import Image

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from _browser import first_visible_css, big_image_srcs, wait_new_images, fetch_image

USER_PROFILE = Path(r"C:\Users\scmms\AppData\Roaming\Mozilla\Firefox\Profiles\hdmyalcf.default-release")
FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
BASE_IMG = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\trainer_gemini.png")

PROMPTS = [
    ("trainer_angry.png", "Masterpiece anime idol game art style, exactly matching character in reference image. Cute blonde hair in twin braids, cute angry pouting tsundere facial expression with flushed cheeks, shouting with slight sharp cat teeth, cute sporty cropped athletic jacket, modern fitness gym, high quality portrait, aspect ratio 1:1"),
    ("trainer_happy.png", "Masterpiece anime idol game art style, exactly matching character in reference image. Cute blonde hair in twin braids, shy sweet blush smiling facial expression looking at viewer, heartwarming tsundere praise smile, cute sporty cropped athletic jacket, modern fitness gym, high quality portrait, aspect ratio 1:1")
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

        for filename, prompt in PROMPTS:
            out_path = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health") / filename
            if out_path.exists():
                continue
                
            # 파일 첨부
            file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if file_inputs and BASE_IMG.exists():
                try:
                    file_inputs[0].send_keys(str(BASE_IMG))
                    time.sleep(3)
                except Exception:
                    pass
                    
            before = set(big_image_srcs(driver))
            box = first_visible_css(driver, prompt_css, 10) or box
            box.click()
            box.send_keys(prompt)
            box.send_keys(Keys.ENTER)
            print(f"Generating {filename}...")
            
            new_imgs = wait_new_images(driver, before, timeout=120, settle=3.0)
            if new_imgs:
                img = fetch_image(driver, new_imgs[0], "https://grok.com")
                img.save(out_path, format="PNG")
                print(f"Saved: {filename}")
            time.sleep(3)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
