# 🎭 言の葉茶屋 (Kotonoha Chaya) - 정통 비주얼 노벨 (VN) 에셋 규격서

본 문서는 프로듀서님의 미연시 프로젝트 표준 규격(동일 바디 포즈 + 표정 스프라이트 시스템)을 기반으로 작성되었습니다.
본 규격은 웹앱(`kotonoha_engine.js`)과 차후 **Naninovel 엔진** 포팅 시 100% 1:1 호환됩니다.

---

## 🎨 1. 캐릭터 표정 규격 (총 14종)

동일한 베이스 바디 포즈(투명 배경 PNG)를 유지하면서, 대화 상황과 감정에 따라 표정만 부드럽게 크로스페이드 전환됩니다.

### 🌟 기본 표정 6종 (Standard Expressions)
| 코드 | 표정 명칭 | 감정 및 사용 상황 | Naninovel 매핑 |
|:---:|:---:|:---|:---:|
| `idle` | 기본 (IDLE) | 평온하고 단아한 기본 표정, 일상적인 경청 및 대기 상태 | `@char gemini.idle` |
| `smile` | 미소 (SMILE) | 밝고 활짝 웃는 표정, 칭찬, 기쁨, 장난스러운 인사 | `@char gemini.smile` |
| `sad` | 슬픔 (SAD) | 눈썹이 처지고 시무룩한 표정, 아쉬움, 걱정, 동정 | `@char gemini.sad` |
| `angry` | 화남/새침 (ANGRY) | 미간을 찌푸린 뾰로통한 표정, 츤데레 츳코미, 운동 잔소리 | `@char gemini.angry` |
| `shy` | 부끄러움 (SHY) | 뺨이 붉게 달아오른 수줍은 표정, 칭찬받았을 때, 심쿵 | `@char gemini.shy` |
| `shock` | 충격/경악 (SHOCK) | 눈이 동그래지고 입을 벌린 멘붕 표정, 체중계 숫자, 돌발 상황 | `@char gemini.shock` |

### 🔮 특별 표정 8종 (Special Expressions, v4.3.17)
| 코드 | 표정 명칭 | 감정 및 사용 상황 | Naninovel 매핑 |
|:---:|:---:|:---|:---:|
| `dark` | 어두움/정색 (DARK) | 눈에 하이라이트가 죽거나 음영이 드리운 차가운 표정, 단식 어겼을 때 | `@char gemini.dark` |
| `joke` | 익살/장난 (JOKE) | 윙크, 혓바닥 내밀기, 능글맞은 미소, 장난칠 때 | `@char gemini.joke` |
| `wink` | 윙크 (WINK) | 한쪽 눈을 감은 밝은 윙크, 응원·격려, 게임클리어 인사 | `@char gemini.wink` |
| `pout` | 삐침 (POUT) | 뺨을 부풀린 삐친 표정, 츤데레 토라짐, 투정 | `@char gemini.pout` |
| `cry` | 울음 (CRY) | 눈물이 맺힌 울먹 표정, 과격 운동 후 처짐, 감동·위로가 필요할 때 | `@char gemini.cry` |
| `smirk` | 씨익 (SMIRK) | 한쪽 눈썹을 올린 능글맞은 자신 표정, 메타 응원, 게임 전략 | `@char gemini.smirk` |
| `love` | 연정 (LOVE) | 하트 눈, 두 손 모은 숭배 표정, 폭풍 칭찬·응원 | `@char gemini.love` |
| `sleepy` | 졸림 (SLEEPY) | 반쯤 감긴 졸린 눈, 하품, 늦은 밤 단식·회복 장면 | `@char gemini.sleepy` |

---

## 📁 2. 파일 저장 경로 및 네이밍 규칙

### 1) 스탠딩 캐릭터 (SCG): `image/scg/{캐릭터}/`
* **규격**: 배경 100% 투명 (Alpha channel PNG), 1080x2560 (또는 종횡비 약 1:2.4~1:3 세로형 전신/반신)
* **네이밍 포맷**: `{캐릭터}_{의상}_{표정}.png`

