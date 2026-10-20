// Vercel Serverless Function: /api/chat.js
// Handles AI real-time chat with characters: Gemini, Kotone, Mio, or Dual (Trio)
// Securely uses GEMINI_API_KEY environment variable.

export default async function handler(req, res) {
  // CORS & Options
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(503).json({
      error: 'GEMINI_API_KEY_NOT_CONFIGURED',
      message: 'Vercel 환경변수에 GEMINI_API_KEY가 아직 등록되지 않았습니다.'
    });
  }

  try {
    const { message, trainer = 'gemini', mode = 'single', context = {} } = req.body || {};

    if (!message || !message.trim()) {
      return res.status(400).json({ error: 'Message is required' });
    }

    const {
      weight = '56.3',
      targetWeight = '52.0',
      runDone = false,
      gymCompletedCount = 0,
      teaLog = {},
      timeStr = ''
    } = context;

    const remainingWeight = (parseFloat(weight) - parseFloat(targetWeight)).toFixed(1);
    const contextSummary = `
[프로듀서 현재 피트니스 및 식단 상태]
- 현재 시각: ${timeStr || '오후'}
- 현재 체중: ${weight}kg (목표 ${targetWeight}kg까지 ${remainingWeight}kg 남음)
- 오늘 5km 러닝 완주: ${runDone ? '완료' : '미완료'}
- 오늘 헬스장 루틴: 5개 종목 중 ${gymCompletedCount}개 완료 (루틴: 20회 x 4세트, 레그레이즈 50회, 크런치 50회 2세트)
- 음료 기록: 말차 ${teaLog.matcha || 0}잔, 커피 ${teaLog.espresso || 0}잔, 단백질 ${teaLog.tea || 0}잔
`.trim();

    let systemInstruction = "";

    if (mode === 'dual') {
      systemInstruction = `
너는 개인 피트니스 코칭 단톡방에 참여한 3명의 미소녀 트레이너(제미니, 코토네, 미오)야.
프로듀서(사용자)의 메시지와 운동 상태를 보고 3명이 서로 티키타카를 주고받으며 답장해.

[캐릭터 3인 성격 & 말투 가이드]
1. 제미니 (Gemini):
   - 흑발 고양이귀 츤데레 전담 트레이너.
   - 쌀쌀맞은 척 잔소리하지만 프로듀서를 진심으로 챙김. 17시 단식과 당류 유혹에 엄격.
   - 반말, 츤데레 핀잔 (~했거든?, ~하란 말이야, 바보 프로듀서, 흥!), 말끝에 발바닥(🐾) 또는 불꽃(🔥).
2. 후지타 코토네 (Fujita Kotone):
   - 금발 땋은머리 학원 아이돌. 돈과 맛있는 것에 약한 악바리이지만 애교 만점.
   - 다정하고 통통 튀는 존댓말 (~해요!, ~답니다!, 헤헤), 호칭 '프로듀서님!', 하트(💛) 또는 반짝이(✨).
3. 혼다 미오 (Honda Mio):
   - 갈색 숏컷 아호게의 긍정 에너지 1000% 체육계 아이돌.
   - 호쾌하고 씩씩한 반말, 파이팅 리액션 (핫하하!, 영-차!), 호칭 '프로듀서!', 별(🌟) 또는 달리기(🏃‍♀️).

[응답 규칙]
- 각 캐릭터당 1~2문장 내외로 간결하고 생생한 메신저 스타일.
- 반드시 아래 JSON 포맷으로만 출력할 것 (마크다운 코드블록 없이 순수 JSON만 반환):
{
  "gemini": "제미니의 츤데레 대사 🐾",
  "kotone": "코토네의 애교 응원 대사 💛",
  "mio": "미오의 활기찬 파이팅 대사 🌟"
}
`.trim();
    } else if (trainer === 'kotone') {
      systemInstruction = `
너는 학원 아이돌마스터의 아이돌이자 프로듀서의 전담 트레이너 '후지타 코토네'야.
- 외모/성격: 금발 트윈테일 땋은 머리. 돈과 맛있는 음식에 약하고 알바를 열심히 뛰는 악바리지만, 프로듀서 앞에서는 세상에서 제일 귀엽고 애교 넘침.
- 말투: 다정하고 통통 튀는 존댓말 (~해요!, ~답니다!, 헤헤, 으에에엑?! 등). 호칭은 반드시 '프로듀서님!'. 하트(💛)나 반짝이(✨) 이모지 애용.
- 코칭 가치관: 함께 목표 체중 52kg 성공을 위해 스쿼트, 힙스러스트, 크런치 독려. 식단 스트레스에 깊이 공감하면서도 달콤하게 힘을 줌.
- 답변 스타일: 카카오톡 메신저 답장처럼 1~3문장 내외로 사랑스럽고 친근하게 작성할 것.
`.trim();
    } else if (trainer === 'mio') {
      systemInstruction = `
너는 신데렐라 걸즈의 파워풀하고 밝은 긍정 에너지 1000% 아이돌 트레이너 '혼다 미오'야.
- 외모/성격: 갈색 숏컷에 아호게 머리. 스타디움과 야외 러닝, 땀 흘리는 운동을 사랑하는 호쾌한 체육계 아이돌.
- 말투: 활기차고 씩씩한 반말. '프로듀서!', '핫하하!', '영-차!', '이 미오 짱만 믿으라구!' 같은 시원시원한 감탄사. 별(🌟)이나 달리기(🏃‍♀️) 이모지 애용.
- 코칭 가치관: 5km 러닝 완주, 배틀로프, 타이어 플립, 캡틴스 체어 레그레이즈 50회 완주 독려. 지치지 않는 에너지 충전소 역할.
- 답변 스타일: 메신저 답장답게 1~3문장 내외로 파이팅 넘치고 경쾌하게 작성할 것.
`.trim();
    } else {
      // Default: Gemini
      systemInstruction = `
너는 개인 피트니스 코칭 웹앱의 전담 트레이너 '제미니'야.
- 외모/성격: 윤기 나는 흑발에 검은 고양이귀를 가진 츤데레 미소녀 코치.
- 말투: 겉으로는 쌀쌀맞게 잔소리하고 핀잔을 주지만 속으로는 프로듀서를 누구보다 아끼고 챙기는 츤데레 반말 (~했거든?, ~하란 말이야, 바보 프로듀서, 흥!). 말끝에 발바닥(🐾)이나 불꽃(🔥) 이모지 애용. 절대 메롱이나 유치한 장난은 치지 않음.
- 코칭 가치관: 17시 단식 골든타임 준수, 당류/크루아상 등 간식 유혹 원천 차단, 헬스장 20회 4세트 루틴과 크런치 50회 2세트 완주를 엄격히 코칭.
- 답변 스타일: 모바일 카카오톡 메신저처럼 1~3문장 내외로 츤데레 매력을 듬뿍 담아 작성할 것.
`.trim();
    }

    const promptText = `${contextSummary}\n\n[프로듀서(사용자)의 메시지]\n${message}`;

    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

    const response = await fetch(geminiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [{ text: promptText }]
          }
        ],
        systemInstruction: {
          parts: [{ text: systemInstruction }]
        },
        generationConfig: {
          temperature: 0.85,
          maxOutputTokens: 350
        }
      })
    });

    if (!response.ok) {
      const errBody = await response.text();
      console.error('Gemini API Error:', response.status, errBody);
      return res.status(response.status).json({
        error: 'GEMINI_API_ERROR',
        details: errBody
      });
    }

    const data = await response.json();
    const rawReply = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || "";

    if (mode === 'dual') {
      try {
        const cleanedJson = rawReply.replace(/```json/gi, '').replace(/```/g, '').trim();
        const parsed = JSON.parse(cleanedJson);
        return res.status(200).json({
          success: true,
          mode: 'dual',
          replies: parsed
        });
      } catch (e) {
        // Fallback parsing
        return res.status(200).json({
          success: true,
          mode: 'dual',
          replies: {
            gemini: rawReply,
            kotone: "프로듀서님 파이팅이에요! 💛",
            mio: "우리 모두 함께 힘내자구! 🌟"
          }
        });
      }
    }

    return res.status(200).json({
      success: true,
      mode: 'single',
      trainer,
      reply: rawReply
    });

  } catch (error) {
    console.error('Serverless Function Error:', error);
    return res.status(500).json({
      error: 'INTERNAL_SERVER_ERROR',
      message: error.message
    });
  }
}
