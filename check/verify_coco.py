"""Verify NS04 'Coco the Capybara': stitch arithmetic + geometry claims.

sc       -> consumes 1 st, produces 1 st
inc      -> consumes 1 st, produces 2 sts
invdec   -> consumes 2 sts, produces 1 st
"""
import math, re

def eval_round(instr, prev):
    """Return (consumed, produced) for one round given `prev` stitches available."""
    s = instr.strip()
    consumed = produced = 0
    # split top-level comma-separated segments
    segments, depth, cur = [], 0, ""
    for ch in s:
        if ch == "[":
            depth += 1; cur += ch
        elif ch == "]":
            depth -= 1; cur += ch
        elif ch == "," and depth == 0:
            segments.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        segments.append(cur.strip())

    for seg in segments:
        m = re.fullmatch(r'\[(?P<inner>.+)\]\s*x\s*(?P<mult>\d+)', seg, re.I)
        if m:
            inner, mult = m.group("inner"), int(m.group("mult"))
            c, p = eval_body(inner)
            consumed += c * mult; produced += p * mult
        else:
            c, p = eval_body(seg)
            consumed += c; produced += p
    return consumed, produced

def eval_body(body):
    b = body.strip().lower()
    consumed = produced = 0
    if "in mr" in b:                                   # e.g. "6 sc in MR"
        n = int(re.search(r'(\d+)\s*sc', b).group(1))
        return 0, n
    if re.fullmatch(r'sc in each st around', b):
        return -1, -1                                   # sentinel: "as many as available"
    if re.fullmatch(r'inc in each st around', b):
        return -2, -2                                   # sentinel: 2x available
    for tok in re.finditer(
            r'(?:(\d+)\s*)?(sc|inc|invdec|dec)(?:\s*x\s*(\d+))?', b):
        n = int(tok.group(1)) if tok.group(1) else 1
        op = tok.group(2)
        if tok.group(3):
            n *= int(tok.group(3))
        if op == "sc":
            consumed += n; produced += n
        elif op == "inc":
            consumed += n; produced += 2 * n
        else:                                           # invdec / dec
            consumed += 2 * n; produced += n
    return consumed, produced

PIECES = {
 "LEG (make 4)": [(1,"6 sc in MR",6),(2,"[1 sc, inc] x3",9),(3,"sc in each st around",9),
   (4,"sc in each st around",9),(5,"sc in each st around",9),(6,"sc in each st around",9),
   (7,"sc in each st around",9),(8,"sc in each st around",9)],
 "EAR (make 2)": [(1,"6 sc in MR",6),(2,"[1 sc, inc] x3",9),(3,"sc in each st around",9)],
 "MUZZLE (make 1)": [(1,"6 sc in MR",6),(2,"[1 sc, inc] x3",9),(3,"[2 sc, inc] x3",12),
   (4,"sc in each st around",12),(5,"sc in each st around",12)],
 "BODY & HEAD (make 1)": [(1,"6 sc in MR",6),(2,"inc in each st around",12),
   (3,"[1 sc, inc] x6",18),(4,"3 sc, [1 sc, inc] x3, 3 sc, [1 sc, inc] x3",24),
   (5,"[3 sc, inc] x6",30),(6,"[4 sc, inc] x6",36),(7,"sc in each st around",36),
   (8,"sc in each st around",36),(9,"sc in each st around",36),(10,"[7 sc, invdec] x4",32),
   (11,"[7 sc, inc] x4",36),(12,"sc in each st around",36),(13,"sc in each st around",36),
   (14,"sc in each st around",36),(15,"sc in each st around",36),(16,"[4 sc, invdec] x6",30),
   (17,"[3 sc, invdec] x6",24),(18,"[2 sc, invdec] x6",18),(19,"[1 sc, invdec] x6",12),
   (20,"invdec x6",6)],
}

grand_total_rounds = 0
grand_fails = 0
for name, table in PIECES.items():
    print(f"\n=== {name} ===")
    fails = 0
    for i, (rnd, instr, stated) in enumerate(table):
        prev = table[i-1][2] if i > 0 else 0
        c, p = eval_round(instr, prev)
        if c == -1: c, p = prev, prev            # "sc in each st around"
        elif c == -2: c, p = prev, prev * 2      # "inc in each st around"
        ok = (p == stated)
        if not ok: fails += 1
        print(f"  {'OK  ' if ok else 'FAIL'} R{rnd:<2} produced={p:<3} stated=({stated:<3})"
              f" consumed={c:<3} prev={prev:<3}  [{instr}]")
        grand_total_rounds += 1
    print(f"  -> {len(table)} rounds, {fails} mismatch(es)")
    grand_fails += fails

print(f"\n########## {grand_total_rounds} rounds checked, {grand_fails} stitch-count mismatches ##########")
