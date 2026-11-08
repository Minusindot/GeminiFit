// ============================================================================
// 言の葉茶屋 (KOTONOHA CHAYA) - INTERACTIVE ENGINE (Hub / TTS Preloader / VN Story / Chat Quiz)
// ============================================================================

let kotonohaRuntime = {
  currentMode: 'hub', // 'hub' | 'loading_tts' | 'story' | 'quiz'
  lessonIdx: 0,
  storyStepIdx: 0,
  quizIdx: 0,
  quizChatMessages: [],
  quizAnswered: false,
  showPronunciation: true, // Aa button toggle: show Korean pronunciation + furigana
  isAiGenerating: false,
  selectedSeason: 1,
  ttsLoading: {
    active: false,
    done: 0,
    total: 1,
    percent: 0,
    currentSpeaker: 'gemini',
    currentText: '',
    targetMode: 'story',
    runId: 0
  }
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
      selectedSeason: 1,
      showPron: true
    };
  }
  kotonohaRuntime.showPronunciation = state.kotonoha.showPron !== false;
  kotonohaRuntime.lessonIdx = state.kotonoha.activeLessonIdx || 0;
  kotonohaRuntime.selectedSeason = state.kotonoha.selectedSeason || 1;
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
const CHARACTER_VOICE_PROFILES = {
  gemini: {
    name: '제미니',
    pitch: 0.95, // 차분하고 단아한 교토 아가씨 톤
    rate: 0.88,  // 여유롭고 부드러운 교토벤 템포
    preferredNames: ['kyoko', 'haruka', 'keiko', 'standard-a', 'google 日本語']
  },
  mio: {
    name: '미오',
    pitch: 1.18, // 활기차고 당찬 체육계 톰보이 톤
    rate: 1.08,  // 시원시원하고 빠른 스포티 템포
    preferredNames: ['nanami', 'otoya', 'standard-c', 'microsoft nanami']
  },
  kotone: {
    name: '코토네',
    pitch: 1.42, // 확실히 높고 통통 튀는 아이돌 하이톤!
    rate: 0.98,  // 리드미컬하고 애교 있는 템포
    preferredNames: ['ayumi', 'sora', 'standard-b', 'microsoft ayumi']
  }
};

// ============================================================================
// VOICEVOX SUBCULTURE ANIME TTS ENGINE & BATCH PRELOADER (Metan / Tsumugi / Zundamon)
// ============================================================================

let currentKotonohaAudio = null;
// Pending quiz-advance: survives per-utterance interruption (e.g. '다시 듣기' replay clicks)
let pendingQuizAdvance = null;
const kotonohaAudioCache = {};
const kotonohaPreloadedAudio = {};

// Pre-bundled high quality VOICEVOX MP3 assets (Instant 0ms latency & authentic anime voices)
const KOTONOHA_PRESET_AUDIO = {
  "靴": "./audio/kotonoha/word_kutsu.mp3",
  "おいでやす": "./audio/kotonoha/word_oideyasu.mp3",
  "白": "./audio/kotonoha/word_shiro.mp3",
  "正解どす！": "./audio/kotonoha/react_correct_gemini.mp3",
  "正解どす": "./audio/kotonoha/react_correct_gemini.mp3",
  "ピンポン-！お見事どすえ🍵": "./audio/kotonoha/react_migoto_gemini.mp3",
  "ピンポン！お見事どすえ": "./audio/kotonoha/react_migoto_gemini.mp3",
  "月曜日の朝。ジェミニの茶屋どす。": "./audio/kotonoha/day1_step1.mp3",
  "プロデューサーはん、おいでやす。今日もおきばりやす！": "./audio/kotonoha/day1_step2.mp3",
  "ヤッホー！新しい白い靴を買ったよ！": "./audio/kotonoha/day1_step3.mp3",
  "わあ、高そうな靴ですね！何円ですか？！": "./audio/kotonoha/day1_step4.mp3",
  "ちょっとミオはん、茶屋の中で靴を履いたらあかんやん！": "./audio/kotonoha/day1_step5.mp3",
  "あ、ほんとだ！ここは土足厳禁でしたね！": "./audio/kotonoha/day1_step6.mp3",
  "あら、ほんまどすなぁ。ふふ、ほな皆でお抹茶を飲みましょか。": "./audio/kotonoha/day1_step7.mp3"
};

// ============================================================================
// PERSISTENT INDEXEDDB VOICEVOX AUDIO CACHE (Survives Reloads & App Restarts)
// ============================================================================
const KOTONOHA_DB_NAME = 'KotonohaAudioDB_v1';
const KOTONOHA_STORE_NAME = 'voicevox_audio_blobs';
let kotonohaDbPromise = null;

function getKotonohaDb() {
  if (!kotonohaDbPromise) {
    kotonohaDbPromise = new Promise((resolve) => {
      if (typeof window === 'undefined' || !('indexedDB' in window)) return resolve(null);
      try {
        const req = indexedDB.open(KOTONOHA_DB_NAME, 1);
        req.onupgradeneeded = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains(KOTONOHA_STORE_NAME)) {
            db.createObjectStore(KOTONOHA_STORE_NAME);
          }
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(null);
      } catch (_) {
        resolve(null);
      }
    });
  }
  return kotonohaDbPromise;
}

async function getCachedAudioBlobFromIdb(key) {
  try {
    const db = await getKotonohaDb();
    if (!db) return null;
    return new Promise((resolve) => {
      const tx = db.transaction(KOTONOHA_STORE_NAME, 'readonly');
      const store = tx.objectStore(KOTONOHA_STORE_NAME);
      const req = store.get(key);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => resolve(null);
    });
  } catch (_) {
    return null;
  }
}

async function saveAudioBlobToIdb(key, blob) {
  try {
    const db = await getKotonohaDb();
    if (!db || !blob) return;
    const tx = db.transaction(KOTONOHA_STORE_NAME, 'readwrite');
    const store = tx.objectStore(KOTONOHA_STORE_NAME);
    store.put(blob, key);
  } catch (_) {}
}

// Warm up in-memory cache from IndexedDB on startup
async function initKotonohaPersistentAudioCache() {
  try {
    const db = await getKotonohaDb();
    if (!db) return;
    const tx = db.transaction(KOTONOHA_STORE_NAME, 'readonly');
    const store = tx.objectStore(KOTONOHA_STORE_NAME);
    const req = store.openCursor();
    req.onsuccess = (e) => {
      const cursor = e.target.result;
      if (cursor) {
        const key = cursor.key;
        const blob = cursor.value;
        if (blob && !kotonohaAudioCache[key]) {
          const blobUrl = URL.createObjectURL(blob);
          kotonohaAudioCache[key] = blobUrl;
          bufferAudioElement(blobUrl, 3000).then((aud) => {
            if (aud) kotonohaPreloadedAudio[key] = aud;
          });
        }
        cursor.continue();
      }
    };
  } catch (_) {}
}

if (typeof window !== 'undefined') {
  setTimeout(initKotonohaPersistentAudioCache, 600);
}

// VOICEVOX Subculture Anime Character Voice Mapping
const VOICEVOX_SPEAKERS = {
  gemini: 2,  // 四国めたん (Shikoku Metan - elegant tsundere ojousama)
  kotone: 8,  // 春日部つむぎ (Kasukabe Tsumugi - lively cute idol)
  mio: 3      // ずんだもん (Zundamon - spirited mascot runner)
};

function cleanKotonohaTtsText(text) {
  return (text || '')
    .replace(/<rt>.*?<\/rt>/g, '')
    .replace(/<[^>]+>/g, '')
    .replace(/[🌸🍵🐾💛✨🌟💸🏃‍♀️🥗⏰💦💖🎉🔥🗣️🇯🇵⛩️♨️🚇🌇📚🎐🍁❄️🌨️💆‍♀️👩‍🍳🥂📏🪭🐣🐙👓🔒🎋📦👒🍂🧤😭🍅🙈⚖️🏅😠🐹🤩🍨🎶💃🏷️⚡👟💧🎍🦶🗺️🚃🍱✏️🧥💪⏱️📣🌿😊🥤💓🤝😱🥇👍🌪️]/g, '')
    .trim();
}

function getKotonohaCacheKey(text, speaker = 'gemini') {
  if (typeof text === 'string' && (text.endsWith('.mp3') || text.startsWith('./audio/'))) {
    return `FILE_${text}`;
  }
  const clean = cleanKotonohaTtsText(text);
  if (KOTONOHA_PRESET_AUDIO[clean]) {
    return `FILE_${KOTONOHA_PRESET_AUDIO[clean]}`;
  }
  const spkId = VOICEVOX_SPEAKERS[speaker] || 2;
  return `${spkId}_${clean}`;
}

function sleepMs(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Wait until an audio URL is actually playable and buffered by the browser
function bufferAudioElement(audioUrl, timeoutMs = 6000) {
  return new Promise((resolve) => {
    try {
      const audio = new Audio();
      audio.preload = 'auto';
      let settled = false;
      const finish = (ok) => {
        if (!settled) {
          settled = true;
          resolve(ok ? audio : null);
        }
      };
      const timer = setTimeout(() => finish(true), timeoutMs);
      audio.oncanplaythrough = () => { clearTimeout(timer); finish(true); };
      audio.onloadeddata = () => { clearTimeout(timer); finish(true); };
      audio.onerror = () => { clearTimeout(timer); finish(false); };
      audio.src = audioUrl;
      audio.load();
    } catch (_) {
      resolve(null);
    }
  });
}

// Wait for VOICEVOX audioStatusUrl to report isAudioReady === true before playing/buffering
async function waitVoicevoxAudioReady(statusUrl, maxWaitMs = 9000) {
  if (!statusUrl) return true;
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    try {
      const r = await fetch(statusUrl);
      if (r.ok) {
        const st = await r.json();
        if (st.isAudioReady) return true;
        if (st.isAudioError) return false;
      }
    } catch (_) {}
    await sleepMs(420);
  }
  return false;
}

