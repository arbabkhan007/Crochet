"""NS05 Little Duck — check each stated dimension against the pattern's own gauge."""
import math, sys
sys.path.insert(0, "ns05")
from pieces import (BODY, WING, WING_CLOSE, BEAK, BEAK_CHAIN, ALL,
                    MM_ST, MM_RND, CLAIM)

fails = []
def check(name, got, want, tol, unit="mm"):
    ok = abs(got - want) <= tol
    print(f"  {'OK  ' if ok else 'FAIL'} {name:<36} computed {got:8.2f} {unit:<4} "
          f"stated {want:8.2f} {unit}")
    if not ok:
        fails.append(f"{name}: {got:.1f} vs stated {want}")

def circ_d(n, w=MM_ST):        # diameter of a ring of n stitches
    return n * w / math.pi

R = MM_RND / MM_ST             # the pattern's own round-to-stitch ratio

print("=" * 78)
print("[1] HEIGHT - 'About 16 cm / 6.25 in tall'")
n = len(BODY)
lo, hi = (n - 1) * MM_RND, n * MM_RND
print(f"    {n} rounds; R1 is a flat MR disc and R23 gathers to 6 st, so the")
print(f"    honest range is {lo:.0f}-{hi:.0f} mm")
check("duck tall", hi, CLAIM["tall"], 8)
print(f"    6.25 in = {CLAIM['tall_in']*25.4:.1f} mm; 16 cm = {160/25.4:.2f} in  "
      f"(difference {abs(160-CLAIM['tall_in']*25.4):.1f} mm - rounding)")
body_h = 12 * MM_RND; head_h = 10 * MM_RND
print(f"    body R1-R12  = {body_h:.0f} mm;  head R14-R23 = {head_h:.0f} mm;  "
      f"head/body = {head_h/body_h:.2f}")

print("\n[2] WIDTH - '7.5 cm / 3 in wide'")
widest = max(s for _, _, s, _ in BODY)
check("duck wide at the widest", circ_d(widest), CLAIM["wide"], 3)
print(f"    3 in = {CLAIM['wide_in']*25.4:.1f} mm vs 7.5 cm = 75.0 mm")

print("\n[3] the shape the rounds actually describe")
waist = [s for l, _, s, _ in BODY if l in ("R12", "R13")]
print(f"    body R5-R9  full width : {widest} st = {circ_d(widest):.1f} mm")
print(f"    waist R12              : {waist[0]} st = {circ_d(waist[0]):.1f} mm")
print(f"    head R14-R19           : {widest} st = {circ_d(widest):.1f} mm")
print(f"    head is the SAME diameter as the body; the {waist[0]}-st waist is what")
print(f"    reads as a neck. Waist-to-body ratio {circ_d(waist[0])/circ_d(widest):.2f}.")

print("\n[4] TROUBLESHOOTING - 'at 10 mm per stitch this pattern finishes near 20 cm'")
w = 10.0
print(f"    scaling the round height with the stitch width keeps the pattern's own")
print(f"    ratio {MM_RND}/{MM_ST} = {R:.3f} -> round height {w*R:.2f} mm")
check("chunky-gauge duck", n * w * R, CLAIM["chunky_tall"], 10)

print("\n[5] 'For a smaller 10-12 cm duck, work ... in DK or velvet on a 3.0 mm hook'")
# DK (#3) worked tight on 3.0 mm; standard DK is 21-24 st / 10 cm on 3.75-4.5 mm
for label, st in (("DK #3 on 3.0 mm (tight)", 3.8), ("DK #3 on 3.0 mm (loose)", 4.2),
                  ("velvet #5 on 3.0 mm (tight)", 5.0), ("velvet #5 on 3.0 mm (loose)", 6.0)):
    h = n * st * R
    verdict = "in range" if CLAIM["dk_tall_lo"] - 5 <= h <= CLAIM["dk_tall_hi"] + 5 else \
              ("TOO SMALL" if h < CLAIM["dk_tall_lo"] else "TOO BIG")
    print(f"    {label:<30} {st:.1f} mm/st -> {h:5.1f} mm = {h/10:.1f} cm   {verdict}")
need = CLAIM["dk_tall_lo"] / n / R
print(f"    to reach 10 cm the round height must be {need:.2f} mm, i.e. "
      f"{need/R:.2f} mm/st - DK on 3.0 mm does not get there")
fails.append("DK on a 3.0 mm hook gives ~8 cm, not the stated 10-12 cm")

