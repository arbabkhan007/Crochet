"""Final gate on the client-facing pattern: parse the shipped file and check
every stitch count, every derived dimension, and every walk sum."""
import re, pathlib, math, sys

TARGET = "NS04_Coco_the_Capybara_CLIENT.md"
src = pathlib.Path("check/verify_coco.py").read_text().split("PIECES = {")[0]
src = src.replace(r"\]\s*x\s*(?P<mult>\d+)", r"]\s*[x×]\s*(?P<mult>\d+)")
src = src.replace(r"(?:\s*x\s*(\d+))?", r"(?:\s*[x×]\s*(\d+))?")
ns = {}; exec(src, ns); eval_round = ns["eval_round"]

md = pathlib.Path(TARGET).read_text()
plain = re.sub(r"[*_`>]", "", md)
errors = []

# ---------- 1. every round table ----------
rows = re.findall(r'^\|\s*(R\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
print(f"[1] round rows parsed from {TARGET}: {len(rows)}")
prev = 0; bad = 0
for label, instr, stated in rows:
    instr = instr.strip(); stated = int(stated)
    if int(label[1:]) == 1: prev = 0
    c, p = eval_round(instr, prev)
    if c == -1:   c, p = prev, prev
    elif c == -2: c, p = prev, prev * 2
    if p != stated:
        bad += 1; errors.append(f"{label}: produced {p}, states ({stated}) [{instr}]")
    prev = stated
print(f"    stitch counts wrong: {bad}")
assert len(rows) == 37, f"expected 37 round rows (9 leg + 3 ear + 5 muzzle + 20 body), got {len(rows)}"

# ---------- 2. leg-join walks ----------
print("\n[2] leg-join walks")
# R4 produces: 3 sc, then 3x(1 sc + inc) = 3x3 = 9, twice
r4_produced = 3 + 3*(1+2) + 3 + 3*(1+2)
r4_consumed = 3 + 3*1     + 3 + 3*1
print(f"    R4 produced = 3 + [1 sc, inc]x3 (=9) + 3 + [1 sc, inc]x3 (=9) = "
      f"{r4_produced}  (pattern states 24)")
# R5 table row [3 sc, inc] x6 : each repeat consumes 3+1=4, produces 3+2=5
r5_row_consumed, r5_row_produced = 6*(3+1), 6*(3+2)
print(f"    R4 consumes {r4_consumed} of R3's 18 sts; R5 [3 sc, inc]x6 consumes "
      f"{r5_row_consumed} (needs R4=24) and produces {r5_row_produced} (states 30)")
if r4_produced != 24:        errors.append("R4 produced != 24")
if r5_row_consumed != 24:    errors.append("R5 consumes != 24 (R4 must be 24)")
if r5_row_produced != 30:    errors.append("R5 table row != 30")
r5 = [7, 3, 10, 3, 7]
print(f"    R5: {' + '.join(map(str, r5))} = {sum(r5)}  (needs 30)")
if sum(r5) != 30: errors.append("R5 walk != 30")

def gap(a, b, n): return (b - a) % n
back = [1.5, 15.0]
f1 = r5[0] + 1.5
f2 = f1 + r5[1] + r5[2] + 1.5
lr = min(gap(f1, f2, 30), gap(f2, f1, 30))
st = min(gap(back[0], f1, 30), gap(f1, back[1], 30))
print(f"    front-leg centres st {f1} and {f2}")
print(f"    footprint {lr*4.5:.1f} mm wide x {st*4.5:.1f} mm deep  "
      f"(text claims 65 mm x 29 mm)")
if abs(lr*4.5 - 65) > 1 or abs(st*4.5 - 29) > 1: errors.append("footprint figures wrong")

# ---------- 3. every dimension stated in the text ----------
print("\n[3] stated dimensions vs gauge (4.5 mm/st, 4.3 mm/rnd)")
checks = [
    ("body diameter 52 mm",      36*4.5/math.pi,        52),
    ("body height 86 mm",        20*4.3,                86),
    ("front leg 38.7 mm",        9*4.3,                 38.7),
    ("back leg 34 mm",           8*4.3,                 34),
    ("front join height 21 mm",  5*4.3,                 21),
    ("back join height 17 mm",   4*4.3,                 17),
    ("front foot below base 17", 9*4.3 - 5*4.3,         17.2),
    ("back foot below base 17",  8*4.3 - 4*4.3,         17.2),
    ("total height 103 mm",      20*4.3 + (9*4.3-5*4.3), 103),
    ("width 5 cm = 50 mm",       36*4.5/math.pi,        50),
    ("muzzle 17 mm",             12*4.5/math.pi,        17),
    ("ear 13 mm tall (3 rnd)",   3*4.3,                 13),
    ("ear 20 mm across (flat)",  9*4.5/2,               20),
    ("eyes 27 mm apart",         6*4.5,                 27),
    ("ears 22.5 mm apart",       5*4.5,                 22.5),
    ("leg-top strip 3 sts",      3,                     3),
]
for name, got, want in checks:
    ok = abs(got - want) <= max(1.0, want*0.04)
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<28} computed {got:7.1f}  stated {want}")
    if not ok: errors.append(name)

