"""Final gate on the corrected NS09 — parses the delivered client markdown."""
import re, pathlib, math, sys
sys.path.insert(0, "ns09")
from verify_stitches import eval_round
from pieces import MM_ST, MM_RND

T = "NS09_Shelby_the_Sea_Turtle_Bag_Charm_CLIENT.md"
md = pathlib.Path(T).read_text()
plain = re.sub(r"[*_`>]", "", md)
flat = re.sub(r"\s+", " ", plain)   # line wraps break literal phrase matching
errors = []

print("[1] the main tables")
rows = re.findall(r'^\|\s*(Rnd\s*\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
main = [r for r in rows if r[0] != "Rnd 8"]
big  = [r for r in rows if r[0] == "Rnd 8"]
print(f"    main rows: {len(main)}   bigger-Shelby rows: {len(big)}")
prev = 0
bad = 0
for label, instr, stated in main:
    n = int(re.search(r'\d+', label).group()); instr = instr.strip(); stated = int(stated)
    if n == 1:
        prev = 0
    try:
        c, p = eval_round(instr, prev)
    except ValueError as e:
        errors.append(f"{label}: parse error {e}"); bad += 1; prev = stated; continue
    cons_ok = (c == prev) or (c == 0 and prev == 0) or (n == 1)
    if p != stated:
        errors.append(f"{label}: produces {p}, states ({stated})"); bad += 1
    elif not cons_ok:
        errors.append(f"{label}: consumes {c} but previous round had {prev}"); bad += 1
    prev = stated
print(f"    stitch-count problems: {bad}")
if len(main) != 11:
    errors.append(f"expected 11 main rows (6 shell + 5 underside), got {len(main)}")

print("\n[2] the bump round — 24 in, 35 out, exactly closing the disc")
bump = main[-1]
c, p = eval_round(bump[1].strip(), 24)
print(f"    consumes {c}, produces {p}; states ({bump[2]})")
if (c, p) != (24, 35):
    errors.append(f"bump round consumes {c} produces {p}, expected 24 and 35")

print("\n[3] THE SIZE CLAIM — this is the defect the file corrects")
RIM = 24
D = RIM * MM_ST / math.pi
hdc_h = MM_RND * 1.6
across, length, depth = D + 2*hdc_h, D + hdc_h, 6*MM_RND
print(f"    {RIM} st disc = {D:.2f} mm across")
print(f"    across the flippers {across:.1f} mm, head to tail {length:.1f} mm, "
      f"depth {depth:.1f} mm")
for name, got, stated in (("across the flippers", across, 37),
                          ("long", length, 32), ("deep", depth, 19)):
    m = re.search(re.escape(f"{stated/10:.1f} cm"), md)
    ok = m is not None and abs(got/10 - stated/10) <= 0.25
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<20} computed {got/10:.2f} cm, "
          f"file states {stated/10:.1f} cm")
    if not ok:
        errors.append(f"{name} not stated correctly")
for wrong in ("6 cm across the flippers", "4.5 cm long"):
    hits = [i+1 for i, l in enumerate(md.splitlines())
            if wrong in l and "do not list the small one as 6 cm" not in l]
    if hits:
        errors.append(f"old size claim '{wrong}' still on lines {hits}")
        print(f"    FAIL old claim '{wrong}' lines {hits}")
print(f"    the old 6 cm claim survives only inside the explicit warning: "
      f"{'do not list the small one as 6 cm' in flat}")

print("\n[4] the join is specified, not left ambiguous")
for need in ["Match 24 to 24, not 24 to 35", "19 plain stitches plus", "base stitch"]:
    ok = need in flat
    print(f"    {'OK  ' if ok else 'FAIL'} states {need!r}")
    if not ok:
        errors.append(f"join note missing '{need}'")

print("\n[5] the bigger Shelby — verify its rounds too")
c, p = eval_round(big[0][1].strip(), 42)
print(f"    Rnd 8 bump round from 42: consumes {c}, produces {p}; states ({big[0][2]})")
if (c, p) != (42, 53):
    errors.append(f"bigger bump round consumes {c} produces {p}, expected 42 and 53")
