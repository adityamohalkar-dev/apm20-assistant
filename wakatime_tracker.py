"""
wakatime_tracker.py
====================
Pulls REAL coding time from WakaTime — replaces self-reported "did you code today?"
with an actual measured number.

Note: this only tracks time spent ACTIVELY typing in an editor with the WakaTime
extension installed. It does NOT track YouTube/video/browser time — that's a
separate, not-yet-built piece. So this gives you verified coding hours, not
the full 50/50 ratio (content vs code) yet.

Requires WAKATIME_API_KEY environment variable.
"""

import base64
import os

import requests

API_BASE = "https://wakatime.com/api/v1"


def _auth_header(api_key: str) -> dict:
    token = base64.b64encode(f"{api_key}:".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def get_today_coding_time(api_key: str) -> dict:
    """
    Returns:
      {
        "ok": bool,
        "human_readable": str,   # e.g. "1 hr 24 mins"
        "total_seconds": float,
        "languages": [{"name": str, "text": str}, ...],  # top languages today
        "error": str or None,
      }
    """
    result = {"ok": False, "human_readable": None, "total_seconds": 0, "languages": [], "error": None}

    if not api_key:
        result["error"] = "WAKATIME_API_KEY not set"
        return result

    try:
        r = requests.get(
            f"{API_BASE}/users/current/summaries",
            headers=_auth_header(api_key),
            params={"range": "Today"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()

        days = data.get("data", [])
        if not days:
            result["ok"] = True
            result["human_readable"] = "0 mins"
            return result

        today = days[0]
        grand_total = today.get("grand_total", {})
        result["human_readable"] = grand_total.get("text", "0 mins")
        result["total_seconds"] = grand_total.get("total_seconds", 0)
        result["languages"] = [
            {"name": lang["name"], "text": lang["text"]}
            for lang in today.get("languages", [])[:3]
        ]
        result["ok"] = True
        return result

    except Exception as e:
        result["error"] = str(e)
        return result
