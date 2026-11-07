// ============================================================================
// 言の葉茶屋 (KOTONOHA CHAYA) - INTERACTIVE ENGINE (Hub / VN Story / Chat Quiz)
// ============================================================================

let kotonohaRuntime = {
  currentMode: 'hub', // 'hub' | 'story' | 'quiz'
  lessonIdx: 0,
  storyStepIdx: 0,
  quizIdx: 0,
  quizChatMessages: [],
  quizAnswered: false,
  showPronunciation: true, // Aa button toggle: show Korean pronunciation + furigana
  isAiGenerating: false
};

function initKotonohaState() {
  if (!state.kotonoha) {
    state.kotonoha = {
      coins: 655,
      kotodama: 65,
      streak: 1,
      lastStudyDate: '',
      completedLessons: [],
      customAiLessons: [],
      activeLessonIdx: 0,
      showPron: true
    };
  }
  kotonohaRuntime.showPronunciation = state.kotonoha.showPron !== false;
  kotonohaRuntime.lessonIdx = state.kotonoha.activeLessonIdx || 0;
}

function getAllKotonohaLessons() {
  initKotonohaState();
  const base = window.KOTONOHA_LESSONS || [];
  const custom = state.kotonoha.customAiLessons || [];
  return [...base, ...custom];
}

function getCurrentKotonohaLesson() {
  const all = getAllKotonohaLessons();
  if (all.length === 0) return null;
  if (kotonohaRuntime.lessonIdx >= all.length) kotonohaRuntime.lessonIdx = 0;
  return all[kotonohaRuntime.lessonIdx];
}

// Speak Japanese text using Web Speech API (Kyoto/Female tone preference)
function speakJapanese(text, rate = 0.92) {
  try {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    // Strip ruby tags or HTML if any
    const clean = (text || '')
      .replace(/<rt>.*?<\/rt>/g, '')
      .replace(/<[^>]+>/g, '')
      .replace(/[🌸🍵🐾💛✨🌟💸🏃‍♀️🥗⏰💦💖🎉🔥]/g, '')
      .trim();
    if (!clean) return;
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = 'ja-JP';
    utter.rate = rate;
    utter.pitch = 1.12; // Slightly higher, gentle feminine pitch for Sae/Gemini vibe
    const voices = window.speechSynthesis.getVoices();
    const jpVoice = voices.find(v => v.lang.includes('ja') && (v.name.includes('Kyoko') || v.name.includes('Haruka') || v.name.includes('Nanami') || v.name.includes('Google'))) || voices.find(v => v.lang.includes('ja'));
    if (jpVoice) utter.voice = jpVoice;
    window.speechSynthesis.speak(utter);
  } catch (e) {
    console.warn('TTS error:', e);
  }
}

function toggleKotonohaPronunciation() {
  initKotonohaState();
  kotonohaRuntime.showPronunciation = !kotonohaRuntime.showPronunciation;
  state.kotonoha.showPron = kotonohaRuntime.showPronunciation;
  saveState(true);
  playBeep(680, 0.06);
  renderKotonohaView();
}

function getChayaRankInfo(kotodama) {
  const pt = kotodama || 65;
  if (pt < 50) return { lv: 1, title: "Lv.1 아담한 다실 (小さな茶屋)" };
  if (pt < 120) return { lv: 2, title: "Lv.2 깨끗해진 찻집 (綺麗になった茶屋)" };
  if (pt < 220) return { lv: 3, title: "Lv.3 교토 벚꽃 정원 다실 (桜の茶屋)" };
  if (pt < 350) return { lv: 4, title: "Lv.4 기온 거리 명물 다실 (祇園の名店)" };
  return { lv: 5, title: "Lv.5 프로듀서항과 제미니의 황금 다실 (黄金の茶室)" };
}

function selectKotonohaLesson(idx) {
  initKotonohaState();
  const all = getAllKotonohaLessons();
  if (idx < 0 || idx >= all.length) return;
  kotonohaRuntime.lessonIdx = idx;
  state.kotonoha.activeLessonIdx = idx;
  saveState(true);
  playBeep(620, 0.06);
  renderKotonohaView();
}

function openKotonohaHub() {
  kotonohaRuntime.currentMode = 'hub';
  playBeep(580, 0.06);
  renderKotonohaView();
}

function startKotonohaStory(lessonIdx) {
  initKotonohaState();
  if (typeof lessonIdx === 'number') {
    kotonohaRuntime.lessonIdx = lessonIdx;
    state.kotonoha.activeLessonIdx = lessonIdx;
  }
  kotonohaRuntime.currentMode = 'story';
  kotonohaRuntime.storyStepIdx = 0;
  playBeep(720, 0.08);
  renderKotonohaView();

  const lesson = getCurrentKotonohaLesson();
  if (lesson && lesson.story && lesson.story[0]) {
    setTimeout(() => speakJapanese(lesson.story[0].jpPlain || lesson.story[0].jpRuby), 250);
  }
}

