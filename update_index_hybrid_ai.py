from pathlib import Path

index_path = Path("index.html")
content = index_path.read_text(encoding="utf-8")

# 1. Update Webhook & AI Modal with Key Input
old_box = """        <!-- 1. Google Gemini AI Serverless Guide -->
        <div class="p-3 rounded-2xl bg-sky-50/80 dark:bg-sky-950/40 border border-sky-200/80 dark:border-sky-800/60 space-y-1.5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">
              <span class="text-sm">✨</span>
              <span class="text-xs font-black text-sky-900 dark:text-sky-200">Google Gemini 실시간 AI</span>
            </div>
            <span class="text-[9px] px-2 py-0.5 rounded-full font-black bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-400/30">
              Vercel 서버리스 연동
            </span>
          </div>
          <p class="text-[10px] text-slate-600 dark:text-slate-300 leading-relaxed">
            모든 기기(PC/모바일)에서 실시간 캐릭터 대화가 구동됩니다. Vercel 프로젝트 대시보드의 <b>Environment Variables</b>에 <code class="px-1 py-0.5 rounded bg-sky-100 dark:bg-sky-900 text-sky-700 dark:text-sky-300 font-mono font-bold">GEMINI_API_KEY</code>를 등록해 주시면 즉시 활성화됩니다.
          </p>
          <div class="pt-0.5">
            <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="text-[10px] text-sky-600 dark:text-sky-400 font-bold hover:underline inline-flex items-center gap-1">
              <span>Google AI Studio에서 무료 API Key 발급받기 ↗</span>
            </a>
          </div>
        </div>"""

new_box = """        <!-- 1. Google Gemini AI Settings -->
        <div class="p-3 rounded-2xl bg-sky-50/80 dark:bg-sky-950/40 border border-sky-200/80 dark:border-sky-800/60 space-y-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">
              <span class="text-sm">✨</span>
              <span class="text-xs font-black text-sky-900 dark:text-sky-200">Google Gemini 실시간 AI</span>
            </div>
            <span id="geminiKeyStatus" class="text-[9px] px-2 py-0.5 rounded-full font-black bg-slate-200 dark:bg-slate-700 text-slate-500">
              미등록 (기본 대사)
            </span>
          </div>
          <p class="text-[10px] text-slate-600 dark:text-slate-300 leading-relaxed">
            API 키를 등록하면 내 모든 채팅에 대해 <b>제미니(츤데레) · 코토네(애교) · 미오(파워풀)</b> 성격과 운동 상태를 반영해 <b>실시간 AI</b>로 대화합니다.
          </p>
          <div class="relative">
            <input type="password" id="geminiApiKeyInput" placeholder="AIzaSy... (Gemini API Key 입력)" class="w-full sub-box px-3 py-1.5 text-xs focus:outline-none focus:border-sky-400 font-mono pr-8">
            <button type="button" onclick="toggleApiKeyVisibility()" class="absolute right-2 top-1.5 text-xs text-slate-400 hover:text-slate-600">👁️</button>
          </div>
          <div class="flex items-center justify-between pt-0.5 text-[10px]">
            <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="text-sky-600 dark:text-sky-400 font-bold hover:underline flex items-center gap-1">
              <span>Google AI Studio에서 무료 키 발급 ↗</span>
            </a>
            <button type="button" onclick="clearGeminiApiKey()" class="text-rose-500 hover:underline font-bold">키 삭제</button>
          </div>
        </div>"""

content = content.replace(old_box.replace("\n", "\r\n"), new_box.replace("\n", "\r\n"))
content = content.replace(old_box, new_box)

