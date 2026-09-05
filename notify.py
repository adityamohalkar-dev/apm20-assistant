"""
notify.py
=========
APM20 Personal Assistant — v2, rolling task-queue engine.

ONE message per day. No morning/evening split anymore — cron-job.org fires
this once, at 7:00 AM IST.

Task completion is 100% automatic: if a real commit landed in SKILL_REPO
since the current task set was first shown, the task set is marked done
and the NEXT one is shown tomorrow. If not, the SAME task set repeats,
with a note on how many days it's been pending.

All secrets are read from environment variables — NEVER hardcode credentials here.
"""

import os
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

import requests

import roadmap
import github_tracker
import wakatime_tracker
import telegram_inbox
import groq_brain
import state_store

IST = ZoneInfo("Asia/Kolkata")
GITHUB_USERNAME = "adityamohalkar-dev"


# ---------------------------------------------------------------
# 1) TASK-QUEUE LOGIC
# ---------------------------------------------------------------
def advance_or_repeat_task(token: str) -> dict:
    """
    Checks whether the current task set is complete (a real push landed in
    SKILL_REPO since it was first shown). Updates state accordingly.

    Returns:
      {
        "task": dict,              # the task set to show today (current or next)
        "task_index": int,
        "just_completed": bool,    # True if yesterday's task set was just finished
        "repeat_count": int,       # how many days this task set has now shown
        "commit_check_ok": bool,
        "commit_check_error": str or None,
        "queue_finished": bool,    # True if you've cleared the whole queue
      }
    """
    state = state_store.load_state()
    now = datetime.now(IST)
    today_str = now.strftime("%Y-%m-%d")

    idx = state.get("current_task_index", 0)
    started_at = state.get("task_started_at")

    result = {
        "task": None,
        "task_index": idx,
        "just_completed": False,
        "repeat_count": state.get("task_repeat_count", 0),
        "commit_check_ok": False,
        "commit_check_error": None,
        "queue_finished": False,
    }

    if idx >= len(roadmap.TASK_QUEUE):
        result["queue_finished"] = True
        return result

    # First time ever showing a task — initialize started_at, don't check anything yet
    if started_at is None:
        state["task_started_at"] = today_str
        state["task_repeat_count"] = 1
        state_store.save_state(state)
        result["task"] = roadmap.TASK_QUEUE[idx]
        result["repeat_count"] = 1
        return result

    # Don't re-check if we already evaluated today (avoid double-advance on re-runs)
    if started_at == today_str:
        result["task"] = roadmap.TASK_QUEUE[idx]
        result["commit_check_ok"] = True
        return result

    since_dt = datetime.strptime(started_at, "%Y-%m-%d").replace(tzinfo=IST)
    check = github_tracker.get_repo_commits_since(GITHUB_USERNAME, roadmap.SKILL_REPO, token, since_dt)
    result["commit_check_ok"] = check["ok"]
    result["commit_check_error"] = check["error"]

    if check["ok"] and check["commit_count"] > 0:
        # Task set complete — advance to the next one
        idx += 1
        state["current_task_index"] = idx
        state["task_started_at"] = today_str
        state["task_repeat_count"] = 1
        result["just_completed"] = True
        if idx >= len(roadmap.TASK_QUEUE):
            result["queue_finished"] = True
            state_store.save_state(state)
            return result
        result["task"] = roadmap.TASK_QUEUE[idx]
        result["repeat_count"] = 1
    else:
        # Not complete — repeat the same task set
        state["task_repeat_count"] = state.get("task_repeat_count", 0) + 1
        result["task"] = roadmap.TASK_QUEUE[idx]
        result["repeat_count"] = state["task_repeat_count"]

    state_store.save_state(state)
    return result