#### 제미니 (Gemini - 흑발 네코미미 사범)
* `image/scg/gemini/gemini_default_idle.png` — 기본 (스포츠브라·레깅스)
* `image/scg/gemini/gemini_teahouse_smile.png` — 다실 유카타+에이프론 (전 표정 14종)
* `image/scg/gemini/gemini_menhera_dark.png` — 멘헤라 패션 (전 표정 14종)
* 그 외 표정: `{idle, smile, sad, angry, shy, shock, dark, joke, wink, pout, cry, smirk, love, sleepy}`

#### 코토네 (Kotone - 자본주의 조교)
* `image/scg/kotone/kotone_default_idle.png` — 기본 (민트 트랙탑)
* `image/scg/kotone/kotone_casual_idle.png` — **일상 사복** (크림 오프숄더 니트 + 핑크 플리츠 미디 스커트 + 로퍼) · 7표정 (v4.3.46)
* `image/scg/kotone/kotone_gakumas_idle.png` — **학원마스 원작 아이돌 의상** (흰 퍼프 블라우스 + 하늘색 코르셋 + 러플 스커트 + 노랑 리본) · 7표정 (v4.3.46)
* `image/scg/kotone/kotone_dress_smile.png` — 아이돌 핑크 프릴 드레스 (레거시, 전 표정 14종)
* 그 외 표정: `{idle, smile, sad, angry, shy, shock, dark, joke, wink, pout, cry, smirk, love, sleepy}`

#### 미오 (Mio - 에너제틱 러닝돌)
* `image/scg/mio/mio_default_idle.png` — 기본 (레드/화이트 트랙탑)
* `image/scg/mio/mio_runwear_smile.png` — 러닝웨어 (전 표정 14종)
* `image/scg/mio/mio_casual_idle.png` — **일상 사복** (옐로 니트 가디건 + 흰 캐미솔 + 데님 스커트 + 스니커즈) · 7표정 (v4.3.46)
* 그 외 표정: `{idle, smile, sad, angry, shy, shock, dark, joke, wink, pout, cry, smirk, love, sleepy}`

#### 부분 세트 (7표정 이하 → `_idle`로 자동 하강)
* `image/scg/gemini/gemini_yukata_{idle,smile,shy,pout,love}.png` (5표정)
* `image/scg/kotone/kotone_casual_*`, `kotone_gakumas_*`, `image/scg/mio/mio_casual_*` (각 7표정: `idle, smile, shy, shock, joke, love, pout`)
* 위 목록에 없는 `expr`을 쓰면 엔진이 자동으로 `{outfit}_idle.png`로 내려간다(`KOTONOHA_SCG_LIMITED_EXPR`).

### 👗 의상 자동 배치 규칙 (v4.3.46)

헬스장 복장이 상황과 무관하게 계속 나오던 문제를 고치기 위해, 엔진이 **장소 → 의상**을 먼저 판단한다.
`resolveKotonohaOutfit(step, lesson)` 우선순위:

1. `step.outfit`이 `default`가 아닌 명시값 → 그대로 사용 (연출 의도 우선)
2. `step.bg` 키 매핑 (`KOTONOHA_BG_OUTFIT`)

| bg 키 | gemini | kotone | mio |
| - | - | - | - |
| `gym_indoor`, `park_track` | default (스포츠) | default (트랙탑) | runwear |
| `teahouse_day/night` | teahouse (기모노+앞치마) | **casual** | **casual** |
| `ryokan_room`, `festival_night` | **yukata** | **casual** | **casual** |
| `osaka_street`, `bookstore` | menhera (캐주얼 후디) | **casual** | **casual** |

