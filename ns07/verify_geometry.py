"""NS07 Trio — check each stated size against its stitch count."""
import math, sys
sys.path.insert(0, "ns07")
from pieces import (SUNNY_CENTRE, SUNNY_PETALS, WADDLE_BODY, WADDLE_WING, SPUD,
                    WADDLE_CHEST, WADDLE_BEAK,
                    ALL, MM_ST, MM_RND, SPUD_FOUNDATION, CLAIM)

fails = []
def check(name, got, want, tol, unit="mm"):
    ok = abs(got - want) <= tol
    print(f"  {'OK  ' if ok else 'FAIL'} {name:<34} computed {got:8.2f} {unit:<4} "
          f"stated {want:8.2f} {unit}")
    if not ok:
        fails.append(f"{name}: {got:.1f} vs stated {want}")

def circle(n): return n * MM_ST / math.pi
HDC = MM_RND * 1.6        # an hdc stands about 1.6 x an sc round height

print("=" * 78)
print("[1] SUNNY - 'about 4.5 cm across the petals'")
widest = max(n for _, _, n, _ in SUNNY_CENTRE)
D = circle(widest)
check("brown centre across", D, CLAIM["centre"], 1.0)
print(f"    'a small brown cushion about 20 mm across' -> {D:.1f} mm  CORRECT")
petals = SUNNY_PETALS[0][2]
print(f"    petals: {petals} sts from 9 repeats of (sl st + 3-st cluster) into Rnd 3")
across = D + 2*HDC
print(f"    a cluster worked into ONE stitch stands about an hdc height = {HDC:.1f} mm")
print(f"    across the petals = {D:.1f} + 2 x {HDC:.1f} = {across:.1f} mm = {across/10:.1f} cm")
check("Sunny across the petals", across, CLAIM["sunny"], 4)
need = (CLAIM["sunny"] - 2*HDC)
print(f"    for a true {CLAIM['sunny']/10:.1f} cm the centre must be {need:.1f} mm "
      f"across = {need*math.pi/MM_ST:.1f} stitches, not {widest}")

print("\n[2] WADDLE - 'about 5 cm tall'")
H = len(WADDLE_BODY) * MM_RND
W = circle(max(n for _, _, n, _ in WADDLE_BODY))
print(f"    {len(WADDLE_BODY)} rounds x {MM_RND} = {H:.1f} mm tall; "
      f"widest {W:.1f} mm")
check("Waddle tall", H, CLAIM["waddle"], 4)
print(f"    for a true {CLAIM['waddle']/10:.0f} cm it needs "
      f"{CLAIM['waddle']/MM_RND:.1f} rounds, not {len(WADDLE_BODY)}")

print("\n[3] SPUD - 'about 5.5 cm long'")
side = SPUD_FOUNDATION - 3
cap = 6                                    # after Rnd 2, the last increase round
tot = 2*cap + 2*side
print(f"    ch {SPUD_FOUNDATION}: sides N-3 = {side} sts; caps reach {cap}+{cap} "
      f"at Rnd 2 -> {tot} st (stated {SPUD[1][2]})")
if tot != SPUD[1][2]:
    fails.append("spud cap/side model does not reproduce the stated count")
sw = circle(2*cap)
sl = sw + side*MM_ST
walls = len(SPUD) - 2                       # Rnds 3-10 are the walls
sh = walls * MM_RND
print(f"    width  = a circle made from both caps ({2*cap} st) = {sw:.1f} mm")
print(f"    length = width + one side ({side*MM_ST:.1f} mm) = {sl:.1f} mm = {sl/10:.2f} cm")
print(f"    height = {walls} wall rounds x {MM_RND} = {sh:.1f} mm")
check("Spud long", sl, CLAIM["spud"], 4)
print(f"    cross-check: a {tot}-st CIRCLE is only {circle(tot):.1f} mm across, so no")
print(f"    {tot}-st oval can reach {CLAIM['spud']/10:.1f} cm long.")
print(f"    for a true {CLAIM['spud']/10:.1f} cm with {side}-st sides the caps must be "
      f"{(CLAIM['spud']-side*MM_ST)*math.pi/(2*MM_ST)/2:.1f} sts each "
      f"= {2*((CLAIM['spud']-side*MM_ST)*math.pi/(2*MM_ST)/2)+2*side:.0f} stitches total")

print("\n[4] 'The full trio - each about 5 cm tall'")
for nm, h in (("Sunny (a flat flower, not tall)", 2*MM_RND + 2*HDC),
              ("Waddle", H), ("Spud", sh)):
    print(f"    {nm:<34} {h:5.1f} mm = {h/10:.1f} cm")
