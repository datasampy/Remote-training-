# =====================================================================
#  PYTHONQUEST — LEVEL PACK  (27 levels, 7 worlds)
#  Each level teaches one idea and auto-checks the player's code.
#  A checker gets (ws, out):  ws = the code's variables,  out = printed text.
#  Starters are SCAFFOLDS with a TODO — running them as-is fails gently,
#  so kids actually write the key line themselves (that's how they learn).
# =====================================================================
from engine import ok, no, norm, lines

LEVELS = [
# ==================== WORLD 1 : 🚀 BLAST OFF (print & strings) =========
dict(world="🚀 World 1 — Blast Off", emoji="🚀",
     title="Say Hello", xp=20, badge="🗣️ First Words",
     story="Every coder's first spell is <code>print()</code>. It makes the "
           "computer say things out loud on the screen!",
     concept="<p><code>print(\"...\")</code> shows whatever is inside the quotes.</p>"
             "<pre>print(\"Hi there!\")</pre>",
     task="Make the computer print exactly: <code>Hello, World!</code>",
     starter='print("")   # <- type  Hello, World!  between the quotes\n',
     hints=["Use the print function.",
            "Put your words inside \"double quotes\".",
            'Type it exactly: print("Hello, World!")'],
     answer='print("Hello, World!")',
     check=lambda ws, out: ok("You just cast your first spell! 🪄")
        if norm(out) == "hello, world!" else
        no("Print the words <b>Hello, World!</b> exactly (with the comma and !).")),

dict(world="🚀 World 1 — Blast Off", emoji="💬",
     title="Two Lines", xp=20,
     story="Each <code>print()</code> starts a brand new line. Let's introduce "
           "you to the computer!",
     concept="<p>Use <code>print()</code> more than once:</p>"
             "<pre>print(\"Line one\")\nprint(\"Line two\")</pre>",
     task="Print your name on the first line, then print your favourite animal "
          "on the second line (any words are fine — just two separate prints).",
     starter='# Line 1: your name. Line 2: your favourite animal.\n'
             'print("")\nprint("")\n',
     hints=["Write two print() lines, one under the other.",
            "The output should have exactly two lines of text."],
     answer='print("Sam")\nprint("Tiger")',
     check=lambda ws, out: ok("Two lines, two prints. Nice rhythm! 🎵")
        if len(lines(out)) >= 2 else
        no("I need <b>two</b> separate lines of text. Fill in both print() lines.")),

dict(world="🚀 World 1 — Blast Off", emoji="🔤",
     title="Glue Words Together", xp=25, badge="🔗 Word Wizard",
     story="Strings are just text. You can glue two strings with <code>+</code>, "
           "or drop values into a sentence with an <b>f-string</b>.",
     concept="<pre>name = \"Zoe\"\nprint(\"Hi \" + name)        # gluing\n"
             "print(f\"Hi {name}!\")        # f-string (easier!)</pre>",
     task="Make a variable <code>hero</code> with any name, then print "
          "<code>My hero is NAME</code> using an f-string.",
     starter='hero = ""      # <- put a name between the quotes\n'
             'print(f"My hero is {hero}")\n',
     hints=["First line: hero = \"SomeName\"",
            "Second line uses the f-string: print(f\"My hero is {hero}\")",
            "Note the little f right before the opening quote."],
     answer='hero = "Ada"\nprint(f"My hero is {hero}")',
     check=lambda ws, out: ok("f-strings will be your best friend! 💪")
        if "hero" in ws and norm(out).startswith("my hero is")
           and norm(str(ws["hero"])) in norm(out) and str(ws["hero"]).strip() != ""
        else no("Give <code>hero</code> a name and print "
                "<code>My hero is {hero}</code> with an f-string.")),

# ==================== WORLD 2 : 📦 MEMORY BOXES =======================
dict(world="📦 World 2 — Memory Boxes", emoji="📦",
     title="Make a Variable", xp=25,
     story="A variable is a labelled box that remembers a value for later.",
     concept="<pre>age = 10          # a box named age holding 10\n"
             "city = \"Cairo\"    # a box named city holding text</pre>",
     task="Create a variable named <code>score</code> equal to the number "
          "<code>100</code>.",
     starter="score = 0   # <- change 0 to 100\n",
     hints=["Use: score = 100", "No quotes — 100 is a number, not text."],
     answer="score = 100",
     check=lambda ws, out: ok("Box packed and labelled! 📦")
        if ws.get("score") == 100 else
        no("Set <code>score</code> to the number 100 (no quotes).")),

dict(world="📦 World 2 — Memory Boxes", emoji="🧮",
     title="Robot Calculator", xp=30, badge="🧮 Number Ninja",
     story="Python is a super calculator: <code>+ - * /</code>. Let's find the "
           "area of a room.",
     concept="<pre>width = 4\nheight = 5\narea = width * height   # 20</pre>",
     task="Make <code>width = 6</code> and <code>height = 7</code>, then make "
          "<code>area</code> equal to width times height. Print the area.",
     starter="width = 6\nheight = 7\narea = 0   # <- make this width * height\nprint(area)\n",
     hints=["Use * to multiply.", "area = width * height",
            "Then print(area) — it should be 42."],
     answer="width = 6\nheight = 7\narea = width * height\nprint(area)",
     check=lambda ws, out: ok("42 — the answer to everything! 🌌")
        if ws.get("area") == 42 else
        no("Make <code>area = width * height</code>. It should equal 42.")),

dict(world="📦 World 2 — Memory Boxes", emoji="🎤",
     title="Ask the Player", xp=30,
     story="<code>input()</code> asks the person a question and hands back what "
           "they type. (In this game it auto-answers <b>Alex</b> so nothing freezes.)",
     concept="<pre>name = input(\"Your name? \")\nprint(\"Hello \" + name)</pre>",
     task="Store <code>input(\"Name? \")</code> in a variable called "
          "<code>name</code>, then print <code>Welcome NAME!</code> with an f-string.",
     starter='name = ""   # <- use  input("Name? ")  instead of ""\n'
             'print(f"Welcome {name}!")\n',
     inputs=["Alex"],
     hints=["name = input(\"Name? \")",
            "print(f\"Welcome {name}!\")"],
     answer='name = input("Name? ")\nprint(f"Welcome {name}!")',
     check=lambda ws, out: ok("You just made an interactive program! 🎮")
        if ws.get("name") == "Alex" and "welcome alex" in norm(out) else
        no("Save <code>input(\"Name? \")</code> into <code>name</code>, then print "
           "<code>Welcome {name}!</code>.")),

dict(world="📦 World 2 — Memory Boxes", emoji="🔢",
     title="Words vs Numbers", xp=30,
     story="Typed answers arrive as <b>text</b>. To do maths, turn text into a "
           "number with <code>int()</code>.",
     concept="<pre>age_text = \"10\"\nage = int(age_text)   # now a number\n"
             "print(age + 5)        # 15</pre>",
     task="You have <code>age = int(\"12\")</code>. Make "
          "<code>next_year</code> equal to age + 1 and print it.",
     starter='age = int("12")\nnext_year = age   # <- add 1 to age\nprint(next_year)\n',
     hints=["int(\"12\") turns the text \"12\" into the number 12.",
            "next_year = age + 1 → should be 13."],
     answer='age = int("12")\nnext_year = age + 1\nprint(next_year)',
     check=lambda ws, out: ok("You tamed types! 🐉")
        if ws.get("next_year") == 13 else
        no("Make <code>next_year = age + 1</code> — it should be 13.")),

# ==================== WORLD 3 : 🔀 CROSSROADS (decisions) =============
dict(world="🔀 World 3 — Crossroads", emoji="⚖️",
     title="True or False?", xp=30, badge="⚖️ Logic Learner",
     story="Comparisons give a <b>boolean</b>: either <code>True</code> or "
           "<code>False</code>. <code>&gt; &lt; == != &gt;= &lt;=</code>",
     concept="<pre>print(10 > 3)     # True\nprint(5 == 6)     # False\n"
             "is_big = 100 > 50 # stores True</pre>",
     task="Make a variable <code>is_adult</code> that ends up <code>True</code> "
          "by writing a comparison such as <code>18 &gt;= 18</code>.",
     starter="is_adult = False   # <- replace with a comparison that is True, e.g. 18 >= 18\nprint(is_adult)\n",
     hints=["Use the >= comparison.", "is_adult = 18 >= 18 gives True."],
     answer="is_adult = 18 >= 18\nprint(is_adult)",
     check=lambda ws, out: ok("True dat! ✅")
        if ws.get("is_adult") is True else
        no("Make <code>is_adult</code> a comparison that results in True.")),

dict(world="🔀 World 3 — Crossroads", emoji="🚪",
     title="The Secret Door", xp=35,
     story="<code>if</code> runs code only when something is true. "
           "<code>else</code> runs when it isn't. Watch the indentation!",
     concept="<pre>password = \"open\"\nif password == \"open\":\n"
             "    print(\"Access granted\")\nelse:\n"
             "    print(\"Denied\")</pre>",
     task="Set <code>password = \"open\"</code>. If it equals <code>\"open\"</code>, "
          "print <code>Access granted</code>, otherwise print <code>Denied</code>.",
     starter='password = "open"\nif password == "open":\n    print("")   # <- print Access granted\nelse:\n    print("")   # <- print Denied\n',
     hints=["Line ends with a colon :  then indent the next line 4 spaces.",
            "Fill the first print with \"Access granted\"."],
     answer='password = "open"\nif password == "open":\n    print("Access granted")\nelse:\n    print("Denied")',
     check=lambda ws, out: ok("You unlocked the door! 🗝️")
        if "access granted" in norm(out) and "denied" not in norm(out) else
        no("It should print <b>Access granted</b> (and not Denied).")),

dict(world="🔀 World 3 — Crossroads", emoji="🎓",
     title="Grade Machine", xp=40, badge="🎯 Decision Maker",
     story="<code>elif</code> lets you check many cases in order — like a "
           "grading machine.",
     concept="<pre>if score >= 90:\n    grade = \"A\"\nelif score >= 70:\n"
             "    grade = \"B\"\nelse:\n    grade = \"C\"</pre>",
     task="Given <code>score = 85</code>, set <code>grade</code> to \"A\" if "
          "score&gt;=90, \"B\" if score&gt;=70, else \"C\". (It should become \"B\".)",
     starter='score = 85\nif score >= 90:\n    grade = "A"\nelif score >= 70:\n    grade = ""   # <- which grade goes here?\nelse:\n    grade = "C"\nprint(grade)\n',
     hints=["Order matters — check the biggest number first.",
            "85 is not >=90 but is >=70, so grade becomes \"B\"."],
     answer='score = 85\nif score >= 90:\n    grade = "A"\nelif score >= 70:\n    grade = "B"\nelse:\n    grade = "C"\nprint(grade)',
     check=lambda ws, out: ok("Grade-A logic! 🎓")
        if ws.get("grade") == "B" else
        no("With score 85 the grade should be <b>\"B\"</b>. Fill in the elif branch.")),

dict(world="🔀 World 3 — Crossroads", emoji="🎢",
     title="Ride Rules", xp=40,
     story="Combine conditions with <code>and</code> (both), <code>or</code> "
           "(either), <code>not</code> (flip).",
     concept="<pre>tall = True\nbrave = False\nprint(tall and brave)  # False\n"
             "print(tall or brave)   # True</pre>",
     task="Given <code>height = 140</code> and <code>has_ticket = True</code>, make "
          "<code>can_ride</code> True only if height &gt;= 120 <b>and</b> has_ticket.",
     starter="height = 140\nhas_ticket = True\ncan_ride = False   # <- use: height >= 120 and has_ticket\nprint(can_ride)\n",
     hints=["Use the word 'and' between the two conditions.",
            "can_ride = height >= 120 and has_ticket"],
     answer="height = 140\nhas_ticket = True\ncan_ride = height >= 120 and has_ticket\nprint(can_ride)",
     check=lambda ws, out: ok("Enjoy the ride! 🎢")
        if ws.get("can_ride") is True else
        no("Use <code>and</code> to combine both rules — result should be True.")),

# ==================== WORLD 4 : 🔁 LOOP LAND =========================
dict(world="🔁 World 4 — Loop Land", emoji="🔁",
     title="Count to Five", xp=35, badge="🔁 Loop Rookie",
     story="A <code>for</code> loop repeats code. <code>range(1, 6)</code> gives "
           "the numbers 1,2,3,4,5.",
     concept="<pre>for n in range(1, 6):\n    print(n)</pre>",
     task="Use a for loop with <code>range(1, 6)</code> to print the numbers "
          "1 to 5, each on its own line.",
     starter="for n in range(1, 1):   # <- fix the second number so you get 1..5\n    print(n)\n",
     hints=["range(1, 6) stops BEFORE 6, so it gives 1..5.",
            "Change the second number to 6."],
     answer="for n in range(1, 6):\n    print(n)",
     check=lambda ws, out: ok("Round and round! 🔁")
        if lines(out) == ["1", "2", "3", "4", "5"] else
        no("Print 1,2,3,4,5 each on its own line using range(1, 6).")),

dict(world="🔁 World 4 — Loop Land", emoji="👫",
     title="Greet the Squad", xp=40,
     story="You can loop over a <b>list</b> of items directly — no numbers needed.",
     concept="<pre>friends = [\"Mia\", \"Leo\"]\nfor f in friends:\n"
             "    print(\"Hi \" + f)</pre>",
     task="Loop over <code>friends = [\"Mia\", \"Leo\", \"Sam\"]</code> and print "
          "<code>Hi NAME</code> for each one.",
     starter='friends = ["Mia", "Leo", "Sam"]\nfor f in friends:\n    print("")   # <- print  Hi  and the name f\n',
     hints=["Inside the loop: print(\"Hi \" + f)",
            "Or use an f-string: print(f\"Hi {f}\")"],
     answer='friends = ["Mia", "Leo", "Sam"]\nfor f in friends:\n    print("Hi " + f)',
     check=lambda ws, out: ok("The whole squad says hi! 👋")
        if all(f"hi {n}" in norm(out) for n in ["mia", "leo", "sam"]) else
        no("Loop the list and print <b>Hi Mia</b>, <b>Hi Leo</b>, <b>Hi Sam</b>.")),

dict(world="🔁 World 4 — Loop Land", emoji="➕",
     title="Add Them Up", xp=45, badge="🧠 Loop Thinker",
     story="A loop can build up an answer step by step. Start a total at 0 and "
           "add to it each time.",
     concept="<pre>total = 0\nfor n in [10, 20, 30]:\n    total = total + n\n"
             "print(total)   # 60</pre>",
     task="Start <code>total = 0</code>, then loop over "
          "<code>[5, 10, 15, 20]</code> adding each number to total. Print total "
          "(it should be 50).",
     starter="total = 0\nfor n in [5, 10, 15, 20]:\n    total = total   # <- add n to total here\nprint(total)\n",
     hints=["Make total = 0 BEFORE the loop.",
            "Inside: total = total + n (or total += n)."],
     answer="total = 0\nfor n in [5, 10, 15, 20]:\n    total += n\nprint(total)",
     check=lambda ws, out: ok("You're an adding machine! 🧮")
        if ws.get("total") == 50 else
        no("Sum the list into <code>total</code> — it should be 50.")),

dict(world="🔁 World 4 — Loop Land", emoji="🚀",
     title="Countdown!", xp=45,
     story="A <code>while</code> loop repeats <b>as long as</b> something is "
           "true. Perfect for a rocket countdown.",
     concept="<pre>n = 3\nwhile n > 0:\n    print(n)\n    n = n - 1\n"
             "print(\"Go!\")</pre>",
     task="Start <code>n = 5</code>. While n &gt; 0, print n then subtract 1. "
          "After the loop, print <code>Blast off!</code>.",
     starter='n = 5\nwhile n > 0:\n    print(n)\n    # <- add a line here that lowers n by 1, or the loop never stops!\nprint("Blast off!")\n',
     hints=["Add  n = n - 1  inside the loop, or it runs forever!",
            "Print \"Blast off!\" AFTER the loop (not indented)."],
     answer='n = 5\nwhile n > 0:\n    print(n)\n    n = n - 1\nprint("Blast off!")',
     check=lambda ws, out: ok("🚀 Liftoff!")
        if lines(out)[:5] == ["5","4","3","2","1"] and "blast off" in norm(out) else
        no("Count 5,4,3,2,1 then print <b>Blast off!</b>. Remember to lower n each loop.")),

# ==================== WORLD 5 : 🗃️ TREASURE CHESTS ===================
dict(world="🗃️ World 5 — Treasure Chests", emoji="🗃️",
     title="Pack a List", xp=40, badge="📋 List Keeper",
     story="A <b>list</b> holds many things in order. Counting starts at <b>0</b>!",
     concept="<pre>fruits = [\"apple\", \"kiwi\", \"mango\"]\n"
             "print(fruits[0])   # apple\nprint(fruits[2])   # mango</pre>",
     task="Make a list <code>colors</code> with \"red\", \"green\", \"blue\". "
          "Print the <b>first</b> colour using <code>colors[0]</code>.",
     starter='colors = ["red", "green", "blue"]\nprint(colors[1])   # <- which index is the FIRST item?\n',
     hints=["The first item is colors[0], not colors[1].",
            "Lists start counting at 0."],
     answer='colors = ["red", "green", "blue"]\nprint(colors[0])',
     check=lambda ws, out: ok("Zero is the start — you got it! 0️⃣")
        if isinstance(ws.get("colors"), list) and len(ws["colors"]) == 3
           and "red" in norm(out) and "green" not in norm(out) else
        no("Print <code>colors[0]</code> — the FIRST colour, which is red.")),

dict(world="🗃️ World 5 — Treasure Chests", emoji="➕",
     title="Grow the List", xp=45,
     story="Lists can grow with <code>.append()</code>, and "
           "<code>len()</code> counts how many items are inside.",
     concept="<pre>bag = [\"gold\"]\nbag.append(\"gem\")\nprint(len(bag))  # 2</pre>",
     task="Start <code>bag = [\"gold\"]</code>, append <code>\"gem\"</code> and "
          "<code>\"key\"</code>, then print <code>len(bag)</code> (should be 3).",
     starter='bag = ["gold"]\n# <- add two lines: bag.append("gem")  and  bag.append("key")\nprint(len(bag))\n',
     hints=["Call bag.append(\"gem\") then bag.append(\"key\") on their own lines.",
            "len(bag) counts the items — you want 3."],
     answer='bag = ["gold"]\nbag.append("gem")\nbag.append("key")\nprint(len(bag))',
     check=lambda ws, out: ok("Treasure collected! 💎")
        if isinstance(ws.get("bag"), list) and len(ws["bag"]) == 3 else
        no("Append two items so the bag has 3, then print len(bag).")),

dict(world="🗃️ World 5 — Treasure Chests", emoji="🔢",
     title="Square Factory", xp=50, badge="🏭 Data Builder",
     story="Loop + list = a factory. Build a new list of squared numbers.",
     concept="<pre>squares = []\nfor n in [1, 2, 3]:\n    squares.append(n * n)\n"
             "print(squares)   # [1, 4, 9]</pre>",
     task="Build a list <code>squares</code> of the squares of 1,2,3,4,5. "
          "The result should be <code>[1, 4, 9, 16, 25]</code>.",
     starter="squares = []\nfor n in range(1, 6):\n    squares.append(n)   # <- append the SQUARE of n (n * n)\nprint(squares)\n",
     hints=["Start with an empty list: squares = []",
            "Inside the loop: squares.append(n * n)"],
     answer="squares = []\nfor n in range(1, 6):\n    squares.append(n * n)\nprint(squares)",
     check=lambda ws, out: ok("Factory running at full power! 🏭")
        if ws.get("squares") == [1, 4, 9, 16, 25] else
        no("Build [1, 4, 9, 16, 25] by appending n*n in a loop.")),

dict(world="🗃️ World 5 — Treasure Chests", emoji="🗂️",
     title="The Name Tag", xp=50,
     story="A <b>dictionary</b> stores pairs: a <b>key</b> and its <b>value</b>. "
           "Great for describing one thing.",
     concept="<pre>hero = {\"name\": \"Zed\", \"hp\": 100}\n"
             "print(hero[\"name\"])   # Zed</pre>",
     task="Make a dictionary <code>pet</code> with keys <code>\"name\"</code> "
          "(any name) and <code>\"legs\"</code> = 4. Print the pet's name using "
          "<code>pet[\"name\"]</code>.",
     starter='pet = {"name": "", "legs": 0}   # <- add a name, and set legs to 4\nprint(pet["name"])\n',
     hints=["Fill in a name and change legs to 4.",
            "Access a value with pet[\"name\"]."],
     answer='pet = {"name": "Rex", "legs": 4}\nprint(pet["name"])',
     check=lambda ws, out: ok("Key + value = power! 🗝️")
        if isinstance(ws.get("pet"), dict) and ws["pet"].get("legs") == 4
           and str(ws["pet"].get("name", "")).strip() != ""
           and norm(str(ws["pet"]["name"])) in norm(out) else
        no("Give <code>pet</code> a name and legs=4, then print its name.")),

dict(world="🗃️ World 5 — Treasure Chests", emoji="📖",
     title="Read the Scores", xp=55, badge="🗂️ Dict Master",
     story="Loop over a dictionary with <code>.items()</code> to see every key "
           "and value.",
     concept="<pre>scores = {\"Mia\": 8, \"Leo\": 5}\n"
             "for name, pts in scores.items():\n    print(name, pts)</pre>",
     task="Given <code>scores = {\"Mia\": 8, \"Leo\": 5}</code>, loop with "
          "<code>.items()</code> and print <code>NAME scored PTS</code> for each.",
     starter='scores = {"Mia": 8, "Leo": 5}\nfor name, pts in scores.items():\n    print("")   # <- print   NAME scored PTS   using an f-string\n',
     hints=["for name, pts in scores.items():",
            "print(f\"{name} scored {pts}\")"],
     answer='scores = {"Mia": 8, "Leo": 5}\nfor name, pts in scores.items():\n    print(f"{name} scored {pts}")',
     check=lambda ws, out: ok("You read the whole scoreboard! 📊")
        if "mia scored 8" in norm(out) and "leo scored 5" in norm(out) else
        no("Loop with .items() and print <b>Mia scored 8</b> and <b>Leo scored 5</b>.")),

# ==================== WORLD 6 : ⚙️ MACHINE SHOP (functions) ==========
dict(world="⚙️ World 6 — Machine Shop", emoji="⚙️",
     title="Build a Machine", xp=45, badge="⚙️ Machine Maker",
     story="A <b>function</b> is a reusable machine you build once and use "
           "again and again with <code>def</code>.",
     concept="<pre>def greet(name):\n    print(\"Hello \" + name)\n\n"
             "greet(\"Mia\")   # Hello Mia</pre>",
     task="Define a function <code>greet(name)</code> that prints "
          "<code>Hello NAME</code>. Then call <code>greet(\"World\")</code>.",
     starter='def greet(name):\n    print("")   # <- print  Hello  and the name\n\ngreet("World")\n',
     hints=["Inside the function: print(\"Hello \" + name)",
            "The call greet(\"World\") should print Hello World."],
     answer='def greet(name):\n    print("Hello " + name)\n\ngreet("World")',
     check=lambda ws, out: ok("Your first machine works! ⚙️")
        if callable(ws.get("greet")) and "hello world" in norm(out) else
        no("Define <code>greet(name)</code> that prints Hello NAME, then call it.")),

dict(world="⚙️ World 6 — Machine Shop", emoji="↩️",
     title="Send Back an Answer", xp=50,
     story="<code>return</code> hands a value <b>back</b> so you can store or "
           "reuse it — much more powerful than just printing.",
     concept="<pre>def add(a, b):\n    return a + b\n\n"
             "total = add(2, 3)   # total is 5</pre>",
     task="Write a function <code>add(a, b)</code> that <b>returns</b> a + b. "
          "(The game will test it with different numbers.)",
     starter="def add(a, b):\n    return 0   # <- return a + b instead of 0\n",
     hints=["Use return, not print.", "return a + b"],
     answer="def add(a, b):\n    return a + b",
     check=lambda ws, out: ok("Machines that answer back — pro level! 🏆")
        if callable(ws.get("add")) and ws["add"](2, 3) == 5
           and ws["add"](10, 20) == 30 else
        no("Make <code>add(a, b)</code> <b>return</b> a + b (use return, not print).")),

dict(world="⚙️ World 6 — Machine Shop", emoji="⚖️",
     title="The Even Detector", xp=55, badge="🔬 Function Scientist",
     story="Functions can make decisions and return True/False. "
           "<code>%</code> gives the remainder — even numbers leave remainder 0.",
     concept="<pre>def is_even(n):\n    return n % 2 == 0\n\n"
             "print(is_even(4))   # True</pre>",
     task="Write <code>is_even(n)</code> that returns <code>True</code> when n is "
          "even, else <code>False</code>. (Use <code>n % 2 == 0</code>.)",
     starter="def is_even(n):\n    return False   # <- return  n % 2 == 0\n",
     hints=["n % 2 is the remainder when dividing by 2.",
            "return n % 2 == 0"],
     answer="def is_even(n):\n    return n % 2 == 0",
     check=lambda ws, out: ok("Detector calibrated! 🔬")
        if callable(ws.get("is_even")) and ws["is_even"](4) is True
           and ws["is_even"](7) is False else
        no("Return <code>n % 2 == 0</code> so even→True, odd→False.")),

dict(world="⚙️ World 6 — Machine Shop", emoji="🔤",
     title="Vowel Counter", xp=60, badge="🧙 Code Combiner",
     story="Time to combine EVERYTHING: a function, a loop, an if, and a "
           "counter. Count the vowels in a word.",
     concept="<pre>def count_vowels(word):\n    count = 0\n"
             "    for letter in word:\n        if letter in \"aeiou\":\n"
             "            count = count + 1\n    return count</pre>",
     task="Write <code>count_vowels(word)</code> returning how many vowels "
          "(a, e, i, o, u) are in the lowercase word. E.g. "
          "<code>count_vowels(\"banana\")</code> → 3.",
     starter='def count_vowels(word):\n    count = 0\n    for letter in word:\n        # <- if the letter is a vowel, add 1 to count\n        pass\n    return count\n',
     hints=["Loop each letter; use  if letter in \"aeiou\":  then count += 1.",
            "Delete the 'pass' line once you add your if.",
            "Return count at the end (not indented inside the loop)."],
     answer='def count_vowels(word):\n    count = 0\n    for letter in word:\n        if letter in "aeiou":\n            count += 1\n    return count',
     check=lambda ws, out: ok("You combined 4 ideas into 1 machine. Wizard! 🧙")
        if callable(ws.get("count_vowels")) and ws["count_vowels"]("banana") == 3
           and ws["count_vowels"]("sky") == 0
           and ws["count_vowels"]("aeiou") == 5 else
        no("Count letters that are in \"aeiou\". \"banana\"→3, \"sky\"→0.")),

# ==================== WORLD 7 : 🏆 BOSS BUILD (real project) =========
dict(world="🏆 World 7 — Boss Build: Quiz Bot", emoji="🧩",
     title="Design the Quiz", xp=60, badge="🏗️ Project Architect",
     story="For your final quest you'll build a real <b>Quiz Bot</b> game — "
           "piece by piece. First, design the questions as data.",
     concept="A list of dictionaries is perfect for a quiz:"
             "<pre>quiz = [\n  {\"q\": \"2+2?\", \"a\": \"4\"},\n"
             "  {\"q\": \"Sky colour?\", \"a\": \"blue\"},\n]</pre>",
     task="Create a list called <code>quiz</code> with <b>at least 2</b> "
          "dictionaries, each having a <code>\"q\"</code> (question) and "
          "<code>\"a\"</code> (answer) key.",
     starter='quiz = [\n    {"q": "What is 2 + 2?", "a": "4"},\n    # <- add one more question dict here, with its own "q" and "a"\n]\nprint(len(quiz), "questions ready!")\n',
     hints=["Copy the first line and change the question and answer.",
            "Each dict needs a \"q\" and an \"a\" key. You need 2 or more."],
     answer='quiz = [\n    {"q": "What is 2 + 2?", "a": "4"},\n    {"q": "What colour is the sky?", "a": "blue"},\n]\nprint(len(quiz), "questions ready!")',
     check=lambda ws, out: ok("Your quiz data is ready to power the game! 🏗️")
        if isinstance(ws.get("quiz"), list) and len(ws["quiz"]) >= 2
           and all(isinstance(q, dict) and "q" in q and "a" in q for q in ws["quiz"])
        else no("Make a <code>quiz</code> list of 2+ dicts, each with \"q\" and \"a\".")),

dict(world="🏆 World 7 — Boss Build: Quiz Bot", emoji="✅",
     title="The Answer Checker", xp=65,
     story="Now build the brain: a function that checks one answer and returns "
           "<code>True</code> or <code>False</code>. Ignore capital letters and "
           "spaces so players aren't punished for typing style.",
     concept="<pre>def check(guess, correct):\n"
             "    return guess.strip().lower() == correct.strip().lower()</pre>",
     task="Write <code>check(guess, correct)</code> that returns True when the "
          "two answers match after <code>.strip().lower()</code>. "
          "<code>check(\" Blue \", \"blue\")</code> must be True.",
     starter="def check(guess, correct):\n    return False   # <- compare guess and correct after .strip().lower()\n",
     hints=[".strip() removes spaces, .lower() makes lowercase.",
            "return guess.strip().lower() == correct.strip().lower()"],
     answer="def check(guess, correct):\n    return guess.strip().lower() == correct.strip().lower()",
     check=lambda ws, out: ok("Fair and smart — great judging! ⚖️")
        if callable(ws.get("check")) and ws["check"](" Blue ", "blue") is True
           and ws["check"]("cat", "dog") is False else
        no("Return True when guess matches correct after .strip().lower().")),

dict(world="🏆 World 7 — Boss Build: Quiz Bot", emoji="🏆",
     title="Run the Whole Game!", xp=120, badge="🏆 Quiz Bot Champion",
     story="THE FINAL BOSS! Put it all together: loop through the quiz, ask "
           "each question, keep <b>score</b>, and give a final result. You've "
           "learned every piece — now assemble the machine! 🚀",
     concept="Use your <code>quiz</code> data and everything you know: a loop, "
             "<code>input()</code>, an <code>if</code>, a counter, and an "
             "f-string.<pre>score = 0\nfor item in quiz:\n"
             "    guess = input(item[\"q\"] + \" \")\n"
             "    if guess.strip().lower() == item[\"a\"].strip().lower():\n"
             "        score += 1\nprint(f\"You scored {score}/{len(quiz)}\")</pre>"
             "<i>(The game auto-answers each question so it runs instantly.)</i>",
     task="Using the same <code>quiz</code> from before, loop through it, ask "
          "each <code>item[\"q\"]</code> with input(), add 1 to <code>score</code> "
          "for each correct answer, and finally print "
          "<code>You scored SCORE/TOTAL</code>. Store the number in "
          "<code>score</code>.",
     starter='quiz = [\n    {"q": "What is 2 + 2?", "a": "4"},\n    {"q": "What colour is the sky?", "a": "blue"},\n]\n\nscore = 0\nfor item in quiz:\n    guess = input(item["q"] + " ")\n    # <- if the cleaned guess matches item["a"], add 1 to score\n\nprint(f"You scored {score}/{len(quiz)}")\n',
     inputs=["4", "blue", "4", "blue", "4", "blue"],
     hints=["Inside the loop compare guess.strip().lower() with item[\"a\"].strip().lower().",
            "When they match:  score += 1",
            "The final print is already written for you."],
     answer='quiz = [\n    {"q": "What is 2 + 2?", "a": "4"},\n    {"q": "What colour is the sky?", "a": "blue"},\n]\nscore = 0\nfor item in quiz:\n    guess = input(item["q"] + " ")\n    if guess.strip().lower() == item["a"].strip().lower():\n        score += 1\nprint(f"You scored {score}/{len(quiz)}")',
     check=lambda ws, out: ok("🏆 YOU BUILT A REAL GAME! Legendary!")
        if isinstance(ws.get("quiz"), list) and ws.get("score") == len(ws["quiz"])
           and "you scored" in norm(out) and f"/{len(ws['quiz'])}" in out else
        no("Loop the quiz, count correct answers into <code>score</code>, and print "
           "<code>You scored score/total</code>. (The auto-player answers correctly, "
           "so score should equal the number of questions.)")),
]
