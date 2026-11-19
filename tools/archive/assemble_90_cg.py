"""Assemble all 90 CGs into index.html
- Gemini: 25 full CGs + 3 Morikinoko SD = 28
- Kotone: 25 full CGs + 3 Morikinoko SD = 28
- Mio: 25 full CGs + 3 Morikinoko SD = 28
- Trio: 6 Joint Specials
Total Pool = 90 CGs!
"""
import re
from pathlib import Path

index_path = Path("index.html")
text = index_path.read_text(encoding="utf-8")

# 1. Update header gallery counter & titles
text = re.sub(
    r'<span class="px-1 py-0\.2 rounded-full bg-pink-500 text-white text-\[9px\] font-black">\d+</span>',
    '<span class="px-1 py-0.2 rounded-full bg-pink-500 text-white text-[9px] font-black">90</span>',
    text
)
text = re.sub(
    r'title="[^"]*이벤트[^"]*도감"',
    'title="90종 이벤트 & SD 치비 도감"',
    text
)
text = re.sub(
    r'<span class="text-\[10px\] px-2 py-0\.5 rounded-full bg-pink-500 text-white font-extrabold">총 [^<]+</span>',
    '<span class="text-[10px] px-2 py-0.5 rounded-full bg-pink-500 text-white font-extrabold">총 90종 (풀CG 75 + SD치비 9 + 3인합동 6)</span>',
    text
)

# 2. Update Gallery Modal Tabs
new_gal_tabs = """<button onclick="renderGalleryGrid('all')" id="galTabAll" class="px-2 py-1 rounded-lg text-[11px] font-extrabold bg-[#4a89dc] text-white">전체 (90)</button>
          <button onclick="renderGalleryGrid('gemini')" id="galTabGemini" class="px-2 py-1 rounded-lg text-[11px] font-bold sub-box">🐾 제미니 (28)</button>
          <button onclick="renderGalleryGrid('kotone')" id="galTabKotone" class="px-2 py-1 rounded-lg text-[11px] font-bold sub-box">💛 코토네 (28)</button>
          <button onclick="renderGalleryGrid('mio')" id="galTabMio" class="px-2 py-1 rounded-lg text-[11px] font-bold sub-box">🌟 미오 (28)</button>
          <button onclick="renderGalleryGrid('dual')" id="galTabDual" class="px-2 py-1 rounded-lg text-[11px] font-bold sub-box text-purple-600 dark:text-purple-300 border border-purple-400/40">⭐ 합동 (6)</button>
          <button onclick="renderGalleryGrid('sd')" id="galTabSd" class="px-2 py-1 rounded-lg text-[11px] font-bold sub-box text-pink-600 dark:text-pink-300 border border-pink-400/40">🐣 SD 치비 (9)</button>"""

text = re.sub(
    r'<div class="px-4 py-2 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-700 flex[^>]*>[\s\S]*?</div>\s*<div id="galleryGridContainer"',
    f'<div class="px-4 py-2 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-700 flex flex-wrap gap-1.5">\n          {new_gal_tabs}\n        </div>\n\n        <div id="galleryGridContainer"',
    text,
    count=1
)

