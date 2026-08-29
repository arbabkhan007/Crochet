"""Validate ALL_10_CROCHET_PATTERNS.md/.txt against the ten source client files.

Checks, per pattern:
  - every source line survives into the Markdown (whitespace-normalised)
  - every source word survives into BOTH files (catches dropped sentences
    even where formatting has changed)
  - every round/row (label, instruction, count) is present in both files
  - design codes present, no duplicated pattern blocks
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MD = (ROOT / "ALL_10_CROCHET_PATTERNS.md").read_text()
TXT = (ROOT / "ALL_10_CROCHET_PATTERNS.txt").read_text()
SOURCES = sorted(ROOT.glob("NS*_CLIENT.md"))

fails = []
def ck(cond, msg):
    if not cond:
        fails.append(msg)
        print(f"  FAIL {msg}")

GLYPH = str.maketrans({"\u00b7": "-", "\u2014": "--", "\u2013": "-", "\u2019": "'",
                       "\u2018": "'", "\u201c": '"', "\u201d": '"', "\u00d7": "x",
                       "\u2248": "~", "\u00a9": "(c)", "\u2026": "...",
                       "\u2192": "->"})


def canon(s):
    """Apply the same glyph map the builder uses, so source and TXT compare."""
    return re.sub(r"\s+", " ", s.translate(GLYPH)).strip()


def words(s):
    return re.findall(r"[a-z0-9]+", s.lower())

def rows(text):
    """(label, instruction, count) for markdown-style rows."""
    out = []
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*(\(\d+\)|\[\d+\])\s*\|",
                         text, re.M):
        lab, ins, cnt = m.groups()
        lab = re.sub(r"[*`]", "", lab).strip()
        ins = re.sub(r"[*`]", "", ins).strip()
        if re.fullmatch(r":?-{2,}:?", lab) or lab.lower() in ("rnd", "round", "row"):
            continue
        out.append((lab, ins, cnt))
    return out

def txt_rows(text):
    """Same rows out of the aligned plain-text tables: label  instruction  (n)."""
    out = []
    for ln in text.splitlines():
        m = re.match(r"^\s{0,2}(\S.*?)\s{2,}(\S.*?)\s{2,}(\(\d+\)|\[\d+\])"
                     r"(?:\s{2,}\S.*)?$", ln)
        if m:
            lab, ins, cnt = m.groups()
            if set(lab) <= {"-"} or lab.lower() in ("rnd", "round", "row"):
                continue
            out.append((lab.strip(), ins.strip(), cnt))
    return out

# split the consolidated files into per-pattern sections
def section(full, idx):
    start = full.index(f"PATTERN {idx} - " if full is TXT else f"# Pattern {idx} —")
    marker = ("COPYRIGHT & LICENSING REVIEW" if full is TXT
              else "## Copyright & Licensing Review")
    try:
        end = full.index(f"PATTERN {idx+1} - " if full is TXT else f"# Pattern {idx+1} —",
                         start)
    except ValueError:
        end = full.index(marker, start)      # must search AFTER start
    return full[start:end]

md_flat = re.sub(r"\s+", " ", MD)
print(f"{'code':<7} {'lines kept':>11} {'words src':>10} {'words md':>9} {'words txt':>10} "
      f"{'rows':>6} {'rows md':>8} {'rows txt':>9}")
for idx, f in enumerate(SOURCES, 1):
    code = re.match(r"(NS\d+)_", f.name).group(1)
    body = f.read_text()
    body_nc = re.sub(r"^#\s+DESIGN CODE\s+NS\s?\d+\s*$", "", body, flags=re.M)

    # 1. every source line present in the markdown
    kept = total = 0
    for ln in body_nc.splitlines():
        n = re.sub(r"\s+", " ", ln).strip()
        if not n or set(n) <= {"-", "|", " ", ":"} or re.fullmatch(r"#{1,6}\s*", n):
            continue
        total += 1
        # headings are demoted, so compare on the text after the #'s
        probe = re.sub(r"^#{1,6}\s*", "", n)
        if probe in md_flat:
            kept += 1
        else:
            ck(False, f"{code}: line missing from MD: {n[:70]!r}")

    # 2. every source word present in both files
    mds, txs = section(MD, idx), section(TXT, idx)
    sw = set(words(body_nc))
    miss_md, miss_txt = sw - set(words(mds)), sw - set(words(txs))
    ck(not miss_md, f"{code}: words missing from MD: {sorted(miss_md)[:8]}")
    ck(not miss_txt, f"{code}: words missing from TXT: {sorted(miss_txt)[:8]}")

    # 3. every round row present in both
    src_rows = rows(body_nc)
    md_rows, txt_r = rows(mds), txt_rows(txs)
    src_set = {(canon(l), canon(i), canon(c)) for l, i, c in src_rows}
    md_set = {(canon(l), canon(i), canon(c)) for l, i, c in md_rows}
    tx_set = {(canon(l), canon(i), canon(c)) for l, i, c in txt_r}
    ck(src_set <= md_set, f"{code}: rows missing from MD: {sorted(src_set - md_set)[:2]}")
    ck(src_set <= tx_set, f"{code}: rows missing from TXT: {sorted(src_set - tx_set)[:2]}")

    print(f"{code:<7} {kept:>5}/{total:<5} {len(words(body_nc)):>10} "
          f"{len(words(mds)):>9} {len(words(txs)):>10} {len(src_rows):>6} "
          f"{len(md_rows):>8} {len(txt_r):>9}")

# 4. structure
print()
ck(MD.count("\n# Pattern ") == 10, f"MD has {MD.count(chr(10)+'# Pattern ')} pattern headings, want 10")
ck(len(re.findall(r"^PATTERN \d+ - ", TXT, re.M)) == 10,
   f"TXT has {len(re.findall(r'^PATTERN ', TXT, re.M))} pattern headers, want 10")
for i in range(1, 11):
    ck(MD.count(f"# Pattern {i} —") == 1, f"Pattern {i} duplicated in MD")
    ck(len(re.findall(rf"^PATTERN {i} - ", TXT, re.M)) == 1, f"Pattern {i} duplicated in TXT")

# 5. design codes
print("design codes:")
for i, f in enumerate(SOURCES, 1):
    code = re.match(r"(NS\d+)_", f.name).group(1)
    spaced = code[:2] + " " + code[2:]
    in_md = f"# Pattern {i} — `{spaced}`" in MD
    in_txt = bool(re.search(rf"^PATTERN {i} - DESIGN CODE {spaced} - ", TXT, re.M))
    ck(in_md, f"{code}: design code missing from MD")
    ck(in_txt, f"{code}: design code missing from TXT")
    print(f"  {spaced}  MD={'Y' if in_md else 'N'}  TXT={'Y' if in_txt else 'N'}")

# 6. copyright and safety consistency
print("\ncopyright / safety:")
# scope these to the pattern sections; the review sections quote both strings
bodies_md = MD[:MD.index("## Copyright & Licensing Review")]
bodies_txt = TXT[:TXT.index("COPYRIGHT & LICENSING REVIEW", TXT.index("PATTERN 10 - "))]
# per-section: exactly the seven files that carry a notice must carry exactly one
HAVE = {"NS02", "NS04", "NS05", "NS06", "NS08", "NS09", "NS10"}
notice = "© Novality Store · Creation Studio"
per = {}
for idx, f in enumerate(SOURCES, 1):
    code = re.match(r"(NS\d+)_", f.name).group(1)
    per[code] = section(MD, idx).count(notice)
bad = {k: n_ for k, n_ in per.items() if n_ != (1 if k in HAVE else 0)}
ck(not bad, f"copyright notice counts wrong per pattern: {bad}")
ck("baby-safe certification" not in bodies_md and "baby-safe certification" not in bodies_txt,
   "the removed 'baby-safe certification' claim is back inside a pattern")
ck("**" not in TXT, f"unconverted markdown bold left in the TXT ({TXT.count('**')} x)")
ck("## Copyright & Licensing Review" in MD and "COPYRIGHT & LICENSING REVIEW" in TXT,
   "copyright review section missing")
ck("## Final Review Summary" in MD and "FINAL REVIEW SUMMARY" in TXT,
   "final review summary missing")
print(f"  copyright notices per pattern: "
      f"{sum(1 for x in per.values() if x == 1)} patterns with exactly one "
      f"(expect {len(HAVE)})")
print(f"  'baby-safe' mentions kept: MD={MD.count('baby-safe')} TXT={TXT.count('baby-safe')}")
print(f"  'Unknown — manual verification required' cells: {MD.count('Unknown — manual verification required')}")

print("\n" + "=" * 70)
print(f"FAIL - {len(fails)} problem(s)" if fails else "PASS - both files match all ten sources")
sys.exit(1 if fails else 0)