// Synthesize & pre-buffer a single line so playback is 100% genuine VOICEVOX with 0ms latency
async function synthesizeAndBufferVoicevox(text, speaker = 'gemini') {
  let audioTarget = null;
  if (typeof text === 'string' && (text.endsWith('.mp3') || text.startsWith('./audio/'))) {
    audioTarget = text;
  }
  const clean = cleanKotonohaTtsText(text);
  if (!audioTarget && KOTONOHA_PRESET_AUDIO[clean]) {
    audioTarget = KOTONOHA_PRESET_AUDIO[clean];
  }

  const cacheKey = getKotonohaCacheKey(text, speaker);

  // 1. Preset local MP3 file
  if (audioTarget) {
    kotonohaAudioCache[cacheKey] = audioTarget;
    if (!kotonohaPreloadedAudio[cacheKey]) {
      const buffered = await bufferAudioElement(audioTarget, 3000);
      if (buffered) kotonohaPreloadedAudio[cacheKey] = buffered;
    }
    return audioTarget;
  }

  if (!clean) return null;

  // 2. Already in memory cache
  if (kotonohaAudioCache[cacheKey] && kotonohaPreloadedAudio[cacheKey]) {
    return kotonohaAudioCache[cacheKey];
  }

  // 2.5. Check persistent IndexedDB cache (Survives app restarts & reloads)
  try {
    const savedBlob = await getCachedAudioBlobFromIdb(cacheKey);
    if (savedBlob) {
      const blobUrl = URL.createObjectURL(savedBlob);
      kotonohaAudioCache[cacheKey] = blobUrl;
      const buffered = await bufferAudioElement(blobUrl, 3500);
      if (buffered) {
        kotonohaPreloadedAudio[cacheKey] = buffered;
        return blobUrl;
      }
    }
  } catch (_) {}

  const spkId = VOICEVOX_SPEAKERS[speaker] || 2;
  const apiUrl = `https://api.tts.quest/v3/voicevox/synthesis?text=${encodeURIComponent(clean)}&speaker=${spkId}`;

  // Up to 3 attempts (respecting retryAfter rate-limit responses from tts.quest)
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 7000);
      const resp = await fetch(apiUrl, { signal: controller.signal });
      clearTimeout(timeout);

      const data = await resp.json().catch(() => ({}));
      if (data && typeof data.retryAfter === 'number' && data.retryAfter > 0) {
        await sleepMs((data.retryAfter + 0.8) * 1000);
        continue;
      }

      const audioUrl = data.mp3DownloadUrl || data.wavDownloadUrl || data.mp3StreamingUrl;
      if (!audioUrl) {
        await sleepMs(600);
        continue;
      }

      // CRITICAL FIX: Wait until VOICEVOX server finishes rendering the MP3 before attempting to load/play!
      if (data.audioStatusUrl) {
        const ready = await waitVoicevoxAudioReady(data.audioStatusUrl, 9500);
        if (!ready) {
          await sleepMs(500);
          continue;
        }
      }

      const buffered = await bufferAudioElement(audioUrl, 5500);
      if (buffered) {
        kotonohaAudioCache[cacheKey] = audioUrl;
        kotonohaPreloadedAudio[cacheKey] = buffered;
        // Persist to IndexedDB in background so user NEVER has to download it again
        fetch(audioUrl)
          .then(r => r.blob())
          .then(b => saveAudioBlobToIdb(cacheKey, b))
          .catch(() => {});
        return audioUrl;
      }
    } catch (_) {
      await sleepMs(600);
    }
  }
  return null;
}

// Collect all unique voice items across Story + Quiz for a lesson
function collectLessonVoiceItems(lesson) {
  if (!lesson) return [];
  const items = [];
  const seen = new Set();

  const addItem = (rawText, speaker, label) => {
    if (!rawText) return;
    const key = getKotonohaCacheKey(rawText, speaker);
    if (seen.has(key)) return;
    seen.add(key);
    items.push({ rawText, speaker: speaker || 'gemini', key, label });
  };

  // 1. All story steps
  (lesson.story || []).forEach((st, idx) => {
    addItem(
      st.audio || st.jpPlain || st.jpRuby,
      st.speaker || 'gemini',
      `스토리 ${idx + 1}/${lesson.story.length} (${st.nameKo || '제미니'})`
    );
  });

  // 2. All quiz questions & reactions
  (lesson.quizzes || []).forEach((q, idx) => {
    addItem(
      q.targetWord || q.promptJp,
      'gemini',
      `퀴즈 Q${idx + 1} 출제 어휘`
    );
    addItem(
      q.geminiReactJp || "<ruby>正解<rt>せいかい</rt></ruby>どす！",
      'gemini',
      `퀴즈 Q${idx + 1} 정답 리액션`
    );
  });

  // 3. Common wrong answer reaction
  addItem(
    "おしい！もう<ruby>一度<rt>いちど</rt></ruby><ruby>確認<rt>かくにん</rt></ruby>しましょね🌸",
    'gemini',
    '퀴즈 오답 격려 보이스'
  );

  return items;
}

function isLessonVoiceFullyCached(lesson) {
  const items = collectLessonVoiceItems(lesson);
  return items.every(it => Boolean(kotonohaAudioCache[it.key] && kotonohaPreloadedAudio[it.key]));
}

// Fallback Browser Web Speech API (Only when completely offline)
function speakJapaneseFallback(clean, speaker = 'gemini', customRate = null, onEndCallback = null) {
  try {
    if (!('speechSynthesis' in window)) {
      if (typeof onEndCallback === 'function') setTimeout(onEndCallback, 300);
      return;
    }
    window.speechSynthesis.cancel();

    const profile = CHARACTER_VOICE_PROFILES[speaker] || CHARACTER_VOICE_PROFILES.gemini;
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = 'ja-JP';
    utter.pitch = profile.pitch;
    utter.rate = customRate || profile.rate;

    const estDurationMs = Math.max(2200, Math.round((clean.length / (profile.rate || 0.9)) * 190 + 700));

    let callbackFired = false;
    const handleComplete = () => {
      if (!callbackFired) {
        callbackFired = true;
        if (typeof onEndCallback === 'function') onEndCallback();
        if (typeof pendingQuizAdvance === 'function') {
          const adv = pendingQuizAdvance;
          pendingQuizAdvance = null;
          adv();
        }
      }
    };

    utter.onend = handleComplete;
    utter.onerror = handleComplete;
    setTimeout(handleComplete, estDurationMs + 800);

    const voices = window.speechSynthesis.getVoices() || [];
    const jpVoices = voices.filter(v => v.lang && (v.lang.includes('ja') || v.lang.startsWith('ja')));

    if (jpVoices.length > 0) {
      let matched = jpVoices.find(v => {
        const vName = (v.name || '').toLowerCase();
        return profile.preferredNames.some(p => vName.includes(p));
      });
      if (!matched && jpVoices.length > 1) {
        if (speaker === 'mio') matched = jpVoices[1 % jpVoices.length];
        else if (speaker === 'kotone') matched = jpVoices[2 % jpVoices.length];
        else matched = jpVoices[0];
      }
      utter.voice = matched || jpVoices[0];
    }

    window.speechSynthesis.speak(utter);
  } catch (e) {
    console.warn('Fallback TTS error:', e);
    if (typeof onEndCallback === 'function') setTimeout(onEndCallback, 300);
  }
}

// Main High-Quality VOICEVOX Anime Speech Player
async function speakJapanese(text, speaker = 'gemini', customRate = null, onEndCallback = null) {
  const clean = cleanKotonohaTtsText(text);
  try {
    // Stop currently playing audio or speech
    if (currentKotonohaAudio) {
      try {
        currentKotonohaAudio.pause();
        currentKotonohaAudio.currentTime = 0;
      } catch (_) {}
      currentKotonohaAudio = null;
    }
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (_) {}
    }

    if (!clean && !(typeof text === 'string' && text.endsWith('.mp3'))) {
      if (typeof onEndCallback === 'function') setTimeout(onEndCallback, 300);
      return;
    }

    const cacheKey = getKotonohaCacheKey(text, speaker);
    const executeFallback = () => {
      speakJapaneseFallback(clean, speaker, customRate, onEndCallback);
    };

    // 1. Instant 0ms playback from preloaded Audio buffer or cache
    let audioUrl = kotonohaAudioCache[cacheKey];
    if (!audioUrl) {
      audioUrl = await synthesizeAndBufferVoicevox(text, speaker);
    }

    if (audioUrl) {
      try {
        const preloaded = kotonohaPreloadedAudio[cacheKey];
        const audio = preloaded || new Audio(audioUrl);
        audio.currentTime = 0;
        currentKotonohaAudio = audio;
        let finished = false;
        const done = () => {
          if (!finished) {
            finished = true;
            if (typeof onEndCallback === 'function') onEndCallback();
            // Fire any pending quiz-advance registered by quiz submit (survives replay interruptions)
            if (typeof pendingQuizAdvance === 'function') {
              const adv = pendingQuizAdvance;
              pendingQuizAdvance = null;
              adv();
            }
          }
        };
        audio.onended = done;
        audio.onerror = executeFallback;
        audio.play().catch(executeFallback);
        return;
      } catch (_) {
        executeFallback();
        return;
      }
    }

    executeFallback();
  } catch (err) {
    speakJapaneseFallback(clean, speaker, customRate, onEndCallback);
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
  const selLesson = all[idx];
  if (selLesson && selLesson.season) {
    kotonohaRuntime.selectedSeason = selLesson.season;
    state.kotonoha.selectedSeason = selLesson.season;
  }
  saveState(true);
  playBeep(620, 0.06);
  renderKotonohaView();
}

function switchKotonohaSeason(seasonNum) {
  initKotonohaState();
  kotonohaRuntime.selectedSeason = seasonNum;
  state.kotonoha.selectedSeason = seasonNum;
  const all = getAllKotonohaLessons();
  const curLesson = getCurrentKotonohaLesson();
  if (!curLesson || (curLesson.season || 1) !== seasonNum) {
    const targetIdx = all.findIndex(l => (l.season || 1) === seasonNum);
    if (targetIdx !== -1) {
      kotonohaRuntime.lessonIdx = targetIdx;
      state.kotonoha.activeLessonIdx = targetIdx;
    }
  }
  saveState(true);
  playBeep(640, 0.05);
  renderKotonohaView();
}

function openKotonohaHub() {
  kotonohaRuntime.ttsLoading.runId++;
  kotonohaRuntime.ttsLoading.active = false;
  kotonohaRuntime.currentMode = 'hub';
  playBeep(580, 0.06);
  renderKotonohaView();
}

// Short-toon manga navigation (legacy modes unreachable — feature abandoned for quality)
function openMangaList() {
  openKotonohaHub();
}

function openMangaRead(idx) {
  initKotonohaState();
  const all = getAllKotonohaLessons();
  if (idx < 0 || idx >= all.length) return;
  kotonohaRuntime.lessonIdx = idx;
  state.kotonoha.activeLessonIdx = idx;
  const selLesson = all[idx];
  if (selLesson && selLesson.season) {
    kotonohaRuntime.selectedSeason = selLesson.season;
    state.kotonoha.selectedSeason = selLesson.season;
  }
  saveState(true);
  playBeep(620, 0.06);
  kotonohaRuntime.currentMode = 'manga_read';
  renderKotonohaView();
}

