"""Automated Grok Batch Generator for 60 New Situation CGs (20 per Heroine: Gemini, Kotone, Mio)
Covers Kotonoha Teahouse lessons (1~12), Kansai travel, urban daily life, 4 seasons, fitness care, and Morikinoko SD comedy.
Resumable: skips any image that is already generated on disk.
"""
from __future__ import annotations
import sys
import time
import shutil
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from evolve_pool import (
    BASE_DIR,
    FIREFOX_EXE,
    PROFILE_DIR,
    SAME_AS_REF,
    ref_diff,
)
from _browser import big_image_srcs, fetch_image, first_visible_css, wait_new_images

ART_DIR = Path(r"C:\Users\scmms\.gemini\antigravity\brain\e596d252-7278-4ce7-b71b-d432f3046069")
REPO_DIR = BASE_DIR / "image" / "90 repository"
SD_POOL = REPO_DIR / "morikinoko_sd"

# Core Character Reference Paths (100% SFW clean Grok survivor PNGs)
REF_GEMINI_MAIN = REPO_DIR / "gemini" / "01_gemini_main.png"
REF_GEMINI_TEA = REPO_DIR / "gemini" / "02_gemini_matcha.png"
REF_GEMINI_GYM = REPO_DIR / "gemini" / "07_gemini_cafe_pout.png"

REF_KOTONE_MAIN = REPO_DIR / "kotone" / "01_kotone_studio.png"
REF_KOTONE_CAFE = REPO_DIR / "kotone" / "03_kotone_cafe_date.png"

REF_MIO_MAIN = REPO_DIR / "reference_mio" / "07_mio_official_standing.png"
REF_MIO_RUN = REPO_DIR / "mio" / "02_mio_park_run.png"

REF_SD_BEAN = BASE_DIR / "image" / "03 gemini" / "sd_gemini_02_matcha_whisk.png"

_UNSAFE_REF_KEYWORDS = ("pool", "bikini", "beach", "locker", "towel", "bed", "night_secret", "rain")
GEMINI_POOL_FILES = [
    p for p in sorted((REPO_DIR / "gemini").glob("*.png"))
    if not any(k in p.name for k in _UNSAFE_REF_KEYWORDS)
]
KOTONE_POOL_FILES = [
    p for p in sorted((REPO_DIR / "kotone").glob("*.png"))
    if not any(k in p.name for k in _UNSAFE_REF_KEYWORDS)
]
MIO_POOL_FILES = [
    p for p in sorted((REPO_DIR / "mio").glob("*.png"))
    if not any(k in p.name for k in _UNSAFE_REF_KEYWORDS)
]

