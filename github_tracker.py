"""
github_tracker.py
==================
Pulls REAL proof-of-work data from GitHub — not self-reported.
Checks every repo you own (including private ones) for commits made today,
and maintains a streak counter in state.json.

Requires a GitHub Personal Access Token (fine-grained, read-only) set as
the GITHUB_PAT environment variable. This is DIFFERENT from the automatic
GITHUB_TOKEN that Actions provides — that one can't see your other repos.
"""

import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

import state_store

IST = ZoneInfo("Asia/Kolkata")
API_BASE = "https://api.github.com"


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _load_state() -> dict:
    return state_store.load_state()


def _save_state(state: dict) -> None:
    state_store.save_state(state)


def get_today_activity(username: str, token: str) -> dict:
    """
    Returns:
      {
        "ok": bool,
        "repos_with_commits": ["repo1", "repo2", ...],
        "total_commits_today": int,
        "error": str or None,
      }
    """
    result = {"ok": False, "repos_with_commits": [], "total_commits_today": 0, "error": None}

    if not token:
        result["error"] = "GITHUB_PAT not set"
        return result

    now_ist = datetime.now(IST)
    start_of_day_ist = now_ist.replace(hour=0, minute=0, second=0, microsecond=0)
    since_iso = start_of_day_ist.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        repos = []
        page = 1
        while True:
            r = requests.get(
                f"{API_BASE}/user/repos",
                headers=_headers(token),
                params={"per_page": 100, "page": page, "affiliation": "owner"},
                timeout=20,
            )
            r.raise_for_status()
            batch = r.json()
            repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1

        for repo in repos:
            repo_name = repo["name"]
            r = requests.get(
                f"{API_BASE}/repos/{username}/{repo_name}/commits",
                headers=_headers(token),
                params={"author": username, "since": since_iso, "per_page": 100},
                timeout=20,
            )
            if r.status_code == 409:
                # empty repo, no commits yet at all — skip
                continue
            r.raise_for_status()
            commits = r.json()
            if commits:
                result["repos_with_commits"].append(repo_name)
                result["total_commits_today"] += len(commits)

        result["ok"] = True
        return result

    except Exception as e:
        result["error"] = str(e)
        return result


def update_streak(had_commits_today: bool) -> dict:
    """
    Call this ONCE per day (evening run only) to update the streak state.
    Returns the updated state dict.
    """
    state = _load_state()
    today_str = datetime.now(IST).strftime("%Y-%m-%d")
    yesterday_str = (datetime.now(IST) - timedelta(days=1)).strftime("%Y-%m-%d")

    if state.get("last_commit_date") == today_str:
        # already updated today, don't double count
        return state

    if had_commits_today:
        if state.get("last_commit_date") == yesterday_str:
            state["current_streak"] = state.get("current_streak", 0) + 1
        else:
            state["current_streak"] = 1
        state["last_commit_date"] = today_str
        state["longest_streak"] = max(state.get("longest_streak", 0), state["current_streak"])
    else:
        # no commit today — streak breaks, but only record the break,
        # don't touch last_commit_date (keeps history honest)
        state["current_streak"] = 0

    _save_state(state)
    return state