function backToMangaList() {
  openKotonohaHub();
}

function openNextMangaEp() {
  const next = kotonohaRuntime.lessonIdx + 1;
  const all = getAllKotonohaLessons();
  if (next < all.length) { openMangaRead(next); return; }
  openKotonohaHub();
}

function skipKotonohaTtsPreload() {
  kotonohaRuntime.ttsLoading.runId++;
  kotonohaRuntime.ttsLoading.active = false;
  const targetMode = kotonohaRuntime.ttsLoading.targetMode || 'story';
  if (targetMode === 'season') {
    openKotonohaHub();
    return;
  }
  if (targetMode === 'quiz') {
    launchKotonohaQuizImmediate();
  } else {
    launchKotonohaStoryImmediate();
  }
}

function launchKotonohaStoryImmediate() {
  kotonohaRuntime.currentMode = 'story';
  kotonohaRuntime.storyStepIdx = 0;
  playBeep(720, 0.08);
  renderKotonohaView();

  const lesson = getCurrentKotonohaLesson();
  if (lesson && lesson.story && lesson.story[0]) {
    setTimeout(() => speakJapanese(lesson.story[0].audio || lesson.story[0].jpPlain || lesson.story[0].jpRuby, lesson.story[0].speaker || 'gemini'), 150);
  }
}


// ============================================================================
// QUIZ HINT & PRONUNCIATION TOGGLE HELPERS
// ============================================================================
function parseKotonohaOptionText(opt) {
  if (typeof opt !== 'string') return { main: opt, pron: '', hasPron: false };
  const match = opt.match(/^([^(（]+)[\s]*[(（]([^)）]+)[)）]$/);
  if (match) {
    return {
      main: match[1].trim(),
      pron: match[2].trim(),
      hasPron: true
    };
  }
  return {
    main: opt,
    pron: '',
    hasPron: false
  };
}

function toggleKotonohaQuizHint(qIdx) {
  if (!kotonohaRuntime.revealedHints) kotonohaRuntime.revealedHints = {};
  kotonohaRuntime.revealedHints[qIdx] = !kotonohaRuntime.revealedHints[qIdx];
  playBeep(650, 0.05);
  renderKotonohaView();
}

function toggleKotonohaOptionPron() {
  kotonohaRuntime.showOptionPron = !kotonohaRuntime.showOptionPron;
  playBeep(680, 0.05);
  renderKotonohaView();
}

function toggleSingleOptionPron(idx, event) {
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }
  if (!kotonohaRuntime.revealedOptionPron) kotonohaRuntime.revealedOptionPron = {};
  const key = `${kotonohaRuntime.quizIdx}_${idx}`;
  kotonohaRuntime.revealedOptionPron[key] = !kotonohaRuntime.revealedOptionPron[key];
  playBeep(720, 0.04);
  renderKotonohaView();
}

function launchKotonohaQuizImmediate() {
  const lesson = getCurrentKotonohaLesson();
  if (!lesson || !lesson.quizzes || lesson.quizzes.length === 0) return;
  kotonohaRuntime.currentMode = 'quiz';
  kotonohaRuntime.quizIdx = 0;
  kotonohaRuntime.quizAnswered = false;
  kotonohaRuntime.quizChatMessages = [];
  kotonohaRuntime.revealedHints = {};
  kotonohaRuntime.revealedOptionPron = {};

  pushQuizQuestionToChat(0);
  playBeep(760, 0.08);
  renderKotonohaView();
}

// Pre-synthesize & buffer ALL Story + Quiz voices for the lesson with a live 0%~100% progress bar!
async function prepareAndStartKotonoha(targetMode = 'story', lessonIdx = undefined) {
  initKotonohaState();
  if (typeof lessonIdx === 'number') {
    kotonohaRuntime.lessonIdx = lessonIdx;
    state.kotonoha.activeLessonIdx = lessonIdx;
  }

  const lesson = getCurrentKotonohaLesson();
  if (!lesson) return;

  const items = collectLessonVoiceItems(lesson);
  const uncached = items.filter(it => !(kotonohaAudioCache[it.key] && kotonohaPreloadedAudio[it.key]));

  // If 100% of Story + Quiz voices are already ready in memory, start immediately!
  if (uncached.length === 0) {
    if (targetMode === 'quiz') {
      launchKotonohaQuizImmediate();
    } else {
      launchKotonohaStoryImmediate();
    }
    return;
  }

  const myRunId = ++kotonohaRuntime.ttsLoading.runId;
  kotonohaRuntime.currentMode = 'loading_tts';
  kotonohaRuntime.ttsLoading = {
    active: true,
    done: items.length - uncached.length,
    total: items.length,
    percent: Math.round(((items.length - uncached.length) / items.length) * 100),
    currentSpeaker: uncached[0]?.speaker || 'gemini',
    currentText: uncached[0]?.label || '보이스 준비 중...',
    targetMode: targetMode,
    runId: myRunId
  };
  playBeep(660, 0.06);
  renderKotonohaView();

  for (let i = 0; i < items.length; i++) {
    if (kotonohaRuntime.ttsLoading.runId !== myRunId) return;
    const it = items[i];
    if (!(kotonohaAudioCache[it.key] && kotonohaPreloadedAudio[it.key])) {
      kotonohaRuntime.ttsLoading.currentSpeaker = it.speaker;
      kotonohaRuntime.ttsLoading.currentText = it.label;
      updateKotonohaLoadingDom();
      await synthesizeAndBufferVoicevox(it.rawText, it.speaker);
    }
    if (kotonohaRuntime.ttsLoading.runId !== myRunId) return;
    kotonohaRuntime.ttsLoading.done = i + 1;
    kotonohaRuntime.ttsLoading.percent = Math.min(100, Math.round(((i + 1) / items.length) * 100));
    updateKotonohaLoadingDom();
  }

  if (kotonohaRuntime.ttsLoading.runId !== myRunId) return;
  kotonohaRuntime.ttsLoading.active = false;
  await sleepMs(220);

  if (targetMode === 'season') {
    openKotonohaHub();
    return;
  }
  if (targetMode === 'quiz') {
    launchKotonohaQuizImmediate();
  } else {
    launchKotonohaStoryImmediate();
  }
}

// Season-wide bulk voice pre-download: ALL lessons' Story + Quiz voices at once
// (deduped by cache key) so every episode in the season starts instantly.
// Returns to hub when done (no episode launch).
async function prepareAndStartSeasonAudio(seasonNum) {
  initKotonohaState();
  kotonohaRuntime.selectedSeason = seasonNum;
  state.kotonoha.selectedSeason = seasonNum;
  saveState(true);
  const lessons = getAllKotonohaLessons().filter(l => (l.season || 1) === seasonNum);
  if (!lessons.length) return;

  const seen = new Set();
  const items = [];
  for (const lesson of lessons) {
    for (const it of collectLessonVoiceItems(lesson)) {
      if (seen.has(it.key)) continue;
      seen.add(it.key);
      items.push({ ...it, label: `S${seasonNum} ${lesson.epCode || ''} ${it.label}` });
    }
  }
  if (!items.length) return;
  const uncached = items.filter(it => !(kotonohaAudioCache[it.key] && kotonohaPreloadedAudio[it.key]));
  const doneAlready = items.length - uncached.length;

  if (uncached.length === 0) {
    showFloatingToast(`시즌 ${seasonNum} 음성 전부 준비 완료!`, '✅');
    openKotonohaHub();
    return;
  }

  const targetMode = 'season';
  const myRunId = ++kotonohaRuntime.ttsLoading.runId;
  kotonohaRuntime.currentMode = 'loading_tts';
  kotonohaRuntime.ttsLoading = {
    active: true,
    done: doneAlready,
    total: items.length,
    percent: Math.round((doneAlready / items.length) * 100),
    currentSpeaker: uncached[0]?.speaker || 'gemini',
    currentText: uncached[0]?.label || '보이스 준비 중...',
    targetMode: targetMode,
    runId: myRunId
  };
  playBeep(660, 0.06);
  renderKotonohaView();

  for (let i = 0; i < items.length; i++) {
    if (kotonohaRuntime.ttsLoading.runId !== myRunId) return;
    const it = items[i];
    if (!(kotonohaAudioCache[it.key] && kotonohaPreloadedAudio[it.key])) {
      kotonohaRuntime.ttsLoading.currentSpeaker = it.speaker;
      kotonohaRuntime.ttsLoading.currentText = it.label;
      updateKotonohaLoadingDom();
      await synthesizeAndBufferVoicevox(it.rawText, it.speaker);
    }
    if (kotonohaRuntime.ttsLoading.runId !== myRunId) return;
    kotonohaRuntime.ttsLoading.done = i + 1;
    kotonohaRuntime.ttsLoading.percent = Math.min(100, Math.round(((i + 1) / items.length) * 100));
    updateKotonohaLoadingDom();
  }

  if (kotonohaRuntime.ttsLoading.runId !== myRunId) return;
  kotonohaRuntime.ttsLoading.active = false;
  await sleepMs(220);
  showFloatingToast(`시즌 ${seasonNum} 전체 음성 다운로드 완료 (${items.length}개 대사)`, '🎙️');
  openKotonohaHub();
}

function isSeasonFullyCached(seasonNum) {
  const lessons = getAllKotonohaLessons().filter(l => (l.season || 1) === seasonNum);
  const seen = new Set();
  for (const lesson of lessons) {
    for (const it of collectLessonVoiceItems(lesson)) {
      if (seen.has(it.key)) continue;
      seen.add(it.key);
      if (!(kotonohaAudioCache[it.key] && kotonohaPreloadedAudio[it.key])) return false;
    }
  }
  return true;
}

function updateKotonohaLoadingDom() {
  const pctEl = document.getElementById('kotonohaTtsPctText');
  const barEl = document.getElementById('kotonohaTtsPctBar');
  const cntEl = document.getElementById('kotonohaTtsCountText');
  const lblEl = document.getElementById('kotonohaTtsLabelText');
  if (pctEl) pctEl.textContent = `${kotonohaRuntime.ttsLoading.percent}%`;
  if (barEl) barEl.style.width = `${kotonohaRuntime.ttsLoading.percent}%`;
  if (cntEl) cntEl.textContent = `${kotonohaRuntime.ttsLoading.done} / ${kotonohaRuntime.ttsLoading.total} 대사 완료`;
  if (lblEl) lblEl.textContent = kotonohaRuntime.ttsLoading.currentText;
}

function startKotonohaStory(lessonIdx) {
  prepareAndStartKotonoha('story', lessonIdx);
}