# 2. Add client-side direct Gemini call functions & update sendDirectMessage
direct_ai_js = """    // ============================================================================
    // GEMINI REAL-TIME AI ENGINE (Direct Client-Side & Serverless Hybrid)
    // ============================================================================
    function getGeminiSystemPrompt(trainer, mode) {
      if (mode === 'dual') {
        return `너는 개인 피트니스 코칭 단톡방에 참여한 3명의 미소녀 트레이너(제미니, 코토네, 미오)야. 프로듀서의 메시지와 운동 상태를 보고 3명이 티키타카를 주고받으며 답장해.
1. 제미니: 흑발 고양이귀 츤데레 코치. 겉으론 쌀쌀맞게 잔소리하지만 속으론 프로듀서 걱정. 반말 (~했거든?, ~하란 말이야, 바보 프로듀서, 흥!), 끝에 🐾 또는 🔥.
2. 코토네: 금발 땋은머리 학원 아이돌. 돈과 간식에 약하지만 다정 애교 만점. 존댓말 (~해요!, ~답니다!, 헤헤), 호칭 '프로듀서님!', 끝에 💛 또는 ✨.
3. 미오: 갈색 숏컷 체육계 아이돌. 호쾌한 긍정 반말 (핫하하!, 영-차!), 호칭 '프로듀서!', 끝에 🌟 또는 🏃‍♀️.
각 캐릭터당 1~2문장 내외로 간결하게. 반드시 아래 JSON 포맷으로만 출력할 것:
{"gemini": "제미니 대사 🐾", "kotone": "코토네 대사 💛", "mio": "미오 대사 🌟"}`;
      } else if (trainer === 'kotone') {
        return `너는 학원 아이돌마스터의 아이돌이자 전담 트레이너 '후지타 코토네'야. 금발 땋은머리, 애교 넘치고 다정한 존댓말 (~해요!, 헤헤, 으에에엑?! 등). 호칭은 '프로듀서님!'. 52kg 감량 목표를 함께하며 식단에 공감하고 달콤하게 응원해. 카카오톡 답장처럼 1~3문장 내외로 작성. 💛✨`;
      } else if (trainer === 'mio') {
        return `너는 신데렐라 걸즈의 파워풀하고 밝은 긍정 에너지 1000% 체육계 아이돌 트레이너 '혼다 미오'야. 갈색 숏컷 아호게 머리. 활기차고 씩씩한 반말 ('프로듀서!', '핫하하!', '영-차!'). 5km 러닝과 헬스장 완주 독려. 1~3문장 내외의 경쾌한 메신저 스타일. 🌟🏃‍♀️`;
      } else {
        return `너는 개인 피트니스 코칭 웹앱의 전담 트레이너 '제미니'야. 흑발에 검은 고양이귀를 가진 츤데레 미소녀 코치. 쌀쌀맞게 잔소리하지만 속으로는 프로듀서를 누구보다 아끼고 챙기는 츤데레 반말 (~했거든?, ~하란 말이야, 바보 프로듀서, 흥!). 절대 메롱이나 유치한 장난은 치지 않음. 17시 단식과 헬스장 20회 4세트 루틴 준수를 엄격히 코칭. 1~3문장 내외 메신저 스타일. 🐾🔥`;
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
    }

    function toggleApiKeyVisibility() {
      const el = document.getElementById('geminiApiKeyInput');
      if (el) el.type = el.type === 'password' ? 'text' : 'password';
    }

    function clearGeminiApiKey() {
      localStorage.removeItem('GEMINI_API_KEY');
      const el = document.getElementById('geminiApiKeyInput');
      if (el) el.value = '';
      updateGeminiKeyStatusUI();
    }

    function updateGeminiKeyStatusUI() {
      const key = localStorage.getItem('GEMINI_API_KEY');
      const badge = document.getElementById('geminiKeyStatus');
      if (badge) {
        badge.textContent = key ? "🟢 AI 실시간 연동 활성화" : "⚪ 미등록 (기본 대사)";
        badge.className = key ? "text-[9px] px-2 py-0.5 rounded-full font-black bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-400/40" : "text-[9px] px-2 py-0.5 rounded-full font-black bg-slate-200 dark:bg-slate-700 text-slate-500";
      }
    }
"""

