"""NS05 Little Duck — client-file gate. Re-runs the stitch and geometry
verifiers, then checks the published .md against what was verified."""
import pathlib, re, subprocess, sys
sys.path.insert(0, "ns05")
from verify_stitches import eval_round, beak_foundation
from pieces import BEAK_CHAIN, MM_RND, MM_ST, CLAIM, BODY

ROOT = pathlib.Path(__file__).resolve().parents[1]
MD = ROOT / "NS05_Little_Duck_Plushie_CLIENT.md"
raw = MD.read_text()
flat = re.sub(r"\s+", " ", re.sub(r"\*\*|__|\*", "", raw))

fails = []
def ck(cond, msg):
    print(f"  {'OK  ' if cond else 'FAIL'} {msg}")
    if not cond:
        fails.append(msg)

# 1. underlying gates
for gate in ("ns05/verify_stitches.py", "ns05/verify_geometry.py"):
    print(f"[gate] {gate}")
    r = subprocess.run([sys.executable, str(ROOT / gate)], capture_output=True, text=True)
    print("   ", r.stdout.strip().splitlines()[-1])
    if r.returncode != 0:
        fails.append(f"{gate} exited {r.returncode}")

# 2. every published table row, plus the two prose beak rounds
print("\n[published rounds]")
row_re = re.compile(r"^\|\s*(R\d+)\s*\|\s*(.+?)\s*\|\s*\((\d+)\)\s*\|", re.M)
prev, n, bad = 0, 0, 0
for label, cell, stated in row_re.findall(raw):
    stated = int(stated)
    cell = cell.strip().rstrip(".").strip()
    if label == "R1":
        prev = 0
    try:
        c, p = eval_round(cell, prev)
    except ValueError as e:
        print(f"  PARSE {label:<5} {e}"); bad += 1; n += 1; continue
    if p != stated or c != prev:
        bad += 1
        print(f"  MISMATCH {label:<5} stated ({stated}) produced {p} consumed {c} "
              f"prev {prev}\n       <- {cell}")
    prev = stated
    n += 1
print(f"  {n} table rows checked")

beak_re = re.compile(r"\*\*Rnd (\d)\.\*\*(.+?)\*\*\[(\d+)\]\*\*", re.S)
for num, cell, stated in beak_re.findall(raw):
    stated = int(stated)
    if num == "1":
        b = beak_foundation(BEAK_CHAIN)
        ok = b["total"] == stated
        print(f"  {'ok  ' if ok else 'FAIL'} beak Rnd 1 around ch {BEAK_CHAIN} -> "
              f"{b['total']} (stated {stated})")
        if not ok:
            bad += 1
        prev = stated
    else:
        cell = cell.strip().rstrip(".").strip()
        c, p = eval_round(cell, prev)
        ok = p == stated and c == prev
        print(f"  {'ok  ' if ok else 'FAIL'} beak Rnd 2 -> produced {p} consumed {c} "
              f"prev {prev} (stated {stated})")
        if not ok:
            bad += 1
        prev = stated
    n += 1
ck(bad == 0, "every published round count is arithmetically correct")
ck(n == 29, f"all rows covered ({n} published; model has 30 incl. the wing close, "
            f"which is prose)")

# 3. no review artefacts
print("\n[no review markup]")
for pat, name in ((r"\bCORRECTED\b", "CORRECTED"), (r"\bCORRECTION\b", "CORRECTION"),
                  (r"\bORIGINAL\b", "ORIGINAL"), (r"\bchangelog\b", "changelog"),
                  (r"\breviewer\b", "reviewer"), (r"NS0[0-9]", "NS0x identifier"),
                  (r"\bverify_", "verifier filename"), (r"\.venv|/home/|~/", "internal path"),
                  (r"\bthis pattern had\b", "self-referential correction")):
    ck(not re.search(pat, raw, re.I), f"absent: {name}")

# 4. claims that were CORRECT must still be there
print("\n[verified claims retained]")
ck(re.search(r"16 cm \(6\.25 in\) tall", flat) is not None, "16 cm / 6.25 in tall kept")
ck(re.search(r"7\.5 cm \(3 in\) wide", flat) is not None, "7.5 cm / 3 in wide kept")
ck(re.search(r"8 mm per\s*\*{0,2}\s*stitch", flat) is not None
   and re.search(r"7 mm per round", flat) is not None, "8 mm/st and 7 mm/rnd kept")
