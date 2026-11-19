#!/usr/bin/env node
/* ==========================================================================
   ocr_pipeline.js 자체 점검 (v4.3.53)

   실행:  node tools/test_ocr_pipeline.js
          node tools/test_ocr_pipeline.js <gemini-response.json>
            -> 실제 Gemini 응답을 저장해 두면 같은 검증기를 통과시켜 볼 수 있다.

   목적: 스크린샷을 다시 찍지 않아도 "읽기/검증" 로직의 회귀를 잡는다.
   ========================================================================== */
'use strict';

const fs = require('fs');
const path = require('path');

const pipelinePath = path.join(__dirname, '..', 'ocr_pipeline.js');
const P = require(pipelinePath);

let pass = 0;
let fail = 0;
const failures = [];

function ok(cond, name, detail) {
  if (cond) { pass++; return; }
  fail++;
  failures.push(name + (detail ? '\n      ' + detail : ''));
}

function eq(actual, expected, name) {
  ok(actual === expected, name, `기대 ${JSON.stringify(expected)} / 실제 ${JSON.stringify(actual)}`);
}

function near(actual, expected, tol, name) {
  const d = Math.abs(actual - expected);
  ok(d <= tol, name, `기대 ${expected}±${tol} / 실제 ${actual}`);
}

function hasWarning(res, field, level) {
  return res.warnings.some(w => w.field === field && (!level || w.level === level));
}

/* ------------------------------------------------------------------ */
/* 1. 프롬프트가 "모르면 null"을 강제하는가                            */
/* ------------------------------------------------------------------ */
(function promptTests() {
  const p = P.GEMINI_PROMPT;
  ok(/null/.test(p), '프롬프트: null 규칙 포함');
  ok(/정상 범위/.test(p) && /읽지 마세요/.test(p), '프롬프트: 범위값(48.5~65.6) 배제 규칙 포함');
  ok(/체지방량/.test(p) && /체지방률/.test(p), '프롬프트: 체지방량/체지방률 구분 규칙 포함');
  ok(/JSON 객체 하나만/.test(p), '프롬프트: JSON only 규칙 포함');
  ok(/"inbodyScore"/.test(p) && /"skeletalMuscle"/.test(p) && /"bmr"/.test(p),
    '프롬프트: 인바디 확장 필드(점수/골격근/기초대사량) 포함');
  ok(/"confidence"/.test(p), '프롬프트: confidence 필드 포함');
})();

/* ------------------------------------------------------------------ */
/* 2. 값 정규화 — 범위 표기/단위/쓰레기 제거                            */
/* ------------------------------------------------------------------ */
(function normalizeTests() {
  eq(P.toNumber('48.5~65.6'), null, '정규화: 범위 문자열은 값이 아니다');
  eq(P.toNumber('66.4 kg'), 66.4, '정규화: 단위 제거');
  eq(P.toNumber('66,4'), 66.4, '정규화: 콤마 소수점');
  eq(P.toNumber(''), null, '정규화: 빈 문자열');
  eq(P.toNumber(null), null, '정규화: null');
  eq(P.toNumber('미감지'), null, '정규화: 미감지 문자열');

  const s = P.normalizeFitnessScan({
    kind: 'inbody',
    weight: '66.4',
    fat: 31.8,
    inbodyScore: '71',
    bodyFatMass: '21.1',
    bmr: '1,397',
    confidence: { weight: 'high', fat: 'medium', bmr: 'LOW' }
  }, 'gemini');
  eq(s.weight, 66.4, '정규화: 체중 숫자 변환');
  eq(s.inbodyScore, 71, '정규화: 점수 정수 변환');
  eq(s.bmr, 1397, '정규화: 천단위 콤마 제거');
  eq(s.confidence.bmr, 'low', '정규화: confidence 소문자화');
  eq(s.engine, 'gemini', '정규화: 엔진 기록');
})();

