#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gemini Fit voice audition lab.

Generates short Japanese samples for many candidate voices so we can pick the
voice that fits 제미니 / 코토네 / 미오 *before* batch-baking the kotonoha lines
into preset MP3s.

The generated files land in tools/tts_lab/clips/ and are listed in
tools/tts_lab/manifest.json, which audition.html plays in the browser.

Usage
-----
  # VOICEVOX via api.tts.quest (free, no key). Enumerate ids 0..59.
  python tools/tts_lab/tts_lab.py voicevox --ids 0-59

  # Fish Audio free model (needs a key: https://fish.audio )
  set FISH_AUDIO_API_KEY=xxxx
  python tools/tts_lab/tts_lab.py fish --voices <model_id>,<model_id>

  # Gemini TTS (uses GEMINI_API_KEY from the environment)
  python tools/tts_lab/tts_lab.py gemini --voices Kore,Puck,Leda

  # Rebuild manifest.json from the clips on disk (no network)
  python tools/tts_lab/tts_lab.py report

Notes
-----
* Clips are temporary audition artifacts. Only the final picks get copied to
  audio/kotonoha/ and wired into KOTONOHA_PRESET_AUDIO.
* tts.quest throttles unauthenticated callers, so requests are spaced out and
  retried using the retryAfter value it returns.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time
import wave
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
CLIPS = ROOT / "clips"
MANIFEST = ROOT / "manifest.json"

# Two registers: a bright standard-Japanese greeting, then the Kyoto-ben
# register that the kotonoha lessons actually use.
AUDITION_LINES = [
    "プロデューサーさん、おはようございます！今日も一緒にがんばりましょうね。",
    "おいでやす。今日もおきばりやす。……無理はあかんで、お茶でも飲んでいき。",
]

SPEAK_DELAY = 1.1  # seconds between tts.quest requests (free tier throttle)


def log(msg: str) -> None:
    print(msg, flush=True)


def ensure_dirs() -> None:
    CLIPS.mkdir(parents=True, exist_ok=True)


def load_manifest() -> dict:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"generatedAt": None, "script": AUDITION_LINES, "clips": []}


def save_manifest(manifest: dict) -> None:
    # Merge with whatever is already on disk: two generators running at the
    # same time must not clobber each other's entries.
    disk = load_manifest()
    by_id = {c.get("id"): c for c in disk.get("clips", []) if c.get("id")}
    for clip in manifest.get("clips", []):
        if clip.get("id"):
            by_id[clip["id"]] = clip
    manifest["clips"] = list(by_id.values())
    manifest["generatedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest["script"] = AUDITION_LINES
    manifest["clips"].sort(key=clip_sort_key)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def clip_sort_key(clip: dict):
    """Numeric ids first (voicevox 2 before 12), then names, so the list reads
    like the engine's own speaker order instead of alphabetical soup."""
    vid = str(clip.get("voiceId", ""))
    return (
        clip.get("provider", ""),
        0 if vid.isdigit() else 1,
        int(vid) if vid.isdigit() else 0,
        clip.get("name", ""),
    )


def upsert_clip(manifest: dict, entry: dict) -> None:
    clips = manifest.setdefault("clips", [])
    for i, c in enumerate(clips):
        if c["id"] == entry["id"]:
            clips[i] = entry
            return
    clips.append(entry)


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------

def synth_voicevox(voice_id: int, text: str, session: requests.Session) -> tuple[bytes, str, str]:
    """Return (audio_bytes, ext, display_name) for one VOICEVOX style id."""
    url = "https://api.tts.quest/v3/voicevox/synthesis"
    payload = None
    for _ in range(5):
        r = session.get(url, params={"text": text, "speaker": voice_id}, timeout=90)
        data = r.json()
        if data.get("success"):
            payload = data
            break
        wait = data.get("retryAfter") or 3
        log(f"    throttled (retryAfter={wait}s)")
        time.sleep(float(wait) + 0.5)
    if not payload:
        raise RuntimeError(f"voicevox id={voice_id}: synthesis request rejected")

    name = payload.get("speakerName") or f"VOICEVOX:{voice_id}"
    status_url = payload.get("audioStatusUrl")
    for _ in range(40):
        st = session.get(status_url, timeout=30).json()
        if st.get("isAudioReady"):
            break
        if st.get("isAudioError"):
            raise RuntimeError(f"voicevox id={voice_id}: audio error")
        time.sleep(0.6)
    else:
        raise RuntimeError(f"voicevox id={voice_id}: audio not ready in time")

    mp3 = session.get(payload["mp3DownloadUrl"], timeout=120).content
    return mp3, "mp3", name


def synth_fish(model_id: str, text: str, key: str, session: requests.Session,
               model: str = "s2.1-pro-free") -> tuple[bytes, str, str]:
    """Fish Audio TTS.

    The model MUST be sent as an HTTP header: when it is only present in the
    JSON body the API silently falls back to the paid `s2.1-pro` model. That
    mistake cost $0.03 once — never put it back in the body.
    """
    r = session.post(
        "https://api.fish.audio/v1/tts",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "model": model,
        },
        json={
            "text": text,
            "reference_id": model_id,
            "format": "mp3",
            "mp3_bitrate": 128,
        },
        timeout=180,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"fish {model_id}: HTTP {r.status_code} {r.text[:300]}")
    return r.content, "mp3", fetch_fish_title(model_id, key, session) or model_id