print("\n[6] BEAK - worked around ch 5")
# Rnd 1 layout: 3 plain | 3-st corner | 3 plain | 2-st corner
layout1 = [("side one plain", 3), ("corner A", 3), ("side two plain", 3), ("corner B", 2)]
# Rnd 2 = inc at sts 1, 4, 7, 10 -> one extra stitch in each of the four groups
layout2 = [(nm, c + 1) for nm, c in layout1]
for tag, layout in (("after Rnd 1 (11 st)", layout1), ("after Rnd 2 (15 st)", layout2)):
    caps = dict(layout)["corner A"] + dict(layout)["corner B"]
    side = dict(layout)["side one plain"]
    width = circ_d(caps)
    length = width + side * MM_ST
    print(f"    {tag:<22} caps {caps} st -> {width:.1f} mm wide; "
          f"{side} st sides -> {length:.1f} mm long")
    if "Rnd 2" in tag:
        beak_len = length
print(f"    sum of the Rnd 2 groups = {sum(c for _, c in layout2)} (must be 15)")
if sum(c for _, c in layout2) != 15:
    fails.append("beak Rnd 2 group model does not reproduce 15")
print(f"    beak is {beak_len/circ_d(widest)*100:.0f}% of the head width "
      f"({circ_d(widest):.1f} mm)")

print("\n[7] WINGS")
wing_d = circ_d(max(s for _, _, s, _ in WING))
print(f"    12-st flat disc = {wing_d:.1f} mm across; closing {WING_CLOSE} sc through")
print(f"    both layers leaves a half-disc about {wing_d:.1f} x {wing_d/2:.1f} mm")
print(f"    placed across R6-R9 = {4*MM_RND:.0f} mm tall - the piece fits the band")

print("\n[8] EYES - 'about 7-8 stitches apart'")
for g in (CLAIM["eye_gap_lo"], CLAIM["eye_gap_hi"]):
    span = g * MM_ST
    print(f"    {g} st = {span:.0f} mm apart on a {circ_d(widest):.1f} mm head -> "
          f"{(circ_d(widest)-span)/2:.1f} mm from each eye to the edge")

print("\n[9] STUFFING VOLUME")
def vol(rows, lo, hi):
    return sum(math.pi*(circ_d(s)/2)**2*MM_RND
               for i, (_, _, s, _) in enumerate(rows) if lo <= i <= hi)/1000
body_v = vol(BODY, 0, 11); head_v = vol(BODY, 13, 22)
print(f"    body R1-R12  {body_v:6.1f} cm3")
print(f"    head R14-R23 {head_v:6.1f} cm3")
print(f"    TOTAL        {body_v+head_v:6.1f} cm3   (wings and beak are not stuffed)")
for d in (30, 55, 80):
    print(f"    at {d} kg/m3 -> {(body_v+head_v)*d/1000:5.1f} g")
print(f"    the pattern states no quantity")

print("\n[10] YARN - 'body yarn ... yellow, ~55-75 g'")
counts = {}
for name, (rows, copies) in ALL.items():
    extra = WING_CLOSE if name == "wing" else 0
    counts[name] = copies * (sum(s for _, _, s, _ in rows) + extra)
total_st = sum(counts.values())
for nm, c in counts.items():
    print(f"    {nm:<12} {c:>4} st")
print(f"    {'TOTAL':<12} {total_st:>4} st")
m = total_st * MM_ST * 3 / 1000        # ~3x the stitch width per stitch
print(f"    at 3x the stitch width: {m:.1f} m of yarn")
for label, per100 in (("chenille #6 (e.g. 266 m / 300 g)", 88.7),
                      ("a plusher 60 m / 100 g chenille", 60.0)):
    g = m / per100 * 100
    print(f"    {label:<36} {g:5.1f} g  (+40% for tails/waste = {g*1.4:5.1f} g)")
print(f"    stated {CLAIM['yarn_body_lo']:.0f}-{CLAIM['yarn_body_hi']:.0f} g for the body alone")
fails.append(f"body yarn {CLAIM['yarn_body_lo']:.0f}-{CLAIM['yarn_body_hi']:.0f} g is "
             f"about {CLAIM['yarn_body_lo']/(m/88.7*100*1.4):.1f}x the {m/88.7*100*1.4:.0f} g actually used")

print("\n[11] swatch")
print(f"    'measure a 12-stitch swatch' = {CLAIM['swatch_st']*MM_ST:.0f} mm wide - a "
      f"usable 10 cm swatch")

print("\n" + "=" * 78)
if fails:
    print(f"{len(fails)} claim(s) do not survive the arithmetic:")
    for f in fails:
        print("  -", f)
else:
    print("every checked claim holds")
