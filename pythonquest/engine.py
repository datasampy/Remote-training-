# =====================================================================
#  🐍 PYTHONQUEST  —  Learn Python by Playing (Google Colab edition)
#  A level-by-level coding adventure engine for kids.
#  Everything runs inside one friendly game panel. Just press RUN.
# =====================================================================
import io, json, os, re, html, contextlib, traceback, random

try:
    import ipywidgets as W
    from IPython.display import display, HTML, clear_output
    _HAS_WIDGETS = True
except Exception:                       # pragma: no cover - non-Colab fallback
    _HAS_WIDGETS = False

# Colab needs this to show custom widgets nicely.
try:
    from google.colab import output as _colab_output
    _colab_output.enable_custom_widget_manager()
except Exception:
    pass

SAVE_PATH = "/content/pythonquest_save.json"
if not os.path.isdir("/content"):        # so it also works off-Colab
    SAVE_PATH = os.path.join(os.path.expanduser("~"), ".pythonquest_save.json")


# ---------------------------------------------------------------------
#  Small helpers used by the level checkers
# ---------------------------------------------------------------------
def norm(text):
    """Lowercase, trim, squeeze spaces — for forgiving text comparison."""
    return re.sub(r"\s+", " ", str(text).strip().lower())

def lines(text):
    return [ln.rstrip() for ln in str(text).splitlines() if ln.strip() != ""]

def ok(msg="Perfect!"):
    return True, msg

def no(msg):
    return False, msg


# ---------------------------------------------------------------------
#  Friendly translations of scary Python errors
# ---------------------------------------------------------------------
def friendly_error(exc):
    name = type(exc).__name__
    detail = html.escape(str(exc))
    tips = {
        "SyntaxError":     "Python couldn't read your code. Check for a missing "
                           ": at the end of a line, or an unmatched ( ) or \" \".",
        "IndentationError":"Your spacing is off. Lines inside an if/for/def need to "
                           "be pushed in (indented) by 4 spaces.",
        "NameError":       "You used a word Python doesn't know yet. Did you spell a "
                           "variable name the same way you made it? Are your quotes missing?",
        "TypeError":       "You mixed things that don't fit — like adding a number to a "
                           "word. Try str() or int() to convert first.",
        "ValueError":      "The value doesn't fit what was expected — e.g. turning the "
                           "word \"cat\" into a number with int().",
        "ZeroDivisionError":"You divided by zero. Nothing can be split into 0 pieces!",
        "IndexError":      "You asked for an item that isn't there. Remember lists start "
                           "counting at 0.",
        "KeyError":        "That key isn't in the dictionary. Check the spelling of the key.",
        "AttributeError":  "That thing can't do that action. Check the method name.",
    }
    tip = tips.get(name, "Read the message carefully — it usually points at the line.")
    return name, detail, tip