# 3. Read current HEROINE_EVENTS and DUAL_EVENTS
# Define new events to append to gemini, kotone, mio, and dual
gemini_extras = """        {
          key: 'ev21',
          tag: '💪 케이블 시티드 로우 조각 등 라인',
          locOutfit: '📍 웨이트존 로우 머신 · 탄탄한 견갑골 & 시선 너머 츤데레 미소',
          img: './image/03 gemini/gemini_21_cable_row.png',
          pos: 'center 15%',
          text: '제대로 봐, 프로듀서! 광배근이랑 견갑골을 꽉 쪼여야 옷태가 사는 거야. 딴생각 말고 내 자세에 집중해! 🐾💪',
          story: '💖 [제미니 EP.21 · 케이블 시티드 로우] "V바를 복부까지 당기며 고개를 돌려 널 쳐다봤어. 땀방울이 맺힌 내 등 라인이 예쁘다고 넋을 잃고 보길래... 일부러 더 세게 당겼잖아."'
        },
        {
          key: 'ev22',
          tag: '🔥 2분 엘보 플랭크 정면 맞대결',
          locOutfit: '📍 블랙 매트 바닥 시점 · 턱 끝에 맺힌 땀방울 & 결의의 눈맞춤',
          img: './image/03 gemini/gemini_22_plank_challenge.png',
          pos: 'center 15%',
          text: '마지막 15초 남았어! 무릎 먼저 닿는 사람이 내일 아침 말차 타주기 내기야, 절대 안 져! 🔥🐾',
          story: '💖 [제미니 EP.22 · 2분 플랭크 챌린지] "매트 위에서 코앞까지 얼굴을 마주 보고 플랭크로 버텼어. 가쁜 숨소리가 닿을 때마다 심장이 터질 것 같았지만... 널 이기고 싶어서 끝까지 버텼어."'
        },
        {
          key: 'ev23',
          tag: '🌙 루프탑 오버핏 후디 캔 호지차',
          locOutfit: '📍 심야 루프탑 난간 · 바람에 날리는 흑발 & 볼에 댄 따뜻한 캔',
          img: './image/03 gemini/gemini_23_night_rooftop_hoodie.png',
          pos: 'center 15%',
          text: '야경 보면서 마시는 따뜻한 차... 너랑 함께 달린 뒤라서 그런지 도시 불빛이 평소보다 훨씬 눈부시네. 🌙✨',
          story: '💖 [제미니 EP.23 · 심야 루프탑 후디] "차가운 밤바람에 펄럭이는 후디를 여미며 따뜻한 캔을 건넸어. 너와 둘만 있는 이 도시의 밤이 너무 소중해서 살며시 네 어깨 쪽에 다가섰어."'
        },
        {
          key: 'ev24',
          tag: '🎯 케틀벨 스윙 폭발적 힙 힌지',
          locOutfit: '📍 프리웨이트 미러존 · 가슴 높이 케틀벨 락아웃 & 역동적 파워',
          img: './image/03 gemini/gemini_24_kettlebell_swing.png',
          pos: 'center 15%',
          text: '팔로 드는 게 아니라 고관절 힙 힌지로 튕겨내는 거야! 내 힙 파워 봤지? 프로듀서도 똑같이 해봐! 🎯🐾',
          story: '💖 [제미니 EP.24 · 케틀벨 스윙 훈련] "거울 앞에서 폭발적으로 케틀벨을 밀어 올리며 당당한 코치 미소를 지어 보였어. 네가 감탄하는 표정을 볼 때가 제일 짜릿하단 말이야."'
        },
        {
          key: 'ev25',
          tag: '🫐 블루베리 프로틴 스무디 1+1 나눔',
          locOutfit: '📍 주스 바 우드 스툴 · 붉어진 볼 & 슬그머니 건네는 유리잔',
          img: './image/03 gemini/gemini_25_post_workout_smoothie.png',
          pos: 'center 15%',
          text: '원플러스원 행사라서 어쩔 수 없이 하나 더 받아온 거야! 널 위해서 특별히 시킨 거 절대 아니니까... 빨리 마시기나 해! 🫐🐾',
          story: '💖 [제미니 EP.25 · 주스 바 스툴 나눔] "보라색 블루베리 스무디 잔을 네 쪽으로 쓱 밀어놓고 귓바퀴를 붉혔어. 네 취향으로 주문했다는 걸 들키지 않으려고 딴청을 피웠지만... 기분은 최고였어."'
        },
        {
          key: 'sd3',
          tag: '🐣 [SD] 플랭크 2분 부들부들 진동 냥이',
          locOutfit: '📍 모리키노코 SD · 파들파들 떨리는 2등신 콩눈 사투',
          img: './image/03 gemini/sd_gemini_03_plank_shiver.png',
          pos: 'center 15%',
          text: '부들부들부들... 복근에 모터 달렸냐고 놀리지 마 바보야... 귀까지 파들파들 떨린단 말이야아! 🐾💦',
          story: '🐣 [제미니 SD EP.3 · 부들부들 플랭크 사투] "모리키노코 특유의 2등신 콩눈 제미니가 온몸을 사시나무 떨듯 부들부들 떨며 만화 같은 땀방울을 사방으로 튀기는 역대급 코믹 씬!"'
        }"""

