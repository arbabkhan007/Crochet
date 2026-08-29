"""NS03 Axel — check every stated dimension and claim against the round tables.

Prints the arithmetic for each claim rather than asserting a label.
"""
import math, sys
sys.path.insert(0, "ns03")
from pieces import BODY, ARM, FOOT, GILL, ALL, MM_ST, MM_RND
from verify_stitches import eval_seq

fails = []
def check(name, got, want, tol, unit="mm"):
    ok = abs(got - want) <= tol
    print(f"  {'OK  ' if ok else 'FAIL'} {name:<42} computed {got:8.1f} {unit}  "
          f"stated {want:8.1f} {unit}  (tol {tol})")
    if not ok:
        fails.append(name)
    return ok

def diam(n_st):
    """Circumference of n stitches -> stuffed diameter."""
    return n_st * MM_ST / math.pi

def vol_cm3(rounds, first=1, last=None):
    """Sum of discs: each round is a 4.3 mm tall disc of that round's diameter."""
    last = last or len(rounds)
    v = 0.0
    for _, _, n, _ in rounds[first-1:last]:
        r = diam(n) / 2
        v += math.pi * r * r * MM_RND
    return v / 1000.0

print("=" * 70)
print("[1] gauge statement: '36 sc around measures about 52 mm in diameter'")
print(f"    36 st x {MM_ST} mm = {36*MM_ST:.1f} mm circumference")
check("head diameter from 36 st", diam(36), 52, 1.0)

print("\n[2] 'head is a true sphere at 52 mm wide x 51.6 mm tall'")
print(f"    head = R1..R12 = 12 rounds x {MM_RND} = {12*MM_RND:.1f} mm tall")
check("head height", 12*MM_RND, 51.6, 0.6)
check("head width vs height (sphere test)", diam(36), 12*MM_RND, 1.0)

print("\n[3] 'about 11.5 cm tall seated'")
print(f"    top of head to body bottom = R1..R26 = 26 rounds x {MM_RND}")
check("seated height", 26*MM_RND, 115, 6)

print("\n[4] 'a 4.3 cm tail' / 'the tail runs R27-R36, ten rounds ~43 mm'")
tail_rounds = len([r for r in BODY if r[0] in
                   ("R27","R28","R29","R30","R31","R32","R33","R34","R35","R36")])
print(f"    R27..R36 inclusive = {tail_rounds} rounds x {MM_RND} = {tail_rounds*MM_RND:.1f} mm")
check("tail length", tail_rounds*MM_RND, 43, 1.0)

print("\n[5] 'about 12 cm wide gill tip to gill tip'")
gill_len = len(GILL) * MM_RND
print(f"    gill = {len(GILL)} rounds x {MM_RND} = {gill_len:.1f} mm long")
print(f"    head {diam(36):.1f} mm + 2 x gill {gill_len:.1f} mm")
bare = diam(36) + 2*gill_len
check("gill span, bare stitches", bare, 120, 1.0)
for halo in (3, 5, 8):
    print(f"    + {halo} mm teased fluff per side -> {(bare + 2*halo)/10:.1f} cm")
need = (120 - diam(36))/2
print(f"    to reach 12 cm each gill must stand {need:.1f} mm clear of the head, "
      f"i.e. {need-gill_len:.1f} mm of fluff on a {gill_len:.1f} mm gill")

print("\n[6] 'six stitches spans about 26 mm on the 52 mm head'")
print(f"    6 st x {MM_ST} = {6*MM_ST:.1f} mm;  that is {6*MM_ST/diam(36)*100:.0f}% of head width")
check("eye spacing", 6*MM_ST, 26, 2.0)

print("\n[7] neck width at R13 (18 st)")
print(f"    18 st -> {diam(18):.1f} mm diameter = {diam(18)/diam(36)*100:.0f}% of the head")

