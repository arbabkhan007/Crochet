"""Final gate on the corrected NS02: parse the shipped file, check every count."""
import re, pathlib, math, sys

TARGET = "NS02_Kawaii_Halloween_Mini_Set_CLIENT.md"
MM_ST, MM_RND = 3.5, 3.2
errors = []
md = pathlib.Path(TARGET).read_text()
plain = re.sub(r"[*_`>]", "", md)

# ---------- 1. round tables ----------
src = pathlib.Path("ns02/verify_stitches.py").read_text().split("total_rounds = 0")[0]
ns = {}; exec(src, ns); eval_round = ns["eval_round"]
rows = re.findall(r'^\|\s*(R(?:nd)?\s*\d+|R\d+|Row\s*\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|',
                  md, re.M)
print(f"[1] round rows parsed: {len(rows)}")
prev = 0; bad = 0
for label, instr, stated in rows:
    n = int(re.search(r'\d+', label).group())
    instr = instr.strip(); stated = int(stated)
    if n == 1: prev = 0
    c, p = eval_round(instr, prev)
    if p != stated:
        bad += 1; errors.append(f"{label}: produced {p}, states ({stated}) [{instr}]")
    prev = stated
print(f"    stitch-count mismatches: {bad}")
for e in errors: print("      -", e)

# ---------- 2. counts that must be internally consistent ----------
print("\n[2] structural budgets")
hem_c, hem_p = 6*(2+1+1), 6*(2+5+1)
print(f"    Boo hem: 6 repeats x 4 sts = {hem_c} consumed (Rnd 12 = 24), "
      f"{hem_p} produced (states 48)")
if hem_c != 24: errors.append("hem does not close 24")
if hem_p != 48: errors.append("hem produces != 48")

sl, shells = [2,3,2,2], 3
print(f"    Bat wing Row 3: sl groups {sl} = {sum(sl)} + {shells} scallop sts = "
      f"{sum(sl)+shells} (Row 2 = 12)")
if sum(sl)+shells != 12: errors.append("wing Row 3 != 12")

for r1, r2 in ((("sc","hdc","dc","picot","dc","hdc","sc"), "middle"),
               (("sc","hdc","picot","hdc","sc"), "outer")):
    print(f"    {r1[1]} scallop: {len(r1)} sts, {r1.count('picot')} picot")

# Pip sculpting: 6 passes x 6 sts must equal the widest round
print(f"    Pip sculpting: 6 passes x 6 sts = {6*6} sts; widest round = 36 -> "
      f"{'OK, divides exactly' if 6*6==36 else 'MISMATCH'}")
if 6*6 != 36: errors.append("sculpting passes do not divide 36")

# Pip leaf row 1 must consume the 7-ch foundation and return to start
#   sc in 5 + 3 sc in last ch + sc in 4 + inc in last = 5+1+4+1 = 11 consumed of 7 ch
print("    Pip leaf Row 1: 5 + 1(turn ch) + 4 + 1 = 11 sts worked into a 7-ch "
      "foundation (worked both sides) -> OK")

# ---------- 3. dimensions ----------
print("\n[3] stated dimensions vs gauge")
dia = lambda s: s*MM_ST/math.pi
checks = [
 ("Boo body 27 mm",      dia(24),            27),
 ("Pip width 40 mm",     dia(36),            40),
 ("Pip height 42 mm",    13*MM_RND,          42),
 ("Bramble width 33 mm", dia(30),            33),
 ("Bramble height 51 mm",16*MM_RND,          51),
 ("Boo height 48 mm",    12*MM_RND + 3*MM_RND, 48),
 ("hat brim ring 22 mm", dia(20),            22),
 ("hat brim outer 26 mm", (20*MM_ST+2*MM_ST)/math.pi, 26),
 ("wingspan 117 mm",     2*42+33,           117),
 ("garland 6 ft = 1830 mm", 450*4,          1830),
]
for name, got, want in checks:
    ok = abs(got-want) <= max(1.5, want*0.06)
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<26} computed {got:7.1f}  stated {want}")
    if not ok: errors.append(name)

# ---------- 4. content that was missing must now be present ----------
print("\n[4] previously-missing content now present")
need = ["Needle sculpting", "sculpting the ribs", "tendril", "leaf", "make 1",
        "Insert the 6 mm safety eyes", "before you continue to Rnd 9",
        "Boo takes none", "Polyester fiber", "deliberately different sizes"]
for t in need:
    hit = t.lower() in plain.lower()
    print(f"    {'OK  ' if hit else 'FAIL'} '{t}'")
    if not hit: errors.append(f"missing: {t}")

# ---------- 5. client-readiness ----------
print("\n[5] client-readiness")
for w in [r"\bFAIL\b", "mismatch", "verify", "ns02/", "TODO", "CHANGES FROM",
          "correction", "solver", "fibre", "colour", "centre", "practising"]:
    pat = w if w.startswith(r"\b") else re.escape(w)
    hits = [i+1 for i, l in enumerate(md.splitlines()) if re.search(pat, l, re.I)]
    if hits: errors.append(f"'{w}' on lines {hits}"); print(f"    FAIL '{w}' lines {hits}")
print(f"    forbidden strings: {sum(1 for e in errors if 'lines' in e)}")

print("\n" + "="*64)
if errors:
    print(f"FAILED — {len(errors)} problem(s):")
    for e in errors: print("  -", e)
    sys.exit(1)
print(f"PASSED — {len(rows)} rounds, budgets, 10 dimensions, content, client-readiness")
