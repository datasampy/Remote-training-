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

buildzone_md = """---

# 🚀 BUILD ZONE — now make your OWN things!

**Congratulations, coder!** 🎉 You finished the quest. In the game you typed in
the little black box. To *build real things*, you write Python in **normal Colab
cells** — exactly the same Python you just learned.

**How to use a real code cell:**
- Click **`+ Code`** at the top to make a new cell (or use the ones below).
- Type your code, then press **▶** (or **Shift + Enter**) to run it.
- Here, `input()` is real — the program will actually wait for you to type! ⌨️

Below are **5 starter projects**. For each one:
1. ▶️ **Run it** and play.
2. ✏️ Find the lines marked `# ✏️` and **change them** to make it yours.
3. 💥 **Break it, fix it, remix it** — that's how real coders learn!

Every project uses only things you learned in the game: `print`, variables,
`input`, `if/elif/else`, loops, lists, dictionaries and functions. 💪
"""

buildzone_1 = '''# 🎲 PROJECT 1 — Guess My Number
# Skills you already know: variables, while loop, if/elif/else, input.
import random

secret = random.randint(1, 20)   # ✏️ change 20 to make it harder or easier
guesses = 0
print("🎲 I'm thinking of a number from 1 to 20. Can you guess it?")

while True:
    guess = int(input("Your guess: "))
    guesses = guesses + 1
    if guess < secret:
        print("⬆️ Too low! Try higher.")
    elif guess > secret:
        print("⬇️ Too high! Try lower.")
    else:
        print(f"🎉 YES! You got it in {guesses} guesses!")
        break
'''

buildzone_2 = '''# 📖 PROJECT 2 — Silly Story Maker (Mad Libs)
# Skills: input, variables, f-strings.
name   = input("A name: ")
animal = input("An animal: ")
place  = input("A place: ")
food   = input("A food: ")

# ✏️ Change the story to anything you want!
print()
print("📖 Here is your silly story:")
print(f"One day, {name} rode a giant {animal} all the way to {place}.")
print(f"They were so hungry they ate {food} until the sun went down. The End! 🌅")
'''

buildzone_3 = '''# ✊✋✌️ PROJECT 3 — Rock, Paper, Scissors
# Skills: functions, lists, dictionaries, random, if/elif/else, loops.
import random

def play_round():
    options = ["rock", "paper", "scissors"]
    you = input("Choose rock, paper or scissors: ").strip().lower()
    computer = random.choice(options)
    print(f"🤖 Computer chose {computer}")
    if you == computer:
        return "tie"
    beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if beats.get(you) == computer:
        return "you"
    return "computer"

score = {"you": 0, "computer": 0}
for round_number in range(3):        # ✏️ play more rounds by changing 3
    print(f"\\n--- Round {round_number + 1} ---")
    result = play_round()
    if result == "you":
        print("✅ You win this round!"); score["you"] += 1
    elif result == "computer":
        print("❌ Computer wins this round."); score["computer"] += 1
    else:
        print("🤝 It's a tie!")

print(f"\\n🏁 Final — You: {score['you']}, Computer: {score['computer']}")
'''

buildzone_4 = '''# 🧮 PROJECT 4 — Pocket-Money Saver
# Skills: input, int, maths, if/else, f-strings.
weekly = int(input("How much pocket money do you get each week? "))
weeks  = int(input("How many weeks will you save? "))
goal   = int(input("How much does the thing you want cost? "))

saved = weekly * weeks
print(f"\\n💰 In {weeks} weeks you'll have saved {saved}.")
if saved >= goal:
    print(f"🎉 That's enough for your {goal} goal — go for it!")
else:
    print(f"😮 You'll still need {goal - saved} more. Try saving longer!")
'''

buildzone_5 = '''# 🤖 PROJECT 5 — Your OWN Quiz Bot (the big one!)
# Skills: EVERYTHING — lists, dictionaries, functions, loops, input, if, f-strings.

# ✏️ Add, remove or change these questions — make the quiz about YOUR topic!
quiz = [
    {"q": "What is the capital of France? ", "a": "paris"},
    {"q": "How many legs does a spider have? ", "a": "8"},
    {"q": "What planet do we live on? ", "a": "earth"},
]

def ask(question, correct):
    guess = input(question).strip().lower()
    return guess == correct.strip().lower()

score = 0
for item in quiz:
    if ask(item["q"], item["a"]):
        print("✅ Correct!")
        score += 1
    else:
        print(f"❌ Nope — the answer was {item['a']}.")

print(f"\\n🏆 You scored {score} out of {len(quiz)}!")
if score == len(quiz):
    print("Perfect score — you're a genius! 🌟")
'''

yourturn_md = """---

## 🧠 Your Turn — challenges to level up

Pick one and build it using the projects above as a starting point:

- 🎨 **Make Project 2 your own story** with 6+ blanks and a twist ending.
- 🏆 **Turn Project 5 into a quiz about your favourite game, animal or team** —
  add 8 questions and a "You are a...!" result at the end based on the score.
- 🔢 **Add difficulty to Project 1**: let the player pick Easy (1–10) or Hard (1–50).
- ✂️ **Best-of-5 Rock Paper Scissors**: keep playing until someone wins 3 rounds.
- 🤖 **Build a tiny chatbot**: ask the user questions in a loop and reply with
  `if/elif` depending on what they type. Type "bye" to stop.

**Where to go next**
- Try Python's `turtle` drawing, or make a to-do list with a `list`.
- Free practice: <https://www.codewars.com>, <https://www.checkio.org>,
  or search "Python for kids projects".

> 🌟 The secret to becoming a real coder: **change working code and see what
> happens.** Every bug you fix makes you stronger.
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
| **7+** | 🚀 Build Zone | 5 real projects to run, edit and remix in normal cells |

**By the end** kids can read code, use variables, make decisions, loop, store
data, write their own functions, and assemble a working program — enough to
build something real of their own. 🎓

**The bridge to real building:** after the game, the **🚀 Build Zone** cells show
kids that the *same* Python works in ordinary Colab cells (where `input()` runs
for real). They run a project, change the `# ✏️` lines, and remix it — this is
where "I learned Python" becomes "I can build things." Great for Day 7 and the
whole second week.

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
        md(buildzone_md),
        code(buildzone_1),
        code(buildzone_2),
        code(buildzone_3),
        code(buildzone_4),
        code(buildzone_5),
        md(yourturn_md),
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

# Safety: make sure every Build Zone project at least compiles (no syntax errors).
for name, src in [("buildzone_1", buildzone_1), ("buildzone_2", buildzone_2),
                  ("buildzone_3", buildzone_3), ("buildzone_4", buildzone_4),
                  ("buildzone_5", buildzone_5)]:
    compile(src, name, "exec")

with open("PythonQuest.ipynb", "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Wrote PythonQuest.ipynb with", len(nb["cells"]), "cells.")
print("Build Zone projects compiled cleanly ✅")