def fetch_fish_title(model_id: str, key: str, session: requests.Session) -> str:
    try:
        r = session.get(f"https://api.fish.audio/model/{model_id}",
                        headers={"Authorization": f"Bearer {key}"}, timeout=30)
        if r.ok:
            return (r.json().get("title") or "").strip()
    except Exception:
        pass
    return ""


def fish_credit(key: str, session: requests.Session) -> str:
    try:
        r = session.get("https://api.fish.audio/wallet/self/api-credit",
                        headers={"Authorization": f"Bearer {key}"}, timeout=30)
        if r.ok:
            return str(r.json().get("credit"))
    except Exception:
        pass
    return "?"


def synth_gemini(voice: str, text: str, key: str, session: requests.Session) -> tuple[bytes, str, str]:
    """Gemini 2.5 Flash TTS. Returns 24 kHz mono PCM wrapped as WAV."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash-preview-tts:generateContent?key={key}"
    )
    body = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }
    r = session.post(url, json=body, timeout=240)
    if r.status_code >= 400:
        raise RuntimeError(f"gemini {voice}: HTTP {r.status_code} {r.text[:300]}")
    data = r.json()
    part = data["candidates"][0]["content"]["parts"][0]
    pcm = base64.b64decode(part["inlineData"]["data"])
    rate = 24000
    mime = part["inlineData"].get("mimeType", "")
    if "rate=" in mime:
        try:
            rate = int(mime.split("rate=")[1].split(";")[0])
        except Exception:
            pass
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)
    return buf.getvalue(), "wav", f"Gemini:{voice}"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def parse_ids(spec: str) -> list[int]:
    ids: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            ids.extend(range(int(a), int(b) + 1))
        else:
            ids.append(int(chunk))
    return ids


def run_generation(provider: str, voices: list, args) -> int:
    ensure_dirs()
    manifest = load_manifest()
    session = requests.Session()
    session.headers.update({"User-Agent": "GeminiFit-TTS-Lab/1.0"})

    key = ""
    if provider == "fish":
        key = args.key or os.environ.get("FISH_AUDIO_API_KEY", "")
        if not key:
            log("FISH_AUDIO_API_KEY is not set. Get a free key at https://fish.audio/developers")
            return 2
    elif provider == "gemini":
        key = args.key or os.environ.get("GEMINI_API_KEY", "")
        if not key:
            log("GEMINI_API_KEY is not set.")
            return 2

    ok = 0
    credit_start = fish_credit(key, session) if provider == "fish" else ""
    if provider == "fish":
        log(f"  fish credit before: {credit_start} (model=s2.1-pro-free)")
    for voice in voices:
        clip_id = f"{provider}_{voice}"
        path = CLIPS / f"{clip_id}.{args.ext or ('mp3' if provider != 'gemini' else 'wav')}"

        if path.exists() and not args.force:
            log(f"  skip {clip_id} (exists)")
            continue

        log(f"  synth {provider} {voice} ...")
        try:
            if provider == "voicevox":
                audio, ext, name = synth_voicevox(voice, args.text, session)
                time.sleep(SPEAK_DELAY)
            elif provider == "fish":
                audio, ext, name = synth_fish(voice, args.text, key, session)
            elif provider == "gemini":
                audio, ext, name = synth_gemini(voice, args.text, key, session)
            else:
                raise ValueError(provider)
        except Exception as exc:  # keep going: one bad voice must not kill the run
            log(f"    FAILED {clip_id}: {exc}")
            continue

        path = CLIPS / f"{clip_id}.{ext}"
        path.write_bytes(audio)
        upsert_clip(
            manifest,
            {
                "id": clip_id,
                "provider": provider,
                "voiceId": str(voice),
                "name": name,
                "file": f"clips/{path.name}",
                "bytes": len(audio),
                "text": args.text,
            },
        )
        save_manifest(manifest)  # incremental: a crash keeps finished clips
        ok += 1
        log(f"    ok {name} -> {path.name} ({len(audio) // 1024} KB)")

        # Spend guard: the "free" Fish model still costs money if the model
        # header is dropped, so stop the moment the wallet starts shrinking.
        if provider == "fish":
            now = fish_credit(key, session)
            try:
                if float(now) < float(credit_start):
                    log(f"  ABORT: credit dropped {credit_start} -> {now}. "
                        f"Stopping before spending more.")
                    return 3
            except ValueError:
                pass

    log(f"done: {ok}/{len(voices)} generated · {MANIFEST}")
    return 0


def run_report() -> int:
    """Rebuild manifest entries from whatever is on disk."""
    manifest = load_manifest()
    known = {c["id"]: c for c in manifest.get("clips", [])}
    for path in sorted(CLIPS.glob("*")):
        if path.suffix.lower() not in {".mp3", ".wav"}:
            continue
        provider = path.stem.split("_", 1)[0]
        known.setdefault(
            path.stem,
            {
                "id": path.stem,
                "provider": provider,
                "voiceId": path.stem.split("_", 1)[-1],
                "name": path.stem,
                "file": f"clips/{path.name}",
                "bytes": path.stat().st_size,
                "text": " ".join(AUDITION_LINES),
            },
        )
    manifest["clips"] = list(known.values())
    save_manifest(manifest)
    log(f"report: {len(manifest['clips'])} clips")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Gemini Fit voice audition lab")
    parser.add_argument("provider", choices=["voicevox", "fish", "gemini", "report"])
    parser.add_argument("--ids", default="", help="voicevox style ids, e.g. 0-59 or 2,8,12")
    parser.add_argument("--voices", default="", help="provider specific voice/model ids, comma separated")
    parser.add_argument("--text", default=" ".join(AUDITION_LINES), help="text to synthesize")
    parser.add_argument("--key", default="", help="API key (falls back to env var)")
    parser.add_argument("--force", action="store_true", help="regenerate existing clips")
    parser.add_argument("--ext", default="", choices=["", "mp3", "wav"])
    args = parser.parse_args(argv)

    if args.provider == "report":
        return run_report()

    if args.provider == "voicevox":
        if not args.ids:
            parser.error("voicevox needs --ids")
        voices: list = parse_ids(args.ids)
    else:
        if not args.voices:
            parser.error(f"{args.provider} needs --voices")
        voices = [v.strip() for v in args.voices.split(",") if v.strip()]

    return run_generation(args.provider, voices, args)


if __name__ == "__main__":
    raise SystemExit(main())