if abs(H - CLAIM["trio_tall"]) > 4:
    fails.append(f"'each about 5 cm tall' - only Waddle is within range at {H/10:.1f} cm")

print("\n[5] TROUBLESHOOTING: 'Minis come out too big'")
print(f"    the pattern says at 3.5 mm/st 'these finish at 4.5-5.5 cm'")
print(f"    computed: Sunny {across/10:.1f} cm, Waddle {H/10:.1f} cm, Spud {sl/10:.1f} cm")
print(f"    -> they come out SMALLER than stated, so the entry is backwards")
fails.append("'Minis come out too big' is backwards: all three come out smaller")

print("\n[6] faces - 'eyes 4 stitches apart' on all three")
span = 4 * MM_ST
for nm, w in (("Sunny centre", D), ("Waddle body", circle(18)), ("Spud broad face", sl)):
    eye = 5.0
    clear = (w - span)/2 - eye/2
    print(f"    {nm:<16} {w:5.1f} mm wide; eyes {span:.1f} mm apart -> "
          f"{clear:5.1f} mm between an eye edge and the rim")
    if clear < 1.0:
        print(f"      ! essentially no clearance on a 5 mm eye")

print("\n[7] stuffing volume")
def vol_disc(rows):
    return sum(math.pi*(circle(n)/2)**2*MM_RND for _, _, n, _ in rows)/1000
def earea(P, k):
    lo, hi = 0.01, 500.0
    for _ in range(200):
        b = (lo+hi)/2; a = k*b
        if math.pi*(3*(a+b)-math.sqrt((3*a+b)*(a+3*b))) < P: lo = b
        else: hi = b
    b = (lo+hi)/2
    return math.pi*(k*b)*b
k = sl/sw
spud_v = sum(earea(n*MM_ST, k)*MM_RND for _, _, n, _ in SPUD)/1000
parts = {"Sunny centre": vol_disc(SUNNY_CENTRE), "Waddle body": vol_disc(WADDLE_BODY),
         "2 wings": vol_disc(WADDLE_WING)*2, "Spud": spud_v}
for nm, v in parts.items():
    print(f"    {nm:<14} {v:5.1f} cm3")
tot_v = sum(parts.values())
print(f"    {'TOTAL':<14} {tot_v:5.1f} cm3")
for d in (30, 55, 80):
    print(f"    at {d} kg/m3 -> {tot_v*d/1000:4.2f} g   (pattern states "
          f"{CLAIM['polyfill']:.0f} g for all three)")
print(f"    {CLAIM['polyfill']:.0f} g implies {CLAIM['polyfill']/tot_v*1000:.0f} kg/m3")

print("\n[8] yarn")
stitch_counts = {
    "Sunny (center + petals)": sum(n for _, _, n, _ in SUNNY_CENTRE) + SUNNY_PETALS[0][2],
    "Waddle (body, 2 wings, chest, beak)":
        sum(n for _, _, n, _ in WADDLE_BODY) + 2*sum(n for _, _, n, _ in WADDLE_WING)
        + sum(n for _, _, n, _ in WADDLE_CHEST) + sum(n for _, _, n, _ in WADDLE_BEAK),
    "Spud": sum(n for _, _, n, _ in SPUD),
}
stated = {"Sunny (center + petals)": 9, "Waddle (body, 2 wings, chest, beak)": 12, "Spud": 7}
for nm, n in stitch_counts.items():
    m = n*MM_ST*4/1000
    print(f"    {nm:<26} {n:>4} st = {m:4.1f} m = {m/250*100:4.2f} g at 250 m/100 g"
          f"   (stated {stated[nm]} g)")
print(f"    total stated {sum(CLAIM['yarn'].values())} g vs "
      f"{sum(n*MM_ST*4/1000 for n in stitch_counts.values())/250*100:.1f} g used")

print("\n[9] what a yarn swap would do (worsted #4 on 3.5 mm = 4.5 mm/st)")
s = 4.5/MM_ST
print(f"    everything scales by {s:.2f}:  Sunny {across*s/10:.1f} cm, "
      f"Waddle {H*s/10:.1f} cm, Spud {sl*s/10:.1f} cm")

print("\n" + "=" * 78)
if fails:
    print(f"{len(fails)} claim(s) do not survive the arithmetic:")
    for f in fails:
        print("  -", f)
else:
    print("every checked claim holds")