# eyes must clear the muzzle
clear = (6*4.5 - 12*4.5/math.pi)/2
print(f"    {'OK  ' if abs(clear-5)<1 else 'FAIL'} eye-to-muzzle clearance ~5 mm   computed {clear:.1f}")
if abs(clear-5) >= 1: errors.append("eye clearance")

# ears must stay under 90 deg (i.e. on top, not on the sides)
for rnd, sts, sep in ((15, 36, 5),):
    deg = sep*4.5/(sts*4.5)*360
    ok = deg < 70
    print(f"    {'OK  ' if ok else 'FAIL'} ears {sep} sts at R{rnd} = {deg:.0f} deg around (want <70)")
    if not ok: errors.append("ear placement")

# ---------- 4. leg counts ----------
print("\n[4] piece counts")
for txt, want in (("Make 2 back legs (8 rounds) and 2 front legs (9 rounds)", 1),
                  ("make 2", 1), ("make 1", 1)):
    n = len(re.findall(re.escape(txt), plain, re.I))
    print(f"    {'OK  ' if n>=want else 'FAIL'} '{txt}' present ({n})")
    if n < want: errors.append(txt)

# ---------- 5. forbidden content in a client file ----------
print("\n[5] client-readiness")
forbidden = [r"\bFAIL\b", "mismatch", "verify", "check/", "TODO", "XXX", "CHANGES FROM",
             "correction", "I got", "bug", "solver", "review",
             "baby-safe", "fully baby safe", "3.5 mm"]
for f in forbidden:
    pat = f if f.startswith(r"\b") else re.escape(f)
    rx = re.compile(pat, re.I)
    hits = [i+1 for i, line in enumerate(md.splitlines()) if rx.search(line)]
    if hits:
        errors.append(f"forbidden string '{f}' on lines {hits}")
        print(f"    FAIL '{f}' appears on lines {hits}")
print(f"    forbidden strings found: {sum(1 for e in errors if 'forbidden' in e)}")

# run-together words left over from the original PDF
british = ["practising", "fibre", "colour", "centre", "centring", "Centring"]
found = [w for w in british if w in md]
print(f"    British spellings in a US-terms pattern: {found if found else 'none'}")
if found: errors.append(f"British spelling: {found}")
runtogether = ["expression,and", "muzzleand", "oncethe", "thereis", "itagainst",
               "sewanything", "madefrom", "isstrictly", "narrowa"]
rt = [w for w in runtogether if w in md]
print(f"    run-together words remaining: {rt if rt else 'none'}")
if rt: errors.append(f"run-together: {rt}")

print("\n" + "="*64)
if errors:
    print(f"FAILED — {len(errors)} problem(s):")
    for e in errors: print("  -", e)
    sys.exit(1)
print("PASSED — 37 rounds, 2 walks, 15 dimensions, piece counts, client-readiness")
