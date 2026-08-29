"""NS01 Hamish — check every stated dimension and claim against the round tables."""
import math, sys
sys.path.insert(0, "ns01")
from pieces import (HEAD, MUZZLE, BODY, BELLY, LEG, EAR_INNER, EAR_OUTER, HORN,
                    MM_ST, MM_RND, FRINGE, TAIL, SCARF, LEG_YARN_A_FROM)

fails = []
def check(name, got, want, tol, unit="mm"):
    ok = abs(got - want) <= tol
    print(f"  {'OK  ' if ok else 'FAIL'} {name:<40} computed {got:8.3f} {unit:<4} "
          f"stated {want:8.3f} {unit}")
    if not ok:
        fails.append(f"{name}: {got:.1f} vs stated {want}")

def diam(n): return n * MM_ST / math.pi

print("=" * 78)
print("[1] gauge self-consistency: '11 sc x 12 rounds = 5 cm'")
check("mm per stitch", 50/11, MM_ST, 0.01)
check("mm per round",  50/12, MM_RND, 0.01)

print("\n[2] head: '70 mm wide x 67 mm tall ... flattened sphere at 0.96'")
w_head = max(n for _,_,n,_ in HEAD)
check("head width (48 st)", diam(w_head), 70, 1.0)
check("head height (16 rnd)", len(HEAD)*MM_RND, 67, 1.0)
ratio = (len(HEAD)*MM_RND)/diam(w_head)
check("height-to-width ratio", ratio, 0.96, 0.02, "")

print("\n[3] body: '70 mm wide body' / '19 rounds ~79 mm'")
check("body width (48 st)", diam(max(n for _,_,n,_ in BODY)), 70, 1.0)
check("body height (19 rnd)", len(BODY)*MM_RND, 79, 1.0)

print("\n[4] sitting height: 'about 15 cm / 6 in'")
sit = len(BODY)*MM_RND + len(HEAD)*MM_RND
check("body + head", sit, 150, 6)

print("\n[5] legs: 'sixteen rounds gives a 67 mm leg'")
check("leg length", len(LEG)*MM_RND, 67, 1.0)

print("\n[6] muzzle rim: 'rim = 35 mm across'")
check("rim diameter (24 st)", diam(MUZZLE[-1][2]), 35, 1.0)

print("\n[7] MUZZLE FIT — does the rim fit between the eyes and the chin?")
rim = diam(MUZZLE[-1][2])
print(f"    rim {rim:.1f} mm across -> {rim/MM_RND:.1f} rounds of head height "
      f"(pattern says 'roughly eight rounds')")
print(f"    eyes at Rnd 9-10; pattern pins the muzzle top 'at about Rnd 10'")
print(f"    pattern says the lower edge falls 'around Rnd 15-16'")
print(f"    Rnd 10 -> Rnd 16 is {16-10} rounds = {(16-10)*MM_RND:.1f} mm")
print(f"    Rnd 10 -> Rnd 15 is {15-10} rounds = {(15-10)*MM_RND:.1f} mm")
print(f"    the rim needs {rim/MM_RND:.1f} rounds -> Rnd 10 + {rim/MM_RND:.1f} = Rnd {10+rim/MM_RND:.1f}")
print(f"    the head has only {len(HEAD)} rounds")
short = (10 + rim/MM_RND) - len(HEAD)
print(f"    => the muzzle overruns the chin by {short:.1f} rounds ({short*MM_RND:.1f} mm)")
if short > 0:
    fails.append(f"muzzle rim {rim:.0f} mm needs {rim/MM_RND:.1f} rounds from Rnd 10 "
                 f"but the head ends at Rnd {len(HEAD)} - overruns by {short*MM_RND:.0f} mm")
print("\n    head width at each round vs the 35 mm rim:")
for label, instr, n, note in HEAD:
    d = diam(n)
    flag = "  <- head narrower than the rim" if d < rim else ""
    print(f"      {label:<8} {n:>3} st -> {d:5.1f} mm wide{flag}")

print("\n[8] neck ring: 'Rnd 19 of the body, an 18-stitch ring about 26mm across'")
check("neck ring", diam(18), 26, 1.0)
print("    head/neck engagement: the head is closed to 6 st; the 26 mm ring grips it")
for label, instr, n, note in reversed(HEAD):
    if diam(n) >= 26:
        eng = (len(HEAD) - int(label.split()[1])) * MM_RND
        print(f"    ring meets the head at {label} ({diam(n):.1f} mm) = {eng:.1f} mm of engagement")
        break

print("\n[9] legs vs their joins")
leg = len(LEG)*MM_RND
front_lo, front_hi = 8*MM_RND, 9*MM_RND
back_lo,  back_hi  = 3*MM_RND, 6*MM_RND
print(f"    leg length {leg:.1f} mm")
print(f"    front join Rnd 8-9  = {front_lo:.1f}-{front_hi:.1f} mm above the base")
print(f"    back  join Rnd 3-6  = {back_lo:.1f}-{back_hi:.1f} mm above the base")
print(f"    the two joins differ by {front_hi-back_lo:.1f} mm, but all four legs are identical")
for deg in (20, 30, 40):
    reach = leg*math.cos(math.radians(deg))
    print(f"    at {deg} deg from vertical a {leg:.0f} mm leg drops {reach:.1f} mm; "
          f"front needs {front_hi:.1f}, back needs {back_hi:.1f}")