# Replace sendDirectMessage to use direct client key first, then /api/chat serverless
old_send_block = """    async function sendDirectMessage() {
      const input = document.getElementById('directChatInput');
      const text = (input.value || '').trim();
      if (!text) return;
      input.value = '';
      playBeep(640, 0.07);

      state.chatHistory.push({ sender: 'user', text, time: getKakaoTimeStr() });
      renderChat();

      // Show Kakao-style typing indicator while AI thinks
      let typingSender = state.activeTrainer || 'gemini';
      let typingName = typingSender === 'kotone' ? '코토네' : typingSender === 'mio' ? '미오' : '제미니';
      if (state.activeMode === 'dual') {
        typingSender = 'dual';
        typingName = '제미니 · 코토네 · 미오';
      }
      activeTypingIndicator = { sender: typingSender, name: typingName };
      renderChat();

      const curTime = getKakaoTimeStr();
      const currentMode = state.activeMode;
      const currentTrainer = state.activeTrainer || 'gemini';

      // Assemble rich workout & routine context for Gemini AI
      const gymCompletedCount = state.gymRoutine ? Object.values(state.gymRoutine).filter(ex => ex.sets && ex.sets.every(Boolean)).length : 0;
      const context = {
        weight: state.weight || '56.3',
        targetWeight: '52.0',
        runDone: !!state.runDone,
        gymCompletedCount,
        teaLog: state.teaLog || {},
        timeStr: curTime
      };

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            trainer: currentTrainer,
            mode: currentMode,
            context
          })
        });

        if (response.ok) {
          const data = await response.json();
          activeTypingIndicator = null;

          if (data.mode === 'dual' && data.replies) {
            if (data.replies.gemini) state.chatHistory.push({ sender: 'gemini', name: '제미니', text: data.replies.gemini, time: curTime });
            if (data.replies.kotone) state.chatHistory.push({ sender: 'kotone', name: '코토네', text: data.replies.kotone, time: curTime });
            if (data.replies.mio) state.chatHistory.push({ sender: 'mio', name: '미오', text: data.replies.mio, time: curTime });
          } else if (data.reply) {
            const senderName = currentTrainer === 'kotone' ? '코토네' : currentTrainer === 'mio' ? '미오' : '제미니';
            state.chatHistory.push({ sender: currentTrainer, name: senderName, text: data.reply, time: curTime });
          }
          addBondExp(20);
          saveState();
          renderChat();
          return;
        }
      } catch (err) {
        console.warn('AI Serverless Chat fallback:', err);
      }

      // Safe fallback if API key is not configured or offline
      activeTypingIndicator = null;
      let gemObj = window.getSmartReply ? window.getSmartReply('gemini', text) : { text: "흥, 바보 프로듀서! 목표 52kg까지 나만 믿고 따라와! 🐾", sit: 'ev1' };
      let kotObj = window.getSmartReply ? window.getSmartReply('kotone', text) : { text: "헤헤~ 프로듀서님! 코토네가 1등으로 응원할게요! 💛", sit: 'ev1' };
      let mioObj = window.getSmartReply ? window.getSmartReply('mio', text) : { text: "프로듀서 목소리 들으니까 기운 펄펄! 오늘도 파이팅이야~ 🌟", sit: 'ev1' };

      if (currentMode === 'dual') {
        setTrainerMode('dual', gemObj.sit || 'ev1');
        state.chatHistory.push({ sender: 'gemini', name: '제미니', text: gemObj.text, time: curTime });
        state.chatHistory.push({ sender: 'kotone', name: '코토네', text: kotObj.text, time: curTime });
        state.chatHistory.push({ sender: 'mio', name: '미오', text: mioObj.text, time: curTime });
      } else if (currentTrainer === 'kotone') {
        setTrainerMode('kotone', kotObj.sit || 'ev1');
        state.chatHistory.push({ sender: 'kotone', name: '코토네', text: kotObj.text, time: curTime });
      } else if (currentTrainer === 'mio') {
        setTrainerMode('mio', mioObj.sit || 'ev1');
        state.chatHistory.push({ sender: 'mio', name: '미오', text: mioObj.text, time: curTime });
      } else {
        setTrainerMode('gemini', gemObj.sit || 'ev1');
        state.chatHistory.push({ sender: 'gemini', name: '제미니', text: gemObj.text, time: curTime });
      }
      addBondExp(15);
      saveState();
      renderChat();
    }"""