kotone_extras = """        {
          key: 'ev7',
          tag: '🍓 훈련 후 벤치 베리 스무디 미소',
          locOutfit: '📍 센터 우드 벤치 · 옐로우 트레이닝복 & 스트라이프 빨대',
          img: './image/02 kotone/kotone_07_smoothie_bench.png',
          pos: 'center 15%',
          text: '프로듀서님과 땀 흘린 뒤에 마시는 베리 스무디는 세상에서 제일 달콤해요! 꿀꺽~ 헤헤! 🍓💛',
          story: '💖 [코토네 EP.7 · 벤치 베리 스무디] "벤치에 나란히 앉아 차가운 컵을 두 손으로 쥐고 웃었어요. 프로듀서님께서 땀을 닦아주시는 다정한 손길에 코토네의 가슴도 달콤하게 녹아내렸답니다."'
        },
        {
          key: 'ev21',
          tag: '⚡ 댄스 스튜디오 스피드 줄넘기',
          locOutfit: '📍 마룻바닥 스튜디오 · 공중 도약 & 허공을 가르는 트윈테일',
          img: './image/02 kotone/kotone_21_jump_rope.png',
          pos: 'center 15%',
          text: '100회 돌파! 200회 갑니다아~! 센터 아이돌의 무한 유산소 체력, 프로듀서님께 보여드릴게요! ⚡💛',
          story: '💖 [코토네 EP.21 · 스피드 줄넘기 점프] "공중으로 폴짝 뛰어오를 때마다 반짝이는 땀방울과 휘날리는 노란 리본! 프로듀서님의 응원 소리가 들려오면 코토네는 백 번이라도 더 뛸 수 있어요!"'
        },
        {
          key: 'ev22',
          tag: '🏋️ 핑크 패드 바벨 힙스러스트',
          locOutfit: '📍 벤치 웨이트존 · 핑크 바벨 패드 & 힙업 집중 코토네',
          img: './image/02 kotone/kotone_22_hip_thrust.png',
          pos: 'center 15%',
          text: '후우- 흡! 무대 위에서 가장 완벽한 댄스 각선미를 위해! 프로듀서님, 코토네 힙 락아웃 자세 완벽하죠?! 🏋️‍♀️✨',
          story: '💖 [코토네 EP.22 · 바벨 힙스러스트] "무거운 바벨을 골반에 얹고 힘차게 밀어 올렸어요. 프로듀서님이 자세를 칭찬해 주실 때마다 알바 피로가 싹 날아가고 자신감이 솟구쳐요!"'
        },
        {
          key: 'ev23',
          tag: '💦 마룻바닥 쿨다운 스포츠 보틀',
          locOutfit: '📍 댄스 연습실 코너 · 어깨에 두른 타월 & 얼음물 한 모금',
          img: './image/02 kotone/kotone_23_sports_drink_towel.png',
          pos: 'center 15%',
          text: '하아아~ 프로듀서님이 건네주신 시원한 스포츠 드링크 마시니까 온몸에 활력이 1000% 충전됐어요! 💦💛',
          story: '💖 [코토네 EP.23 · 연습실 바닥 쿨다운] "마룻바닥에 팔을 짚고 기대앉아 시원한 물을 마셨어요. 젖은 머리칼을 쓸어 넘기며 마주친 프로듀서님의 따뜻한 눈빛에 심장이 사르르 녹아내렸답니다."'
        },
        {
          key: 'ev24',
          tag: '🎀 필라테스 래더 바렐 사이드 아치',
          locOutfit: '📍 부티크 기구 필라테스룸 · 우아한 곡선 스트레칭 & 까르르 웃음',
          img: './image/02 kotone/kotone_24_pilates_ladder.png',
          pos: 'center 15%',
          text: '프로듀서님 보세요! 리본처럼 유연하게 쭈욱~ 코토네의 코어 라인 점점 더 슬림해지고 있죠? 🎀✨',
          story: '💖 [코토네 EP.24 · 래더 바렐 아치] "나무 바렐 위에서 우아하게 팔을 뻗어 옆구리를 늘렸어요. 코토네의 유연성에 감탄하시는 프로듀서님 표정이 너무 귀여워서 까르르 웃음이 터졌답니다."'
        },
        {
          key: 'ev25',
          tag: '🍠 심야 편의점 따끈한 군고구마 반 토막',
          locOutfit: '📍 편의점 파라솔 의자 · 김이 모락모락 나는 황금빛 고구마 나눔',
          img: './image/02 kotone/kotone_25_night_convenience_chat.png',
          pos: 'center 15%',
          text: '오늘 훈련도 완벽 클리어! 더 큰 쪽은 프로듀서님 거예요! 우리 둘이 손잡고 52kg 꼭 성공해요, 약속! 🍠💛',
          story: '💖 [코토네 EP.25 · 심야 편의점 군고구마] "가로등 불빛 아래에서 따끈한 고구마를 반으로 쪼개어 건넸어요. 김이 모락모락 피어오르는 사이로 전해진 온기는 코토네 인생 최고의 행복이었답니다."'
        },
        {
          key: 'sd3',
          tag: '🐣 [SD] 체중계 0.2kg 증가 멘붕 절규',
          locOutfit: '📍 모리키노코 SD · 미니 체중계 위 볼 감싸 쥔 콩눈 공포',
          img: './image/02 kotone/sd_kotone_03_scale_shock.png',
          pos: 'center 15%',
          text: '으에에엑?! 0.2kg 늘었어어어?! 방금 마신 물 한 컵 무게가 그대로 잰 거 맞죠?! 코토네 멘붕이에요오! 💸😱',
          story: '🐣 [코토네 SD EP.3 · 눈물의 0.2kg 절규] "모리키노코 2등신 콩눈 코토네가 미니 체중계 위에서 양 볼을 감싸 쥐고 영혼이 탈출하는 표정으로 절규하는 레전드 개그 씬!"'
        }"""