print("\n[8] tail fin: 'the ridge holds 10 stitches and 5 scallops need exactly 10'")
print(f"    flattened tail R27..R36 = {tail_rounds} rows; side edge of sc rows takes")
print(f"    ~1 st per row -> {tail_rounds} ridge stitches along one side")
check("ridge stitches vs scallop demand", tail_rounds, 5*2, 0)
print(f"    each scallop = 5 dc in 1 st + sl st in next = 2 sts; 5 scallops = 10 sts")
print(f"    ridge pitch = {tail_rounds*MM_RND/tail_rounds:.1f} mm/stitch over "
      f"{tail_rounds*MM_RND:.1f} mm of tail")

print("\n[9] TROUBLESHOOTING neck alternative — the pattern says:")
print("    'work R13 as [7 sc, inc] x2, 2 sc (20)' then 'change R14 to [4 sc, inc] x4 (24)'")
prev = 18                                   # R12 leaves 18 stitches
for label, instr, stated in (("R13 alt", "[7 sc, inc] x2, 2 sc", 20),
                             ("R14 alt", "[4 sc, inc] x4", 24)):
    c, p = eval_seq(instr, prev)
    ok = (p == stated)
    print(f"    {'OK  ' if ok else 'FAIL'} {label}: {instr!r}")
    print(f"          from {prev} available -> consumes {c}, produces {p}, "
          f"pattern states ({stated})")
    if not ok:
        fails.append(f"{label} produces {p}, pattern states ({stated})")
    if c != prev:
        print(f"          !! consumes {c} but only {prev} stitches exist")
        fails.append(f"{label} consumes {c} of {prev}")
    prev = stated if ok else prev

print("    independent cross-check, same evaluator, restarting from R12's 18:")
prev = 18
for label, instr, stated in (("R13 alt", "[8 sc, inc] x2", 20),
                             ("R14 alt", "[4 sc, inc] x4", 24)):
    c, p = eval_seq(instr, prev)
    print(f"    {'OK  ' if p == stated and c == prev else 'FAIL'} {label}: {instr!r} "
          f"consumes {c} of {prev}, produces {p} (stated {stated})")
    if p != stated or c != prev:
        fails.append(f"{label}")
    prev = p

print("\n[10] stuffing volume (each round modelled as a 4.3 mm disc)")
head_v = vol_cm3(BODY, 1, 12)
body_v = vol_cm3(BODY, 13, 26)
tail_v = vol_cm3(BODY, 27, 36)
foot_v = vol_cm3(FOOT) * 2
print(f"    head R1-R12   {head_v:6.1f} cm3   (stuffed firmly)")
print(f"    neck+body     {body_v:6.1f} cm3   (stuffed lightly)")
print(f"    tail R27-R36  {tail_v:6.1f} cm3   (lightly, to R32)")
print(f"    2 feet        {foot_v:6.1f} cm3   (lightly)")
tot = head_v + body_v + tail_v + foot_v
rest = body_v + tail_v + foot_v
firm = head_v * 60 / 1000 + rest * 25 / 1000      # cm3 x kg/m3 -> g
print(f"    total volume {tot:.0f} cm3")
print(f"    at 30-55 kg/m3 polyfill -> {tot*30/1000:.1f}-{tot*55/1000:.1f} g; "
      f"firm head + light body -> ~{firm:.0f} g   (pattern states 30 g)")

print("\n[11] yarn weight")
stitches = sum(n for _, _, n, _ in BODY)
for name, (rows, copies) in ALL.items():
    if name == "body":
        continue
    stitches += sum(n for _, _, n, _ in rows) * copies
for per in (3.5, 4.0, 4.5):
    metres = stitches * MM_ST * per / 1000
    grams = metres / 190 * 100
    print(f"    {stitches} stitches x {MM_ST} mm x {per} = {metres:5.1f} m "
          f"-> {grams:4.1f} g at 190 m/100 g")
print(f"    pattern states 40 g main + 15 g gill + 5 g fin = 60 g")

print("\n" + "=" * 70)
if fails:
    print(f"{len(fails)} claim(s) do not survive the arithmetic:")
    for f in fails:
        print("  -", f)
else:
    print("every checked claim holds")
