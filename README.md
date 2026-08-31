# APM20 Assistant — v1 (Accountability Engine)

A free, self-hosted notifier that reads your own roadmap and pings you
twice a day (11:00 AM IST / 9:55 PM IST) via Telegram, Email, and optionally
WhatsApp. Runs on GitHub Actions — no server, no cost, no laptop needs to stay on.

This is Layer 1 of 4 (see chat). It has zero AI in it on purpose —
it's a dumb, reliable scheduler first. The "brain" gets added later.

---

## 1. Push this to GitHub

```bash
cd apm20-assistant
git init
git add .
git commit -m "APM20 Assistant v1 — accountability engine"
git branch -M main
git remote add origin https://github.com/<your-username>/apm20-assistant.git
git push -u origin main
```

## 2. Set up Telegram (5 minutes, do this one — it's the most reliable)

1. Open Telegram, search **@BotFather**, send `/newbot`, follow prompts.
2. BotFather gives you a **token** like `123456:ABC-DEF...` — save it.
3. Send your new bot any message (so it can find your chat).
4. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser —
   find `"chat":{"id":XXXXXXX` — that's your **chat_id**.

## 3. Set up Email (Gmail, 5 minutes)

1. Go to your Google Account → Security → **App Passwords**
   (requires 2-Step Verification to be on).
2. Generate an app password for "Mail".
3. That 16-character password is `EMAIL_APP_PASSWORD` — NOT your real Gmail password.

## 4. Set up WhatsApp (optional, less reliable — free personal-use hack)

1. Save `+34 644 59 71 65` as a contact.
2. Message it on WhatsApp: `I allow callmebot to send me messages`
3. It replies with your `apikey`. Your `CALLMEBOT_PHONE` is your number in
   international format, e.g. `919876543210`.

## 5. Add secrets to GitHub

Repo → **Settings → Secrets and variables → Actions → New repository secret**.
Add whichever of these you have:

| Secret name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | from step 2 |
| `TELEGRAM_CHAT_ID` | from step 2 |
| `EMAIL_SENDER` | your Gmail address |
| `EMAIL_APP_PASSWORD` | from step 3 |
| `EMAIL_RECIPIENT` | where to receive it (can be same as sender) |
| `CALLMEBOT_PHONE` | from step 4 (optional) |
| `CALLMEBOT_APIKEY` | from step 4 (optional) |

You don't need all of them — any channel with missing secrets is just skipped.

## 6. Test it manually

Repo → **Actions** tab → "APM20 Assistant Notify" → **Run workflow**.
Check the run logs — you'll see `[telegram] sent` / `[email] sent` etc.,
or `[channel] skipped` / `[channel] FAILED: <reason>` if something's wrong.

Once that works, it runs automatically forever, for free, on the cron schedule
in `.github/workflows/notify.yml`.

---

## Editing your plan

Everything the assistant says comes from **`roadmap.py`**. When the 8-day
sprint ends and you move into the weekly OS, you don't need to touch
`notify.py` at all — just edit the data in `roadmap.py` and push.

## What's next (Layer 2+, not built yet)

- Log actual GitHub commits/LeetCode counts instead of just asking about them
- YouTube watch-time vs code-time ratio tracking
- Claude/Groq API layer so it can actually respond, not just broadcast

We build these once Layer 1 has been running for real for a week or two —
not before.
