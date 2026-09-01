"""
notify.py
=========
APM20 Personal Assistant — notification engine.

Reads today's plan from roadmap.py and pushes it out over whichever
channels have credentials set (Telegram / Email / WhatsApp).
Missing credentials = that channel is silently skipped, others still run.

Runs for free on a schedule via GitHub Actions (see .github/workflows/notify.yml).
All secrets are read from environment variables — NEVER hardcode credentials here.
"""

import os
import smtplib
import sys
from datetime import datetime
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

import requests

import roadmap
import github_tracker

IST = ZoneInfo("Asia/Kolkata")
GITHUB_USERNAME = "adityamohalkar-dev"


# ---------------------------------------------------------------
# 1) BUILD TODAY'S MESSAGE
# ---------------------------------------------------------------
def build_message(mode: str) -> str:
    now = datetime.now(IST)
    today_str = now.strftime("%Y-%m-%d")
    weekday = now.strftime("%A")

    lines = [f"APM20 // {weekday}, {now.strftime('%d %b %Y')} // {mode.upper()}", ""]

    # --- REAL proof-of-work check (not self-reported) ---
    token = os.environ.get("GITHUB_PAT")
    activity = github_tracker.get_today_activity(GITHUB_USERNAME, token)
    state = None
    if mode == "evening":
        state = github_tracker.update_streak(activity["ok"] and activity["total_commits_today"] > 0)

    if activity["ok"]:
        if activity["total_commits_today"] > 0:
            repos = ", ".join(activity["repos_with_commits"])
            lines.append(
                f"PROOF-OF-WORK (verified): {activity['total_commits_today']} commit(s) today in [{repos}]"
            )
        else:
            lines.append("PROOF-OF-WORK (verified): 0 commits today so far")
        if state:
            lines.append(f"Streak: {state['current_streak']} day(s) (best: {state['longest_streak']})")
        lines.append("")
    elif token:
        lines.append(f"[proof-of-work check failed: {activity['error']}]")
        lines.append("")

    sprint_day = roadmap.SPRINT_8DAY.get(today_str)

    if sprint_day:
        lines.append(f"SPRINT DAY — {sprint_day['focus']}")
        lines.append("Tasks:")
        for t in sprint_day["tasks"]:
            lines.append(f"  - {t}")
        lines.append(f"Deliverable: {sprint_day['deliverable']}")
        if sprint_day.get("resources"):
            lines.append("")
            lines.append("Resources:")
            for r in sprint_day["resources"]:
                lines.append(f"  - {r}")
    elif weekday == "Sunday":
        lines.append("SUNDAY DEEP WORK SPRINT (10-12 hrs)")
        for b in roadmap.SUNDAY_BLOCK:
            lines.append(f"  - {b}")
        if mode == "evening":
            lines.append("")
            lines.append("SUNDAY SELF-AUDIT — answer honestly:")
            for i, q in enumerate(roadmap.SUNDAY_REVIEW_CHECKLIST, 1):
                lines.append(f"  {i}. {q}")
        lines.append("")
        lines.append("Resources:")
        for r in roadmap.GENERAL_RESOURCES:
            lines.append(f"  - {r}")
    else:
        lines.append("WEEKDAY OPERATING BLOCK (5:30-9:30 PM)")
        for b in roadmap.WEEKDAY_BLOCK:
            lines.append(f"  - {b}")
        lines.append("")
        lines.append("Resources:")
        for r in roadmap.GENERAL_RESOURCES:
            lines.append(f"  - {r}")

    if mode == "evening" and weekday != "Sunday":
        lines.append("")
        lines.append("Before you close the laptop: did you commit/push something today?")

    lines.append("")
    lines.append(f"Rule reminder: {roadmap.CORE_RULES[now.day % len(roadmap.CORE_RULES)]}")

    return "\n".join(lines)


# ---------------------------------------------------------------
# 2) CHANNELS — each is independent, each fails silently on its own
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
        msg["Subject"] = "APM20 Assistant — Today's Plan"
        msg["From"] = sender
        msg["To"] = recipient
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, [recipient], msg.as_string())
        print("[email] sent")
    except Exception as e:
        print(f"[email] FAILED: {e}")


def send_whatsapp(message: str) -> None:
    """
    Uses CallMeBot's free personal-use API (not official WhatsApp Business API).
    Setup: message +34 644 59 71 65 on WhatsApp with 'I allow callmebot to send me messages'
    to get your apikey, then set CALLMEBOT_PHONE and CALLMEBOT_APIKEY as secrets.
    Free-tier limits apply and delivery isn't as reliable as Telegram/Email.
    """
    phone = os.environ.get("CALLMEBOT_PHONE")
    apikey = os.environ.get("CALLMEBOT_APIKEY")
    if not phone or not apikey:
        print("[whatsapp] skipped — CALLMEBOT_PHONE / CALLMEBOT_APIKEY not set")
        return
    url = "https://api.callmebot.com/whatsapp.php"
    try:
        r = requests.get(
            url,
            params={"phone": phone, "text": message, "apikey": apikey},
            timeout=15,
        )
        r.raise_for_status()
        print("[whatsapp] sent")
    except Exception as e:
        print(f"[whatsapp] FAILED: {e}")


# ---------------------------------------------------------------
# 3) ENTRYPOINT
# ---------------------------------------------------------------
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"  # "morning" or "evening"
    message = build_message(mode)
    print(message)
    print("-" * 40)

    send_telegram(message)
    send_email(message)
    send_whatsapp(message)


if __name__ == "__main__":
    main()
