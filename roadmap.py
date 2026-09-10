"""
roadmap.py
==========
Rolling task queue. There are NO fixed dates here anymore — the bot tracks
which task set you're currently on (state.json: current_task_index) and
only advances to the next one once a real git push is detected for the
current one. If no push lands by the next 7 AM check, the SAME task set
is shown again.

Every task set targets SKILL_REPO — push your work there to mark it done.
Budget: 2 hours/day for skill-building, always. Keep each task set doable
inside that window; don't pad it with more than 1-2 real resources.

--- Month 1 (Sep 2026) — from APM20_Level0_Execution_Plan ---
Technical Focus: Terminal, Git/GitHub, Python Syntax
Math Core: Discrete Math Basics (Logic, Sets)
Proof-of-Work: CLI Tool #1 (File Automation in Python)
DSA/CP: 10 LeetCode Easy (Python)
"""

SKILL_REPO = "cli-file-automation"  # push your daily work here to auto-complete a task set

TASK_QUEUE = [
    {
        "title": "Day 1 — Terminal, Python & Your First Real Push",
        "tasks": [
            "Open the integrated terminal in VS Code (Terminal -> New Terminal)",
            "Learn 6 commands: pwd/cd, dir or ls, mkdir, cd .., cls or clear, exit",
            "Create hello.py with print(\"Hello\") and run it: python hello.py",
            "Learn 4 git commands: git init, git status, git add ., git commit -m \"message\"",
            "Create the repo cli-file-automation on github.com/adityamohalkar-dev (empty, no README)",
            "git remote add origin <url>, git branch -M main, git push -u origin main — refresh GitHub, confirm hello.py is live",
        ],
        "resources": [
            "Git basics (official docs): https://docs.github.com/en/get-started/git-basics",
        ],
    },
    {
        "title": "Python Syntax — Variables & Control Flow",
        "tasks": [
            "Watch Bro Code's Python full course, up through loops and conditionals (link below)",
            "Solve 5 exercises: FizzBuzz, string reversal, even/odd checker, simple calculator, temperature converter",
            "Save all 5 as separate .py files in a folder called python-basics",
            "git push the python-basics folder to cli-file-automation",
        ],
        "resources": [
            "Bro Code — Python Full Course (direct video): https://www.youtube.com/watch?v=XKHEtdqhLK8",
        ],
    },
    {
        "title": "Functions & File I/O — Building Blocks for CLI Tool #1",
        "tasks": [
            "Read CS50P's file I/O material (link below) — focus on open(), read(), write(), os module basics",
            "Write one script that reads a folder's file list and prints each filename",
            "Write one script that renames or moves files based on their extension (the core mechanic you'll need for CLI Tool #1)",
            "git push both scripts to cli-file-automation",
        ],
        "resources": [
            "CS50P — File I/O lecture (direct playlist): https://www.youtube.com/playlist?list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V",
        ],
    },
    {
        "title": "Proof-of-Work: CLI Tool #1 — File Automation in Python",
        "tasks": [
            "Read the Python argparse tutorial below — just enough to build one command with an argument",
            "Build the tool: a script that organizes a messy folder by sorting files into subfolders by extension (.pdf, .jpg, .py, etc.), run from the terminal with a folder path argument",
            "Test it on a real messy folder (e.g. your Downloads) and confirm it actually works",
            "Write a short README.md — what it does, how to run it",
            "git push the whole project to cli-file-automation",
        ],
        "resources": [
            "Python argparse — official tutorial (direct): https://docs.python.org/3/howto/argparse.html",
        ],
    },
    {
        "title": "Discrete Math Basics — Logic & Sets",
        "tasks": [
            "Watch Neso Academy's Propositional Logic playlist (link below) — through truth tables and logical equivalence",
            "Watch Neso Academy's Set Theory basics (same channel) — union, intersection, subsets",
            "Solve 10 practice problems (5 logic, 5 sets) — any textbook or online problem set",
            "Write your 10 answers with brief reasoning in a file discrete-math-notes.md",
            "git push the notes file to cli-file-automation",
        ],
        "resources": [
            "Neso Academy — Propositional Logic (direct playlist): https://www.youtube.com/playlist?list=PLBlnK6fEyqRjT3oJxFXRgjPNzeS-LFY-q",
        ],
    },
    {
        "title": "10 LeetCode Easy (Python) — Month 1 DSA Target",
        "tasks": [
            "Solve 10 LeetCode Easy problems in Python (arrays, strings, basic loops — no need to pick a topic, just start with the Top 100 Liked Easy filter)",
            "For each one, save your solution as a .py file with a comment explaining your approach in 1-2 sentences",
            "Create a leetcode folder with all 10 solutions",
            "git push the leetcode folder to cli-file-automation — this closes out Month 1",
        ],
        "resources": [
            "LeetCode — filter by Easy: https://leetcode.com/problemset/?difficulty=EASY",
        ],
    },
]

# Generic fallback resources if you ever finish the whole queue above
GENERAL_RESOURCES = [
    "LeetCode (DSA practice): https://leetcode.com/",
    "freeCodeCamp: https://www.freecodecamp.org/",
]

CORE_RULES = [
    "Proof-of-Work Above Pedigree — public GitHub proof beats grades alone",
    "The 50/50 Rule — max 50% consuming content, min 50% writing/debugging code",
    "Zero Fake Credentials — never list what isn't a real public commit",
]
