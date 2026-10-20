"""grok_browser.py(Firefox) / gemini_browser.py(Chrome) 공용 Selenium 헬퍼.

로그인 방식(두 도구 공통): 구글/X 로그인은 자동화 브라우저를 막으므로, --setup은 실제 브라우저를 전용 프로필로
**자동화 없이** 띄워 사람이 로그인하게 하고(창을 닫으면 세션 저장), 생성할 때만 Selenium이 같은 브라우저 +
같은 프로필을 조종한다. 드라이버(geckodriver/chromedriver)는 Selenium Manager가 자동으로 받아온다.
보안 확인(캡차)은 자동으로 넘기지 않는다 - 창이 떠 있으니 사람이 처리하면 이어서 기다린다.
"""
from __future__ import annotations

import base64
import io
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

MIN_RESULT_SIDE = 400  # 이보다 작은 <img>는 아이콘/썸네일로 보고 무시


def find_exe(candidates: list[str], which_name: str) -> str:
    for c in candidates:
        if Path(c).exists():
            return c
    found = shutil.which(which_name)
    if found:
        return found
    sys.exit(f"[browser] {which_name} 실행 파일을 찾지 못했습니다.")


def manual_login(cmd: list[str], profile_dir: Path, site: str) -> None:
    profile_dir.mkdir(parents=True, exist_ok=True)
    print(f"[browser] 전용 프로필 브라우저를 엽니다. {site} 로그인을 끝낸 뒤 **그 브라우저 창을 닫으세요.**")
    subprocess.Popen(cmd).wait()
    print(f"[browser] 세션 저장 완료: {profile_dir}")


def first_visible_css(driver, selectors, timeout=15.0):
    from selenium.webdriver.common.by import By

    end = time.time() + timeout
    while time.time() < end:
        for sel in selectors:
            for el in driver.find_elements(By.CSS_SELECTOR, sel)[:5]:
                try:
                    if el.is_displayed():
                        return el
                except Exception:
                    pass
        time.sleep(0.4)
    return None


def click_first_xpath(driver, xpaths, timeout=1.5) -> bool:
    from selenium.webdriver.common.by import By

    end = time.time() + timeout
    while time.time() < end:
        for xp in xpaths:
            for el in driver.find_elements(By.XPATH, xp)[:3]:
                try:
                    if el.is_displayed() and el.is_enabled():
                        el.click()
                        return True
                except Exception:
                    pass
        time.sleep(0.3)
    return False


def type_multiline(element, text: str) -> None:
    """줄바꿈은 Shift+Enter로 넣는다(입력창에서 Enter = 전송). 프롬프트 서식(행/칸 구분)을 그대로 보내기 위함."""
    from selenium.webdriver.common.keys import Keys

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line:
            element.send_keys(line)
        if i < len(lines) - 1:
            element.send_keys(Keys.SHIFT, Keys.ENTER)


def insert_text(driver, element, text: str) -> bool:
    """contenteditable 입력창에 text를 한 번에 넣고, 실제로 들어갔는지 확인해 돌려준다.

    send_keys로 2천 자짜리 여러 줄 프롬프트를 치면 느리고, 줄바꿈(Shift+Enter)이 사이트에 따라 전송으로 먹혀
    앞 한 줄만 나가는 일이 있다. 브라우저의 execCommand('insertText')는 사람이 붙여넣은 것과 같은 입력
    이벤트를 내서(Quill 같은 편집기도 인식) 줄마다 문단으로 그대로 들어간다. 실패하면 type_multiline으로 대신 친다."""
    def current() -> str:
        return driver.execute_script("return arguments[0].innerText || arguments[0].value || ''", element) or ""

    probe = " ".join(text.split())[:40]
    driver.execute_script(
        "const [el, t] = arguments; el.focus(); document.execCommand('insertText', false, t);", element, text)
    time.sleep(0.4)
    if probe and probe in " ".join(current().split()):
        return True

    element.click()
    type_multiline(element, text)
    time.sleep(0.4)
    return bool(probe) and probe in " ".join(current().split())


