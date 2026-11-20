# GeminiFit 프로젝트 가이드 & 작업 기준

> **AI/작업자 필독**: 이 문서는 폴더 이동 및 과거 배포 흔적으로 인한 혼동을 막기 위한 공식 기준 문서입니다.

## 1. 공식 배포 주소 & 저장소
- **실제 라이브 사이트 (GitHub Pages)**: https://minusindot.github.io/GeminiFit/
- **GitHub 저장소**: `https://github.com/Minusindot/GeminiFit.git` (`main` 브랜치)
- **로컬 워크스페이스 경로**: `D:\GoogleDrive\Works\02 AI Works\GeminiFit`
- **배포 방식**: `main` 브랜치에 커밋 & 푸시하면 GitHub Pages에 자동 반영됨.

> ⚠️ **과거 흔적 주의 (사용 금지)**  
> 코드 일부(`index.html` 디스코드 웹훅 아바타 폴백 등)나 `.vercelignore`에 남아 있는 `git-hub-private-psi.vercel.app`는 **예전 테스트 흔적**입니다. 라이브 확인 및 모든 링크 기준은 반드시 **https://minusindot.github.io/GeminiFit/** 를 사용하세요.

## 2. 핵심 파일 구조
- `index.html` — 메인 앱(UI, 식단/운동/인바디 기록, GitHub `state.json` 동기화, `buildComprehensiveConsultPrompt` Gemini 코칭 프롬프트 추출 등)
- `state.json` — 폰 ↔ PC 간 GitHub API로 실시간 동기화되는 사용자 상태 데이터
- `kotonoha_engine.js` / `kotonoha_data.js` — 일본어/코토노하 학습 및 에피소드 엔진
- `trainer_episodes.js` / `dialogue_pool.js` / `weekly_reports.js` — 3인 트레이너(제미니·코토네·미오) 대사, VN 에피소드, 주간 리포트
- `ocr_pipeline.js` — 인바디/러닝 등 이미지 OCR 파이프라인
- `sw.js` / `manifest.json` — PWA 서비스 워커 및 매니페스트 (캐시 버전 관리 주의)
- `tools/` — TTS 생성 및 테스트 유틸리티

## 3. 작업 시 기본 규칙
1. 수정 후 배포 확인은 `main` 푸시 → https://minusindot.github.io/GeminiFit/ (필요 시 캐시/강력 새로고침 및 `sw.js` 버전 확인).
2. `state.json`은 앱에서 자동 동기화되는 사용자 실데이터이므로, 코드 수정 시 사용자 데이터를 덮어쓰지 않도록 주의 (`git pull --rebase` 습관화).
3. 버전 업 시 커밋 메시지에 `v4.x.xx: 요약` 형식을 유지.
