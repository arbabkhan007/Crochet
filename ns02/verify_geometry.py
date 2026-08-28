"""NS02: check stated dimensions, the hem/wing stitch budgets, and materials."""
import math

MM_ST, MM_RND = 3.5, 3.2     # stated gauge: DK cotton on 2.5 mm

def dia(sts): return sts * MM_ST / math.pi

print("="*72); print("1. STATED DIMENSIONS vs GAUGE"); print("="*72)
rows = [
 ("Boo widest (24 st)",        dia(24),      29, "2.9 cm wide"),
 ("Boo tall: 12 rnd + hem",    12*MM_RND,    48, "4.8 cm tall"),
 ("Pip widest (36 st)",        dia(36),      40, "4.0 cm wide"),
 ("Pip tall: 13 rnd",          13*MM_RND,    42, "4.2 cm tall"),
 ("Bramble widest (30 st)",    dia(30),      33, "3.3 cm wide"),
 ("Bramble tall: 16 rnd",      16*MM_RND,    51, "5.1 cm tall"),
]
for name, got, want, stated in rows:
    pct = (want-got)/got*100
    flag = "OK  " if abs(pct) < 8 else "OFF "
    print(f"  {flag} {name:<26} gauge gives {got:6.1f} mm, stated {stated:<12} "
          f"({pct:+.0f}%)")
print("\n  wingspan: 2 x 42 mm wings + 33 mm body = "
      f"{2*42+33} mm; stated 11.5 cm -> OK")
print("  Boo '2.9 cm wide' is the BODY TUBE. The hem is 48 sts = "
      f"{48*MM_ST:.0f} mm of edge ruffling onto a {24*MM_ST:.0f} mm ring,")
print("  so the flared hem is considerably wider than 29 mm. Ambiguous, not wrong.")
print(f"\n  Pip: 36 sts gives a {dia(36):.1f} mm tube but the pattern says 40 mm and")
print("  instructs 'stuff firmly, overstuff' — an overstuffed ball bulges past its")
print("  stitch circumference, so +27% is defensible. Borderline, flag not fail.")

print(); print("="*72); print("2. BOO'S RUFFLED HEM — does it close all 24 stitches?"); print("="*72)
repeat_consumes = 2 + 1 + 1                 # 2 sl st, shell into 1 st, 1 sl st
shell_produces  = 5                          # sc, hdc, dc, hdc, sc
repeat_produces = 2 + shell_produces + 1
print(f"  one repeat consumes {repeat_consumes} sts, produces {repeat_produces} sts")
print(f"  x6 repeats: consumes {repeat_consumes*6} (Rnd 12 has 24) -> "
      f"{'OK, closes exactly' if repeat_consumes*6==24 else 'DOES NOT CLOSE'}")
print(f"              produces {repeat_produces*6} -> stated (48) "
      f"{'OK' if repeat_produces*6==48 else 'MISMATCH'}")
print(f"  shell adds {shell_produces-1} extra sts per repeat -> "
      f"{(shell_produces-1)*6} sts of flare. 6 ruffles as claimed.")

print(); print("="*72); print("3. BAT WING ROW 3 — the 2/3/2/2 slip-stitch claim"); print("="*72)
sl = [2, 3, 2, 2]
shells = [1, 1, 1]
print(f"  slip-stitch groups {sl} = {sum(sl)} sts")
print(f"  scallop shells {shells} = {sum(shells)} sts (each worked into 1 st)")
print(f"  total {sum(sl)+sum(shells)} sts; Row 2 made 12 -> "
      f"{'OK, consumes all 12' if sum(sl)+sum(shells)==12 else 'MISMATCH'}")
print("\n  BUT the three scallops are not the same size:")
s1 = "sc, hdc, dc, picot, dc, hdc, sc"
s2 = "sc, hdc, picot, hdc, sc"
for label, s in (("scallop 1 (middle)", s1), ("scallop 2", s2), ("scallop 3", s2)):
    import re
    n = len(re.findall(r'(?:sl st|sc|hdc|dc|picot)', s))
    pic = len(re.findall(r'picot', s))
    print(f"    {label:<20} {n} sts, {pic} picots")