mio_extras = """        {
          key: 'ev21',
          tag: '☀️ 햇살 가득 공원 트랙 러닝 미소',
          locOutfit: '📍 녹음 짙은 공원 트랙 · 오렌지 저지 & 반짝이는 눈맞춤',
          img: './image/01 mio/mio_21_sunlight_track.png',
          pos: 'center 14%',
          text: '프로듀서! 햇살 받으면서 달리는 거 진짜 최고지?! 우리 20바퀴 목표까지 같이 힘차게 달려보자구! ☀️🏃‍♀️',
          story: '💖 [미오 EP.21 · 햇살 공원 트랙 러닝] "초록빛 나뭇잎 사이로 눈부신 햇살이 쏟아지는 트랙에서 미오가 환하게 웃어 보였어요! 프로듀서의 페이스에 맞춰 함께 호흡하며 달리는 이 순간이 너무 행복했어!"'
        },
        {
          key: 'ev22',
          tag: '🌊 파도치는 배틀로프 풀파워 슬램',
          locOutfit: '📍 웨이트존 바닥 · 출렁이는 검은 로프 파도 & 땀방울 날리는 미소',
          img: './image/01 mio/mio_22_battle_ropes.png',
          pos: 'center 14%',
          text: '파도처럼 철썩철썩! 상체 체지방이 불타는 소리 들리지 프로듀서?! 이 기세로 1분 더 가자! 🌊💪',
          story: '💖 [미오 EP.22 · 배틀로프 전신 버닝] "두꺼운 로프를 양손으로 쥐고 연속 슬램을 내리꽂았어! 출렁이는 로프 파도 속에서 프로듀서와 눈이 마주친 순간 터져 나온 아드레날린은 무적이었어!"'
        },
        {
          key: 'ev23',
          tag: '🏃 스타디움 콘크리트 계단 스퍼트',
          locOutfit: '📍 석양빛 스타디움 계단 꼭대기 · 뒤돌아 손 내미는 눈부신 미소',
          img: './image/01 mio/mio_23_stair_sprint.png',
          pos: 'center 14%',
          text: '계단 100개 완주! 프로듀서 손 잡아, 제일 높은 꼭대기에서 노을 같이 보자! 🏃‍♀️🌇',
          story: '💖 [미오 EP.23 · 스타디움 계단 스퍼트] "숨을 헐떡이며 계단 정상에 먼저 도착해 프로듀서를 향해 손을 뻗었어. 붉게 물든 노을 속에서 맞잡은 손바닥의 온기가 가슴속 깊이 남았어."'
        },
        {
          key: 'ev24',
          tag: '🪞 랫풀다운 거울 눈맞춤 광배근 코칭',
          locOutfit: '📍 케이블 랫풀다운 머신 · 와이드 그립 바 가슴 당기기',
          img: './image/01 mio/mio_24_lat_pulldown.png',
          pos: 'center 14%',
          text: '20회 4세트 3세트째! 팔꿈치를 수직으로 찍어 누르는 느낌... 프로듀서가 가르쳐준 대로 딱 잡았지? 🪞✨',
          story: '💖 [미오 EP.24 · 랫풀다운 광배근 단련] "거울을 통해 프로듀서와 눈을 맞추며 바를 부드럽게 가슴으로 끌어당겼어. 탄탄하게 자리 잡은 등 근육을 칭찬해 주는 프로듀서 목소리에 힘이 번쩍 났어!"'
        },
        {
          key: 'ev25',
          tag: '🌌 트랙 잔디밭 누워 밤하늘 별 보기',
          locOutfit: '📍 야간 스타디움 필드 잔디 · 나란히 누워 마주 보는 다정한 눈빛',
          img: './image/01 mio/mio_25_night_stargazing.png',
          pos: 'center 14%',
          text: '밤하늘에 별 진짜 많다... 프로듀서와 함께 달리고 이렇게 누워있는 이 시간이, 세상에서 제일 행복해. 🌌🌟',
          story: '💖 [미오 EP.25 · 밤하늘 별빛 잔디밭] "10km 야간 러닝을 마치고 잔디밭에 나란히 누워 고개를 돌렸어. 별빛을 담은 프로듀서 눈동자를 바라보며 속삭인 진심은 미오의 소중한 고백이었어."'
        },
        {
          key: 'sd3',
          tag: '🐣 [SD] 통통 튀는 고무공 버피 100회',
          locOutfit: '📍 모리키노코 SD · 용수철 스프링 달고 통통 튀는 콩눈 미오',
          img: './image/01 mio/sd_mio_03_burpee_bounce.png',
          pos: 'center 14%',
          text: '통- 통- 통! 버피 테스트 100회 초스피드 완료! 미오 짱은 지치지 않는 무한 에너지 고무공이라구! 🌟💨',
          story: '🐣 [미오 SD EP.3 · 무한 통통 버피 점프] "모리키노코 특유의 2등신 콩눈 미오가 발밑에 용수철을 단 것처럼 통통 튀며 광속 버피를 뛰는 웃음 폭발 SD 코믹 씬!"'
        }"""