new_send_block = f"""{direct_ai_js}
    async function sendDirectMessage() {{
      const input = document.getElementById('directChatInput');
      const text = (input.value || '').trim();
      if (!text) return;
      input.value = '';
      playBeep(640, 0.07);

      state.chatHistory.push({{ sender: 'user', text, time: getKakaoTimeStr() }});
      renderChat();

      // Show Kakao-style typing indicator while AI thinks
      let typingSender = state.activeTrainer || 'gemini';
      let typingName = typingSender === 'kotone' ? '코토네' : typingSender === 'mio' ? '미오' : '제미니';
      if (state.activeMode === 'dual') {{
        typingSender = 'dual';
        typingName = '제미니 · 코토네 · 미오';
      }}
      activeTypingIndicator = {{ sender: typingSender, name: typingName }};
      renderChat();

      const curTime = getKakaoTimeStr();
      const currentMode = state.activeMode;
      const currentTrainer = state.activeTrainer || 'gemini';

      // Assemble rich workout & routine context for Gemini AI
      const gymCompletedCount = state.gymRoutine ? Object.values(state.gymRoutine).filter(ex => ex.sets && ex.sets.every(Boolean)).length : 0;
      const context = {{
        weight: state.weight || '56.3',
        targetWeight: '52.0',
        runDone: !!state.runDone,
        gymCompletedCount,
        teaLog: state.teaLog || {{}},
        timeStr: curTime
      }};

      // 1. Direct Client-side Gemini Call (if API key saved in localStorage)
      const localApiKey = localStorage.getItem('GEMINI_API_KEY');
      if (localApiKey) {{
        try {{
          const aiResult = await callGeminiDirectClient(localApiKey, text, currentTrainer, currentMode, context);
          activeTypingIndicator = null;
          if (aiResult.mode === 'dual' && aiResult.replies) {{
            if (aiResult.replies.gemini) state.chatHistory.push({{ sender: 'gemini', name: '제미니', text: aiResult.replies.gemini, time: curTime }});
            if (aiResult.replies.kotone) state.chatHistory.push({{ sender: 'kotone', name: '코토네', text: aiResult.replies.kotone, time: curTime }});
            if (aiResult.replies.mio) state.chatHistory.push({{ sender: 'mio', name: '미오', text: aiResult.replies.mio, time: curTime }});
          }} else if (aiResult.reply) {{
            const senderName = currentTrainer === 'kotone' ? '코토네' : currentTrainer === 'mio' ? '미오' : '제미니';
            state.chatHistory.push({{ sender: currentTrainer, name: senderName, text: aiResult.reply, time: curTime }});
          }}
          addBondExp(20);
          saveState();
          renderChat();
          return;
        }} catch (e) {{
          console.warn('Direct Gemini API error, falling back:', e);
        }}
      }}

      // 2. Serverless /api/chat Fallback (if Vercel environment variable configured)
      try {{
        const response = await fetch('/api/chat', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            message: text,
            trainer: currentTrainer,
            mode: currentMode,
            context
          }})
        }});

        if (response.ok) {{
          const data = await response.json();
          activeTypingIndicator = null;

          if (data.mode === 'dual' && data.replies) {{
            if (data.replies.gemini) state.chatHistory.push({{ sender: 'gemini', name: '제미니', text: data.replies.gemini, time: curTime }});
            if (data.replies.kotone) state.chatHistory.push({{ sender: 'kotone', name: '코토네', text: data.replies.kotone, time: curTime }});
            if (data.replies.mio) state.chatHistory.push({{ sender: 'mio', name: '미오', text: data.replies.mio, time: curTime }});
          }} else if (data.reply) {{
            const senderName = currentTrainer === 'kotone' ? '코토네' : currentTrainer === 'mio' ? '미오' : '제미니';
            state.chatHistory.push({{ sender: currentTrainer, name: senderName, text: data.reply, time: curTime }});
          }}
          addBondExp(20);
          saveState();
          renderChat();
          return;
        }}
      }} catch (err) {{
        console.warn('AI Serverless Chat fallback:', err);
      }}

      // 3. Smart Scripted Fallback if no API key or offline
      activeTypingIndicator = null;
      let gemObj = window.getSmartReply ? window.getSmartReply('gemini', text) : {{ text: "흥, 바보 프로듀서! 목표 52kg까지 나만 믿고 따라와! 🐾", sit: 'ev1' }};
      let kotObj = window.getSmartReply ? window.getSmartReply('kotone', text) : {{ text: "헤헤~ 프로듀서님! 코토네가 1등으로 응원할게요! 💛", sit: 'ev1' }};
      let mioObj = window.getSmartReply ? window.getSmartReply('mio', text) : {{ text: "프로듀서 목소리 들으니까 기운 펄펄! 오늘도 파이팅이야~ 🌟", sit: 'ev1' }};

      if (currentMode === 'dual') {{
        setTrainerMode('dual', gemObj.sit || 'ev1');
        state.chatHistory.push({{ sender: 'gemini', name: '제미니', text: gemObj.text, time: curTime }});
        state.chatHistory.push({{ sender: 'kotone', name: '코토네', text: kotObj.text, time: curTime }});
        state.chatHistory.push({{ sender: 'mio', name: '미오', text: mioObj.text, time: curTime }});
      }} else if (currentTrainer === 'kotone') {{
        setTrainerMode('kotone', kotObj.sit || 'ev1');
        state.chatHistory.push({{ sender: 'kotone', name: '코토네', text: kotObj.text, time: curTime }});
      }} else if (currentTrainer === 'mio') {{
        setTrainerMode('mio', mioObj.sit || 'ev1');
        state.chatHistory.push({{ sender: 'mio', name: '미오', text: mioObj.text, time: curTime }});
      }} else {{
        setTrainerMode('gemini', gemObj.sit || 'ev1');
        state.chatHistory.push({{ sender: 'gemini', name: '제미니', text: gemObj.text, time: curTime }});
      }}
      addBondExp(15);
      saveState();
      renderChat();
    }}"""

