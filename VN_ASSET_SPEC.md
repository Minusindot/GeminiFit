# 🎭 言の葉茶屋 (Kotonoha Chaya) - 정통 비주얼 노벨 (VN) 에셋 규격서

본 문서는 프로듀서님의 미연시 프로젝트 표준 규격(동일 바디 포즈 + 표정 스프라이트 시스템)을 기반으로 작성되었습니다.
본 규격은 웹앱(`kotonoha_engine.js`)과 차후 **Naninovel 엔진** 포팅 시 100% 1:1 호환됩니다.

---

## 🎨 1. 캐릭터 표정 규격 (총 8종)

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

### 🔮 특별 표정 2종 (Special Expressions)
| 코드 | 표정 명칭 | 감정 및 사용 상황 | Naninovel 매핑 |
|:---:|:---:|:---|:---:|
| `dark` | 어두움/정색 (DARK) | 눈에 하이라이트가 죽거나 음영이 드리운 차가운 표정, 단식 어겼을 때 | `@char gemini.dark` |
| `joke` | 익살/장난 (JOKE) | 윙크, 혓바닥 내밀기, 능글맞은 미소, 장난칠 때 | `@char gemini.joke` |

---

## 📁 2. 파일 저장 경로 및 네이밍 규칙

### 1) 스탠딩 캐릭터 (SCG): `image/scg/{캐릭터}/`
* **규격**: 배경 100% 투명 (Alpha channel PNG), 1080x2560 (또는 종횡비 약 1:2.4~1:3 세로형 전신/반신)
* **네이밍 포맷**: `{캐릭터}_{의상}_{표정}.png`

#### 제미니 (Gemini - 흑발 네코미미 사범)
* `image/scg/gemini/gemini_default_idle.png`
* `image/scg/gemini/gemini_default_smile.png`
* `image/scg/gemini/gemini_default_sad.png`
* `image/scg/gemini/gemini_default_angry.png`
* `image/scg/gemini/gemini_default_shy.png`
* `image/scg/gemini/gemini_default_shock.png`
* `image/scg/gemini/gemini_default_dark.png`
* `image/scg/gemini/gemini_default_joke.png`

#### 코토네 (Kotone - 자본주의 조교)
* `image/scg/kotone/kotone_default_idle.png`
* `image/scg/kotone/kotone_default_smile.png`
* `image/scg/kotone/kotone_default_sad.png`
* `image/scg/kotone/kotone_default_angry.png`
* `image/scg/kotone/kotone_default_shy.png`
* `image/scg/kotone/kotone_default_shock.png`
* `image/scg/kotone/kotone_default_dark.png`
* `image/scg/kotone/kotone_default_joke.png`

#### 미오 (Mio - 에너제틱 러닝돌)
* `image/scg/mio/mio_default_idle.png`
* `image/scg/mio/mio_default_smile.png`
* `image/scg/mio/mio_default_sad.png`
* `image/scg/mio/mio_default_angry.png`
* `image/scg/mio/mio_default_shy.png`
* `image/scg/mio/mio_default_shock.png`
* `image/scg/mio/mio_default_dark.png`
* `image/scg/mio/mio_default_joke.png`

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