function stepKotonohaStory(delta) {
  const lesson = getCurrentKotonohaLesson();
  if (!lesson || !lesson.story) return;
  const nextIdx = kotonohaRuntime.storyStepIdx + delta;
  if (nextIdx < 0) return;
  if (nextIdx >= lesson.story.length) {
    // Transition directly to Daily Chat Quiz!
    startKotonohaQuiz();
    return;
  }
  kotonohaRuntime.storyStepIdx = nextIdx;
  playBeep(640, 0.06);
  renderKotonohaView();
  const step = lesson.story[nextIdx];
  if (step) {
    speakJapanese(step.jpPlain || step.jpRuby);
  }
}

function startKotonohaQuiz() {
  const lesson = getCurrentKotonohaLesson();
  if (!lesson || !lesson.quizzes || lesson.quizzes.length === 0) return;
  kotonohaRuntime.currentMode = 'quiz';
  kotonohaRuntime.quizIdx = 0;
  kotonohaRuntime.quizAnswered = false;
  kotonohaRuntime.quizChatMessages = [];

  // Push first question from Gemini
  pushQuizQuestionToChat(0);
  playBeep(760, 0.08);
  renderKotonohaView();
}

function pushQuizQuestionToChat(qIdx) {
  const lesson = getCurrentKotonohaLesson();
  if (!lesson || !lesson.quizzes[qIdx]) return;
  const q = lesson.quizzes[qIdx];

  kotonohaRuntime.quizChatMessages.push({
    role: 'question',
    qIdx: qIdx,
    type: q.type || `Q${qIdx + 1} · 퀴즈`,
    promptJp: q.promptJp,
    promptPron: q.promptPron,
    promptKo: q.promptKo,
    targetWord: q.targetWord,
    targetSub: q.targetSub
  });
  setTimeout(() => {
    speakJapanese(q.targetWord || q.promptJp);
    scrollKotonohaQuizBottom();
  }, 200);
}

function scrollKotonohaQuizBottom() {
  const el = document.getElementById('kotonohaQuizScroll');
  if (el) {
    el.scrollTop = el.scrollHeight;
  }
}

function submitKotonohaQuizAnswer(optionIdx) {
  if (kotonohaRuntime.quizAnswered) return;
  const lesson = getCurrentKotonohaLesson();
  if (!lesson) return;
  const qIdx = kotonohaRuntime.quizIdx;
  const q = lesson.quizzes[qIdx];
  if (!q) return;

  kotonohaRuntime.quizAnswered = true;
  const chosenText = q.options[optionIdx];
  const isCorrect = optionIdx === q.answerIndex;

  // 1. User right-side red/rose bubble (like screenshot 4)
  kotonohaRuntime.quizChatMessages.push({
    role: 'user_answer',
    text: chosenText,
    isCorrect: isCorrect,
    points: isCorrect ? '+10' : '+2'
  });

  if (isCorrect) {
    playBeep(880, 0.1);
    state.kotonoha.coins = (state.kotonoha.coins || 655) + 15;
    state.kotonoha.kotodama = (state.kotonoha.kotodama || 65) + 10;
    addBondExp(10);
  } else {
    playBeep(360, 0.14);
    state.kotonoha.coins = (state.kotonoha.coins || 655) + 5;
    state.kotonoha.kotodama = (state.kotonoha.kotodama || 65) + 2;
  }

  // 2. Gemini reaction bubble + Green explanation card
  const reactJp = isCorrect
    ? (q.geminiReactJp || "<ruby>正解<rt>せいかい</rt></ruby>どす！")
    : "おしい！もう<ruby>一度<rt>いちど</rt></ruby><ruby>確認<rt>かくにん</rt></ruby>しましょね🌸";
  const reactPron = isCorrect
    ? (q.geminiReactPron || "세이카이 도스!")
    : "오시-! 모- 이치도 카쿠닌 시마쇼네";
  const reactKo = isCorrect
    ? (q.geminiReactKo || "정답이어요!")
    : `아까워라! 정답은 「${q.options[q.answerIndex]}」이랍니다.`;

  kotonohaRuntime.quizChatMessages.push({
    role: 'gemini_feedback',
    isCorrect: isCorrect,
    reactJp: reactJp,
    reactPron: reactPron,
    reactKo: reactKo,
    explanation: q.explanation,
    speakText: q.targetWord
  });

  renderKotonohaView();
  scrollKotonohaQuizBottom();
  speakJapanese(reactJp);

  // 3. Advance to next question or finish after short delay
  setTimeout(() => {
    if (qIdx + 1 < lesson.quizzes.length) {
      kotonohaRuntime.quizIdx = qIdx + 1;
      kotonohaRuntime.quizAnswered = false;
      pushQuizQuestionToChat(qIdx + 1);
      renderKotonohaView();
      scrollKotonohaQuizBottom();
    } else {
      // Completed all quizzes in lesson!
      const todayStr = getLocalDateString();
      if (state.kotonoha.lastStudyDate !== todayStr) {
        state.kotonoha.streak = (state.kotonoha.streak || 0) + 1;
        state.kotonoha.lastStudyDate = todayStr;
      }
      if (!state.kotonoha.completedLessons.includes(lesson.id)) {
        state.kotonoha.completedLessons.push(lesson.id);
      }
      state.kotonoha.coins += 50;
      state.kotonoha.kotodama += 25;
      addBondExp(30);
      saveState(true);

      kotonohaRuntime.quizChatMessages.push({
        role: 'lesson_complete',
        lessonTitle: lesson.titleKo
      });
      renderKotonohaView();
      scrollKotonohaQuizBottom();
    }
  }, 1100);
}