trio_extras = """      {
        key: 'trio5',
        tag: '🥗 키친 아일랜드 다이어트 밀프랩 파티',
        locOutfit: '📍 햇살 키친 · 핑크 앞치마 제미니 & 고구마 코토네 & 아보카도 미오',
        img: './image/00 common/trio_05_cooking_mealprep.png',
        pos: 'center 15%',
        text: '제미니 · 코토네 · 미오: 프로듀서의 클린 식단을 위해 우리 셋이 정성껏 만든 특제 헬시 도시락 완성! 🥗🍱💖',
        story: '💖 [3인 합동 EP.5 · 키친 헬시 밀프랩 파티] "닭가슴살을 굽는 제미니, 고구마를 담는 코토네, 아보카도를 써는 미오가 앞치마를 두르고 까르르 웃으며 도시락을 완성했어요! 세상에서 제일 맛있는 특급 사랑의 식단!"'
      },
      {
        key: 'trio6',
        tag: '🎆 여름밤 언덕 스파클러 불꽃 축하',
        locOutfit: '📍 불꽃축제 언덕 · 3색 유카타 & 타오르는 스파클러 & 빛나는 눈맞춤',
        img: './image/00 common/trio_06_fireworks_summer.png',
        pos: 'center 15%',
        text: '제미니 · 코토네 · 미오: 함께 달려온 모든 계절에 감사하며... 프로듀서, 목표 체중 52kg 성공을 진심으로 축하해! 사랑해! 🎆💖',
        story: '💖 [3인 합동 EP.6 · 여름밤 스파클러 피날레] "언덕 위에서 밤하늘 불꽃놀이를 배경으로 셋이 타오르는 스파클러를 들고 프로듀서를 둘러쌌어요! 흘린 땀방울과 눈부신 추억이 영원한 사랑으로 완성된 감동의 순간!"'
      }"""

