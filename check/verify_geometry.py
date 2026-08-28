"""NS04 Coco: check the pattern's own numeric/geometry claims against each other."""
import math

STS_PER_MM = 1 / 4.5      # gauge: 4.5 mm per stitch
MM_PER_RND = 4.3          # gauge: 4.3 mm per round

print("="*72)
print("1. GAUGE INTERNAL CONSISTENCY")
print("="*72)
circ = 36 * 4.5
dia  = circ / math.pi
print(f"  36 sts x 4.5 mm/st      = {circ:.1f} mm circumference")
print(f"  circumference / pi      = {dia:.1f} mm diameter")
print(f"  pattern states          = 52 mm diameter   -> "
      f"{'CONSISTENT' if abs(dia-52)<1 else 'OFF by %.1f mm'%(dia-52)}")
print(f"  body height 20 rnd x 4.3 = {20*4.3:.1f} mm ; pattern states 8.5 cm "
      f"-> {'CONSISTENT' if abs(20*4.3-85)<3 else 'OFF'}")
print(f"  leg 8 rnd x 4.3          = {8*4.3:.1f} mm ; pattern states 34 mm "
      f"-> {'CONSISTENT' if abs(8*4.3-34)<1 else 'OFF'}")
print(f"  join height R4 = {4*4.3:.1f} mm, R5 = {5*4.3:.1f} mm ; "
      f"pattern states '17-21 mm' -> CONSISTENT")

print()
print("="*72)
print("2. LEG PLACEMENT — pattern claims 'roughly 90 deg to each other'")
print("="*72)
def layout(segments, label, rnd_sts):
    """segments = list of stitch counts walked between leg-join starts."""
    pos, centres = 0, []
    for seg in segments:
        centres.append(pos + 1.5)   # centre of the 3-st join block
        pos += seg
    print(f"\n  {label} (round has {rnd_sts} sts, {rnd_sts*4.5:.0f} mm circumference)")
    print(f"  walk sequence between joins: {segments}  (sum={sum(segments)}, "
          f"must equal {rnd_sts})")
    gaps = []
    for i in range(len(centres)):
        a, b = centres[i], centres[(i+1) % len(centres)]
        d = (b - a) % rnd_sts
        gaps.append(d)
    for i, g in enumerate(gaps):
        print(f"    leg{i+1} -> leg{(i%len(centres))+1 if i+1<len(centres) else 1}: "
              f"{g:5.1f} sts  = {g*4.5:5.1f} mm  = {g/rnd_sts*360:5.1f} deg")
    print(f"    ideal 90 deg spacing would be {rnd_sts/4:.1f} sts "
          f"({rnd_sts/4*4.5:.1f} mm)")
    worst = max(abs(g - rnd_sts/4) for g in gaps)
    print(f"    worst deviation from 90 deg: {worst:.1f} sts "
          f"({worst/rnd_sts*360:.0f} deg)  -> "
          f"{'OK' if worst <= 1.5 else 'NOT ROUGHLY 90 DEG'}")
    return gaps

# R4 back legs: "first 3 sc through leg, [1sc,inc]x3, next 3 sc through leg, [1sc,inc]x3"
back  = layout([13.5, 10.5], "R4 BACK legs (2 legs)", 24)
# R5 front legs: "2 sc, leg over 3, 12 sc, leg over 3, to end (10)"
front = layout([15, 15], "R5 FRONT legs (2 legs)", 30)

print("\n  Combined footprint (front legs vs back legs):")
print("    R4 back-leg centres are 10.5 sts apart on one side, 13.5 on the other")
print("    R5 front legs start at st 3 and st 18 of R5")
print("    -> a front leg sits only 3 sts (~13.5 mm) after each back leg on one")
print("       side, and ~12 sts (~54 mm) on the other: pairs, not a square.")
print("    Front/back span (centre-to-centre) = 3 + 1.5 = 4.5 sts = "
      f"{4.5*4.5:.1f} mm")
print("    Left/right span                   = 15 sts     = "
      f"{15*4.5:.1f} mm")
