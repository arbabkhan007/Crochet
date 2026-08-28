"""Verify the shipped corrected pattern, with correct circular arithmetic."""
import re, pathlib, math

src = pathlib.Path("check/verify_coco.py").read_text().split("PIECES = {")[0]
src = src.replace(r"\]\s*x\s*(?P<mult>\d+)", r"]\s*[x×]\s*(?P<mult>\d+)")
src = src.replace(r"(?:\s*x\s*(\d+))?", r"(?:\s*[x×]\s*(\d+))?")
ns = {}; exec(src, ns); eval_round = ns["eval_round"]

md = pathlib.Path("NS04_Coco_the_Capybara_CORRECTED.md").read_text()
rows = re.findall(r'^\|\s*(R\d+)\s*\|([^|]+?)\|\s*\((\d+)\)\s*\|', md, re.M)
print(f"parsed {len(rows)} round rows\n")
prev = 0; fails = 0
for label, instr, stated in rows:
    instr = instr.strip(); stated = int(stated)
    if int(label[1:]) == 1: prev = 0
    c, p = eval_round(instr, prev)
    if c == -1:   c, p = prev, prev
    elif c == -2: c, p = prev, prev * 2
    if p != stated: fails += 1
    print(f"  {'OK  ' if p==stated else 'FAIL'} {label:<4} produced={p:<3} stated=({stated:<3})  [{instr}]")
    prev = stated
print(f"\n########## {len(rows)} rounds, {fails} mismatches ##########")

def gap(a, b, n):        # forward distance a->b on an n-stitch circle
    return (b - a) % n

print("\n=== R5 walk 7, 3, 10, 3, 7 (circular) ===")
w = [7, 3, 10, 3, 7]; assert sum(w) == 30
back  = [1.5, 15.0]                 # R4 centres
f1    = w[0] + 1.5                  # 8.5
f2    = f1 + w[1] + w[2] + 1.5      # 21.5
print(f"  sum = {sum(w)} -> OK   front centres st {f1}, {f2}")
lr = min(gap(f1, f2, 30), gap(f2, f1, 30))
print(f"  left-right  = min({gap(f1,f2,30)}, {gap(f2,f1,30)}) = {lr} sts = {lr*4.5:.1f} mm")
stag = min(gap(back[0], f1, 30), gap(f1, back[1], 30))
print(f"  front-back  = min({gap(back[0],f1,30)}, {gap(f1,back[1],30)}) = {stag} sts = {stag*4.5:.1f} mm")
print(f"  ratio {lr/stag:.2f}:1")
print("  --- original walk (2, 3, 12, 3, 10) for comparison ---")
g1 = 2 + 1.5; g2 = g1 + 3 + 12 + 1.5
lro = min(gap(g1, g2, 30), gap(g2, g1, 30))
sto = min(gap(back[0], g1, 30), gap(g1, back[1], 30))
print(f"  centres st {g1}, {g2}; left-right {lro} sts = {lro*4.5:.1f} mm; "
      f"front-back {sto} sts = {sto*4.5:.1f} mm; ratio {lro/sto:.2f}:1")

print("\n=== leg lengths (front = longer pair) ===")
for name, rnds, join in (("front @R5", 9, 5), ("back  @R4", 8, 4)):
    print(f"  {name}: {rnds} rnd = {rnds*4.3:.1f} mm, joins {join*4.3:.1f} mm up "
          f"-> foot {rnds*4.3 - join*4.3:.1f} mm below body base")
print(f"  total height = {20*4.3:.1f} + {9*4.3-5*4.3:.1f} = {20*4.3 + (9*4.3-5*4.3):.1f} mm")

print("\n=== ears ===")
for rnd, sts in ((15, 36), (16, 30)):
    circ = sts * 4.5
    for sep in (5, 7):
        print(f"  R{rnd}: {sep} sts = {sep*4.5:.1f} mm = {sep*4.5/circ*360:.0f} deg")
print("\n=== eyes / muzzle ===")
mz, ey = 12*4.5/math.pi, 6*4.5
print(f"  muzzle {mz:.1f} mm, eyes {ey:.1f} mm apart -> {(ey-mz)/2:.1f} mm clearance")