ck(re.search(r"at 10 mm per stitch this pattern finishes near 20 cm", flat) is not None,
   "the 10 mm -> 20 cm troubleshooting entry kept")
ck(re.search(r"12-stitch swatch", flat) is not None, "12-stitch swatch advice kept")
ck(re.search(r"7\u20138 stitches apart", flat) is not None, "eye spacing kept")

# 5. claims that were WRONG must be replaced
print("\n[corrected claims]")
ck("55–75 g" not in flat and "55-75 g" not in flat, "old 55-75 g body yarn figure gone")
ck(re.search(r"about 25\u201335 g", flat) is not None, "body yarn corrected to 25-35 g")
ck(re.search(r"enough for three ducks", flat) is not None, "the scrap-saving point is made")
ck(re.search(r"about 25\u201335 g\*\*, packed firmly", raw) is not None,
   "fiberfill quantity now stated")
ck(re.search(r"DK / light worsted \(#3\)\s*\|\s*7\u20138 cm", flat) is not None,
   "DK re-scoped to 7-8 cm")
ck(re.search(r"Velvet / bulky \(#5\)\s*\|\s*10\u201312 cm", flat) is not None,
   "velvet carries the 10-12 cm claim")
ck(re.search(r"lands at\s*about 8 cm rather than 10\u201312 cm", flat) is not None,
   "the DK shortfall is explained, not hidden")

# 6. construction fixes
print("\n[construction]")
ck(re.search(r"start stuffing now", raw) is not None
   and re.search(r"Start stuffing at R10, not R12", flat) is not None,
   "stuffing moved earlier, with the reason")
ck(re.search(r"through the \*\*FLO\*\* of each", raw) is not None,
   "FLO is now actually used, so the abbreviation earns its place")
ck(re.search(r"Do not stuff the beak", flat) is not None
   and re.search(r"Flatten it before pinning", flat) is not None,
   "beak flattening stated")
ck(re.search(r"work \*\*Rnd 1 only\*\*", raw) is not None
   and re.search(r"about 37 mm long", flat) is not None,
   "smaller-beak option offered with its verified size")
ck(re.search(r"about 50 mm long", flat) is not None
   and re.search(r"two-thirds of the head width", flat) is not None,
   "as-written beak size disclosed")
ck(re.search(r"same diameter", flat) is not None
   and re.search(r"stop the reflare at R13", flat) is not None,
   "head/body proportion disclosed with an alternative")

# 7. techniques and abbreviations
print("\n[techniques and abbreviations]")
for t in ("Magic ring", "continuous spiral", "Invisible decreases",
          "both sides of a starting chain", "through both layers",
          "Embroidery", "Sewing on"):
    ck(t in raw, f"listed: {t}")
ck(re.search(r"## Invisible Decrease", raw) is not None, "invisible decrease explained")
for ab in ("MR", "ch", "sc", "inc", "dec", "sl st", "FLO", "FO"):
    ck(re.search(r"^\| " + re.escape(ab) + r" \|", raw, re.M) is not None,
       f"abbreviation defined: {ab}")

# 8. safety and terms
print("\n[safety and terms]")
ck(re.search(r"embroidered eyes", flat, re.I) is not None, "embroidered eyes noted as safer")
ck(re.search(r"EN 71", flat) is not None and re.search(r"ASTM F963", flat) is not None
   and re.search(r"CPSIA", flat) is not None, "standards named")
ck(re.search(r"shed", flat) is not None, "chenille shedding flagged")
ck(re.search(r"Novality Store", flat) is not None
   and re.search(r"strictly prohibited", flat) is not None, "terms of use preserved")

# 9. copy quality
print("\n[copy quality]")
for w in ("centre", "centred", "colour", "fibre"):
    ck(w not in raw, f"no British '{w}' in a US-terms pattern")
for typo in ("perround", "swatchbefore", "asmaller", "mmhook", "oncethe", "thereis",
             "thecheeks", "ofstuffing", "10mm", "duck,which", "itagainst",
             "sewanything", "madefrom", "isstrictly", "&amp;"):
    ck(typo not in raw, f"typo absent: {typo!r}")
ck(re.search(r"\b4\.5 mm \(US 7\)", flat) is not None, "hook given with its US size")

print("\n" + "=" * 74)
if fails:
    print(f"FAIL - {len(fails)} problem(s):")
    for f in fails:
        print("  -", f)
else:
    print(f"PASS - {n} published rounds verified; client file is clean")
sys.exit(1 if fails else 0)