prose = re.findall(r'Rnd (\d+):\s+([^(]+?)\s+\((\d+)\)', flat)
shell_big = [(int(a), b.strip(), int(cc)) for a, b, cc in prose if int(a) <= 9]
print(f"    prose rounds found: {len(shell_big)}")
prev = 0
for n, instr, stated in shell_big:
    if n == 1:
        prev = 0
    try:
        c, p = eval_round(instr, prev)
    except ValueError as e:
        print(f"      Rnd {n}: parse error {e}"); continue
    cons_ok = (c == prev) or (n == 1)
    tag = "OK" if p == stated and cons_ok else "MISMATCH"
    print(f"      Rnd {n:<2} {instr[:34]:<36} stated ({stated:>2}) produced {p:>2} {tag}")
    if p != stated or not cons_ok:
        errors.append(f"bigger Shelby Rnd {n}: {instr} -> {p}, states ({stated})")
    prev = stated
D42 = 42 * MM_ST / math.pi
print(f"    42 st disc = {D42:.1f} mm -> across the flippers {D42+2*hdc_h:.1f} mm "
      f"= {(D42+2*hdc_h)/10:.1f} cm, depth {9*MM_RND/10:.1f} cm")
for want in ("5.7 cm across the flippers", "2.9 cm deep"):
    if want not in flat:
        errors.append(f"bigger Shelby missing '{want}'")

print("\n[6] materials stated in the file")
stitches = sum(int(s) for _, _, s in main)
vol = 8.3
print(f"    {stitches} stitches -> {stitches*MM_ST*4/1000:.1f} m -> "
      f"{stitches*MM_ST*4/1000/250*100:.2f} g at 250 m/100 g DK")
print(f"    shell holds about {vol:.0f} cm3 -> {vol*55/1000:.2f}-{vol*80/1000:.2f} g")
for pat, label in ((r'cotton, about \*\*(\d+) g\*\*', "shell yarn"),
                   (r'DK cotton, about \*\*(\d+) g\*\*', "body yarn")):
    m = re.search(pat, md)
    print(f"    {label}: {m.group(1) if m else 'NOT FOUND'} g")
    if not m:
        errors.append(f"{label} figure not found")
if "pinch of polyfill" not in flat:
    errors.append("polyfill figure not restated")

print("\n[7] eye guidance is honest about the fit")
for need in ["washer of roughly 6\u20137 mm", "French knots are the better choice",
             "1 stitch apart"]:
    ok = need in flat
    print(f"    {'OK  ' if ok else 'FAIL'} states {need!r}")
    if not ok:
        errors.append(f"eye note missing '{need}'")

print("\n[8] safety wording")
DISC = re.compile(r'not been tested to a toy-safety standard', re.I)
has = bool(DISC.search(plain))
print(f"    'not been tested to a toy-safety standard' present: {has}")
if not has:
    errors.append("safety disclaimer missing")
for need in ["ASTM F963", "pull-test", "small parts", "pocket toy"]:
    ok = need.lower() in plain.lower()
    print(f"    {'OK  ' if ok else 'FAIL'} '{need}' present")
    if not ok:
        errors.append(f"safety section missing '{need}'")

print("\n[9] technique coverage — every technique the pattern uses is taught")
for tech in ["MAGIC RING", "SPIRAL", "BACK LOOP ONLY", "INTO ONE STITCH",
             "WHIP STITCH", "FRENCH KNOTS"]:
    ok = tech.lower() in plain.lower()
    print(f"    {'OK  ' if ok else 'FAIL'} teaches {tech}")
    if not ok:
        errors.append(f"techniques section missing {tech}")

print("\n[10] client-readiness")
for w in [r"\bFAIL\b", "mismatch", "verify", "ns09/", "TODO", "CHANGES FROM",
          "correction", "solver", "&amp;", "innext st", "sc\)in next st",
          "oncethe", "thereis", "itacross", "sewanything", "madefrom",
          "isstrictly", "mixed-colour", "colour", "Colourways", "centred"]:
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
print(f"PASSED - {len(main)} main rows + bigger variant, size, join, materials, "
      f"eyes, safety, techniques, readiness")
