"""NS07 Trio — client-file gate. Re-runs the stitch + geometry verifiers, then
checks the published .md against what was verified."""
import pathlib, re, subprocess, sys
sys.path.insert(0, "ns07")
from verify_stitches import eval_round

ROOT = pathlib.Path(__file__).resolve().parents[1]
MD = ROOT / "NS07_Pocket_Positivity_Trio_CLIENT.md"
raw = MD.read_text()
flat = re.sub(r"\s+", " ", re.sub(r"\*\*|__|\*", "", raw))

fails = []
def ck(cond, msg):
    print(f"  {'OK  ' if cond else 'FAIL'} {msg}")
    if not cond:
        fails.append(msg)

# 1. the two underlying gates still pass on the published instruction text
for gate in ("ns07/verify_stitches.py", "ns07/verify_geometry.py"):
    print(f"[gate] {gate}")
    r = subprocess.run([sys.executable, str(ROOT / gate)], capture_output=True, text=True)
    print("   ", r.stdout.strip().splitlines()[-1])
    if r.returncode != 0:
        fails.append(f"{gate} exited {r.returncode}")

# 2. every table round in the file parses and verifies.
#    The published cells use three conventions the raw instruction text does not:
#      - a trailing note after the count:  "dec x6 (6) - stuff firmly"
#      - a compressed multi-round cell:    "sc in each st around, 3 rnd"
#      - a chain-start foundation row:     "ch 6, sc in 2nd ch from hook, ..."
#    Each is expanded here so every stated count is actually checked.
print("\n[published rounds]")
row_re = re.compile(
    r"^\|\s*(Rnd [\dA-Za-z\u2013-]+|Petal rnd)\s*\|\s*(.+?)\s*\|\s*\((\d+)\)\s*\|",
    re.M)
rows = row_re.findall(raw)


def chain_start_total(text):
    """Sum the stitches written into a foundation chain: ch 6 -> 12."""
    body = re.sub(r"^ch\s+\d+\s*,\s*", "", text)
    body = re.sub(r"working on the other side of the chain\s*:", ",", body)
    body = re.sub(r"in\s+(?:2nd ch from hook|last ch|next ch)", "", body)
    return sum(int(t) if t else 1
               for t in re.findall(r"(?:(\d+)\s+)?sc", body))


prev, n_rounds, n_rows, n_bad = 0, 0, 0, 0
for label, cell, stated in rows:
    stated = int(stated)
    cell = cell.strip()
    # drop the restated count and anything after it
    cell = re.sub(r"\s*\(\d+\).*$", "", cell)
    cell = re.sub(r"\s*[\u2014-]\s*[^,;]*$", "", cell).strip().rstrip(".").strip()
    # expand a compressed "..., 3 rnd" cell
    m = re.search(r",\s*(\d+)\s*rnd\s*$", cell)
    reps = int(m.group(1)) if m else 1
    if m:
        cell = cell[:m.start()].strip()
    if cell.startswith("ch ") or "2nd ch from hook" in cell:
        got = chain_start_total(cell)
        ok = got == stated
        print(f"  {'ok  ' if ok else 'FAIL'} {label:<10} chain row -> {got} "
              f"(stated {stated})")
        if not ok:
            n_bad += 1
            print(f"       <- {cell}")
        n_rounds += 1; n_rows += 1; prev = stated
        continue
    if re.fullmatch(r"Rnd 1", label):
        prev = 0
    if label == "Petal rnd":
        # the petals are worked into Rnd 3 of the center, not the last round
        prev = int(next(c for l, _, c in rows if l == "Rnd 3"))  # Sunny center, first
    for _ in range(reps):
        try:
            c, p_ = eval_round(cell, prev)
        except ValueError as e:
            print(f"  PARSE {label:<10} {e}"); n_bad += 1; n_rounds += 1; continue
        if p_ != stated or c != prev:
            n_bad += 1
            print(f"  MISMATCH {label:<9} stated ({stated}) produced {p_} "
                  f"consumed {c} prev {prev}\n       <- {cell}")
        n_rounds += 1
    prev = stated
    n_rows += 1
print(f"  {n_rows} published rows -> {n_rounds} rounds checked, {n_bad} mismatches")
ck(n_bad == 0, "every published round count is arithmetically correct")
ck(n_rounds == 38, f"all rounds covered ({n_rounds} expanded; model says 38)")