# ---------------------------------------------------------------
# 2) BUILD TODAY'S MESSAGE
# ---------------------------------------------------------------
def build_message() -> tuple:
    """Returns (message_text, context_dict) — context feeds the AI review."""
    now = datetime.now(IST)
    today_str = now.strftime("%Y-%m-%d")
    weekday = now.strftime("%A")

    lines = [f"APM20 // {weekday}, {now.strftime('%d %b %Y')}", ""]
    context = {
        "commits_today": 0, "repos": [], "coding_time": "0 mins",
        "streak": 0, "best_streak": 0, "sprint_focus": None,
        "activity_log_today": [],
    }

    token = os.environ.get("GITHUB_PAT")

    # --- Task queue: advance or repeat ---
    tq = advance_or_repeat_task(token)

    if tq["queue_finished"]:
        lines.append("You've cleared every task in the queue. Time to add more — edit roadmap.py.")
        lines.append("")
        for r in roadmap.GENERAL_RESOURCES:
            lines.append(f"  - {r}")
        return "\n".join(lines), context

    task = tq["task"]
    context["sprint_focus"] = task["title"]

    if tq["just_completed"]:
        lines.append(f"PREVIOUS TASK SET: COMPLETE — real push detected. Moving on.")
        lines.append("")

    header = f"TASK SET — {task['title']}"
    if tq["repeat_count"] > 1:
        header += f"  (day {tq['repeat_count']} — still pending, no push detected yet)"
    lines.append(header)
    lines.append("")
    lines.append("Today's tasks (2-hour budget — this is the whole list, don't add more):")
    for i, t in enumerate(task["tasks"], 1):
        lines.append(f"  {i}. {t}")
    lines.append("")
    lines.append(f"Done = push to `{roadmap.SKILL_REPO}`. That's the only completion signal — nothing else to report.")

    if task.get("resources"):
        lines.append("")
        lines.append("Resources:")
        for r in task["resources"]:
            lines.append(f"  - {r}")

    if tq["commit_check_error"]:
        lines.append("")
        lines.append(f"[commit check failed: {tq['commit_check_error']}]")

    # --- REAL proof-of-work stats (informational, not what drives completion) ---
    activity = github_tracker.get_today_activity(GITHUB_USERNAME, token)
    state_after = github_tracker.update_streak(activity["ok"] and activity["total_commits_today"] > 0)
    if activity["ok"]:
        context["commits_today"] = activity["total_commits_today"]
        context["repos"] = activity["repos_with_commits"]
        context["streak"] = state_after["current_streak"]
        context["best_streak"] = state_after["longest_streak"]
        lines.append("")
        lines.append(
            f"Stats: {activity['total_commits_today']} commit(s) today | "
            f"Streak: {state_after['current_streak']}d (best {state_after['longest_streak']}d)"
        )

    # --- REAL coding time (WakaTime) ---
    waka_key = os.environ.get("WAKATIME_API_KEY")
    coding = wakatime_tracker.get_today_coding_time(waka_key)
    if coding["ok"]:
        context["coding_time"] = coding["human_readable"]
        lines.append(f"Coding time so far: {coding['human_readable']}")

    lines.append("")
    lines.append(f"Rule reminder: {roadmap.CORE_RULES[now.day % len(roadmap.CORE_RULES)]}")

    full_state = state_store.load_state()
    context["activity_log_today"] = [
        e for e in full_state.get("activity_log", []) if e.get("date") == today_str
    ]

    # --- Daily snapshot: one real record per day for the dashboard's history/charts ---
    snapshots = full_state.get("daily_snapshots", [])
    snapshots = [s for s in snapshots if s.get("date") != today_str]  # avoid dupes on re-runs
    snapshots.append({
        "date": today_str,
        "commits_today": context["commits_today"],
        "repos": context["repos"],
        "coding_time": context["coding_time"],
        "streak": context["streak"],
        "task_title": task["title"],
        "task_index": tq["task_index"],
        "repeat_count": tq["repeat_count"],
    })
    full_state["daily_snapshots"] = snapshots[-90:]  # keep ~3 months

    # --- Roadmap snapshot: mirrors roadmap.TASK_QUEUE so the dashboard can show progress ---
    full_state["roadmap_snapshot"] = {
        "total_tasks": len(roadmap.TASK_QUEUE),
        "titles": [t["title"] for t in roadmap.TASK_QUEUE],
    }
    state_store.save_state(full_state)

    return "\n".join(lines), context


# ---------------------------------------------------------------
# 3) CHANNELS — each is independent, each fails silently on its own
# ---------------------------------------------------------------
def send_telegram(message: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[telegram] skipped — TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=15)
        r.raise_for_status()
        print("[telegram] sent")
    except Exception as e:
        print(f"[telegram] FAILED: {e}")


def send_email(message: str) -> None:
    sender = os.environ.get("EMAIL_SENDER")
    app_password = os.environ.get("EMAIL_APP_PASSWORD")
    recipient = os.environ.get("EMAIL_RECIPIENT", sender)
    if not sender or not app_password:
        print("[email] skipped — EMAIL_SENDER / EMAIL_APP_PASSWORD not set")
        return
    try:
        msg = MIMEText(message)
        msg["Subject"] = "APM20 Assistant — Today's Tasks"
        msg["From"] = sender
        msg["To"] = recipient
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, [recipient], msg.as_string())
        print("[email] sent")
    except Exception as e:
        print(f"[email] FAILED: {e}")


def send_whatsapp(message: str) -> None:
    phone = os.environ.get("CALLMEBOT_PHONE")
    apikey = os.environ.get("CALLMEBOT_APIKEY")
    if not phone or not apikey:
        print("[whatsapp] skipped — CALLMEBOT_PHONE / CALLMEBOT_APIKEY not set")
        return
    url = "https://api.callmebot.com/whatsapp.php"
    try:
        r = requests.get(url, params={"phone": phone, "text": message, "apikey": apikey}, timeout=15)
        r.raise_for_status()
        print("[whatsapp] sent")
    except Exception as e:
        print(f"[whatsapp] FAILED: {e}")


# ---------------------------------------------------------------
# 4) ENTRYPOINT
# ---------------------------------------------------------------
def main():
    # --- Check for /skip, /log commands sent since last run (no /done needed anymore) ---
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    inbox = telegram_inbox.process_new_messages(token)
    if inbox["ok"] and inbox["processed"]:
        print(f"[inbox] processed {len(inbox['processed'])} command(s): {inbox['processed']}")
        for reply in inbox["reply_texts"]:
            send_telegram(reply)
    elif inbox["error"]:
        print(f"[inbox] check failed: {inbox['error']}")

    message, context = build_message()

    review = groq_brain.generate_reflection(context)
    if review["ok"]:
        message += f"\n\nAI REVIEW:\n{review['text']}"
        print("[ai review] generated")
    elif review["error"] and os.environ.get("GROQ_API_KEY"):
        print(f"[ai review] FAILED: {review['error']}")

    print(message)
    print("-" * 40)

    send_telegram(message)
    send_email(message)
    send_whatsapp(message)


if __name__ == "__main__":
    main()