# =====================================================================
#  THE GAME ENGINE
# =====================================================================
class PythonQuest:
    RANKS = [
        (0,   "🐣 Hatchling Coder"),
        (60,  "🐍 Baby Python"),
        (150, "🦎 Code Explorer"),
        (280, "🐲 Loop Wizard"),
        (450, "🦅 Function Master"),
        (650, "🚀 Python Hero"),
        (900, "👑 Grand Code Champion"),
    ]

    def __init__(self, levels, player=None):
        self.levels = levels
        self.state = self._load()
        if player:
            self.state["player"] = player
        # persistent code workspace shared across levels (feels like one program)
        self.ws = {}
        self.hint_i = 0
        self.revealed = False
        self.screen = W.Output() if _HAS_WIDGETS else None

    # ---------- save / load ----------
    def _fresh(self):
        return {"player": "Coder", "xp": 0, "level": 0,
                "done": [], "badges": []}

    def _load(self):
        try:
            with open(SAVE_PATH) as f:
                s = json.load(f)
                for k, v in self._fresh().items():
                    s.setdefault(k, v)
                return s
        except Exception:
            return self._fresh()

    def _save(self):
        try:
            with open(SAVE_PATH, "w") as f:
                json.dump(self.state, f)
        except Exception:
            pass

    def reset(self):
        """Wipe all progress and start the adventure over."""
        self.state = self._fresh()
        self.ws = {}
        self._save()
        print("🧹 Progress reset! Run  quest.start()  to begin again.")

    # ---------- rank / progress ----------
    def _rank(self):
        r = self.RANKS[0][1]
        for need, title in self.RANKS:
            if self.state["xp"] >= need:
                r = title
        return r

    def _next_rank_need(self):
        for need, _ in self.RANKS:
            if self.state["xp"] < need:
                return need
        return self.RANKS[-1][0]

    # =================================================================
    #  PUBLIC ENTRY POINTS
    # =================================================================
    def start(self):
        if not _HAS_WIDGETS:
            print("This game needs ipywidgets (built into Google Colab).")
            return
        self._inject_css()
        display(self.screen)
        self._render()

    def map(self):
        """Show the whole adventure map and what you've unlocked."""
        if not _HAS_WIDGETS:
            return
        self._inject_css()
        rows, world = [], None
        for i, lv in enumerate(self.levels):
            if lv["world"] != world:
                world = lv["world"]
                rows.append(f"<div class='pq-world'>{html.escape(world)}</div>")
            if i in self.state["done"]:
                mark, cls = "✅", "pq-cell done"
            elif i == self.state["level"]:
                mark, cls = "▶️", "pq-cell now"
            elif i <= self.state["level"]:
                mark, cls = "🔓", "pq-cell open"
            else:
                mark, cls = "🔒", "pq-cell lock"
            rows.append(
                f"<div class='{cls}'>{mark} <b>{i+1}.</b> "
                f"{html.escape(lv['title'])}</div>")
        badges = " ".join(self.state["badges"]) or "—"
        display(HTML(
            f"<div class='pq-card pq-map'><h2>🗺️ Your Quest Map</h2>"
            f"<div class='pq-sub'>Rank: <b>{self._rank()}</b> &nbsp;•&nbsp; "
            f"XP: <b>{self.state['xp']}</b> &nbsp;•&nbsp; Badges: {badges}</div>"
            + "".join(rows) + "</div>"))

    # =================================================================
    #  RENDERING A LEVEL
    # =================================================================
    def _render(self):
        self.hint_i = 0
        self.revealed = False
        with self.screen:
            clear_output(wait=True)

            if self.state["level"] >= len(self.levels):
                display(HTML(self._certificate()))
                return

            i = self.state["level"]
            lv = self.levels[i]

            display(HTML(self._header(i, lv)))
            display(HTML(self._story(lv)))
            display(HTML(self._concept(lv)))

            code = W.Textarea(
                value=lv.get("starter", "# write your code here\n"),
                layout=W.Layout(width="100%", height="150px"))
            code.add_class("pq-code")
            self._code = code

            run   = W.Button(description="▶  RUN & CHECK", button_style="success")
            hint  = W.Button(description="💡 Hint")
            ans   = W.Button(description="👀 Show Answer")
            skip  = W.Button(description="⏭ Skip")
            back  = W.Button(description="🗺 Map")
            run.add_class("pq-btn"); hint.add_class("pq-btn")
            ans.add_class("pq-btn"); skip.add_class("pq-btn"); back.add_class("pq-btn")

            run.on_click(self._on_run)
            hint.on_click(self._on_hint)
            ans.on_click(self._on_answer)
            skip.on_click(self._on_skip)
            back.on_click(lambda b: self.map())

            self._out = W.Output()
            display(W.HTML("<div class='pq-label'>✏️ Your code:</div>"))
            display(code)
            display(W.HBox([run, hint, ans, skip, back]))
            display(self._out)

    # ---------- HTML blocks ----------
    def _header(self, i, lv):
        pct = int(len(self.state["done"]) / len(self.levels) * 100)
        nxt = self._next_rank_need()
        return (
            f"<div class='pq-card pq-head'>"
            f"<div class='pq-headtop'>"
            f"<div><span class='pq-lvl'>LEVEL {i+1} / {len(self.levels)}</span>"
            f"<h1>{html.escape(lv['title'])}</h1>"
            f"<div class='pq-world2'>{html.escape(lv['world'])}</div></div>"
            f"<div class='pq-avatar'>{lv.get('emoji','🐍')}</div></div>"
            f"<div class='pq-sub'>👤 {html.escape(self.state['player'])} "
            f"&nbsp;•&nbsp; {self._rank()} &nbsp;•&nbsp; "
            f"⭐ {self.state['xp']} XP</div>"
            f"<div class='pq-bar'><div class='pq-fill' style='width:{pct}%'>"
            f"{pct}%</div></div></div>")

    def _story(self, lv):
        return (f"<div class='pq-card pq-story'>"
                f"<b>🤖 Pixel says:</b> {lv['story']}</div>")

    def _concept(self, lv):
        return (f"<div class='pq-card pq-concept'>"
                f"<h3>📚 What to learn</h3>{lv['concept']}"
                f"<div class='pq-task'><b>🎯 Your mission:</b><br>{lv['task']}</div>"
                f"</div>")

    # ---------- button handlers ----------
    def _on_run(self, b):
        lv = self.levels[self.state["level"]]
        src = self._code.value
        with self._out:
            clear_output(wait=True)
            buf = io.StringIO()
            self.ws["input"] = _mock_input(lv.get("inputs", []))
            try:
                with contextlib.redirect_stdout(buf), _loop_guard():
                    exec(src, self.ws)
            except _LoopRunaway:                 # infinite / runaway loop
                display(HTML(
                    "<div class='pq-card pq-err'>"
                    "<b>🔁 Whoa! Your loop ran WAY too many times.</b><br>"
                    "I stopped it so nothing freezes. This usually means a "
                    "<code>while</code> loop never stops — did you forget to "
                    "change the value that ends it? "
                    "(for example <code>n = n - 1</code> inside the loop)</div>"))
                return
            except Exception as e:               # kid-friendly error
                name, detail, tip = friendly_error(e)
                display(HTML(
                    f"<div class='pq-card pq-err'>"
                    f"<b>😅 Oops — {name}</b><br>"
                    f"<code>{detail}</code><br><br>💡 {tip}</div>"))
                return

            out = buf.getvalue()
            if out.strip():
                display(HTML("<div class='pq-out'><b>🖥️ Output:</b><pre>"
                             + html.escape(out) + "</pre></div>"))

            try:
                passed, msg = lv["check"](self.ws, out)
            except Exception:
                passed, msg = False, ("Almost! Something in your answer wasn't "
                                      "quite what the mission asked for.")

            if passed:
                self._win(lv, msg)
            else:
                display(HTML(f"<div class='pq-card pq-try'>"
                             f"<b>🤔 Not yet!</b> {msg}<br>"
                             f"<small>Tweak your code and press RUN again. "
                             f"Stuck? Tap 💡 Hint.</small></div>"))

    def _win(self, lv, msg):
        i = self.state["level"]
        first = i not in self.state["done"]
        gained = lv.get("xp", 20) if first else 0
        if first:
            self.state["done"].append(i)
            self.state["xp"] += gained
            if lv.get("badge") and lv["badge"] not in self.state["badges"]:
                self.state["badges"].append(lv["badge"])
            self._save()

        conf = "".join(random.choice("🎉✨🎊⭐🌟💫") for _ in range(10))
        display(HTML(
            f"<div class='pq-card pq-win'><div class='pq-conf'>{conf}</div>"
            f"<h2>✅ Level Complete!</h2><p>{msg}</p>"
            f"<p>{'⭐ +' + str(gained) + ' XP' if gained else 'Replayed — no new XP'} "
            f"&nbsp;•&nbsp; Rank: <b>{self._rank()}</b>"
            + (f"<br>🏅 New badge: <b>{lv['badge']}</b>" if first and lv.get('badge') else "")
            + "</p></div>"))

        nxt = W.Button(description="➡  NEXT LEVEL", button_style="primary")
        nxt.add_class("pq-btn")
        nxt.on_click(self._on_next)
        display(nxt)

    def _on_next(self, b):
        if self.state["level"] < len(self.levels):
            self.state["level"] += 1
            self._save()
        self._render()

    def _on_skip(self, b):
        self._on_next(b)

    def _on_hint(self, b):
        lv = self.levels[self.state["level"]]
        hints = lv.get("hints", [])
        with self._out:
            clear_output(wait=True)
            if not hints:
                display(HTML("<div class='pq-card pq-hint'>No hints for this one — "
                             "you've got it! 💪</div>"))
                return
            h = hints[min(self.hint_i, len(hints) - 1)]
            display(HTML(f"<div class='pq-card pq-hint'>💡 <b>Hint "
                         f"{min(self.hint_i+1, len(hints))}:</b> {h}</div>"))
            self.hint_i = min(self.hint_i + 1, len(hints))

    def _on_answer(self, b):
        lv = self.levels[self.state["level"]]
        with self._out:
            clear_output(wait=True)
            if not self.revealed and self.hint_i < 1:
                display(HTML("<div class='pq-card pq-hint'>Try a 💡 Hint first! "
                             "The answer will unlock after a hint.</div>"))
                self.hint_i = 1
                return
            self.revealed = True
            display(HTML(
                "<div class='pq-card pq-ans'><b>👀 One good answer:</b>"
                f"<pre>{html.escape(lv.get('answer','(no answer provided)'))}</pre>"
                "<small>Type it into the code box yourself, then press RUN — "
                "your fingers remember what your eyes forget!</small></div>"))

    # ---------- finale ----------
    def _certificate(self):
        badges = " ".join(self.state["badges"]) or "🏅"
        return (
            f"<div class='pq-card pq-cert'>"
            f"<div class='pq-conf'>🎉✨🎊🌟💫⭐🎉✨🎊🌟</div>"
            f"<h1>🏆 QUEST COMPLETE! 🏆</h1>"
            f"<h2>{html.escape(self.state['player'])}</h2>"
            f"<p>has journeyed through all {len(self.levels)} levels of PythonQuest</p>"
            f"<p class='pq-big'>{self._rank()}</p>"
            f"<p>⭐ {self.state['xp']} XP &nbsp;•&nbsp; Badges: {badges}</p>"
            f"<hr><p>You can now read code, use variables, make decisions, "
            f"loop, store data in lists &amp; dictionaries, and build your own "
            f"functions and programs. Go build something real! 🚀</p>"
            f"<small>Run <code>quest.reset()</code> to play again, or "
            f"<code>quest.map()</code> to see your map.</small></div>")

    # ---------- styling ----------
    def _inject_css(self):
        display(HTML("""
<style>
.pq-card{font-family:'Segoe UI',system-ui,sans-serif;border-radius:18px;
  padding:18px 22px;margin:12px 0;box-shadow:0 6px 18px rgba(0,0,0,.12);
  line-height:1.5;color:#1f2937;}
.pq-head{background:linear-gradient(135deg,#7c3aed,#db2777);color:#fff;}
.pq-head h1{margin:2px 0;font-size:26px;}
.pq-headtop{display:flex;justify-content:space-between;align-items:center;}
.pq-lvl{background:rgba(255,255,255,.25);padding:3px 10px;border-radius:20px;
  font-size:12px;font-weight:700;letter-spacing:1px;}
.pq-world2{opacity:.9;font-weight:600;}
.pq-avatar{font-size:52px;}
.pq-sub{margin-top:8px;font-size:14px;opacity:.95;}
.pq-bar{background:rgba(255,255,255,.3);border-radius:20px;height:20px;
  margin-top:10px;overflow:hidden;}
.pq-fill{background:#fde047;color:#78350f;height:100%;text-align:center;
  font-size:12px;font-weight:700;border-radius:20px;transition:width .4s;}
.pq-story{background:#ecfeff;border-left:6px solid #06b6d4;}
.pq-concept{background:#fffbeb;border-left:6px solid #f59e0b;}
.pq-concept h3{margin:0 0 8px;color:#b45309;}
.pq-concept code,.pq-story code{background:#1f2937;color:#a7f3d0;padding:1px 6px;
  border-radius:6px;font-size:13px;}
.pq-concept pre{background:#1f2937;color:#e5e7eb;padding:12px;border-radius:10px;
  overflow:auto;font-size:13px;}
.pq-task{background:#fef3c7;border-radius:10px;padding:10px 12px;margin-top:10px;}
.pq-label{font-weight:700;margin:6px 0;font-family:'Segoe UI',sans-serif;color:#374151;}
.pq-code textarea{font-family:'Fira Mono','Consolas',monospace!important;
  font-size:14px!important;background:#0f172a!important;color:#e2e8f0!important;
  border-radius:12px!important;padding:12px!important;line-height:1.5!important;}
.pq-btn{margin:6px 6px 6px 0!important;border-radius:10px!important;
  font-weight:700!important;}
.pq-out{background:#0f172a;color:#a7f3d0;border-radius:12px;padding:10px 14px;
  margin:8px 0;font-family:'Segoe UI',sans-serif;}
.pq-out pre{margin:6px 0 0;color:#e2e8f0;white-space:pre-wrap;}
.pq-win{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;text-align:center;}
.pq-win h2{margin:6px 0;}
.pq-conf{font-size:24px;letter-spacing:4px;}
.pq-try{background:#fef2f2;border-left:6px solid #ef4444;}
.pq-err{background:#fef2f2;border-left:6px solid #dc2626;}
.pq-err code{background:#1f2937;color:#fca5a5;padding:2px 6px;border-radius:6px;}
.pq-hint{background:#eff6ff;border-left:6px solid #3b82f6;}
.pq-ans{background:#f5f3ff;border-left:6px solid #8b5cf6;}
.pq-ans pre{background:#1f2937;color:#e5e7eb;padding:12px;border-radius:10px;}
.pq-map .pq-world{font-weight:800;margin:14px 0 6px;color:#7c3aed;font-size:16px;}
.pq-cell{padding:6px 10px;border-radius:8px;margin:3px 0;}
.pq-cell.done{background:#dcfce7;} .pq-cell.now{background:#fef9c3;font-weight:700;}
.pq-cell.open{background:#f1f5f9;} .pq-cell.lock{background:#f8fafc;color:#94a3b8;}
.pq-cert{background:linear-gradient(135deg,#f59e0b,#db2777);color:#fff;text-align:center;}
.pq-cert h1{font-size:34px;margin:6px 0;}
.pq-big{font-size:22px;font-weight:800;background:rgba(255,255,255,.2);
  display:inline-block;padding:6px 16px;border-radius:20px;}
.pq-cert hr{border-color:rgba(255,255,255,.4);}
</style>"""))


class _LoopRunaway(Exception):
    """Raised when a player's code runs too many steps (e.g. an endless loop)."""


import sys as _sys

class _loop_guard:
    """Context manager that stops runaway/infinite loops so Colab never freezes.
    It counts executed lines and bails out after a generous limit."""
    LIMIT = 500_000

    def __enter__(self):
        self.n = 0
        self._prev = _sys.gettrace()
        _sys.settrace(self._trace)
        return self

    def __exit__(self, *exc):
        _sys.settrace(self._prev)
        return False

    def _trace(self, frame, event, arg):
        self.n += 1
        if self.n > self.LIMIT:
            raise _LoopRunaway()
        return self._trace


def _mock_input(queue):
    """A safe stand-in for input() so kids' programs never freeze in a game.
    Returns preset answers one by one and echoes them like a real prompt."""
    q = list(queue) if queue else ["Alex"]
    box = {"i": 0}
    def _fake(prompt=""):
        val = q[box["i"]] if box["i"] < len(q) else q[-1]
        box["i"] += 1
        print(f"{prompt}{val}")
        return val
    return _fake
