"""Final gate on the corrected NS10."""
import re, pathlib, math, sys
T = "NS10_Willow_the_Bunny_Lovey_CLIENT.md"
MM, MM_RND = 4.3, 3.8
errors = []
md = pathlib.Path(T).read_text(); plain = re.sub(r"[*_`>]", "", md)

src = pathlib.Path("ns10/verify_stitches.py").read_text().split("total_rounds = 0")[0]
ns = {}; exec(src, ns); eval_round = ns["eval_round"]
rows = re.findall(r'^\|\s*(R\d+|Rnd\s*\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
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
for e in errors: print("     -", e)
if len(rows) != 25: errors.append(f"expected 25 round rows (14 head + 11 ear), got {len(rows)}")

print("\n[2] blanket growth table must equal 12n")
tbl = dict((int(a), int(b)) for a, b in re.findall(r'^\|\s*(\d+)\s*\|\s*(\d+)\s*\|$', md, re.M))
for n, v in sorted(tbl.items()):
    ok = v == 12*n
    print(f"    Rnd {n:<3} stated {v:<4} 12n = {12*n:<4} {'OK' if ok else 'MISMATCH'}")
    if not ok: errors.append(f"blanket Rnd {n} = {v}, should be {12*n}")
if 20 not in tbl: errors.append("Rnd 20 row missing")

print("\n[3] blanket geometry")
edge_dc = 3*20
print(f"    60 dc per edge -> the text claims 60? {'60 dc along each edge' in plain}")
if "60 dc along each edge" not in plain: errors.append("60 dc claim missing")
for n, want in ((18, 23), (20, 26), (22, 28)):
    got = 3*n*MM/10
    ok = abs(got-want) <= 1.0
    print(f"    {'OK  ' if ok else 'FAIL'} {n} rounds -> {got:.1f} cm, stated {want} cm")
    if not ok: errors.append(f"{n} rounds = {got:.1f}, stated {want}")
print(f"    growth per round = 3 x {MM} = {3*MM/10:.2f} cm (stated 1.3 cm)")
if abs(3*MM/10 - 1.3) > 0.06: errors.append("growth per round")
# 240 dc is the whole perimeter -> 60 dc per edge; 60 x 4.3 mm = 25.8 cm
per_edge = tbl.get(20, 240) // 4
size_cm = per_edge * MM / 10
print(f"    perimeter {tbl.get(20)} dc / 4 = {per_edge} dc per edge -> {size_cm:.1f} cm "
      f"(stated 26 cm)")
if abs(size_cm - 26) > 1.0: errors.append("dc-to-size mismatch")

print("\n[4] border count")
b = 240 + 4*3
print(f"    240 dc + 4 corners x 3 sc = {b} sc; text states 252? {'252 sc' in plain}")
if b != 252 or "252 sc" not in plain: errors.append("border count")

print("\n[5] dimensions")
for name, got, want in [
    ("head across 4.9 cm", 36*MM/math.pi/10, 4.9),
    ("head height 5.3 cm", 14*MM_RND/10, 5.3),
    ("gauge check 9 dc = 39 mm", 9*MM, 39),
]:
    ok = abs(got-want) <= max(0.15, want*0.04)
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<26} computed {got:6.2f}  stated {want}")
    if not ok: errors.append(name)

print("\n[6] safety claim must not say 'fully baby-safe'")
for bad_phrase in ["fully baby-safe", "fully baby safe"]:
    if bad_phrase in plain.lower(): errors.append(f"'{bad_phrase}' still present")
print(f"    'fully baby-safe' present: {'fully baby-safe' in plain.lower()}")
print(f"    cot/supervision warning present: {'under 12 months' in plain}")
if "under 12 months" not in plain: errors.append("cot warning missing")

print("\n[7] client-readiness")
for w in [r"\bFAIL\b","mismatch","verify","ns10/","TODO","CHANGES FROM","correction",
          "solver","fibre","colour","centre","practising","&amp;","oncethe","thereis",
          "pinkor","ababy","pullsthe","inthe","cmfrom","itagainst","sewanything",
          "madefrom","isstrictly","adds 24 stitches","4.6 cm"]:
    pat = w if w.startswith(r"\b") else re.escape(w)
    hits = [i+1 for i,l in enumerate(md.splitlines()) if re.search(pat,l,re.I)]
    if hits: errors.append(f"'{w}' lines {hits}"); print(f"    FAIL '{w}' lines {hits}")
print(f"    forbidden strings: {sum(1 for e in errors if 'lines' in e)}")

print("\n" + "="*64)
if errors:
    print(f"FAILED — {len(errors)}:"); [print("  -",e) for e in errors]; sys.exit(1)
print(f"PASSED — {len(rows)} rounds, blanket table, geometry, border, readiness")
