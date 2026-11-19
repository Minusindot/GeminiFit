import re
from pathlib import Path

index_path = Path("index.html")
content = index_path.read_text(encoding="utf-8")

# 1. Update Webhook Modal to Settings & AI Modal
old_modal = """    <!-- Webhook Modal -->
    <div id="webhookModal" class="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
      <div class="game-card max-w-sm w-full p-5 space-y-3">
        <div class="flex justify-between items-center">
          <h3 class="text-sm font-extrabold">디스코드 Webhook URL 설정</h3>
          <button onclick="closeWebhookModal()" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>
        <input type="url" id="webhookInput" placeholder="https://discord.com/api/webhooks/..." class="w-full sub-box px-3 py-2 text-xs focus:outline-none focus:border-sky-400 font-mono">
        <div class="flex justify-end gap-2 pt-2">
          <button onclick="closeWebhookModal()" class="px-3 py-1.5 text-xs text-slate-500 font-bold">취소</button>
          <button onclick="saveWebhook()" class="px-4 py-1.5 text-xs font-extrabold bg-[#4a89dc] text-white rounded-xl shadow-sm">저장</button>
        </div>
      </div>
    </div>"""

new_modal = """    <!-- Webhook & AI Settings Modal -->
    <div id="webhookModal" class="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
      <div class="game-card max-w-sm w-full p-5 space-y-3.5">
        <div class="flex justify-between items-center pb-2 border-b border-slate-200 dark:border-slate-700">
          <div class="flex items-center gap-1.5">
            <span class="text-sm">⚙️</span>
            <h3 class="text-sm font-black text-slate-800 dark:text-slate-100">환경 & AI 연동 설정</h3>
          </div>
          <button onclick="closeWebhookModal()" class="text-slate-400 hover:text-slate-600 p-1">✕</button>
        </div>

        <!-- 1. Google Gemini AI Serverless Guide -->
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
        </div>

        <!-- 2. Discord Webhook Setting -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1">
            <span>📢</span>
            <span>디스코드 브리핑 Webhook URL</span>
          </label>
          <input type="url" id="webhookInput" placeholder="https://discord.com/api/webhooks/..." class="w-full sub-box px-3 py-2 text-xs focus:outline-none focus:border-sky-400 font-mono">
        </div>

        <div class="flex justify-end gap-2 pt-2 border-t border-slate-200 dark:border-slate-700">
          <button onclick="closeWebhookModal()" class="px-3 py-1.5 text-xs text-slate-500 font-bold">취소</button>
          <button onclick="saveWebhook()" class="px-4 py-1.5 text-xs font-extrabold bg-[#4a89dc] hover:bg-sky-500 text-white rounded-xl shadow-sm transition-all">저장</button>
        </div>
      </div>
    </div>"""

# Normalize CRLF for replacement
content = content.replace(old_modal.replace("\n", "\r\n"), new_modal.replace("\n", "\r\n"))
content = content.replace(old_modal, new_modal)

# 2. Update sendDirectMessage to call /api/chat
old_send_msg = """    function sendDirectMessage() {
      const input = document.getElementById('directChatInput');
      const text = (input.value || '').trim();
      if (!text) return;
      input.value = '';
      playBeep(640, 0.07);

      state.chatHistory.push({ sender: 'user', text, time: getKakaoTimeStr() });
      renderChat();

      triggerTrainerTypingReply(() => {
        let gemObj = window.getSmartReply ? window.getSmartReply('gemini', text) : { text: "흥, 바보 프로듀서! 목표 52kg까지 나만 믿고 따라와! 🐾", sit: 'ev1' };
        let kotObj = window.getSmartReply ? window.getSmartReply('kotone', text) : { text: "헤헤~ 프로듀서님! 코토네가 1등으로 응원할게요! 💛", sit: 'ev1' };
        let mioObj = window.getSmartReply ? window.getSmartReply('mio', text) : { text: "프로듀서 목소리 들으니까 기운 펄펄! 오늘도 파이팅이야~ 🌟", sit: 'ev1' };

        const curTime = getKakaoTimeStr();
        if (state.activeMode === 'dual') {
          setTrainerMode('dual', gemObj.sit || 'ev1');
          state.chatHistory.push({ sender: 'gemini', name: '제미니', text: gemObj.text, time: curTime });
          state.chatHistory.push({ sender: 'kotone', name: '코토네', text: kotObj.text, time: curTime });
          state.chatHistory.push({ sender: 'mio', name: '미오', text: mioObj.text, time: curTime });
        } else if (state.activeTrainer === 'kotone') {
          setTrainerMode('kotone', kotObj.sit || 'ev1');
          state.chatHistory.push({ sender: 'kotone', name: '코토네', text: kotObj.text, time: curTime });
        } else if (state.activeTrainer === 'mio') {
          setTrainerMode('mio', mioObj.sit || 'ev1');
          state.chatHistory.push({ sender: 'mio', name: '미오', text: mioObj.text, time: curTime });
        } else {
          setTrainerMode('gemini', gemObj.sit || 'ev1');
          state.chatHistory.push({ sender: 'gemini', name: '제미니', text: gemObj.text, time: curTime });
        }
        addBondExp(15);
        saveState();
      }, 900);
    }"""

new_send_msg = """    async function sendDirectMessage() {
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

content = content.replace(old_send_msg.replace("\n", "\r\n"), new_send_msg.replace("\n", "\r\n"))
content = content.replace(old_send_msg, new_send_msg)

index_path.write_text(content, encoding="utf-8")
print("apply_ai_chat_update.py finished successfully!")
