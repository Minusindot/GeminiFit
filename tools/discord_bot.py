#!/usr/bin/env python3
"""
GeminiFit Unattended Discord Webhook Notifier
Runs via GitHub Actions (or locally) to send:
  1. morning : 어제 요약 + 코토노하 오답/진도 기반 ||스포일러|| 10초 일본어 퀴즈 + 트레이너 아바타 연동
  2. evening : 조건부 밤 스트릭 보호 스마트 넛지 (오늘 기록/코토노하 학습이 비어있을 때만 발송)
  3. weekly  : 일요일 저녁 주간 결산 + Matplotlib 다크 테마 미니 그래프 (체중/체지방 추이 + 주간 습관 달성률)
"""

from __future__ import annotations

import argparse
import io
import json
import os
import random
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Constants & Paths
# ---------------------------------------------------------------------------
KST = timezone(timedelta(hours=9))
REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = REPO_ROOT / "state.json"
NOTIFY_STATE_PATH = REPO_ROOT / "tools" / "discord_notify_state.json"
KOTONOHA_PATH = REPO_ROOT / "kotonoha_data.js"
APP_URL = "https://minusindot.github.io/GeminiFit/"

TRAINERS: dict[str, dict[str, Any]] = {
    "kotone": {
        "name": "코토네",
        "bot_name": "코토네 · GeminiFit 조교",
        "avatar": f"{APP_URL}image/02%20kotone/avatar_kotone.png",
        "color": 0xFBBF24,
        "emoji": "💛",
        "morning_greetings": [
            "좋은 아침이에요, 프로듀서님! ☀️ 오늘도 알차게 루틴 챙겨서 특급 칭찬 받아가세요~ 💛",
            "프로듀서님~ 기상 완료! 🌅 어제 기록 체크하고 오늘도 상쾌하게 출발해 봐요! 💛",
            "안뇨옹~ 프로듀서님! ✨ 오늘 하루도 코토네가 옆에서 팍팍 응원할게요! 💛",
        ],
        "nudge_both": "프로듀서님~ 벌써 밤이에요! 🌙 오늘 건강 기록이랑 코토노하 학습이 아직 비어있어요. 자정 전에 딱 1분만 들러서 스트릭 지켜주세요! 💛",
        "nudge_koto": "오늘 루틴 챙기신 건 최고인데, 코토노하 일본어 스트릭이 아직이에요! 🍵 자정 전에 10초만 투자해서 연속 기록 지켜요! 💛",
        "nudge_fit": "코토노하 학습은 벌써 완료하셨네요! 대단해요~ 👏 오늘 식단/물/운동 기록만 10초 컷으로 남겨두면 완벽해요! 💛",
    },
    "mio": {
        "name": "미오",
        "bot_name": "미오 · GeminiFit 러닝 파트너",
        "avatar": f"{APP_URL}image/01%20mio/avatar_mio.png",
        "color": 0xF472B6,
        "emoji": "🌟",
        "morning_greetings": [
            "야호~! 프로듀서, 좋은 아침! ☀️ 오늘도 기분 좋게 몸 깨우고 달려보자구! 🌟",
            "프로듀서 일어났어?! 🌅 어제 기록 돌아보고 오늘도 텐션 업업!! 🌟",
            "굿모닝 프로듀서! ✨ 물 한 잔 쭉 마시고 오늘 루틴 스타트! 🌟",
        ],
        "nudge_both": "어이 프로듀서! 🌙 오늘 기록이랑 코토노하 아직 안 찍혔어! 스트릭 끊기면 아깝잖아, 지금 바로 1분 컷 가자!! 🌟",
        "nudge_koto": "오늘 운동이랑 식단 챙긴 거 완전 나이스! 👍 근데 코토노하 스트릭이 위험해! 자기 전에 딱 한 문제만 풀고 자자! 🌟",
        "nudge_fit": "코토노하 공부 완료했구나! 짱이야~ ✨ 오늘 먹은 거랑 물 마신 것만 GeminiFit에 쓱 남겨두자! 🌟",
    },
    "gemini": {
        "name": "제미니",
        "bot_name": "제미니 · GeminiFit 교토 사범",
        "avatar": f"{APP_URL}image/03%20gemini/avatar_gemini.png",
        "color": 0xC084FC,
        "emoji": "🌸",
        "morning_greetings": [
            "프로듀서님, 오하요 도스~🍵 오늘도 차분하고 우아하게 몸과 마음을 가꾸시와요 🌸",
            "좋은 아침이옵니다, 프로듀서님 🌅 어제의 발자취를 살피고 오늘도 오키바리야스! 🌸",
            "어서 오시어요, 프로듀서님~ ☀️ 따뜻한 물 한 잔과 함께 오늘을 열어보시와요 🌸",
        ],
        "nudge_both": "프로듀서님, 밤이 깊었사옵니다 🌙 오늘의 기록과 코토노하 다실 출석이 아직이시와요. 자정 전에 잠시 들러 스트릭을 지키시어요 🌸",
        "nudge_koto": "오늘 몸 관리는 훌륭하셨사옵니다 🍵 허나 코토노하 다실에 발걸음이 없으셨사와요! 스트릭이 꺼지기 전에 잠시 들르시와요 🌸",
        "nudge_fit": "코토노하 다실 출석은 참으로 기특하옵니다 🌸 오늘의 식단과 운동 기록도 잊지 말고 남겨두시와요 🐾",
    },
}

NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]


# ---------------------------------------------------------------------------
# Data Loading & Helpers
# ---------------------------------------------------------------------------
def load_state() -> dict[str, Any]:
    with STATE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_kotonoha_lessons() -> list[dict[str, Any]]:
    raw = KOTONOHA_PATH.read_text(encoding="utf-8")
    m = re.search(r"window\.KOTONOHA_LESSONS\s*=\s*(\[.*\]);", raw, re.S)
    if not m:
        raise ValueError("Could not parse window.KOTONOHA_LESSONS from kotonoha_data.js")
    return json.loads(m.group(1))


