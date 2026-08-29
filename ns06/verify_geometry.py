"""NS06 Momo — the loaf shape is set entirely by the oval base, so check that first."""
import math, sys
sys.path.insert(0, "ns06")
from pieces import BODY, EAR, TAIL, MM_ST, MM_RND, FOUNDATION, CLAIM

fails = []
def check(name, got, want, tol, unit="mm"):
    ok = abs(got - want) <= tol
    print(f"  {'OK  ' if ok else 'FAIL'} {name:<38} computed {got:8.2f} {unit:<4} "
          f"stated {want:8.2f} {unit}")
    if not ok:
        fails.append(f"{name}: {got:.1f} vs stated {want}")

def circle_diam(n_st):
    return n_st * MM_ST / math.pi

def oval_dims(cap_st, side_st):
    """The two end caps together form one full circle, so the oval's width is
    the diameter of that circle. Length = width + one straight side."""
    w = circle_diam(2 * cap_st)
    return w, w + side_st * MM_ST

def ellipse_area(perim, k):
    """Semi-axes of an ellipse with aspect ratio k = a/b and the given perimeter."""
    lo, hi = 0.01, 500.0
    for _ in range(200):
        b = (lo + hi) / 2
        a = k * b
        P = math.pi * (3*(a+b) - math.sqrt((3*a+b)*(a+3*b)))
        if P < perim: lo = b
        else:         hi = b
    b = (lo + hi) / 2
    return math.pi * (k*b) * b

print("=" * 78)
print("[1] the oval base — where do the caps and sides end up?")
print(f"    ch {FOUNDATION}: sides are N-3 = {FOUNDATION-3} sts, caps start at 3")
print("    the pattern adds 3 sts per cap and 1 at the round start each round,")
print("    so the caps grow 3 per round and the long sides never change:\n")
cap, side = 3, FOUNDATION - 3
base_row = None
for rnd in range(1, 5):
    stated = BODY[rnd-1][2]
    if rnd > 1:
        cap += 3
    total = 2*cap + 2*side
    ok = total == stated
    w, l = oval_dims(cap, side)
    print(f"    Rnd {rnd}: caps {cap:>2}+{cap:<2} sides {side}+{side}  = {total:>3} st "
          f"(stated {stated}) {'OK' if ok else 'MISMATCH'}   "
          f"-> {l:5.1f} long x {w:5.1f} wide")
    if not ok:
        fails.append(f"oval Rnd {rnd}: {total} vs stated {stated}")
    base_row = (cap, side, w, l)
cap, side, W, L = base_row

print("\n[2] 'The base is an oval about 75 mm long and 55 mm across'")
check("base length", L, CLAIM["base_length"], 2)
check("base width",  W, CLAIM["base_width"],  2)
print(f"    cross-check: a {BODY[3][2]}-st CIRCLE is {circle_diam(BODY[3][2]):.1f} mm across.")
print(f"    An oval made from the same stitches must be NARROWER than that circle,")
print(f"    so a {BODY[3][2]}-st oval cannot be {CLAIM['base_width']:.0f} mm across.")
if W < CLAIM["base_width"] - 2:
    fails.append(f"base width {W:.1f} mm cannot reach the stated {CLAIM['base_width']:.0f} mm")

print("\n[3] height: 'the walls add only ten rounds ... about 43 mm tall'")
wall_first = next(i for i, r in enumerate(BODY) if "BLO" in r[1]) + 1
walls = len(BODY) - wall_first + 1
H = walls * MM_RND
print(f"    BLO Rnd {wall_first} through Rnd {len(BODY)} = {walls} rounds x {MM_RND} "
      f"= {H:.1f} mm")
check("wall height", H, CLAIM["wall_height"], 1.0)

print("\n[4] THE LOAF PREMISE: 'genuinely wider than it is tall'")
print(f"    length {L:.1f} mm  x  width {W:.1f} mm  x  height {H:.1f} mm")
ratio = W / H
print(f"    width / height = {ratio:.2f}  ->  "
      f"{'WIDER than tall' if ratio > 1 else 'TALLER THAN WIDE - the opposite of a loaf'}")