3. `sceneImg` 파일명 키워드 (`KOTONOHA_SCENE_OUTFIT_RULES`) — AI가 즉석 생성한 화는 `bg` 없이 `bgImage`만 있으므로 이 규칙으로 추론한다.
4. 그래도 없으면 `default`.

즉 **`outfit`을 일부러 `default`로 적어두면 장소가 헬스장일 때만 트레이닝복이 나온다.** 나머지 장소에서는 2·3번 규칙이 이긴다(그래서 예전 데이터의 `default` 잔재가 자동 교정됨).

`kotone_gakumas`는 자동 배치 대상이 **아니다**. 무대·축하 연출처럼 작가가 `outfit: "gakumas"`로 콕 집은 장면에서만 나온다(현재 2-4 목표 달성 건배, 3-6 감사 인사).

SCG 파일이 없을 때의 하강 순서: `{outfit}_{expr}` → `{outfit}_idle` → `{char}_default_idle` → ECG 일러스트(`ecgFallback`).
`kotonohaScgError()`가 `data-scg-chain`을 따라 내려가므로, 새 의상을 일부 표정만 그려도 깨지지 않는다.

---

### 2) 순수 장소 배경 (BG): `image/bg/`
* **규격**: 인물이 전혀 없는 16:9 와이드 (1920x1080 권장 JPG 또는 PNG)
* **네이밍 포맷**: `bg_{장소}_{시간/상태}.png`
* **필수 배경 목록**:
  * `bg_teahouse_day.png` (교토 다실 실내 다다미방 낮)
  * `bg_teahouse_night.png` (교토 다실 실내 밤 등롱)
  * `bg_osaka_street.png` (오사카 번화가 거리)
  * `bg_ryokan_room.png` (온천 료칸 객실)
  * `bg_gym_indoor.png` (피트니스 헬스장)
  * `bg_park_track.png` (러닝 공원 산책로)
  * `bg_bookstore.png` (고서점 실내)

---

## 💻 3. 시나리오 데이터 연동 표준

```javascript
// kotonoha_data.js 에피소드 스텝 구조
{
  bg: "teahouse_day",            // image/bg/bg_teahouse_day.png 자동 매핑
  speaker: "gemini",             // 화자
  outfit: "default",             // 의상 세트
  expr: "shy",                   // 표정 (8종 코드)
  // -> 엔진이 자동으로 image/scg/gemini/gemini_default_shy.png 로드!
  
  jpRuby: "そ、そんなに見つめられたら…照れてしまいますえ…///",
  pron: "소, 손나니 미츠메라레타라… 테레테 시마이마스에…",
  ko: "그, 그렇게 빤히 바라보시면… 저, 부끄러워져 버린다 말이옵니다…///"
}
```

### 🎬 Naninovel 스크립트 1:1 자동 변환 결과
```naninovel
@back teahouse_day
@char gemini.shy pos:50
제미니: そ、そんなに見つめられたら…照れてしまいますえ…///
```

---

## 🛠️ 4. 에셋 생산 파이프라인 (v4.3.10 준비, 쿼터 해제 후 재개)

> 상태(2026-11-08): ✅ 완료 (SCG 24장 + BG 7장 실전 에셋, v4.3.11).
> 아래 절차대로 그대로 재개하면 된다. 레퍼런스 폴더는 `image/90 repository/`(레포 내장) 기준.

### 4-1. 레퍼런스 앵커 (캐릭터·화풍 일관성)
* 화풍: `image/90 repository/gakumas_style/` (U149 아트풍 = 본 프로젝트 미연시 스타일)
* 제미니: `image/90 repository/reference_gemini/` + `image/03 gemini/gemini_01_main.png`, `avatar_gemini.png`
* 코토네: `image/02 kotone/kotone_01_studio.png`, `avatar_kotone.png`
* 미오: `image/01 mio/mio_01_main.png`, `avatar_mio.png`