# 60 Bespoke Camera Angles, Framing & Head/Body Orientations to prevent repetitive frontal poses
CAMERA_BY_FILE = {
    "gemini_26_kyoto_teahouse.png": "OVER-THE-SHOULDER TATAMI TEA CEREMONY SHOT from behind her right shoulder looking down at her hands whisking green matcha in a ceramic bowl on the tatami mat, her face turned 3/4 back toward the viewer with a serene Kyoto ojousama smile.",
    "gemini_27_kyoto_cherry_walk.png": "LOW-ANGLE WALKING-AHEAD REAR-3/4 VIEW on a stone-paved Gion street under weeping cherry blossoms, her kimono sleeves fluttering in the breeze as she pauses and glances back over her left shoulder.",
    "gemini_28_genkan_shoes_off.png": "LOW-ANGLE FLOOR-LEVEL POV from the stone entryway looking UP at her full body stepping onto the raised wooden tatami floor, her body turned 45-degrees sideways bending down toward the camera.",
    "mio_26_sneaker_showoff_grin.png": "EXTREME LOW-ANGLE WORM'S-EYE WIDE SHOT from ground level with her lifted white sneaker sole huge in the foreground perspective, her torso leaning back dynamically.",
    "kotone_26_osaka_bargain_sparkle.png": "OVER-THE-SHOULDER SHOPKEEPER POV looking slightly DOWN at her leaning far forward across a market stall counter, head tilted UP with chin resting near her clasped hands.",
    "gemini_29_wagashi_sweet_smile.png": "SIDE-PROFILE 3/4 TABLE-LEVEL MACRO SHOT with a matcha bowl blurred in the extreme foreground, her face turned in delicate side profile looking toward the garden window.",
    "kotone_27_matcha_bitter_wink.png": "HIGH-ANGLE OVERHEAD BIRD'S-EYE POV looking down at her sitting cross-legged on tatami, hunching her shoulders playfully as she peeks up over the rim of the ceramic tea bowl.",
    "mio_27_ramen_counter_slurp.png": "SIDE-COUNTER HORIZONTAL CINEMATIC SHOT from the seat next to her, showing her in 90-degree side profile stretching one arm high into the air toward the kitchen while turning her head toward the camera.",
    "gemini_30_osaka_takoyaki_tsukkomi.png": "DYNAMIC DUTCH-ANGLE (15-DEGREE TILT) ACTION SHOT from waist level, her body twisted mid-motion swinging a paper fan forward toward the lens in dramatic foreshortening.",
    "kotone_28_shrine_omikuji_cheer.png": "LOW-ANGLE SKYWARD SHOT looking up against red torii gates and blue sky as she leaps mid-air with both arms stretched high overhead, hair ribbons flying.",
    "mio_28_arashiyama_bamboo_jog.png": "REAR-3/4 BACK VIEW FULL-BODY TRACKING SHOT following behind her as she runs away down the bamboo path, twisting her upper back and head 150-degrees back over her left shoulder.",
    "gemini_31_ryokan_yukata_lantern.png": "CINEMATIC WIDE NIGHT CORRIDOR SHOT from the side, her body facing away toward the dark garden pond while glancing sideways over her shoulder, illuminated from below by the handheld lantern.",
    "kotone_29_ryokan_table_feast.png": "TABLE-SURFACE LOW-ANGLE POV looking across plates of colorful ryokan food in the foreground toward her leaning down close to the dishes.",
    "mio_29_onsen_milk_cheers.png": "HEAD-TILTED-BACK SIDE PROFILE SHOT as she tilts her head 60-degrees upward drinking from a glass milk bottle, one hand on hip, seen from a cool side-angle.",
    "gemini_32_subway_ic_card_tap.png": "REAR OVER-THE-SHOULDER WALKING VIEW showing her back and flowing coat as she walks ahead through the ticket gate, turning only her head back in sharp profile.",
    "kotone_30_clock_panic_sprint.png": "EXTREME DUTCH-TILT MOTION-BLUR ACTION SHOT from a low diagonal corner as she sprints past the camera, leaning forward at a 40-degree running angle.",
    "mio_30_bus_stop_map_point.png": "WIDE TWO-POINT PERSPECTIVE STREET SHOT from behind the open paper map in the foreground, her arm reaching right toward the camera lens pointing far into the distance.",
    "gemini_33_train_window_sunset.png": "90-DEGREE SIDE PROFILE SILHOUETTE-LIT SHOT seated against the glowing orange train window, her face in pure side profile looking down at the earphone in her hand before glancing sideways.",
    "kotone_31_ticket_machine_confused.png": "THREE-QUARTER BACK VIEW looking at the glowing ticket machine screen over her shoulder, her reflection faintly visible as she scratches the back of her head.",
    "mio_31_train_strap_smile.png": "LOW-ANGLE UPWARD SHOT from a seated passenger's eye-level looking up at her standing tall holding the high overhead train strap, leaning diagonally.",
    "gemini_34_wrist_watch_late_glare.png": "DRAMATIC FORESHORTENED CLOSE-UP where her wrist and watch are thrust close to the camera lens in the foreground while she leans back with arms crossed and chin raised haughtily.",
    "kotone_32_supermarket_protein_cart.png": "INSIDE-THE-SHOPPING-CART LOW POV looking up from inside the wire basket as she leans both elbows onto the cart handle looking down at the camera.",
    "mio_32_bento_lunchbox_proud.png": "TOP-DOWN 60-DEGREE HIGH-ANGLE POV from a standing viewer looking down at her sitting on a low bench holding the open bento box up toward the sky.",
    "gemini_35_bookstore_kanji_teach.png": "INTIMATE SIDE-BY-SIDE DESK-LEVEL POV where she leans her head down onto her folded arm on the desk, looking sideways and slightly up at the viewer through round glasses.",
    "kotone_33_cafe_study_pencil.png": "SLIGHT HIGH-ANGLE ACROSS-THE-BOOTH SHOT showing her slumped backwards into the cafe sofa with her head tilted far back balancing a pencil on her upper lip.",
    "mio_33_sports_shop_shoes_try.png": "CROUCHING FLOOR-LEVEL SHOT where she is bent all the way forward tying her shoelace near the floor, looking up from beneath her eyebrows with her chin near her knees.",
    "gemini_40_shoulder_massage_care.png": "OVER-THE-SHOULDER REAR POV where the viewer is sitting in front and she is kneeling behind the viewer's back, leaning her chin right next to the camera's left edge.",
    "kotone_38_calf_cramp_tears.png": "GROUND-LEVEL HORIZONTAL SHOT of her sitting flat on the gym mat with legs stretched toward the camera in perspective, curling her torso forward over her knee.",
    "mio_38_bicep_flex_wink.png": "MIRROR-REFLECTION DOUBLE-ANGLE SHOT showing her from the rear-side in the foreground while her beaming face and flexing bicep are captured clearly in the gym mirror.",
    "gemini_41_kitchen_apron_cooking.png": "COUNTER-DEPTH OVER-THE-STOVE SHOT with a steaming pan in the lower foreground, her body angled sideways at the stove turning her upper torso to reach a spoon toward the lens.",
    "kotone_39_salad_bowl_fork_smile.png": "EXTREME FORESHORTENED POV where the fork with a cherry tomato is sharp and large right in front of the camera lens, and she is leaning across the table in the background.",
    "mio_39_timer_stopwatch_shout.png": "DYNAMIC LOW-ANGLE COACH STANCE with one foot stepped up on a plyo box, leaning her elbow on her raised knee while thrusting the stopwatch toward the viewer.",
    "gemini_43_tape_measure_waist_smirk.png": "CIRCLING SIDE-AROUND POV where she stands slightly behind and to the side of the viewer, wrapping the yellow tape measure around the camera frame itself.",
    "kotone_40_scale_peek_fingers.png": "STEEP BIRD'S-EYE VERTICAL OVERHEAD SHOT from directly above her head looking straight down at the top of her blonde braids, her hands covering her face, standing on the digital scale below.",
    "mio_40_post_run_grass_lie_down.png": "PURE TOP-DOWN 90-DEGREE ZENITH OVERHEAD SHOT looking straight down at her lying flat on her back on the green grass, her hair fanned out on the ground and arms stretched wide.",
    "gemini_42_protein_toast_cheers.png": "LOUNGE SOFA RECLINING SHOT where she is leaning sideways against sofa cushions with legs tucked to the side, raising her glass diagonally across the frame.",
    "kotone_41_confetti_medal_hug.png": "WIDE-ANGLE FISHEYE-STYLE CLOSE-UP as she lunges forward into the camera frame with arms wrapping around the lens, tilted head and dynamic perspective.",
    "mio_41_protein_jug_chug_victory.png": "SILHOUETTE SUNSET LOW-ANGLE HERO SHOT from knee level looking up against the blazing orange sky as she stands on a rooftop bench raising the shaker high into the sun.",
    "gemini_36_summer_handfan_ice.png": "ENGAWA VERANDA SIDE-LONG SHOT showing her sitting sideways on the wooden porch edge with bare legs dangling down into the garden, leaning back on one hand.",
    "kotone_34_cherry_blossom_bento.png": "LYING-ON-PICNIC-BLANKET EYE-LEVEL POV where she is lying on her stomach on the picnic mat propped up on both elbows, kicking her feet up behind her.",
    "mio_34_spring_wind_stretch.png": "THREE-QUARTER REAR VIEW looking toward the river and cherry trees as she arches her back and stretches both arms behind her head, looking back sideways.",
    "gemini_37_autumn_maple_teacup.png": "FRAMED-THROUGH-MAPLE-BRANCHES SHOT with blurred red autumn leaves in the immediate foreground, showing her in serene side profile looking up at falling leaves.",
    "kotone_35_summer_sunscreen_hat.png": "WINDY SEASIDE BACK-TURN SHOT where her body faces the ocean waves, sundress blowing in the wind, turning her head and upper shoulder back while holding down her wide straw hat.",
    "mio_35_summer_water_hose_laugh.png": "LOW-ANGLE SIDE SPLASH ACTION SHOT as she bends sideways over an outdoor faucet, splashing an arc of sparkling water droplets across the diagonal of the frame.",
    "gemini_38_winter_kotatsu_mandarin.png": "FLOOR-LEVEL KOTATSU POV where she has her chin resting flat on top of the kotatsu table surface like a sleepy cat, looking horizontally straight into the lens.",
    "kotone_36_autumn_sweet_potato.png": "BENCH SIDE-ANGLE PROFILE SHOT sitting sideways with knees pulled up to her chest on a park bench, blowing steam off a sweet potato held close to her lips.",
    "mio_36_autumn_sunset_track_jacket.png": "WALKING-AWAY LOOK-BACK SHOT down an autumn leaf trail, seen from waist-to-head in 3/4 rear profile as she tugs her jacket zipper up to her chin.",
    "gemini_39_snowy_muffler_blush.png": "HIGH-ANGLE TALL-VIEWER POV looking down at her buried deep in a thick winter scarf under falling snow, her face tilted upward toward the tall viewer with snow on her cat ears.",
    "kotone_37_winter_earmuffs_hotpack.png": "EXTREME CLOSE-UP OFF-CENTER COMPOSITION where her gloved hands press a warm hand-warmer right against the side of the camera frame, her head tilted 30-degrees the opposite way.",
    "mio_37_winter_breath_jogging_gloves.png": "MID-STRIDE DIAGONAL RUNNING SHOT from a low corner angle, capturing her dynamic knee lift and gloved fists pumping with clouds of white breath trailing behind.",
    "gemini_44_extreme_blush_hide_face.png": "DRAMATIC THREE-QUARTER TURN-AWAY PORTRAIT where she turns her shoulders and head away in embarrassment, hiding her mouth behind a folding fan while peeking sideways with one eye.",
    "gemini_45_ikezu_cold_smile_fan.png": "LOW-ANGLE DOMINANT OJOUSAMA POV looking up at her tilting her chin down haughtily, looking down her nose at the viewer with half-lidded smiling eyes and dark aura.",
    "kotone_42_pout_cheeks_angry_cute.png": "SIDE-TURNED SULKING POSE where her body and crossed arms are turned 90-degrees away from the viewer, twisting only her puffed-cheek pouting face sideways to glare cutely.",
    "kotone_43_starry_eyes_praise.png": "HIGH-ANGLE UPWARD-GAZE CLOSE-UP looking down at her leaning both elbows on a table and resting her chin in her palms, gazing up with giant starry eyes.",
    "mio_42_headpat_big_laugh_blush.png": "FIRST-PERSON OVERHEAD HEADPAT POV looking down at her scrunching her shoulders and tilting her head into the viewer's hand at the top of the frame.",
    "mio_43_serious_coach_gaze.png": "GROUND-LEVEL FALLEN-VIEWER POV looking up from the floor as she crouches down on one knee in front of the camera, extending an open hand right toward the lens.",
}


