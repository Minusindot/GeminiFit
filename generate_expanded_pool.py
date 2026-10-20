"""신규 30종 확장 CG 풀 배치 생성기 (미오 10종 전면 재작업 + 제미니 5종 추가 + 코토네 5종 추가)
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from evolve_pool import run_batch

# ── [우선순위 1] 미오 10종: 완벽히 차별화된 10가지 구도·앵글·표정 전면 재작업 ──
MIO_JOBS = [
    # 01. 트랙 바닥 앉아 쉬기 (로우 앵글 & 땀 흘리며 수건으로 목 닦는 숨가쁜 표정)
    (
        "mio",
        "track_ground_rest",
        "01_mio_track_rest.png",
        "mio_01_main.png",
        (
            "COMPOSITION & POSE: Dynamic dramatic low-angle perspective looking up from ground level. "
            "Mio is sitting cross-legged on the red running track tartan turf with one knee bent up. "
            "She is draping a clean white sports towel around her neck, holding both towel ends with her hands, "
            "chest heaving lightly with glistening beads of sweat on her forehead and collarbone. "
            "EXPRESSION: Breathless, radiant pink cheeks, competitive playful smirk, looking directly down into camera: "
            "'Haa... 5km interval done! You kept up pretty well today, Producer! Don't collapse yet!' "
            "OUTFIT & SETTING: Sunlit modern high school stadium track. Wearing an athletic orange & white sleeveless compression tank top "
            "and black runner shorts."
        )
    ),
    # 02. 1인칭 POV 손잡아 일으켜주기 (위에서 내려다보는 역동적 하이앵글 & 활짝 웃는 표정)
    (
        "mio",
        "pov_hand_pull",
        "02_mio_hand_pull.png",
        "mio_02_park_run.png",
        (
            "COMPOSITION & POSE: First-person POV high-angle view looking down. The viewer is sitting on the grass catching breath, "
            "and Mio is leaning down from above, enthusiastically reaching her right hand directly towards the camera to pull the viewer up! "
            "Her caramel short hair bounces with dynamic motion lines. "
            "EXPRESSION: Ultra-bright wide open-mouthed beaming smile, sparkling amber eyes full of life, cheering encouragement: "
            "'Come on, grab my hand! We've still got 1km left to our goal! Together until the end!' "
            "OUTFIT & SETTING: Sun-dappled park running path with cherry blossom greenery. Wearing a lime-yellow zip windbreaker over sport crop top."
        )
    ),
    # 03. 실내 수영장 물장구 (워터 스플래시 다이내믹 사선 앵글 & 장난기 가득한 윙크)
    (
        "mio",
        "pool_splash_wink",
        "03_mio_pool_splash.png",
        "mio_03_poolside.png",
        (
            "COMPOSITION & POSE: Dynamic Dutch-tilt diagonal shot at water level inside a sparkling luxury indoor swimming pool. "
            "Mio is waist-deep in clear turquoise water, playfully splashing a crystalline burst of water droplets directly at the camera lens! "
            "Water droplets freeze mid-air with refraction effects. "
            "EXPRESSION: Cheeky teasing wink with one eye closed, sticking her tongue out playfully (tehepero face) in pure joyful mischief. "
            "OUTFIT: Sporty one-piece training swimsuit in navy-blue with sunset-orange side racing stripes, wet caramel bangs sticking adorably to forehead."
        )
    ),
    # 04. 체육관 벤치프레스 거꾸로 눕기 (인버티드 앵글 - 위아래 반전 시점)
    (
        "mio",
        "inverted_bench_rest",
        "04_mio_inverted_bench.png",
        "mio_04_cheer_stage.png",
        (
            "COMPOSITION & POSE: Creative inverted upside-down camera angle! Mio is lying on her back along a gym workout bench after an abs set, "
            "tilting her head backwards over the bench edge to look upside-down directly at the viewer standing behind her. "
            "Her soft caramel hair spills freely downwards towards the floor. "
            "EXPRESSION: Flushed upside-down face, playful crooked grin, one eyebrow raised: "
            "'Hey, looking at me upside down tightens your core twice as fast! ...Ehehe, made you look, Producer!' "
            "OUTFIT & SETTING: High-tech fitness gym with barbell racks. Wearing a coral-pink cropped racerback top and grey training tights."
        )
    ),
    # 05. 황혼빛 해변 모래사장 스쿼트 (광각 역광 실루엣 & 진지하고 섹시한 집중 표정)
    (
        "mio",
        "sunset_beach_squat",
        "05_mio_beach_squat.png",
        "mio_05_sunset_beach.png",
        (
            "COMPOSITION & POSE: Cinematic low-angle wide shot at golden sunset on an open ocean beach. "
            "Mio is in a deep, powerful athletic squat posture right on the wet shoreline where gentle waves lap her bare feet. "
            "Warm golden orange sunlight creates an ethereal rim-light edge glow around her athletic curves and caramel hair strands. "
            "EXPRESSION: Focused, determined athletic concentration, lightly biting her bottom lip, glowing amber eyes reflecting the sunset waves. "
            "OUTFIT: Sunset orange gradient sporty bikini top and navy dolphin running shorts."
        )
    ),
    # 06. 비 오는 날 버스정류장 하나의 우산 (초밀착 클로즈업 & 두근거리는 부끄러운 옆모습)
    (
        "mio",
        "rain_shared_umbrella",
        "06_mio_rain_umbrella.png",
        "mio_06_shared_umbrella.png",
        (
            "COMPOSITION & POSE: Intimate Dutch-angle close-up at a rainy bus stop under a single clear transparent umbrella. "
            "Mio is standing shoulder-to-shoulder, pressed closely against the viewer to stay dry from the heavy rain splashing around them. "
            "Raindrops blur beautifully on the umbrella dome above. "
            "EXPRESSION: Shy, flustered blush spreading across her cheeks and ears, looking up sideways through eyelashes with soft parted lips: "
            "'U-um... our shoulders are touching, Producer... my heart is beating louder than the rain...' "
            "OUTFIT: Cozy oversized cream school cardigan over athletic polo shirt, wet hair tips clinging softly to her neck."
        )
    ),
    # 07. 편의점 앞 벤치 에너지바 나눠먹기 (옆모습 측면 프로필 & 입에 에너지바 문 귀여운 표정)
    (
        "mio",
        "conveni_protein_bar",
        "07_mio_conveni_bench.png",
        "mio_07_convenience_bar.png",
        (
            "COMPOSITION & POSE: Charming side-profile mid-shot sitting on a wooden bench outside a brightly illuminated Japanese convenience store at night. "
            "Mio has a chocolate protein bar lightly clenched between her teeth while checking her running watch, then turns her gaze toward the viewer. "
            "EXPRESSION: Adorable puffed hamster cheeks around the snack, surprised wide round eyes, cute muffled questioning expression: "
            "'Mmmph? (Producer want the other half?)' "
            "OUTFIT: Casual streetwear oversized black windbreaker hoodie, cycling shorts, sporty sneakers."
        )
    ),
    # 08. 트랙 잔디밭 대자로 눕기 (탑뷰 버즈아이 시점 - 하늘에서 수직으로 내려다보는 구도)
    (
        "mio",
        "grass_zenith_topview",
        "08_mio_grass_topview.png",
        "mio_08_zenith_rest.png",
        (
            "COMPOSITION & POSE: Overhead zenith bird's-eye perspective looking straight down from the sky. "
            "Mio is sprawled out flat on her back on lush green stadium grass in a star-shape pose, catching her breath under bright afternoon sunlight. "
            "Her caramel hair spreads out like a soft fan on the grass blades. "
            "EXPRESSION: Utterly blissful, peaceful closed eyes with a serene satisfied smile, chest softly resting after maximum workout. "
            "OUTFIT: Sky-blue sleeveless athletic crop top, navy runner shorts, white sweatband on wrist."
        )
    ),
    # 09. 복싱 링 코너 글러브 가드 (다이내믹 어안렌즈 어반 앵글 & 파이팅 넘치는 미소)
    (
        "mio",
        "boxing_guard_fisheye",
        "09_mio_boxing_guard.png",
        "mio_09_boxing_sparring.png",
        (
            "COMPOSITION & POSE: Dynamic wide-angle / fisheye close perspective inside a boxing ring. "
            "Mio holds up two glossy bright-red boxing gloves in a tight high guard directly towards the viewer/sparring partner. "
            "Red corner ropes and spotlight bokeh in background. "
            "EXPRESSION: Fierce, spirited grin with gleaming sharp amber eyes full of fighting energy: "
            "'Come on, Producer! Show me your jab! Don't hold back just because I'm an idol!' "
            "OUTFIT: Crimson athletic sports bra, black athletic shorts with gold trim, boxing hand wraps."
        )
    ),
    # 10. 여름 축제 유카타 볼 콕콕 (아이컨택 바짝 밀착 & 심쿵 유발 눈맞춤)
    (
        "mio",
        "yukata_cheek_poke",
        "10_mio_yukata_poke.png",
        "mio_10_festival_date.png",
        (
            "COMPOSITION & POSE: Intimate eye-contact close-up amidst warm orange festival lantern light and evening fireworks bokeh. "
            "Mio is leaning in cheek-to-cheek, playfully poking the viewer's cheek with her index finger. "
            "EXPRESSION: Heart-fluttering, radiant, tender affectionate gaze with sweet warm smile and soft blush: "
            "'Hehe! You've been staring at me more than the fireworks tonight, Producer~ ❤️' "
            "OUTFIT: Vibrant sunflower-yellow and orange goldfish pattern summer yukata with red sash, delicate floral hairpin."
        )
    ),
]

# ── [우선순위 2] 제미니 5종 추가 (gemini_06 ~ gemini_10) ──
GEMINI_JOBS = [
    # 06. 전신 거울 앞 척추 기립근 스트레칭 (뒤태 & 거울 속 곁눈질 앵글)
    (
        "gemini",
        "mirror_spine_stretch",
        "06_gemini_mirror_stretch.png",
        "gemini_06_mirror_stretch.png",
        (
            "COMPOSITION & POSE: Over-the-shoulder mirror reflection perspective in a private fitness studio. "
            "Gemini is standing facing the mirror with arms raised high, stretching her back and waist. "
            "Her gorgeous waist-length silky black hair cascades dramatically down her arched back. "
            "In the mirror reflection, her face turns slightly to look back over her shoulder at the viewer with an amused teasing smirk. "
            "EXPRESSION: Mischievous cat-like smirk with sharp little fang visible, arched eyebrow: "
            "'Where are your eyes wandering, Producer? Check my spine alignment, not my waist!' "
            "OUTFIT: Form-fitting dark violet backless athletic bodysuit highlighting slender curves, black cat ears."
        )
    ),
    # 07. 테라스 카페 턱 괴고 삐진 척 (로우 앵글 & 뾰로통한 볼 찌푸림)
    (
        "gemini",
        "cafe_pout_chin",
        "07_gemini_cafe_pout.png",
        "gemini_07_cafe_pout.png",
        (
            "COMPOSITION & POSE: Low table-level perspective across a wooden cafe terrace table under a striped awning. "
            "Gemini is resting her chin in both hands, elbows propped on the table, leaning forward intimately. "
            "An iced black americano sits untouched next to her. "
            "EXPRESSION: Pouting puffed cheeks with cute little fang peeking over lower lip, mock-scolding tsundere glare: "
            "'Did you just stare at that butter croissant in the display case?! We're in intermittent fasting golden time! Hmph!' "
            "OUTFIT: Chic black sleeveless turtleneck knit top, delicate silver necklace, ribbon hairpins on raven sidelocks."
        )
    ),
    # 08. 소파 위 체성분 인바디 분석표 검토 (무릎 끌어안은 위에서 내려다보는 앵글)
    (
        "gemini",
        "inbody_sheet_check",
        "08_gemini_inbody_check.png",
        "gemini_08_inbody_sheet.png",
        (
            "COMPOSITION & POSE: Cozy high-angle perspective looking down at Gemini sitting curled up on a plush velvet sofa hugging her knees. "
            "She is holding the printed InBody composition sheet in one hand, wearing stylish thin gold-rimmed reading glasses perched on her nose. "
            "Her long black hair pools around her legs on the cushions. "
            "EXPRESSION: Looking up over the top of her glasses at the viewer with proud, impressed, glowing cat-eyes and a soft genuine blush: "
            "'Muscle mass +0.4kg, visceral fat down... Hmph, you actually listened to my coaching. Good boy, Producer.' "
            "OUTFIT: Oversized pastel pink hoodie, knee-high black socks, cute plush slippers."
        )
    ),
    # 09. 비 오는 날 체육관 락커룸 수건 머리 털기 (초밀착 클로즈업 & 촉촉한 눈빛)
    (
        "gemini",
        "locker_towel_close",
        "09_gemini_locker_towel.png",
        "gemini_09_rain_locker.png",
        (
            "COMPOSITION & POSE: Very intimate close-up in a warm dim private locker room. "
            "Gemini has a fluffy white towel draped over her head, using both hands to softly shake and dry her damp raven-black hair. "
            "Her bangs are parted naturally, water droplets sparkling on her neck and clavicle. "
            "EXPRESSION: Soft, tender, unguarded affectionate gaze directly into camera, flushed pink cheeks, gentle fang smile: "
            "'You ran all the way through the rain just to train with me? Dummy... here, come closer. Let me dry your head too.' "
            "OUTFIT: Black ribbed athletic camisole, soft white towel, loose hair strands framing porcelain face."
        )
    ),
    # 10. 아침 침대 부스스한 잠투정 (탑뷰 사선 & 졸린 소악마 표정)
    (
        "gemini",
        "bed_messy_morning",
        "10_gemini_bed_morning.png",
        "gemini_10_morning_bed.png",
        (
            "COMPOSITION & POSE: Diagonal top-down view of Gemini lying in a cozy sun-drenched white bed in the early morning. "
            "Her waist-length black hair is artfully tousled across white linen pillows, black cat ears twitching sleepily. "
            "She is clutching the duvet up to her chin with one hand while rubbing one eye with a tiny fist. "
            "EXPRESSION: Sleepy, vulnerable, pouting little yawn with cute visible fang, half-open drowsy eyes: "
            "'Mmm... 5 more minutes of sleep... unless Producer already whisked that morning matcha latte...?' "
            "OUTFIT: Silky black satin pajama camisole set, soft morning light filtering through sheer curtains."
        )
    ),
]

# ── [우선순위 3] 코토네 5종 추가 (kotone_06 ~ kotone_10) ──
KOTONE_JOBS = [
    # 06. 트레이닝 룸 바닥 방전 (대자로 뻗어 헥헥거리는 앵글)
    (
        "kotone",
        "studio_floor_melt",
        "06_kotone_floor_melt.png",
        "kotone_06_floor_melt.png",
        (
            "COMPOSITION & POSE: Wide-angle view looking down at Kotone completely collapsed flat on the polished wooden studio floor after brutal workout. "
            "Her blonde twin braids are sprawled out on both sides like melted butter, limbs limp in comic exhaustion. "
            "EXPRESSION: Comical dazed spiral eyes, tongue lightly lolling out in dramatic exhaustion, panting: "
            "'Pro...ducer-nim... Kotone is officially melted into a golden puddle... emergency praise and cash bonus needed immediately... 💸😵' "
            "OUTFIT: Yellow idol training tee soaked with sweat around collar, gym shorts, colorful sneakers."
        )
    ),
    # 07. 다이어트 샐러드 볼 빵빵 (입안 가득 토마토 물고 햄스터 볼)
    (
        "kotone",
        "salad_hamster_cheeks",
        "07_kotone_salad_hamster.png",
        "kotone_07_salad_hamster.png",
        (
            "COMPOSITION & POSE: Frontal medium close-up sitting at a training table with a huge healthy salad bowl filled with cherry tomatoes and greens. "
            "Kotone holds a fork in hand, having stuffed cherry tomatoes into her mouth. "
            "EXPRESSION: Hilariously cute puffed hamster cheeks bulging with food, wide startled golden eyes, blushing bright red: "
            "'Mmmph?! Don't look! Kotone is fueling up idol muscle fibers! No laughing, Producer-nim!' "
            "OUTFIT: Cute school uniform blouse with loose yellow necktie, cardigan draped over chair."
        )
    ),
    # 08. 거울 앞에서 머리핀 입에 물고 헤어 정돈 (일상 로우/사선 앵글)
    (
        "kotone",
        "mirror_hairpin_mouth",
        "08_kotone_hairpin_mirror.png",
        "kotone_08_mirror_hairpin.png",
        (
            "COMPOSITION & POSE: Backstage dressing room shot. Kotone is looking into a brightly lit dressing mirror with bulbs, "
            "holding a yellow bobby pin between her lips while both hands are up re-weaving her iconic blonde twin braids. "
            "EXPRESSION: Caught by surprise in the mirror reflection, shy blush, golden eyes glancing sideways toward the viewer: "
            "'Mmm... (Wait a second, Producer-nim, let me finish my hair before you look at me!)' "
            "OUTFIT: Casual pink hoodie with sleeves rolled up, hair clips, vanity lights glowing softly."
        )
    ),
    # 09. 야간 책상 위 인바디 다이어리 적다 꾸벅꾸벅 (따뜻한 스탠드 조명 앵글)
    (
        "kotone",
        "desk_nap_diary",
        "09_kotone_desk_nap.png",
        "kotone_09_desk_nap.png",
        (
            "COMPOSITION & POSE: Warm ambient perspective lit by a small golden desk lamp at midnight. "
            "Kotone has fallen fast asleep at her study desk, resting her soft cheek directly against the open fitness diary. "
            "Her pen has rolled from her relaxed hand. "
            "EXPRESSION: Peaceful, adorable sleeping angel expression, squished cheek, tiny cute breathing bubble, gentle smile dreaming of sweets. "
            "OUTFIT: Soft fluffy yellow pajama onesie with cute bear ears on hood, cozy bedroom atmosphere."
        )
    ),
    # 10. 비치 발리볼 점프 스파이크 (역동적인 하이 점프 액션 앵글)
    (
        "kotone",
        "beach_volleyball_spike",
        "10_kotone_beach_spike.png",
        "kotone_10_beach_volleyball.png",
        (
            "COMPOSITION & POSE: Thrilling upward action shot under vivid tropical blue sky! "
            "Kotone is leaping high into the air above the volleyball net on a white sand beach, arm cocked back powerfully to spike the ball! "
            "Her blonde twin braids fly dramatically in the ocean sea breeze with sparkling sand particles. "
            "EXPRESSION: Exuberant, triumphant, roaring confident smile with sparkling amber eyes: "
            "'Take this, Producer-nim! Fujita Kotone's maximum calorie-burning power spike!! 🏐✨' "
            "OUTFIT: Bright sunshine-yellow sporty two-piece bikini with white sporty trims, sunglasses propped on her head."
        )
    ),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = []
    if mode in ("mio", "all"):
        jobs.extend(MIO_JOBS)
    if mode in ("gemini", "all"):
        jobs.extend(GEMINI_JOBS)
    if mode in ("kotone", "all"):
        jobs.extend(KOTONE_JOBS)

    print(f"🚀 총 {len(jobs)}개 다이내믹 이벤트 CG 생성 시작 (모드: {mode})...")
    run_batch(jobs)
    print("🎉 생성 배치 완료!")
