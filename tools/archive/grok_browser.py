"""Grok(grok.com) 웹 화면을 **실제 설치된 Firefox**로 자동 조작해 캐릭터 일러스트 / 이벤트 CG를 받아온다(API 키 없이 로그인 세션 사용).

- --setup: 실제 Firefox를 전용 프로필(tools/.firefox_profile)로 자동화 없이 띄움 → 로그인 → 창 닫으면 저장.
  (Playwright의 개조 Firefox는 구글/X 로그인이 막혀서 쓰지 않는다 - 공용 설명은 _browser.py 참고)
- 생성: Selenium이 같은 Firefox + 프로필로 프롬프트 전송 → 새로 생긴 큰 이미지를 받아 PNG 저장.
- Grok 화면 구조는 자주 바뀌므로 아래 상수만 고치면 되게 모아뒀다. 실패하면 tools/.grok_debug.png.

사용 예
  python tools/grok_browser.py --setup
  python tools/grok_browser.py --type character --prompt "..." --out "Assets/.../HYEIN_SMUG.png" --prep-standing
  python tools/grok_browser.py --type cg --prompt "..." --out "Assets/.../CG_Q05_HYEIN_BARCODE.png"
  python tools/grok_browser.py --type character --ref concept.png --ref ARIN_IDLE.png --prompt "..." --out ...
    (--ref = 참고 이미지 업로드(여러 장 가능). 캐릭터 고정(기본형 컨셉)이나 다른 히로인 스탠딩 구도를 보여줄 때.
     프롬프트에 "첫 번째 이미지의 캐릭터를, 두 번째 이미지 구도로"처럼 각 이미지의 역할을 적어줄 것)

환경: pip install selenium requests pillow numpy scipy (Firefox 설치 필요)
주의: 생성 중에는 --setup 창(같은 프로필)을 닫아둘 것. 평소 쓰는 Firefox는 켜져 있어도 된다.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

from _browser import (big_image_srcs, click_first_xpath, debug_shot, fetch_image, find_exe, first_visible_css,
                      manual_login, wait_new_images)
from _common import TOOLS_DIR, refresh_hint, resolve_asset_path

PROFILE_DIR = TOOLS_DIR / ".firefox_profile"
DEBUG_SHOT = TOOLS_DIR / ".grok_debug.png"
FIREFOX_CANDIDATES = [r"C:\Program Files\Mozilla Firefox\firefox.exe", r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"]

# ── 화면 구조가 바뀌면 여기만 고친다 ──────────────────────────────────────────
HOME_URL = "https://grok.com"
IMAGINE_URL = "https://grok.com/imagine"   # 이미지 생성 전용 화면(입력창이 안 보이면 HOME_URL 채팅으로 폴백)
PROMPT_CSS = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
FILE_INPUT_CSS = "input[type='file']"   # 첨부(참고 이미지) - 숨김 input이라도 send_keys로 파일 경로를 넣을 수 있다
ASPECT_MENU_XPATH = ["//button[contains(@aria-label,'spect')]", "//button[contains(.,'Aspect')]", "//button[contains(.,'비율')]"]
ASPECT = {
    "character": ("9:16", "vertical 9:16 portrait, single character, upper body to thighs, plain pure white background"),
    "cg": ("16:9", "horizontal 16:9 cinematic event CG, detailed background"),
    "icon": ("1:1", "square 1:1"),
}
# ────────────────────────────────────────────────────────────────────────────


def firefox_exe() -> str:
    return find_exe(FIREFOX_CANDIDATES, "firefox")


def setup() -> None:
    manual_login([firefox_exe(), "-no-remote", "-profile", str(PROFILE_DIR), HOME_URL], PROFILE_DIR, "grok.com")


def make_driver(headless: bool):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options

    if not PROFILE_DIR.exists():
        sys.exit("[grok] 로그인 세션이 없습니다. 먼저 python tools/grok_browser.py --setup")
    opts = Options()
    opts.binary_location = firefox_exe()
    if headless:
        opts.add_argument("-headless")
    opts.add_argument("-profile")
    opts.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    return driver


def try_select_aspect(driver, ratio: str) -> bool:
    if click_first_xpath(driver, ASPECT_MENU_XPATH):
        if click_first_xpath(driver, [f"//*[self::button or @role='menuitem' or @role='option'][contains(.,'{ratio}')]"], 2):
            return True
    return click_first_xpath(driver, [f"//button[contains(.,'{ratio}')]"], 0.8)


def attach_references(driver, paths: list[str]) -> None:
    """참고 이미지를 Grok 입력창에 첨부한다. 글 묘사만으로는 얼굴/구도가 매번 달라지므로(2026-10 테스트) 캐릭터
    기본형이나 기존 스탠딩을 직접 보여주는 게 훨씬 안정적이다. webp 등은 PNG로 바꿔서 올린다."""
    import time

    from PIL import Image
    from selenium.webdriver.common.by import By

    files = []
    for p in paths:
        src = resolve_asset_path(p)
        if not src.exists():
            raise RuntimeError(f"참고 이미지가 없습니다: {src}")
        if src.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            conv = TOOLS_DIR / f".grok_ref_{src.stem}.png"
            Image.open(src).convert("RGB").save(conv)
            src = conv
        files.append(str(src))

    inputs = driver.find_elements(By.CSS_SELECTOR, FILE_INPUT_CSS)
    if not inputs:
        raise RuntimeError("첨부용 파일 입력을 찾지 못했습니다(Grok 화면 구조 변경? FILE_INPUT_CSS 확인).")
    target = next((i for i in inputs if i.get_attribute("multiple") is not None), inputs[0])
    if len(files) > 1 and target.get_attribute("multiple") is None:
        for f in files:  # 한 장씩만 받는 input이면 하나씩 넣는다
            target.send_keys(f)
            time.sleep(3)
    else:
        target.send_keys("\n".join(files))
    time.sleep(4 + 2 * len(files))  # 업로드/미리보기 생성 대기
    print(f"[grok] 참고 이미지 {len(files)}장 첨부")
    return files


SAME_AS_REF = 15  # _ref_diff가 이보다 작으면 첨부한 참고 그림 그 자체로 본다


def _ref_diff(a, b) -> float:
    """참고 그림과의 차이 점수(블러 후 최대 픽셀 차). 재표시/재압축 0~4, 표정만 바꾼 편집 43 이상(2026-10-07 측정)."""
    import numpy as np
    from scipy import ndimage

    size = (504, 896) if a.height >= a.width else (896, 504)
    x = np.asarray(a.convert("L").resize(size), dtype=float)
    y = np.asarray(b.convert("L").resize(size), dtype=float)
    return float(ndimage.gaussian_filter(np.abs(x - y), 3).max())


def _looks_same(a, b) -> bool:
    """두 이미지가 사실상 같은 그림인지. 평균 차이만 보면 "표정만 바꾼 편집 결과"(얼굴 일부만 다름)까지 같은
    그림으로 걸러버리므로(2026-10-07 표정 9장 전부 버려짐) 국소적으로 크게 달라진 곳을 본다."""
    return _ref_diff(a, b) < SAME_AS_REF


def generate_image(prompt: str, kind: str = "character", timeout: int = 180, headless: bool = False, pick: int = 0,
                   refs: list[str] | None = None):
    """프롬프트를 보내고 생성된 이미지(PIL.Image)를 돌려준다(다른 스크립트에서 import 가능)."""
    from selenium.webdriver.common.keys import Keys

    ratio, hint = ASPECT[kind]
    driver = make_driver(headless)
    sent = False  # 프롬프트를 실제로 보냈는지(사용량 기록 기준)
    try:
        driver.set_script_timeout(90)
        driver.get(IMAGINE_URL)
        box = first_visible_css(driver, PROMPT_CSS, 15)
        if box is None:
            driver.get(HOME_URL)
            box = first_visible_css(driver, PROMPT_CSS, 20)
        if box is None:
            raise RuntimeError("프롬프트 입력창을 찾지 못했습니다(로그인 만료? → --setup 다시).")
        picked = try_select_aspect(driver, ratio)
        ref_imgs = []
        if refs:
            from PIL import Image

            ref_imgs = [Image.open(f) for f in attach_references(driver, refs)]
            box = first_visible_css(driver, PROMPT_CSS, 10) or box
        text = " ".join(f"{prompt} ({hint}, aspect ratio {ratio})".split())  # Grok 입력창은 줄바꿈 = 전송
        before = set(big_image_srcs(driver))
        box.click()
        box.send_keys(text)
        box.send_keys(Keys.ENTER)
        sent = True
        print(f"[grok] 전송 완료 (비율 버튼 {'선택' if picked else '못 찾음 → 프롬프트로만 요청'}). 생성 대기 중...")
        import time

        end = time.time() + timeout
        filtered = []  # 참고 그림으로 판정해 걸러낸 것들(점수, 이미지) - 판정이 틀렸을 때의 안전망
        while True:
            # 걸러낸 게 이미 있으면 "진짜 결과"를 오래 기다리지 않는다: 45초 안에 더 안 나오면 걸러낸 것 중
            # 참고 그림과 가장 다른 걸 결과로 쓴다(2026-10-07 판정 오류로 매 장 6분씩 헛기다린 일 방지).
            wait = int(end - time.time()) if not filtered else min(45, int(end - time.time()))
            new = wait_new_images(driver, before, max(5, wait))
            if not new:
                if filtered:
                    score, img = max(filtered, key=lambda t: t[0])
                    if score > 5:
                        print(f"[grok] 경고: 새 결과가 더 안 나와 참고 그림과 가장 다른 이미지(차이 {score:.0f})를 결과로 씁니다 - 꼭 확인할 것")
                        log_usage(kind, len(refs or []), 1, "ok (fallback)", scan_quota_text(driver))
                        return img
                raise RuntimeError(f"{timeout}초 안에 생성된 이미지를 찾지 못했습니다.")
            results = []
            for src in new:
                got = fetch_image(driver, src, HOME_URL)
                scores = [_ref_diff(got, r) for r in ref_imgs]
                if scores and min(scores) < SAME_AS_REF:
                    before.add(src)  # 첨부한 참고 이미지가 메시지에 다시 뜬 것 - 결과 아님
                    filtered.append((min(scores), got))
                else:
                    results.append(got)
            if results:
                img = results[min(pick, len(results) - 1)]
                print(f"[grok] 결과 {len(results)}장 중 {pick}번 ({img.size[0]}x{img.size[1]})")
                log_usage(kind, len(refs or []), len(results), "ok", scan_quota_text(driver))
                return img
            if time.time() >= end:
                raise RuntimeError("참고 이미지 말고 새로 생성된 이미지가 나오지 않았습니다.")
    except Exception as e:
        debug_shot(driver, DEBUG_SHOT)
        if sent:
            log_usage(kind, len(refs or []), 0, f"fail: {e}"[:120], scan_quota_text(driver))
        raise SystemExit(f"[grok] 실패: {e}")
    finally:
        driver.quit()
        if sent:
            print_usage_summary()


# ─── 사용량 기록 ────────────────────────────────────────────────────────────
# Grok 계정은 팀 공용이라 "이번에 얼마나 썼는지"를 매번 알려야 한다. Grok 화면에는 정확한 잔여량 API가 없어서,
# 전송할 때마다 tools/.grok_usage.csv에 한 줄씩 남기고(요청 수 = 실제로 프롬프트를 보낸 횟수, 실패 포함),
# 페이지에 한도/남은 횟수 같은 문구가 보이면 그것도 같이 적는다.

USAGE_LOG = TOOLS_DIR / ".grok_usage.csv"
QUOTA_WORDS = ("limit", "remaining", "quota", "upgrade", "한도", "남은", "제한", "rate")


def scan_quota_text(driver) -> str:
    try:
        text = driver.execute_script("return document.body ? document.body.innerText : ''") or ""
    except Exception:
        return ""
    hits = [ln.strip() for ln in text.splitlines()
            if 4 < len(ln.strip()) < 160 and any(w in ln.lower() for w in QUOTA_WORDS)]
    return " | ".join(dict.fromkeys(hits))[:300]


def log_usage(kind: str, refs: int, images: int, status: str, quota: str) -> None:
    import csv
    from datetime import datetime

    new = not USAGE_LOG.exists()
    with open(USAGE_LOG, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "type", "refs", "images", "status", "page_quota_text"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), kind, refs, images, status, quota])
    if quota:
        print(f"[grok] 화면의 한도 관련 문구: {quota}")


def print_usage_summary() -> None:
    import csv
    from datetime import datetime

    if not USAGE_LOG.exists():
        return
    rows = list(csv.DictReader(open(USAGE_LOG, encoding="utf-8")))
    today = datetime.now().strftime("%Y-%m-%d")
    month = today[:7]
    t = [r for r in rows if r["time"].startswith(today)]
    m = [r for r in rows if r["time"].startswith(month)]
    print(f"[grok] 사용량: 오늘 요청 {len(t)}회(생성 이미지 {sum(int(r['images']) for r in t)}장) / "
          f"이번 달 {len(m)}회 - 기록 {USAGE_LOG.name}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--setup", action="store_true", help="실제 Firefox(전용 프로필)로 grok.com 수동 로그인 → 창 닫으면 저장")
    ap.add_argument("--prompt", help="이미지 생성 프롬프트")
    ap.add_argument("--type", choices=list(ASPECT), default="character", help="character=9:16, cg=16:9, icon=1:1")
    ap.add_argument("--out", help="저장 경로(Assets/... 상대 또는 절대, PNG)")
    ap.add_argument("--pick", type=int, default=0, help="결과가 여러 장일 때 몇 번째를 저장할지(0부터)")
    ap.add_argument("--timeout", type=int, default=180, help="생성 대기 최대 초")
    ap.add_argument("--headless", action="store_true", help="창 없이 실행(보안 확인이 뜨면 실패할 수 있음)")
    ap.add_argument("--keep-raw", action="store_true", help="후처리 전 원본도 *_raw.png로 저장")
    ap.add_argument("--ref", action="append", default=[], help="참고 이미지 첨부(여러 번 가능): 캐릭터 기본형/구도 예시")
    ap.add_argument("--prep-standing", action="store_true", help="character일 때 스탠딩 규격(692x2048 투명) 후처리까지")
    ap.add_argument("--usage", action="store_true", help="지금까지의 사용량(오늘/이번 달 요청 수)만 출력")
    args = ap.parse_args()

    if args.usage:
        print_usage_summary()
        return
    if args.setup:
        setup()
        return
    if not args.prompt or not args.out:
        ap.error("--prompt와 --out이 필요합니다(처음이면 --setup 먼저).")

    out = resolve_asset_path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img = generate_image(args.prompt, args.type, args.timeout, args.headless, args.pick, args.ref)
    if args.keep_raw:
        img.save(out.with_name(out.stem + "_raw.png"), "PNG")
    if args.type == "cg" and img.size != (1920, 1080):
        # 기존 이벤트 CG 규격(1920x1080)에 맞춘다. Grok은 1792x1008 등으로 주므로 16:9 중앙 크롭 후 확대.
        from PIL import Image

        w, h = img.size
        cw, ch = (w, round(w * 9 / 16)) if w * 9 / 16 <= h else (round(h * 16 / 9), h)
        img = img.crop(((w - cw) // 2, (h - ch) // 2, (w - cw) // 2 + cw, (h - ch) // 2 + ch)).resize((1920, 1080), Image.LANCZOS)
        img = img.convert("RGB")
    img.convert("RGB" if args.type == "cg" else "RGBA").save(out, "PNG")
    if args.prep_standing and args.type == "character":
        subprocess.run([sys.executable, str(TOOLS_DIR / "prep_standing.py"), "--in", str(out), "--out", str(out)], check=True)
    refresh_hint(out)


if __name__ == "__main__":
    main()
