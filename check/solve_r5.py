"""Find the R5 leg-join walk that maximises the front-back stagger,
subject to summing to exactly 30 stitches."""
print("R4 back legs are fixed by the increase round: centres at st 1.5 and 15.0")
print("R5 has 30 sts. Two 3-st joins; find the walk that staggers them best.\n")
print(f"{'walk (a,3,b,3,c)':<22}{'sum':>4}  {'F centres':<14}{'L-R gap':>9}"
      f"{'F-B stagger':>13}  {'footprint L-R x F-B':>22}")
best = None
for a in range(0, 25):
    for b in range(0, 25):
        c = 30 - (a + 3 + b + 3)
        if c < 0:
            continue
        f1 = a + 1.5
        f2 = f1 + 3 + b + 1.5
        lr = abs(f2 - f1)                       # front legs apart, sts
        # stagger = distance from a front centre to the nearer back centre
        stagger = min(abs(f1 - 1.5), abs(f1 - 15.0))
        if abs(lr - 15) > 1.0:                  # keep the pair roughly opposite
            continue
        key = (stagger, -abs(lr - 15))
        if best is None or key > best[0]:
            best = (key, (a, 3, b, 3, c), f1, f2, lr, stagger)
        print(f"{str((a,3,b,3,c)):<22}{a+3+b+3+c:>4}  {f1:>5.1f},{f2:<8.1f}"
              f"{lr*4.5:>7.1f}mm{stagger*4.5:>11.1f}mm"
              f"{lr*4.5:>11.1f} x {stagger*4.5:.1f} mm")
key, walk, f1, f2, lr, stagger = best
print(f"\nBEST: work {walk[0]} sc, join leg over 3, work {walk[2]} sc, "
      f"join leg over 3, work {walk[4]} sc  (sum={sum(walk)})")
print(f"  front-leg centres at st {f1} and {f2}")
print(f"  left-right span  {lr:.1f} sts = {lr*4.5:.1f} mm")
print(f"  front-back span  {stagger:.1f} sts = {stagger*4.5:.1f} mm")
print(f"  ratio {max(lr,stagger)/min(lr,stagger):.2f} : 1  (was 3.33 : 1)")
print(f"\n  CHECK my earlier claim '2 sc, leg/3, 6 sc, leg/3, 13 sc':")
print(f"    2+3+6+3+13 = {2+3+6+3+13}  -> WRONG, must equal 30")