# 3. no review artefacts
print("\n[no review markup]")
for pat, name in ((r"\bCORRECTED\b", "CORRECTED"), (r"\bCORRECTION\b", "CORRECTION"),
                  (r"\bORIGINAL\b", "ORIGINAL"), (r"\bNOTE TO\b", "NOTE TO"),
                  (r"\bchangelog\b", "changelog"), (r"\breviewer\b", "reviewer"),
                  (r"NS0[0-9]", "NS0x identifier"), (r"\bverify_", "verifier filename"),
                  (r"\.venv|/home/|~/", "internal path"), (r"\bthis pattern had\b",
                  "self-referential correction")):
    ck(not re.search(pat, raw, re.I), f"absent: {name}")

# 4. the corrected sizes are in, the overstated ones are out
print("\n[sizes]")
ck(re.search(r"3\.0 cm \(1\.2 in\) across the petals", flat) is not None,
   "Sunny corrected to 3.0 cm")
ck(re.search(r"3\.8 cm \(1\.5 in\) tall", flat) is not None, "Waddle corrected to 3.8 cm")
ck(re.search(r"2\.7 cm \(1\.1 in\) long", flat) is not None, "Spud corrected to 2.7 cm")
for bad in ("4.5 cm across the petals", "5 cm tall", "5.5 cm long",
            "each about 5 cm tall", "4.5–5.5 cm", "4.5-5.5 cm"):
    ck(bad not in flat, f"overstated claim removed: '{bad}'")
ck(re.search(r"about 3\.9 cm", flat) is not None
   and re.search(r"about 4\.9 cm tall", flat) is not None
   and re.search(r"about 3\.5 cm long", flat) is not None,
   "bigger-trio variant carries its own verified sizes")

# 5. the backwards troubleshooting entry is fixed
print("\n[troubleshooting]")
ck("come out too big" not in flat, "'Minis come out too big' removed")
ck(re.search(r"smaller than the sizes in the table", flat) is not None,
   "too-small entry present")
ck(re.search(r"larger than the sizes in the table", flat) is not None,
   "too-large entry present")
ck(re.search(r"Nine repeats of the petal sequence use exactly 18 stitches", flat)
   is not None, "petal-round closure explained")

# 6. safety
print("\n[safety]")
ck(re.search(r"not intended for children under 3", flat, re.I) is not None,
   "under-3 warning present")
ck(flat.count("baby-safe") <= 2 and "Do not market these as" in flat,
   "'baby-safe' appears only as a warning against the claim")
ck(re.search(r"EN 71", flat) is not None and re.search(r"ASTM F963", flat) is not None
   and re.search(r"CPSIA", flat) is not None, "standards named")
ck(re.search(r"embroider the eyes", flat, re.I) is not None,
   "embroidered-eye alternative offered")
ck(re.search(r"fully baby-safe", flat, re.I) is None, "'fully baby-safe' removed")

# 7. eyes
print("\n[eyes]")
ck(flat.count("3 stitches apart") >= 2, "Sunny and Waddle both set to 3 stitches apart")
ck(re.search(r"four stitches is about 14 mm", flat, re.I) is not None,
   "the reason for the change is explained")
ck(re.search(r"5 stitches apart", flat) is not None,
   "Spud's wider face keeps a wider spacing")

# 8. techniques actually listed
print("\n[techniques]")
need = ["Magic ring", "continuous spiral", "Invisible decreases",
        "Clusters worked into one stitch", "Slip stitch edging",
        "Oval base worked around a chain", "Sewing and embroidery"]
for t in need:
    ck(t in raw, f"listed: {t}")

# 9. quantities
print("\n[quantities]")
ck(re.search(r"roughly 8 m of yarn in total", flat) is not None, "yarn total corrected to ~8 m")
ck(re.search(r"about 3 g in total", flat) is not None, "fiberfill corrected to 3 g")
ck(not re.search(r"\b10 g\b", flat), "old 10 g fiberfill figure gone")
ck(not re.search(r"\b(9 g|12 g|7 g)\b", flat), "old per-toy yarn weights gone")

# 10. copy quality
print("\n[copy quality]")
ck("centre" not in raw, "no British 'centre' in a US-terms pattern")
ck("colour" not in raw, "no British 'colour'")
for typo in ("black ~6 g,white", "cmlong", "closesall", "oncethe", "thereis",
             "Foundatio n", "itagainst", "sewanything", "madefrom", "isstrictly",
             "&amp;", "~1.2 in):", "~1.5 in):"):
    ck(typo not in raw, f"typo removed: {typo!r}")
ck(raw.count("US E/4") >= 3, "hook size repeated in the summary table")

print("\n" + "=" * 70)
if fails:
    print(f"FAIL - {len(fails)} problem(s):")
    for f in fails:
        print("  -", f)
else:
    print(f"PASS - {n_rounds} published rounds verified; client file is clean")
sys.exit(1 if fails else 0)
