"""학원 아이돌마스터 스타일 (맑고 투명한 파스텔 셀화, 부드러운 선화)
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
TARGET_OUTPUT = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\trainer_gemini.png")

PROMPT = (
    "Masterpiece, official Gakuen Idolmaster game illustration art style, extremely soft delicate anime aesthetic. "
    "Cute charming 19-year-old anime idol trainer girl, soft natural blonde hair in loose twin braids, "
    "warm glowing amber eyes, sweet gentle tsundere smile looking at viewer, "
    "wearing cute cozy pastel mint and white oversized sporty track jacket over light sportswear, "
    "bright airy high-key lighting, soft pastel color palette, clean light delicate linework, "
    "transparent watercolor cel-shaded texture, airy Japanese idol game visual, upper body portrait, aspect ratio 1:1"
)

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

        before = set(big_image_srcs(driver))
        box.click()
        box.send_keys(PROMPT)
        box.send_keys(Keys.ENTER)
        print("Generating soft Gakuen Idolmaster style...")
        
        new_imgs = wait_new_images(driver, before, timeout=120, settle=3.0)
        if new_imgs:
            img = fetch_image(driver, new_imgs[0], "https://grok.com")
            img.save(TARGET_OUTPUT, format="PNG")
            print("Successfully saved soft idol style image!")
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
