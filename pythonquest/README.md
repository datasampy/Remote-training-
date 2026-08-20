# 🐍 PythonQuest — Learn Python by Playing

A colourful, level-by-level coding **game** that teaches kids Python inside a
**Google Colab notebook**. Kids go from their very first `print()` to building a
real **Quiz Bot game** — enough Python to build something of their own within a
week.

No boring definitions to memorise. Every idea is learned by *doing* a small
puzzle that auto-checks the code and celebrates every win. 🎉

---

## ▶️ How to play (2 ways to open it)

**Option A — one-click in Colab (easiest)**

Open this link (replace the branch/path if you moved the file):

```
https://colab.research.google.com/github/datasampy/remote-training-/blob/claude/python-kids-learning-game-e81pwy/pythonquest/PythonQuest.ipynb
```

**Option B — upload the file**

1. Download `PythonQuest.ipynb`.
2. Go to <https://colab.research.google.com> → **File → Upload notebook** → pick it.

Then, inside the notebook:

1. ▶️ Run **STEP 1** once (loads the game).
2. 🕹️ Put your name in **STEP 2** and run it — your game panel opens!
3. Type code in the black box and press **▶ RUN & CHECK**.

> 💾 Tip: each child should do **File → *Save a copy in Drive*** so their
> progress and edits are their own. Progress also auto-saves during a session.

---

## 🗺️ The adventure — 7 worlds, 27 levels

| World | Theme | Skills |
|------|-------|--------|
| 🚀 1 — Blast Off | Talking to the computer | `print`, strings, f-strings |
| 📦 2 — Memory Boxes | Storing things | variables, maths, `input()`, `int()` |
| 🔀 3 — Crossroads | Making decisions | booleans, `if/elif/else`, `and/or/not` |
| 🔁 4 — Loop Land | Repeating | `for`, `range`, `while`, counters |
| 🗃️ 5 — Treasure Chests | Storing lots | lists & dictionaries |
| ⚙️ 6 — Machine Shop | Reusable machines | **functions**, `return`, `%` |
| 🏆 7 — Boss Build | A real project | build a working **Quiz Bot** 🎮 |

Kids earn **XP**, climb **ranks** (🐣 Hatchling → 👑 Grand Champion), and collect
**badges**. There's a hint ladder 💡 and a *Show Answer* 👀 safety net, plus
kid-friendly translations of Python errors so nobody gets stuck or scared.

### Suggested 1-week plan
~4 levels a day, one world per day (Worlds 1–2 can share Day 1–2 comfortably).
By Day 7 they assemble the Quiz Bot themselves — then the real fun: **"change
the questions to your own!"**

---

## 🛠️ For developers / editing the game

The notebook is generated from small, readable source files:

| File | What it is |
|------|-----------|
| `engine.py` | The game engine (UI, XP, checking, error help, loop guard) |
| `levels.py` | All 27 levels: story, concept, task, hints, answer, checker |
| `build_notebook.py` | Bundles `engine.py` + `levels.py` into `PythonQuest.ipynb` |
| `test_levels.py` | Verifies every answer passes & every scaffold has a real TODO |
| `PythonQuest.ipynb` | **The generated notebook kids actually open** |

**Add or edit a level:** edit `levels.py`, then:

```bash
python3 test_levels.py        # all answers pass, all starters fail (as intended)
python3 build_notebook.py     # regenerate PythonQuest.ipynb
```

Each level is a dict. The `check(ws, out)` function receives the player's
variables (`ws`) and everything they printed (`out`) and returns
`(passed, message)`. Starters are **scaffolds with a `# <- TODO`** so kids write
the key line themselves; the `answer` is the reveal shown by *Show Answer*.

**Safety:** player code runs through a loop guard, so an accidental infinite
`while` loop is stopped automatically instead of freezing Colab. `input()` is
mocked with preset answers so interactive programs never hang.
