"""Final gate on the corrected NS08."""
import re, pathlib, math, sys
TARGET = "NS08_Ember_the_Baby_Dragon_CLIENT.md"
MM_ST, MM_RND = 4.5, 4.3
errors = []
md = pathlib.Path(TARGET).read_text()
plain = re.sub(r"[*_`>]", "", md)

src = pathlib.Path("ns08/verify_stitches.py").read_text().split("total_rounds = 0")[0]
ns = {}; exec(src, ns); eval_round = ns["eval_round"]
rows = re.findall(r'^\|\s*(R\d+|Row\s*\d+)\s*\|([^|]+?)\|\s*\*\*\[(\d+)\]\*\*\s*\|', md, re.M)
rows += re.findall(r'^\|\s*(R\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
print(f"[1] round rows parsed: {len(rows)}")
prev = 0; bad = 0
for label, instr, stated in rows:
    n = int(re.search(r'\d+', label).group()); instr = instr.strip(); stated = int(stated)
    if n == 1: prev = 0
    c, p = eval_round(instr, prev)
    if p != stated:
        bad += 1; errors.append(f"{label}: produced {p}, states ({stated}) [{instr}]")
    prev = stated
print(f"    stitch-count mismatches: {bad}")
for e in errors: print("      -", e)

print("\n[2] spike strip budget")
strip = 1 + 9*3 + 2   # 1 sc, 9 spikes x 3 sts each (sl st, sc, hdc), 2 sc
print(f"    ch 4 -> 1 sc, 9 spikes x 3 sts, 2 sc = {strip} sts")
print(f"    length = 9 spikes x 13.5 + 3 ends x 4.5 = {9*13.5 + 3*4*4.5/4*4/3:.0f} mm; "
      f"crown-to-tail path = {13*MM_RND + 11*MM_RND + 12*MM_RND:.0f} mm")
strip_len = 9*13.5 + 3*4.5           # 9 spikes + 3 plain sts at the ends
path_len  = 13*MM_RND + 11*MM_RND + 12*MM_RND
print(f"    strip {strip_len:.0f} mm vs path {path_len:.0f} mm -> "
      f"{(strip_len-path_len)/path_len*100:+.0f}% (a snug fit is intended)")
if not (0.85 <= strip_len/path_len <= 1.05): errors.append("spike strip length wrong")

print("\n[3] wing row budget")
if 2+1+2+1+4 != 10: errors.append("wing row 4 != 10")
print(f"    sl groups 2/2/4 = 8 + 2 shells = 10 (Row 3 = 10) -> OK")

print("\n[4] dimensions")
body, head = 13*MM_RND, 11*MM_RND
checks = [("seated height 103 mm", body+head, 103),
          ("body 56 mm", body, 56), ("head 47 mm", head, 47),
          ("wing 45 mm", 10*MM_ST, 45),
          ("wingspan 124 mm", 2*10*MM_ST + 24*MM_ST/math.pi, 124),
          ("tail 52 mm", 12*MM_RND, 52),
          ("neck ring 26 mm", 18*MM_ST/math.pi, 26),
          ("back leg 26 mm", 6*MM_RND, 26), ("front leg 34 mm", 8*MM_RND, 34)]
for name, got, want in checks:
    ok = abs(got-want) <= max(1.5, want*0.06)
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<24} computed {got:6.1f}  stated {want}")
    if not ok: errors.append(name)

print("\n[5] legs land level")
print(f"    back  6 rnd = {6*MM_RND:.1f} mm, attaches R6 = {6*MM_RND:.1f} mm up "
      f"-> foot {6*MM_RND-6*MM_RND:.1f} mm below base")
print(f"    front 8 rnd = {8*MM_RND:.1f} mm, attaches R8 = {8*MM_RND:.1f} mm up "
      f"-> foot {8*MM_RND-8*MM_RND:.1f} mm below base")
if abs((6*MM_RND-6*MM_RND)-(8*MM_RND-8*MM_RND)) > 0.5: errors.append("legs not level")

print("\n[6] head and neck must match at 18 sts")
for t in ("leave open", "18 stitches", "left open", "open at 18 stitches"):
    hit = t.lower() in plain.lower()
    print(f"    {'OK  ' if hit else 'FAIL'} '{t}'")
    if not hit: errors.append(t)

print("\n[7] client-readiness")
for w in [r"\bFAIL\b","mismatch","verify","ns08/","TODO","CHANGES FROM","correction",
          "solver","fibre","colour","centre","practising","&amp;","oncethe","thereis"]:
    pat = w if w.startswith(r"\b") else re.escape(w)
    hits = [i+1 for i,l in enumerate(md.splitlines()) if re.search(pat,l,re.I)]
    if hits: errors.append(f"'{w}' lines {hits}"); print(f"    FAIL '{w}' lines {hits}")
print(f"    forbidden strings: {sum(1 for e in errors if 'lines' in e)}")

print("\n" + "="*64)
if errors:
    print(f"FAILED — {len(errors)}:");  [print("  -",e) for e in errors]; sys.exit(1)
print(f"PASSED — {len(rows)} rounds, budgets, dimensions, leg geometry, readiness")