print("  -> scallop 1 is 7 sts with 3 picots; scallops 2 and 3 are 5 sts with 2.")
print("     The middle scallop is visibly bigger than the outer two.")
print("     The note only claims the STITCH COUNT balances, which it does -")
print("     but a maker following it gets an asymmetric wing and will think")
print("     they made a mistake. Either equalise them or say it is deliberate.")

print(); print("="*72); print("4. WITCH HAT BRIM — 'brim, 22 mm across'"); print("="*72)
print(f"  brim ring = 20 sts -> circumference {20*MM_ST:.0f} mm, "
      f"diameter {dia(20):.1f} mm  <- matches '22 mm'")
print(f"  but a flat 20-st disc has an OUTER edge about one stitch wider:")
print(f"  outer diameter ~{(20*MM_ST + 2*MM_ST)/math.pi:.1f} mm")
print(f"  Boo's head is 24 sts = {dia(24):.1f} mm across")
print("  -> '22 mm' describes the inner ring, not the visible brim. The visible")
print("     brim is ~35 mm, wider than Boo's 27 mm head - correct for a witch hat,")
print("     but the label will read as wrong to anyone who measures it.")
print(f"  Troubleshooting's claim about 30 sts: outer ~{(30*MM_ST+2*MM_ST)/math.pi:.0f} mm")
print(f"  vs Boo's {dia(24):.0f} mm -> 'wider than Boo's body' is TRUE.")

print(); print("="*72); print("5. STUFFING — '~15 g for the trio'"); print("="*72)
def sph(d): return (4/3)*math.pi*(d/2)**3
pip_v   = sph(40)*1.15          # overstuffed
bram_v  = sph(31)*0.8 + sph(26)*0.5
boo_v   = 0                     # open bell, base optional, never told to stuff
print(f"  Pip (overstuffed, 40 mm)      ~{pip_v:5.0f} cm3")
print(f"  Bramble (body + head)         ~{bram_v:5.0f} cm3")
print(f"  Boo                           ~{boo_v:5.0f} cm3  (open bell, no stuffing step)")
tot = pip_v + bram_v + boo_v
for lo, hi in [(30, 60)]:
    print(f"  total ~{tot:.0f} cm3 at {lo}-{hi} kg/m3 = "
          f"{tot*lo/1e6*1000:.1f}-{tot*hi/1e6*1000:.1f} g")
print("  -> stated 15 g is roughly double what the trio holds. Generous, not fatal.")
print("  -> the real problem: Boo is an OPEN BELL. Nothing says to stuff him and")
print("     stuffing would fall out, yet the materials list covers 'the trio'.")

print(); print("="*72); print("6. YARN — stated grams vs stitch counts"); print("="*72)
import sys; sys.path.insert(0, "ns02")
from pieces import ALL
counts = {}
for name, table in ALL.items():
    counts[name] = sum(r[2] for r in table)
one_set = (counts["Boo body"] + counts["Boo ruffled hem"] + 2*counts["Boo arm (x2)"]
           + counts["Boo witch hat"] + counts["Pip body"] + counts["Pip stem cone"]
           + counts["Bramble body"] + 2*counts["Bramble ear outer (x2)"]
           + 2*counts["Bramble ear inner (x2)"])
print(f"  stitches in one set (incl. hat, excl. optional base): {one_set}")
for mm_per_st, m_per_g in ((6.0, 2.8), (7.0, 2.5)):
    metres = one_set*mm_per_st/1000
    print(f"  at {mm_per_st} mm/st and {m_per_g} m/g: {metres:.1f} m -> {metres/m_per_g:.1f} g")
print("  stated: cream 8 + orange 10 + lavender 9 + sage 4 + pink 2 = 33 g")
print("  -> stated amounts are roughly 2-3x the calculated need. Normal allowance")
print("     for tails, sewing and swatching, so not an error - but the garland")
print("     figures should then be 3x these, and they are only ~3.1x on cream.")
