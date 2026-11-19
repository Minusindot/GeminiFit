"""3인 히로인(제미니 / 코토네 / 미오) 각 5종 미연시 이벤트 CG 일괄 수렴진화 생성 스크립트
"""
from pathlib import Path
import shutil
from evolve_pool import KOTONE_POOL, BASE_DIR, run_batch

def prepare_kotone_existing():
    # 코토네 기존 01, 02 리네이밍 정리 (03~05 구버전 동일 복장은 새 데이트 의상 컷으로 교체)
    if (KOTONE_POOL / "01_gemini_main_studio.png").exists():
        shutil.move(str(KOTONE_POOL / "01_gemini_main_studio.png"), str(KOTONE_POOL / "01_kotone_studio.png"))
    if (KOTONE_POOL / "02_gemini_morning_sunlight.png").exists():
        shutil.move(str(KOTONE_POOL / "02_gemini_morning_sunlight.png"), str(KOTONE_POOL / "02_kotone_morning.png"))
    for old in ["03_gemini_matcha_tea.png", "04_gemini_evening_window.png", "05_gemini_home_cafe.png"]:
        p = KOTONE_POOL / old
        if p.exists():
            p.unlink()

JOBS = [
    # ── 1. 신규 오리지널 캐릭터: 제미니 (5종 전부 다른 의상/장소/미연시 시츄) ──
    (
        "gemini",
        "main_vip",
        "01_gemini_main.png",
        "gemini_01_main.png",
        "Standing closely in a sunlit private VIP fitness studio. Wearing a stylish black and rose-gold off-shoulder cropped zip-up athletic top and a cute black ribbon choker with a tiny gold cat bell. Her short milk-tea ash-blonde bob has a distinct pure white front streak in the bangs and cute fluffy cat ears on top. Looking at viewer with half-lidded teasing golden-amber cat eyes, warm blush, and a cute tiny single fang showing on her smug affectionate smile. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "gemini",
        "matcha_neko",
        "02_gemini_matcha.png",
        "gemini_02_matcha.png",
        "Sitting in a warm sunlit traditional tatami tea room (chashitsu). Wearing a glamorous modern red and white off-shoulder shrine-maiden neko haori outfit with white fluffy fur trim and a black-and-white waist ribbon with gold cat bells (matching the character reference outfit). Holding a ceramic matcha tea bowl with green froth in both hands, blushing deeply with a shy yet teasing tsundere fang smile looking up at viewer. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "gemini",
        "rehab_touch",
        "03_gemini_rehab_touch.png",
        "gemini_03_rehab_touch.png",
        "Kneeling closely on a yoga mat in a sunset-lit private pilates room during a 1-on-1 wrist rehabilitation session. Wearing a form-fitting pastel-grey halter-neck sports top with a loose white cardigan slipping off one shoulder. Gently holding the viewer's wrist with both hands, leaning in close, looking up with a seductive, caring, playfully smug golden-amber cat-eye gaze and tiny fang smile, glowing sunset light. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "gemini",
        "pool_bikini",
        "04_gemini_pool_bikini.png",
        "gemini_04_pool_bikini.png",
        "Leaning on the edge of a sparkling turquoise luxury outdoor swimming pool in summer sunlight. Wearing a chic black halter-neck bikini (inspired by the pool reference image) with cute X and red heart hairpins clipped to her white-streaked ash-blonde bob with cat ears. Glistening water droplets on her collarbone and shoulders, flushed cheeks, gazing intimately at the viewer with sultry half-lidded amber eyes. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "gemini",
        "night_secret",
        "05_gemini_night_secret.png",
        "gemini_05_night_secret.png",
        "Standing by a luxury penthouse balcony window at night with warm indoor fairy lights and city bokeh behind her, celebrating the end of intermittent fasting. Wearing an elegant burgundy-red silk off-shoulder night slip dress with a delicate choker. Holding a crystal glass of sparkling lemon water, tilting her head with an alluring, affectionate sleepy cat-like smile and tiny fang. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),

    # ── 2. 코토네 (학원마스 후지타 코토네: 나머지 3종의 완전히 다른 의상/장소 데이트 CG) ──
    (
        "kotone",
        "cafe_date",
        "03_kotone_cafe_date.png",
        "kotone_03_cafe_date.png",
        "On a romantic weekend cafe date at a sunny European-style outdoor terrace cafe. Wearing a cute casual off-shoulder cream knit sweater, a pastel pink beret hat, and a dainty necklace (completely different from her tracksuit). Sitting across the table with an iced coffee and berry parfait, clasping her hands together happily with sparkling amber eyes and a beaming, slightly spoiled 'Hehe, thank you for treating me Producer!' smile. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "kotone",
        "rain_locker",
        "04_kotone_rain_locker.png",
        "kotone_04_rain_locker.png",
        "Caught in a sudden evening rain shower, sheltering alone with the viewer in a warm softly-lit gym locker room. Wearing a slightly damp oversized white dress shirt over a pastel camisole, drying her blonde twin braids with a fluffy white towel. Flushed red cheeks, shy flustered heart-fluttering expression looking up closely at the viewer. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "kotone",
        "festival_yukata",
        "05_kotone_festival_yukata.png",
        "kotone_05_festival_yukata.png",
        "At a romantic summer night riverside festival with warm paper lanterns and colorful fireworks glowing in the night sky behind her. Wearing a gorgeous pastel-yellow and coral-pink floral Japanese yukata with a ribbon obi, holding a glossy red candy apple. Turning back toward the viewer with a breathtakingly sweet, affectionate blushing smile. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),

    # ── 3. 미오 (혼다 미오 + 학원마스 화풍: 나머지 4종의 완전히 다른 의상/장소 데이트 CG) ──
    (
        "mio",
        "park_run",
        "02_mio_park_run.png",
        "mio_02_park_run.png",
        "Resting together under cherry blossom and green trees in a sunlit morning park right after an outdoor jog. Wearing a fitted white athletic crop sports top with a pastel-orange headband pushing back her cute side bangs, a towel around her neck. Healthy glowing skin with a few sparkling sweat droplets, handing a cold sports water bottle toward the viewer with a radiant heart-melting smile. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "mio",
        "poolside",
        "03_mio_poolside.png",
        "mio_03_poolside.png",
        "At a sunlit luxury resort poolside during an aqua-therapy vacation date. Wearing a cute sporty yellow-and-white frilled bikini with an open sheer white summer hoodie over her shoulders. Sitting at the edge of the sparkling blue pool, hair slightly damp, winking playfully with a bright blushing smile at the viewer. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "mio",
        "cheer_stage",
        "04_mio_cheer_stage.png",
        "mio_04_cheer_stage.png",
        "Performing a private 1-on-1 cheerleading routine in a brightly lit evening stadium just for the viewer. Wearing a dazzling yellow, white, and navy sleeveless cheerleader crop uniform with pleated skirt collar details, holding sparkling gold pom-poms near her cheek, energetic loving gaze with warm blush. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
    (
        "mio",
        "sunset_beach",
        "05_mio_sunset_beach.png",
        "mio_05_sunset_beach.png",
        "Walking together along a golden-pink sunset ocean beach on a romantic evening date. Wearing a pure white lace off-shoulder sundress and holding a straw sun hat as the sea breeze gently blows her caramel-brown bob hair. Looking at the viewer with a tender, unusually shy and deeply romantic expression with glowing sunset rim lighting. Close-up upper body dating-sim event CG, aspect ratio 9:16"
    ),
]

if __name__ == "__main__":
    prepare_kotone_existing()
    run_batch(JOBS)
