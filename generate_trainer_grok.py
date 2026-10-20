"""Gemini Fit AI Trainer (제미니) 캐릭터 이미지 재성생 스크립트
사용자가 제공한 아이돌마스터/학마스 스타일 레퍼런스를 첨부하여 Grok으로 생성합니다.
"""
import os
import sys
import time
import shutil
from pathlib import Path
from PIL import Image

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from _browser import (
    first_visible_css, click_first_xpath,
    big_image_srcs, wait_new_images, fetch_image
)

USER_PROFILE = Path(r"C:\Users\scmms\AppData\Roaming\Mozilla\Firefox\Profiles\hdmyalcf.default-release")
FIREFOX_EXE = r"C:\Program Files\Mozilla Firefox\firefox.exe"
TARGET_OUTPUT = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\trainer_gemini.png")

REF_1 = Path(r"C:\Users\scmms\.gemini\antigravity\brain\acd72411-9330-4563-8940-20997c2e2063\.user_uploaded\media_1792477460936_75850d14.png")
REF_2 = Path(r"C:\Users\scmms\.gemini\antigravity\brain\acd72411-9330-4563-8940-20997c2e2063\.user_uploaded\media_1792477475997_1257c477.png")

PROMPT_TEXT = (
    "Masterpiece anime idol game art style, exactly matching the character visual aesthetic in the reference image. "
    "A gorgeous, charming energetic young female personal fitness trainer, cute blonde hair in stylish twin braids, bright golden-amber eyes, "
    "confident cute tsundere smile looking at viewer, wearing stylish pastel & sporty fitness athletic crop training wear, "
    "clean modern fitness studio background with soft warm natural lighting, high resolution mobile game SSR card quality upper body portrait, aspect ratio 1:1"
)

def make_profile():
    work_profile = Path(r"d:\OneDrive\WorkSpace\02 AI 작업물\Health\.grok_profile")
    work_profile.mkdir(parents=True, exist_ok=True)
    for fname in ["cookies.sqlite", "key4.db", "cert9.db", "logins.json", "permissions.sqlite"]:
        src = USER_PROFILE / fname
        if src.exists():
            try:
                shutil.copy2(src, work_profile / fname)
            except Exception:
                pass
    storage_src = USER_PROFILE / "storage"
    storage_dst = work_profile / "storage"
    if storage_src.exists() and not storage_dst.exists():
        try:
            shutil.copytree(storage_src, storage_dst, ignore=shutil.ignore_patterns("cache", "Cache", "tmp"))
        except Exception:
            pass
    return work_profile

def attach_files(driver, paths):
    file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
    if not file_inputs:
        print("[참고] 파일 업로드 input 태그를 찾지 못함, 프롬프트 전송 계속")
        return
    inp = file_inputs[0]
    valid_paths = [str(p) for p in paths if p.exists()]
    if valid_paths:
        try:
            inp.send_keys("\n".join(valid_paths))
            print(f"[업로드] 레퍼런스 이미지 {len(valid_paths)}장 첨부 완료")
            time.sleep(4)
        except Exception as e:
            print(f"레퍼런스 첨부 예외: {e}")

def run():
    profile_dir = make_profile()
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
            print("[에러] 입력창 없음")
            return
            
        # 레퍼런스 이미지 첨부
        attach_files(driver, [REF_1, REF_2])
        
        before_imgs = set(big_image_srcs(driver))
        box.click()
        box.send_keys(PROMPT_TEXT)
        box.send_keys(Keys.ENTER)
        print("[성공] 프롬프트 및 레퍼런스 전송 완료! 생성 대기 중...")
        
        new_imgs = wait_new_images(driver, before_imgs, timeout=120, settle=3.0)
        if not new_imgs:
            raise RuntimeError("이미지 생성 시간 초과")
            
        img_src = new_imgs[0]
        pil_img = fetch_image(driver, img_src, "https://grok.com")
        pil_img.save(TARGET_OUTPUT, format="PNG")
        print("Done: Saved new trainer image!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
