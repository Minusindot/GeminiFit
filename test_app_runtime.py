import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def test():
    # Test with headless Edge/Chrome
    opts = ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=opts)
    try:
        url = Path("index.html").resolve().as_uri()
        driver.get(url)
        print("Page loaded successfully:", driver.title)

        # Check JS logs
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l.get("level") == "SEVERE"]
        if severe_errors:
            print("Browser severe errors:", severe_errors)
        else:
            print("No severe browser errors!")

        # Open Gallery Modal
        driver.execute_script("openGalleryModal();")
        print("openGalleryModal executed!")

        # Check gallery tabs
        for tab_id in ['galTabAll', 'galTabGemini', 'galTabKotone', 'galTabMio', 'galTabDual', 'galTabSd']:
            btn = driver.find_element(By.ID, tab_id)
            print(f"Tab {tab_id}: '{btn.text}'")

        # Test switching to SD tab
        driver.execute_script("renderGalleryGrid('sd');")
        cards = driver.find_elements(By.CSS_SELECTOR, "#galleryGridContainer > div")
        print(f"SD tab cards rendered: {len(cards)}")

        # Test switching to all tab
        driver.execute_script("renderGalleryGrid('all');")
        all_cards = driver.find_elements(By.CSS_SELECTOR, "#galleryGridContainer > div")
        print(f"All tab cards rendered: {len(all_cards)}")

        # Close modal
        driver.execute_script("closeGalleryModal();")

        # Take screenshot of main stage
        driver.set_window_size(430, 932)
        driver.save_screenshot("test_app_mobile_90.png")
        print("Mobile stage screenshot saved: test_app_mobile_90.png")

        driver.set_window_size(1280, 800)
        driver.save_screenshot("test_app_pc_90.png")
        print("PC stage screenshot saved: test_app_pc_90.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    test()
