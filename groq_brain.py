"""
groq_brain.py
=============
The AI reasoning layer. Only runs on the evening message, and only reviews
REAL data (from github_tracker, wakatime_tracker, state_store) — it never
sees or evaluates self-reported claims. If there's no real data yet, it
says so instead of making something up.

Uses Groq's free-tier API (OpenAI-compatible). Model names on Groq's free
tier change periodically — if this stops working, check console.groq.com
for the current model list and swap MODEL below.
"""

import os

import requests

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a blunt, honest accountability reviewer for a first-year CS student's daily execution log. You are NOT a cheerleader. You do not use exclamation marks, generic encouragement, or phrases like "great job" or "keep it up" unless the data genuinely earns it.

You will be given real, verified data for one day: GitHub commits, coding time (WakaTime), current streak, and any /done, /skip, or /log entries the person sent themselves.

Write 2-3 sentences maximum. Rules:
- If the data shows real work (commits > 0 or coding time > 0), acknowledge it specifically using the actual numbers — don't just say "good work."
- If the data shows nothing happened, say that plainly. Don't soften it, don't guilt-trip either — just state the fact and note what tomorrow needs.
- If there's a mismatch (e.g. they logged /done but commits=0), point that out directly — that's exactly the kind of gap this system exists to catch.
- Never invent progress that isn't in the data. Never use motivational-poster language.
- No preamble like "Here's my review:" — just the 2-3 sentences directly.
"""


def generate_reflection(context: dict) -> dict:
    """
    context should contain: commits_today, repos, coding_time, streak,
    best_streak, sprint_focus, activity_log_today (list of dicts)

    Returns: {"ok": bool, "text": str, "error": str or None}
    """
    result = {"ok": False, "text": None, "error": None}

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        result["error"] = "GROQ_API_KEY not set"
        return result

    log_lines = []
    for entry in context.get("activity_log_today", []):
        log_lines.append(f"  - {entry.get('time','')} {entry.get('type','')}: {entry.get('detail','') or '(no detail)'}")
    log_text = "\n".join(log_lines) if log_lines else "  (no self-logged entries today)"

    user_message = f"""Today's real data:
- Focus for today: {context.get('sprint_focus', 'N/A')}
- GitHub commits: {context.get('commits_today', 0)} in {context.get('repos', []) or '(no repos)'}
- Coding time (WakaTime): {context.get('coding_time', '0 mins')}
- Current streak: {context.get('streak', 0)} days (best: {context.get('best_streak', 0)})
- Self-logged entries today:
{log_text}

Give your 2-3 sentence review."""

    try:
        r = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                "max_tokens": 150,
                "temperature": 0.4,
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        result["text"] = data["choices"][0]["message"]["content"].strip()
        result["ok"] = True
        return result
    except Exception as e:
        result["error"] = str(e)
        return result
