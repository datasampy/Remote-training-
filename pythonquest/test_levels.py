"""Self-test that mirrors the engine's real run model:
  - every level's ANSWER must PASS its checker
  - every scaffold STARTER must NOT pass (kids must write the key line)
  - runaway loops are caught by the loop guard (nothing freezes)
Runs headless, no ipywidgets needed."""
import io, contextlib, sys
from engine import _mock_input, _loop_guard, _LoopRunaway
from levels import LEVELS

def run(code, inputs):
    ws = {"input": _mock_input(inputs or [])}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), _loop_guard():
            exec(code, ws)
    except _LoopRunaway:
        return ws, buf.getvalue(), "LOOP_RUNAWAY"
    except Exception as e:
        return ws, buf.getvalue(), f"ERROR:{type(e).__name__}"
    return ws, buf.getvalue(), None

fails = 0
for i, lv in enumerate(LEVELS):
    for key in ("world", "title", "story", "concept", "task", "check",
                "answer", "starter", "hints"):
        assert key in lv, f"L{i+1} missing {key}"

    # 1) ANSWER must pass
    ws, out, err = run(lv["answer"], lv.get("inputs", []))
    if err:
        ans_pass, msg = False, f"answer raised {err}"
    else:
        try:
            ans_pass, msg = lv["check"](ws, out)
        except Exception as e:
            ans_pass, msg = False, f"checker raised {e!r}"

    # 2) STARTER should NOT pass (proves the scaffold has a real TODO)
    sws, sout, serr = run(lv["starter"], lv.get("inputs", []))
    if serr in ("LOOP_RUNAWAY",) or (serr and serr.startswith("ERROR")):
        starter_pass = False          # errors/runaways clearly aren't a pass
    else:
        try:
            starter_pass, _ = lv["check"](sws, sout)
        except Exception:
            starter_pass = False

    problems = []
    if not ans_pass:
        problems.append(f"ANSWER FAILS ({msg})")
    if starter_pass:
        problems.append("STARTER already passes (no real TODO!)")

    status = "ok " if not problems else "!! "
    if problems:
        fails += 1
    note = f"starter={serr or 'ran'}"
    print(f"{status}L{i+1:>2} {lv['title']:<22} | {note:<16} | "
          + ("; ".join(problems) if problems else msg[:40]))

print("\n" + ("ALL CHECKS PASS ✅" if fails == 0 else f"{fails} LEVEL(S) HAVE ISSUES ❌"))
sys.exit(1 if fails else 0)