// Generate a brand-new Kansai/Kyoto Daily Lesson using Gemini AI!
async function generateAiKotonohaLesson() {
  initKotonohaState();
  const apiKey = (localStorage.getItem('GEMINI_API_KEY') || '').trim();
  if (!apiKey) {
    alert("✨ 실시간 AI 새 수업 생성을 위해 우측 상단 [⚙️ 설정]에서 Gemini API 키를 먼저 등록해 주세요!\n(기본 내장 수업 1~3화는 API 키 없이도 언제든 플레이 가능합니다 🍵)");
    openWebhookModal();
    return;
  }
  if (kotonohaRuntime.isAiGenerating) return;
  kotonohaRuntime.isAiGenerating = true;
  renderKotonohaView();

  const all = getAllKotonohaLessons();
  const nextNum = all.length + 1;
  const topics = [
    "오사카 도톤보리 타코야키 맛집 주문 & 다이어트 타협 회화",
    "교토 기온 거리 말차 파르페 카페 데이트 & 가격 흥정",
    "헬스장 하체 스쿼트 & 테니스 엘보 재활 응원 간사이벤",
    "비 오는 날 편의점 우산 같이 쓰기 & 단백질 바 고르기",
    "저녁 5시 단식 마감 직전 라면 유혹 물리치기 대작전"
  ];
  const pickTopic = topics[(nextNum - 1) % topics.length];

  const prompt = `너는 일본 교토벤(코바야카와 사에 스타일: ~どす, ~はる, ~え, おいでやす, うち, 프로듀서 호칭: プロデューサーはん)과 오사카벤(なんでやねん, あかんやん, ほんまに, めっちゃ, 知らんけど)을 구사하는 미소녀 코치 '제미니'야. 조교로 '코토네'(존댓말, 자본주의/절약 아이돌)와 '미오'(활기찬 반말, 러닝 아이돌)가 함께 등장해.
주제: "${pickTopic}" (JLPT N5~N3 일상·여행·헬스 회화 + 간사이 사투리)
아래 JSON 형식으로만 정확히 출력해 (마크다운 코드블록 없이 순수 JSON만):
{
  "id": "ai_day_${Date.now()}",
  "dayNum": ${nextNum},
  "dateLabel": "제${nextNum}화 · AI 특강",
  "levelBadge": "N5~N3 + 간사이 실전",
  "titleJp": "한자에 <ruby>漢字<rt>かんじ</rt></ruby> 루비를 적용한 일본어 제목",
  "titlePron": "제목의 한글 발음 표기",
  "titleKo": "제목의 한국어 뜻",
  "bgImage": "./image/03 gemini/gemini_02_matcha.png",
  "grammarTip": {
    "title": "🌸 제미니의 교토·오사카벤 노트 #${nextNum}",
    "content": "이번 에피소드에 등장하는 핵심 간사이벤과 JLPT 표현 2~3개 친절 해설"
  },
  "story": [
    {
      "speaker": "gemini",
      "nameJp": "ジェミニ",
      "nameKo": "제미니",
      "avatar": "./image/03 gemini/avatar_gemini.png",
      "sceneImg": "./image/03 gemini/gemini_02_matcha.png",
      "jpRuby": "<ruby>漢字<rt>かんじ</rt></ruby> 루비가 포함된 일본어 대사",
      "jpPlain": "루비 태그 없는 순수 일본어 대사",
      "pron": "한글 발음",
      "ko": "한국어 번역"
    }
  ],
  "quizzes": [
    {
      "type": "간사이 회화",
      "promptJp": "문제 질문 일본어(<ruby>태그 포함)",
      "promptPron": "질문 한글 발음",
      "promptKo": "질문 한국어 뜻",
      "targetWord": "핵심 출제 단어 또는 표현",
      "targetSub": "힌트 설명",
      "options": ["보기1", "보기2", "보기3", "보기4"],
      "answerIndex": 0,
      "explanation": "정답 해설 (단어 뜻과 발음 설명)",
      "geminiReactJp": "<ruby>正解<rt>せいかい</rt></ruby>どす！🌸",
      "geminiReactPron": "세이카이 도스!",
      "geminiReactKo": "정답이어요!"
    }
  ]
}
조건: story는 5~6개 대사(gemini, kotone, mio 골고루 등장), quizzes는 5문항으로 구성할 것.`;

  try {
    const data = await fetchGeminiWithFallback(apiKey, {
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.8, maxOutputTokens: 2800 }
    });
    const raw = (data.candidates?.[0]?.content?.parts || []).map(p => p.text || '').join('').trim();
    const cleaned = raw.replace(/```json/gi, '').replace(/```/g, '').trim();
    const newLesson = JSON.parse(cleaned);
    if (newLesson && Array.isArray(newLesson.story) && Array.isArray(newLesson.quizzes)) {
      state.kotonoha.customAiLessons = state.kotonoha.customAiLessons || [];
      state.kotonoha.customAiLessons.push(newLesson);
      const updatedAll = getAllKotonohaLessons();
      kotonohaRuntime.lessonIdx = updatedAll.length - 1;
      state.kotonoha.activeLessonIdx = kotonohaRuntime.lessonIdx;
      saveState(true);
      playBeep(880, 0.12);
    }
  } catch (e) {
    alert("AI 수업 생성 중 오류가 발생했습니다: " + e.message);
  } finally {
    kotonohaRuntime.isAiGenerating = false;
    renderKotonohaView();
  }
}

