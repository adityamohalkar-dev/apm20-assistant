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
