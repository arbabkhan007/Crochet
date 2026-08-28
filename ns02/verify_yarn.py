import sys; sys.path.insert(0, "ns02")
from pieces import ALL
c = {k: sum(r[2] for r in v) for k, v in ALL.items()}

# DK cotton ~250 m per 50 g = 5.0 m/g. Yarn consumed per sc on 2.5 mm DK:
# a stitch wraps roughly pi x hook dia + legs + take-up -> ~16 mm.
M_PER_G, MM_ST = 5.0, 16.0
g = lambda sts: sts * MM_ST / 1000 / M_PER_G

boo  = c["Boo body"] + c["Boo ruffled hem"] + 2*c["Boo arm (x2)"]
hat  = c["Boo witch hat"]
pip  = c["Pip body"]
stem = c["Pip stem cone"] + 45          # cone + tendril + leaf allowance
bram = c["Bramble body"]
ears = 2*c["Bramble ear outer (x2)"]    # lavender outers only
pink = 2*c["Bramble ear inner (x2)"]

print(f"  consumption assumed: {MM_ST} mm of yarn per sc, {M_PER_G} m/g for DK cotton\n")
print(f"  {'colour / piece':<26}{'sts':>6}{'calc g':>8}{'stated':>8}{'allowance':>11}")
for n, s, stated in [("cream - Boo + hat", boo+hat, 8), ("orange - Pip", pip, 10),
                     ("lavender - Bramble + ears", bram+ears, 9),
                     ("sage - stem/tendril/leaf", stem, 4), ("pink - 2 ear linings", pink, 2)]:
    print(f"  {n:<26}{s:>6}{g(s):>8.1f}{stated:>8}{stated/g(s):>10.0f}x")
tot_c = g(boo+hat+pip+stem+bram+ears+pink)
print(f"\n  calculated total {tot_c:.1f} g, stated total 33 g -> {33/tot_c:.1f}x overall")
print("  -> every figure is generous by roughly an order of magnitude. A customer")
print("     buying 50 g balls will have most of each ball left over. Not an error,")
print("     but '~8 g' reads as a measured quantity when it is really 'one ball,")
print("     most of it unused'. Worth rewording rather than renumbering.")