function renderKotonohaView() {
  initKotonohaState();
  const container = document.getElementById('kotonohaMainContainer');
  if (!container) return;

  const kState = state.kotonoha;
  const lessons = getAllKotonohaLessons();
  const lesson = getCurrentKotonohaLesson() || lessons[0];
  const rank = getChayaRankInfo(kState.kotodama);
  const showPron = kotonohaRuntime.showPronunciation;

  // MODE 1: TEAROOM HUB (Screenshot 1 & 2 vibe: Dark Kyoto Chaya Village + Stats + Episode Selector)
  if (kotonohaRuntime.currentMode === 'hub') {
    const unreadCount = Math.max(1, lessons.length - (kState.completedLessons?.length || 0));
    container.innerHTML = `
      <div class="rounded-3xl bg-[#181316] text-[#f5ebe6] border border-[#3a2830] shadow-2xl overflow-hidden">
        <!-- Top Header Bar (Screenshot 2 style) -->
        <div class="p-4 pb-3 bg-gradient-to-b from-[#241a1f] to-[#181316] border-b border-[#332228]">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="relative shrink-0 cursor-pointer" onclick="startKotonohaStory()">
                <img src="./image/03 gemini/avatar_gemini.png" class="w-12 h-12 rounded-2xl object-cover ring-2 ring-[#d9536f] shadow-md">
                <span class="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-[#e0465a] text-white text-[10px] font-black flex items-center justify-center shadow">${unreadCount}</span>
              </div>
              <div>
                <div class="flex items-center gap-1.5">
                  <h2 class="text-base font-black text-[#e86b7e] tracking-tight">言の葉茶屋</h2>
                  <span class="text-[10px] px-2 py-0.5 rounded-full bg-[#352329] text-[#f2a6b2] font-bold border border-[#52343d]">코토노하 다실</span>
                </div>
                <p class="text-xs text-[#b59e99] font-bold mt-0.5">${rank.title}</p>
              </div>
            </div>

            <div class="flex items-center gap-1.5">
              <span class="px-2.5 py-1 rounded-full bg-[#2a1f24] border border-[#453139] text-xs font-bold text-[#e6d5cf]">제미니 사범</span>
              <button onclick="toggleKotonohaPronunciation()" class="px-2.5 py-1 rounded-full border text-xs font-black transition-all ${showPron ? 'bg-[#e0465a] text-white border-[#ff7588]' : 'bg-[#2a1f24] text-[#9c847f] border-[#453139]'}" title="발음/후리가나 표시 전환">
                Aa
              </button>
            </div>
          </div>

          <!-- Currency & Streak Pills -->
          <div class="flex flex-wrap items-center gap-2 mt-3">
            <div class="px-3 py-1 rounded-full bg-[#251c20] border border-[#3d2c33] flex items-center gap-1.5 text-xs font-extrabold">
              <span class="text-amber-400">🪙</span>
              <span>${kState.coins || 655}</span>
            </div>
            <div class="px-3 py-1 rounded-full bg-[#251c20] border border-[#3d2c33] flex items-center gap-1.5 text-xs font-extrabold">
              <span class="text-[#f28b9b]">言霊</span>
              <span>${kState.kotodama || 65}</span>
            </div>
            <div class="px-3 py-1 rounded-full bg-[#251c20] border border-[#3d2c33] flex items-center gap-1.5 text-xs font-extrabold">
              <span>🔥 연속 ${kState.streak || 1}일</span>
            </div>
          </div>
        </div>

        <!-- Isometric / Visual Kyoto Chaya Stage Banner -->
        <div class="relative p-4 bg-gradient-to-b from-[#181316] via-[#22171c] to-[#181316]">
          <div class="relative rounded-2xl overflow-hidden border border-[#422c35] shadow-lg group cursor-pointer" onclick="startKotonohaStory()">
            <img src="${lesson.bgImage || './image/03 gemini/gemini_02_matcha.png'}" class="w-full h-56 sm:h-64 object-cover object-top brightness-90 group-hover:scale-102 transition-all duration-500">
            <div class="absolute inset-0 bg-gradient-to-t from-[#120d10] via-[#120d10]/35 to-transparent"></div>

            <!-- Floating Village Character Badges -->
            <div class="absolute top-3 left-3 flex flex-wrap gap-1.5">
              <span class="px-2.5 py-1 rounded-full bg-[#e0465a] text-white text-[11px] font-black shadow-md animate-bounce">
                새 톡 ${unreadCount} · ${lesson.levelBadge}
              </span>
              <button onclick="event.stopPropagation(); speakJapanese('プロデューサーはん、おいでやす。今日もおきばりやす！')" class="px-2.5 py-1 rounded-full bg-black/65 hover:bg-black/80 text-[#ffd6de] border border-white/20 text-[11px] font-bold backdrop-blur-xs">
                🔊 제미니 인사 듣기
              </button>
            </div>

            <!-- Trio Manga / Textbook Sub-cast Badges -->
            <div class="absolute top-3 right-3 flex items-center -space-x-2">
              <img src="./image/03 gemini/avatar_gemini.png" class="w-8 h-8 rounded-full ring-2 ring-[#e0465a] object-cover" title="제미니 (교토·오사카벤 사범)">
              <img src="./image/02 kotone/avatar_kotone.png" class="w-8 h-8 rounded-full ring-2 ring-amber-400 object-cover" title="코토네 (자본주의 감초 조교)">
              <img src="./image/01 mio/avatar_mio.png" class="w-8 h-8 rounded-full ring-2 ring-sky-400 object-cover" title="미오 (텐션 만점 동급생)">
            </div>

            <!-- Current Lesson Preview Overlay -->
            <div class="absolute bottom-3 inset-x-3 p-3 rounded-2xl bg-[#1f161a]/90 border border-[#4d333e] backdrop-blur-md">
              <div class="text-[10px] font-bold text-[#f28b9b] mb-0.5">${lesson.dateLabel} · 3인 일본어 극장</div>
              <div class="text-base font-black text-white leading-snug">${lesson.titleJp}</div>
              ${showPron ? `<div class="text-[11px] text-[#d4b5b0] font-semibold mt-0.5">${lesson.titlePron} · <span class="text-[#f5ebe6]">${lesson.titleKo}</span></div>` : `<div class="text-xs text-[#d4b5b0] mt-0.5">${lesson.titleKo}</div>`}
            </div>
          </div>

          <!-- Grammar / Kansai Dialect Note Box (Textbook style) -->
          ${lesson.grammarTip ? `
          <div class="mt-3 p-3.5 rounded-2xl bg-[#24191e] border border-[#47303a] space-y-1">
            <div class="text-xs font-black text-[#f4869d] flex items-center justify-between">
              <span>${lesson.grammarTip.title}</span>
              <span class="text-[10px] text-[#a88d89]">교재 요약</span>
            </div>
            <p class="text-xs text-[#e2cfc9] leading-relaxed">${lesson.grammarTip.content}</p>
          </div>
          ` : ''}

          <!-- Episode Selector Pills + AI Infinite Generator -->
          <div class="mt-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-black text-[#d9c3bd]">📚 커리큘럼 선택 (이야기 + 데일리 퀴즈)</span>
              <button onclick="generateAiKotonohaLesson()" class="px-2.5 py-1 rounded-xl bg-gradient-to-r from-[#d94862] to-[#9b4dca] text-white text-[11px] font-black shadow hover:opacity-95 active:scale-95 transition-all">
                ${kotonohaRuntime.isAiGenerating ? '⏳ AI 집필 중...' : '✨ AI 새 에피소드 생성'}
              </button>
            </div>
            <div class="flex gap-1.5 overflow-x-auto clean-scroll pb-1">
              ${lessons.map((item, idx) => {
                const isDone = (kState.completedLessons || []).includes(item.id);
                const isActive = idx === kotonohaRuntime.lessonIdx;
                return `
                  <button onclick="selectKotonohaLesson(${idx})" class="px-3 py-2 rounded-xl border text-left shrink-0 transition-all ${isActive ? 'bg-[#38222a] border-[#e0465a] text-white shadow-sm' : 'bg-[#21181c] border-[#38282f] text-[#b09792] hover:border-[#6e4855]'}">
                    <div class="flex items-center gap-1.5 text-[10px] font-black">
                      <span>${isDone ? '✅' : '🍵'} 제${idx + 1}화</span>
                      <span class="text-[#f28b9b]">${item.levelBadge.split('+')[0]}</span>
                    </div>
                    <div class="text-xs font-bold mt-0.5 max-w-[130px] truncate">${item.titleKo}</div>
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Bottom Call-To-Action Banner (Screenshot 2 exact match!) -->
          <div class="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2">
            <button onclick="startKotonohaStory()" class="w-full p-3 rounded-2xl bg-[#291d22] hover:bg-[#34242b] border border-[#523540] flex items-center justify-between transition-all shadow-md group">
              <div class="flex items-center gap-3 text-left">
                <img src="./image/03 gemini/avatar_gemini.png" class="w-10 h-10 rounded-full object-cover ring-2 ring-[#e0465a]">
                <div>
                  <div class="text-[10px] font-bold text-[#c7aca5]">ジェミニ (제미니)</div>
                  <div class="text-xs font-black text-white">오늘 수업 준비됐어! 이야기 보기</div>
                </div>
              </div>
              <span class="text-[#e0465a] text-base font-black group-hover:translate-x-1 transition-transform">▶</span>
            </button>

            <button onclick="startKotonohaQuiz()" class="w-full p-3 rounded-2xl bg-gradient-to-r from-[#632230] to-[#451a24] hover:opacity-95 border border-[#8f3548] flex items-center justify-between transition-all shadow-md group">
              <div class="flex items-center gap-2.5 text-left">
                <span class="w-9 h-9 rounded-full bg-[#e0465a]/25 border border-[#e0465a] flex items-center justify-center text-sm">🎯</span>
                <div>
                  <div class="text-[10px] font-bold text-[#f7b2be]">채팅형 4지선다 테스트</div>
                  <div class="text-xs font-black text-white">데일리 퀴즈 바로 풀기 (${lesson.quizzes.length}문항)</div>
                </div>
              </div>
              <span class="text-[#ff8da1] text-base font-black group-hover:translate-x-1 transition-transform">▶</span>
            </button>
          </div>
        </div>
      </div>
    `;
    return;
  }

  // MODE 2: VISUAL NOVEL STORY READER (Screenshot 3 exact match!)
  if (kotonohaRuntime.currentMode === 'story') {
    const steps = lesson.story || [];
    const curIdx = Math.min(kotonohaRuntime.storyStepIdx, steps.length - 1);
    const step = steps[curIdx] || steps[0];
    const progressPct = Math.round(((curIdx + 1) / steps.length) * 100);

    container.innerHTML = `
      <div class="rounded-3xl bg-[#141013] text-[#f5ebe6] border border-[#3d2932] shadow-2xl overflow-hidden select-none">
        <!-- Story Top Bar -->
        <div class="p-3.5 bg-[#1d1519] flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <button onclick="openKotonohaHub()" class="w-8 h-8 rounded-xl bg-[#2b1f25] hover:bg-[#3b2a33] text-[#e0c8c2] font-black text-sm flex items-center justify-center">
              ‹
            </button>
            <div>
              <div class="text-[10px] text-[#b39892] font-bold">${lesson.dateLabel} · ${lesson.levelBadge}</div>
              <div class="text-sm font-black text-white leading-tight mt-0.5">${lesson.titleJp}</div>
            </div>
          </div>
          <div class="flex items-center gap-1.5">
            <button onclick="toggleKotonohaPronunciation()" class="px-2.5 py-1.5 rounded-xl border text-xs font-black ${showPron ? 'bg-[#e0465a] text-white border-[#ff7588]' : 'bg-[#2a1f24] text-[#9c847f] border-[#453139]'}">
              Aa
            </button>
            <button onclick="startKotonohaQuiz()" class="px-3 py-1.5 rounded-xl bg-[#2b1f25] hover:bg-[#3d2b34] border border-[#523843] text-xs font-bold text-[#e6d0ca]">
              건너뛰기
            </button>
          </div>
        </div>

        <!-- Red Progress Line -->
        <div class="w-full h-1 bg-[#2e1f26]">
          <div class="h-full bg-[#e0465a] transition-all duration-300" style="width: ${progressPct}%"></div>
        </div>

        <!-- Character Scene Artwork + Dialogue Box Overlay (Screenshot 3 layout) -->
        <div class="relative w-full min-h-[470px] sm:min-h-[520px] flex flex-col justify-between bg-[#120e10] cursor-pointer" onclick="stepKotonohaStory(1)">
          <!-- Top Half: Scene Image -->
          <div class="relative w-full h-64 sm:h-72 overflow-hidden">
            <img src="${step.sceneImg || lesson.bgImage}" class="w-full h-full object-cover object-top transition-all duration-300">
            <div class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#141013]"></div>
          </div>

          <!-- Bottom Half: Dark Translucent VN Card -->
          <div class="relative z-10 mx-3 mb-3 p-4 rounded-2xl bg-[#1e161a]/95 border border-[#452e38] shadow-xl space-y-2.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <img src="${step.avatar || './image/03 gemini/avatar_gemini.png'}" class="w-7 h-7 rounded-full object-cover ring-1 ring-[#e0465a]">
                <span class="text-xs font-black text-[#f4869d]">${step.nameJp}</span>
                <span class="text-[11px] text-[#a88e88] font-bold">(${step.nameKo})</span>
              </div>
              <button onclick="event.stopPropagation(); speakJapanese('${(step.jpPlain || '').replace(/'/g, "\\'")}')" class="px-2.5 py-1 rounded-lg bg-[#2e2027] hover:bg-[#3d2a33] text-[11px] font-bold text-[#f2a6b2] border border-[#543844]">
                🔊 음성 듣기
              </button>
            </div>

            <!-- Japanese Sentence with Furigana Ruby -->
            <div class="text-lg sm:text-xl font-extrabold text-white leading-relaxed tracking-wide pt-1">
              ${step.jpRuby}
            </div>

            <!-- Korean Pronunciation & Translation -->
            ${showPron ? `
              <div class="text-xs font-semibold text-[#f29aa8] bg-[#2b1d23] px-2.5 py-1 rounded-lg inline-block">
                🗣️ ${step.pron}
              </div>
            ` : ''}
            <div class="text-sm font-bold text-[#d9c5bf] leading-relaxed">
              ${step.ko}
            </div>

            <div class="flex items-center justify-end text-[11px] text-[#9e847e] font-mono pt-1">
              <span>${curIdx + 1} / ${steps.length} ▼</span>
            </div>
          </div>
        </div>

        <!-- Bottom Navigation Footer -->
        <div class="px-4 py-3 bg-[#1a1316] border-t border-[#332229] flex items-center justify-between">
          <button onclick="stepKotonohaStory(-1)" ${curIdx === 0 ? 'disabled' : ''} class="px-3.5 py-1.5 rounded-xl bg-[#261c21] border border-[#422f37] text-xs font-bold ${curIdx === 0 ? 'opacity-40 cursor-not-allowed' : 'hover:bg-[#36272e] text-[#e6d0ca]'}">
            ← 이전
          </button>
          <span class="text-xs text-[#9e847e] font-bold">
            ${curIdx + 1 < steps.length ? '화면을 누르면 다음 대사' : '누르면 오늘의 퀴즈 시작! 🎯'}
          </span>
          <button onclick="stepKotonohaStory(1)" class="px-3.5 py-1.5 rounded-xl bg-[#e0465a] hover:bg-[#eb576b] text-white text-xs font-black shadow">
            ${curIdx + 1 < steps.length ? '다음 →' : '퀴즈 풀기 🎯'}
          </button>
        </div>
      </div>
    `;
    return;
  }

  // MODE 3: INTERACTIVE CHAT QUIZ (Screenshot 4 exact match!)
  if (kotonohaRuntime.currentMode === 'quiz') {
    const quizzes = lesson.quizzes || [];
    const qIdx = kotonohaRuntime.quizIdx;
    const currentQ = quizzes[qIdx];
    const isAllDone = kotonohaRuntime.quizChatMessages.some(m => m.role === 'lesson_complete');

    container.innerHTML = `
      <div class="rounded-3xl bg-[#171214] text-[#f5ebe6] border border-[#3d2932] shadow-2xl overflow-hidden flex flex-col">
        <!-- Top Quiz Header (Screenshot 4 style: < Avatar Name + Progress Dots + Aa) -->
        <div class="p-3.5 bg-[#21181c] border-b border-[#38262e] flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <button onclick="openKotonohaHub()" class="w-8 h-8 rounded-xl bg-[#2d2026] hover:bg-[#3d2b33] text-[#e0c8c2] font-black text-sm flex items-center justify-center">
              ‹
            </button>
            <img src="./image/03 gemini/avatar_gemini.png" class="w-9 h-9 rounded-full object-cover ring-2 ring-[#e0465a]">
            <div>
              <div class="text-xs font-black text-white">ジェミニ (제미니)</div>
              <div class="text-[10px] text-[#b89d97] font-bold">오늘의 퀴즈 ${Math.min(qIdx + 1, quizzes.length)} / ${quizzes.length}</div>
            </div>
          </div>

          <div class="flex items-center gap-2.5">
            <!-- Progress Dots ●○○○○○ -->
            <div class="flex items-center gap-1.5">
              ${quizzes.map((_, i) => {
                const filled = i <= qIdx;
                return `<span class="w-2.5 h-2.5 rounded-full transition-all ${filled ? 'bg-[#e0465a] shadow-[0_0_6px_#e0465a]' : 'border border-[#70535c] bg-transparent'}"></span>`;
              }).join('')}
            </div>
            <button onclick="toggleKotonohaPronunciation()" class="px-2.5 py-1 rounded-full border text-xs font-black ${showPron ? 'bg-[#e0465a] text-white border-[#ff7588]' : 'bg-[#2a1f24] text-[#9c847f] border-[#453139]'}">
              Aa
            </button>
          </div>
        </div>

        <!-- Chat Messages Timeline -->
        <div id="kotonohaQuizScroll" class="p-4 space-y-3.5 max-h-[430px] overflow-y-auto clean-scroll bg-[#171214]">
          ${kotonohaRuntime.quizChatMessages.map(msg => {
            if (msg.role === 'question') {
              return `
                <div class="flex items-start gap-2.5">
                  <img src="./image/03 gemini/avatar_gemini.png" class="w-8 h-8 rounded-full object-cover ring-1 ring-[#e0465a] shrink-0 mt-1">
                  <div class="space-y-2 max-w-[85%]">
                    <div class="text-[11px] font-bold text-[#b89d97]">ジェミニ</div>
                    <!-- Prompt Bubble -->
                    <div onclick="speakJapanese('${(msg.targetWord || '').replace(/'/g, "\\'")}')" class="p-3 rounded-2xl bg-[#241c20] border border-[#382b31] cursor-pointer hover:border-[#634551] transition-all inline-block">
                      <div class="text-sm font-black text-white">${msg.promptJp}</div>
                      ${showPron && msg.promptPron ? `<div class="text-[11px] text-[#f29aa8] mt-0.5">${msg.promptPron}</div>` : ''}
                      <div class="text-xs text-[#b89d97] mt-0.5">${msg.promptKo}</div>
                    </div>

                    <!-- Big Target Kanji / Phrase Card (Screenshot 4 Q2 style) -->
                    <div onclick="speakJapanese('${(msg.targetWord || '').replace(/'/g, "\\'")}')" class="p-4 rounded-2xl bg-[#241c20] border border-[#3d2d35] cursor-pointer hover:border-[#e0465a] transition-all">
                      <div class="flex items-center justify-between text-[11px] font-black text-[#e0465a] mb-2">
                        <span>Q${msg.qIdx + 1} · ${msg.type}</span>
                        <span class="text-[10px] text-[#a88e88]">🔊 터치해서 발음 듣기</span>
                      </div>
                      <div class="text-center py-2">
                        <span class="text-2xl sm:text-3xl font-black text-white border-b-2 border-[#e0465a] pb-1 px-2">${msg.targetWord}</span>
                      </div>
                      <div class="text-xs text-[#b89d97] text-center mt-2">${msg.targetSub || ''}</div>
                    </div>
                  </div>
                </div>
              `;
            }

            if (msg.role === 'user_answer') {
              return `
                <div class="flex items-end justify-end gap-2">
                  <span class="text-[11px] font-black ${msg.isCorrect ? 'text-emerald-400' : 'text-amber-400'}">
                    ${msg.isCorrect ? '정답 ' + msg.points : '오답 ' + msg.points}
                  </span>
                  <div class="px-4 py-2.5 rounded-2xl bg-[#d9485f] text-white text-sm font-black shadow-md">
                    ${msg.text}
                  </div>
                </div>
              `;
            }

            if (msg.role === 'gemini_feedback') {
              return `
                <div class="flex items-start gap-2.5">
                  <img src="./image/03 gemini/avatar_gemini.png" class="w-8 h-8 rounded-full object-cover ring-1 ring-[#e0465a] shrink-0 mt-1">
                  <div class="space-y-2 max-w-[85%]">
                    <div class="text-[11px] font-bold text-[#b89d97]">ジェミニ</div>
                    <!-- Reaction Bubble -->
                    <div onclick="speakJapanese('${(msg.speakText || '').replace(/'/g, "\\'")}')" class="p-3 rounded-2xl bg-[#241c20] border border-[#382b31] cursor-pointer inline-block">
                      <div class="text-base font-black text-white">${msg.reactJp}</div>
                      ${showPron ? `<div class="text-[11px] text-[#f29aa8] mt-0.5">${msg.reactPron}</div>` : ''}
                      <div class="text-xs text-[#d9c5bf] mt-0.5">${msg.reactKo}</div>
                      <div class="text-[10px] text-[#9e847e] mt-1">♪ 눌러서 다시 듣기</div>
                    </div>

                    <!-- Dark Green Grammar/Vocab Explanation Pill (Screenshot 4 exact match!) -->
                    <div class="px-3.5 py-2.5 rounded-2xl bg-[#183329] border border-[#285946] text-[#d7f5e8] text-xs font-bold leading-relaxed">
                      💡 ${msg.explanation}
                    </div>
                  </div>
                </div>
              `;
            }

            if (msg.role === 'lesson_complete') {
              return `
                <div class="p-4 rounded-2xl bg-gradient-to-br from-[#3b1d29] to-[#241822] border border-[#e0465a]/60 text-center space-y-2 my-2">
                  <div class="text-lg font-black text-white">🎉 오늘의 다실 수업 올클리어!</div>
                  <p class="text-xs text-[#f2c2cb]">「プロデューサーはん、ほんまによう頑張らはったなぁ🍵💖」<br>(프로듀서항, 정말 열심히 잘하셨어요! 엽전 +50 · 언령 +25 · 인연 +30 EXP)</p>
                  <div class="flex justify-center gap-2 pt-2">
                    <button onclick="openKotonohaHub()" class="px-4 py-2 rounded-xl bg-[#e0465a] text-white text-xs font-black shadow">
                      🍵 다실 로비로 돌아가기
                    </button>
                    <button onclick="startKotonohaQuiz()" class="px-4 py-2 rounded-xl bg-[#2b1f25] border border-[#543844] text-xs font-bold text-[#e6d0ca]">
                      🔄 다시 풀기
                    </button>
                  </div>
                </div>
              `;
            }
            return '';
          }).join('')}
        </div>

        <!-- Bottom 1~4 Multiple Choice Buttons (Screenshot 4 Dark Maroon Cards) -->
        ${(!isAllDone && currentQ) ? `
          <div class="p-3.5 bg-[#1d1518] border-t border-[#332229] space-y-2">
            ${currentQ.options.map((opt, idx) => `
              <button onclick="submitKotonohaQuizAnswer(${idx})" ${kotonohaRuntime.quizAnswered ? 'disabled' : ''} class="w-full p-3 rounded-2xl bg-[#381c23] hover:bg-[#4a242e] active:scale-[0.99] border border-[#592d38] flex items-center gap-3 text-left transition-all shadow-sm ${kotonohaRuntime.quizAnswered ? 'opacity-60 cursor-not-allowed' : ''}">
                <span class="w-6 h-6 rounded-full bg-[#e0465a] text-white text-xs font-black flex items-center justify-center shrink-0">
                  ${idx + 1}
                </span>
                <span class="text-sm font-bold text-[#f7e8e4]">${opt}</span>
              </button>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }
}