def get_trainer(state: dict[str, Any]) -> dict[str, Any]:
    key = str(state.get("activeTrainer") or "kotone").lower()
    return TRAINERS.get(key, TRAINERS["kotone"])


def strip_ruby(text: str, keep_reading: bool = True) -> str:
    """Convert <ruby>漢字<rt>かんじ</rt></ruby> into 漢字(かんじ) or 漢字."""
    if not text:
        return ""
    if keep_reading:
        cleaned = re.sub(r"<ruby>([^<]+)<rt>([^<]+)</rt></ruby>", r"\1(\2)", text)
    else:
        cleaned = re.sub(r"<ruby>([^<]+)<rt>[^<]+</rt></ruby>", r"\1", text)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    return cleaned.strip()


def parse_ymd(s: str) -> date | None:
    try:
        return date.fromisoformat(str(s)[:10])
    except Exception:
        return None


def fmt_delta(cur: float | None, prev: float | None, unit: str) -> str:
    if cur is None:
        return "기록 없음"
    if prev is None:
        return f"**{cur:.1f}{unit}**"
    diff = cur - prev
    if abs(diff) < 0.05:
        return f"**{cur:.1f}{unit}** (±0.0)"
    sign = "+" if diff > 0 else ""
    return f"**{cur:.1f}{unit}** ({sign}{diff:.1f})"


def collect_body_metrics(state: dict[str, Any]) -> dict[str, tuple[float | None, float | None]]:
    """
    Merge dailyLogs + inbodyHistory into {YYYY-MM-DD: (weight, fat)}.
    inbodyHistory takes precedence on the same date because it is measured OCR data.
    """
    metrics: dict[str, tuple[float | None, float | None]] = {}
    daily_logs = state.get("dailyLogs") or {}
    for d_str, log in daily_logs.items():
        if not parse_ymd(d_str) or not isinstance(log, dict):
            continue
        w = log.get("weight")
        f_val = log.get("fat")
        w_num = float(w) if isinstance(w, (int, float)) and w > 0 else None
        f_num = float(f_val) if isinstance(f_val, (int, float)) and f_val > 0 else None
        if w_num is not None or f_num is not None:
            metrics[d_str] = (w_num, f_num)

    for entry in state.get("inbodyHistory") or []:
        d_str = str(entry.get("date") or "")[:10]
        if not parse_ymd(d_str):
            continue
        w = entry.get("weight")
        f_val = entry.get("fat")
        w_num = float(w) if isinstance(w, (int, float)) and w > 0 else None
        f_num = float(f_val) if isinstance(f_val, (int, float)) and f_val > 0 else None
        if w_num is not None or f_num is not None:
            metrics[d_str] = (w_num, f_num)

    return dict(sorted(metrics.items()))


def get_day_gym(state: dict[str, Any], target_date: str) -> list[dict[str, Any]]:
    return [g for g in (state.get("gymHistory") or []) if str(g.get("fullDate") or "")[:10] == target_date]


def get_day_runs(state: dict[str, Any], target_date: str) -> list[dict[str, Any]]:
    return [r for r in (state.get("runningLogs") or []) if str(r.get("date") or "")[:10] == target_date]


def has_day_fitness_activity(state: dict[str, Any], target_date: str) -> bool:
    """Check whether any fitness/diet/hydration/rehab activity was recorded on target_date."""
    daily_logs = state.get("dailyLogs") or {}
    log = daily_logs.get(target_date)
    if isinstance(log, dict):
        tea = log.get("teaLog") or {}
        if (
            int(log.get("mealsDone") or 0) > 0
            or len(log.get("mealLogs") or []) > 0
            or bool(log.get("runDone"))
            or bool(log.get("absDone"))
            or bool(log.get("gymDone"))
            or int(log.get("rehabDone") or 0) > 0
            or any(int(tea.get(k) or 0) > 0 for k in ("water", "matcha", "espresso", "tea"))
        ):
            return True

    if str(state.get("lastActiveDate") or "")[:10] == target_date:
        tea = state.get("teaLog") or {}
        gym_routine = state.get("gymRoutine") or {}
        gym_any_set = bool(gym_routine.get("allDone")) or any(
            any(item.get("sets") or [])
            for item in (gym_routine.get("items") or [])
            if isinstance(item, dict)
        )
        if (
            any(state.get("meals") or [])
            or len(state.get("mealLogs") or []) > 0
            or bool(state.get("runDone"))
            or bool(state.get("absDone"))
            or any(state.get("rehab") or [])
            or gym_any_set
            or any(int(tea.get(k) or 0) > 0 for k in ("water", "matcha", "espresso", "tea"))
        ):
            return True

    if get_day_gym(state, target_date) or get_day_runs(state, target_date):
        return True

    for entry in state.get("inbodyHistory") or []:
        if str(entry.get("date") or "")[:10] == target_date:
            return True

    return False


def has_day_kotonoha_activity(state: dict[str, Any], target_date: str) -> bool:
    koto = state.get("kotonoha") or {}
    return str(koto.get("lastStudyDate") or "")[:10] == target_date