# Insert gemini extras before kotone
text = text.replace(
    """        {
          key: 'sd2',
          tag: '🐣 [SD] 광속 폭풍 말차 격불',
          locOutfit: '📍 모리키노코 SD · 대형 다완 & 초고속 차선 휘젓기',
          img: './image/03 gemini/sd_gemini_02_matcha_whisk.png',
          pos: 'center 15%',
          text: '카테킨 폭풍 격불이다냥!! 거품이 넘칠 때까지 분노의 말차 차선 젓기! 🍵💨',
          story: '🐣 [제미니 SD EP.2 · 폭풍의 말차 격불] "대형 말차 그릇 앞에서 진지한 콩눈 표정으로 차선을 빛의 속도로 휘젓는 제미니! 튀어오르는 초록빛 거품과 결의에 찬 눈망울이 너무 깜찍합니다!"'
        }
      ],""",
    f"""        {{
          key: 'sd2',
          tag: '🐣 [SD] 광속 폭풍 말차 격불',
          locOutfit: '📍 모리키노코 SD · 대형 다완 & 초고속 차선 휘젓기',
          img: './image/03 gemini/sd_gemini_02_matcha_whisk.png',
          pos: 'center 15%',
          text: '카테킨 폭풍 격불이다냥!! 거품이 넘칠 때까지 분노의 말차 차선 젓기! 🍵💨',
          story: '🐣 [제미니 SD EP.2 · 폭풍의 말차 격불] "대형 말차 그릇 앞에서 진지한 콩눈 표정으로 차선을 빛의 속도로 휘젓는 제미니! 튀어오르는 초록빛 거품과 결의에 찬 눈망울이 너무 깜찍합니다!"'
        }},
{gemini_extras}
      ],"""
)

