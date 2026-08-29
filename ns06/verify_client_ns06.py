"""Final gate on the corrected NS06 — parses the delivered client markdown."""
import re, pathlib, math, sys
sys.path.insert(0, "ns06")
from verify_stitches import eval_round, oval_foundation
from pieces import MM_ST, MM_RND, FOUNDATION

T = "NS06_Momo_the_Loaf_Cat_CLIENT.md"
md = pathlib.Path(T).read_text()
plain = re.sub(r"[*_`>]", "", md)
errors = []

print("[1] every round/row in the delivered file")
rows = re.findall(r'^\|\s*(Rnd\s*\d+|Row\s*\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
print(f"    rows parsed: {len(rows)}")
prev = 0
bad = 0
for i, (label, instr, stated) in enumerate(rows):
    n = int(re.search(r'\d+', label).group()); instr = instr.strip(); stated = int(stated)
    if n == 1:
        prev = 0
    if "2nd ch from hook" in instr:
        p = oval_foundation(FOUNDATION)["total"]; c = 0
    else:
        try:
            c, p = eval_round(instr, prev)
        except ValueError as e:
            errors.append(f"{label}: parse error {e}"); bad += 1; prev = stated; continue
    cons_ok = (c == prev) or (c == 0 and prev == 0) or (n == 1)
    if p != stated:
        errors.append(f"{label}: produces {p}, states ({stated}) [{instr}]"); bad += 1
    elif not cons_ok:
        errors.append(f"{label}: consumes {c} but previous row had {prev}"); bad += 1
    prev = stated
print(f"    stitch-count problems: {bad}")
if len(rows) != 27:
    errors.append(f"expected 27 rows (16 body + 3 ear + 8 tail), got {len(rows)}")

def circle_diam(n): return n * MM_ST / math.pi

print("\n[2] THE OVAL BASE — this is the defect the file corrects")
body = rows[:16]
SIDE = FOUNDATION - 3
print(f"    ch {FOUNDATION} -> the two long sides are N-3 = {SIDE} sts and never change")
for label, instr, stated in body[:6]:
    cap = (int(stated) - 2*SIDE) // 2
    print(f"    {label:<8} {stated:>3} st -> caps {cap}+{cap} sides {SIDE}+{SIDE}  "
          f"{'(sides present in the instruction)' if '6 sc' in instr else ''}")
base_st = int(body[5][2])
cap6 = (base_st - 2*SIDE) // 2
W = circle_diam(2*cap6)
L = W + SIDE*MM_ST
print(f"    base at full size = {base_st} st; caps {cap6} each")
print(f"    width  = a circle made from both caps ({2*cap6} st) = {W:.1f} mm")
print(f"    length = width + one side ({SIDE*MM_ST:.1f} mm) = {L:.1f} mm")
if base_st != 48:
    errors.append(f"base must reach 48 st to be a loaf, reaches {base_st}")

print("\n[3] the loaf premise: wider than it is tall")
blo = next(i for i, (l, ins, s) in enumerate(body) if "BLO" in ins)
walls = len(body) - blo
H = walls * MM_RND
print(f"    BLO at {body[blo][0]}, body ends {body[-1][0]} -> {walls} wall rounds "
      f"x {MM_RND} = {H:.1f} mm tall")
print(f"    {L:.1f} long x {W:.1f} wide x {H:.1f} tall;  width/height = {W/H:.2f}")
if W <= H:
    errors.append(f"width {W:.1f} mm not greater than height {H:.1f} mm - not a loaf")
for name, got, want, tol in [("length 79 mm", L, 79, 2), ("width 52 mm", W, 52, 2),
                             ("height 43 mm", H, 43, 1)]:
    ok = abs(got - want) <= tol
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<20} computed {got:7.2f}  stated {want}")
    if not ok:
        errors.append(name)
print(f"    cross-check: a {base_st}-st circle would be {circle_diam(base_st):.1f} mm "
      f"across; the oval is {W:.1f} mm - narrower, as it must be")

print("\n[4] eyes")
print(f"    7 st = {7*MM_ST:.1f} mm = {7*MM_ST/W*100:.0f}% of body width")
if not 50 <= 7*MM_ST/W*100 <= 75:
    errors.append("eye spacing outside a plausible share of body width")

