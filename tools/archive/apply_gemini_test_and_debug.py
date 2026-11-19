from pathlib import Path

index_path = Path("index.html")
content = index_path.read_text(encoding="utf-8")

# 1. Update Settings Modal to add Test Connection Button
old_settings_box = """          <div class="relative">
            <input type="password" id="geminiApiKeyInput" placeholder="AIzaSy... (Gemini API Key 입력)" class="w-full sub-box px-3 py-1.5 text-xs focus:outline-none focus:border-sky-400 font-mono pr-8">
            <button type="button" onclick="toggleApiKeyVisibility()" class="absolute right-2 top-1.5 text-xs text-slate-400 hover:text-slate-600">👁️</button>
          </div>
          <div class="flex items-center justify-between pt-0.5 text-[10px]">
            <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="text-sky-600 dark:text-sky-400 font-bold hover:underline flex items-center gap-1">
              <span>Google AI Studio에서 무료 키 발급 ↗</span>
            </a>
            <button type="button" onclick="clearGeminiApiKey()" class="text-rose-500 hover:underline font-bold">키 삭제</button>
          </div>"""

new_settings_box = """          <div class="relative">
            <input type="password" id="geminiApiKeyInput" placeholder="AIzaSy... (Gemini API Key 입력)" class="w-full sub-box px-3 py-1.5 text-xs focus:outline-none focus:border-sky-400 font-mono pr-8">
            <button type="button" onclick="toggleApiKeyVisibility()" class="absolute right-2 top-1.5 text-xs text-slate-400 hover:text-slate-600">👁️</button>
          </div>
          <div class="flex items-center justify-between pt-1 gap-2 text-[10px]">
            <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="text-sky-600 dark:text-sky-400 font-bold hover:underline flex items-center gap-1">
              <span>무료 키 발급 ↗</span>
            </a>
            <div class="flex items-center gap-2">
              <button type="button" onclick="testGeminiApiKey()" class="px-2 py-0.5 rounded-lg bg-sky-500 hover:bg-sky-600 text-white font-bold transition-all shadow-xs">⚡ 연결 테스트</button>
              <button type="button" onclick="clearGeminiApiKey()" class="text-rose-500 hover:underline font-bold">키 삭제</button>
            </div>
          </div>"""

content = content.replace(old_settings_box.replace("\n", "\r\n"), new_settings_box.replace("\n", "\r\n"))
content = content.replace(old_settings_box, new_settings_box)

# 2. Add testGeminiApiKey function and improve callGeminiDirectClient with clear error handling
old_gemini_fn = """    async function callGeminiDirectClient(apiKey, userText, trainer, mode, context) {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
      const systemPrompt = getGeminiSystemPrompt(trainer, mode);
      const remaining = (parseFloat(context.weight) - parseFloat(context.targetWeight)).toFixed(1);
      const promptWithContext = `[프로듀서 현재 피트니스 상태]\\n- 현재 시각: ${context.timeStr}\\n- 현재 체중: ${context.weight}kg (목표 ${context.targetWeight}kg까지 ${remaining}kg 남음)\\n- 오늘 5km 러닝: ${context.runDone ? '완료' : '미완료'}\\n- 오늘 헬스장 루틴: 5개 종목 중 ${context.gymCompletedCount}개 완료\\n- 음료: 말차 ${context.teaLog?.matcha || 0}잔, 커피 ${context.teaLog?.espresso || 0}잔, 단백질 ${context.teaLog?.tea || 0}잔\\n\\n[프로듀서의 메시지]\\n${userText}`;

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ role: 'user', parts: [{ text: promptWithContext }] }],
          systemInstruction: { parts: [{ text: systemPrompt }] },
          generationConfig: { temperature: 0.85, maxOutputTokens: 350 }
        })
      });

      if (!res.ok) throw new Error('Gemini API Error: ' + res.status);
      const data = await res.json();
      const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || '';

      if (mode === 'dual') {
        try {
          const cleaned = rawText.replace(/```json/gi, '').replace(/```/g, '').trim();
          return { mode: 'dual', replies: JSON.parse(cleaned) };
        } catch (e) {
          return { mode: 'dual', replies: { gemini: rawText, kotone: "프로듀서님 파이팅이에요! 💛", mio: "우리 모두 함께 힘내자구! 🌟" } };
        }
      }
      return { mode: 'single', reply: rawText };
    }"""