/* ------------------------------------------------------------------ */
/* 3. 실제 결과지 (2026-11-18 인바디 270) — 아는 값만 통과해야 한다     */
/* ------------------------------------------------------------------ */
(function realSheetTests() {
  const scan = P.normalizeFitnessScan({
    kind: 'inbody',
    source: '인바디',
    measuredAt: '2026-11-18',
    weight: 66.4,
    fat: 31.8,
    inbodyScore: null,
    skeletalMuscle: null,
    bodyFatMass: null,
    bmr: null,
    confidence: { weight: 'high', fat: 'high' }
  }, 'gemini');

  const res = P.validateFitnessScan(scan, { prevWeight: 65.6, prevWeightIsReal: true, prevFat: null, prevFatIsReal: false });
  eq(res.ok, true, '실측: 66.4kg / 31.8% 는 오류 없이 통과');
  eq(res.blocked.length, 0, '실측: 차단된 필드 없음');
  eq(res.parsed.weight, 66.4, '실측: 체중 보존');
  eq(res.parsed.inbodyScore, null, '실측: 점수는 null 유지 (63 기본값 주입 금지)');
  eq(res.parsed.skeletalMuscle, null, '실측: 골격근량은 null 유지 (24.8 기본값 주입 금지)');
  ok(!hasWarning(res, 'weight', 'warn'), '실측: 65.6 -> 66.4 (+0.8kg) 는 급변 경고 아님');

  // 체지방량 정합성: 66.4 * 31.8% = 21.1
  const withMass = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, fat: 31.8, bodyFatMass: 21.1 }, 'gemini');
  const resMass = P.validateFitnessScan(withMass, {});
  ok(!hasWarning(resMass, 'bodyFatMass', 'warn'), '정합성: 체지방량 21.1kg 은 체중x체지방률과 일치');

  const badMass = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, fat: 31.8, bodyFatMass: 31.8 }, 'gemini');
  ok(hasWarning(P.validateFitnessScan(badMass, {}), 'bodyFatMass', 'warn'),
    '정합성: 체지방률(31.8)을 체지방량 칸에 넣으면 경고');
})();

/* ------------------------------------------------------------------ */
/* 4. 판독 실패는 조용히 기본값이 되지 않는다                          */
/* ------------------------------------------------------------------ */
(function noFakeDefaultTests() {
  const empty = P.normalizeFitnessScan({ kind: 'unknown' }, 'tesseract');
  const res = P.validateFitnessScan(empty, {});
  eq(res.ok, false, '실패: 아무것도 못 읽으면 error');
  ok(res.warnings.some(w => w.field === 'all'), '실패: "핵심 수치 미감지" 안내');
  eq(res.parsed.weight, null, '실패: 체중 null 유지');
})();

/* ------------------------------------------------------------------ */
/* 5. 하드 범위 초과는 차단 (소수점 누락 664kg 같은 사고)               */
/* ------------------------------------------------------------------ */
(function rangeTests() {
  const s = P.normalizeFitnessScan({ kind: 'weight', weight: 664, fat: 88 }, 'tesseract');
  const res = P.validateFitnessScan(s, {});
  eq(res.parsed.weight, null, '범위: 664kg 는 차단');
  eq(res.parsed.fat, null, '범위: 88% 는 차단');
  ok(res.blocked.includes('weight') && res.blocked.includes('fat'), '범위: 차단 필드 기록');

  const normal = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, fat: 31.8, inbodyScore: 63 }, 'gemini');
  ok(P.validateFitnessScan(normal, {}).ok, '범위: 63점은 정상 범위');
})();

/* ------------------------------------------------------------------ */
/* 6. 직전값 대비 급변 / BMI 역산                                      */
/* ------------------------------------------------------------------ */
(function deltaTests() {
  const s = P.normalizeFitnessScan({ kind: 'weight', weight: 66.4 }, 'gemini');
  ok(hasWarning(P.validateFitnessScan(s, { prevWeight: 55.0, prevWeightIsReal: true }), 'weight', 'warn'),
    '급변: -11.4kg 는 경고');
  ok(!hasWarning(P.validateFitnessScan(s, { prevWeight: 55.0, prevWeightIsReal: false }), 'weight', 'warn'),
    '급변: 직전값이 샘플이면 경고하지 않음');

  const bmi = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, bmi: 50 }, 'gemini');
  ok(hasWarning(P.validateFitnessScan(bmi, {}), 'bmi', 'warn'), 'BMI: 체중/BMI 조합이 비현실적이면 경고');

  const okBmi = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, bmi: 25.8 }, 'gemini');
  ok(!hasWarning(P.validateFitnessScan(okBmi, {}), 'bmi', 'warn'), 'BMI: 66.4kg / 25.8 은 통과');
})();

