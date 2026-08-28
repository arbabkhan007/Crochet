import math
print("="*70); print("POLYFILL — corrected density arithmetic"); print("="*70)
# stuffed toy volume: body sphere (d 51.6 mm) + head sphere (d 51.6, x0.75 overlap)
r = 25.8
v_body = (4/3)*math.pi*r**3
v_head = v_body*0.7
v_limbs = 4*(4/3)*math.pi*(9.5/2)**3 + 2*(4/3)*math.pi*(9.5/2)**3*0.5
v_mm3 = v_body + v_head + v_limbs
v_cm3 = v_mm3/1000
print(f"  body sphere d=51.6 mm      = {v_body/1000:6.1f} cm3")
print(f"  head (70% of a sphere)     = {v_head/1000:6.1f} cm3")
print(f"  4 legs + 2 ears            = {v_limbs/1000:6.1f} cm3")
print(f"  TOTAL stuffed volume       = {v_cm3:6.1f} cm3")
for lo, hi in [(30,60),(60,100)]:
    print(f"  at {lo}-{hi} kg/m3 (= {lo/1000:.3f}-{hi/1000:.3f} g/cm3): "
          f"{v_cm3*lo/1000:.1f} - {v_cm3*hi/1000:.1f} g")
print("  -> polyester fibre is roughly 30-60 kg/m3 when firmly packed.")
print("  -> Coco needs ~4-8 g. Pattern states 15 g: ~2-3x more than fits.")

print(); print("="*70)
print("LEG JOIN WIDTH — 'flatten only the top 3 sts' vs 'caught fully'")
print("="*70)
leg_sts = 9
print(f"  leg opening at R8            = {leg_sts} sts")
print(f"  flattened edge of a 9-st tube= ~{math.ceil(leg_sts/2)} sts across")
print(f"  stitches the body round joins= 3 sts")
print(f"  => {math.ceil(leg_sts/2)-3} edge stitches of each leg are NOT joined")
print("  Pattern says 'flatten only the top 3 sts' (leg) but also 'make sure")
print("  the flattened top of each leg is caught fully in the round' (assembly).")
print("  Those two cannot both be true unless the whole 9-st top is pinched")
print("  down to a 3-stitch strip. Needs one sentence to say so.")

print(); print("="*70); print("EAR PLACEMENT vs HEAD WIDTH AT R15-R16"); print("="*70)
for rnd, sts in [(15,36),(16,30)]:
    circ = sts*4.5; d = circ/math.pi
    sep = 7*4.5
    print(f"  R{rnd}: {sts} sts -> circ {circ:.0f} mm, diameter {d:.1f} mm")
    print(f"       ears 7 sts apart = {sep:.1f} mm = {sep/circ*360:.0f} deg around")
print("  -> 7 sts puts the ears at/over the 90-deg side line on a 30-st round.")
print("     Capybara ears sit on TOP of the head; 4-5 sts would read better.")

print(); print("="*70); print("R5 LEG JOIN — trailing stitch count is left implicit"); print("="*70)
print("  '2 sc, join leg over 3 sc, 12 sc, join leg over 3 sc, work to end (30)'")
print(f"  2 + 3 + 12 + 3 = {2+3+12+3}; 30 - 20 = {30-20} sts left unstated")
print("  Every other round states its count explicitly; this one makes the")
print("  crocheter derive the final 10 sc from the (30) total.")
