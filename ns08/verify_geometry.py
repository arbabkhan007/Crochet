import math
MM_ST, MM_RND = 4.5, 4.3
dia = lambda s: s*MM_ST/math.pi
print("="*72); print("1. STATED DIMENSIONS vs GAUGE"); print("="*72)
body_h, head_h = 13*MM_RND, 13*MM_RND
print(f"  body 13 rnd            = {body_h:.1f} mm")
print(f"  head 13 rnd            = {head_h:.1f} mm")
print(f"  head seated on neck    = {body_h+head_h:.1f} mm  = {(body_h+head_h)/10:.1f} cm")
leg, join_back, join_front = 8*MM_RND, 6*MM_RND, 8*MM_RND
lift = leg - join_back
print(f"  + back legs lift body   = {lift:.1f} mm  (leg {leg:.1f} - join {join_back:.1f})")
print(f"  TOTAL seated height     = {(body_h+head_h+lift)/10:.1f} cm")
print(f"  pattern states          = 16 cm  -> OVERSTATED by "
      f"{160-(body_h+head_h+lift):.0f} mm ({(160-(body_h+head_h+lift))/160*100:.0f}%)")
print(f"  to reach 16 cm each of body and head would need "
      f"{(160-lift)/2/MM_RND:.0f} rounds, not 13.")

print(f"\n  tail 12 rnd            = {12*MM_RND:.1f} mm; stated 6 cm "
      f"-> overstated by {60-12*MM_RND:.1f} mm ({(60-12*MM_RND)/60*100:.0f}%)")

print("\n  wingspan:")
wing = 10*MM_ST
print(f"    wing straight edge (10 sts) = {wing:.1f} mm")
print(f"    widest body (30 sts)        = {dia(30):.1f} mm")
print(f"    body at wing rows 10-11 (24 sts) = {dia(24):.1f} mm")
for b in (dia(30), dia(24), 30):
    print(f"    2 x {wing:.0f} + {b:.0f} = {2*wing+b:.0f} mm")
print(f"    stated 13 cm = 130 mm -> overstated by "
      f"{130-(2*wing+dia(24)):.0f}-{130-(2*wing+dia(30)):.0f} mm")
print("    and the wings are 'angled up and out', which shortens the horizontal")
print("    span further. 13 cm is not reachable.")

print("\n  neck ring: 18 sts -> " + f"{dia(18):.1f} mm; stated 'about 26 mm' OK")
print(f"  eyes 8 sts apart on 36-st head = {8*MM_ST:.1f} mm = {8/36*360:.0f} deg")

print(); print("="*72); print("2. WING ROW 4 — the scallop budget"); print("="*72)
cons = 2 + 1 + 2 + 1 + 4
print(f"  slip groups 2 / 2 / 4 = {2+2+4}, shells 1 + 1 = 2 -> {cons} sts")
print(f"  Row 3 produced 10 -> {'OK, closes exactly' if cons==10 else 'MISMATCH'}")
print("  both scallops are (sc, hdc, dc, hdc, sc) = 5 sts -> SYMMETRIC. Good.")
print(f"  wing rows: R1 {4+3+3}, R2 {3+3+4}, R3 {2+4+4} -> all 10. Consistent.")

print(); print("="*72); print("3. SPIKE STRIP — the serious one"); print("="*72)
print("  Base strip: 'Ch 4. Row 1: sc in 2nd ch from hook, sc in next 2.'")
print(f"  -> the base row is {3} stitches long.")
print("  Spike row: '(repeat 9 times): ch 4, sl st in 2nd ch from hook, sc in next")
print("             ch, hdc in next ch, then sl st into the NEXT STITCH OF THE BASE ROW'")
print(f"  -> 9 spikes, each anchored into one base-row stitch.")
print(f"  -> 9 anchors needed, {3} available. THE STRIP IS 3 STITCHES LONG.")
print("  A 3-stitch strip is ~13.5 mm. The path it must cover is crown to tail tip:")
print(f"    head {head_h:.0f} + body {body_h:.0f} + tail {12*MM_RND:.0f} "
      f"= {head_h+body_h+12*MM_RND:.0f} mm")
print(f"  -> the strip is about {(head_h+body_h+12*MM_RND)/13.5:.0f}x too short.")
print("  This is not a typo you can squint at: the piece as written cannot exist.")

print(); print("="*72); print("4. HEAD-TO-NECK JOIN"); print("="*72)
print(f"  head closes: R13 = 6 sts -> cinched to about {6*MM_ST/math.pi:.1f} mm across")
print(f"  body neck:   R13 = 18 sts -> open ring {dia(18):.1f} mm across")
print(f"  -> a {6*MM_ST/math.pi:.0f} mm gathered point is being ladder-stitched to a "
      f"{dia(18):.0f} mm ring.")
print("  The pattern then says 'this joint carries the whole head', and its own")
print("  troubleshooting says 'head flops forward'. Those are the same problem.")

print(); print("="*72); print("5. LEGS — 'all four identical', seated pose"); print("="*72)
print(f"  all four legs 8 rnd = {leg:.1f} mm")
print(f"  back legs join Rnd 6 = {join_back:.1f} mm above the body base")
print(f"  front legs join Rnd 8 = {join_front:.1f} mm above the body base")
print(f"  back feet hang  {leg-join_back:.1f} mm BELOW the base")
print(f"  front feet hang {leg-join_front:.1f} mm below the base -> they end AT it")
print("  -> back legs 8.6 mm longer in effect than the front. Ember rocks back")
print("     onto her back feet with the front feet in the air.")
print("  And 'sits square' contradicts 'reach the table': if the back legs reach")
print("  the table they lift the body 8.6 mm off it, so she is not sitting.")

print(); print("="*72); print("6. STUFFING"); print("="*72)
v_head = (4/3)*math.pi*(dia(36)/2)**3/1000
v_body = v_head*0.85
v_leg  = 4*(4/3)*math.pi*5**3/1000
v_tail = 14
tot = v_head+v_body+v_leg+v_tail
print(f"  head {v_head:.0f} cm3 + body {v_body:.0f} cm3 + legs {v_leg:.0f} cm3 "
      f"+ tail {v_tail} cm3 = {tot:.0f} cm3")
print(f"  at 30-60 kg/m3 -> {tot*30/1000:.1f}-{tot*60/1000:.1f} g")
print(f"  stated 45 g -> about {45/(tot*45/1000):.0f}x what the toy can hold")
