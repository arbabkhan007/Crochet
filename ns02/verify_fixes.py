"""Corrected checks for the two figures I got wrong, plus the missing-content audit."""
import math, re

MM_ST, MM_RND = 3.5, 3.2

print("="*72); print("A. WING SCALLOPS — counted properly (label excluded)"); print("="*72)
scal = {"scallop 1 (middle)": "sc, hdc, dc, picot, dc, hdc, sc",
        "scallop 2":           "sc, hdc, picot, hdc, sc",
        "scallop 3":           "sc, hdc, picot, hdc, sc"}
OPS = r'(?:sl st|sc|hdc|dc|picot)'
for k, v in scal.items():
    toks = re.findall(OPS, v)
    pic  = toks.count("picot")
    print(f"  {k:<20} {len(toks):>2} sts  {pic} picot  {toks}")
print("  -> all three have exactly ONE picot. They differ in WIDTH (7 vs 5 vs 5)")
print("     and in the tallest stitch used (dc in the middle, hdc at the sides).")
print("     So the middle scallop is bigger. That is probably deliberate - it is")
print("     the wing tip - but the pattern never says so.")

print(); print("="*72); print("B. STUFFING — units corrected"); print("="*72)
def sph_cm3(d_mm): return (4/3)*math.pi*(d_mm/2)**3 / 1000     # mm3 -> cm3
pip  = sph_cm3(40)*1.15
bram = sph_cm3(31)*0.8 + sph_cm3(26)*0.5
print(f"  Pip (40 mm, overstuffed x1.15)   {pip:6.1f} cm3")
print(f"  Bramble (body 31 + head 26 mm)   {bram:6.1f} cm3")
print(f"  Boo (open bell, never stuffed)   {0:6.1f} cm3")
tot = pip + bram
print(f"  total                            {tot:6.1f} cm3")
for dens in (30, 60):
    print(f"  at {dens} kg/m3 ({dens/1000:.3f} g/cm3) -> {tot*dens/1000:.1f} g")
print(f"  stated 15 g -> about {15/(tot*45/1000):.1f}x what the trio can hold "
      f"(at 45 kg/m3 = {tot*45/1000:.1f} g)")

print(); print("="*72); print("C. BOO'S HEIGHT — does 4.8 cm survive?"); print("="*72)
body = 12*MM_RND
print(f"  body R1-R12            = {body:.1f} mm")
for extra in (1, 2, 3):
    print(f"  + {extra} rnd of hem depth = {body + extra*MM_RND:.1f} mm")
print(f"  stated 48 mm -> needs about {(48-body)/MM_RND:.1f} extra rounds of hem depth.")
print("  Plausible, but the pattern never states the hem's depth, and the WIDTH")
print(f"  figure (29 mm) is the 24-st body tube ({24*MM_ST/math.pi:.1f} mm) while the")
print("  48-st hem flares well past that. Boo's width and height are measured on")
print("  different parts of the toy.")

print(); print("="*72); print("D. MISSING CONTENT — referenced but never given"); print("="*72)
claims = [
 ("'HOW IT COMES TOGETHER / The core techniques...'",
  "the technique entries themselves", "section is a header with no content"),
 ("intro: 'the picots, split rounds and needle sculpting'",
  "any needle-sculpting instructions", "Pip's 65 cm tail is reserved for sculpting"),
 ("Pip: 'FO leaving a 25 in / 65 cm tail for sculpting'",
  "how to use that tail", "no sculpting step anywhere in the pattern"),
 ("Troubleshooting: 'Ribs vanish ... pull each rib firmly'",
  "any rib instructions", "Pip has no sculpting/rib step"),
 ("heading: 'Pip - stem cone, tendril & leaf'",
  "tendril pattern, leaf pattern", "only the 5-round cone is given"),
 ("Materials: 'sage green ~4 g (stem, tendril, leaf)'",
  "tendril and leaf to use it on", "yarn budgeted for pieces that do not exist"),
 ("Materials: '2 pairs of 6 mm' safety eyes",
  "an insertion step", "Bramble closes at R16; Boo's eyes are noted at R8-9"),
 ("Materials: 'add a third pair' for Pip's optional face",
  "size, placement, or the face itself", "'optional face' is never described"),
 ("'Polyester fibre fill'", "US spelling", "pattern declares US crochet terms"),
]
for ref, missing, note in claims:
    print(f"  MISSING: {missing}")
    print(f"           referenced by: {ref}")
    print(f"           -> {note}")

print(); print("="*72); print("E. THINGS THAT ARE ACTUALLY FINE"); print("="*72)
print(f"  Boo hem  : 6 repeats x 4 sts = 24, closes Rnd 12 exactly; 48 sts produced")
print(f"  Bat wing : slip groups 2/3/2/2 = 9 + 3 shell sts = 12, consumes Row 2 exactly")
print(f"  Hat brim : 20 sts -> {20*MM_ST:.0f} mm around = {20*MM_ST/math.pi:.1f} mm across (stated 22 mm)")
print(f"  R8 eyes  : [11 sc, inc] x2 on 24 sts -> incs 13 sts apart, symmetric")
print(f"  Garland  : 450 ch x ~4 mm = {450*4/1000:.1f} m = {450*4/1000/0.3048:.1f} ft (stated 6 ft)")
print(f"  Wingspan : 2 x 42 + 33 = {2*42+33} mm (stated 11.5 cm)")
