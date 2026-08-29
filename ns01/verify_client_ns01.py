"""Final gate on the corrected NS01 — parses the delivered client markdown."""
import re, pathlib, math, sys
sys.path.insert(0, "ns01")
from verify_stitches import eval_round, oval_foundation
from pieces import MM_ST, MM_RND

T = "NS01_Hamish_the_Highland_Cow_CLIENT.md"
md = pathlib.Path(T).read_text()
plain = re.sub(r"[*_`>]", "", md)
errors = []

print("[1] every round row in the delivered file")
rows = re.findall(r'^\|\s*(Rnd\s*\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
print(f"    round rows parsed: {len(rows)}")
prev = 0
bad = 0
for label, instr, stated in rows:
    n = int(re.search(r'\d+', label).group()); instr = instr.strip(); stated = int(stated)
    if n == 1:
        prev = 0
    if "2nd ch from hook" in instr:            # oval worked around a chain
        p = oval_foundation(9)["total"]; c = 0
    else:
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
if len(rows) != 80:
    errors.append(f"expected 80 round rows (16+8+19+4+16+3+7+7), got {len(rows)}")

def diam(n): return n * MM_ST / math.pi

print("\n[2] geometry claims restated in the file")
for name, got, want, tol in [
    ("mm per stitch",            50/11,           4.55, 0.01),
    ("mm per round",             50/12,           4.17, 0.01),
    ("head width 70 mm",         diam(48),        70,   1.0),
    ("head height 67 mm",        16*MM_RND,       67,   1.0),
    ("height-to-width 0.96",     16*MM_RND/diam(48), 0.96, 0.02),
    ("body width 70 mm",         diam(48),        70,   1.0),
    ("body height 79 mm",        19*MM_RND,       79,   1.0),
    ("sitting 150 mm",           19*MM_RND+16*MM_RND, 150, 6),
    ("leg 67 mm",                16*MM_RND,       67,   1.0),
    ("neck ring 26 mm",          diam(18),        26,   1.0),
    ("eyes 32 mm apart",         7*MM_ST,         32,   1.0),
]:
    ok = abs(got - want) <= tol
    print(f"    {'OK  ' if ok else 'FAIL'} {name:<26} computed {got:8.3f}  stated {want}")
    if not ok:
        errors.append(name)

print("\n[3] MUZZLE MUST FIT — the defect this file corrects")
mz = re.findall(r'^\|\s*Rnd\s*(\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
muzzle = mz[16:24]                      # muzzle table follows the 16-round head
rim_st = int(muzzle[-1][2])
face_st = max(int(s) for _, _, s in muzzle)
rim, face = diam(rim_st), diam(face_st)
avail = (16 - 10) * MM_RND
print(f"    muzzle face {face_st} st = {face:.1f} mm;  rim {rim_st} st = {rim:.1f} mm")
print(f"    rim needs {rim/MM_RND:.1f} rounds;  Rnd 10 -> Rnd 16 offers {avail:.1f} mm "
      f"= {avail/MM_RND:.1f} rounds")
# A crochet rim sewn onto a sphere is eased in, so a small overrun is normal
# sewing, not a defect. 1.5 mm here is ~4.5 mm of seam circumference over an
# ~79 mm seam. The original rim overran by 9.7 mm (39%) - that was the defect.
EASE = 1.5
over = rim - avail
ok = over <= EASE
print(f"    overrun {over:+.2f} mm ({over/avail*100:+.1f}% of the space) = "
      f"{math.pi*over:.1f} mm to ease around a {math.pi*avail:.1f} mm seam; "
      f"allowance {EASE} mm")
print(f"    {'OK  ' if ok else 'FAIL'} rim fits between the eyes and the chin")
if not ok:
    errors.append(f"muzzle rim {rim:.1f} mm overruns {avail:.1f} mm of head by {over:.1f} mm")
print(f"    (the original 24-st rim overran by "
      f"{24*MM_ST/math.pi - avail:.1f} mm = {(24*MM_ST/math.pi-avail)/avail*100:.0f}%)")
seam_centre = diam(24)      # head at Rnd 13
print(f"    {'OK  ' if rim <= seam_centre else 'FAIL'} rim {rim:.1f} mm vs head width at "
      f"the seam centre (Rnd 13) {seam_centre:.1f} mm")
if rim > seam_centre:
    errors.append("rim wider than the head at the seam centre")
for claim, val in (("35 mm", face), ("26 mm", rim)):
    if claim not in plain:
        errors.append(f"muzzle {claim} figure missing"); print(f"    FAIL '{claim}' not stated")
print(f"    file states the face as 35 mm and the rim as 26 mm: "
      f"{'35 mm' in plain and '26 mm' in plain}")
if "Rnd 15–16" not in md:
    errors.append("pinning rounds not stated")

print("\n[4] leg geometry is disclosed, not hidden")
# search the markup-stripped text: bold inside a phrase breaks literal matching
for need in ["55° from vertical", "68–70°", "front pair only to Rnd 10", "42 mm"]:
    if need not in plain:
        errors.append(f"leg note missing '{need}'")
    print(f"    {'OK  ' if need in plain else 'FAIL'} states {need!r}")
print(f"    check: front join {9*MM_RND:.1f} mm up, leg {16*MM_RND:.1f} mm -> "
      f"{math.degrees(math.acos(9*MM_RND/(16*MM_RND))):.0f} deg")
print(f"    check: back join {6*MM_RND:.1f} mm up -> "
      f"{math.degrees(math.acos(6*MM_RND/(16*MM_RND))):.0f} deg")
print(f"    check: 10-round leg = {10*MM_RND:.1f} mm")

print("\n[5] materials figures stated in the file")
def vol(rows, copies=1):
    return copies*sum(math.pi*(diam(n)/2)**2*MM_RND for _,_,n,_ in rows)/1000
from pieces import HEAD, MUZZLE as MZ_ORIG, BODY, LEG, EAR_OUTER, HORN
mz_rows = [(f"Rnd {i+1}", "", int(s), "") for i, (_, _, s) in enumerate(muzzle)]
tot = vol(HEAD)+vol(BODY)+vol(LEG,4)+vol(EAR_OUTER,2)+vol(HORN,2)+vol(mz_rows)
print(f"    stuffed volume {tot:.0f} cm3 -> {tot*55/1000:.0f}-{tot*80/1000:.0f} g "
      f"at a firm pack")
for pat, label in ((r'fiber fill, about \*\*(\d+) g\*\*', "stuffing"),
                   (r'whole cow uses about \*\*(\d+) g\*\*', "yarn A used")):
    m = re.search(pat, md)
    print(f"    {label}: {m.group(1) if m else 'NOT FOUND'} g")
    if not m:
        errors.append(f"{label} figure not found")
m = re.search(r'about \*\*(\d+) g\*\*', md)
for v in ("50 g", "80 g", "160 g"):
    if v not in md:
        errors.append(f"three-sizes table missing {v}")
print(f"    three-sizes yarn column present: "
      f"{all(v in md for v in ('50 g','80 g','160 g'))}")

print("\n[6] safety section")
print(f"    'fully baby-safe' present: {'fully baby-safe' in plain.lower()}")
if "fully baby-safe" in plain.lower():
    errors.append("'fully baby-safe' present")
for need in ["ASTM F963", "pull-test", "small parts", "under three"]:
    ok = need.lower() in plain.lower()
    print(f"    {'OK  ' if ok else 'FAIL'} '{need}' present")
    if not ok:
        errors.append(f"safety section missing '{need}'")

print("\n[7] technique coverage — every technique the pattern uses is taught")
for tech in ["MAGIC RING", "SPIRAL", "INVISIBLE DECREASE", "BACK LOOP ONLY",
             "AROUND A CHAIN", "LARK'S HEAD", "LADDER STITCH"]:
    ok = tech.lower() in plain.lower()
    print(f"    {'OK  ' if ok else 'FAIL'} teaches {tech}")
    if not ok:
        errors.append(f"techniques section missing {tech}")

print("\n[8] client-readiness")
for w in [r"\bFAIL\b", "mismatch", "verify", "ns01/", "TODO", "CHANGES FROM",
          "correction", "solver", "&amp;", "fibre fill", "yourfabric", "oncethe",
          "thereis", "Foundatio n", "afew degrees", "about40", "forwardand",
          "thehooves", "headfabric", "makethe", "itagainst", "sewanything",
          "hoovesflat", "madefrom", "isstrictly", "under theneck", "26mm across",
          "seat,so", "70x 67", "=colour", "Colourways", "centred", "Centre it"]:
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
print(f"PASSED - {len(rows)} rounds, geometry, muzzle fit, legs, materials, "
      f"safety, techniques, readiness")