content = content.replace(old_send_block.replace("\n", "\r\n"), new_send_block.replace("\n", "\r\n"))
content = content.replace(old_send_block, new_send_block)

# 3. Update openWebhookModal and saveWebhook
old_webhook_js = """    function openWebhookModal() {
      document.getElementById('webhookInput').value = state.webhookUrl || '';
      document.getElementById('webhookModal').classList.remove('hidden');
    }
    function closeWebhookModal() {
      document.getElementById('webhookModal').classList.add('hidden');
    }
    function saveWebhook() {
      state.webhookUrl = document.getElementById('webhookInput').value.trim();
      saveState();
      closeWebhookModal();
      alert('디스코드 Webhook 저장 완료!');
    }"""

new_webhook_js = """    function openWebhookModal() {
      document.getElementById('webhookInput').value = state.webhookUrl || '';
      const keyInput = document.getElementById('geminiApiKeyInput');
      if (keyInput) keyInput.value = localStorage.getItem('GEMINI_API_KEY') || '';
      updateGeminiKeyStatusUI();
      document.getElementById('webhookModal').classList.remove('hidden');
    }
    function closeWebhookModal() {
      document.getElementById('webhookModal').classList.add('hidden');
    }
    function saveWebhook() {
      state.webhookUrl = document.getElementById('webhookInput').value.trim();
      const keyInput = document.getElementById('geminiApiKeyInput');
      if (keyInput) {
        const key = keyInput.value.trim();
        if (key) localStorage.setItem('GEMINI_API_KEY', key);
        else localStorage.removeItem('GEMINI_API_KEY');
      }
      updateGeminiKeyStatusUI();
      saveState();
      closeWebhookModal();
      alert('설정이 저장되었습니다!');
    }"""

content = content.replace(old_webhook_js.replace("\n", "\r\n"), new_webhook_js.replace("\n", "\r\n"))
content = content.replace(old_webhook_js, new_webhook_js)

index_path.write_text(content, encoding="utf-8")
print("update_index_hybrid_ai.py finished successfully!")