# ---------------------------------------------------------------------------
# Kotonoha 10-Second Quiz Selector
# ---------------------------------------------------------------------------
def select_daily_quiz(state: dict[str, Any], lessons: list[dict[str, Any]], today: date) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """
    Pick one quiz prioritizing:
      1. Kotonoha wrongWords (오답 복습)
      2. Active / next lesson or completed lessons (진도 복습/예습)
    Returns (badge_label, lesson_dict, quiz_dict).
    """
    koto = state.get("kotonoha") or {}
    wrong_words = [str(w).strip() for w in (koto.get("quizStats") or {}).get("wrongWords") or [] if str(w).strip()]
    completed_ids = set(koto.get("completedLessons") or [])
    active_idx = int(koto.get("activeLessonIdx") or 0)

    # 1) Wrong-word matched quizzes
    wrong_pool: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for lesson in lessons:
        for q in lesson.get("quizzes") or []:
            tw = str(q.get("targetWord") or "")
            if any(w == tw or w in tw for w in wrong_words):
                wrong_pool.append((lesson, q))

    day_seed = today.toordinal()

    # If there are wrong words, serve them 2 out of 3 days and progress quiz 1 out of 3 days
    # (or always if progress pool is empty) so wrong words get strong spaced repetition without feeling stuck.
    progress_pool: list[tuple[dict[str, Any], dict[str, Any]]] = []
    if 0 <= active_idx < len(lessons):
        for q in lessons[active_idx].get("quizzes") or []:
            progress_pool.append((lessons[active_idx], q))
    for lesson in lessons:
        if lesson.get("id") in completed_ids:
            for q in lesson.get("quizzes") or []:
                progress_pool.append((lesson, q))
    if not progress_pool:
        for lesson in lessons:
            for q in lesson.get("quizzes") or []:
                progress_pool.append((lesson, q))

    if wrong_pool and (day_seed % 3 != 2 or not progress_pool):
        lesson, quiz = wrong_pool[day_seed % len(wrong_pool)]
        ep = lesson.get("epCode") or lesson.get("id")
        return f"🎯 오답 복습 · 제{ep}화", lesson, quiz

    lesson, quiz = progress_pool[day_seed % len(progress_pool)]
    ep = lesson.get("epCode") or lesson.get("id")
    is_completed = lesson.get("id") in completed_ids
    tag = "📖 진도 복습" if is_completed else "✨ 다음 레슨 예습"
    return f"{tag} · 제{ep}화", lesson, quiz


