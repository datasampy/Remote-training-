"""Assemble PythonQuest.ipynb from engine.py + levels.py + intro cells."""
import json, re

with open("engine.py") as f:
    engine_src = f.read()
with open("levels.py") as f:
    levels_src = f.read()
# levels.py imports helpers from engine; in the merged cell they already exist.
levels_src = re.sub(r"^from engine import .*\n", "", levels_src, flags=re.M)

setup_cell = (
    "# @title 🎮 STEP 1 — Load the game  { display-mode: \"form\" }\n"
    "# Just press the ▶ play button on the left of this cell. You don't need to\n"
    "# read this code — it's the game engine. (Curious kids: peek all you like!)\n\n"
    + engine_src.rstrip() + "\n\n\n"
    + "# ---------------------------------------------------------------\n"
    + "#  THE 27 LEVELS\n"
    + "# ---------------------------------------------------------------\n"
    + levels_src.rstrip() + "\n\n\n"
    + 'print("✅ Game engine loaded with", len(LEVELS),\n'
    + '      "levels! Now run STEP 2 below to play. 🚀")\n'
)

launch_cell = (
    "# @title 🕹️ STEP 2 — Play!  { display-mode: \"form\" }\n"
    "# 1) Change the name below to YOUR name.\n"
    "# 2) Press the ▶ play button. Your adventure begins!\n\n"
    'my_name = "Coder"   # <-- put your name here, keep the quotes\n\n'
    "quest = PythonQuest(LEVELS, player=my_name)\n"
    "quest.start()\n"
)

commands_cell = (
    "# 🧭 HANDY COMMANDS — run any of these in a new cell whenever you like:\n"
    "\n"
    "quest.map()      # 🗺️  see the whole adventure map & your progress\n"
    "# quest.start()  # ▶️  jump back into the current level\n"
    "# quest.reset()  # 🧹  erase progress and start the whole quest over\n"
)

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}

def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": text.splitlines(keepends=True)}

intro_md = """# 🐍 PythonQuest — Learn Python by Playing!

### Welcome, brave coder! 🚀

This is a **game**, not a boring lesson. You'll travel through **7 worlds** and
**27 levels**, starting from your very first `print()` and ending by building a
**real Quiz Bot game** all by yourself. Meet **Pixel** 🤖, your robot guide!

**How to play — only 2 steps:**

1. ▶️ Run **STEP 1** below once (it loads the game). Press the little **play
   button** on the left of the cell, or click it and press **Shift + Enter**.
2. 🕹️ Run **STEP 2** to open your game panel. Type code in the black box and
   press **▶ RUN & CHECK**!

> 💡 **Tip:** Stuck on a level? Tap **💡 Hint**. Really stuck? **👀 Show Answer**
> appears after a hint — but try typing it yourself, that's how your fingers
> learn! Your progress **saves automatically**, so you can close Colab and come
> back later.

---
"""

teacher_md = """---

## 👩‍🏫 For the teacher / parent — a 1-week plan

Kids learn each idea, then **immediately use it** in a puzzle that auto-checks
their code and celebrates every win. No memorising definitions — they *do* it.

| Day | Worlds | They learn to… |
|----|---------|----------------|
| **1** | 🚀 World 1 | print, strings, f-strings — make the computer talk |
| **2** | 📦 World 2 | variables, numbers/maths, `input()`, types |
| **3** | 🔀 World 3 | booleans, `if/elif/else`, `and/or/not` — decisions |
| **4** | 🔁 World 4 | `for`, `range`, `while` loops, building totals |
| **5** | 🗃️ World 5 | lists & dictionaries — storing lots of data |
| **6** | ⚙️ World 6 | **functions** — building reusable machines |
| **7** | 🏆 World 7 | **build a real Quiz Bot game** from scratch! |

**By the end** kids can read code, use variables, make decisions, loop, store
data, write their own functions, and assemble a working program — enough to
build something real of their own. 🎓

**Tips for running it**
- One notebook per child (File → *Save a copy in Drive*). Progress saves per session.
- ~4 levels a day keeps it fun and un-rushed; let fast learners race ahead.
- The **💡 Hint** ladder is designed so kids solve it themselves — nudge them to
  hints before answers.
- After World 7, challenge them: *"Now change the quiz questions to your own!"* —
  editing working code is where confidence really grows.

*Built with ❤️ to make first steps in Python feel like play.*
"""

nb = {
    "cells": [
        md(intro_md),
        code(setup_cell),
        code(launch_cell),
        md("### 🧭 Extra commands\n\nRun this cell any time to see your map, or to reset your progress.\n"),
        code(commands_cell),
        md(teacher_md),
    ],
    "metadata": {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}

with open("PythonQuest.ipynb", "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Wrote PythonQuest.ipynb with", len(nb["cells"]), "cells.")