function stepKotonohaStory(delta) {
  const lesson = getCurrentKotonohaLesson();
  if (!lesson || !lesson.story) return;
  const nextIdx = kotonohaRuntime.storyStepIdx + delta;
  if (nextIdx < 0) return;
  if (nextIdx >= lesson.story.length) {
    // Transition directly to Daily Chat Quiz (already 100% preloaded!)
    launchKotonohaQuizImmediate();
    return;
  }
  kotonohaRuntime.storyStepIdx = nextIdx;
  playBeep(640, 0.06);
  renderKotonohaView();
  const step = lesson.story[nextIdx];
  if (step) {
    speakJapanese(step.audio || step.jpPlain || step.jpRuby, step.speaker || 'gemini');
  }
}

function startKotonohaQuiz() {
  prepareAndStartKotonoha('quiz');
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
    speakJapanese(q.targetWord || q.promptJp, 'gemini');
    scrollKotonohaQuizBottom();
  }, 450);
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

  if (!state.kotonoha.quizStats) {
    state.kotonoha.quizStats = { total: 0, correct: 0, wrongWords: [] };
  }
  state.kotonoha.quizStats.total = (state.kotonoha.quizStats.total || 0) + 1;

  if (isCorrect) {
    state.kotonoha.quizStats.correct = (state.kotonoha.quizStats.correct || 0) + 1;
    playBeep(880, 0.1);
    state.kotonoha.coins = (state.kotonoha.coins || 655) + 15;
    state.kotonoha.kotodama = (state.kotonoha.kotodama || 65) + 10;
    addBondExp(10);
  } else {
    playBeep(360, 0.14);
    state.kotonoha.coins = (state.kotonoha.coins || 655) + 5;
    state.kotonoha.kotodama = (state.kotonoha.kotodama || 65) + 2;
    if (q.targetWord) {
      if (!state.kotonoha.quizStats.wrongWords) state.kotonoha.quizStats.wrongWords = [];
      if (!state.kotonoha.quizStats.wrongWords.includes(q.targetWord)) {
        state.kotonoha.quizStats.wrongWords.push(q.targetWord);
      }
    }
  }
  saveState(true);

  // 2. Gemini reaction bubble + Green explanation card
  const reactJp = isCorrect
    ? (q.geminiReactJp || "<ruby>正解<rt>せいかい</rt></ruby>どす！")
    : "おしい！もう<ruby>一度<rt>いちど</rt></ruby><ruby>確認<rt>かくにん</rt></ruby>しましょね🌸";
  const reactPron = isCorrect
    ? (q.geminiReactPron || "세이카이 도스!")
    : "오시-! 모- 이치도 카쿠닌 시마쇼네";
  const reactKo = isCorrect
    ? (q.geminiReactKo || "정답이옵니다!")
    : `아까워라! 정답은 「${q.options[q.answerIndex]}」이라지요.`;

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
  // 음성 피드백 완료 후 여유 있게 다음 문제로 진행하는 안전 콜백
  let hasAdvanced = false;
  const proceedToNextStep = () => {
    if (hasAdvanced) return;
    hasAdvanced = true;
    if (pendingQuizAdvance === proceedToNextStep) pendingQuizAdvance = null;

    // 음성이 완전히 끝난 후, 정답 리액션과 해설(녹색 박스)을 충분히 읽을 수 있도록 1.4초 여유 대기
    setTimeout(() => {
      if (kotonohaRuntime.currentMode !== 'quiz') return;
      if (qIdx + 1 < lesson.quizzes.length) {
        kotonohaRuntime.quizIdx = qIdx + 1;
        kotonohaRuntime.quizAnswered = false;
        pushQuizQuestionToChat(qIdx + 1);
        renderKotonohaView();
        scrollKotonohaQuizBottom();
      } else {
        // 모든 퀴즈 완료!
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
    }, 1400);
  };

  // QUIZ-ADVANCE BINDING: registered in module scope so replay clicks ('다시 듣기')
  // never trap the flow — whether speech ends/cancelled, the advance still fires.
  pendingQuizAdvance = proceedToNextStep;
  // Watchdog: if TTS errors/cancel swallow callbacks, advance after 12s anyway.
  setTimeout(() => {
    if (pendingQuizAdvance === proceedToNextStep) {
      pendingQuizAdvance = null;
      proceedToNextStep();
    }
  }, 12000);

  // 리액션 음성 재생 (음성이 완전히 끝난 후 proceedToNextStep 호출)
  speakJapanese(reactJp, 'gemini', null, proceedToNextStep);
}