print("\n[5] materials stated in the file")
def earea(P, k):
    lo, hi = 0.01, 500.0
    for _ in range(200):
        b = (lo+hi)/2; a = k*b
        if math.pi*(3*(a+b)-math.sqrt((3*a+b)*(a+3*b))) < P: lo = b
        else: hi = b
    b = (lo+hi)/2
    return math.pi*(k*b)*b
vol = sum(earea(int(s)*MM_ST, L/W)*MM_RND for _, _, s in body)/1000
stitches = sum(int(s) for _, _, s in rows)
print(f"    volume {vol:.0f} cm3 -> {vol*55/1000:.1f}-{vol*80/1000:.1f} g at 55-80 kg/m3")
print(f"    {stitches} stitches -> {stitches*MM_ST*4/1000:.1f} m -> "
      f"{stitches*MM_ST*4/1000/190*100:.1f} g at 190 m/100 g")
for pat, label, lo, hi in ((r'Worsted #4, about \*\*(\d+) g\*\*', "main yarn", 4, 15),
                           (r'Polyfill about \*\*(\d+) g\*\*', "polyfill",
                            vol*55/1000, vol*80/1000*1.2)):
    m = re.search(pat, md)
    if not m:
        errors.append(f"{label} figure not found"); print(f"    FAIL {label} not found")
    else:
        v = float(m.group(1))
        ok = lo <= v <= hi
        print(f"    {'OK  ' if ok else 'FAIL'} {label}: {v} g (plausible {lo:.1f}-{hi:.1f})")
        if not ok:
            errors.append(f"{label} {v} g outside {lo:.1f}-{hi:.1f}")

print("\n[6] safety wording")
if re.search(r'embroider\w* in black for a baby-safe version', plain, re.I):
    errors.append("still calls embroidered eyes a 'baby-safe version'")
print(f"    'baby-safe version' claim present: "
      f"{bool(re.search(r'for a baby-safe version', plain, re.I))}")
DISCLAIMER = re.compile(r'not been tested to a toy-safety standard', re.I)
has_disclaimer = bool(DISCLAIMER.search(plain))
if "baby-safe" in plain.lower() and not has_disclaimer:
    errors.append("baby-safe mentioned without the testing disclaimer")
for need in ["ASTM F963", "pull-test", "small parts"]:
    ok = need.lower() in plain.lower()
    print(f"    {'OK  ' if ok else 'FAIL'} '{need}' present")
    if not ok:
        errors.append(f"safety section missing '{need}'")
print(f"    {'OK  ' if has_disclaimer else 'FAIL'} 'not been tested to a toy-safety "
      f"standard' present")
if not has_disclaimer:
    errors.append("safety section missing the testing disclaimer")

print("\n[7] technique coverage — every technique the pattern uses is taught")
for tech in ["AROUND A CHAIN", "MAGIC RING", "SPIRAL", "BACK LOOP ONLY",
             "INVISIBLE DECREASE", "FLAT ROWS", "INTO BODY FABRIC"]:
    ok = tech.lower() in plain.lower()
    print(f"    {'OK  ' if ok else 'FAIL'} teaches {tech}")
    if not ok:
        errors.append(f"techniques section missing {tech}")

print("\n[8] client-readiness")
for w in [r"\bFAIL\b", "mismatch", "verify", "ns06/", "TODO", "CHANGES FROM",
          "correction", "solver", "&amp;", "Foundatio n", "oncethe", "thereis",
          "theoval", "long,low", "itagainst", "sewanything", "madefrom",
          "isstrictly", "Colourways", "centred", "ALL PIECES BEFORE ASSEMBLY",
          r"\bEasy\b"]:
    pat = w if w.startswith(r"\b") else re.escape(w)
    hits = [i+1 for i, l in enumerate(md.splitlines()) if re.search(pat, l, re.I)]
    if hits:
        errors.append(f"'{w}' lines {hits}")
        print(f"    FAIL '{w}' lines {hits}")
print(f"    forbidden strings: {sum(1 for e in errors if 'lines' in e)}")

print("\n" + "=" * 66)
if errors:
    print(f"FAILED - {len(errors)} problem(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"PASSED - {len(rows)} rows, oval base, loaf premise, materials, safety, "
      f"techniques, readiness")