STYLE_SSR = (
    "CRITICAL ART STYLE: Gakumas (Gakuen Idolmaster) & Cinderella Girls official SSR anime game CG illustration, "
    "vibrant cell-shaded anime visual novel CG, cinematic lighting, clean delicate lineart, expressive anime eyes. "
    "Absolutely NO readable text, NO speech bubbles, NO watermarks, NO brand logos."
)

STYLE_SD = (
    "CRITICAL ART STYLE: Strictly draw in the exact comedy 2-head-tall chibi art style of the attached SD reference image (sd_gemini_02_matcha_whisk) — "
    "tiny super-deformed 2-head-tall mini chibi character interacting with a giant oversized prop, solid black oval bean-eyes (검은 콩눈 / 점눈), "
    "blushing cheeks, bold clean comic lineart, dynamic manga radial speed lines (집중선) on a clean white background. "
    "Absolutely NO readable text, NO speech bubbles, NO brand logos."
)

CHAR_GEMINI = (
    "CHARACTER: elegant Japanese anime idol girl from the attached reference images, long waist-length glossy raven-black hair "
    "with straight blunt bangs and cheek-length sidelocks, cute black cat ears (nekomimi) with a tiny ribbon pin, "
    "sparkling violet-amethyst eyes, graceful Kyoto lady + tsundere charm."
)

CHAR_KOTONE = (
    "CHARACTER (Fujita Kotone): cheerful blonde anime idol girl with twin braids tied with yellow ribbons, "
    "warm amber eyes, expressive eyebrows, affectionate energetic idol vibe."
)

CHAR_MIO = (
    "CHARACTER (Honda Mio): energetic athletic anime idol girl, short caramel-brown layered bob hair with flipped ends "
    "and a bouncy ahoge on top, bright honey-gold eyes, radiant sporty smile."
)