def big_image_srcs(driver) -> list[str]:
    return driver.execute_script(
        """return Array.from(document.querySelectorAll('img'))
             .filter(i => i.complete && Math.min(i.naturalWidth, i.naturalHeight) >= arguments[0])
             .map(i => i.currentSrc || i.src);""",
        MIN_RESULT_SIDE,
    )


def wait_new_images(driver, before: set, timeout: int, settle: float = 4.0) -> list[str]:
    """before에 없던 큰 이미지가 나타나고 목록이 settle초 동안 그대로일 때까지 기다린다(미리보기 → 최종본 교체 대비)."""
    end = time.time() + timeout
    new, last, stable_since = [], None, None
    while time.time() < end:
        new = [s for s in big_image_srcs(driver) if s not in before]
        if new and new == last:
            stable_since = stable_since or time.time()
            if time.time() - stable_since >= settle:
                return new
        else:
            stable_since = None
        last = new
        time.sleep(1)
    return new


def _fetch_in_page(driver, src: str):
    return driver.execute_async_script(
        """const [src, done] = arguments;
           const opts = src.startsWith('blob:') ? {} : {credentials: 'include'};
           fetch(src, opts).then(r => r.ok ? r.blob() : null).then(b => {
             if (!b) return done(null);
             const fr = new FileReader(); fr.onload = () => done(fr.result.split(',')[1]); fr.readAsDataURL(b);
           }).catch(() => done(null));""",
        src,
    )


def _img_via_canvas(driver, src: str):
    """페이지에 이미 떠 있는 <img>를 캔버스에 원본 크기(naturalWidth)로 그려 PNG로 뽑는다. blob: 주소는 페이지
    밖(requests)에서 못 받고, 사이트 보안 정책(CSP) 때문에 페이지 안 fetch도 막힐 수 있어서 쓰는 마지막 방법."""
    return driver.execute_script(
        """const src = arguments[0];
           const img = Array.from(document.querySelectorAll('img')).find(i => (i.currentSrc || i.src) === src);
           if (!img || !img.complete || !img.naturalWidth) return null;
           const c = document.createElement('canvas');
           c.width = img.naturalWidth; c.height = img.naturalHeight;
           c.getContext('2d').drawImage(img, 0, 0);
           try { return c.toDataURL('image/png').split(',')[1]; } catch (e) { return null; }""",
        src,
    )


def fetch_image(driver, src: str, referer: str) -> Image.Image:
    if src.startswith("data:"):
        return Image.open(io.BytesIO(base64.b64decode(src.split(",", 1)[1])))

    if src.startswith("blob:"):
        b64 = _fetch_in_page(driver, src) or _img_via_canvas(driver, src)
        if b64:
            return Image.open(io.BytesIO(base64.b64decode(b64)))
        raise RuntimeError("blob 이미지를 꺼내지 못했습니다")

    candidates = [src]
    # 구글 이미지 서버 URL은 끝의 크기 지정(=s1024 등)을 =s0으로 바꾸면 원본 해상도를 준다.
    if "googleusercontent.com" in src:
        candidates.insert(0, re.sub(r"=[^/=]*$", "=s0", src) if re.search(r"=[^/=]*$", src) else src + "=s0")

    for url in candidates:
        b64 = _fetch_in_page(driver, url)
        if b64:
            return Image.open(io.BytesIO(base64.b64decode(b64)))

    # 교차 출처라 페이지 fetch가 막히면 브라우저 쿠키를 실어 직접 받는다.
    import requests

    sess = requests.Session()
    for c in driver.get_cookies():
        sess.cookies.set(c["name"], c["value"], domain=c.get("domain"))
    ua = driver.execute_script("return navigator.userAgent")
    for url in candidates:
        r = sess.get(url, headers={"User-Agent": ua, "Referer": referer}, timeout=60)
        if r.ok and r.content:
            return Image.open(io.BytesIO(r.content))
    raise RuntimeError("이미지 다운로드 실패")


def debug_shot(driver, path: Path) -> None:
    try:
        driver.save_screenshot(str(path))
        print(f"[browser] 디버그 스크린샷: {path}")
    except Exception:
        pass
