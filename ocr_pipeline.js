/* ==========================================================================
   GeminiFit - 체성분 / 러닝 스캔 파이프라인 (v4.3.53)
   --------------------------------------------------------------------------
   index.html 안에 흩어져 있던 판독 로직을 밖으로 꺼낸 이유:
     1) node에서 그대로 테스트할 수 있게 (tools/test_ocr_pipeline.js)
     2) "못 읽은 값"과 "읽은 값"을 코드 레벨에서 구분하기 위해
   설계 원칙:
     - 판독기는 값을 '추측'하지 않는다. 확신 없으면 null.
     - 저장 전에 범위/정합성/직전값 대비 검사를 통과해야 한다.
     - 두 엔진(Gemini Vision / Tesseract) 결과가 다르면 조용히 하나를 고르지 않고 경고한다.
   ========================================================================== */
(function (root) {
  'use strict';

  const PIPELINE_VERSION = '4.4.0';

  // ------------------------------------------------------------------------
  // 1. Gemini Vision 프롬프트
  //    - responseMimeType: application/json 과 함께 쓴다.
  //    - InBody270 / 370 / 570 / 770 한국어 표준 결과지 레이아웃을 정확히 반영한다.
  //    - 하단 "신체변화(Body Composition History)" 과거 그래프 숫자는 절대 읽지 않는다.
  // ------------------------------------------------------------------------
  const GEMINI_PROMPT = [
    '당신은 인바디(InBody270/370/570/770) 결과지 / 삼성헬스 / 나이키런 / 애플피트니스 / 가민 화면을 읽는 정밀 데이터 추출기입니다.',
    '이미지에 실제로 보이는 오늘의 측정 숫자만 JSON으로 옮기세요.',
    '',
    '[절대 규칙]',
    '1. 보이지 않거나 확실하지 않은 값은 예외 없이 null 입니다. 추측, 평균, 기본값 채우기는 금지입니다.',
    '2. 괄호 안의 정상 범위(예: 48.5~65.6, 32.0~39.2)와 단위 표시(kg, %, kcal, 점)는 값이 아닙니다. 절대 읽지 마세요.',
    '3. 체중(kg) / 골격근량(kg) / 체지방량(kg) / 체지방률(%) 은 서로 다른 항목입니다. 절대 섞지 마세요.',
    '   - 체지방률(fat)은 반드시 "비만분석 > 체지방률 (%)" 항목이며, 체지방량(bodyFatMass)은 "체지방량 (kg)" 항목입니다.',
    '4. 인바디 결과지 맨 아래 "신체변화 (Body Composition History)" 꺾은선 그래프에는 과거 날짜 기록이 여러 개 적혀 있습니다.',
    '   과거 그래프 숫자는 절대 읽지 말고, 반드시 상단~중단의 오늘 측정 표에서만 읽으세요.',
    '5. 측정일시(검사일시)가 인쇄돼 있으면 YYYY-MM-DD 형식으로 measuredAt에 적으세요. 없으면 null.',
    '6. 출력은 JSON 객체 하나만. 코드펜스, 설명, 주석 모두 금지.',
    '',
    '[한국어 인바디(InBody270 등) 정확한 영역 위치]',
    '- 상단 좌측 [체성분분석 표]: 체수분(L), 단백질(kg), 무기질(kg), 체지방량(kg), 체중(kg) — 각 행 괄호 왼쪽의 첫 번째 숫자.',
    '- 중단 좌측 [골격근·지방분석 막대]: 체중(kg), 골격근량(kg), 체지방량(kg) — 각 막대 끝에 적힌 굵은 숫자.',
    '- 중단 좌측 [비만분석 막대]: BMI(kg/m²), 체지방률(%) — 각 막대 끝에 적힌 굵은 숫자.',
    '- 상단 우측 [인바디점수]: 큰 숫자 / 100 점 (예: 64 / 100 점 -> inbodyScore: 64).',
    '- 중단 우측 [내장지방레벨] & [연구항목]: 내장지방레벨(정수), 제지방량(kg), 기초대사량(kcal).',
    '- 삼성헬스 체중 화면: "체중" 또는 "몸무게" 아래 kg 값, "체지방" 아래 %.',
    '- 러닝 화면: 거리(km), 시간(mm:ss 또는 hh:mm:ss), 평균 페이스, 칼로리, 평균 심박수, 케이던스, 걸음수.',
    '',
    '[출력 스키마]',
    '{',
    '  "kind": "inbody" | "running" | "weight" | "unknown",',
    '  "source": "인바디" | "삼성헬스" | "나이키런" | "애플피트니스" | "가민" | "기타",',
    '  "measuredAt": "YYYY-MM-DD" | null,',
    '  "weight": 숫자 | null,',
    '  "fat": 숫자 | null,',
    '  "inbodyScore": 정수 | null,',
    '  "skeletalMuscle": 숫자 | null,',
    '  "bodyFatMass": 숫자 | null,',
    '  "bmr": 정수 | null,',
    '  "visceralFatLevel": 정수 | null,',
    '  "bmi": 숫자 | null,',
    '  "bodyWater": 숫자 | null,',
    '  "protein": 숫자 | null,',
    '  "mineral": 숫자 | null,',
    '  "distance": 숫자 | null,',
    '  "duration": "mm:ss" | null,',
    '  "pace": "mm\'ss\\"" | null,',
    '  "calories": 정수 | null,',
    '  "heartRate": 정수 | null,',
    '  "cadence": 정수 | null,',
    '  "steps": 정수 | null,',
    '  "confidence": { "weight": "high"|"medium"|"low" },',
    '  "notes": "판독이 애매했던 부분 한 줄"',
    '}'
  ].join('\n');

  const INBODY_FIELDS = ['weight', 'fat', 'inbodyScore', 'skeletalMuscle', 'bodyFatMass',
    'bmr', 'visceralFatLevel', 'bmi', 'bodyWater', 'protein', 'mineral'];
  const RUN_FIELDS = ['distance', 'calories', 'heartRate', 'cadence', 'steps'];
  const INT_FIELDS = ['inbodyScore', 'bmr', 'visceralFatLevel', 'calories', 'heartRate', 'cadence', 'steps'];

  const LABELS = {
    weight: '체중', fat: '체지방률', inbodyScore: '인바디 점수', skeletalMuscle: '골격근량',
    bodyFatMass: '체지방량', bmr: '기초대사량', visceralFatLevel: '내장지방', bmi: 'BMI',
    bodyWater: '체수분', protein: '단백질', mineral: '무기질',
    distance: '거리', duration: '시간', pace: '페이스', calories: '칼로리',
    heartRate: '평균 심박수', cadence: '케이던스', steps: '걸음수'
  };

  const UNITS = {
    weight: 'kg', fat: '%', inbodyScore: '점', skeletalMuscle: 'kg', bodyFatMass: 'kg',
    bmr: 'kcal', visceralFatLevel: '레벨', bmi: '', bodyWater: 'L', protein: 'kg', mineral: 'kg',
    distance: 'km', calories: 'kcal', heartRate: 'bpm', cadence: 'spm', steps: '걸음'
  };

  // 하드 범위 = 넘으면 그 필드는 저장 자체를 막는다. 소프트 범위 = 경고만.
  const RULES = {
    weight: { min: 30, max: 200, softMin: 40, softMax: 160, step: 0.1 },
    fat: { min: 3, max: 65, softMax: 60, step: 0.1 },
    inbodyScore: { min: 40, max: 100, step: 1 },
    skeletalMuscle: { min: 8, max: 60, softMax: 50, step: 0.1 },
    bodyFatMass: { min: 1, max: 90, step: 0.1 },
    bmr: { min: 700, max: 3500, softMin: 900, softMax: 2600, step: 1 },
    visceralFatLevel: { min: 1, max: 30, softMax: 20, step: 1 },
    bmi: { min: 10, max: 60, softMax: 45, step: 0.1 },
    bodyWater: { min: 10, max: 70, step: 0.1 },
    protein: { min: 3, max: 30, step: 0.1 },
    mineral: { min: 0.5, max: 10, step: 0.01 },
    distance: { min: 0.05, max: 100, softMax: 60, step: 0.01 },
    calories: { min: 20, max: 3000, softMax: 1800, step: 1 },
    heartRate: { min: 40, max: 220, softMin: 50, softMax: 200, step: 1 },
    cadence: { min: 50, max: 240, softMax: 200, step: 1 },
    steps: { min: 50, max: 90000, softMax: 60000, step: 1 }
  };

  // ------------------------------------------------------------------------
  // 2. 값 정규화
  // ------------------------------------------------------------------------
  function toNumber(v) {
    if (v === null || v === undefined) return null;
    if (typeof v === 'number') return Number.isFinite(v) ? v : null;
    if (typeof v === 'boolean') return null;
    let s = String(v).trim();
    if (!s || /^(null|none|n\/a|-|미감지|없음)$/i.test(s)) return null;
    // 단위/범위 표기를 먼저 걷어낸다. "48.5~65.6" 같은 범위는 값이 아니다.
    if (/[~～]/.test(s) && /\d\s*[~～]\s*\d/.test(s)) return null;
    s = s.replace(/[^\d.,-]/g, '').replace(/,(\d{1,2})$/, '.$1').replace(/,/g, '');
    const n = parseFloat(s);
    return Number.isFinite(n) ? n : null;
  }

  function round1(n) {
    return (n === null || n === undefined) ? null : Math.round(n * 10) / 10;
  }

  // 필드별 소수 자릿수. 거리(6.01km)를 1자리로 반올림하면 페이스 계산이 틀어진다.
  const DECIMALS = {
    distance: 2, bmi: 1, mineral: 2, bodyWater: 1, protein: 1,
    weight: 1, fat: 1, skeletalMuscle: 1, bodyFatMass: 1
  };

  function roundTo(n, digits) {
    if (n === null || n === undefined) return null;
    const p = Math.pow(10, digits);
    return Math.round(n * p) / p;
  }

  function normalizeFitnessScan(raw, engine) {
    const src = raw && typeof raw === 'object' ? raw : {};
    const out = {
      kind: 'unknown',
      engine: engine || 'unknown',
      source: src.source || '',
      measuredAt: null,
      confidence: {},
      notes: typeof src.notes === 'string' ? src.notes.slice(0, 200) : '',
      filledFrom: {}
    };

    const kind = String(src.kind || '').toLowerCase();
    if (kind === 'inbody' || kind === 'running' || kind === 'weight') out.kind = kind;

    if (typeof src.measuredAt === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(src.measuredAt)) {
      out.measuredAt = src.measuredAt;
    }

    for (const f of INBODY_FIELDS.concat(RUN_FIELDS)) {
      let v = toNumber(src[f]);
      if (v === null) { out[f] = null; continue; }
      if (INT_FIELDS.includes(f)) v = Math.round(v);
      else v = roundTo(v, DECIMALS[f] !== undefined ? DECIMALS[f] : 1);
      out[f] = v;
    }

    // duration / pace 는 문자열로 유지한다 (표시 형식이 중요).
    out.duration = (typeof src.duration === 'string' && parseDuration(src.duration) ? src.duration.trim() : null);
    out.pace = (typeof src.pace === 'string' && parsePace(src.pace) ? src.pace.trim() : null);

    const conf = (src.confidence && typeof src.confidence === 'object') ? src.confidence : {};
    for (const f of Object.keys(conf)) {
      const c = String(conf[f] || '').toLowerCase();
      if (c === 'high' || c === 'medium' || c === 'low') out.confidence[f] = c;
    }

    // kind 추론
    if (out.kind === 'unknown') {
      const hasBody = INBODY_FIELDS.some(f => out[f] !== null);
      const hasRun = out.distance !== null || out.duration !== null;
      if (hasRun && !hasBody) out.kind = 'running';
      else if (hasBody) out.kind = (out.inbodyScore !== null || out.skeletalMuscle !== null || out.bodyFatMass !== null) ? 'inbody' : 'weight';
    }
    return out;
  }

  // ------------------------------------------------------------------------
  // 3. 시간 / 페이스
  // ------------------------------------------------------------------------
  function parseDuration(str) {
    if (str === null || str === undefined) return null;
    const s = String(str).trim().replace(/[^\d:]/g, '');
    if (!s) return null;
    const parts = s.split(':').filter(p => p !== '');
    if (!parts.length || parts.length > 3) return null;
    let sec = 0;
    for (const p of parts) {
      const n = parseInt(p, 10);
      if (!Number.isFinite(n)) return null;
      sec = sec * 60 + n;
    }
    return sec > 0 ? sec : null;
  }

  function formatDuration(sec) {
    if (!Number.isFinite(sec) || sec <= 0) return null;
    const s = Math.round(sec);
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const ss = s % 60;
    const pad = (n) => String(n).padStart(2, '0');
    return h > 0 ? `${h}:${pad(m)}:${pad(ss)}` : `${pad(m)}:${pad(ss)}`;
  }

  // "09'17\"" / "9:17" / "9분17초" -> 초/킬로
  function parsePace(str) {
    if (str === null || str === undefined) return null;
    const m = String(str).match(/(\d{1,2})\s*[':분]\s*(\d{1,2})/);
    if (!m) return null;
    const sec = parseInt(m[1], 10) * 60 + parseInt(m[2], 10);
    return sec > 0 ? sec : null;
  }

  function formatPace(secPerKm) {
    if (!Number.isFinite(secPerKm) || secPerKm <= 0) return null;
    const s = Math.round(secPerKm);
    const m = Math.floor(s / 60);
    const ss = s % 60;
    return `${String(m).padStart(2, '0')}'${String(ss).padStart(2, '0')}"`;
  }

  function paceFromDistanceDuration(distance, durationStr) {
    const d = toNumber(distance);
    const sec = parseDuration(durationStr);
    if (!d || d <= 0 || !sec) return null;
    return sec / d;
  }

  // ------------------------------------------------------------------------
  // 4. 검증
  //    반환: { parsed, warnings, blocked, ok }
  //      blocked  = 하드 범위를 벗어나 null로 되돌린 필드 목록
  //      warnings = { level:'error'|'warn'|'info', field, msg }
  // ------------------------------------------------------------------------
  function validateFitnessScan(scan, ctx) {
    const c = ctx || {};
    const parsed = Object.assign({}, scan);
    const warnings = [];
    const blocked = [];
    const add = (level, field, msg) => warnings.push({ level, field, msg });

    const check = (f) => {
      const v = parsed[f];
      if (v === null || v === undefined) return;
      const r = RULES[f];
      if (!r) return;
      const label = LABELS[f] || f;
      if (v < r.min || v > r.max) {
        add('error', f, `${label} ${v}${UNITS[f] || ''} 는 판독 오류로 보입니다 (허용 ${r.min}~${r.max}). 저장하지 않습니다.`);
        parsed[f] = null;
        blocked.push(f);
        return;
      }
      if ((r.softMin !== undefined && v < r.softMin) || (r.softMax !== undefined && v > r.softMax)) {
        add('warn', f, `${label} ${v}${UNITS[f] || ''} 는 일반 범위를 벗어납니다. 원본과 대조해 주세요.`);
      }
      const conf = (parsed.confidence || {})[f];
      if (conf === 'low') add('warn', f, `${label} 판독 신뢰도가 낮습니다 (${v}). 직접 확인이 필요합니다.`);
    };

    INBODY_FIELDS.concat(RUN_FIELDS).forEach(check);

    // --- 직전 실제 값 대비 급변 검사
    if (parsed.weight !== null && typeof c.prevWeight === 'number' && c.prevWeightIsReal) {
      const d = Math.round((parsed.weight - c.prevWeight) * 10) / 10;
      if (Math.abs(d) >= 2.5) {
        add('warn', 'weight', `직전 ${c.prevWeight}kg 대비 ${d > 0 ? '+' : ''}${d}kg 차이입니다. 다른 사람 결과지이거나 단위 오류일 수 있습니다.`);
      }
    }
    if (parsed.fat !== null && typeof c.prevFat === 'number' && c.prevFatIsReal) {
      const d = Math.round((parsed.fat - c.prevFat) * 10) / 10;
      if (Math.abs(d) >= 5) {
        add('warn', 'fat', `직전 ${c.prevFat}% 대비 ${d > 0 ? '+' : ''}${d}%p 차이입니다. 확인해 주세요.`);
      }
    }

    // --- 체성분 정합성: 체지방량 ~= 체중 x 체지방률
    //     체지방률(%)을 못 읽었지만 체중과 체지방량(kg)을 둘 다 읽었으면 자동 계산해 채운다.
    if (parsed.weight !== null && parsed.weight > 0 && parsed.bodyFatMass !== null) {
      if (parsed.fat === null) {
        const computedFat = round1((parsed.bodyFatMass / parsed.weight) * 100);
        if (computedFat >= RULES.fat.min && computedFat <= RULES.fat.max) {
          parsed.fat = computedFat;
          parsed.filledFrom = Object.assign({}, parsed.filledFrom, { fat: 'computed' });
          add('info', 'fat', `체지방률을 직접 읽지 못해 체지방량÷체중으로 계산했습니다 (${computedFat}%).`);
        }
      } else {
        const expected = parsed.weight * parsed.fat / 100;
        const diff = Math.abs(parsed.bodyFatMass - expected);
        if (diff > Math.max(1.5, parsed.weight * 0.05)) {
          add('warn', 'bodyFatMass', `체지방량 ${parsed.bodyFatMass}kg 은 체중×체지방률 계산값 ${round1(expected)}kg 과 차이가 큽니다.`);
        }
      }
    }
    // --- 골격근량 + 체지방량 > 체중 이면 판독 오류
    if (parsed.weight !== null && parsed.skeletalMuscle !== null && parsed.bodyFatMass !== null) {
      if (parsed.skeletalMuscle + parsed.bodyFatMass > parsed.weight * 1.05) {
        add('warn', 'skeletalMuscle', `골격근량 + 체지방량이 체중보다 큽니다. 항목이 뒤바뀌었을 수 있습니다.`);
      }
    }
    // --- BMI 정합성 (키를 모르므로 2차 확인용): BMI 18~35 구간에서 체중/BMI 로 키를 역산해 상식선인지
    if (parsed.weight !== null && parsed.bmi !== null && parsed.bmi > 0) {
      const heightM = Math.sqrt(parsed.weight / parsed.bmi);
      if (heightM < 1.2 || heightM > 2.1) {
        add('warn', 'bmi', `체중 ${parsed.weight}kg / BMI ${parsed.bmi} 조합이 비현실적입니다 (역산 키 ${(heightM * 100).toFixed(0)}cm).`);
      }
    }

    // --- 러닝 정합성: 페이스 = 시간 / 거리
    if (parsed.distance !== null && parsed.duration) {
      const computed = paceFromDistanceDuration(parsed.distance, parsed.duration);
      if (computed) {
        const parsedPaceSec = parsePace(parsed.pace);
        if (parsedPaceSec === null) {
          parsed.pace = formatPace(computed);
          parsed.filledFrom.pace = 'computed';
          add('info', 'pace', `페이스를 읽지 못해 시간÷거리로 계산했습니다 (${parsed.pace}).`);
        } else if (Math.abs(parsedPaceSec - computed) > 25) {
          add('warn', 'pace', `표시된 페이스 ${parsed.pace} 와 시간÷거리 계산값 ${formatPace(computed)} 이 다릅니다.`);
        }
      }
    } else if (parsed.distance !== null && parsed.pace && !parsed.duration) {
      const p = parsePace(parsed.pace);
      if (p) {
        parsed.duration = formatDuration(p * parsed.distance);
        parsed.filledFrom.duration = 'computed';
        add('info', 'duration', `시간을 읽지 못해 거리×페이스로 계산했습니다 (${parsed.duration}).`);
      }
    }

    // --- 아무것도 못 읽음
    const core = parsed.kind === 'running'
      ? [parsed.distance, parsed.duration]
      : [parsed.weight, parsed.fat, parsed.inbodyScore, parsed.skeletalMuscle];
    if (core.every(v => v === null || v === undefined)) {
      add('error', 'all', '핵심 수치를 하나도 읽지 못했습니다. 직접 입력해 주세요.');
    }

    return {
      parsed,
      warnings,
      blocked,
      ok: !warnings.some(w => w.level === 'error'),
      hasWarn: warnings.some(w => w.level === 'warn')
    };
  }

  // ------------------------------------------------------------------------
  // 5. 두 엔진 교차검증
  //    primary(Gemini)가 비운 칸을 secondary(Tesseract)가 채우고,
  //    둘 다 값이 있는데 다르면 경고를 남긴다. (조용히 하나를 고르지 않는다)
  // ------------------------------------------------------------------------
  const CROSS_TOLERANCE = {
    weight: 0.4, fat: 0.6, inbodyScore: 1, skeletalMuscle: 0.4, bodyFatMass: 0.6,
    bmr: 30, visceralFatLevel: 1, bmi: 0.4,
    distance: 0.15, calories: 25, heartRate: 4, cadence: 6, steps: 150
  };

  function mergeScanResults(primary, secondary) {
    const merged = Object.assign({}, primary, { warnings: [], filledFrom: Object.assign({}, primary.filledFrom || {}) });
    if (!secondary) return merged;

    for (const f of INBODY_FIELDS.concat(RUN_FIELDS)) {
      const a = primary[f];
      const b = secondary[f];
      const tol = CROSS_TOLERANCE[f] !== undefined ? CROSS_TOLERANCE[f] : 0.5;
      if ((a === null || a === undefined) && b !== null && b !== undefined) {
        merged[f] = b;
        merged.filledFrom[f] = 'tesseract';
        merged.warnings.push({ level: 'info', field: f, msg: `${LABELS[f] || f} 은 AI가 놓쳐서 로컬 OCR 값(${b})으로 채웠습니다.` });
      } else if (a !== null && a !== undefined && b !== null && b !== undefined && Math.abs(a - b) > tol) {
        merged.warnings.push({ level: 'warn', field: f, msg: `AI ${a} vs 로컬 OCR ${b} 불일치 (${LABELS[f] || f}). 무엇이 맞는지 확인해 주세요.` });
      }
    }
    return merged;
  }

  // ------------------------------------------------------------------------
  // 6. 표시용 요약 / 복사용 리포트
  // ------------------------------------------------------------------------
  function summarizeScan(scan) {
    const parts = [];
    if (scan.weight !== null && scan.weight !== undefined) parts.push(`체중 ${scan.weight}kg`);
    if (scan.fat !== null && scan.fat !== undefined) parts.push(`체지방 ${scan.fat}%`);
    if (scan.inbodyScore !== null && scan.inbodyScore !== undefined) parts.push(`점수 ${scan.inbodyScore}점`);
    if (scan.skeletalMuscle !== null && scan.skeletalMuscle !== undefined) parts.push(`골격근 ${scan.skeletalMuscle}kg`);
    if (scan.distance !== null && scan.distance !== undefined) parts.push(`${scan.distance}km`);
    if (scan.duration) parts.push(scan.duration);
    return parts.length ? parts.join(' · ') : '읽은 값 없음';
  }

  function buildScanReport(meta) {
    const m = meta || {};
    const s = m.parsed || {};
    const lines = [];
    lines.push(`[GeminiFit 스캔 리포트] ${m.at || ''}`.trim());
    lines.push(`엔진: ${s.engine || '?'}${m.enginesTried ? ' (' + m.enginesTried.join(' -> ') + ')' : ''}`);
    lines.push(`분류: ${s.kind || 'unknown'}  소스: ${s.source || '-'}`);
    lines.push('');
    lines.push('[읽은 값]');
    const rows = INBODY_FIELDS.concat(['duration', 'pace'], RUN_FIELDS);
    let any = false;
    for (const f of rows) {
      const v = s[f];
      if (v === null || v === undefined) continue;
      any = true;
      const conf = (s.confidence || {})[f];
      const from = (s.filledFrom || {})[f];
      lines.push(`- ${LABELS[f] || f}: ${v}${UNITS[f] || ''}${conf ? ' [' + conf + ']' : ''}${from ? ' <' + from + '>' : ''}`);
    }
    if (!any) lines.push('- (없음)');
    lines.push('');
    const nulls = INBODY_FIELDS.concat(RUN_FIELDS).filter(f => s[f] === null || s[f] === undefined);
    if (nulls.length) lines.push(`[미감지] ${nulls.map(f => LABELS[f] || f).join(', ')}`);
    if ((m.warnings || []).length) {
      lines.push('');
      lines.push('[경고]');
      for (const w of m.warnings) lines.push(`- (${w.level}) ${w.msg}`);
    }
    if (m.rawText) {
      lines.push('');
      lines.push('[원문]');
      lines.push(String(m.rawText).slice(0, 1200));
    }
    return lines.join('\n');
  }

  const SLEEP_GEMINI_PROMPT = [
    '당신은 삼성헬스(Samsung Health) / 애플건강 / 가민 수면 화면 스크린샷을 읽는 정밀 데이터 추출기입니다.',
    '화면에 실제로 보이는 수면 기록 숫자만 JSON으로 옮기세요.',
    '',
    '[규칙]',
    '1. 보이지 않거나 확실하지 않은 값은 null 입니다. 추측 금지.',
    '2. 취침 시각(bedtime)과 기상 시각(wakeup)은 반드시 24시간제 "HH:mm" 문자열로 변환하세요.',
    '   - 예: "오전 1:15" -> "01:15", "오후 11:40" -> "23:40", "오전 12:20" -> "00:20", "오후 12:10" -> "12:10".',
    '3. 총 수면 시간(durationMin)은 분 단위 정수입니다. (예: "6시간 24분" -> 384).',
    '4. 날짜(date)가 보이면 "YYYY-MM-DD" 형식으로 적으세요. 연도가 생략된 "11월 21일" 등은 null 대신 월-일만 쓰지 말고 오늘 연도를 추정하지 말아 null로 두어도 됩니다.',
    '5. 출력은 JSON 객체 하나만. 코드펜스·설명 금지.',
    '',
    '[출력 스키마]',
    '{',
    '  "source": "삼성헬스" | "애플건강" | "기타",',
    '  "date": "YYYY-MM-DD" | null,',
    '  "bedtime": "HH:mm" | null,',
    '  "wakeup": "HH:mm" | null,',
    '  "durationMin": 정수 | null,',
    '  "score": 정수 | null,',
    '  "deepMin": 정수 | null,',
    '  "remMin": 정수 | null,',
    '  "notes": "한 줄 메모 또는 null"',
    '}'
  ].join('\n');

  function normalizeTimeHHMM(val) {
    if (val === null || val === undefined) return null;
    const s = String(val).trim();
    if (!s) return null;
    const ampm = s.match(/(오전|오후|AM|PM)\s*(\d{1,2})\s*[:시]\s*(\d{1,2})/i);
    if (ampm) {
      let h = parseInt(ampm[2], 10);
      const m = parseInt(ampm[3], 10);
      const tag = ampm[1].toUpperCase();
      if ((tag === '오후' || tag === 'PM') && h < 12) h += 12;
      if ((tag === '오전' || tag === 'AM') && h === 12) h = 0;
      if (h >= 0 && h <= 23 && m >= 0 && m <= 59) {
        return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
      }
    }
    const hm = s.match(/(\d{1,2})\s*[:시]\s*(\d{1,2})/);
    if (hm) {
      const h = parseInt(hm[1], 10);
      const m = parseInt(hm[2], 10);
      if (h >= 0 && h <= 23 && m >= 0 && m <= 59) {
        return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
      }
    }
    return null;
  }

  function calcSleepDurationMin(bedtime, wakeup) {
    if (!bedtime || !wakeup) return null;
    const [bh, bm] = bedtime.split(':').map(Number);
    const [wh, wm] = wakeup.split(':').map(Number);
    if ([bh, bm, wh, wm].some(n => !Number.isFinite(n))) return null;
    let diff = (wh * 60 + wm) - (bh * 60 + bm);
    if (diff <= 0) diff += 24 * 60;
    return (diff >= 30 && diff <= 18 * 60) ? diff : null;
  }

  function formatSleepDuration(min) {
    if (!Number.isFinite(min) || min <= 0) return '-';
    const h = Math.floor(min / 60);
    const m = Math.round(min % 60);
    return h > 0 ? (m > 0 ? `${h}시간 ${m}분` : `${h}시간`) : `${m}분`;
  }

  function normalizeSleepScan(raw) {
    const r = raw || {};
    const bedtime = normalizeTimeHHMM(r.bedtime);
    const wakeup = normalizeTimeHHMM(r.wakeup);
    let durationMin = toNumber(r.durationMin);
    if (durationMin !== null) durationMin = Math.round(durationMin);
    if (durationMin === null || durationMin < 30 || durationMin > 18 * 60) {
      durationMin = calcSleepDurationMin(bedtime, wakeup);
    }
    let score = toNumber(r.score);
    if (score !== null) {
      score = Math.round(score);
      if (score < 1 || score > 100) score = null;
    }
    const deepMin = toNumber(r.deepMin);
    const remMin = toNumber(r.remMin);
    const dateStr = (typeof r.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(r.date.trim())) ? r.date.trim() : null;
    return {
      source: r.source || '삼성헬스',
      date: dateStr,
      bedtime,
      wakeup,
      durationMin,
      durationText: formatSleepDuration(durationMin),
      score,
      deepMin: deepMin !== null && deepMin >= 0 && deepMin <= 600 ? Math.round(deepMin) : null,
      remMin: remMin !== null && remMin >= 0 && remMin <= 600 ? Math.round(remMin) : null,
      notes: r.notes || null
    };
  }

  function parseSleepTextFallback(text) {
    const s = String(text || '');
    let durationMin = null;
    const durMatch = s.match(/(\d{1,2})\s*시간\s*(\d{1,2})?\s*분?/);
    if (durMatch) {
      const h = parseInt(durMatch[1], 10);
      const m = durMatch[2] ? parseInt(durMatch[2], 10) : 0;
      if (h >= 0 && h <= 18 && m >= 0 && m <= 59) durationMin = h * 60 + m;
    }
    const timeMatches = [];
    const re = /(?:(오전|오후|AM|PM)\s*)?(\d{1,2})\s*:\s*(\d{2})/gi;
    let m;
    while ((m = re.exec(s)) !== null) {
      const t = normalizeTimeHHMM(m[0]);
      if (t) timeMatches.push(t);
    }
    let bedtime = null, wakeup = null;
    if (timeMatches.length >= 2) {
      bedtime = timeMatches[0];
      wakeup = timeMatches[1];
    }
    let score = null;
    const scoreMatch = s.match(/수면\s*점수[^\d]{0,12}(\d{2,3})|(\d{2,3})\s*점/);
    if (scoreMatch) {
      const v = parseInt(scoreMatch[1] || scoreMatch[2], 10);
      if (v >= 20 && v <= 100) score = v;
    }
    return normalizeSleepScan({ source: '삼성헬스(OCR)', bedtime, wakeup, durationMin, score });
  }

  const API = {
    PIPELINE_VERSION,
    GEMINI_PROMPT,
    SLEEP_GEMINI_PROMPT,
    INBODY_FIELDS,
    RUN_FIELDS,
    LABELS,
    UNITS,
    RULES,
    CROSS_TOLERANCE,
    toNumber,
    normalizeFitnessScan,
    validateFitnessScan,
    mergeScanResults,
    normalizeTimeHHMM,
    calcSleepDurationMin,
    formatSleepDuration,
    normalizeSleepScan,
    parseSleepTextFallback,
    parseDuration,
    formatDuration,
    parsePace,
    formatPace,
    paceFromDistanceDuration,
    summarizeScan,
    buildScanReport
  };

  root.OcrPipeline = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof globalThis !== 'undefined' ? globalThis : this);
