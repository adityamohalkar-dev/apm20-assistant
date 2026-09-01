"""
telegram_inbox.py
==================
Two-way commands, polling-based (not instant — checked each time the
workflow runs, which is why pairing this with a frequent external
trigger like cron-job.org matters).

Commands understood:
  /done          - log that you did the work today
  /skip <reason> - log that you skipped, with a reason
  /log <note>    - log a free-text note

Everything gets appended to state.json's activity_log (kept to the last
50 entries so the file doesn't grow forever), and the bot sends a short
confirmation reply for each command it processes.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import requests

import state_store

IST = ZoneInfo("Asia/Kolkata")
MAX_LOG_ENTRIES = 50


def _get_updates(token: str, offset: int) -> list:
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    r = requests.get(url, params={"offset": offset + 1, "timeout": 0}, timeout=15)
    r.raise_for_status()
    return r.json().get("result", [])


def _parse_command(text: str) -> tuple:
    """Returns (log_type, detail) or (None, None) if not a recognized command."""
    text = text.strip()
    if text == "/done":
        return "done", ""
    if text.startswith("/skip"):
        return "skip", text[len("/skip"):].strip()
    if text.startswith("/log"):
        return "note", text[len("/log"):].strip()
    return None, None


def process_new_messages(token: str) -> dict:
    """
    Fetches any new Telegram messages since last check, logs recognized
    commands, updates the offset so we don't reprocess them.

    Returns:
      {
        "ok": bool,
        "processed": [{"type": str, "detail": str}, ...],
        "reply_texts": [str, ...],   # confirmations to send back
        "error": str or None,
      }
    """
    result = {"ok": False, "processed": [], "reply_texts": [], "error": None}

    if not token:
        result["error"] = "TELEGRAM_BOT_TOKEN not set"
        return result

    state = state_store.load_state()
    offset = state.get("telegram_offset", 0)

    try:
        updates = _get_updates(token, offset)
    except Exception as e:
        result["error"] = str(e)
        return result

    if not updates:
        result["ok"] = True
        return result

    log = state.get("activity_log", [])
    today_str = datetime.now(IST).strftime("%Y-%m-%d")
    time_str = datetime.now(IST).strftime("%H:%M")

    for update in updates:
        offset = update["update_id"]  # advance past every update, recognized or not
        message = update.get("message", {})
        text = message.get("text", "")
        if not text:
            continue

        log_type, detail = _parse_command(text)
        if log_type is None:
            continue

        entry = {"date": today_str, "time": time_str, "type": log_type, "detail": detail}
        log.append(entry)
        result["processed"].append({"type": log_type, "detail": detail})

        if log_type == "done":
            result["reply_texts"].append("Logged: done for today. Good.")
        elif log_type == "skip":
            reason = detail if detail else "(no reason given)"
            result["reply_texts"].append(f"Logged: skipped today — {reason}")
        elif log_type == "note":
            result["reply_texts"].append(f"Logged note: {detail}")

    log = log[-MAX_LOG_ENTRIES:]  # keep it bounded

    state["telegram_offset"] = offset
    state["activity_log"] = log
    state_store.save_state(state)

    result["ok"] = True
    return result
