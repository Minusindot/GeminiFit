from pathlib import Path

index_path = Path("index.html")
content = index_path.read_text(encoding="utf-8")

old_code = """    async function testGeminiApiKey() {
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

new_code = """    async function fetchGeminiWithFallback(apiKey, bodyPayload) {
      const endpoints = [
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',
        'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent',
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent',
        'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent'
      ];

      let lastError = null;
      for (const base of endpoints) {
        try {
          const res = await fetch(`${base}?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyPayload)
          });
          if (res.ok) {
            return await res.json();
          }
          const errData = await res.json().catch(() => ({}));
          const errMsg = errData.error?.message || ('HTTP ' + res.status);
          lastError = new Error(errMsg);
          if (res.status === 404 || errMsg.toLowerCase().includes('not found') || errMsg.toLowerCase().includes('not supported')) {
            continue;
          }
          throw lastError;
        } catch (e) {
          lastError = e;
          if (e.message && (e.message.toLowerCase().includes('not found') || e.message.toLowerCase().includes('not supported'))) {
            continue;
          }
          throw e;
        }
      }
      throw lastError || new Error('사용 가능한 Gemini 모델 엔드포인트를 찾지 못했습니다.');
    }

    async function testGeminiApiKey() {
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
        const data = await fetchGeminiWithFallback(key, {
          contents: [{ role: 'user', parts: [{ text: '안녕! 제미니 트레이너로서 한국어로 한 문장 인사해줘.' }] }]
        });
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
      const systemPrompt = getGeminiSystemPrompt(trainer, mode);
      const remaining = (parseFloat(context.weight) - parseFloat(context.targetWeight)).toFixed(1);
      const promptWithContext = `[프로듀서 현재 피트니스 상태]\\n- 현재 시각: ${context.timeStr}\\n- 현재 체중: ${context.weight}kg (목표 ${context.targetWeight}kg까지 ${remaining}kg 남음)\\n- 오늘 5km 러닝: ${context.runDone ? '완료' : '미완료'}\\n- 오늘 헬스장 루틴: 5개 종목 중 ${context.gymCompletedCount}개 완료\\n- 음료: 말차 ${context.teaLog?.matcha || 0}잔, 커피 ${context.teaLog?.espresso || 0}잔, 단백질 ${context.teaLog?.tea || 0}잔\\n\\n[프로듀서의 메시지]\\n${userText}`;

      const data = await fetchGeminiWithFallback(apiKey, {
        contents: [{ role: 'user', parts: [{ text: promptWithContext }] }],
        systemInstruction: { parts: [{ text: systemPrompt }] },
        generationConfig: { temperature: 0.85, maxOutputTokens: 350 }
      });

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

content = content.replace(old_code.replace("\n", "\r\n"), new_code.replace("\n", "\r\n"))
content = content.replace(old_code, new_code)

index_path.write_text(content, encoding="utf-8")
print("apply_multi_endpoint_fix.py finished successfully!")
