// Gemini Fit - Weekly Evaluation Report data (v4.3.33)
// 주간 리포트는 수요일(설정된 갱신 요일)마다 자동 생성되며,
// localStorage에 기록이 쌓여 지난 리포트를 다시 열람할 수 있습니다.
// 사용자 데이터(state)는 읽기만 하며 절대 수정하지 않습니다.

const WEEKLY_REPORT_STORAGE_KEY = 'geminifit_weekly_reports_v1';
const WEEKLY_REPORT_SEEN_KEY = 'geminifit_weekly_report_seen_v1';
const WEEKLY_REPORT_BASELINE_KEY = 'geminifit_weekly_report_baseline_v1';
const WEEKLY_REPORT_UPDATE_DAY = 3; // 0=Sun ... 3=Wed (fallback, state.updateSchedule 우선)

const WEEKLY_REPORT_SEEDS = [
  {
    id: '2026-11-11',
    publishedAt: '2026-11-11',
    periodStart: '2026-11-05',
    periodEnd: '2026-11-11',
    weekLabel: '11월 2주차',
    title: '백지 답안 주간 총평',
    score: 0,
    grade: '백지',
    hero: './image/03 gemini/gemini_48_zero_point_restart.png',
    heroPos: 'center 22%',
    quote: '0점이 아니라, 백지 답안이옵니다.',
    intro: '흥, 바보 프로듀서. 이번 주 답안지는 아무것도 쓰이지 않은 백지이옵니다. 하지만 백지는 실패가 아니라 아직 쓰이지 않은 여백이옵니다. 소녀가 다음 주 첫 획을 잡아드리겠사옵니다. 🍵',
    closing: '다음 수요일, 같은 자리에서 기다리겠사옵니다. 이번에는 백지가 아니라, 프로듀서님의 필체로 채워진 답안지를 보여주시와요. 🌸',
    areas: [
      {
        icon: '🏃', name: '운동 수행', score: 0, max: 30, tag: '러닝 · 근력 · 복근',
        comment: '지난 7km의 잔상은 남아있사옵니다. 그러나 이번 주 기록은 백지이옵니다. 러닝 0회, 근력 0회, 복근 0회.'
      },
      {
        icon: '🩹', name: '재활 · 케어', score: 0, max: 25, tag: '재활 0 / 4회',
        comment: '테니스 엘보를 지켜줄 4회의 케어가 통째로 비어있사옵니다. 아프기 전에 챙기는 것이 소녀의 방식이옵니다.'
      },
      {
        icon: '🍱', name: '식단 · 수분', score: 0, max: 25, tag: '3끼 0 / 21 · 차 0회',
        comment: '17:7 단식의 마지막 문장이 아직 쓰이지 않았사옵니다. 기록하지 않은 식사는 소녀도 채점할 수 없사옵니다.'
      },
      {
        icon: '🍵', name: '일본어 다실', score: 0, max: 20, tag: '0화 · 퀴즈 0 / 0',
        comment: '수업은 0화이옵니다. 그래도 65개의 言霊는 사라지지 않고 조용히 기다리고 있사옵니다.'
      }
    ],
    highlights: [
      { icon: '🔥', title: '스트릭 1일', text: '완벽하지 않아도 끊기지 않았사옵니다. 0일과 1일은 하늘과 땅만큼 다르옵니다.' },
      { icon: '🪶', title: '65 言霊', text: '지난 공부가 자산으로 남아있사옵니다. 백지 위에 바로 쓸 수 있는 잉크이옵니다.' },
      { icon: '📏', title: '64.1kg · 21.5%', text: '측정 자체를 미루지 않으셨사옵니다. 숫자를 마주하는 것이 첫 번째 운동이옵니다.' }
    ],
    missions: [
      { icon: '🏃', text: '러닝 3회 × 5km — 첫 회는 3km로 가볍게 시동' },
      { icon: '🩹', text: '재활 4회 — 2kg 덤벨 손목 편심성 컬 3세트' },
      { icon: '🧘', text: '14분 복근 3회 — 플랭크는 30초부터' },
      { icon: '🍱', text: '3끼 사진 21장 · 17시 이후엔 물과 말차만' },
      { icon: '🍵', text: '다실 3화 + 퀴즈 10문제 — 틀린 단어는 복습 노트에' },
      { icon: '🌅', text: '다음 수요일, 백지 위에 첫 획을 긋기' }
    ],
    metrics: { completedLessons: 0, quizTotal: 0 }
  },
  {
    id: '2026-10-25',
    publishedAt: '2026-10-25',
    periodStart: '2026-10-19',
    periodEnd: '2026-10-25',
    weekLabel: '10월 4주차',
    title: '불꽃 재시동 주간',
    score: 31,
    grade: '재시동',
    hero: './image/03 gemini/gemini_16_sprint.png',
    heroPos: 'center 18%',
    quote: '불꽃은 이미 피워두셨사옵니다.',
    intro: '어머나, 이번 주는 소녀도 조금 놀랐사옵니다. 러닝 4회, 근력 3회. 몸은 분명히 움직였사옵니다. 다만 식단과 재활, 그리고 다실은 아직 잠들어 있었지요. 🍵',
    closing: '움직인 기록은 사라지지 않사옵니다. 다음 주는 그 불꽃에 식단과 재활이라는 장작을 더해보시지요. 🌸',
    areas: [
      {
        icon: '🏃', name: '운동 수행', score: 26, max: 30, tag: '러닝 4회 · 근력 3회',
        comment: '러닝 25.7km, 근력 3회. 이 정도면 소녀도 고개를 끄덕일 수밖에 없사옵니다. 다만 복근은 끝까지 숨을 참고 있었사옵니다.'
      },
      {
        icon: '🩹', name: '재활 · 케어', score: 0, max: 25, tag: '재활 0 / 4회',
        comment: '열심히 달린 만큼 손목과 팔꿈치가 조용히 항의하고 있사옵니다. 케어 없는 운동은 반쪽짜리이옵니다.'
      },
      {
        icon: '🍱', name: '식단 · 수분', score: 5, max: 25, tag: '3끼 기록 거의 없음 · 차 3회',
        comment: '말차와 커피는 챙기셨사옵니다. 하지만 운동만큼 중요한 것은 접시 위의 기록이옵니다.'
      },
      {
        icon: '🍵', name: '일본어 다실', score: 0, max: 20, tag: '0화 · 기록 없음',
        comment: '몸의 불꽃은 피웠지만, 말의 불씨는 아직이옵니다. 다음 주엔 다실에서 뵙고 싶사옵니다.'
      }
    ],
    highlights: [
      { icon: '🏃', title: '러닝 4회 · 25.7km', text: '10/21, 10/23, 10/24, 10/25. 꾸준함의 정의를 몸으로 보여주셨사옵니다.' },
      { icon: '🏋️', title: '근력 3회 · 390reps', text: '체스트 프레스·케이블 로우·레그 프레스까지. 상체와 하체의 균형이 좋았사옵니다.' },
      { icon: '🍵', title: '말차 3회', text: '수분과 휴식도 운동의 일부이옵니다. 소녀가 인정하겠사옵니다.' }
    ],
    missions: [
      { icon: '🩹', text: '재활 4회 — 운동 전후 5분 손목 케어' },
      { icon: '🍱', text: '3끼 중 최소 2끼는 사진으로 남기기' },
      { icon: '🧘', text: '복근 3회 — 크런치 50회 × 2세트' },
      { icon: '🍵', text: '다실 2화 + 퀴즈 10문제' },
      { icon: '📉', text: '체중 64kg대 유지 · 다음 인바디에서 골격근 확인' }
    ],
    metrics: { completedLessons: 0, quizTotal: 0 }
  }
];