def _strip_quiz_reading(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", str(text or ""))
    s = re.sub(r"（[^）]*）|\([^)]*\)", "", s)
    s = re.sub(r"[\s\u3000~〜\-－·.。、/／!?！？]", "", s)
    return s


def format_quiz_block(
    badge: str,
    lesson: dict[str, Any],
    quiz: dict[str, Any],
    today: date | None = None,
) -> str:
    q_type = str(quiz.get("type") or "퀴즈")
    is_reading_quiz = "읽기" in q_type
    prompt_jp = strip_ruby(str(quiz.get("promptJp") or ""), keep_reading=not is_reading_quiz)
    prompt_ko = strip_ruby(str(quiz.get("promptKo") or ""), keep_reading=not is_reading_quiz)
    target_word = str(quiz.get("targetWord") or "")
    target_sub = strip_ruby(str(quiz.get("targetSub") or ""), keep_reading=not is_reading_quiz)

    raw_options = list(quiz.get("options") or [])
    raw_ans_idx = int(quiz.get("answerIndex") or 0)
    if raw_options:
        tagged = [(opt, i == raw_ans_idx) for i, opt in enumerate(raw_options)]
        seed_str = f"{today.isoformat() if today else ''}|{lesson.get('id', '')}|{prompt_jp}|{target_word}"
        rng = random.Random(seed_str)
        rng.shuffle(tagged)
        options = [opt for opt, _ in tagged]
        ans_idx = next((i for i, (_, is_ans) in enumerate(tagged) if is_ans), 0)
    else:
        options = []
        ans_idx = 0

    ans_text = options[ans_idx] if 0 <= ans_idx < len(options) else ""
    explanation = strip_ruby(str(quiz.get("explanation") or ""), keep_reading=True)

    # Avoid leaking the answer when targetWord is identical to or contained in the correct option
    tw_clean = _strip_quiz_reading(target_word)
    ans_clean = _strip_quiz_reading(ans_text)
    keyword_exposes_answer = bool(tw_clean and ans_clean and (tw_clean in ans_clean or ans_clean in tw_clean))

    lines = [f"**[{badge} · {q_type}]**"]
    if target_word and not keyword_exposes_answer and target_word not in prompt_jp and target_word not in prompt_ko:
        lines.append(f"> 키워드: **{target_word}**")
    if prompt_jp and prompt_jp != prompt_ko:
        lines.append(f"> {prompt_jp}")
    if prompt_ko:
        lines.append(f"> {prompt_ko}")
    if target_sub:
        lines.append(f"> _{target_sub}_")

    if options:
        opt_lines = [
            f"{NUMBER_EMOJIS[i] if i < len(NUMBER_EMOJIS) else f'{i+1}.'} {opt}"
            for i, opt in enumerate(options)
        ]
        lines.append("\n".join(opt_lines))

    lines.append(f"\n정답: ||{ans_idx + 1}번 · {ans_text}||")
    if explanation:
        lines.append(f"해설: ||{explanation}||")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Mode 1: Morning Briefing + 10-sec Japanese
# ---------------------------------------------------------------------------
def build_morning_payload(state: dict[str, Any], lessons: list[dict[str, Any]], today: date) -> dict[str, Any]:
    trainer = get_trainer(state)
    yesterday = today - timedelta(days=1)
    y_str = yesterday.isoformat()

    daily_logs = state.get("dailyLogs") or {}
    y_log = daily_logs.get(y_str)
    summary_date_label = f"어제 ({yesterday.strftime('%m/%d')})"

    # Fallback if yesterday wasn't archived into dailyLogs yet, but lastActiveDate == yesterday
    if not y_log and str(state.get("lastActiveDate") or "")[:10] == y_str:
        y_log = {
            "weight": state.get("weight"),
            "fat": state.get("fat"),
            "mealsDone": sum(1 for m in (state.get("meals") or []) if m),
            "mealLogs": state.get("mealLogs") or [],
            "runDone": bool(state.get("runDone")),
            "absDone": bool(state.get("absDone")),
            "rehabDone": sum(1 for r in (state.get("rehab") or []) if r),
            "gymDone": bool((state.get("gymRoutine") or {}).get("allDone")),
            "teaLog": state.get("teaLog") or {},
        }

    # Body metrics comparison
    metrics = collect_body_metrics(state)
    metric_dates = list(metrics.keys())
    cur_w = float(state.get("weight")) if isinstance(state.get("weight"), (int, float)) else None
    cur_f = float(state.get("fat")) if isinstance(state.get("fat"), (int, float)) else None
    prev_w, prev_f = None, None
    if y_str in metrics:
        cur_w, cur_f = metrics[y_str]
        idx = metric_dates.index(y_str)
        if idx > 0:
            prev_w, prev_f = metrics[metric_dates[idx - 1]]
    elif len(metric_dates) >= 2:
        cur_w, cur_f = metrics[metric_dates[-1]]
        prev_w, prev_f = metrics[metric_dates[-2]]

    # Build yesterday summary text
    if y_log:
        meals_done = int(y_log.get("mealsDone") or 0)
        meal_names = [m.get("name") for m in (y_log.get("mealLogs") or []) if isinstance(m, dict) and m.get("name")]
        meal_str = f"**{meals_done}/3끼**" + (f" ({', '.join(meal_names[:2])})" if meal_names else "")

        tea = y_log.get("teaLog") or {}
        drinks = []
        if tea.get("water"):
            drinks.append(f"물 {tea['water']}")
        if tea.get("espresso"):
            drinks.append(f"커피 {tea['espresso']}")
        if tea.get("matcha"):
            drinks.append(f"말차 {tea['matcha']}")
        if tea.get("tea"):
            drinks.append(f"티/단백질 {tea['tea']}")
        drink_str = " · ".join(drinks) if drinks else "기록 없음"

        y_gyms = get_day_gym(state, y_str)
        y_runs = get_day_runs(state, y_str)
        workouts = []
        if y_gyms:
            tot_sets = sum(int(g.get("totalSets") or 0) for g in y_gyms)
            tot_reps = sum(int(g.get("totalReps") or 0) for g in y_gyms)
            workouts.append(f"🏋️ 헬스 {tot_sets}세트({tot_reps}회)")
        elif y_log.get("gymDone"):
            workouts.append("🏋️ 헬스 완료")
        if y_runs:
            tot_km = sum(float(r.get("distance") or 0) for r in y_runs)
            src = y_runs[0].get("source") or "유산소"
            workouts.append(f"🏃 {src} {tot_km:.1f}km")
        elif y_log.get("runDone"):
            workouts.append("🏃 유산소 완료")
        if y_log.get("absDone"):
            workouts.append("🔥 복근 완료")
        if int(y_log.get("rehabDone") or 0) > 0:
            workouts.append(f"🩹 재활 {y_log['rehabDone']}세트")
        workout_str = "\n".join(f"• {w}" for w in workouts) if workouts else "• 휴식일 (또는 미기록)"

        yesterday_summary = (
            f"• 식단: {meal_str}\n"
            f"• 음료: {drink_str}\n"
            f"{workout_str}"
        )
    else:
        last_active = state.get("lastActiveDate") or "미기록"
        yesterday_summary = (
            f"어제({yesterday.strftime('%m/%d')})는 아직 기록이 비어있어요!\n"
            f"• 최근 기록일: **{last_active}**\n"
            f"• 오늘은 물 한 잔부터 가볍게 시작해 볼까요? 💧"
        )

    # Kotonoha stats & 10-sec quiz
    koto = state.get("kotonoha") or {}
    streak = int(koto.get("streak") or 0)
    q_stats = koto.get("quizStats") or {}
    q_total = int(q_stats.get("total") or 0)
    q_correct = int(q_stats.get("correct") or 0)
    acc = (q_correct / q_total * 100.0) if q_total > 0 else 0.0
    wrong_cnt = len(q_stats.get("wrongWords") or [])

    badge, lesson, quiz = select_daily_quiz(state, lessons, today)
    quiz_text = format_quiz_block(badge, lesson, quiz, today=today)

    greeting = trainer["morning_greetings"][today.toordinal() % len(trainer["morning_greetings"])]
    bond_rank = state.get("bondRank", 1)
    bond_exp = state.get("bondExp", 0)

    embed = {
        "author": {
            "name": f"GEMINI FIT · MORNING BRIEFING ({today.strftime('%Y.%m.%d')})",
            "url": APP_URL,
            "icon_url": trainer["avatar"],
        },
        "title": f"☀️ {today.strftime('%m월 %d일')} 모닝 브리핑 & 10초 일본어",
        "description": f"**{trainer['name']}:** \"{greeting}\"",
        "color": trainer["color"],
        "thumbnail": {"url": trainer["avatar"]},
        "fields": [
            {
                "name": "⚖️ 최근 바디 체크",
                "value": f"체중 {fmt_delta(cur_w, prev_w, 'kg')}\n체지방 {fmt_delta(cur_f, prev_f, '%')}",
                "inline": True,
            },
            {
                "name": "🔥 코토노하 현황",
                "value": f"스트릭: **{streak}일 연속**\n정답률: **{acc:.1f}%** ({q_correct}/{q_total})\n오답 노트: **{wrong_cnt}개**",
                "inline": True,
            },
            {
                "name": f"📋 {summary_date_label} 요약",
                "value": yesterday_summary,
                "inline": False,
            },
            {
                "name": "🍵 오늘의 10초 일본어 (클릭해서 정답 확인!)",
                "value": quiz_text[:1024],
                "inline": False,
            },
            {
                "name": "🚀 바로가기",
                "value": f"[GeminiFit 앱 열기]({APP_URL}) — 오늘 첫 기록 남기고 스트릭 이어가기!",
                "inline": False,
            },
        ],
        "footer": {
            "text": f"인연 랭크 Lv.{bond_rank} ({bond_exp}%) · 담당 트레이너: {trainer['name']} {trainer['emoji']}",
            "icon_url": TRAINERS["gemini"]["avatar"],
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return {
        "username": trainer["bot_name"],
        "avatar_url": trainer["avatar"],
        "embeds": [embed],
    }


# ---------------------------------------------------------------------------
# Mode 2: Evening Streak Protection Smart Nudge (Conditional)
# ---------------------------------------------------------------------------
def build_evening_payload(
    state: dict[str, Any], today: date, force: bool = False
) -> dict[str, Any] | None:
    t_str = today.isoformat()
    fit_done = has_day_fitness_activity(state, t_str)
    koto_done = has_day_kotonoha_activity(state, t_str)

    if fit_done and koto_done and not force:
        return None

    trainer = get_trainer(state)
    koto = state.get("kotonoha") or {}
    streak = int(koto.get("streak") or 0)

    if not fit_done and not koto_done:
        msg = trainer["nudge_both"]
        title = "🌙 스트릭 보호 알림 · 오늘 기록 & 코토노하 대기 중!"
        color = 0xF59E0B
    elif not koto_done:
        msg = trainer["nudge_koto"]
        title = f"🔥 코토노하 {streak}일 스트릭 보호 알림!"
        color = 0xEF4444
    elif not fit_done:
        msg = trainer["nudge_fit"]
        title = "📝 오늘 건강/식단 기록이 아직 비어있어요!"
        color = trainer["color"]
    else:
        # Only reachable when --force is passed while both are done
        msg = f"오늘 기록과 코토노하 모두 완료하셨어요! (테스트 강제 발송) {trainer['emoji']}"
        title = "✅ [테스트] 오늘 루틴 올클리어!"
        color = 0x10B981

    checklist = (
        f"{'✅' if fit_done else '❌'} **오늘 건강/식단/운동 기록** "
        f"({'완료!' if fit_done else '미기록 — 물/식단 10초 컷 추천'})\n"
        f"{'✅' if koto_done else '❌'} **코토노하 일본어 학습** "
        f"({'완료!' if koto_done else f'미완료 — 현재 🔥{streak}일 연속 스트릭'})"
    )

    embed = {
        "author": {
            "name": f"GEMINI FIT · SMART NUDGE ({today.strftime('%Y.%m.%d')})",
            "url": APP_URL,
            "icon_url": trainer["avatar"],
        },
        "title": title,
        "description": f"**{trainer['name']}:** \"{msg}\"",
        "color": color,
        "thumbnail": {"url": trainer["avatar"]},
        "fields": [
            {"name": "📌 오늘 체크리스트", "value": checklist, "inline": False},
            {
                "name": "⚡ 1분 만에 스트릭 지키기",
                "value": f"[GeminiFit 바로 열기]({APP_URL})",
                "inline": False,
            },
        ],
        "footer": {
            "text": "오늘 기록과 코토노하가 모두 완료되면 이 알림은 자동으로 쉬어갑니다 💤",
            "icon_url": trainer["avatar"],
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return {
        "username": trainer["bot_name"],
        "avatar_url": trainer["avatar"],
        "embeds": [embed],
    }


# ---------------------------------------------------------------------------
# Mode 3: Sunday Weekly Summary + Matplotlib Dark Theme Mini Chart
# ---------------------------------------------------------------------------
def configure_korean_font() -> str | None:
    import matplotlib
    from matplotlib import font_manager

    preferred = [
        "NanumGothic",
        "NanumBarunGothic",
        "Malgun Gothic",
        "AppleGothic",
        "Noto Sans CJK KR",
        "Noto Sans KR",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in available:
            matplotlib.rcParams["font.family"] = name
            matplotlib.rcParams["axes.unicode_minus"] = False
            return name
    matplotlib.rcParams["axes.unicode_minus"] = False
    return None


def compute_weekly_stats(state: dict[str, Any], today: date) -> dict[str, Any]:
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    week_strs = [d.isoformat() for d in week_dates]
    daily_logs = state.get("dailyLogs") or {}

    meal_days = 0
    total_meals = 0
    hydration_days = 0
    cardio_days = 0
    total_cardio_km = 0.0
    gym_days = 0
    total_gym_sets = 0
    total_gym_reps = 0
    rehab_days = 0
    abs_days = 0

    for d_str in week_strs:
        log = daily_logs.get(d_str) or {}
        if not log and str(state.get("lastActiveDate") or "")[:10] == d_str:
            log = {
                "mealsDone": sum(1 for m in (state.get("meals") or []) if m),
                "mealLogs": state.get("mealLogs") or [],
                "runDone": bool(state.get("runDone")),
                "absDone": bool(state.get("absDone")),
                "rehabDone": sum(1 for r in (state.get("rehab") or []) if r),
                "gymDone": bool((state.get("gymRoutine") or {}).get("allDone")),
                "teaLog": state.get("teaLog") or {},
            }

        m_cnt = max(int(log.get("mealsDone") or 0), len(log.get("mealLogs") or []))
        if m_cnt > 0:
            meal_days += 1
            total_meals += m_cnt

        tea = log.get("teaLog") or {}
        if any(int(tea.get(k) or 0) > 0 for k in ("water", "matcha", "espresso", "tea")):
            hydration_days += 1

        runs = get_day_runs(state, d_str)
        if runs or bool(log.get("runDone")):
            cardio_days += 1
            total_cardio_km += sum(float(r.get("distance") or 0) for r in runs)

        gyms = get_day_gym(state, d_str)
        if gyms or bool(log.get("gymDone")):
            gym_days += 1
            total_gym_sets += sum(int(g.get("totalSets") or 0) for g in gyms)
            total_gym_reps += sum(int(g.get("totalReps") or 0) for g in gyms)

        if int(log.get("rehabDone") or 0) > 0:
            rehab_days += 1
        if bool(log.get("absDone")):
            abs_days += 1

    # Body metrics trend (up to last 14 recorded points within 35 days, fallback to all points)
    all_metrics = collect_body_metrics(state)
    cutoff = (today - timedelta(days=35)).isoformat()
    recent_metrics = [(d, v) for d, v in all_metrics.items() if cutoff <= d <= today.isoformat()]
    if len(recent_metrics) < 3:
        recent_metrics = list(all_metrics.items())[-12:]
    else:
        recent_metrics = recent_metrics[-14:]

    weights = [(d, v[0]) for d, v in recent_metrics if v[0] is not None]
    fats = [(d, v[1]) for d, v in recent_metrics if v[1] is not None]

    week_start_str = week_strs[0]
    week_weights = [w for d, w in weights if d >= week_start_str]
    week_fats = [f for d, f in fats if d >= week_start_str]

    habits = [
        {"label": "식단 기록", "done": meal_days, "target": 7, "unit": "일", "color": "#FBBF24"},
        {"label": "수분·티 로그", "done": hydration_days, "target": 7, "unit": "일", "color": "#38BDF8"},
        {"label": "헬스 근력", "done": gym_days, "target": 3, "unit": "회", "color": "#C084FC"},
        {"label": "유산소·러닝", "done": cardio_days, "target": 3, "unit": "회", "color": "#F472B6"},
        {"label": "엘보 재활", "done": rehab_days, "target": 5, "unit": "일", "color": "#34D399"},
    ]

    overall_rate = sum(min(h["done"] / h["target"], 1.0) for h in habits) / len(habits) * 100.0

    return {
        "week_start": week_dates[0],
        "week_end": week_dates[-1],
        "meal_days": meal_days,
        "total_meals": total_meals,
        "hydration_days": hydration_days,
        "cardio_days": cardio_days,
        "total_cardio_km": total_cardio_km,
        "gym_days": gym_days,
        "total_gym_sets": total_gym_sets,
        "total_gym_reps": total_gym_reps,
        "rehab_days": rehab_days,
        "abs_days": abs_days,
        "weights": weights,
        "fats": fats,
        "week_weights": week_weights,
        "week_fats": week_fats,
        "habits": habits,
        "overall_rate": overall_rate,
    }


def render_weekly_chart(stats: dict[str, Any], out_path: Path | None = None) -> bytes:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    configure_korean_font()

    bg_outer = "#1E1F22"
    bg_card = "#2B2D31"
    text_main = "#F2F3F5"
    text_muted = "#B5BAC1"
    grid_color = "#3F4147"
    weight_color = "#38BDF8"
    fat_color = "#F472B6"

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.5, 4.4), dpi=160, gridspec_kw={"width_ratios": [1.25, 1.0]}
    )
    fig.patch.set_facecolor(bg_outer)
    fig.subplots_adjust(left=0.07, right=0.96, top=0.82, bottom=0.16, wspace=0.28)

    period_title = f"GeminiFit 주간 리포트  ({stats['week_start'].strftime('%m/%d')} ~ {stats['week_end'].strftime('%m/%d')})"
    fig.suptitle(period_title, color=text_main, fontsize=14, fontweight="bold", x=0.07, ha="left", y=0.95)

    # --- Panel 1: Weight & Body Fat Trend ---
    ax1.set_facecolor(bg_card)
    for spine in ("top", "right"):
        ax1.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax1.spines[spine].set_color(grid_color)

    weights = stats["weights"]
    fats = stats["fats"]

    if weights:
        x_idx = list(range(len(weights)))
        x_labels = [d[5:].replace("-", "/") for d, _ in weights]
        y_w = [w for _, w in weights]

        ax1.plot(x_idx, y_w, color=weight_color, linewidth=2.4, marker="o", markersize=5.5, label="체중 (kg)", zorder=4)
        w_min, w_max = min(y_w), max(y_w)
        pad = max((w_max - w_min) * 0.35, 0.8)
        ax1.set_ylim(w_min - pad, w_max + pad)
        ax1.fill_between(x_idx, y_w, w_min - pad, color=weight_color, alpha=0.12, zorder=2)

        # Annotate first and last weight points
        ax1.annotate(
            f"{y_w[-1]:.1f}kg",
            xy=(x_idx[-1], y_w[-1]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            color=weight_color,
            fontsize=8.5,
            fontweight="bold",
        )
        if len(y_w) > 1:
            ax1.annotate(
                f"{y_w[0]:.1f}",
                xy=(x_idx[0], y_w[0]),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center",
                color=text_muted,
                fontsize=8,
            )

        # Show thin x-ticks so labels never overlap
        step = max(1, len(x_labels) // 5)
        tick_pos = list(range(0, len(x_labels), step))
        last_idx = len(x_labels) - 1
        if last_idx not in tick_pos:
            if tick_pos and (last_idx - tick_pos[-1]) <= 1:
                tick_pos[-1] = last_idx
            else:
                tick_pos.append(last_idx)
        ax1.set_xticks(tick_pos)
        ax1.set_xticklabels([x_labels[i] for i in tick_pos], color=text_muted, fontsize=8.5)
        ax1.tick_params(axis="y", colors=weight_color, labelsize=8.5)
        ax1.grid(axis="y", color=grid_color, linestyle="--", linewidth=0.7, alpha=0.7)

        # Secondary axis for body fat
        fat_map = dict(fats)
        fat_pts = [(i, fat_map[d]) for i, (d, _) in enumerate(weights) if d in fat_map]
        lines_for_legend = ax1.get_lines()
        if fat_pts:
            ax1_r = ax1.twinx()
            ax1_r.spines["top"].set_visible(False)
            ax1_r.spines["left"].set_visible(False)
            ax1_r.spines["bottom"].set_visible(False)
            ax1_r.spines["right"].set_color(grid_color)

            fx = [p[0] for p in fat_pts]
            fy = [p[1] for p in fat_pts]
            ax1_r.plot(fx, fy, color=fat_color, linewidth=2.0, linestyle="--", marker="s", markersize=4.5, label="체지방 (%)", zorder=3)
            f_min, f_max = min(fy), max(fy)
            f_pad = max((f_max - f_min) * 0.4, 1.5)
            ax1_r.set_ylim(f_min - f_pad, f_max + f_pad)
            ax1_r.tick_params(axis="y", colors=fat_color, labelsize=8.5)
            ax1_r.annotate(
                f"{fy[-1]:.1f}%",
                xy=(fx[-1], fy[-1]),
                xytext=(0, -13),
                textcoords="offset points",
                ha="center",
                color=fat_color,
                fontsize=8.5,
                fontweight="bold",
            )
            lines_for_legend = list(lines_for_legend) + list(ax1_r.get_lines())

        leg = ax1.legend(
            lines_for_legend,
            [ln.get_label() for ln in lines_for_legend],
            loc="lower left",
            frameon=True,
            facecolor=bg_outer,
            edgecolor=grid_color,
            fontsize=8,
            labelcolor=text_main,
        )
        leg.set_zorder(10)
    else:
        ax1.text(0.5, 0.5, "체중/체지방 기록 없음", ha="center", va="center", color=text_muted, fontsize=11, transform=ax1.transAxes)
        ax1.set_xticks([])
        ax1.set_yticks([])

    ax1.set_title("체중(kg) · 체지방(%) 추이", color=text_main, fontsize=11, fontweight="bold", pad=10, loc="left")

    # --- Panel 2: Weekly Habit Completion Rate ---
    ax2.set_facecolor(bg_card)
    for spine in ("top", "right", "bottom", "left"):
        ax2.spines[spine].set_visible(False)

    habits = stats["habits"]
    y_pos = list(range(len(habits)))[::-1]
    labels = [h["label"] for h in habits]
    pcts = [min(h["done"] / h["target"] * 100.0, 100.0) for h in habits]
    colors = [h["color"] for h in habits]

    # Background tracks
    ax2.barh(y_pos, [100.0] * len(habits), height=0.52, color="#383A40", edgecolor="none", zorder=1)
    # Filled progress bars
    ax2.barh(y_pos, pcts, height=0.52, color=colors, edgecolor="none", alpha=0.92, zorder=2)

    ax2.set_xlim(0, 134)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels, color=text_main, fontsize=9.5, fontweight="bold")
    ax2.set_xticks([])
    ax2.tick_params(axis="y", length=0, pad=8)

    for y, h, pct in zip(y_pos, habits, pcts):
        txt = f"{h['done']}/{h['target']}{h['unit']} ({pct:.0f}%)"
        ax2.text(103, y, txt, va="center", ha="left", color=text_main, fontsize=8.8, fontweight="bold")

    ax2.set_title(
        f"주간 습관 달성률  (평균 {stats['overall_rate']:.0f}%)",
        color=text_main,
        fontsize=11,
        fontweight="bold",
        pad=10,
        loc="left",
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=bg_outer)
    plt.close(fig)
    png_bytes = buf.getvalue()

    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(png_bytes)

    return png_bytes


def build_weekly_payload(state: dict[str, Any], today: date) -> tuple[dict[str, Any], bytes]:
    trainer = get_trainer(state)
    stats = compute_weekly_stats(state, today)
    png_bytes = render_weekly_chart(stats)

    # Weight / fat weekly delta
    if stats["week_weights"]:
        w_start, w_end = stats["week_weights"][0], stats["week_weights"][-1]
        w_line = f"{w_start:.1f}kg → {fmt_delta(w_end, w_start, 'kg')}" if len(stats["week_weights"]) >= 2 else f"**{w_end:.1f}kg**"
    elif stats["weights"]:
        w_line = f"최근 **{stats['weights'][-1][1]:.1f}kg**"
    else:
        w_line = "기록 없음"

    if stats["week_fats"]:
        f_start, f_end = stats["week_fats"][0], stats["week_fats"][-1]
        f_line = f"{f_start:.1f}% → {fmt_delta(f_end, f_start, '%')}" if len(stats["week_fats"]) >= 2 else f"**{f_end:.1f}%**"
    elif stats["fats"]:
        f_line = f"최근 **{stats['fats'][-1][1]:.1f}%**"
    else:
        f_line = "기록 없음"

    koto = state.get("kotonoha") or {}
    streak = int(koto.get("streak") or 0)
    completed_cnt = len(koto.get("completedLessons") or [])
    q_stats = koto.get("quizStats") or {}
    q_total = int(q_stats.get("total") or 0)
    q_correct = int(q_stats.get("correct") or 0)
    acc = (q_correct / q_total * 100.0) if q_total > 0 else 0.0

    # Dynamic 3-trainer comments
    rate = stats["overall_rate"]
    if rate >= 75:
        trio_comment = (
            "💛 **코토네:** \"이번 주 달성률 진짜 대박이에요! 프로듀서님 완전 프로 다이어터~ 💛\"\n"
            "🌟 **미오:** \"꾸준함이 제일 무서운 법이지! 다음 주도 이 기세 그대로 가자! 🌟\"\n"
            "🌸 **제미니:** \"한 주간 참으로 훌륭하셨사옵니다. 푹 쉬시고 내일 또 뵈시와요 🍵\""
        )
    elif rate >= 40:
        trio_comment = (
            "💛 **코토네:** \"바쁜 와중에도 꾸준히 챙기신 거 다 알아요! 다음 주는 물이랑 식단 조금만 더 힘내봐요~ 💛\"\n"
            "🌟 **미오:** \"좋아좋아! 페이스 잡혀가고 있어! 다음 주엔 땀 한 번 더 빼보자구! 🌟\"\n"
            "🌸 **제미니:** \"조급해하지 마시고 한 걸음씩 나아가시와요. 소녀들이 늘 곁에 있사옵니다 🍵\""
        )
    else:
        trio_comment = (
            "💛 **코토네:** \"이번 주는 조금 바쁘셨죠? 괜찮아요! 다음 주 월요일부터 다시 리셋해서 화이팅해요! 💛\"\n"
            "🌟 **미오:** \"가볍게 10분 걷기랑 물 한 잔부터 다시 시동 걸어보자 프로듀서! 🌟\"\n"
            "🌸 **제미니:** \"쉬어가는 주간도 수련의 일부이옵니다. 내일 아침 다실에서 기다리겠사옵니다 🍵\""
        )

    embed = {
        "author": {
            "name": f"GEMINI FIT · WEEKLY REPORT ({stats['week_start'].strftime('%m/%d')} ~ {stats['week_end'].strftime('%m/%d')})",
            "url": APP_URL,
            "icon_url": trainer["avatar"],
        },
        "title": f"📊 주간 결산 리포트 · 종합 달성률 {rate:.0f}%",
        "description": trio_comment,
        "color": trainer["color"],
        "thumbnail": {"url": trainer["avatar"]},
        "fields": [
            {
                "name": "⚖️ 바디 변화",
                "value": f"• 체중: {w_line}\n• 체지방: {f_line}",
                "inline": True,
            },
            {
                "name": "🏋️ 주간 운동",
                "value": (
                    f"• 헬스: **{stats['gym_days']}회** ({stats['total_gym_sets']}세트 / {stats['total_gym_reps']}회)\n"
                    f"• 유산소: **{stats['cardio_days']}회** ({stats['total_cardio_km']:.1f}km)\n"
                    f"• 재활: **{stats['rehab_days']}일** · 복근: **{stats['abs_days']}일**"
                ),
                "inline": True,
            },
            {
                "name": "🥗 식단 · 코토노하",
                "value": (
                    f"• 식단 기록: **{stats['meal_days']}/7일** (총 {stats['total_meals']}끼) · 수분/티: **{stats['hydration_days']}/7일**\n"
                    f"• 코토노하: 🔥**{streak}일 스트릭** · 완료 **{completed_cnt}강** · 정답률 **{acc:.1f}%**"
                ),
                "inline": False,
            },
        ],
        "image": {"url": "attachment://weekly_report.png"},
        "footer": {
            "text": f"인연 랭크 Lv.{state.get('bondRank', 1)} ({state.get('bondExp', 0)}%) · 매주 일요일 자동 결산",
            "icon_url": TRAINERS["gemini"]["avatar"],
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    payload = {
        "username": "GeminiFit 주간 리포트",
        "avatar_url": trainer["avatar"],
        "embeds": [embed],
    }
    return payload, png_bytes


# ---------------------------------------------------------------------------
# Discord Webhook Sender
# ---------------------------------------------------------------------------
def send_webhook(webhook_url: str, payload: dict[str, Any], image_bytes: bytes | None = None, image_name: str = "weekly_report.png") -> None:
    if image_bytes is not None:
        resp = requests.post(
            webhook_url,
            data={"payload_json": json.dumps(payload, ensure_ascii=False)},
            files={"files[0]": (image_name, image_bytes, "image/png")},
            timeout=25,
        )
    else:
        resp = requests.post(webhook_url, json=payload, timeout=25)

    if resp.status_code not in (200, 204):
        raise RuntimeError(f"Discord webhook failed ({resp.status_code}): {resp.text[:400]}")


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------
def load_notify_state() -> dict[str, str]:
    if not NOTIFY_STATE_PATH.exists():
        return {}
    try:
        with NOTIFY_STATE_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_notify_state(mode: str, date_str: str) -> None:
    data = load_notify_state()
    data[mode] = date_str
    NOTIFY_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NOTIFY_STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="GeminiFit Discord Webhook Notifier")
    parser.add_argument("--mode", choices=["morning", "evening", "weekly"], required=True)
    parser.add_argument("--date", help="Override KST date (YYYY-MM-DD) for testing")
    parser.add_argument("--force", action="store_true", help="Force sending evening nudge even if today is complete")
    parser.add_argument("--skip-if-sent", action="store_true", help="Skip if this mode was already sent today (for backup crons)")
    parser.add_argument("--record-state", action="store_true", help="Record today's date in discord_notify_state.json after sending")
    parser.add_argument("--dry-run", action="store_true", help="Print payload instead of sending to Discord")
    parser.add_argument("--chart-out", help="Optional path to save generated weekly PNG chart")
    args = parser.parse_args()

    today = parse_ymd(args.date) if args.date else datetime.now(KST).date()
    if today is None:
        print(f"Invalid --date format: {args.date} (expected YYYY-MM-DD)", file=sys.stderr)
        return 2

    if args.skip_if_sent:
        notify_state = load_notify_state()
        if notify_state.get(args.mode) == today.isoformat():
            print(f"[{args.mode}] {today.isoformat()}: 이미 오늘 발송 완료됨 -> 백업 크론 스킵!")
            return 0

    state = load_state()
    image_bytes: bytes | None = None

    if args.mode == "morning":
        lessons = load_kotonoha_lessons()
        payload = build_morning_payload(state, lessons, today)
    elif args.mode == "evening":
        payload = build_evening_payload(state, today, force=args.force)
        if payload is None:
            print(f"[evening] {today.isoformat()}: 오늘 기록 & 코토노하 모두 완료됨 -> 알림 생략!")
            return 0
    else:
        payload, image_bytes = build_weekly_payload(state, today)
        if args.chart_out:
            out_p = Path(args.chart_out)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_bytes(image_bytes)
            print(f"[weekly] Chart saved to {out_p} ({len(image_bytes):,} bytes)")

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if image_bytes is not None:
            print(f"[dry-run] Attachment weekly_report.png: {len(image_bytes):,} bytes")
        return 0

    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL environment variable is not set.", file=sys.stderr)
        return 1

    send_webhook(webhook_url, payload, image_bytes=image_bytes)
    if args.record_state:
        save_notify_state(args.mode, today.isoformat())
    print(f"[{args.mode}] Successfully dispatched Discord notification for {today.isoformat()}!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
