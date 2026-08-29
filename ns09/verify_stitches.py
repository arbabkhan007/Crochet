"""Check every stated stitch count in NS01 Hamish against its instructions.

dec is an invisible decrease: 2 sts in, 1 st out.
BLO sc around is still one sc per stitch.
"""
import re, sys
sys.path.insert(0, "ns09")
from pieces import ALL

OPS = r'(?:sl st|invdec|dec|sc|hdc|dc|inc|picot)'


def eval_group(g):
    """One group -> (consumed, produced). -1/-2 = 'all stitches'."""
    g = g.strip()
    low = g.lower().rstrip('.')
    if re.fullmatch(r'(?:blo\s+)?sc (?:in each st )?around', low):  return -1, -1
    if re.fullmatch(r'inc in each st around', low):                 return -2, -2
    m = re.fullmatch(r'(\d+)\s+sc\s+in\s+(?:mr|magic ring)', low)
    if m:  return 0, int(m.group(1))

    c = p = 0
    i = 0
    while i < len(g):
        m = re.match(r'\s*'+OPS+r'(?:\s+in\s+(?:each st around|next st))?\s*$', g[i:])
        if m:
            op = m.group(0).strip().lower()
            if   op == "sc":                c += 1; p += 1
            elif op in ("invdec", "dec"):   c += 2; p += 1
            elif op == "inc":               c += 1; p += 2
            elif op == "picot":             p += 1
            i += m.end(); continue
        # a cluster: (sc, hdc, hdc, sc) in next st -> 1 st in, len(group) sts out
        m = re.match(r'\s*\(([^)]+)\)\s*in\s+next\s+st', g[i:])
        if m:
            n = len(re.findall(OPS, m.group(1)))
            c += 1; p += n
            i += m.end(); continue
        # "sc in next 5" -> 5 sc
        m = re.match(r'\s*(' + OPS + r')\s+in\s+next\s+(\d+)', g[i:])
        if m:
            op, n = m.group(1).lower(), int(m.group(2))
            if   op == "sc":              c += n;   p += n
            elif op in ("invdec","dec"):  c += 2*n; p += n
            elif op == "inc":             c += n;   p += 2*n
            i += m.end(); continue
        m = re.match(r'\s*(?:(\d+)\s+)?(' + OPS + r')(?:\s+in\s+(?:next st|each st around))?'
                     r'(?:\s*[x×]\s*(\d+))?', g[i:])
        if m:
            n, op = int(m.group(1) or 1), m.group(2).lower()
            if m.group(3):
                n *= int(m.group(3))
            if   op == "sc":              c += n;   p += n
            elif op in ("invdec","dec"):  c += 2*n; p += n
            elif op == "inc":             c += n;   p += 2*n
            elif op == "picot":           p += n
            i += m.end(); continue
        m = re.match(r'\s*[,;]\s*', g[i:])
        if m:
            i += m.end(); continue
        raise ValueError(f"cannot parse {g[i:]!r} in {g!r}")
    return c, p


def split_top(s):
    """Split on commas that are not inside [brackets] or (parentheses).
    Both matter here: clusters are written (sc, hdc, sc) in next st."""
    parts, depth, buf = [], 0, ""
    for ch in s:
        if ch in "[(":
            depth += 1; buf += ch
        elif ch in "])":
            depth -= 1; buf += ch
        elif ch == "," and depth == 0:
            parts.append(buf); buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf)
    return [p.strip() for p in parts if p.strip()]


def eval_seq(instr, prev):
    """Comma-separated sequence of groups, brackets allowed -> (consumed, produced)."""
    total_c = total_p = 0
    for part in split_top(instr.strip().rstrip('.')):
        m = re.match(r'^\[(.+?)\]\s*[x×]\s*(\d+)\s*$', part, re.I)
        if m:
            c = p = 0
            for sub in split_top(m.group(1)):
                sc, sp = eval_group(sub)
                if sc < 0:
                    raise ValueError(f"sentinel inside bracket: {sub!r}")
                c += sc; p += sp
            total_c += c*int(m.group(2)); total_p += p*int(m.group(2))
        else:
            c, p = eval_group(part)
            if   c == -1: total_c += prev; total_p += prev
            elif c == -2: total_c += prev; total_p += 2*prev
            else:         total_c += c;    total_p += p
    return total_c, total_p


def eval_round(instr, prev):
    return eval_seq(instr, prev)


if __name__ == "__main__":
    from pieces import ALL, BUMPS_CLAIM, BUMPS_ROW
    total = bad = 0
    for name, (rows, copies) in ALL.items():
        prev = 0
        print(f"--- {name} (make {copies}) ---")
        for idx, (label, instr, stated, note) in enumerate(rows):
            if idx == 0:
                prev = 0
            try:
                c, p = eval_round(instr, prev)
            except ValueError as e:
                print(f"  {label:<8} PARSE ERROR {e}"); bad += 1; total += 1; continue
            cons_ok = (c == prev) or (c == 0 and prev == 0) or (idx == 0)
            ok = (p == stated)
            if not ok or not cons_ok:
                bad += 1
            cons = "" if cons_ok else f"   [consumes {c}, prev had {prev}]"
            shown = instr if len(instr) < 60 else instr[:57] + "..."
            print(f"  {label:<8} {shown:<60} stated ({stated:>3}) produced {p:>3} "
                  f"consumed {c:>3}  {'OK' if ok and cons_ok else 'MISMATCH'}{cons}")
            prev = stated
            total += 1
        print()

    print("--- the pattern's own claim about the bump round ---")
    # the claim is a plain sum, so add it directly rather than through the parser
    terms = [int(x) for x in BUMPS_CLAIM["note"].split("=")[0].split("+")]
    print(f"    {BUMPS_CLAIM['note']}")
    print(f"    terms {terms} sum to {sum(terms)}; pattern claims "
          f"{BUMPS_CLAIM['consumed']}")
    c, p = eval_round(BUMPS_ROW[0][1], 24)
    print(f"    the instruction itself: consumes {c}, produces {p}  "
          f"(pattern claims {BUMPS_CLAIM['consumed']} and {BUMPS_CLAIM['produced']})")
    if sum(terms) != BUMPS_CLAIM["consumed"] or (c, p) != (24, 35):
        bad += 1; print("    MISMATCH")
    runs = BUMPS_CLAIM["plain_runs"]
    print(f"    plain runs {runs} sum to {sum(runs)}; + 5 bumps = {sum(runs)+5} "
          f"(must equal 24)")
    if sum(runs) + 5 != 24:
        bad += 1; print("    MISMATCH")
    print(f"    troubleshooting says '3, 4, 3, 4, 3, then 2 at the end' -> "
          f"{'MATCHES' if runs == [3,4,3,4,3,2] else 'DOES NOT MATCH'}")

    print("=" * 70)
    print(f"NS09 Shelby: {total} rounds/rows checked, {bad} problems")
    print("PASS" if bad == 0 else "FAIL")
    sys.exit(0 if bad == 0 else 1)
