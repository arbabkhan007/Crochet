"""Final gate on the corrected NS03 — parses the delivered client markdown."""
import re, pathlib, math, sys
sys.path.insert(0, "ns03")
from verify_stitches import eval_round
from pieces import MM_ST, MM_RND

T = "NS03_Axel_the_Axolotl_CLIENT.md"
md = pathlib.Path(T).read_text()
plain = re.sub(r"[*_`>]", "", md)
errors = []

print("[1] every round row in the delivered file")
rows = re.findall(r'^\|\s*(R\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
print(f"    round rows parsed: {len(rows)}")
prev = 0
bad = 0
for label, instr, stated in rows:
    n = int(label[1:]); instr = instr.strip(); stated = int(stated)
    if n == 1:
        prev = 0
    try:
        c, p = eval_round(instr, prev)
    except ValueError as e:
        errors.append(f"{label}: parse error {e}"); bad += 1; prev = stated; continue
    cons_ok = (c == prev) or (c == 0 and prev == 0)
    if p != stated:
        errors.append(f"{label}: produces {p}, states ({stated}) [{instr}]"); bad += 1
    elif not cons_ok:
        errors.append(f"{label}: consumes {c} but previous round had {prev}"); bad += 1
    prev = stated
print(f"    stitch-count problems: {bad}")
if len(rows) != 52:
    errors.append(f"expected 52 round rows (36+6+5+5), got {len(rows)}")

print("\n[2] geometry claims in the file")
def diam(n): return n * MM_ST / math.pi
gill_len = 5 * MM_RND
checks = [
    ("head dia 52 mm",        diam(36),                 52,  1.0),
    ("head height 51.6 mm",   12 * MM_RND,              51.6, 0.6),
    ("tail 43 mm",            10 * MM_RND,              43,  1.0),
    ("seated 115 mm",         26 * MM_RND,              115, 6),
    ("eye span 27 mm",        6 * MM_ST,                27,  1.5),
    ("gill span bare 94.6",   diam(36) + 2 * gill_len,  94.6, 1.0),
]
for name, got, want, tol in checks:
    ok = abs(got - want) <= tol
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<24} computed {got:7.1f}  stated {want}")
    if not ok:
        errors.append(name)

# the span the file advertises must be reachable
m = re.search(r'about \*\*(\d+(?:\.\d+)?) cm \([^)]*\)\*\* wide\s*\n?gill tip to gill tip',
              plain)
if not m:
    m = re.search(r'about (\d+(?:\.\d+)?) cm \([^)]*\) wide\s+gill tip to gill tip', plain)
if not m:
    errors.append("could not find the advertised gill span")
    print("    FAIL advertised gill span not found")
else:
    adv = float(m.group(1))
    bare = (diam(36) + 2 * gill_len) / 10
    ok = bare - 0.6 <= adv <= bare + 2.0
    print(f"    {'OK  ' if ok else 'FAIL'} advertised span {adv} cm vs bare {bare:.1f} cm "
          f"(+ up to 2 cm of teased fluff)")
    if not ok:
        errors.append(f"advertised span {adv} cm not reachable")

print("\n[3] stuffing / yarn figures stated in the file")
vol = 0.0
for _, _, n, _ in __import__("pieces").BODY:
    vol += math.pi * (diam(n) / 2) ** 2 * MM_RND
for rows_, copies in ((__import__("pieces").FOOT, 2),):
    for _, _, n, _ in rows_:
        vol += copies * math.pi * (diam(n) / 2) ** 2 * MM_RND
vol_cm3 = vol / 1000
g = vol_cm3 * 30 / 1000, vol_cm3 * 55 / 1000
print(f"    stuffed volume {vol_cm3:.0f} cm3 -> {g[0]:.1f}-{g[1]:.1f} g at 30-55 kg/m3")
m = re.search(r'Polyfill about \*\*(\d+) g\*\*', md)   # raw md: markup intact
stated_g = float(m.group(1)) if m else None
print(f"    file states {stated_g} g")
if stated_g is None:
    errors.append("polyfill figure not found")
elif not (g[0] <= stated_g <= g[1] * 1.4):
    errors.append(f"polyfill {stated_g} g outside {g[0]:.1f}-{g[1]*1.4:.1f} g")
for label, pat in (("main yarn", r'pale pink, about \*\*(\d+) g\*\*'),
                   ("gill yarn", r'dark pink, about \*\*(\d+) g\*\*')):
    mm = re.search(pat, md)   # raw md: markup intact
    print(f"    {label}: {mm.group(1) if mm else 'NOT FOUND'} g")
    if not mm:
        errors.append(f"{label} figure not found")

print("\n[4] safety section")
print(f"    'fully baby-safe' present: {'fully baby-safe' in plain.lower()}")
if "fully baby-safe" in plain.lower():
    errors.append("'fully baby-safe' present")
for need in ["ASTM F963", "pull-test", "small parts"]:
    if need.lower() not in plain.lower():
        errors.append(f"safety section missing '{need}'")
    print(f"    '{need}' present: {need.lower() in plain.lower()}")

print("\n[5] techniques coverage — every technique the pattern uses is taught")
for tech in ["MAGIC RING", "SPIRAL", "INVISIBLE DECREASE", "BOTH LAYERS", "SHELL"]:
    ok = tech.lower() in plain.lower()
    print(f"    {'OK  ' if ok else 'FAIL'} teaches {tech}")
    if not ok:
        errors.append(f"techniques section missing {tech}")

print("\n[6] client-readiness")
for w in [r"\bFAIL\b", "mismatch", "verify", "ns03/", "TODO", "CHANGES FROM",
          "correction", "solver", "&amp;", "fibre", "colour", "centred",
          "fluffygills", "oncethe", "thereis", "thebody", "stuffinginto",
          "permanentlysturdier", "shortenedthe", "charcoalbody", "theshell",
          "itagainst", "sewanything", "madefrom", "isstrictly", "cmtail",
          "stitchmarker", "close-set", "12 cm wide gill tip", "pet slicker"]:
    pat = w if w.startswith(r"\b") else re.escape(w)
    hits = [i + 1 for i, l in enumerate(md.splitlines()) if re.search(pat, l, re.I)]
    if hits:
        errors.append(f"'{w}' lines {hits}")
        print(f"    FAIL '{w}' lines {hits}")
print(f"    forbidden strings: {sum(1 for e in errors if 'lines' in e)}")

print("\n" + "=" * 64)
if errors:
    print(f"FAILED - {len(errors)} problem(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"PASSED - {len(rows)} rounds, geometry, materials, safety, techniques, readiness")