# Insert kotone extras before mio
text = text.replace(
    """        {
          key: 'sd2',
          tag: '🐣 [SD] 복근 50개 후 버터 팬케이크화',
          locOutfit: '📍 모리키노코 SD · 마룻바닥에 납작하게 녹아내린 핫케이크',
          img: './image/02 kotone/sd_kotone_02_butter_melt.png',
          pos: 'center 15%',
          text: '크런치 50회 2세트... 코토네는 이제 버터처럼 녹아버렸어요... 영혼 가출 삐이... 🥞👻',
          story: '🐣 [코토네 SD EP.2 · 바닥에 녹은 버터 팬케이크] "체육관 바닥에 노란 버터처럼 납작하게 녹아내려 빙글빙글 뱅뱅이 눈을 한 코토네! 입에서 하얀 영혼 유령이 둥실 떠오르는 역대급 개그 컷!"'
        }
      ],""",
    f"""        {{
          key: 'sd2',
          tag: '🐣 [SD] 복근 50개 후 버터 팬케이크화',
          locOutfit: '📍 모리키노코 SD · 마룻바닥에 납작하게 녹아내린 핫케이크',
          img: './image/02 kotone/sd_kotone_02_butter_melt.png',
          pos: 'center 15%',
          text: '크런치 50회 2세트... 코토네는 이제 버터처럼 녹아버렸어요... 영혼 가출 삐이... 🥞👻',
          story: '🐣 [코토네 SD EP.2 · 바닥에 녹은 버터 팬케이크] "체육관 바닥에 노란 버터처럼 납작하게 녹아내려 빙글빙글 뱅뱅이 눈을 한 코토네! 입에서 하얀 영혼 유령이 둥실 떠오르는 역대급 개그 컷!"'
        }},
{kotone_extras}
      ],"""
)

# Insert mio extras before DUAL_EVENTS
text = text.replace(
    """        {
          key: 'sd2',
          tag: '🐣 [SD] 레그레이즈 50개 후 크레페화',
          locOutfit: '📍 모리키노코 SD · 파란 요가매트 위 모락모락 김나는 납작이',
          img: './image/01 mio/sd_mio_02_legraise_melt.png',
          pos: 'center 14%',
          text: '행잉 레그레이즈 50회 완주... 머리에서 김이 모락모락... 미오는 크레페가 되었습니다... 🥞💨',
          story: '🐣 [미오 SD EP.2 · 캡틴스 체어 레그레이즈 방전] "요가매트 위에 갓 구운 크레페처럼 납작하게 눌려버린 미오! 콩눈으로 천장을 멍하니 바라보며 머리 위로 하얀 김을 뿜어내는 레전드 개그 씬!"'
        }
      ]
    };""",
    f"""        {{
          key: 'sd2',
          tag: '🐣 [SD] 레그레이즈 50개 후 크레페화',
          locOutfit: '📍 모리키노코 SD · 파란 요가매트 위 모락모락 김나는 납작이',
          img: './image/01 mio/sd_mio_02_legraise_melt.png',
          pos: 'center 14%',
          text: '행잉 레그레이즈 50회 완주... 머리에서 김이 모락모락... 미오는 크레페가 되었습니다... 🥞💨',
          story: '🐣 [미오 SD EP.2 · 캡틴스 체어 레그레이즈 방전] "요가매트 위에 갓 구운 크레페처럼 납작하게 눌려버린 미오! 콩눈으로 천장을 멍하니 바라보며 머리 위로 하얀 김을 뿜어내는 레전드 개그 씬!"'
        }},
{mio_extras}
      ]
    }};"""
)

# Insert trio extras into DUAL_EVENTS
text = text.replace(
    """        text: '제미니 · 코토네 · 미오: 해냈다 프로듀서! 목표 체중 52kg 감량 대성공! 우리 셋의 영원한 프로듀서, 사랑해! 🌇💖',
        story: '💖 [3인 합동 EP.4 · 황혼빛 루프탑 승리] "황금빛 노을이 쏟아지는 루프탑에서 셋이 프로듀서의 손을 높이 번쩍 들어 올렸어요! 서로 흘린 땀방울이 눈부신 추억으로 완성된 순간!"'
      }
    ];""",
    f"""        text: '제미니 · 코토네 · 미오: 해냈다 프로듀서! 목표 체중 52kg 감량 대성공! 우리 셋의 영원한 프로듀서, 사랑해! 🌇💖',
        story: '💖 [3인 합동 EP.4 · 황혼빛 루프탑 승리] "황금빛 노을이 쏟아지는 루프탑에서 셋이 프로듀서의 손을 높이 번쩍 들어 올렸어요! 서로 흘린 땀방울이 눈부신 추억으로 완성된 순간!"'
      }},
{trio_extras}
    ];"""
)

index_path.write_text(text, encoding="utf-8")
print("assemble_90_cg.py finished cleanly!")