# ==============================================================================
# 60 JOBS ORDERED BY PRIORITY (Kotonoha Lesson Matchers First -> Seasons -> Expressions/SD)
# ==============================================================================
JOBS = [
    (
        "gemini_26_kyoto_teahouse.png",
        "image/03 gemini/gemini_26_kyoto_teahouse.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Inside a traditional Kyoto wooden teahouse room with open shoji doors showing a bamboo courtyard. "
        "Gemini kneeling in seiza on tatami wearing an elegant floral kimono, delicately whisking emerald-green matcha tea with a bamboo chasen, glancing back over her shoulder with a refined smile."
    ),
    (
        "gemini_27_kyoto_cherry_walk.png",
        "image/03 gemini/gemini_27_kyoto_cherry_walk.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Historic Kyoto Gion cobblestone path lined with wooden machiya townhouses and blooming weeping cherry blossom trees. "
        "Gemini walking ahead holding a traditional red paper wagasa umbrella tilted over her shoulder, turning back toward the viewer with cherry petals drifting past."
    ),
    # --------------------------------------------------------------------------
    # BATCH 1: THEME A - KOTONOHA TEAHOUSE & KANSAI TRAVEL (12 CGs)
    # --------------------------------------------------------------------------
    (
        "gemini_28_genkan_shoes_off.png",
        "image/03 gemini/gemini_28_genkan_shoes_off.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Traditional Kyoto wooden teahouse entrance (genkan) with tatami step. "
        "Gemini wearing an elegant floral kimono with white kappogi apron, stepping up onto the wooden floor in white tabi socks while pointing her index finger "
        "down at the shoes on the stone entryway with a cute scolding tsundere pout: 'No shoes inside the teahouse!'. Warm morning sunlight."
    ),
    (
        "mio_26_sneaker_showoff_grin.png",
        "image/01 mio/mio_26_sneaker_showoff_grin.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Standing outside a traditional Kyoto wooden teahouse entrance on a sunny morning. "
        "Mio wearing a sporty blue-and-white track jacket and running shorts, energetically lifting one leg high to proudly show off her brand-new sparkling white running sneakers, "
        "flashing a huge V-sign peace gesture and a beaming grin."
    ),
    (
        "kotone_26_osaka_bargain_sparkle.png",
        "image/02 kotone/kotone_26_osaka_bargain_sparkle.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Bustling Osaka shopping arcade street market. "
        "Kotone wearing cute casual streetwear with a yellow crossbody purse, clasping her hands together with a small coin purse, "
        "leaning forward with huge sparkling puppy-dog eyes begging the shopkeeper for a discount: 'Please make it a little cheaper!'. Warm lively market lanterns."
    ),
    (
        "gemini_29_wagashi_sweet_smile.png",
        "image/03 gemini/gemini_29_wagashi_sweet_smile.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Inside a sunlit Kyoto tatami teahouse room overlooking a garden. "
        "Gemini in a pastel kimono holding a small wooden pick with a pink cherry-blossom wagashi sweet near her lips, "
        "her eyes curved into happy crescent moons with a blissful gentle blush savoring the sweet flavor, a green matcha bowl on the table."
    ),
    (
        "kotone_27_matcha_bitter_wink.png",
        "image/02 kotone/kotone_27_matcha_bitter_wink.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Sitting on tatami in a traditional Japanese teahouse holding a ceramic bowl of thick green matcha tea with both hands. "
        "Kotone wearing a soft cream knit cardigan, squeezing one eye shut in a comical cute wince with her tongue slightly sticking out because the matcha is unexpectedly bitter!"
    ),
    (
        "mio_27_ramen_counter_slurp.png",
        "image/01 mio/mio_27_ramen_counter_slurp.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Cozy Osaka eatery wooden counter seat after workout. "
        "Mio in a sleeveless athletic hoodie, raising one hand cheerfully to call the staff while holding a clear glass pitcher of ice water: "
        "'Excuse me, water please!'. Energetic refreshing smile, warm restaurant glow."
    ),
    (
        "gemini_30_osaka_takoyaki_tsukkomi.png",
        "image/03 gemini/gemini_30_osaka_takoyaki_tsukkomi.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Vibrant Osaka Dotonbori canal night street with glowing neon festival lanterns. "
        "Gemini wearing a stylish modern kimono haori jacket over casual wear, holding a paper boat of steaming hot takoyaki in one hand and a folded paper fan in the other, "
        "giving a playful sharp Osaka tsukkomi gesture with a teasing smirk."
    ),
    (
        "kotone_28_shrine_omikuji_cheer.png",
        "image/02 kotone/kotone_28_shrine_omikuji_cheer.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Red torii gate courtyard of a Kyoto Shinto shrine in spring. "
        "Kotone wearing a cute yellow-ribbon spring dress, jumping with joy while holding up a paper fortune slip (Omikuji) with both hands, "
        "radiant overjoyed idol smile surrounded by soft sunlight."
    ),
    (
        "mio_28_arashiyama_bamboo_jog.png",
        "image/01 mio/mio_28_arashiyama_bamboo_jog.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Kyoto Arashiyama towering green bamboo grove path at sunrise with golden sunbeams filtering through bamboo stalks. "
        "Mio in sleek running attire jogging lightly along the path, looking back over her shoulder and waving her hand inviting the viewer to run together."
    ),
    (
        "gemini_31_ryokan_yukata_lantern.png",
        "image/03 gemini/gemini_31_ryokan_yukata_lantern.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Traditional Kyoto ryokan outdoor garden wooden corridor at night near an onsen bath. "
        "Gemini wearing a soft indigo after-bath yukata, damp glossy black hair, holding a warm glowing paper lantern, "
        "tucking hair behind her cat ear with a bashful rosy blush and tender gaze."
    ),
    (
        "kotone_29_ryokan_table_feast.png",
        "image/02 kotone/kotone_29_ryokan_table_feast.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Traditional Japanese ryokan tatami room at dinner time. "
        "Kotone in a cute yellow floral yukata kneeling before a low wooden table filled with colorful healthy Japanese dishes, "
        "clapping her hands together with chopsticks in an excited 'Itadakimasu!' pose, eyes sparkling with happiness."
    ),
    (
        "mio_29_onsen_milk_cheers.png",
        "image/01 mio/mio_29_onsen_milk_cheers.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Traditional Japanese bathhouse wooden lounge after a hot spring soak. "
        "Mio wearing a light cotton yukata with a small white towel draped around her neck, one hand on her hip and the other holding a cold glass milk bottle, "
        "giving a refreshed 'Ahh!' grin with rosy cheeks."
    ),

    # --------------------------------------------------------------------------
    # BATCH 2: THEME B - URBAN DAILY LIFE, SUBWAY, CLOCK & SHOPPING (12 CGs)
    # --------------------------------------------------------------------------
    (
        "gemini_32_subway_ic_card_tap.png",
        "image/03 gemini/gemini_32_subway_ic_card_tap.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Modern Japanese train station ticket gate. "
        "Gemini wearing a chic beige trench coat over a dark knit sweater and skirt, tapping a transit IC card onto the glowing ticket gate sensor, "
        "glancing back over her shoulder at the viewer with a poised gentle smile beckoning them forward."
    ),
    (
        "kotone_30_clock_panic_sprint.png",
        "image/02 kotone/kotone_30_clock_panic_sprint.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Sunny city sidewalk intersection in the morning. "
        "Kotone in casual school-style cardigan and pleated skirt with a shoulder bag, running at full speed in a cute comical panic while looking at her smartphone clock screen, "
        "twin braids flying, flustered 'I'm gonna be late!' expression."
    ),
    (
        "mio_30_bus_stop_map_point.png",
        "image/01 mio/mio_30_bus_stop_map_point.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Kyoto city street near a bus stop and retro streetlamp. "
        "Mio wearing a sporty cap backwards and a casual varsity jacket, holding an unfolded travel map with one hand and pointing confidently down the street with a bright smile."
    ),
    (
        "gemini_33_train_window_sunset.png",
        "image/03 gemini/gemini_33_train_window_sunset.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Inside a quiet Japanese commuter train car during golden hour sunset. "
        "Warm orange sunlight streaming through the train window behind her, Gemini sitting beside the viewer in a neat blouse and cardigan, "
        "gently offering one white earphone toward the camera with a soft affectionate blush."
    ),
    (
        "kotone_31_ticket_machine_confused.png",
        "image/02 kotone/kotone_31_ticket_machine_confused.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Standing in front of a Japanese train station ticket machine and colorful subway route map wall. "
        "Kotone wearing her pink beret and casual outfit, tilting her head with a finger on her cheek in adorable confusion, looking back for help."
    ),
    (
        "mio_31_train_strap_smile.png",
        "image/01 mio/mio_31_train_strap_smile.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Inside a bright Japanese train car in daylight. "
        "Mio wearing a lightweight windbreaker and backpack, holding onto the overhead hanging train strap with one hand, leaning slightly with the train motion and laughing cheerfully at the viewer."
    ),
    (
        "gemini_34_wrist_watch_late_glare.png",
        "image/03 gemini/gemini_34_wrist_watch_late_glare.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: In front of a modern gym entrance plaza at 5 PM sunset. "
        "Gemini in stylish athleisure jacket, holding up her left wrist and tapping her wristwatch with her right index finger, "
        "cheeks slightly puffed in a cute scolding tsundere glare: 'Do you know what time it is, Producer?!'."
    ),
    (
        "kotone_32_supermarket_protein_cart.png",
        "image/02 kotone/kotone_32_supermarket_protein_cart.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Bright Japanese supermarket chilled food aisle. "
        "Kotone pushing a shopping cart and holding up two packs of chicken breast and tofu with shiny discount stickers, "
        "beaming with triumphant thrifty pride and starry eyes."
    ),
    (
        "mio_32_bento_lunchbox_proud.png",
        "image/01 mio/mio_32_bento_lunchbox_proud.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Wooden park bench under green trees at lunchtime. "
        "Mio in a casual checkered shirt over a white tee, holding open a two-tier homemade healthy protein bento box (boiled eggs, broccoli, salmon, brown rice), "
        "smiling proudly and offering chopsticks to the viewer."
    ),
    (
        "gemini_35_bookstore_kanji_teach.png",
        "image/03 gemini/gemini_35_bookstore_kanji_teach.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Quiet wooden study cafe table with bookshelves in background. "
        "Gemini wearing stylish round reading glasses and a cozy knit sweater, leaning close to the viewer while pointing with a pen at a Japanese notebook, "
        "giving an intelligent, gentle, slightly teasing smile."
    ),
    (
        "kotone_33_cafe_study_pencil.png",
        "image/02 kotone/kotone_33_cafe_study_pencil.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Cozy sunlit cafe booth with open notebooks and vocabulary flashcards spread on the table. "
        "Kotone balancing a wooden pencil between her upper lip and nose while crossing her arms and concentrating hard with a cute furrowed brow."
    ),
    (
        "mio_33_sports_shop_shoes_try.png",
        "image/01 mio/mio_33_sports_shop_shoes_try.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Modern sporting goods store shoe section with colorful running shoes on display shelves. "
        "Mio sitting on a try-on bench tying the laces of a bright new running shoe, looking up at the viewer with excited sparkling eyes."
    ),

    # --------------------------------------------------------------------------
    # BATCH 3: THEME D - FITNESS CARE, MUSCLE SORENESS, SCALE & CHEERS (12 CGs)
    # --------------------------------------------------------------------------
    (
        "gemini_40_shoulder_massage_care.png",
        "image/03 gemini/gemini_40_shoulder_massage_care.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Quiet stretching mat area in a warm fitness studio. "
        "Close-up POV of Gemini kneeling beside the viewer in sleek yoga wear, reaching both hands forward gently to massage and check the viewer's sore shoulders and back, "
        "her amber eyes filled with tender concern behind a shy blush."
    ),
    (
        "kotone_38_calf_cramp_tears.png",
        "image/02 kotone/kotone_38_calf_cramp_tears.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Sitting on a blue gym stretching mat after leg day workout. "
        "Kotone in yellow athletic top and shorts, hugging and rubbing her sore calf with both hands, looking up at the viewer with cute teary puppy eyes and a pouting lip: "
        "'My legs are so sore and heavy, Producer~!'."
    ),
    (
        "mio_38_bicep_flex_wink.png",
        "image/01 mio/mio_38_bicep_flex_wink.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: In front of a bright gym wall mirror. "
        "Mio in an orange athletic tank top, raising one arm in a classic energetic bicep flex pose and pointing at her toned shoulder with the other hand, "
        "giving a playful confident wink and big grin: 'Soreness means your muscles are growing!'."
    ),
    (
        "gemini_41_kitchen_apron_cooking.png",
        "image/03 gemini/gemini_41_kitchen_apron_cooking.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Bright modern home kitchen counter. "
        "Gemini with her black hair tied up in a high ponytail, wearing a cute frilly pastel apron over homewear, "
        "holding a wooden spoon and blowing gently on a piece of warm tofu steak to feed the viewer, blushing shyly."
    ),
    (
        "kotone_39_salad_bowl_fork_smile.png",
        "image/02 kotone/kotone_39_salad_bowl_fork_smile.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Sunny dining table with a large wooden bowl of colorful chicken breast, avocado, and cherry tomato salad. "
        "Kotone leaning across the table holding a fork with a cherry tomato toward the viewer's mouth, smiling sweetly: 'Say ahh, Producer!'."
    ),
    (
        "mio_39_timer_stopwatch_shout.png",
        "image/01 mio/mio_39_timer_stopwatch_shout.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Gym floor during circuit training. "
        "Mio wearing a coach whistle around her neck and holding up a digital stopwatch timer toward the camera with an intense, fiery, encouraging grin: "
        "'It's 5 o'clock! Time to start our sets, let's go fast!'."
    ),
    (
        "gemini_43_tape_measure_waist_smirk.png",
        "image/03 gemini/gemini_43_tape_measure_waist_smirk.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: InBody body composition checkup room with a digital scale in the background. "
        "Gemini in fitted black-and-pink trainer attire, pulling a yellow tailoring tape measure taut between both hands while stepping close to the viewer "
        "with a teasing, smug Kyoto ojousama smile: 'Don't run away from the scale, Producer!'."
    ),
    (
        "kotone_40_scale_peek_fingers.png",
        "image/02 kotone/kotone_40_scale_peek_fingers.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Standing on a digital body weight scale in a bright fitness checkup room. "
        "Kotone covering her flushed face with both hands in adorable dread while peeking nervously down through a gap in her fingers at the scale display."
    ),
    (
        "mio_40_post_run_grass_lie_down.png",
        "image/01 mio/mio_40_post_run_grass_lie_down.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: High-angle shot looking down at Mio resting on lush green park grass after a refreshing run, "
        "arms spread wide, looking up at the viewer with a bright, energetic, utterly happy laugh."
    ),
    (
        "gemini_42_protein_toast_cheers.png",
        "image/03 gemini/gemini_42_protein_toast_cheers.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Cozy evening celebration in the teahouse lounge decorated with warm fairy lights. "
        "Gemini in a gorgeous off-shoulder knit dress, clinking her protein shaker cup / matcha latte glass toward the camera in a celebratory toast, "
        "her eyes shining with genuine pride and affection: 'Congratulations on finishing the week, Producer!'."
    ),
    (
        "kotone_41_confetti_medal_hug.png",
        "image/02 kotone/kotone_41_confetti_medal_hug.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Bright fitness studio celebration. "
        "Kotone leaning right into the camera with arms wide open for a celebratory hug, holding a handmade gold ribbon medal, "
        "eyes sparkling with joyful tears and a huge proud smile."
    ),
    (
        "mio_41_protein_jug_chug_victory.png",
        "image/01 mio/mio_41_protein_jug_chug_victory.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Sunset rooftop terrace after completing a 1-week workout challenge. "
        "Mio raising a pink shaker cup high toward the sky in a triumphant victory toast while giving a high-five with her other hand, radiant champion smile."
    ),

    # --------------------------------------------------------------------------
    # BATCH 4: THEME C - FOUR SEASONS & WEATHER SPECIALS (12 CGs)
    # --------------------------------------------------------------------------
    (
        "gemini_36_summer_handfan_ice.png",
        "image/03 gemini/gemini_36_summer_handfan_ice.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Sunlit wooden veranda (engawa) of a Kyoto house in midsummer with a glass wind chime (furin) hanging above. "
        "Gemini in a cool light-blue summer yukata, pressing an icy glass of cold green tea against her flushed cheek while fanning herself with a round uchiwa fan."
    ),
    (
        "kotone_34_cherry_blossom_bento.png",
        "image/02 kotone/kotone_34_cherry_blossom_bento.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Spring hanami picnic on a blanket under full-bloom pink cherry blossom trees. "
        "Kotone in a soft pink spring cardigan, a single cherry blossom petal resting on her blonde bangs, smiling brightly while holding out a cute picnic snack."
    ),
    (
        "mio_34_spring_wind_stretch.png",
        "image/01 mio/mio_34_spring_wind_stretch.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Riverside running path lined with blooming cherry blossoms under a crystal-clear blue spring sky. "
        "Mio in a mint-green athletic top stretching both arms high overhead in the refreshing spring breeze with a carefree joyful smile."
    ),
    (
        "gemini_37_autumn_maple_teacup.png",
        "image/03 gemini/gemini_37_autumn_maple_teacup.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Kyoto temple garden in peak autumn with fiery red and gold maple leaves (momiji) falling around. "
        "Gemini wearing a rich burgundy kimono shawl, cradling a warm ceramic teacup in both hands, looking at the viewer with serene autumn romance."
    ),
    (
        "kotone_35_summer_sunscreen_hat.png",
        "image/02 kotone/kotone_35_summer_sunscreen_hat.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Sparkling blue summer seaside boardwalk under bright sunshine. "
        "Kotone wearing a wide-brimmed straw sunhat and a breezy white sundress, holding her hat against the sea breeze while handing a cold sports drink to the viewer."
    ),
    (
        "mio_35_summer_water_hose_laugh.png",
        "image/01 mio/mio_35_summer_water_hose_laugh.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Outdoor school track water tap on a scorching summer day. "
        "Mio splashing cool water onto her face from the faucet, sparkling water droplets flying in the sunlight, laughing with pure refreshing summer energy."
    ),
    (
        "gemini_38_winter_kotatsu_mandarin.png",
        "image/03 gemini/gemini_38_winter_kotatsu_mandarin.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Cozy tatami room in winter with snow falling outside the window. "
        "Gemini wearing an oversized cream cable-knit sweater, tucked warmly under a traditional heated kotatsu table blanket like a sleepy cat, "
        "peeling a bright orange mandarin (mikan) and patting the spot next to her inviting the viewer in."
    ),
    (
        "kotone_36_autumn_sweet_potato.png",
        "image/02 kotone/kotone_36_autumn_sweet_potato.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Park bench surrounded by golden autumn ginkgo leaves at dusk. "
        "Kotone in a cozy plaid vest and beret, breaking open a steaming hot roasted sweet potato (yaki-imo) in a paper wrapper, blowing on it with a blissful smile."
    ),
    (
        "mio_36_autumn_sunset_track_jacket.png",
        "image/01 mio/mio_36_autumn_sunset_track_jacket.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Park trail carpeted with fallen red and orange autumn leaves during golden sunset. "
        "Mio zipping up a warm athletic windbreaker, wiping sweat from her brow and looking at the viewer with a gentle, proud post-run smile."
    ),
    (
        "gemini_39_snowy_muffler_blush.png",
        "image/03 gemini/gemini_39_snowy_muffler_blush.png",
        [REF_GEMINI_MAIN, REF_GEMINI_GYM],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Romantic snow-covered Kyoto street at night under warm streetlamp glow, soft snowflakes falling on her black hair and cat ears. "
        "Gemini wearing a dark winter wool coat and a thick burgundy plaid scarf wrapped up to her chin, white breath in the cold air, "
        "shyly reaching out her gloved hand to hold the viewer's hand."
    ),
    (
        "kotone_37_winter_earmuffs_hotpack.png",
        "image/02 kotone/kotone_37_winter_earmuffs_hotpack.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Snowy winter city street with twinkling winter illumination lights. "
        "Kotone wearing fluffy white faux-fur earmuffs and a pastel puffer jacket, gently pressing a warm white pocket hand-warmer (kairo) against the viewer's cheek with a sweet smile."
    ),
    (
        "mio_37_winter_breath_jogging_gloves.png",
        "image/01 mio/mio_37_winter_breath_jogging_gloves.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Crisp frosty winter morning park with snow on the pine trees. "
        "Mio wearing a cute knit beanie hat, thermal running jacket, and sporty gloves, jogging in place with puffs of white breath, grinning brightly to warm up."
    ),

    # --------------------------------------------------------------------------
    # BATCH 5: THEME E - EXPRESSIONS CLOSE-UP & MORIKINOKO SD CHIBIS (12 CGs)
    # --------------------------------------------------------------------------
    (
        "gemini_44_extreme_blush_hide_face.png",
        "image/03 gemini/gemini_44_extreme_blush_hide_face.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Dramatic close-up portrait of Gemini completely flustered by a sudden compliment from the Producer. "
        "Her cheeks and even the tips of her black cat ears are glowing bright red, holding a decorative folding fan over the lower half of her face "
        "while her shimmering amber eyes look up waveringly with heart-melting embarrassment."
    ),
    (
        "gemini_45_ikezu_cold_smile_fan.png",
        "image/03 gemini/gemini_45_ikezu_cold_smile_fan.png",
        [REF_GEMINI_MAIN, REF_GEMINI_TEA],
        f"{STYLE_SSR} {CHAR_GEMINI} SCENE & POSE: Dramatic close-up portrait of Gemini's signature 'Kyoto Ikezu' (polite yet terrifying pressure smile) "
        "after hearing the Producer ate late-night ramen. Her eyes are closed in a sweet polite crescent smile, holding a teacup gracefully, "
        "while a comical dark purple intimidating aura glows softly behind her."
    ),
    (
        "kotone_42_pout_cheeks_angry_cute.png",
        "image/02 kotone/kotone_42_pout_cheeks_angry_cute.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Close-up portrait of Kotone puffing out both cheeks like an angry little hamster, "
        "arms crossed over her chest, eyebrows furrowed in an ultra-adorable sulky pout because the Producer teased her."
    ),
    (
        "kotone_43_starry_eyes_praise.png",
        "image/02 kotone/kotone_43_starry_eyes_praise.png",
        [REF_KOTONE_MAIN, REF_KOTONE_CAFE],
        f"{STYLE_SSR} {CHAR_KOTONE} SCENE & POSE: Close-up portrait of Kotone clasping both hands beside her rosy cheeks in pure admiration, "
        "huge glowing golden stars sparkling inside her amber eyes as she praises the Producer with 1000% idol affection."
    ),
    (
        "mio_42_headpat_big_laugh_blush.png",
        "image/01 mio/mio_42_headpat_big_laugh_blush.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Close-up POV portrait of Mio being patted on the head by the Producer. "
        "Her ahoge hair flattened slightly, eyes closed in a radiantly happy, bashful grin with a deep pink blush across her nose and cheeks."
    ),
    (
        "mio_43_serious_coach_gaze.png",
        "image/01 mio/mio_43_serious_coach_gaze.png",
        [REF_MIO_MAIN, REF_MIO_RUN],
        f"{STYLE_SSR} {CHAR_MIO} SCENE & POSE: Dramatic close-up POV from the gym floor looking up at Mio. "
        "Instead of her usual goofy laugh, she has a cool, deeply supportive, determined expression, extending her hand down toward the camera to pull the Producer up."
    ),
    (
        "sd_gemini_04_takoyaki_burn_panic.png",
        "image/03 gemini/sd_gemini_04_takoyaki_burn_panic.png",
        [REF_SD_BEAN, REF_GEMINI_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with long black hair and black cat ears, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi girl standing inside a giant wooden takoyaki boat trying to lift a huge steaming-hot takoyaki ball with giant toothpicks, "
        "waving in comical panic as steam puffs out, cat ears standing straight up in shock, manga radial speed lines."
    ),
    (
        "sd_gemini_05_kanji_teacher_stick.png",
        "image/03 gemini/sd_gemini_05_kanji_teacher_stick.png",
        [REF_SD_BEAN, REF_GEMINI_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with long black hair, cat ears, round glasses, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny teacher chibi standing atop a giant open Japanese dictionary, dramatically swinging an oversized pointer stick with a smug puffed-out chest, "
        "manga radial speed lines on white background."
    ),
    (
        "sd_gemini_06_5pm_padlock_fridge.png",
        "image/03 gemini/sd_gemini_06_5pm_padlock_fridge.png",
        [REF_SD_BEAN, REF_GEMINI_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with long black hair and black cat ears, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi girl wrapping a giant heavy iron chain and huge padlock around a refrigerator door at 5 PM fasting time, "
        "striking a victorious guard pose with glowing bean-eyes and manga radial speed lines."
    ),
    (
        "sd_gemini_07_cat_box_loaf.png",
        "image/03 gemini/sd_gemini_07_cat_box_loaf.png",
        [REF_SD_BEAN, REF_GEMINI_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with long black hair and black cat ears, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi girl sitting snugly inside a giant ceramic teacup / cardboard box like a loafing cat with only her head, cat ears, and tiny hands peeking over the rim, "
        "blushing cheeks and manga radial speed lines."
    ),
    (
        "sd_kotone_04_icecream_guilt_sweat.png",
        "image/02 kotone/sd_kotone_04_icecream_guilt_sweat.png",
        [REF_SD_BEAN, REF_KOTONE_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with blonde twin braids and yellow ribbons, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi Kotone sitting on top of a giant ice cream tub hugging a huge metal scoop at midnight, frozen in comical shock with flying sweat drops, "
        "solid black oval bean-eyes and manga radial speed lines."
    ),
    (
        "sd_kotone_05_tambourine_cheer_dance.png",
        "image/02 kotone/sd_kotone_05_tambourine_cheer_dance.png",
        [REF_SD_BEAN, REF_KOTONE_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with blonde twin braids and yellow ribbons, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi Kotone popping out from inside a giant golden piggy bank while shaking an oversized tambourine with flying coins and musical notes, "
        "happy solid black bean-eyes and manga radial speed lines."
    ),
    (
        "sd_kotone_06_halfprice_sticker_slap.png",
        "image/02 kotone/sd_kotone_06_halfprice_sticker_slap.png",
        [REF_SD_BEAN, REF_KOTONE_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with blonde twin braids and yellow ribbons, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi Kotone leaping through the air to slap a giant red round discount sticker onto a huge bento box with intense determination, "
        "solid black oval bean-eyes and dramatic manga radial speed lines."
    ),
    (
        "sd_mio_04_shoes_mud_shock.png",
        "image/01 mio/sd_mio_04_shoes_mud_shock.png",
        [REF_SD_BEAN, REF_MIO_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with short brown bob hair and ahoge, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi Mio standing inside a giant white running sneaker like a boat on a tatami mat, frozen in comical shock with wavy panic lines, "
        "solid black oval bean-eyes and manga radial speed lines."
    ),
    (
        "sd_mio_05_gold_medal_thumbsup.png",
        "image/01 mio/sd_mio_05_gold_medal_thumbsup.png",
        [REF_SD_BEAN, REF_MIO_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with short brown bob hair and ahoge, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi Mio sitting proudly on top of a giant gleaming gold trophy cup, giving a huge double thumbs-up with solid black oval bean-eyes "
        "and manga radial speed lines."
    ),
    (
        "sd_mio_06_treadmill_fly_away.png",
        "image/01 mio/sd_mio_06_treadmill_fly_away.png",
        [REF_SD_BEAN, REF_MIO_MAIN],
        f"{STYLE_SD} CHARACTER: Tiny 2-head-tall chibi girl with short brown bob hair and ahoge, solid black oval bean-eyes. "
        "SCENE & POSE: Tiny chibi Mio running on a giant treadmill with her stubby legs spinning like a cartoon whirlwind, arms flailing in hilarious high-speed chaos, "
        "solid black oval bean-eyes and manga radial speed lines."
    ),
]

# Interleave SD jobs across the main queue at a 1~2 per 10 ratio (every 5 jobs) so SDs are generated evenly mixed in!
_non_sd = [j for j in JOBS if not j[0].startswith("sd_")]
_sd_only = [j for j in JOBS if j[0].startswith("sd_")]
_interleaved = []
_sd_idx = 0
for _i, _job in enumerate(_non_sd, 1):
    _interleaved.append(_job)
    if _i % 5 == 0 and _sd_idx < len(_sd_only):
        _interleaved.append(_sd_only[_sd_idx])
        _sd_idx += 1
while _sd_idx < len(_sd_only):
    _interleaved.append(_sd_only[_sd_idx])
    _sd_idx += 1
JOBS = _interleaved


def pick_diverse_refs(filename: str, default_refs: list[Path]) -> list[Path]:
    if filename.startswith("sd_"):
        return default_refs
    idx = sum(ord(c) for c in filename)
    if filename.startswith("gemini_") and len(GEMINI_POOL_FILES) >= 4:
        p1 = GEMINI_POOL_FILES[idx % len(GEMINI_POOL_FILES)]
        p2 = GEMINI_POOL_FILES[(idx + 5) % len(GEMINI_POOL_FILES)]
        return [p1, p2]
    if filename.startswith("kotone_") and len(KOTONE_POOL_FILES) >= 4:
        p1 = KOTONE_POOL_FILES[idx % len(KOTONE_POOL_FILES)]
        p2 = KOTONE_POOL_FILES[(idx + 4) % len(KOTONE_POOL_FILES)]
        return [p1, p2]
    if filename.startswith("mio_") and len(MIO_POOL_FILES) >= 4:
        p1 = MIO_POOL_FILES[idx % len(MIO_POOL_FILES)]
        p2 = MIO_POOL_FILES[(idx + 5) % len(MIO_POOL_FILES)]
        return [p1, p2]
    return default_refs


def generate_image(driver, filename, dest_rel, ref_paths, prompt):
    ref_paths = pick_diverse_refs(filename, ref_paths)
    cam_rule = CAMERA_BY_FILE.get(filename, "")
    if cam_rule:
        prompt = (
            f"MANDATORY CAMERA ANGLE & POSE OVERRIDE (DO NOT COPY REFERENCE POSE OR FRONTAL FACE ANGLE! "
            f"Use attached images ONLY for hair/eye color identity): {cam_rule} "
            f"{prompt} "
            f"STRICT COMPOSITION CHECK: Camera and body posture MUST follow: {cam_rule}"
        )

    print(f"\n=======================================================")
    print(f"🎨 [CG 생성 중] {filename}")
    if cam_rule:
        print(f"📐 [구도 지시] {cam_rule[:95]}...")
    print(f"📎 [레퍼런스] {[r.name for r in ref_paths]}")
    print(f"=======================================================")

    ref_imgs = [Image.open(r) for r in ref_paths if r.exists()]
    driver.get("https://grok.com/imagine")
    time.sleep(3.5)

    prompt_css = ["textarea", "div[contenteditable='true']", "[role='textbox']"]
    box = first_visible_css(driver, prompt_css, 15)
    if not box:
        driver.get("https://grok.com")
        box = first_visible_css(driver, prompt_css, 20)
    if not box:
        raise RuntimeError("Grok input box not found")

    for r in ref_paths:
        if not r.exists():
            continue
        try:
            file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            if not file_inputs:
                break
            target_input = next((i for i in file_inputs if i.get_attribute("multiple") is not None), file_inputs[0])
            target_input.send_keys(str(r.resolve()))
            time.sleep(2.5)
        except Exception as ex:
            print("Attachment note:", ex)
            break
    time.sleep(2.0)

    before = set(big_image_srcs(driver))
    box = first_visible_css(driver, prompt_css, 10) or box
    box.click()
    time.sleep(0.5)
    box.send_keys(" ".join(prompt.split()))
    time.sleep(1.5)
    box.send_keys(Keys.ENTER)
    time.sleep(2.0)
    # If text is still in the input box (e.g. attachment was still uploading), press ENTER again
    try:
        rem = (box.get_attribute("value") or box.text or "").strip()
        if len(rem) > 20:
            time.sleep(2.0)
            box.send_keys(Keys.ENTER)
    except Exception:
        pass
    print("⏳ Grok CG 렌더링 대기 중...")

    end_time = time.time() + 55
    while time.time() < end_time:
        new_srcs = wait_new_images(driver, before, timeout=30, settle=2.5)
        for src in new_srcs:
            cand = fetch_image(driver, src, "https://grok.com")
            diffs = [ref_diff(cand, r_im) for r_im in ref_imgs]
            min_diff = min(diffs) if diffs else 999.0
            if min_diff < SAME_AS_REF:
                print(f"   [필터] 레퍼런스 재표시 건너뜀 (diff={min_diff:.1f})")
                before.add(src)
                continue

            target_path = BASE_DIR / dest_rel
            target_path.parent.mkdir(parents=True, exist_ok=True)
            cand.save(target_path, format="PNG")
            print(f"✨ [생성 완료] {target_path.relative_to(BASE_DIR)} ({cand.size})")

            try:
                ART_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target_path, ART_DIR / target_path.name)
            except Exception:
                pass
            return target_path

    raise RuntimeError(f"[{filename}] 생성 타임아웃")


def main():
    lock_file = PROFILE_DIR / "parent.lock"
    if lock_file.exists():
        try:
            lock_file.unlink()
        except Exception:
            pass

    opts = Options()
    opts.binary_location = FIREFOX_EXE
    opts.add_argument("-profile")
    opts.add_argument(str(PROFILE_DIR))
    driver = webdriver.Firefox(options=opts)
    try:
        driver.set_window_size(1400, 1000)
    except Exception:
        pass
    driver.set_script_timeout(180)

    total = len(JOBS)
    done_count = 0
    try:
        for pass_num in (1, 2):
            print(f"\n================ PASS {pass_num}/2 ================")
            done_count = 0
            for idx, (fname, dest_rel, refs, prompt) in enumerate(JOBS, 1):
                target_file = BASE_DIR / dest_rel
                if target_file.exists() and target_file.stat().st_size > 30000:
                    if pass_num == 1:
                        print(f"[{idx}/{total}] Skipping already existing {target_file.name}")
                    done_count += 1
                    continue
                print(f"\n🚀 [Pass {pass_num} | {idx}/{total}] Starting {fname}...")
                try:
                    generate_image(driver, fname, dest_rel, refs, prompt)
                    done_count += 1
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ [{idx}/{total}] Error on {fname}: {e}")
                    time.sleep(4)
    finally:
        driver.quit()
        print(f"\n🎉 Batch finished! ({done_count}/{total} images available)")


if __name__ == "__main__":
    main()