// Generate a brand-new Kansai/Kyoto Daily Lesson using Gemini AI!
async function generateAiKotonohaLesson() {
  initKotonohaState();
  const apiKey = (localStorage.getItem('GEMINI_API_KEY') || '').trim();
  if (!apiKey) {
    alert("✨ 실시간 AI 새 수업 생성을 위해 우측 상단 [⚙️ 설정]에서 Gemini API 키를 먼저 등록해 주세요!\n(기본 내장 수업 1~12화는 API 키 없이도 언제든 플레이 가능합니다 🍵)");
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
중요 번역 규칙: 제미니의 한국어 대사("ko" 필드)를 번역할 때는 전라도/경상도 등 한국 지역 사투리로 직역하지 말고, 반드시 서브컬쳐 교토 아가씨(코바야카와 사에) 로컬라이징 말투('~사와요', '~시와요', '~사옵니다', '~하옵니다', '~라지요', '~하시어요', '어머나', '우후후', '소녀')를 사용해 우아하고 고풍스럽게 번역해!
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
      "geminiReactKo": "정답이옵니다!"
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

// ============================================================================
// VISUAL NOVEL HYBRID VISUAL RESOLVER (Seamless SCG + BG & Full ECG Fallback)
// ============================================================================
function resolveKotonohaVisuals(step, lesson, stepIdx = -1, prevSceneImg = '') {
  // 1. Adaptive mixing: ECG for impactful beats (emotion peaks / cinematic scenes),
  //    SCG for calm beats. Deterministic so the mix is stable across sessions.
  if (step.sceneImg) {
    const sceneLower = (step.sceneImg || '').toLowerCase();
    const prevLower = (prevSceneImg || '').toLowerCase();
    const cinematic = /(night|rooftop|sunset|splash|pool|secret|ikezu|blush|extreme|massive|fireworks|beach|winter|osaka|takoyaki|yukata|ryokan|onsen|lantern)/.test(sceneLower);
    const emotionalExpr = ['shock', 'dark', 'cry', 'love', 'sleepy', 'smirk', 'angry'].includes(step.expr || '');
    const sceneChange = prevLower && prevLower !== sceneLower;
    const every3rd = stepIdx >= 0 && (stepIdx % 3 === 0);
    if (emotionalExpr || cinematic || sceneChange || every3rd) {
      return {
        isScg: false,
        ecgUrl: step.sceneImg,
        ecgFallback: './image/03 gemini/gemini_26_kyoto_teahouse.png'
      };
    }
  }
  // 2. If step explicitly specifies SCG expression (e.g. expr: 'shy', 'smile', 'angry')
  if (step.expr && step.speaker) {
    const outfit = step.outfit || 'default';
    const scgPath = step.scg || ('./image/scg/' + step.speaker + '/' + step.speaker + '_' + outfit + '_' + step.expr + '.png');
    const bgPath = step.bg ? (step.bg.startsWith('./') ? step.bg : ('./image/bg/bg_' + step.bg + '.png')) : (lesson.bgImage || './image/03 gemini/gemini_26_kyoto_teahouse.png');
    // Per-speaker ECG fallback when the transparent SCG asset is missing (v4.3.10)
    const ecgFallbackMap = {
      gemini: './image/03 gemini/gemini_26_kyoto_teahouse.png',
      kotone: './image/02 kotone/kotone_03_cafe_date.png',
      mio: './image/01 mio/mio_01_main.png'
    };
    const ecgFallback = step.sceneImg || lesson.bgImage || ecgFallbackMap[step.speaker] || './image/03 gemini/gemini_26_kyoto_teahouse.png';
    return {
      isScg: true,
      speaker: step.speaker,
      scgUrl: scgPath,
      bgUrl: bgPath,
      ecgFallback: ecgFallback
    };
  }

  // 2. Default Clean Full-Illustration ECG Presentation
  const ecgUrl = step.sceneImg || lesson.bgImage || './image/03 gemini/gemini_26_kyoto_teahouse.png';
  return {
    isScg: false,
    ecgUrl: ecgUrl,
    ecgFallback: './image/03 gemini/gemini_26_kyoto_teahouse.png'
  };
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

  // MODE 0: BATCH VOICEVOX PRE-SYNTHESIS LOADER (0% ~ 100% Real-time Progress)
  if (kotonohaRuntime.currentMode === 'loading_tts') {
    const tl = kotonohaRuntime.ttsLoading;
    const spkAvatar = tl.currentSpeaker === 'kotone'
      ? './image/02 kotone/avatar_kotone.png'
      : tl.currentSpeaker === 'mio'
        ? './image/01 mio/avatar_mio.png'
        : './image/03 gemini/avatar_gemini.png';

    container.innerHTML = `
      <div class="rounded-3xl bg-[#181316] text-[#f5ebe6] border border-[#452e38] shadow-2xl overflow-hidden p-6 sm:p-8">
        <div class="max-w-md mx-auto text-center space-y-5">
          <!-- Animated Avatar & Soundwave Ring -->
          <div class="relative w-24 h-24 mx-auto">
            <div class="absolute inset-0 rounded-full bg-[#e0465a]/30 animate-ping"></div>
            <img src="${spkAvatar}" class="relative z-10 w-24 h-24 rounded-full object-cover ring-4 ring-[#e0465a] shadow-xl mx-auto">
            <span class="absolute -bottom-1 -right-1 z-20 px-2 py-0.5 rounded-full bg-[#e0465a] text-white text-[10px] font-black shadow">
              VOICEVOX
            </span>
          </div>

          <div class="space-y-1.5">
            <div class="text-xs font-extrabold text-[#f28b9b] tracking-wide">${lesson.dateLabel} · ${lesson.titleKo}</div>
            <h3 class="text-lg font-black text-white">🎙️ 레슨~퀴즈 성우 보이스 일괄 준비 중...</h3>
            <p class="text-xs text-[#b89d97] leading-relaxed">
              중간에 기본 기계음으로 바뀌지 않도록, 이번 화의 <strong class="text-[#ffd6de]">모든 스토리 대사와 퀴즈 보이스</strong>를 한꺼번에 준비하고 있사옵니다 🍵
            </p>
          </div>

          <!-- Big Percentage Counter & Smooth Progress Bar -->
          <div class="p-4 rounded-2xl bg-[#23191e] border border-[#3f2b34] space-y-2.5">
            <div class="flex items-baseline justify-between">
              <span id="kotonohaTtsLabelText" class="text-xs font-bold text-[#f2a6b2] truncate">${tl.currentText}</span>
              <span id="kotonohaTtsPctText" class="text-2xl font-black text-[#ff6b81] font-mono">${tl.percent}%</span>
            </div>
            <div class="w-full h-3 rounded-full bg-[#150f12] overflow-hidden border border-[#38252d]">
              <div id="kotonohaTtsPctBar" class="h-full bg-gradient-to-r from-[#e0465a] via-[#ff758c] to-[#ffb199] transition-all duration-300 rounded-full" style="width: ${tl.percent}%"></div>
            </div>
            <div class="flex items-center justify-between text-[11px] text-[#9e847e] font-bold">
              <span id="kotonohaTtsCountText">${tl.done} / ${tl.total} 대사 완료</span>
              <span>100% 도달 시 자동 시작 🌸</span>
            </div>
          </div>

          <div class="flex items-center justify-center gap-2 pt-1">
            <button onclick="openKotonohaHub()" class="px-4 py-2 rounded-xl bg-[#261c21] hover:bg-[#34262d] border border-[#422f37] text-xs font-bold text-[#c9b1aa]">
              취소하고 로비로
            </button>
            <button onclick="skipKotonohaTtsPreload()" class="px-4 py-2 rounded-xl bg-[#35222a] hover:bg-[#472d38] border border-[#633d4c] text-xs font-bold text-[#f5d0d8]">
              ⚡ 대기 없이 바로 시작
            </button>
          </div>
        </div>
      </div>
    `;
    return;
  }

  // MODE 1: TEAROOM HUB (Optimized: Full Character Visibility + Vertical Curriculum List + Season 1/2)
  if (kotonohaRuntime.currentMode === 'hub') {
    const unreadCount = Math.max(1, lessons.length - (kState.completedLessons?.length || 0));
    const isCurrentCached = isLessonVoiceFullyCached(lesson);
    const activeSeason = kotonohaRuntime.selectedSeason || lesson.season || 1;
    
    // Filter lessons by active season (custom AI lessons default to season 2 or active season)
    const seasonLessons = lessons.map((item, idx) => ({ ...item, globalIdx: idx }))
      .filter(item => (item.season || 1) === activeSeason);

    container.innerHTML = `
      <div class="rounded-3xl bg-[#181316] text-[#f5ebe6] border border-[#3a2830] shadow-2xl overflow-hidden">
        <!-- Top Header Bar: Profile, Title, Streak & Currencies -->
        <div class="p-3.5 sm:p-4 pb-2.5 bg-gradient-to-b from-[#241a1f] to-[#181316] border-b border-[#332228]">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5 sm:gap-3">
              <div class="relative shrink-0 cursor-pointer" onclick="startKotonohaStory()">
                <img src="./image/03 gemini/avatar_gemini.png" class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl object-cover ring-2 ring-[#d9536f] shadow-md">
                <span class="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-[#e0465a] text-white text-[10px] font-black flex items-center justify-center shadow">${unreadCount}</span>
              </div>
              <div>
                <div class="flex items-center gap-1.5">
                  <h2 class="text-sm sm:text-base font-black text-[#e86b7e] tracking-tight">言の葉茶屋</h2>
                  <span class="text-[9px] sm:text-[10px] px-2 py-0.5 rounded-full bg-[#352329] text-[#f2a6b2] font-bold border border-[#52343d]">코토노하 다실</span>
                </div>
                <p class="text-[11px] sm:text-xs text-[#b59e99] font-bold mt-0.5">${rank.title}</p>
              </div>
            </div>

            <div class="flex items-center gap-1.5">
              <button onclick="toggleKotonohaPronunciation()" class="px-2.5 py-1 rounded-full border text-xs font-black transition-all ${showPron ? 'bg-[#e0465a] text-white border-[#ff7588]' : 'bg-[#2a1f24] text-[#9c847f] border-[#453139]'}" title="발음/후리가나 표시 전환">
                Aa
              </button>
            </div>
          </div>

          <!-- Currency & Streak Pills -->
          <div class="flex flex-wrap items-center gap-1.5 sm:gap-2 mt-2.5">
            <div class="px-2.5 py-0.5 rounded-full bg-[#251c20] border border-[#3d2c33] flex items-center gap-1 text-[11px] font-extrabold">
              <span class="text-amber-400">🪙</span>
              <span>${kState.coins || 655}</span>
            </div>
            <div class="px-2.5 py-0.5 rounded-full bg-[#251c20] border border-[#3d2c33] flex items-center gap-1 text-[11px] font-extrabold">
              <span class="text-[#f28b9b]">言霊</span>
              <span>${kState.kotodama || 65}</span>
            </div>
            <div class="px-2.5 py-0.5 rounded-full bg-[#251c20] border border-[#3d2c33] flex items-center gap-1 text-[11px] font-extrabold">
              <span>🔥 연속 ${kState.streak || 1}일</span>
            </div>
            <button onclick="openMangaList()" class="ml-auto px-2.5 py-0.5 rounded-full bg-gradient-to-r from-[#2d4038] to-[#1c2a26] hover:opacity-95 border border-[#4a6a5c] text-[11px] font-black text-[#d8f5e8] flex items-center gap-1 shadow transition-all active:scale-95">
              📖 미니툰
            </button>
          </div>
        </div>

        <!-- Main Banner: Optimized for 100% Character Visibility (No Obtrusive Overlays on Face/Body) -->
        <div class="relative p-3 sm:p-4 bg-gradient-to-b from-[#181316] via-[#22171c] to-[#181316]">
          <div class="relative rounded-2xl overflow-hidden border border-[#422c35] shadow-lg group cursor-pointer" onclick="startKotonohaStory()">
            <!-- Clean Image with focus on upper body/face -->
            <img src="${lesson.bgImage || './image/03 gemini/gemini_02_matcha.png'}" class="w-full h-52 sm:h-60 object-cover object-[center_12%] brightness-95 group-hover:scale-102 transition-all duration-500">
            <!-- Subtle edge vignetting without blocking the character -->
            <div class="absolute inset-0 bg-gradient-to-t from-[#181316] via-transparent to-black/25"></div>

            <!-- Top Left Floating Badges -->
            <div class="absolute top-2.5 left-2.5 flex flex-wrap gap-1.5 z-10">
              <span class="px-2.5 py-1 rounded-full bg-[#e0465a] text-white text-[10px] sm:text-[11px] font-black shadow-md animate-bounce">
                새 톡 ${unreadCount} · ${lesson.levelBadge.split('+')[0]}
              </span>
              <button onclick="event.stopPropagation(); speakJapanese('プロデューサーはん、おいでやす。今日もおきばりやす！', 'gemini')" class="px-2.5 py-1 rounded-full bg-black/65 hover:bg-black/85 text-[#ffd6de] border border-white/20 text-[10px] sm:text-[11px] font-bold backdrop-blur-xs">
                🔊 제미니 인사
              </button>
            </div>

            <!-- Top Right Heroine Cast Avatars -->
            <div class="absolute top-2.5 right-2.5 flex items-center -space-x-2 z-10">
              <img src="./image/03 gemini/avatar_gemini.png" class="w-7 h-7 sm:w-8 sm:h-8 rounded-full ring-2 ring-[#e0465a] object-cover" title="제미니 (교토·오사카벤 사범)">
              <img src="./image/02 kotone/avatar_kotone.png" class="w-7 h-7 sm:w-8 sm:h-8 rounded-full ring-2 ring-amber-400 object-cover" title="코토네 (자본주의 조교)">
              <img src="./image/01 mio/avatar_mio.png" class="w-7 h-7 sm:w-8 sm:h-8 rounded-full ring-2 ring-sky-400 object-cover" title="미오 (에너제틱 동급생)">
            </div>

            <!-- Bottom Sub-Strip (Clean Title Preview attached underneath image bottom) -->
            <div class="absolute bottom-0 inset-x-0 p-2.5 bg-gradient-to-t from-[#140e11] via-[#1a1216]/90 to-transparent flex items-center justify-between">
              <div class="min-w-0 pr-2">
                <div class="text-[9px] sm:text-[10px] font-bold text-[#f28b9b] flex items-center gap-1.5">
                  <span>시즌 ${lesson.season || 1} · 제${lesson.epCode || (lesson.dayNum ? '1-' + lesson.dayNum : '1-1')}화</span>
                  <span class="text-[#ffd6de] opacity-80">· 3인 극장</span>
                </div>
                <div class="text-xs sm:text-sm font-black text-white truncate">${lesson.titleJp}</div>
                ${showPron ? `<div class="text-[10px] sm:text-[11px] text-[#d4b5b0] truncate mt-0.5">${lesson.titlePron} · <span class="text-[#ffd0d9] font-bold">${lesson.titleKo}</span></div>` : `<div class="text-[11px] text-[#d4b5b0] truncate mt-0.5">${lesson.titleKo}</div>`}
              </div>
              <span class="shrink-0 px-2.5 py-1 rounded-xl bg-[#e0465a]/90 text-white text-[11px] font-black shadow group-hover:scale-105 transition-transform flex items-center gap-1">
                <span>감상</span><span>▶</span>
              </span>
            </div>
          </div>

          <!-- Grammar / Kansai Dialect Note Box (Compact Textbook style) -->
          ${lesson.grammarTip ? `
          <div class="mt-2.5 p-3 rounded-2xl bg-[#24191e] border border-[#47303a] space-y-1">
            <div class="text-xs font-black text-[#f4869d] flex items-center justify-between">
              <span>${lesson.grammarTip.title}</span>
              <span class="text-[10px] text-[#a88d89]">교재 요약</span>
            </div>
            <p class="text-xs text-[#e2cfc9] leading-relaxed">${lesson.grammarTip.content}</p>
          </div>
          ` : ''}

          <!-- Season Selector Tabs + Vertical Curriculum List -->
          <div class="mt-3 space-y-2">
            <!-- Header with AI Button -->
            <div class="flex items-center justify-between">
              <span class="text-xs font-black text-[#d9c3bd]">📚 커리큘럼 선택 (세로 목록)</span>
              <div class="flex items-center gap-1.5">
                ${isSeasonFullyCached(activeSeason) ? `
                  <span class="px-2 py-1 rounded-lg bg-emerald-500/15 border border-emerald-400/40 text-emerald-300 text-[10px] font-black flex items-center gap-1">🎙️ 시즌 ${activeSeason} 음성 준비완료</span>
                ` : `
                  <button onclick="prepareAndStartSeasonAudio(${activeSeason})" class="px-2.5 py-1 rounded-xl bg-[#1d2f2a] hover:bg-[#263d34] border border-[#3a5a4e] text-[#a8e6cc] text-[11px] font-black shadow transition-all active:scale-95">
                    🎙️ 시즌 ${activeSeason} 전체 음성 다운로드
                  </button>
                `}
                <button onclick="generateAiKotonohaLesson()" class="px-2.5 py-1 rounded-xl bg-gradient-to-r from-[#d94862] to-[#9b4dca] text-white text-[11px] font-black shadow hover:opacity-95 active:scale-95 transition-all">
                  ${kotonohaRuntime.isAiGenerating ? '⏳ AI 집필 중...' : '✨ AI 새 에피소드'}
                </button>
              </div>
            </div>

            <!-- Season Switcher Tabs (Season 1 vs Season 2) -->
            <div class="grid grid-cols-2 gap-2">
              <button onclick="switchKotonohaSeason(1)" class="p-2 rounded-xl border text-center transition-all ${activeSeason === 1 ? 'bg-[#3e242f] border-[#e0465a] text-white shadow-md font-black ring-1 ring-[#e0465a]/60' : 'bg-[#21181c] border-[#38282f] text-[#a8908b] hover:text-white'}">
                <div class="text-[11px] font-black flex items-center justify-center gap-1">
                  <span>🍵 시즌 1</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded-full bg-[#2e1d23] text-[#f28b9b]">1-1 ~ 1-12</span>
                </div>
                <div class="text-[10px] opacity-80 mt-0.5">교토 다실 & 기초 생활</div>
              </button>

              <button onclick="switchKotonohaSeason(2)" class="p-2 rounded-xl border text-center transition-all ${activeSeason === 2 ? 'bg-[#3e242f] border-[#e0465a] text-white shadow-md font-black ring-1 ring-[#e0465a]/60' : 'bg-[#21181c] border-[#38282f] text-[#a8908b] hover:text-white'}">
                <div class="text-[11px] font-black flex items-center justify-center gap-1">
                  <span>🌸 시즌 2</span>
                  <span class="text-[9px] px-1.5 py-0.2 rounded-full bg-[#401f29] text-[#ff758c]">2-1 ~ 2-6 신설</span>
                </div>
                <div class="text-[10px] opacity-80 mt-0.5">칸사이 만유 & 피트니스</div>
              </button>
            </div>

            <!-- Vertical Scrollable Episode List (Clear, readable and fits comfortably in phone viewport) -->
            <div class="flex flex-col gap-1.5 max-h-44 sm:max-h-52 overflow-y-auto clean-scroll pr-1">
              ${seasonLessons.map(item => {
                const isDone = (kState.completedLessons || []).includes(item.id);
                const isActive = item.globalIdx === kotonohaRuntime.lessonIdx;
                const epBadge = item.epCode || (item.season ? item.season + '-' + (item.episode || (item.dayNum || 1)) : '1-' + item.dayNum);
                return `
                  <button onclick="selectKotonohaLesson(${item.globalIdx})" class="w-full p-2 sm:p-2.5 rounded-xl border text-left transition-all flex items-center justify-between group ${isActive ? 'bg-[#3b232c] border-[#e0465a] text-white shadow-md ring-1 ring-[#e0465a]/50' : 'bg-[#20181c] border-[#34262c] text-[#ab948f] hover:border-[#5e3846] hover:bg-[#281c22]'}">
                    <div class="flex items-center gap-2.5 min-w-0">
                      <span class="px-2 py-0.5 rounded-lg text-[10px] font-black shrink-0 ${isActive ? 'bg-[#e0465a] text-white shadow' : 'bg-[#2b1c22] text-[#f28b9b] border border-[#482e37]'}">
                        ${isDone ? '✅ ' : '🍵 '}${epBadge}
                      </span>
                      <div class="min-w-0">
                        <div class="text-xs font-bold ${isActive ? 'text-white' : 'text-[#e6d6d2]'} truncate">${item.titleKo}</div>
                        <div class="text-[10px] text-[#9c847f] truncate mt-0.5">${item.titleJp.replace(/<[^>]+>/g, '')}</div>
                      </div>
                    </div>
                    <div class="flex items-center gap-2 shrink-0 pl-2">
                      <span class="text-[9px] px-1.5 py-0.5 rounded bg-[#2b1d22] text-[#d4b0a8] border border-[#452e37]">${item.levelBadge.split('+')[0]}</span>
                      <span class="text-xs font-black ${isActive ? 'text-[#ff6b81]' : 'text-[#6a5450] group-hover:text-[#ab948f]'}">›</span>
                    </div>
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Bottom Action Buttons: Full Voice Story & Instant Daily Quiz -->
          <div class="mt-3.5 grid grid-cols-1 sm:grid-cols-2 gap-2">
            <button onclick="startKotonohaStory()" class="w-full p-2.5 sm:p-3 rounded-2xl bg-[#291d22] hover:bg-[#34242b] border border-[#523540] flex items-center justify-between transition-all shadow-md group">
              <div class="flex items-center gap-2.5 sm:gap-3 text-left min-w-0">
                <img src="./image/03 gemini/avatar_gemini.png" class="w-9 h-9 sm:w-10 sm:h-10 rounded-full object-cover ring-2 ring-[#e0465a] shrink-0">
                <div class="min-w-0">
                  <div class="text-[10px] font-bold text-[#c7aca5] truncate">ジェミニ (제미니) · ${isCurrentCached ? '⚡ 보이스 준비완료' : '🎙️ 풀보이스 자동합성'}</div>
                  <div class="text-xs font-black text-white truncate">오늘 수업 준비됐어! 이야기 보기</div>
                </div>
              </div>
              <span class="text-[#e0465a] text-sm font-black group-hover:translate-x-1 transition-transform pl-1 shrink-0">▶</span>
            </button>

            <button onclick="startKotonohaQuiz()" class="w-full p-2.5 sm:p-3 rounded-2xl bg-gradient-to-r from-[#632230] to-[#451a24] hover:opacity-95 border border-[#8f3548] flex items-center justify-between transition-all shadow-md group">
              <div class="flex items-center gap-2.5 text-left min-w-0">
                <span class="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-[#e0465a]/25 border border-[#e0465a] flex items-center justify-center text-sm shrink-0">🎯</span>
                <div class="min-w-0">
                  <div class="text-[10px] font-bold text-[#f7b2be] truncate">채팅형 4지선다 테스트</div>
                  <div class="text-xs font-black text-white truncate">데일리 퀴즈 바로 풀기 (${lesson.quizzes.length}문항)</div>
                </div>
              </div>
              <span class="text-[#ff8da1] text-sm font-black group-hover:translate-x-1 transition-transform pl-1 shrink-0">▶</span>
            </button>
          </div>
        </div>
      </div>
    `;
    return;
  }

  // MODE 2: VISUAL NOVEL STORY READER (Clean Full-Illustration ECG Presentation)
  if (kotonohaRuntime.currentMode === 'story') {
    const steps = lesson.story || [];
    const curIdx = Math.min(kotonohaRuntime.storyStepIdx, steps.length - 1);
    const step = steps[curIdx] || steps[0];
    const progressPct = Math.round(((curIdx + 1) / steps.length) * 100);
    const prevStep = curIdx > 0 ? steps[curIdx - 1] : null;
    const visuals = resolveKotonohaVisuals(step, lesson, curIdx, prevStep ? (prevStep.sceneImg || '') : '');
    const sceneImage = visuals.ecgUrl || visuals.scgUrl;

    container.innerHTML = `
      <div class="rounded-3xl bg-[#141013] text-[#f5ebe6] border border-[#3d2932] shadow-2xl overflow-hidden select-none flex flex-col">
        <!-- Story Top Bar -->
        <div class="p-3.5 bg-[#1d1519] border-b border-[#302228] flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <button onclick="openKotonohaHub()" class="w-8 h-8 rounded-xl bg-[#2b1f25] hover:bg-[#3b2a33] text-[#e0c8c2] font-black text-sm flex items-center justify-center transition-all">
              ‹
            </button>
            <div>
              <div class="text-[10px] text-[#b39892] font-bold flex items-center gap-1.5">
                <span>${lesson.dateLabel}</span>
                <span class="text-[#f28b9b]">· ${lesson.levelBadge.split('+')[0]}</span>
              </div>
              <div class="text-sm font-black text-white leading-tight mt-0.5">${lesson.titleJp}</div>
            </div>
          </div>
          <div class="flex items-center gap-1.5">
            <button onclick="toggleKotonohaPronunciation()" class="px-2.5 py-1.5 rounded-xl border text-xs font-black transition-all ${showPron ? 'bg-[#e0465a] text-white border-[#ff7588]' : 'bg-[#2a1f24] text-[#9c847f] border-[#453139]'}">
              Aa
            </button>
            <button onclick="launchKotonohaQuizImmediate()" class="px-3 py-1.5 rounded-xl bg-[#2b1f25] hover:bg-[#3d2b34] border border-[#523843] text-xs font-bold text-[#e6d0ca] transition-all">
              건너뛰기
            </button>
          </div>
        </div>

        <!-- Red Progress Line -->
        <div class="w-full h-1 bg-[#2e1f26]">
          <div class="h-full bg-gradient-to-r from-[#e0465a] to-[#ff758c] transition-all duration-300" style="width: ${progressPct}%"></div>
        </div>

        <!-- Full Illustration Cinematic Stage: Click anywhere to advance (classic VN: big standing + slim overlay textbox) -->
        <div class="relative w-full flex flex-col bg-[#0e0a0c] cursor-pointer overflow-hidden" onclick="stepKotonohaStory(1)">
          
          <!-- Visual Presentation: True Transparent SCG (Commercial VN large standing) vs Clean Full ECG -->
          <div class="relative w-full h-[560px] sm:h-[640px] overflow-hidden bg-[#0c080a] flex items-start justify-center">
            ${visuals.isScg ? `
              <!-- [TRUE SCG + BG MODE] Pure Background Layer (No Characters) -->
              <img src="${visuals.bgUrl}" onerror="this.style.display='none'" class="absolute inset-0 w-full h-full object-cover filter brightness-[0.85] contrast-[1.02] pointer-events-none transition-all duration-500">
              <div class="absolute inset-0 bg-gradient-to-t from-[#141013] via-transparent to-black/25 pointer-events-none"></div>

              <!-- Pure Standing Character Sprite — oversized, head near top, feet cropped (classic VN look) -->
              <div class="relative z-10 h-full flex items-start justify-center pointer-events-none w-full">
                <img src="${visuals.scgUrl}" onerror="this.onerror=null;this.src='${visuals.ecgFallback}'" class="relative h-[135%] w-auto max-w-none object-contain object-top drop-shadow-[0_12px_28px_rgba(0,0,0,0.85)] transition-all duration-200">
              </div>
            ` : `
              <!-- [CLEAN FULL ECG MODE] Cinematic Ambient Blur + Center Illustration (Never Cut Off) -->
              <img src="${sceneImage}" onerror="this.onerror=null;this.src='${visuals.ecgFallback}'" class="absolute inset-0 w-full h-full object-cover filter blur-xl opacity-45 scale-125 pointer-events-none" style="object-position: center 25%;">
              <img src="${sceneImage}" onerror="this.onerror=null;this.src='${visuals.ecgFallback}'" class="relative z-10 max-h-full max-w-full object-contain mx-auto drop-shadow-[0_10px_25px_rgba(0,0,0,0.85)] transition-all duration-300">
            `}
            <!-- Smooth Gradient Blend into Dialogue Box -->
            <div class="absolute inset-0 z-20 pointer-events-none bg-gradient-to-b from-black/25 via-transparent to-[#141013]"></div>
          </div>

          <!-- Bottom Dialogue Box: Translucent VN Card (slim classic overlay so the standing stays visible) -->
          <div class="absolute left-3 right-3 bottom-2.5 z-30 p-3 rounded-2xl bg-[#1e161a]/90 border border-[#48303a] shadow-2xl backdrop-blur-md space-y-1.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <img src="${step.avatar || './image/03 gemini/avatar_gemini.png'}" class="w-7 h-7 rounded-full object-cover ring-2 ring-[#e0465a] shadow-xs">
                <span class="text-xs font-black text-[#f4869d]">${step.nameJp}</span>
                <span class="text-[11px] text-[#b89f99] font-bold">(${step.nameKo})</span>
              </div>
              <button onclick="event.stopPropagation(); speakJapanese('${(step.audio || step.jpPlain || '').replace(/'/g, "\\'")}', '${step.speaker || 'gemini'}')" class="px-2.5 py-1 rounded-xl bg-[#2e2027] hover:bg-[#3d2a33] text-[11px] font-bold text-[#f2a6b2] border border-[#543844] shadow-xs flex items-center gap-1 transition-all">
                <span>🔊</span><span>음성 듣기</span>
              </button>
            </div>

            <!-- Japanese Sentence with Furigana Ruby -->
            <div class="text-base sm:text-lg font-extrabold text-white leading-relaxed tracking-wide pt-0.5">
              ${step.jpRuby}
            </div>

            <!-- Korean Pronunciation Pill -->
            ${showPron ? `
              <div class="text-[11px] font-semibold text-[#f29aa8] bg-[#2b1d23] border border-[#472d38] px-2.5 py-0.5 rounded-lg inline-block">
                🗣️ ${step.pron}
              </div>
            ` : ''}

            <!-- Korean Translation -->
            <div class="text-[13px] font-bold text-[#e0cfca] leading-relaxed">
              ${step.ko}
            </div>

            <div class="flex items-center justify-end text-[11px] text-[#9e847e] pt-0.5">
              <span class="font-mono text-[#f2a6b2] font-bold">${curIdx + 1} / ${steps.length} ▼</span>
            </div>
          </div>
        </div>

        <!-- Bottom Navigation Footer -->
        <div class="px-4 py-3 bg-[#1a1316] border-t border-[#332229] flex items-center justify-between">
          <button onclick="stepKotonohaStory(-1)" ${curIdx === 0 ? 'disabled' : ''} class="px-3.5 py-1.5 rounded-xl bg-[#261c21] border border-[#422f37] text-xs font-bold ${curIdx === 0 ? 'opacity-40 cursor-not-allowed' : 'hover:bg-[#36272e] text-[#e6d0ca]'} transition-all">
            ← 이전
          </button>
          <span class="text-xs text-[#b09690] font-bold">
            ${curIdx + 1 < steps.length ? '화면을 누르면 다음 대사' : '누르면 오늘의 퀴즈 시작! 🎯'}
          </span>
          <button onclick="stepKotonohaStory(1)" class="px-3.5 py-1.5 rounded-xl bg-[#e0465a] hover:bg-[#eb576b] text-white text-xs font-black shadow transition-all">
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
                    <div onclick="speakJapanese('${(msg.targetWord || '').replace(/'/g, "\\'")}', 'gemini')" class="p-3 rounded-2xl bg-[#241c20] border border-[#382b31] cursor-pointer hover:border-[#634551] transition-all inline-block">
                      <div class="text-sm font-black text-white">${msg.promptJp}</div>
                      ${showPron && msg.promptPron ? `<div class="text-[11px] text-[#f29aa8] mt-0.5">${msg.promptPron}</div>` : ''}
                      <div class="text-xs text-[#b89d97] mt-0.5">${msg.promptKo}</div>
                    </div>

                    <!-- Big Target Kanji / Phrase Card (Screenshot 4 Q2 style) -->
                    <div onclick="speakJapanese('${(msg.targetWord || '').replace(/'/g, "\\'")}', 'gemini')" class="p-4 rounded-2xl bg-[#241c20] border border-[#3d2d35] cursor-pointer hover:border-[#e0465a] transition-all">
                      <div class="flex items-center justify-between text-[11px] font-black text-[#e0465a] mb-2">
                        <span>Q${msg.qIdx + 1} · ${msg.type}</span>
                        <span class="text-[10px] text-[#a88e88]">🔊 터치해서 발음 듣기</span>
                      </div>
                      <div class="text-center py-2">
                        <span class="text-2xl sm:text-3xl font-black text-white border-b-2 border-[#e0465a] pb-1 px-2">${msg.targetWord}</span>
                      </div>
                      ${msg.targetSub ? `
                        <div class="text-center mt-2.5">
                          ${kotonohaRuntime.revealedHints && kotonohaRuntime.revealedHints[msg.qIdx] ? `
                            <div class="p-2 sm:p-2.5 rounded-xl bg-[#1b1417] border border-[#543340] text-xs text-[#ffdbe2] leading-relaxed text-left animate-fadeIn">
                              <div class="flex items-center justify-between text-[10px] font-black text-[#f28b9b] mb-1">
                                <span>💡 문제 힌트</span>
                                <button onclick="event.stopPropagation(); toggleKotonohaQuizHint(${msg.qIdx})" class="text-[#ab908a] hover:text-[#ffd6de] text-[10px]">숨기기 ▴</button>
                              </div>
                              ${msg.targetSub}
                            </div>
                          ` : `
                            <button onclick="event.stopPropagation(); toggleKotonohaQuizHint(${msg.qIdx})" class="px-3 py-1 rounded-full bg-[#2c1d23] hover:bg-[#3d2630] border border-[#52333f] hover:border-[#e0465a] text-[11px] font-black text-[#f2a6b2] hover:text-white transition-all shadow-xs inline-flex items-center gap-1.5 active:scale-95">
                              <span>💡 힌트 보기</span>
                              <span class="text-[9px] text-[#ab8a83]">(터치하여 확인)</span>
                            </button>
                          `}
                        </div>
                      ` : ''}
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
                    <div onclick="speakJapanese('${(msg.reactJp || msg.speakText || '').replace(/'/g, "\\'")}', 'gemini')" class="p-3 rounded-2xl bg-[#241c20] border border-[#382b31] cursor-pointer inline-block">
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
                  <p class="text-xs text-[#f2c2cb]">「プロデューサーはん、ほんまによう頑張らはったなぁ🍵💖」<br>(프로듀서항, 정말 열심히 잘하셨사옵니다! 엽전 +50 · 언령 +25 · 인연 +30 EXP)</p>
                  <div class="flex justify-center gap-2 pt-2">
                    <button onclick="openKotonohaHub()" class="px-4 py-2 rounded-xl bg-[#e0465a] text-white text-xs font-black shadow">
                      🍵 다실 로비로 돌아가기
                    </button>
                    <button onclick="launchKotonohaQuizImmediate()" class="px-4 py-2 rounded-xl bg-[#2b1f25] border border-[#543844] text-xs font-bold text-[#e6d0ca]">
                      🔄 다시 풀기
                    </button>
                  </div>
                </div>
              `;
            }
            return '';
          }).join('')}
        </div>

        <!-- Bottom 1~4 Multiple Choice Buttons (Clean Japanese First + Pronunciation Toggle) -->
        ${(!isAllDone && currentQ) ? `
          <div class="p-3 sm:p-3.5 bg-[#1d1518] border-t border-[#332229] space-y-2">
            <div class="flex items-center justify-between px-1 text-xs text-[#b89d97]">
              <span class="font-bold text-[11px] text-[#d6beba]">정답을 선택하세요</span>
              <button onclick="toggleKotonohaOptionPron()" class="px-2.5 py-0.5 rounded-full border text-[11px] font-bold transition-all flex items-center gap-1 ${kotonohaRuntime.showOptionPron ? 'bg-[#e0465a] text-white border-[#ff7287] shadow-xs' : 'bg-[#291b21] text-[#d4b0a8] border-[#472d37] hover:border-[#6a3f50]'}">
                <span>🗣️</span>
                <span>${kotonohaRuntime.showOptionPron ? '한글 발음 숨기기' : '전체 발음 보기'}</span>
              </button>
            </div>
            ${currentQ.options.map((opt, idx) => {
              const parsed = parseKotonohaOptionText(opt);
              const singleKey = `${qIdx}_${idx}`;
              const isPronVisible = kotonohaRuntime.showOptionPron || Boolean(kotonohaRuntime.revealedOptionPron && kotonohaRuntime.revealedOptionPron[singleKey]);
              return `
                <button onclick="submitKotonohaQuizAnswer(${idx})" ${kotonohaRuntime.quizAnswered ? 'disabled' : ''} class="w-full p-2.5 sm:p-3 rounded-2xl bg-[#381c23] hover:bg-[#4a242e] active:scale-[0.99] border border-[#592d38] flex items-center justify-between text-left transition-all shadow-sm group ${kotonohaRuntime.quizAnswered ? 'opacity-60 cursor-not-allowed' : ''}">
                  <div class="flex items-center gap-2.5 min-w-0 pr-2">
                    <span class="w-6 h-6 rounded-full bg-[#e0465a] text-white text-xs font-black flex items-center justify-center shrink-0 shadow-xs">
                      ${idx + 1}
                    </span>
                    <span class="text-sm font-black text-[#fdf2f0] tracking-wide truncate group-hover:text-white">
                      ${parsed.main}
                    </span>
                  </div>
                  ${parsed.hasPron ? `
                    <div class="shrink-0 pl-1">
                      ${isPronVisible ? `
                        <span class="px-2 py-0.5 rounded-lg bg-[#27151a] text-[#ffd6de] border border-[#5a2a37] text-xs font-bold animate-fadeIn">
                          ${parsed.pron}
                        </span>
                      ` : `
                        <span onclick="toggleSingleOptionPron(${idx}, event)" class="px-2 py-0.5 rounded-lg bg-[#2a1b22] hover:bg-[#3d2530] text-[#c9a7a0] hover:text-[#ffd6de] border border-[#482d38] text-[10px] font-bold transition-all shadow-xs cursor-pointer" title="이 선택지 발음 보기">
                          발음 보기
                        </span>
                      `}
                    </div>
                  ` : ''}
                </button>
              `;
            }).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }

  // MODE 4: SHORT-TOON MANGA - Episode List
  if (kotonohaRuntime.currentMode === 'manga_list') {
    const activeSeason = kotonohaRuntime.selectedSeason || 1;
    const seasonLessons = lessons.map((item, idx) => ({ ...item, globalIdx: idx }))
      .filter(item => (item.season || 1) === activeSeason);
    container.innerHTML = `
      <div class="rounded-3xl bg-[#181316] text-[#f5ebe6] border border-[#3a2830] shadow-2xl overflow-hidden">
        <div class="p-3.5 bg-gradient-to-b from-[#241a1f] to-[#181316] border-b border-[#332228] flex items-center justify-between">
          <div class="flex items-center gap-2">
            <button onclick="openKotonohaHub()" class="w-8 h-8 rounded-xl bg-[#2b1f25] hover:bg-[#3b2a33] text-[#e0c8c2] font-black text-sm flex items-center justify-center">‹</button>
            <div>
              <h2 class="text-sm font-black text-[#e86b7e]">📖 미니툰</h2>
              <p class="text-[11px] text-[#b59e99] font-bold">3인 히로인 웹툰 - 편당 1화</p>
            </div>
          </div>
          <span class="text-[10px] px-2 py-1 rounded-full bg-[#352329] text-[#f2a6b2] font-bold border border-[#52343d]">시즌 ${activeSeason}</span>
        </div>

        <div class="grid grid-cols-2 gap-2 p-3">
          <button onclick="switchKotonohaSeason(1)" class="p-2 rounded-xl border text-center ${activeSeason === 1 ? 'bg-[#3e242f] border-[#e0465a] text-white font-black' : 'bg-[#21181c] border-[#38282f] text-[#a8908b]'}">🍵 시즌 1</button>
          <button onclick="switchKotonohaSeason(2)" class="p-2 rounded-xl border text-center ${activeSeason === 2 ? 'bg-[#3e242f] border-[#e0465a] text-white font-black' : 'bg-[#21181c] border-[#38282f] text-[#a8908b]'}">🌸 시즌 2</button>
        </div>

        <div class="p-3 pt-0 space-y-3 max-h-[560px] overflow-y-auto clean-scroll">
          ${seasonLessons.map(item => {
            const isDone = (kState.completedLessons || []).includes(item.id);
            const epBadge = item.epCode || (item.season ? item.season + '-' + (item.episode || 1) : '1-' + item.dayNum);
            return `
              <div class="rounded-2xl overflow-hidden border border-[#422c35] bg-[#1d1519] cursor-pointer group" onclick="openMangaRead(${item.globalIdx})">
                <div class="relative h-32 overflow-hidden">
                  <img src="${item.bgImage || './image/03 gemini/gemini_02_matcha.png'}" onerror="this.src='./image/03 gemini/gemini_26_kyoto_teahouse.png'" class="w-full h-full object-cover object-[center_15%] group-hover:scale-105 transition-all duration-500">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-transparent to-black/10"></div>
                  <div class="absolute top-2 left-2 flex gap-1.5">
                    <span class="px-2 py-0.5 rounded-full bg-[#e0465a] text-white text-[10px] font-black shadow">${isDone ? '✅ ' : ''}${epBadge}</span>
                    <span class="px-2 py-0.5 rounded-full bg-black/60 text-[#ffd6de] text-[10px] font-bold border border-white/20">${item.levelBadge.split('+')[0]}</span>
                  </div>
                </div>
                <div class="p-2.5 flex items-center justify-between gap-2">
                  <div class="min-w-0">
                    <div class="text-xs font-bold text-white truncate">${item.titleKo}</div>
                    <div class="text-[10px] text-[#9c847f] truncate mt-0.5">${item.titleJp.replace(/<[^>]+>/g, '')}</div>
                  </div>
                  <span class="text-xs font-black text-[#ff6b81]">읽기 ›</span>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
    return;
  }

  // MODE 5: SHORT-TOON MANGA - Vertical Panel Reader (per episode)
  if (kotonohaRuntime.currentMode === 'manga_read') {
    const steps = (lesson.story || []).slice(0, 12);
    container.innerHTML = `
      <div class="rounded-3xl bg-[#141013] text-[#f5ebe6] border border-[#3a2830] shadow-2xl overflow-hidden">
        <div class="p-3 bg-[#1d1519] border-b border-[#332228] flex items-center justify-between sticky top-0 z-30">
          <div class="flex items-center gap-2 min-w-0">
            <button onclick="backToMangaList()" class="w-8 h-8 shrink-0 rounded-xl bg-[#2b1f25] hover:bg-[#3b2a33] text-[#e0c8c2] font-black text-sm flex items-center justify-center">‹</button>
            <div class="min-w-0">
              <div class="text-[10px] text-[#b89d97] font-bold">제${lesson.epCode || ''}화 · ${lesson.levelBadge.split('+')[0]}</div>
              <div class="text-xs font-black text-white truncate">${lesson.titleJp}</div>
            </div>
          </div>
          <button onclick="event.stopPropagation(); speakJapanese('${lesson.titleJp.replace(/<[^>]+>/g, '').replace(/'/g, "\\'")}', 'gemini')" class="px-2.5 py-1 rounded-xl bg-[#2e2027] hover:bg-[#3d2b34] text-[11px] font-bold text-[#f2a6b2] border border-[#543844]">🔊 제목</button>
        </div>

        <div class="bg-white p-1.5 space-y-1.5">
          ${steps.map((step, i) => {
            const visuals = resolveKotonohaVisuals(step, lesson);
            const sceneImage = visuals.ecgUrl || visuals.scgUrl;
            const audioArg = (step.audio || step.jpPlain || step.jpRuby || '').replace(/'/g, "\\'");
            const speaker = step.speaker || 'gemini';
            const speakerName = step.nameJp || '';
            const speakerKo = step.nameKo || '';
            // Panel rhythm: opening tall, beats medium, every 3rd short
            const panelH = i === 0 ? 'h-[430px] sm:h-[500px]' : (i % 3 === 2 ? 'h-[260px] sm:h-[320px]' : 'h-[340px] sm:h-[420px]');
            const bubbleSide = i % 2 === 0 ? 'left-2.5' : 'right-2.5';
            const facing = i % 2 === 0 ? 'items-start' : 'items-end';
            const tailClass = i % 2 === 0 ? 'absolute -bottom-1.5 left-5 w-3 h-3 bg-white border-b border-r border-[#2b2b2b] rotate-45' : 'absolute -bottom-1.5 right-5 w-3 h-3 bg-white border-b border-l border-[#2b2b2b] rotate-45';
            return `
              <div class="border-[3px] border-black bg-[#0c080a] cursor-pointer active:brightness-125 transition-all" onclick="speakJapanese('${audioArg}', '${speaker}')">
                <div class="relative ${panelH} w-full overflow-hidden flex items-start justify-center">
                  ${visuals.isScg ? `
                    <img src="${visuals.bgUrl}" onerror="this.style.display='none'" class="absolute inset-0 w-full h-full object-cover filter brightness-[0.85] pointer-events-none">
                    <img src="${visuals.scgUrl}" onerror="this.src='${visuals.ecgFallback}'" class="relative z-10 h-[130%] w-auto max-w-none object-contain object-top drop-shadow-[0_12px_28px_rgba(0,0,0,0.85)] pointer-events-none">
                  ` : `
                    <img src="${sceneImage}" onerror="this.src='${visuals.ecgFallback}'" class="absolute inset-0 w-full h-full object-cover filter blur-xl opacity-40 scale-125 pointer-events-none" style="object-position: center 25%;">
                    <img src="${sceneImage}" onerror="this.src='${visuals.ecgFallback}'" class="relative z-10 max-h-full max-w-full object-contain mx-auto pointer-events-none">
                  `}
                  <!-- Cut number label -->
                  <span class="absolute top-2 left-2 px-1.5 py-0.5 bg-black/70 text-white text-[10px] font-black rounded-sm z-20">${i + 1}</span>
                </div>
                <!-- Speech bubble overlay (manhwa style, white balloon like reference) -->
                <div class="relative px-2 pb-2 -mt-14 z-20 flex ${facing} pointer-events-none">
                  <div class="relative bg-white border-2 border-[#2b2b2b] rounded-2xl px-3 py-2 max-w-[72%] shadow-md">
                    <div class="${tailClass}"></div>
                    <div class="text-[10px] font-bold text-[#7a5c63] mb-0.5">${speakerName}${speakerKo ? ' · ' + speakerKo : ''}</div>
                    <div class="text-[13px] font-extrabold text-[#141013] leading-snug">${step.jpRuby}</div>
                    ${showPron ? `<div class="text-[10px] font-semibold text-[#b03a52] mt-0.5">${step.pron}</div>` : ''}
                  </div>
                </div>
                <!-- Narration box (Korean translation, classic webtoon white caption) -->
                <div class="px-2 pb-2">
                  <div class="bg-white border-[1.5px] border-black px-3 py-2">
                    <div class="text-xs font-bold text-[#141013] leading-relaxed">${step.ko}</div>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div class="p-3 bg-[#181316] border-t border-[#332228] text-center">
          <div class="text-[10px] text-[#8a7a77] font-mono mb-2.5">— ${steps.length} -</div>
          <div class="flex items-center justify-between">
            <button onclick="backToMangaList()" class="px-3 py-1.5 rounded-xl bg-[#261c21] border border-[#422f37] text-xs font-bold text-[#e6d0ca]">← 목록</button>
            <button onclick="openNextMangaEp()" class="px-3 py-1.5 rounded-xl bg-[#e0465a] text-white text-xs font-black shadow">다음 화 ›</button>
          </div>
        </div>
      </div>
    `;
    return;
  }

}