/* ------------------------------------------------------------------ */
/* 7. 러닝: 시간/거리/페이스 3각 검증                                   */
/* ------------------------------------------------------------------ */
(function runTests() {
  eq(P.parseDuration('55:32'), 3332, '러닝: 55:32 -> 초');
  eq(P.parseDuration('1:02:33'), 3753, '러닝: hh:mm:ss -> 초');
  eq(P.parsePace('09\'13"'), 553, '러닝: 페이스 문자열 파싱');

  const computed = P.paceFromDistanceDuration(6.01, '55:32');
  near(computed, 554.4, 1, '러닝: 6.01km / 55:32 -> 554초/km');
  eq(P.formatPace(computed), '09\'14"', '러닝: 계산 페이스 표기');

  const good = P.normalizeFitnessScan({ kind: 'running', distance: 6.01, duration: '55:32', pace: '09\'13"' }, 'gemini');
  ok(!hasWarning(P.validateFitnessScan(good, {}), 'pace', 'warn'), '러닝: 표시 페이스와 계산 페이스 일치');

  const bad = P.normalizeFitnessScan({ kind: 'running', distance: 6.01, duration: '55:32', pace: '07\'00"' }, 'gemini');
  ok(hasWarning(P.validateFitnessScan(bad, {}), 'pace', 'warn'), '러닝: 페이스가 계산값과 다르면 경고');

  const noPace = P.normalizeFitnessScan({ kind: 'running', distance: 6.01, duration: '55:32' }, 'gemini');
  const resNoPace = P.validateFitnessScan(noPace, {});
  eq(resNoPace.parsed.pace, '09\'14"', '러닝: 페이스 미감지시 계산해서 채움');
  ok(hasWarning(resNoPace, 'pace', 'info'), '러닝: 계산으로 채웠다고 알려줌');
})();

/* ------------------------------------------------------------------ */
/* 8. 교차검증: 빈 칸은 채우고, 충돌은 경고                             */
/* ------------------------------------------------------------------ */
(function crossCheckTests() {
  const gem = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, fat: null }, 'gemini');
  const tes = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, fat: 31.8 }, 'tesseract');

  const merged = P.mergeScanResults(gem, tes);
  eq(merged.fat, 31.8, '교차: AI가 놓친 체지방률을 로컬 OCR로 채움');
  eq(merged.filledFrom.fat, 'tesseract', '교차: 채운 출처 기록');
  ok(!merged.warnings.some(w => w.level === 'warn'), '교차: 체중 일치시 경고 없음');

  const conflict = P.mergeScanResults(
    P.normalizeFitnessScan({ kind: 'weight', weight: 66.4 }, 'gemini'),
    P.normalizeFitnessScan({ kind: 'weight', weight: 64.1 }, 'tesseract')
  );
  ok(conflict.warnings.some(w => w.level === 'warn' && w.field === 'weight'),
    '교차: AI 66.4 vs OCR 64.1 불일치 경고');
})();

/* ------------------------------------------------------------------ */
/* 9. 리포트 / 요약                                                    */
/* ------------------------------------------------------------------ */
(function reportTests() {
  const s = P.normalizeFitnessScan({ kind: 'inbody', weight: 66.4, fat: 31.8, inbodyScore: 71 }, 'gemini');
  const res = P.validateFitnessScan(s, {});
  const rep = P.buildScanReport({ parsed: res.parsed, warnings: res.warnings, at: '2026-11-19', enginesTried: ['gemini'] });
  ok(/체중: 66\.4kg/.test(rep), '리포트: 체중 줄 포함');
  ok(/미감지/.test(rep), '리포트: 미감지 항목 표시');
  ok(P.summarizeScan(s).includes('66.4kg'), '요약: 체중 포함');
})();

/* ------------------------------------------------------------------ */
/* 10. (선택) 실제 Gemini 응답 파일 검증                               */
/* ------------------------------------------------------------------ */
const fileArg = process.argv[2];
if (fileArg) {
  const raw = JSON.parse(fs.readFileSync(fileArg, 'utf8'));
  const scan = P.normalizeFitnessScan(raw, 'gemini');
  const res = P.validateFitnessScan(scan, {});
  console.log('\n=== 실제 응답 검증: ' + fileArg + ' ===');
  console.log(P.buildScanReport({ parsed: res.parsed, warnings: res.warnings }));
  console.log('판정:', res.ok ? 'PASS' : 'FAIL');
  if (!res.ok) { fail++; failures.push('실제 응답 검증 실패'); }
}

/* ------------------------------------------------------------------ */
console.log(`\nocr_pipeline ${P.PIPELINE_VERSION} — ${pass} passed, ${fail} failed`);
if (fail) {
  console.log('\n실패 항목:');
  failures.forEach(f => console.log('  ✗ ' + f));
  process.exit(1);
}
console.log('모든 점검 통과');
