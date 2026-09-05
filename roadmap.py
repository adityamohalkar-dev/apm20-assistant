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
"""

SKILL_REPO = "hello-world"  # push your daily work here to auto-complete a task set

TASK_QUEUE = [
    {
        "title": "Windows Terminal Basics (CMD + PowerShell)",
        "tasks": [
            "Watch the CMD basics video below",
            "Watch the PowerShell basics video below",
            "Practice 10 commands yourself: cd, dir, mkdir, del, copy, cls, echo, exit, ls (PowerShell), Get-Location (PowerShell)",
            "Create a file commands.txt listing the 10 commands + what each does, in one sentence",
            "git push commands.txt to hello-world",
        ],
        "resources": [
            "CMD basics (direct video): https://www.youtube.com/watch?v=QBWX_4ho8D4",
            "PowerShell basics (direct video, ~30 min): https://www.youtube.com/watch?v=GyvEMcMh3rc",
        ],
    },
    {
        "title": "Python Fundamentals — Variables & Control Flow",
        "tasks": [
            "Watch CS50P Lecture 0 (Functions, Variables) from the playlist below",
            "Solve 5 exercises: FizzBuzz, String Reversal, even/odd checker, simple calculator, temperature converter",
            "Save all 5 as separate .py files in a new folder called python-basics",
            "git push the python-basics folder to hello-world",
        ],
        "resources": [
            "CS50P Lecture 0 (Harvard, direct playlist — watch episode 0 only): https://www.youtube.com/playlist?list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V",
        ],
    },
    {
        "title": "Functions, Modules & File I/O",
        "tasks": [
            "Read the Real Python article on *args/**kwargs (link below)",
            "Write 3 functions using *args and **kwargs that actually do something (not toy examples — e.g. a function that sums any number of inputs)",
            "Write one script that reads a .csv file and prints each row",
            "git push both to hello-world",
        ],
        "resources": [
            "Real Python — *args/**kwargs (direct article): https://realpython.com/python-kwargs-and-args/",
        ],
    },
    {
        "title": "Object-Oriented Python (OOP)",
        "tasks": [
            "Watch Corey Schafer's OOP video below (Classes and Instances)",
            "Build one class with at least 2 methods and 2 attributes (pick something real — e.g. a BankAccount or a Student class)",
            "Add basic error handling (try/except) to one method",
            "git push the class file to hello-world",
        ],
        "resources": [
            "Corey Schafer — Python OOP, Classes & Instances (direct video): https://youtu.be/ZDa-Z5JzLYM",
        ],
    },
    {
        "title": "Build Project #1 — A Real CLI Tool",
        "tasks": [
            "Read the Python argparse tutorial below (just enough to build one command)",
            "Build a small CLI tool that does ONE real thing (e.g. a word counter, a simple to-do list, a unit converter)",
            "Write a short README.md explaining what it does and how to run it",
            "git push the whole project as a new folder in hello-world",
        ],
        "resources": [
            "Python argparse — official tutorial (direct): https://docs.python.org/3/howto/argparse.html",
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
