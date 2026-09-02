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
        "resources": [
            "Python install: https://www.python.org/downloads/",
            "VS Code: https://code.visualstudio.com/download",
            "Git install: https://git-scm.com/downloads",
            "GitHub SSH key guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh",
        ],
    },
    "2026-09-01": {
        "focus": "Command Line & Git Workflows",
        "tasks": [
            "Master CLI commands (cd, ls, mkdir, rm)",
            "Learn branching, commit squashing, remote syncing",
        ],
        "deliverable": "CLI cheat-sheet documented",
        "resources": [
            "CLI basics (freeCodeCamp — verified): https://www.youtube.com/watch?v=mABpAI-pCw0",
            "Git branching (interactive, learn by doing): https://learngitbranching.js.org/",
            "Atlassian Git branching guide: https://www.atlassian.com/git/tutorials/using-branches",
            "Git rebase/squash guide: https://www.atlassian.com/git/tutorials/rewriting-history",
        ],
    },
    "2026-09-02": {
        "focus": "Python Logic & Control Flow",
        "tasks": [
            "CS50P (Week 0-1) or Bro Code — variables, if/else, loops",
        ],
        "deliverable": "15 logic exercises solved (FizzBuzz, String Reversal, etc.)",
        "resources": [
            "CS50P full course (Harvard, free): https://cs50.harvard.edu/python/2022/",
            "CS50P full playlist — start at Lecture 0 (verified): https://www.youtube.com/playlist?list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V",
            "Bro Code Python full course playlist (verified): https://www.youtube.com/playlist?list=PL6zix6brJZNFp_nAtoPGEps1YAZO10G5S",
            "Practice problems: https://www.hackerrank.com/domains/python",
        ],
    },
    "2026-09-03": {
        "focus": "Functions, Modules & File I/O",
        "tasks": [
            "Functional scope, *args/**kwargs, modules",
            "Reading/writing files (csv, json)",
        ],
        "deliverable": "File parsing script pushed via Git branch",
        "resources": [
            "CS50P Week 3 (Functions): https://cs50.harvard.edu/python/2022/weeks/3/",
            "Real Python — *args/**kwargs: https://realpython.com/python-kwargs-and-args/",
            "Real Python — Reading/Writing files: https://realpython.com/read-write-files-python/",
            "Python csv/json docs: https://docs.python.org/3/library/csv.html",
        ],
    },
    "2026-09-04": {
        "focus": "Object-Oriented Python (OOP)",
        "tasks": [
            "Classes, Objects, Inheritance, Methods, Encapsulation",
            "Error handling (try/except)",
        ],
        "deliverable": "Modular class-based script, no errors",
        "resources": [
            "Corey Schafer OOP series, part 1 (verified): https://youtu.be/ZDa-Z5JzLYM",
            "CS50P Week 6 (OOP): https://cs50.harvard.edu/python/2022/weeks/6/",
            "Real Python — OOP intro: https://realpython.com/python3-object-oriented-programming/",
            "Real Python — try/except: https://realpython.com/python-exceptions/",
        ],
    },
    "2026-09-05": {
        "focus": "Building Project #1 (CLI Tool)",
        "tasks": [
            "Build a full CLI tool (Log Analyzer / Grade Calculator)",
        ],
        "deliverable": "Core project architecture + working code",
        "resources": [
            "Python argparse tutorial (build real CLIs): https://docs.python.org/3/howto/argparse.html",
            "Example CLI tool projects: https://github.com/topics/cli-tool?l=python",
            "CS50P Week 7 (File I/O project ideas): https://cs50.harvard.edu/python/2022/weeks/7/",
        ],
    },
    "2026-09-06": {
        "focus": "Documentation & Code Quality",
        "tasks": [
            "Format with Black/Flake8",
            "Write a clean README.md",
        ],
        "deliverable": "First documented CLI project published on GitHub",
        "resources": [
            "Black formatter docs: https://black.readthedocs.io/en/stable/",
            "Flake8 docs: https://flake8.pycqa.org/en/latest/",
            "How to write a good README: https://www.makeareadme.com/",
            "Awesome README examples: https://github.com/matiassingers/awesome-readme",
        ],
    },
    "2026-09-07": {
        "focus": "Linear Algebra in Python",
        "tasks": [
            "3Blue1Brown — Essence of Linear Algebra",
            "Pure Python vector/matrix multiplication",
        ],
        "deliverable": "10 pure-Python math scripts committed",
        "resources": [
            "3Blue1Brown — Essence of Linear Algebra (full playlist): https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab",
            "Khan Academy Linear Algebra: https://www.khanacademy.org/math/linear-algebra",
        ],
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

# Generic ongoing resources — shown on weekday/Sunday messages (post-sprint)
GENERAL_RESOURCES = [
    "LeetCode (DSA practice): https://leetcode.com/",
    "freeCodeCamp: https://www.freecodecamp.org/",
    "Awesome lists (curated free resources, any topic): https://github.com/sindresorhus/awesome",
]

# ---------------------------------------------------------------
# 3) CORE OPERATING RULES (shown occasionally as reinforcement)
# ---------------------------------------------------------------
CORE_RULES = [
    "Proof-of-Work Above Pedigree — public GitHub proof beats grades alone",
    "The 50/50 Rule — max 50% consuming content, min 50% writing/debugging code",
    "Zero Fake Credentials — never list what isn't a real public commit",
]