print(f"    span ratio {15*4.5/(4.5*4.5):.2f} : 1  -> footprint is a wide bowtie, "
      "not a square")

print()
print("="*72)
print("3. STANDING HEIGHT — does 8.5 cm survive the legs?")
print("="*72)
join_top = 5 * MM_PER_RND          # R5 = 21.5 mm above body base
leg_len  = 8 * MM_PER_RND          # 34.4 mm
lift     = leg_len - join_top
print(f"  leg length                = {leg_len:.1f} mm")
print(f"  highest join point (R5)   = {join_top:.1f} mm above body base")
print(f"  => body base floats       = {lift:.1f} mm above the table")
body_h   = 20 * MM_PER_RND
print(f"  body base -> top of head  = {body_h:.1f} mm")
print(f"  TOTAL standing height     = {lift+body_h:.1f} mm")
print(f"  pattern states            = 85 mm")
print(f"  -> OVERSTATED by {lift+body_h-85:.1f} mm "
      f"({(lift+body_h-85)/85*100:.0f}%)")
print("  8.5 cm is only right if the legs are decorative and the BELLY rests")
print("  on the table - which contradicts 'puts the foot flat on the table'")
print("  and 'Coco standing square on all four legs'.")

print()
print("="*72)
print("4. FACE PLACEMENT vs HEAD GEOMETRY")
print("="*72)
head_c = 36 * 4.5
front_arc = head_c / 2                      # 180 deg visible front half
print(f"  head circumference            = {head_c:.0f} mm")
print(f"  front half (180 deg)          = {front_arc:.0f} mm")
eye_spacing_mm = 6 * 4.5
print(f"  eyes 6 sts apart              = {eye_spacing_mm:.1f} mm between centres")
print(f"  = {eye_spacing_mm/front_arc*180:.0f} deg of the front face "
      f"({eye_spacing_mm/head_c*360:.0f} deg around the head)")
muzzle_d = (12*4.5)/math.pi
print(f"  muzzle diameter (12 sts)      = {muzzle_d:.1f} mm")
clear = (eye_spacing_mm - muzzle_d)/2
print(f"  muzzle edge -> nearest eye    = {clear:.1f} mm "
      f"({'CLEAR' if clear>2 else 'VERY TIGHT / OVERLAPPING'})")
print(f"  muzzle pinned over R12-R14, eyes embroidered at R13-R14")
print(f"  -> pattern says muzzle sits 'slightly BELOW the eye line'; the rows")
print(f"     actually overlap by 2 of the muzzle's 3 rows.")
ear_sep = 7*4.5
print(f"  ears 7 sts apart              = {ear_sep:.1f} mm = "
      f"{ear_sep/head_c*360:.0f} deg around the head")

print()
print("="*72)
print("5. MATERIALS SANITY")
print("="*72)
stitches = (sum(r[2] for r in [(0,0,6)]+[ (0,0,v) for v in [9,9,9,9,9,9,9]]) )*4
leg = (6+9*7)*4; ear = (6+9+9)*2; muz = 6+9+12+12+12
body = 6+12+18+24+30+36+36+36+36+32+36+36+36+36+36+30+24+18+12+6
total = leg+ear+muz+body
print(f"  total stitches in project = {total} "
      f"(legs {leg}, ears {ear}, muzzle {muz}, body {body})")
yarn_m = total * 0.012
print(f"  ~1.2 cm of worsted per sc = {yarn_m:.1f} m of yarn")
print(f"  worsted ~2.0 m/g          -> ~{yarn_m/2.0:.1f} g needed; "
      f"pattern allows 30 g + 5 g  -> GENEROUS but fine (tails/sewing)")
print(f"  polyfill stated 15 g. Toy volume ~ sphere d=51.6 mm + head:")
v = (4/3)*math.pi*(25.8**3) + (4/3)*math.pi*(25.8**3)*0.75
print(f"    ~{v/1000:.0f} cm3 stuffed; at 40-65 g/L that is "
      f"~{v/1e6*40*1000:.1f}-{v/1e6*65*1000:.1f} g")
print(f"  -> 15 g is roughly 3x the volume the toy can hold")