### 4-2. 생성 순서 (Grok + Firefox, `generate_assets_v4311.py`)
1. **BG 7종** → `image/bg/bg_{장소}.png` (16:9, 인물 없음, 1920x1080 RGB로 정규화)
2. **캐릭터당 베이스 스탠딩 1장** → `image/_scg_work/{char}/base_raw.png`
   * **순수 흰 배경**, 전신·정면·팔 내린 포즈, 참조 이미지로 얼굴/의상 고정
3. **표정 7종 편집** → `idle`을 제외한 7장을 **베이스를 참고 이미지로 첨부**해 편집 생성
   (동일 포즈·의상·흰 배경 유지, **표정만** 변경 지시) → `image/_scg_work/{char}/{expr}_raw.png`
4. **투명화**: `python make_scg_transparent.py`
   (`_common.remove_flat_background` = 테두리 연결 영역만 투명화, 흰 옷 보호 + idle 기준 공통 트림 박스 + 1080×2560 캔버스)
   → `image/scg/{char}/{char}_default_{expr}.png` (8종 × 3인 = 24장)

### 4-3. 데이터 연동
* 스텝에 `expr`/`bg`/`outfit` 필드를 추가하면 엔진(`resolveKotonohaVisuals`)이 자동 SCG 모드 전환.
* 현재 `kotonoha_data.js`는 `sceneImg`/`bgImage`만 있어 전부 ECG 모드 (v4.3.10 폴백도 동작).
* 에셋 도착 후 `expr` 값 매핑(감정 키워드 기준) → Naninovel 변환은 본 규격 표 참조.

### 4-4. 마무리 체크리스트
- [x] BG 7종 `image/bg/` 저장 확인
- [x] SCG 24종 `image/scg/{char}/` 저장 + 투명 채널 확인
- [x] 엔진 렌더링 스팟 체크 (SCG/BG/ECG 폴백)
- [x] 버전 범프 **v4.3.11** (`index.html`, `sw.js`) → 커밋·푸시

---

## 🚫 5. 퀴즈 스포일러 금지 규칙 (v4.3.50)

퀴즈는 **정답을 고르기 전에 답을 보여주면 안 된다.** 수요일 퀴즈에서 문제 카드가 정답 문장을 그대로 띄우던 사고가 있었다.

### 5-1. 데이터 규칙
* `promptJp` · `promptKo`에 **정답 선택지의 일본어/읽기/한자**를 적지 않는다. (`explanation`에만 허용)
* 정답의 **일부 조각(2자 이상 가나/한자)** 도 금지한다. 예: 정답 `三日坊主`에 `三日(3일) + 坊主(스님)` 같은 힌트, 정답 `おきばりやす`에 `おきばりやす의 과거형` 같은 설명은 정답을 그대로 알려주는 것과 같다.
* 같은 뜻의 선택지를 4개 안에 중복 배치하지 않는다.
* `targetWord`는 "출제 어휘"이므로 정답 선택지와 같아도 무방하다. 단 화면 노출은 엔진이 처리한다.

### 5-2. 엔진 방어 (kotonoha_engine.js)
* `kotonohaQuizExposesAnswer(q)`: `targetWord`와 정답 선택지가 실질적으로 같으면 **큰 카드를 한국어 큐로 교체**.
* `kotonohaQuizCueKo(q)`: 문제 문장 안의 **따옴표 한글**만 큐로 사용. 없으면 **큰 카드를 아예 생략**하고 힌트 버튼만 남긴다.
* 해당 퀴즈는 `promptPron`(발음) · 문제 버블 발음 재생 · 문제 진입 자동 TTS를 모두 차단한다.

### 5-3. 검증 (커밋 전 필수)
```bash
node tools/audit_quiz_leaks.js   # exit 1 이면 스포일러 → 커밋 금지
```
* 87퀴즈/20레슨 검사, 프롬프트·서브힌트 누출(정답 조각 포함) 및 중복 선택지를 잡는다.
* "masked at runtime" 목록은 엔진이 한국어 큐로 가리는 정상 케이스다.