need_f = leg/math.cos(math.radians(0))
ang = math.degrees(math.acos(front_hi/leg))
print(f"    for the front hoof to land on the table the leg must splay {ang:.0f} deg from vertical")

print("\n[10] fringe count: 'about 24 + 10 + 9 = 43 knots ... 44 strands'")
r8, r7, r6 = FRINGE["rows"]["Rnd 8"], FRINGE["rows"]["Rnd 7"], FRINGE["rows"]["Rnd 6"]
knots = r8//2 + (r7//2)//2 + (r6//2)//2
print(f"    Rnd 8 every stitch over a half-round = {r8}//2 = {r8//2}")
print(f"    Rnd 7 every other stitch             = {(r7//2)}//2 = {(r7//2)//2}")
print(f"    Rnd 6 every other stitch             = {(r6//2)}//2 = {(r6//2)//2}")
print(f"    total {knots} knots, {FRINGE['strands']} strands cut -> "
      f"{'OK' if abs(knots-FRINGE['strands']) <= 1 else 'MISMATCH'}")
if abs(knots - FRINGE["strands"]) > 1:
    fails.append(f"fringe: {knots} knots vs {FRINGE['strands']} strands")

print("\n[11] tail: '6 strands ... divide into 3 groups of 4'")
ends = TAIL["strands"]*2
print(f"    6 strands folded in half (lark's head) = {ends} hanging ends")
print(f"    3 groups x 4 = {TAIL['groups']*TAIL['per_group']} -> "
      f"{'OK' if ends == TAIL['groups']*TAIL['per_group'] else 'MISMATCH'}")
if ends != TAIL["groups"]*TAIL["per_group"]:
    fails.append("tail braid grouping")

print("\n[12] scarf: 'ch 61 ... hdc in 2nd ch from hook and in each ch across (60)'")
check("hdc from ch 61", SCARF["ch"]-1, SCARF["hdc_row1"], 0, "st")

print("\n[13] face spacing")
check("eyes 7 st apart", 7*MM_ST, 31.9, 0.5)
print(f"    eye spacing is {7*MM_ST/diam(48)*100:.0f}% of head width; "
      f"muzzle face (30 st) = {diam(30):.1f} mm")

print("\n[14] stuffing volume (each round modelled as a %.2f mm disc)" % MM_RND)
def vol(rows, copies=1):
    return copies*sum(math.pi*(diam(n)/2)**2*MM_RND for _,_,n,_ in rows)/1000
v = {"head": vol(HEAD), "muzzle": vol(MUZZLE), "body": vol(BODY),
     "belly(flat)": 0.0, "4 legs": vol(LEG,4), "2 ears": vol(EAR_OUTER,2),
     "2 horns": vol(HORN,2)}
for k, x in v.items():
    print(f"    {k:<12} {x:7.1f} cm3")
tot = sum(v.values())
print(f"    {'TOTAL':<12} {tot:7.1f} cm3")
for dens in (30, 55, 80):
    print(f"    at {dens} kg/m3 -> {tot*dens/1000:5.1f} g     "
          f"(pattern states 55-60 g; head+body alone stated at 40 g)")
hb = v["head"]+v["body"]
print(f"    head+body = {hb:.0f} cm3; 40 g implies {40/hb*1000:.0f} kg/m3")
print(f"    whole toy = {tot:.0f} cm3; 55-60 g implies {55/tot*1000:.0f}-{60/tot*1000:.0f} kg/m3")

print("\n[15] yarn")
yarn_a_st = (sum(n for _,_,n,_ in HEAD) + sum(n for _,_,n,_ in BODY)
             + sum(n for _,_,n,_ in LEG[LEG_YARN_A_FROM-1:])*4
             + sum(n for _,_,n,_ in EAR_OUTER)*2)
FRINGE_M = FRINGE["strands"]*FRINGE["cut_cm"]/100
TAIL_M   = TAIL["strands"]*TAIL["cut_cm"]/100
print(f"    Yarn A stitches (head+body+4 legs from Rnd 6+2 outer ears) = {yarn_a_st}")
for per in (3.0, 4.0, 4.5):
    m = yarn_a_st*MM_ST*per/1000
    print(f"    at {per} x stitch width = {m:5.1f} m  "
          f"+ fringe {FRINGE_M:.1f} m + tail {TAIL_M:.1f} m = {m+FRINGE_M+TAIL_M:5.1f} m "
          f"-> {(m+FRINGE_M+TAIL_M)/150*80:5.1f} g at 150 m/80 g")
print(f"    pattern states 80 g / 150 m for Yarn A")

print("\n[16] three-sizes scaling ('stitch counts stay the same')")
for name, hook, height, yarn, stuff in (("Wee", 2.75, 12, 48, 30),
                                        ("Classic", 3.5, 15, 80, 57.5),
                                        ("Cuddle", 5.0, 21, 115, 175)):
    s = height/15
    print(f"    {name:<8} height {height} cm -> linear scale {s:.2f}; "
          f"area {s**2:.2f} -> yarn {80*s**2:5.0f} g (stated {yarn} g); "
          f"volume {s**3:.2f} -> stuffing {57.5*s**3:5.0f} g (stated {stuff} g)")

print("\n" + "=" * 78)
if fails:
    print(f"{len(fails)} claim(s) do not survive the arithmetic:")
    for f in fails:
        print("  -", f)
else:
    print("every checked claim holds")
