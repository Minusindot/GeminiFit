# TTS 오디션 랩

Gemini Fit의 세 캐릭터(제미니 · 코토네 · 미오) 목소리를 **듣고 고르는** 도구입니다.
여기서 고른 목소리로 나중에 `kotonoha_data.js`의 실제 낭독 문장(약 180줄)을 한 번에 구워
`audio/kotonoha/auto/` 프리셋 MP3로 넣습니다.

## 1. 후보 생성

```bash
# VOICEVOX (api.tts.quest, 무료 · 키 불필요)
python tools/tts_lab/tts_lab.py voicevox --ids 0-59

# 특정 ID만 다시 뽑기
python tools/tts_lab/tts_lab.py voicevox --ids 2,8,12 --force

# Fish Audio 무료 모델 (s2.1-pro-free, 키 필요)
set FISH_AUDIO_API_KEY=발급받은키
python tools/tts_lab/tts_lab.py fish --voices <model_id>,<model_id>

# Gemini TTS (환경변수 GEMINI_API_KEY 사용)
python tools/tts_lab/tts_lab.py gemini --voices Kore,Leda,Aoede

# 클립만 다시 스캔해서 manifest 재생성 (네트워크 없음)
python tools/tts_lab/tts_lab.py report
```

결과물은 `tools/tts_lab/clips/*.mp3` + `manifest.json`에 쌓입니다.
이미 받은 클립은 건너뛰므로 중간에 끊겨도 이어서 실행하면 됩니다.

## 2. 듣고 고르기

로컬 서버를 띄운 뒤 브라우저에서 엽니다.

```bash
python -m http.server 8777
```

→ <http://127.0.0.1:8777/tools/tts_lab/audition.html>

- ▶ 또는 `Space`로 재생, 자동으로 다음 후보로 넘어갑니다
- `1`~`5` 키로 별점
- 상단에서 **제미니 / 코토네 / 미오** 슬롯을 고른 뒤 행의 **배정** 버튼
- `선택 결과 복사` → JSON을 그대로 저에게 붙여주시면 배치 작업을 진행합니다

## 3. 배치 (다음 단계)

고른 목소리가 정해지면:

```bash
# 무엇이 구워질지 먼저 확인 (네트워크 없음)
python tools/tts_lab/batch_tts.py --selection tts_selection.json --dry-run

# 실제 생성 (무료 tts.quest 기준 약 12분, 144줄)
python tools/tts_lab/batch_tts.py --selection tts_selection.json

# kotonoha_engine.js 에 붙일 매핑 스니펫 생성
python tools/tts_lab/batch_tts.py --emit-js
```

- `kotonoha_data.js`의 **스토리 대사 84개 + 퀴즈 단어 82개 + 레슨 제목 19개** 중
  중복 제거·기존 수제 MP3 제외 시 **약 144줄**이 대상입니다
- 결과물: `audio/kotonoha/auto/*.mp3` + `tools/tts_lab/preset_map.json`
- `preset_map.json`의 문장 키는 앱의 `cleanKotonohaTtsText()`와 **동일한 함수**로
  계산되므로 런타임 캐시 키와 정확히 일치합니다
- 기존 수제 녹음(`day1_step*.mp3` 등)은 덮어쓰지 않습니다 (`--include-existing` 로만 재생성)

이렇게 하면 런타임에는 API 호출이 0이 되고, 오프라인에서도 재생되며,
tts.quest 레이트리밋과 무관해집니다.

## ⚠️ Fish Audio 비용 주의

`model` 은 **JSON 본문이 아니라 HTTP 헤더**로 보내야 합니다.

```python
headers = {"Authorization": f"Bearer {key}", "model": "s2.1-pro-free"}   # ✅
json    = {"text": ..., "model": "s2.1-pro-free"}                        # ❌ 유료로 청구됨
```

본문에만 넣으면 API가 조용히 **유료 `s2.1-pro`로 폴백**합니다 (공식 문서 명시).
실제로 이 실수로 후보 21개를 만드는 데 **$0.059 (약 80원)** 이 청구됐습니다.
현재 코드는 헤더로 보내고, 실행 중 잔액이 줄면 즉시 중단하는 가드를 갖고 있습니다.

잔액 확인:

```bash
curl -H "Authorization: Bearer $FISH_AUDIO_API_KEY" https://api.fish.audio/wallet/self/api-credit
```

VOICEVOX(tts.quest)는 키도 결제도 없이 **완전 무료**이므로, 비용을 절대 쓰고 싶지
않다면 배치도 VOICEVOX로만 돌리면 됩니다.

## 라이선스 주의

- **VOICEVOX**: 각 캐릭터 이용약관(크레딧 표기)을 지켜야 합니다.
- **Fish Audio `s2.1-pro-free`**: 개발/테스트용 무료 모델입니다. 실서비스 상시 호출은 약관 확인 필요.
- 기존 애니 캐릭터의 목소리를 복제한 모델은 **배포 시 권리 문제**가 있으니 사용하지 않습니다.
