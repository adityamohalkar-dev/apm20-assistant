"""
roadmap.py
==========
Single source of truth for APM20 Assistant.
Edit THIS file whenever your plan changes — notify.py just reads it.
Dates use ISO format "YYYY-MM-DD".
"""

# ---------------------------------------------------------------
# 1) THE 8-DAY PRE-COLLEGE SPRINT (Aug 31 - Sep 7, 2026)
# ---------------------------------------------------------------
SPRINT_8DAY = {
    "2026-08-31": {
        "focus": "Dev Environment & Git Setup",
        "tasks": [
            "Install Python 3.11+, VS Code, Git, WSL2/Linux terminal",
            "Set up SSH keys for GitHub",
        ],
        "deliverable": "Terminal working; `hello-world` repo pushed to GitHub",
    },
    "2026-09-01": {
        "focus": "Command Line & Git Workflows",
        "tasks": [
            "Master CLI commands (cd, ls, mkdir, rm)",
            "Learn branching, commit squashing, remote syncing",
        ],
        "deliverable": "CLI cheat-sheet documented",
    },
    "2026-09-02": {
        "focus": "Python Logic & Control Flow",
        "tasks": [
            "CS50P (Week 0-1) or Bro Code — variables, if/else, loops",
        ],
        "deliverable": "15 logic exercises solved (FizzBuzz, String Reversal, etc.)",
    },
    "2026-09-03": {
        "focus": "Functions, Modules & File I/O",
        "tasks": [
            "Functional scope, *args/**kwargs, modules",
            "Reading/writing files (csv, json)",
        ],
        "deliverable": "File parsing script pushed via Git branch",
    },
    "2026-09-04": {
        "focus": "Object-Oriented Python (OOP)",
        "tasks": [
            "Classes, Objects, Inheritance, Methods, Encapsulation",
            "Error handling (try/except)",
        ],
        "deliverable": "Modular class-based script, no errors",
    },
    "2026-09-05": {
        "focus": "Building Project #1 (CLI Tool)",
        "tasks": [
            "Build a full CLI tool (Log Analyzer / Grade Calculator)",
        ],
        "deliverable": "Core project architecture + working code",
    },
    "2026-09-06": {
        "focus": "Documentation & Code Quality",
        "tasks": [
            "Format with Black/Flake8",
            "Write a clean README.md",
        ],
        "deliverable": "First documented CLI project published on GitHub",
    },
    "2026-09-07": {
        "focus": "Linear Algebra in Python",
        "tasks": [
            "3Blue1Brown — Essence of Linear Algebra",
            "Pure Python vector/matrix multiplication",
        ],
        "deliverable": "10 pure-Python math scripts committed",
    },
}

SPRINT_END_DATE = "2026-09-07"

# ---------------------------------------------------------------
# 2) WEEKLY OPERATING OS (from Sep 8 onward)
# ---------------------------------------------------------------
WEEKDAY_BLOCK = [
    "Hour 1 (5:30-6:30 PM): College academics / exam prep",
    "Hours 2-3 (6:30-8:30 PM): Deep skill building (Python / C++ / Math)",
    "Hour 4 (8:30-9:30 PM): LeetCode / DSA / logic puzzles",
]

SUNDAY_BLOCK = [
    "Block 1 (4 hrs): Real-world projects & systems architecture",
    "Block 2 (3 hrs): Open-source PRs & hackathon builds",
    "Block 3 (3 hrs): Networking, cold outreach, weekly self-audit",
]

SUNDAY_REVIEW_CHECKLIST = [
    "What exact phase/sub-topic was I focused on this week?",
    "Did I stick to ONE primary resource (no tutorial hell)?",
    "Was at least 50% of my time spent writing/debugging code?",
    "What did I push to my public GitHub this week?",
    "How many LeetCode/DSA problems did I solve independently?",
    "Did I contact 5+ engineering leads or submit open-source PRs?",
]

# ---------------------------------------------------------------
# 3) CORE OPERATING RULES (shown occasionally as reinforcement)
# ---------------------------------------------------------------
CORE_RULES = [
    "Proof-of-Work Above Pedigree — public GitHub proof beats grades alone",
    "The 50/50 Rule — max 50% consuming content, min 50% writing/debugging code",
    "Zero Fake Credentials — never list what isn't a real public commit",
]
