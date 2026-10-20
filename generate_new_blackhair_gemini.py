"""신규 흑발 롱헤어 제미니 (포즈·구도·표정 극대화 5종 미연시 이벤트 CG) Grok 생성 스크립트
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from evolve_pool import run_batch

JOBS = [
    # ── 1. VIP 헬스장: 상체 앞으로 푹 숙여 얼굴을 들이대는 짓궂은 로우/클로즈업 앵글 ──
    (
        "gemini",
        "main_vip",
        "01_gemini_main.png",
        "gemini_01_main.png",
        (
            "COMPOSITION & POSE: Dynamic close-up camera angle from below (low-angle perspective). "
            "Gemini is holding two 2kg pink dumbbells and leaning her upper body deeply forward toward the camera, "
            "getting intimately close to the viewer's face! Her very long silky raven-black hair cascades dramatically forward over her shoulders. "
            "EXPRESSION: Mischievous teasing smug smirk with her tongue slightly sticking out (playful mesugaki tongue poke like reference) "
            "and her cute sharp fang visible, eyebrow raised playfully, flushed red cheeks: 'Already tired after one set, Producer? Hehe!' "
            "OUTFIT & SETTING: Sunlit modern VIP fitness studio with mirror reflections. Wearing a stylish black off-shoulder cropped sports top "
            "and athletic leggings, black choker with a tiny gold cat bell."
        )
    ),
    # ── 2. 전통 다실: 무릎 꿇고 정좌한 하이앵글 & 볼 붉힌 부끄러운 츤데레 곁눈질 ──
    (
        "gemini",
        "matcha_neko",
        "02_gemini_matcha.png",
        "gemini_02_matcha.png",
        (
            "COMPOSITION & POSE: High-angle view looking down slightly at Gemini sitting in a proper kneeling seiza posture "
            "on a warm sunlit tatami mat in a traditional Japanese tea room (chashitsu). "
            "She is holding a dark ceramic matcha tea bowl with vibrant green froth with both hands. "
            "Her very long flowing raven-black hair pools gracefully across the tatami floor behind her. "
            "EXPRESSION: Shy flustered tsundere expression! Blushing intensely across her whole face and ears, looking sideways away from the viewer "
            "with a cute pouting lip and sharp little fang showing: '...Hmph, I whisked this matcha specially for you, so don't you dare leave a single drop!' "
            "OUTFIT: Elegant white-and-red modern shrine-maiden neko haori with fluffy white fur collar trim and black cat ears."
        )
    ),
    # ── 3. 노을빛 필라테스룸: 1인칭 POV 시점, 바닥에서 올려다보며 손목을 감싸 쥔 초밀착 케어 ──
    (
        "gemini",
        "rehab_touch",
        "03_gemini_rehab_touch.png",
        "gemini_03_rehab_touch.png",
        (
            "COMPOSITION & POSE: First-person POV intimate angle! The viewer's arm and wrist are extended forward, and Gemini is sitting close on the floor mat, "
            "gently wrapping both of her soft hands around the viewer's wrist for tennis elbow eccentric rehab care. "
            "Her white oversized knit cardigan has completely slipped off one shoulder. "
            "She is looking up directly into the viewer's eyes from below (dramatic upturned gaze). "
            "EXPRESSION: Heart-meltingly tender and deeply caring gaze with soft genuine affection, warm blush, cute tiny fang: "
            "'Dummy, you should have told me your elbow hurt... Don't worry, I'll massage it until it's completely healed.' "
            "OUTFIT & SETTING: Sunset-lit pilates studio with golden orange rays filling the room. Wearing a pastel-grey ribbed halter-neck top and slipping white cardigan."
        )
    ),
    # ── 4. 서머 풀사이드: 선베드에 비스듬히 누워 선글라스를 내리며 윙크하는 사선 다이내믹 앵글 ──
    (
        "gemini",
        "pool_bikini",
        "04_gemini_pool_bikini.png",
        "gemini_04_pool_bikini.png",
        (
            "COMPOSITION & POSE: Dynamic diagonal wide-angle shot. Gemini is reclining sideways on a white poolside sun lounger bed, "
            "propping herself up on one elbow. With her other hand, she is tipping down stylish dark sunglasses to peek over the frames. "
            "Her glistening long wet raven-black hair fans out across the white towel on the lounger. "
            "EXPRESSION: Charming playful wink, confident teasing smile with cute sharp fang, sparkling water droplets on her collarbone and shoulders. "
            "OUTFIT & SETTING: Luxury resort pool with crystal turquoise water and palm trees in bright summer sunshine. "
            "Wearing a chic strappy black monokini bikini with red heart hairpins."
        )
    ),
    # ── 5. 펜트하우스 야경 발코니: 난간에 기대어 뒤돌아보는 매혹적인 오버 더 숄더 앵글 ──
    (
        "gemini",
        "night_secret",
        "05_gemini_night_secret.png",
        "gemini_05_night_secret.png",
        (
            "COMPOSITION & POSE: Cinematic over-the-shoulder turning back perspective! Gemini is leaning against a glass balcony railing "
            "overlooking glowing city night skyline bokeh. She turns her head and upper torso back over her shoulder to gaze at the viewer, "
            "holding up a sparkling crystal glass of lemon water in a private toast. "
            "A gentle night breeze blows her waist-length black hair in dramatic flowing strands across the frame. "
            "EXPRESSION: Sultry, sleepy, affectionate half-lidded cat-like eyes with a gentle loving fang smile under the moonlight: "
            "'Intermittent fasting shutdown completed for today, Producer. Come stand with me for a bit.' "
            "OUTFIT: Luxurious backless burgundy silk slip night dress and delicate black ribbon choker."
        )
    ),
]

if __name__ == "__main__":
    print(f"총 {len(JOBS)}개 흑발 롱헤어 제미니 다이내믹 CG 생성 시작...")
    run_batch(JOBS)
    print("모든 작업 완료!")
