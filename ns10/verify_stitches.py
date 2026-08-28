"""Check every stated stitch count in NS02 against the instructions.

sc / sl st / hdc / dc  -> 1 st in, 1 st out
inc                    -> 1 st in, 2 sts out
dec                    -> 2 sts in, 1 st out
(a, b, c) in next st   -> 1 st in, len(a,b,c) sts out   (a cluster)
picot                  -> 0 sts in, 1 st out
"""
import re, sys
sys.path.insert(0, "ns10")
from pieces import ALL

OPS = r'(?:sl st|sc|hdc|dc|inc|dec|picot)'

def eval_group(g, prev):
    """Evaluate one group. Returns (consumed, produced); sentinels -1/-2 mean
    'all available stitches'."""
    g = g.strip()
    low = g.lower().rstrip('.')
    if re.fullmatch(r'sc in each st around', low):  return -1, -1
    if re.fullmatch(r'inc in each st around', low): return -2, -2

    c = p = 0
    i = 0
    while i < len(g):
        m = re.match(r'\s*\(([^)]+)\)\s*in next st', g[i:])
        if m:
            inner = m.group(1)
            n = len(re.findall(OPS, inner))
            c += 1; p += n
            i += m.end(); continue
        m = re.match(r'\s*(?:(\d+)\s*)?(' + OPS + r')(?:\s+in\s+(?:next|first|last|each))?'
                     r'(?:\s*[x×]?\s*(\d+))?', g[i:])
        if m:
            lead, op, trail = m.group(1), m.group(2), m.group(3)
            n = int(lead) if lead else 1
            if trail: n *= int(trail)
            if   op == "sc":     c += n;   p += n
            elif op == "inc":    c += n;   p += 2*n
            elif op == "dec":    c += 2*n; p += n
            elif op == "picot":  pass
            else:                c += n;   p += n      # sl st / hdc / dc
            i += m.end(); continue
        i += 1
    return c, p

def eval_round(instr, prev):
    s = re.sub(r'\b(FLO|BLO)\s*:?', '', instr).strip()
    c = p = 0
    consumed_any = False
    m = re.search(r'\[([^\]]+)\]\s*[x×]\s*(\d+)', s)
    if m:
        inner, mult = m.group(1), int(m.group(2))
        gc, gp = eval_group(inner, prev)
        if gc == -1: return prev, prev*mult
        if gc == -2: return prev*2, prev*2*mult
        return gc*mult, gp*mult
    gc, gp = eval_group(s, prev)
    if gc == -1: return prev, prev
    if gc == -2: return prev*2, prev*2
    return gc, gp

total_rounds = 0; fails = 0
for name, table in ALL.items():
    print(f"\n=== {name} ===")
    prev = 0; bad = 0
    for rnd, instr, stated in table:
        if rnd == 1: prev = 0
        c, p = eval_round(instr, prev)
        ok = (p == stated)
        if not ok: bad += 1; fails += 1
        print(f"  {'OK  ' if ok else 'FAIL'} R{rnd:<2} produced={p:<3} stated=({stated:<3}) "
              f"consumed={c:<3} prev={prev:<3} [{instr[:54]}]")
        prev = stated
        total_rounds += 1
    if bad: print(f"  ^^ {bad} mismatch(es)")
print(f"\n########## NS02: {total_rounds} rounds, {fails} stitch-count mismatches ##########")