new_gemini_fn = """    async function testGeminiApiKey() {
      const keyInput = document.getElementById('geminiApiKeyInput');
      const key = (keyInput ? keyInput.value : '').trim() || localStorage.getItem('GEMINI_API_KEY');
      const statusEl = document.getElementById('geminiKeyStatus');
      if (!key) {
        alert('먼저 Gemini API 키를 입력해 주세요!');
        return;
      }
      if (statusEl) {
        statusEl.textContent = "⏳ 연결 테스트 중...";
        statusEl.className = "text-[9px] px-2 py-0.5 rounded-full font-black bg-amber-500/20 text-amber-600";
      }
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${key}`;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ role: 'user', parts: [{ text: '안녕! 제미니 트레이너로서 한국어로 한 문장 인사해줘.' }] }]
          })
        });
        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.error?.message || ('HTTP ' + res.status));
        }
        const data = await res.json();
        const testReply = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
        localStorage.setItem('GEMINI_API_KEY', key);
        updateGeminiKeyStatusUI();
        alert(`✅ Gemini AI 정상 연결 성공!\\n\\n[AI 테스트 응답]\\n"${testReply}"`);
      } catch (err) {
        if (statusEl) {
          statusEl.textContent = "🔴 연결 실패";
          statusEl.className = "text-[9px] px-2 py-0.5 rounded-full font-black bg-rose-500/20 text-rose-600";
        }
        alert(`❌ Gemini AI 연결 실패:\\n${err.message}\\n\\nGoogle AI Studio에서 API 키를 다시 확인해 주세요!`);
      }
    }

    async function callGeminiDirectClient(apiKey, userText, trainer, mode, context) {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
      const systemPrompt = getGeminiSystemPrompt(trainer, mode);
      const remaining = (parseFloat(context.weight) - parseFloat(context.targetWeight)).toFixed(1);
      const promptWithContext = `[프로듀서 현재 피트니스 상태]\\n- 현재 시각: ${context.timeStr}\\n- 현재 체중: ${context.weight}kg (목표 ${context.targetWeight}kg까지 ${remaining}kg 남음)\\n- 오늘 5km 러닝: ${context.runDone ? '완료' : '미완료'}\\n- 오늘 헬스장 루틴: 5개 종목 중 ${context.gymCompletedCount}개 완료\\n- 음료: 말차 ${context.teaLog?.matcha || 0}잔, 커피 ${context.teaLog?.espresso || 0}잔, 단백질 ${context.teaLog?.tea || 0}잔\\n\\n[프로듀서의 메시지]\\n${userText}`;

      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ role: 'user', parts: [{ text: promptWithContext }] }],
          systemInstruction: { parts: [{ text: systemPrompt }] },
          generationConfig: { temperature: 0.85, maxOutputTokens: 350 }
        })
      });

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        const errMsg = errJson?.error?.message || ('HTTP ' + res.status);
        throw new Error(errMsg);
      }
      const data = await res.json();
      const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || '';

      if (mode === 'dual') {
        try {
          const cleaned = rawText.replace(/```json/gi, '').replace(/```/g, '').trim();
          return { mode: 'dual', replies: JSON.parse(cleaned) };
        } catch (e) {
          return { mode: 'dual', replies: { gemini: rawText, kotone: "프로듀서님 파이팅이에요! 💛", mio: "우리 모두 함께 힘내자구! 🌟" } };
        }
      }
      return { mode: 'single', reply: rawText };
    }"""

content = content.replace(old_gemini_fn.replace("\n", "\r\n"), new_gemini_fn.replace("\n", "\r\n"))
content = content.replace(old_gemini_fn, new_gemini_fn)

# 3. Update sendDirectMessage error reporting
old_catch = """        } catch (e) {
          console.warn('Direct Gemini API error, falling back:', e);
        }"""

new_catch = """        } catch (e) {
          console.error('Direct Gemini API error:', e);
          activeTypingIndicator = null;
          const senderName = currentTrainer === 'kotone' ? '코토네' : currentTrainer === 'mio' ? '미오' : '제미니';
          state.chatHistory.push({
            sender: currentTrainer,
            name: senderName,
            text: `⚠️ [Gemini AI 연결 오류: ${e.message}] 설정(⚙️) 창에서 [⚡ 연결 테스트]를 눌러 키를 확인해 주세요!`,
            time: curTime
          });
          renderChat();
          return;
        }"""

content = content.replace(old_catch.replace("\n", "\r\n"), new_catch.replace("\n", "\r\n"))
content = content.replace(old_catch, new_catch)

# 4. Connect topic choice buttons to real-time AI if API key is present
old_select_topic = """    function selectTopicOption(topicKey, idx) {
      const list = TOPIC_CHOICES[topicKey];
      if (!list || !list[idx]) return;
      const item = list[idx];
      playBeep(660, 0.08);

      state.chatHistory.push({ sender: 'user', text: item.text, time: getKakaoTimeStr() });
      renderChat();

      if (item.sit) {
        setTrainerMode(state.activeMode, item.sit);
      }

      triggerTrainerTypingReply(() => {"""

new_select_topic = """    function selectTopicOption(topicKey, idx) {
      const list = TOPIC_CHOICES[topicKey];
      if (!list || !list[idx]) return;
      const item = list[idx];
      playBeep(660, 0.08);

      const localApiKey = localStorage.getItem('GEMINI_API_KEY');
      if (localApiKey) {
        if (item.sit) setTrainerMode(state.activeMode, item.sit);
        document.getElementById('directChatInput').value = item.text;
        sendDirectMessage();
        return;
      }

      state.chatHistory.push({ sender: 'user', text: item.text, time: getKakaoTimeStr() });
      renderChat();

      if (item.sit) {
        setTrainerMode(state.activeMode, item.sit);
      }

      triggerTrainerTypingReply(() => {"""

content = content.replace(old_select_topic.replace("\n", "\r\n"), new_select_topic.replace("\n", "\r\n"))
content = content.replace(old_select_topic, new_select_topic)

index_path.write_text(content, encoding="utf-8")
print("apply_gemini_test_and_debug.py finished successfully!")
