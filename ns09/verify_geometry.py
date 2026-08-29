"""NS09 Shelby — the size claims all follow from one number: 24 stitches."""
import math, sys
sys.path.insert(0, "ns09")
from pieces import SHELL, UNDERSIDE, BUMPS_ROW, ALL, MM_ST, MM_RND, CLAIM, BUMPS_CLAIM

fails = []
def check(name, got, want, tol, unit="mm"):
    ok = abs(got - want) <= tol
    print(f"  {'OK  ' if ok else 'FAIL'} {name:<36} computed {got:8.2f} {unit:<4} "
          f"stated {want:8.2f} {unit}")
    if not ok:
        fails.append(f"{name}: {got:.1f} vs stated {want}")

def diam(n): return n * MM_ST / math.pi

RIM = SHELL[-1][2]
D = diam(RIM)

print("=" * 78)
print("[1] the number everything follows from")
print(f"    shell and underside both finish at {RIM} st")
print(f"    {RIM} st x {MM_ST} mm = {RIM*MM_ST:.1f} mm circumference -> {D:.2f} mm across")

print("\n[2] 'About 6 cm across the flippers, 4.5 cm long and 2 cm deep'")
print("    the head and flippers are clusters worked into ONE stitch each, so they")
print("    can only protrude about the height of their tallest stitch:")
hdc_h = MM_RND * 1.6
print(f"    sc ~{MM_RND:.1f} mm tall, hdc ~{hdc_h:.1f} mm -> a bump stands "
      f"~{hdc_h:.0f} mm proud")
across = D + 2*hdc_h
length = D + hdc_h
print(f"    across the flippers = {D:.1f} + 2 x {hdc_h:.1f} = {across:.1f} mm")
print(f"    head to tail        = {D:.1f} + 1 x {hdc_h:.1f} = {length:.1f} mm")
check("across the flippers", across, CLAIM["across_flippers"], 4)
check("length", length, CLAIM["length"], 4)
check("depth (6 shell rounds)", len(SHELL)*MM_RND, CLAIM["depth"], 2)
print(f"    => the stated {CLAIM['across_flippers']/10:.0f} cm / {CLAIM['length']/10:.1f} cm "
      f"are {CLAIM['across_flippers']/across:.2f}x and {CLAIM['length']/length:.2f}x "
      f"the real figures; only the depth is right")
need = CLAIM["across_flippers"] - 2*hdc_h
print(f"    for a true {CLAIM['across_flippers']/10:.0f} cm span the disc must be "
      f"{need:.1f} mm across = {need*math.pi/MM_ST:.1f} stitches")

print("\n[3] bump placement — is the turtle symmetrical?")
runs = BUMPS_CLAIM["plain_runs"]
pos, p = [], 0
for i, r in enumerate(runs):
    p += r
    if i < 5:
        pos.append(p + 1)      # the stitch the bump is worked into
        p += 1
print(f"    plain runs {runs}; the 5 bumps sit on stitches {pos}")
gaps = [pos[i+1]-pos[i] for i in range(len(pos)-1)] + [RIM - pos[-1] + pos[0]]
print(f"    bump-to-bump gaps {gaps} (sum {sum(gaps)})")
print(f"    angles from the head: "
      f"{[round((q-pos[0])*360/RIM) for q in pos]}")
mir = [round((q-pos[0])*360/RIM) for q in pos]
print(f"    right side {mir[1]} deg / left side {360-mir[-1]} deg; "
      f"asymmetry {abs(mir[1]-(360-mir[-1]))} deg = "
      f"{abs(mir[1]-(360-mir[-1]))/360*RIM:.1f} stitch")
if abs(mir[1]-(360-mir[-1])) > 360/RIM*1.5:
    fails.append("bump placement is not symmetrical")

print("\n[4] the join — do the two edges have the same stitch count?")
print(f"    shell rim: {RIM} st")
print(f"    underside outer round (Rnd 5): {BUMPS_ROW[0][2]} st")
print(f"    but the {BUMPS_ROW[0][2]} stitches sit in only {RIM} anchor positions "
      f"({sum(runs)} plain + 5 clusters)")
print(f"    -> the pattern says 'line up the rim of the shell with the outer edge of")
print(f"       the disc' without saying which count to match. {RIM} to "
      f"{BUMPS_ROW[0][2]} will not pair 1:1.")
fails.append(f"join not specified: shell {RIM} st vs underside outer round "
             f"{BUMPS_ROW[0][2]} st")

print("\n[5] eyes on the head bump")
eye_span = 2 * MM_ST
print(f"    '2 stitches apart' = {eye_span:.1f} mm centre to centre")
print(f"    the head bump is (sc, hdc, hdc, sc) in ONE stitch: {4*MM_ST:.1f} mm of "
      f"stitch width fanned into a loop about {4*MM_ST/2:.0f}-{4*MM_ST:.0f} mm across")
print(f"    a 4 mm safety eye needs a washer of roughly 6-7 mm")
print(f"    -> eyes at {eye_span:.1f} mm sit at the very edge of the bump, and the")
print(f"       washers are unlikely to fit inside it")

print("\n[6] stuffing volume")
cap_h = 4 * MM_RND                       # Rnds 1-4 form the cap
rim_h = (len(SHELL) - 4) * MM_RND        # Rnds 5-6 are the rim
a = D / 2
cap_v = (math.pi * cap_h / 6) * (3*a*a + cap_h*cap_h)
rim_v = math.pi * a * a * rim_h
vol = (cap_v + rim_v) / 1000
print(f"    spherical cap h={cap_h:.1f} mm over a {D:.1f} mm rim = {cap_v/1000:.1f} cm3")
print(f"    + rim {rim_h:.1f} mm tall = {rim_v/1000:.1f} cm3;  total {vol:.1f} cm3")
for d in (30, 55, 80):
    print(f"    at {d} kg/m3 -> {vol*d/1000:.2f} g   (pattern states {CLAIM['polyfill']:.0f} g)")

print("\n[7] yarn")
st = sum(n for _,_,n,_ in SHELL) + sum(n for _,_,n,_ in UNDERSIDE) + BUMPS_ROW[0][2]
for per in (3.0, 4.0, 4.5):
    m = st * MM_ST * per / 1000
    print(f"    {st} st x {MM_ST} x {per} = {m:4.1f} m -> {m/250*100:4.2f} g "
          f"at 250 m/100 g DK")
print(f"    pattern states {CLAIM['shell_yarn']:.0f} g shell + {CLAIM['body_yarn']:.0f} g "
      f"body = {CLAIM['shell_yarn']+CLAIM['body_yarn']:.0f} g, and 'under 10 g' in section 5")

print("\n[8] abbreviations listed but never used")
import re, pathlib
md = pathlib.Path("/dev/stdin")  # not read here; the gate checks the delivered file
for term, instrs in (("dec", [i for _, i, _, _ in SHELL+UNDERSIDE+BUMPS_ROW]),
                     ("ch",  [i for _, i, _, _ in SHELL+UNDERSIDE+BUMPS_ROW])):
    used = any(re.search(rf'(?<![a-z]){term}(?![a-z])', x) for x in instrs)
    print(f"    '{term}' used in any round: {used}")

print("\n" + "=" * 78)
if fails:
    print(f"{len(fails)} claim(s) do not survive the arithmetic:")
    for f in fails:
        print("  -", f)
else:
    print("every checked claim holds")
