"""
state_store.py
===============
Shared read/write for state.json. Every module that needs persistent
storage goes through here — load the FULL dict, modify only your own
keys, save the FULL dict back. This is what prevents one tracker's
write from wiping out another tracker's data.
"""

import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"

DEFAULTS = {
    "last_commit_date": None,
    "current_streak": 0,
    "longest_streak": 0,
    "telegram_offset": 0,
    "activity_log": [],
    "current_task_index": 0,       # pointer into roadmap.TASK_QUEUE
    "task_started_at": None,       # ISO date the current task set was first shown
    "task_repeat_count": 0,        # how many days in a row this same task set has repeated
    "daily_snapshots": [],         # one entry per day the assistant ran: real commits/coding-time/streak/task
    "roadmap_snapshot": {},        # {"total_tasks": int, "titles": [str, ...]} — mirrors roadmap.TASK_QUEUE for the dashboard
}


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            # backfill any keys added in later versions
            for k, v in DEFAULTS.items():
                data.setdefault(k, v)
            return data
        except Exception:
            pass
    return dict(DEFAULTS)


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))