if ratio <= 1:
    fails.append(f"width {W:.1f} mm < height {H:.1f} mm: the loaf is taller than it is wide")
check("finished length (7.5 cm)", L, CLAIM["length"], 3)
check("finished width (5.5 cm)",  W, CLAIM["width"],  3)
check("finished height (4.5 cm)", H, CLAIM["height"], 3)

print("\n[5] what the base would have to be to make the stated size true")
for target_w, target_l in ((CLAIM["width"], CLAIM["length"]),):
    need_caps = target_w * math.pi / (2 * MM_ST)      # width = 2*cap*MM_ST/pi
    print(f"    for a {target_w:.0f} mm width each cap needs {need_caps:.1f} sts")
    print(f"    with {side}-st sides, length would then be "
          f"{target_w + side*MM_ST:.1f} mm (stated {target_l:.0f} mm)")
print("    rounding to a clean repeat: caps of 18 ->")
w48, l48 = oval_dims(18, side)
tot48 = 2*18 + 2*side
print(f"      {tot48} st base = {l48:.1f} long x {w48:.1f} wide;  "
      f"width/height = {w48/H:.2f}")

print("\n[6] eyes: 'about 7 stitches apart, low and wide'")
eye = 7 * MM_ST
print(f"    7 st = {eye:.1f} mm")
print(f"    as a share of body width: {eye/W*100:.0f}% on the {W:.1f} mm base as written, "
      f"{eye/w48*100:.0f}% on the {w48:.1f} mm base")

print("\n[7] stuffing volume (each round as an ellipse of the base's aspect ratio)")
k = L / W
vol = sum(ellipse_area(n * MM_ST, k) * MM_RND for _, _, n, _ in BODY) / 1000
print(f"    base aspect ratio {k:.2f};  total {vol:.1f} cm3")
for d in (30, 55, 80):
    print(f"    at {d} kg/m3 -> {vol*d/1000:5.1f} g     (pattern states {CLAIM['polyfill']:.0f} g)")
print(f"    {CLAIM['polyfill']:.0f} g implies {CLAIM['polyfill']/vol*1000:.0f} kg/m3")
vol48 = sum(ellipse_area(n * MM_ST, l48/w48) * MM_RND
            for n in (18,24,30,36,42,48,48,48,48,48,42,36,30,24,18,12,6)) / 1000
print(f"    the 48-st base version holds {vol48:.0f} cm3 -> "
      f"{vol48*55/1000:.1f}-{vol48*80/1000:.1f} g")

print("\n[8] yarn")
st = sum(n for _,_,n,_ in BODY) + 2*sum(n for _,_,n,_ in EAR) + sum(n for _,_,n,_ in TAIL)
st48 = sum((18,24,30,36,42,48,48,48,48,48,42,36,30,24,18,12,6)) \
       + 2*sum(n for _,_,n,_ in EAR) + sum(n for _,_,n,_ in TAIL)
for label, n in (("as written", st), ("48-st base", st48)):
    for per in (3.0, 4.0, 4.5):
        m = n * MM_ST * per / 1000
        print(f"    {label:<12} {n:>4} st x {MM_ST} x {per} = {m:5.1f} m "
              f"-> {m/190*100:4.1f} g at 190 m/100 g")
print(f"    pattern states {CLAIM['yarn']:.0f} g")

print("\n[9] ears: the pattern's own consumption claim")
print("    'Each row consumes exactly what the row before produced: 5 stitches into")
print("     Row 2 (2 + 1 + 2), then 3 stitches into Row 3 (2 + 1).'")
print(f"    Row 1 = 5 st; Row 2 dec,sc,dec consumes {2+1+2} produces {3}; "
      f"Row 3 dec,sc consumes {2+1} produces {2} -> {'CORRECT' if 2+1+2==5 and 2+1==3 else 'WRONG'}")

print("\n" + "=" * 78)
if fails:
    print(f"{len(fails)} claim(s) do not survive the arithmetic:")
    for f in fails:
        print("  -", f)
else:
    print("every checked claim holds")
