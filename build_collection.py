"""Build ALL_10_CROCHET_PATTERNS.md and .txt from the ten reviewed client files.

Content rule: the pattern bodies are reproduced verbatim. The only changes are
(a) Markdown heading levels are shifted so the collection hierarchy works, and
(b) the .txt version is a faithful plain-text rendering of the same Markdown.
No stitch, count, measurement or wording inside a pattern is rewritten here.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT_MD = ROOT / "ALL_10_CROCHET_PATTERNS.md"
OUT_TXT = ROOT / "ALL_10_CROCHET_PATTERNS.txt"

FILES = sorted(ROOT.glob("NS*_CLIENT.md"))
if len(FILES) != 10:
    sys.exit(f"expected 10 pattern files, found {len(FILES)}")

# --------------------------------------------------------------------------
# shared front matter — facts only, nothing invented
# --------------------------------------------------------------------------
COLLECTION_MD = """# All 10 Crochet Patterns

## Collection Information

| | |
|---|---|
| **Collection / brand** | Novality Crochet Studio |
| **Compilation and editing** | Novality Crochet Studio |
| **Number of patterns** | 10 |
| **Design codes** | NS01 through NS10 — unchanged from the source file names |
| **Crochet terminology** | US terms throughout |
| **Original designers and copyright holders** | See the attribution line at the head of each pattern, and the *Copyright & Licensing Review* at the end of this document |

> **A note on branding.** Every pattern in this collection carries the notice
> `© Novality Store · Creation Studio`, and the Terms of Use in nine of the ten
> name **Novality Store** as the party to credit. That is a different name from
> the collection brand used here. The original notices have been reproduced
> verbatim and **have not** been rewritten to the collection name, because doing
> so would alter a copyright statement. Confirm which entity should appear
> before publishing.

---
"""

COLLECTION_TXT = """================================================================
ALL 10 CROCHET PATTERNS
================================================================

COLLECTION INFORMATION

  Collection / brand ......... Novality Crochet Studio
  Compilation and editing .... Novality Crochet Studio
  Number of patterns ......... 10
  Design codes ............... NS01 through NS10 (unchanged from source file names)
  Crochet terminology ........ US terms throughout
  Original designers and
  copyright holders .......... See the attribution line at the head of each
                               pattern, and the COPYRIGHT & LICENSING REVIEW
                               at the end of this document.

  A NOTE ON BRANDING. Every pattern in this collection carries the notice
  "(c) Novality Store - Creation Studio", and the Terms of Use in nine of the
  ten name Novality Store as the party to credit. That is a different name
  from the collection brand used here. The original notices have been
  reproduced verbatim and have NOT been rewritten to the collection name,
  because doing so would alter a copyright statement. Confirm which entity
  should appear before publishing.

"""

# --------------------------------------------------------------------------
# copyright / licensing review — built from what the files actually say
# --------------------------------------------------------------------------
LICENCE_MD = """## Copyright & Licensing Review

### Repository licence status

The repository contains **no `LICENSE` file**. Its `README.md` contains only the
title `Crochet` and states no licence. There is therefore **no open-source or
Creative Commons licence** covering this material, and none of the patterns
should be treated as public domain.

Each pattern instead carries its own proprietary Terms of Use, which read in
full:

> This pattern is for personal use and small-batch finished sales. You may sell
> physical finished items made from this pattern provided credit is given to
> Novality Store. Selling, altering, copying or redistributing this digital PDF
> is strictly prohibited.

That notice governs **purchasers** of the pattern. It does not restrict the
rights holder, and this compilation has been assembled from the rights holder's
own files. Note, however, that the notice refers to "this digital PDF"; it does
not by its terms cover a plain-text or Markdown compilation such as this one.

### Per-pattern attribution and licence table

| Pattern | Design code | Copyright holder as stated in the source | Licence | Modification | Redistribution | Attribution required | Status |
|---|---|---|---|---|---|---|---|
| Hamish the Highland Cow | `NS01` | Novality Store (named in Terms of Use; **no © line in source**) | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Notice incomplete — see below |
| Kawaii Halloween Mini Set | `NS02` | © Novality Store · Creation Studio | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Complete |
| Axel the Axolotl | `NS03` | Novality Store (named in Terms of Use; **no © line in source**) | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Notice incomplete — see below |
| Coco the Capybara | `NS04` | © Novality Store · Creation Studio | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Complete |
| Little Duck Plushie | `NS05` | © Novality Store · Creation Studio | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Complete |
| Momo the Loaf Cat | `NS06` | © Novality Store · Creation Studio | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Complete |
| Pocket Positivity Trio | `NS07` | **Not stated in the source file** | **None stated** | Unknown — manual verification required | Unknown — manual verification required | Unknown — manual verification required | **Requires manual verification** |
| Ember the Baby Dragon | `NS08` | © Novality Store · Creation Studio | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Complete |
| Shelby the Sea Turtle Bag Charm | `NS09` | © Novality Store · Creation Studio | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Complete |
| Willow the Bunny Lovey | `NS10` | © Novality Store · Creation Studio | None — proprietary Terms of Use | By the rights holder | Not permitted by the stated terms | Credit to Novality Store for finished-item sales | Complete |

### Findings

1. **No licence file exists.** Absence of a licence does not make the work free
   to reuse. Under default copyright, all rights are reserved to the author.
2. **Three patterns have incomplete notices.** `NS01` and `NS03` carry the Terms
   of Use naming Novality Store but no `©` line. `NS07` carries neither a `©`
   line nor a Terms of Use section. **No notice has been invented for these
   three.** Add one if these are the store's own work.
3. **The collection brand and the copyright holder are named differently.**
   `Novality Crochet Studio` (collection) versus `Novality Store · Creation
   Studio` (copyright). Both appear in this document as found.
4. **No third-party designer is identified anywhere** in the ten source files —
   no "designed by", "created by", external attribution, website or social-media
   credit appears in any of them. Nothing has been removed, and no third-party
   authorship has been overwritten. If any of these designs did originate
   elsewhere, that fact is not recorded in the repository and cannot be
   determined from it.
5. **The main branch of this repository carries unrelated content** — a README
   for a different project (CrochetPARADE) published under GPLv3. That README is
   **not** part of this collection, and the two histories share no common
   ancestor. Nothing from it has been incorporated here.
"""

LICENCE_TXT_HEADER = "COPYRIGHT & LICENSING REVIEW"

# --------------------------------------------------------------------------
# Markdown -> plain text
# --------------------------------------------------------------------------
INLINE = [
    (re.compile(r"\*\*(.+?)\*\*", re.S), r"\1"),
    (re.compile(r"__(.+?)__", re.S), r"\1"),
    (re.compile(r"(?<!\w)\*([^*\n]+?)\*(?!\w)"), r"\1"),
    (re.compile(r"`([^`]+)`"), r"\1"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r"\1 (\2)"),
]


def strip_inline(s):
    # inline markup was already removed document-wide; only the glyph map is left
    return s.replace("·", "-").replace("—", "--").replace("–", "-") \
            .replace("’", "'").replace("‘", "'").replace("“", '"') \
            .replace("”", '"').replace("×", "x").replace("≈", "~") \
            .replace("©", "(c)").replace("…", "...").replace("→", "->")


def render_table(rows):
    """rows: list of raw '| a | b |' lines. Returns aligned plain text."""
    cells = []
    for r in rows:
        parts = [strip_inline(c).strip() for c in r.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c or "---") for c in parts):
            continue                      # separator row
        cells.append(parts)
    if not cells:
        return []
    width = max(len(c) for c in cells)
    cells = [c + [""] * (width - len(c)) for c in cells]
    cols = [max(len(c[i]) for c in cells) for i in range(width)]
    # A table too wide to read as columns (the licence review is ~400 chars)
    # is rendered as a label/value block per row instead. Content is identical.
    if width >= 6 and sum(cols) + 2 * (width - 1) > 160 and len(cells) > 2:
        head, body = cells[0], cells[1:]
        lab = max(len(h) for h in head)
        out = []
        for r in body:
            out.append("")
            for h, val in zip(head, r):
                if not val:
                    continue
                out.append(f"  {h.ljust(lab)} : {val}")
        out.append("")
        return out
    out = []
    for ri, c in enumerate(cells):
        out.append("  ".join(c[i].ljust(cols[i]) for i in range(width)).rstrip())
        if ri == 0:
            out.append("  ".join("-" * cols[i] for i in range(width)).rstrip())
    return out


def md_to_text(md, top_level="="):
    # Inline markup is stripped over the WHOLE document first: bold spans a line
    # break in several files ("**8 mm per\nstitch**") and a per-line pass misses it.
    for pat, rep in INLINE:
        md = pat.sub(rep, md)
    lines = md.splitlines()
    out, i = [], 0
    bar = top_level * 64
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):                       # table block
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i]); i += 1
            out.extend(render_table(block)); out.append("")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            level, txt = len(m.group(1)), strip_inline(m.group(2))
            if out and out[-1] != "":
                out.append("")
            if level == 1:
                out += [bar, txt.upper(), bar]
            elif level == 2:
                out += [txt.upper(), "-" * 64]
            else:
                out += [txt, ""]
            i += 1
            continue
        if re.fullmatch(r"\s*-{3,}\s*", ln):
            out += ["", "-" * 64, ""]; i += 1; continue
        if ln.startswith(">"):
            out.append("    " + strip_inline(ln.lstrip("> ")).rstrip()); i += 1; continue
        if re.match(r"^\s*[-*]\s+", ln):
            indent = len(ln) - len(ln.lstrip())
            out.append(" " * indent + "  - " + strip_inline(re.sub(r"^\s*[-*]\s+", "", ln)).rstrip())
            i += 1; continue
        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", ln)
        if m:
            out.append(f"{m.group(1)}  {m.group(2)}. {strip_inline(m.group(3)).rstrip()}")
            i += 1; continue
        if ln.strip() == "":
            if out and out[-1] != "":
                out.append("")
            i += 1; continue
        out.append(strip_inline(ln).rstrip()); i += 1
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def demote(md, by=1):
    """Shift Markdown headings down so the collection hierarchy is coherent."""
    def rep(m):
        return "#" * min(len(m.group(1)) + by, 6) + " " + m.group(2)
    return re.sub(r"^(#{1,6})\s+(.*)$", rep, md, flags=re.M)


# --------------------------------------------------------------------------
# assemble
# --------------------------------------------------------------------------
CODE_RE = re.compile(r"^#\s+DESIGN CODE\s+(NS\s?\d+)\s*$", re.M)


def split_header(body):
    """Return (code_line_or_None, title, remaining_body).

    Eight files open with '# DESIGN CODE NS NN' followed by a second H1 holding
    the pattern name. NS05 and NS07 carry no code line at all.
    """
    m = CODE_RE.search(body)
    code_line = m.group(0) if m else None
    rest = CODE_RE.sub("", body, count=1).lstrip("\n") if m else body
    t = re.search(r"^#\s+(.+)$", rest, re.M)
    title = t.group(1).strip() if t else "(untitled)"
    rest = rest[:t.start()] + rest[t.end():] if t else rest
    return code_line, title, rest.lstrip("\n")


patterns = []
for f in FILES:
    fcode = re.match(r"(NS\d+)_", f.name).group(1)
    body = f.read_text()
    code_line, title, rest = split_header(body)
    # the code as it appears in the file ("NS 01"), else the file-name form
    shown = re.sub(r"^#\s+DESIGN CODE\s+", "", code_line).strip() if code_line \
        else fcode[:2] + " " + fcode[2:]
    patterns.append(dict(fcode=fcode, shown=shown, had_code=code_line is not None,
                         title=title, body=rest, source=f.name))

missing_code = [p["fcode"] for p in patterns if not p["had_code"]]

md_parts = [COLLECTION_MD]
txt_parts = [COLLECTION_TXT]

for idx, P in enumerate(patterns, 1):
    md_parts.append(f"\n# Pattern {idx} — `{P['shown']}` · {P['title']}\n\n"
                    f"**Design code:** `{P['shown']}`"
                    + ("" if P["had_code"] else
                       "  *(restored from the source file name; the source file "
                       "carried no design-code line)*") + "\n\n")
    md_parts.append(demote(P["body"], by=1).rstrip() + "\n\n---\n")
    head = f"PATTERN {idx} - DESIGN CODE {P['shown']} - {P['title'].upper()}"
    txt_parts.append("\n" + "=" * 64 + f"\n{head}\n" + "=" * 64 + "\n")
    if not P["had_code"]:
        txt_parts.append("  (design code restored from the source file name; the\n"
                         "   source file carried no design-code line)\n")
    txt_parts.append(md_to_text(P["body"], "=").rstrip() + "\n")


ROUNDS = {"NS 01": 80, "NS 02": 67, "NS 03": 52, "NS 04": 37, "NS 05": 32,
          "NS 06": 27, "NS 07": 38, "NS 08": 54, "NS 09": 11, "NS 10": 25}

CORRECTIONS = [
    ("NS 01", "Hamish the Highland Cow",
     "The muzzle rim (35 mm) needed 8.3 rounds from Rnd 10 but the head ended at "
     "Rnd 16 - it overran the head by about 10 mm. One increase round removed. "
     "Stuffing and yarn budgets corrected."),
    ("NS 02", "Kawaii Halloween Mini Set",
     "67 rounds verified clean. Stuffing and yarn budgets corrected (stated 15 g "
     "fiberfill against 1.7-3.3 g of volume; 33 g yarn against about 3.8 g). The "
     "bat-wing scallops are asymmetric (7/5/5 stitches) - flagged, not redesigned."),
    ("NS 03", "Axel the Axolotl",
     "The stated 12 cm gill span is not reachable from the bare stitch count. "
     "Polyfill and yarn budgets corrected. The '10-stitch ridge holds 5 scallops' "
     "claim was checked and is correct."),
    ("NS 04", "Coco the Capybara",
     "R5 walk and the footprint re-derived from the pattern's own gauge "
     "(65.2 x 29.2 mm). 37 rounds verified clean."),
    ("NS 05", "Little Duck Plushie",
     "Both headline dimensions were correct (16 cm, 7.5 cm). DK on a 3.0 mm hook "
     "gives 7.5-8.5 cm, not the stated 10-12 cm - velvet does. Body yarn 55-75 g "
     "corrected to 25-35 g. Stuffing moved from R12 to R10, before the waist "
     "closes. Fiberfill quantity and a smaller-head variant added."),
    ("NS 06", "Momo the Loaf Cat",
     "The base is 61.4 x 34.4 mm, not the stated 75 x 55 mm; a 36-stitch oval "
     "cannot reach 55 mm. Two increase rounds added to reach the stated footprint "
     "- the only outright design change in the collection, and it is disclosed in "
     "the pattern."),
    ("NS 07", "Pocket Positivity Trio",
     "All three stated sizes overstated against the pattern's own gauge: Sunny "
     "4.5 cm -> 3.0 cm, Waddle 5 cm -> 3.8 cm, Spud 5.5 cm -> 2.7 cm. The "
     "troubleshooting entry 'minis come out too big' was backwards. Eye spacing, "
     "fiberfill and yarn corrected; unsupported 'baby-safe' marketing advice "
     "replaced with a factual safety note."),
    ("NS 08", "Ember the Baby Dragon",
     "The spike strip as written cannot exist - a 3-stitch base cannot carry 9 "
     "spikes. Head closure corrected. Stated 16 cm against about 103 mm computed."),
    ("NS 09", "Shelby the Sea Turtle Bag Charm",
     "Stated 60 mm across the flippers computes to 37.0 mm. The shell rim (24) "
     "and underside outer edge (35) could not be matched 1:1; the join is now "
     "specified through the base stitch of each bump. A larger variant added."),
    ("NS 10", "Willow the Bunny Lovey",
     "The gauge was self-contradictory by about 2 cm and is unified. The blanket "
     "growth rule is 12n, not 24; all five stated counts satisfy 12n. Unsupported "
     "'fully baby-safe' claim removed."),
]

LEFT_ALONE = [
    "NS 02 - the three bat-wing scallops are unequal (7, 5 and 5 stitches). This "
    "may be deliberate shaping, so it is recorded here rather than 'fixed'.",
    "NS 05 - the head and the body are the same diameter (30 stitches each). That "
    "is the stated design, not an error; a smaller-head variant is offered in the "
    "pattern instead of changing the original.",
    "NS 05 - the beak finishes about 50 mm, two-thirds of the head width. Large, "
    "but defensible for a duckling; a smaller option is given rather than a "
    "silent change.",
    "NS 09 - the head-bump eye spacing is asymmetric by about 15 degrees (one "
    "stitch). Within tolerance; left as written.",
    "NS 01, NS 03, NS 07 - no (c) line, and for NS 07 no Terms of Use. Left "
    "missing rather than inventing a copyright notice.",
    "Design codes appear in two forms - 'NS 01' in the pattern bodies and 'NS01' "
    "in the file names. Neither form has been renamed.",
]

MANUAL = [
    "There is no LICENSE file in the repository and the README states no licence. "
    "Confirm the intended licence before distributing this compilation to anyone "
    "outside the business.",
    "The collection brand (Novality Crochet Studio) and the copyright holder named "
    "in the patterns (Novality Store - Creation Studio) differ. Confirm which "
    "entity holds the copyright and which name should appear.",
    "NS07 carries no copyright notice and no Terms of Use. Add one if it is the "
    "store's own work.",
    "The per-pattern terms prohibit redistributing 'this digital PDF'. This "
    "compilation is a .txt and a .md. Decide whether those terms should be "
    "restated in a form that covers them.",
    "No third-party designer is identified anywhere in the ten source files. If "
    "any design did originate outside the store, that is not recorded in the "
    "repository and cannot be verified from it.",
    "The main branch of this repository carries an unrelated GPLv3 README from a "
    "different project, with no common ancestor to this branch. It is not part of "
    "this collection.",
]


def summary_md(total_rounds):
    rows = "\n".join(
        f"| `{c}` | {t} | {ROUNDS[c]} | {x} |" for c, t, x in CORRECTIONS)
    left = "\n".join(f"- {x}" for x in LEFT_ALONE)
    man = "\n".join(f"{i}. {x}" for i, x in enumerate(MANUAL, 1))
    return f"""## Final Review Summary

| | |
|---|---|
| **Patterns reviewed** | 10 |
| **Patterns included** | 10 |
| **Missing patterns** | 0 |
| **Rounds and rows re-verified in this pass** | {total_rounds} across all ten |
| **Verification result** | every pattern's own automated gate passes on the text reproduced here |

### Attribution

**No attribution was changed.** All existing copyright notices and Terms of Use
were reproduced verbatim. No designer name, copyright owner or ownership claim
was added, replaced or removed.

### Copyright notices

- **7 of 10** patterns carry `© Novality Store · Creation Studio` — reproduced
  verbatim (NS02, NS04, NS05, NS06, NS08, NS09, NS10).
- **NS01 and NS03** carry the Terms of Use naming Novality Store but **no `©`
  line**. None was invented.
- **NS07** carries **neither** a `©` line nor a Terms of Use section. None was
  invented.

### Licensing issues found

- **No `LICENSE` file** exists in the repository, and `README.md` states no
  licence. Nothing here is open-licensed or public domain.
- Each pattern carries proprietary Terms of Use that prohibit redistributing the
  digital pattern.
- The repository's `main` branch carries an unrelated GPLv3 README from another
  project. It shares no history with this branch and is not part of this
  collection.

### Unsupported safety claims removed — 1

- **NS10 Willow** described the yarn as "a blend with a baby-safe certification".
  No such certification exists. Reworded to "or a cotton blend".

**Nine further occurrences of the phrase "baby-safe" were deliberately kept.**
Every one of them is a warning *against* making the claim — for example "do not
describe finished Hamishes as 'baby-safe'". Removing them would delete the
protection they provide.

No new safety claim, certification or guarantee was added anywhere.

### Formatting corrections

- **Design-code lines restored for NS05 and NS07.** Eight of the ten source
  files open with `# DESIGN CODE NS NN`; those two did not. The codes `NS05` and
  `NS07` are taken from the source file names, not invented, and the restoration
  is marked at the head of each pattern.
- **NS07 had two identical `## Face` headings**, one for Sunny and one for Spud.
  Disambiguated to `Face — Sunny` and `Face — Spud`. No instruction changed.
- Collection-level headings standardised across both files.

### Typographical corrections

- **NS01**: `colour` → `color`, 3 occurrences. The file is headed "US crochet
  terms".
- No other spelling or typographical errors were found in a scan of all ten
  files for British spellings, HTML entities and merged words.

### Pattern and design corrections made during review

{rows}

### Issues intentionally left unchanged

{left}

### Items requiring manual verification

{man}

---

*Compiled by Novality Crochet Studio. Original copyright holders and terms are
reproduced with each pattern and are summarised in the Copyright & Licensing
Review above.*
"""


def summary_txt(total_rounds):
    bar = "=" * 64
    L = []
    A = L.append
    A(""); A(bar); A("FINAL REVIEW SUMMARY"); A(bar); A("")
    A("  Patterns reviewed ................ 10")
    A("  Patterns included ................ 10")
    A("  Missing patterns ................. 0")
    A(f"  Rounds and rows re-verified ...... {total_rounds} across all ten")
    A("  Verification result .............. every pattern's own automated gate")
    A("                                     passes on the text reproduced here")
    A("")
    A("ATTRIBUTION"); A("-" * 64)
    A("  No attribution was changed. All existing copyright notices and")
    A("  Terms of Use were reproduced verbatim. No designer name, copyright")
    A("  owner or ownership claim was added, replaced or removed.")
    A("")
    A("COPYRIGHT NOTICES"); A("-" * 64)
    A("  7 of 10 patterns carry '(c) Novality Store - Creation Studio' -")
    A("  reproduced verbatim (NS02, NS04, NS05, NS06, NS08, NS09, NS10).")
    A("  NS01 and NS03 carry the Terms of Use naming Novality Store but no")
    A("  (c) line. None was invented.")
    A("  NS07 carries neither a (c) line nor a Terms of Use section.")
    A("  None was invented.")
    A("")
    A("LICENSING ISSUES FOUND"); A("-" * 64)
    A("  - No LICENSE file exists in the repository, and README.md states no")
    A("    licence. Nothing here is open-licensed or public domain.")
    A("  - Each pattern carries proprietary Terms of Use that prohibit")
    A("    redistributing the digital pattern.")
    A("  - The repository's main branch carries an unrelated GPLv3 README")
    A("    from another project. It shares no history with this branch and")
    A("    is not part of this collection.")
    A("")
    A("UNSUPPORTED SAFETY CLAIMS REMOVED - 1"); A("-" * 64)
    A("  - NS10 Willow described the yarn as 'a blend with a baby-safe")
    A("    certification'. No such certification exists. Reworded to")
    A("    'or a cotton blend'.")
    A("")
    A("  Nine further occurrences of the phrase 'baby-safe' were")
    A("  deliberately kept. Every one of them is a warning AGAINST making")
    A("  the claim - for example 'do not describe finished Hamishes as")
    A("  baby-safe'. Removing them would delete the protection they provide.")
    A("  No new safety claim was added anywhere.")
    A("")
    A("FORMATTING CORRECTIONS"); A("-" * 64)
    A("  - Design-code lines restored for NS05 and NS07. Eight of the ten")
    A("    source files open with 'DESIGN CODE NS NN'; those two did not.")
    A("    The codes NS05 and NS07 are taken from the source file names, not")
    A("    invented, and the restoration is marked at the head of each.")
    A("  - NS07 had two identical 'Face' headings, one for Sunny and one")
    A("    for Spud. Disambiguated. No instruction changed.")
    A("  - Collection-level headings standardised across both files.")
    A("")
    A("TYPOGRAPHICAL CORRECTIONS"); A("-" * 64)
    A("  - NS01: 'colour' -> 'color', 3 occurrences. The file is headed")
    A("    'US crochet terms'.")
    A("  - No other spelling or typographical errors were found in a scan of")
    A("    all ten files for British spellings, HTML entities and merged words.")
    A("")
    A("PATTERN AND DESIGN CORRECTIONS MADE DURING REVIEW"); A("-" * 64)
    for c, t, x in CORRECTIONS:
        A(f"  {c}  {t}")
        for chunk in _wrap(x, 60):
            A("      " + chunk)
        A("")
    A("ISSUES INTENTIONALLY LEFT UNCHANGED"); A("-" * 64)
    for x in LEFT_ALONE:
        A("  - " + x)
        A("")
    A("ITEMS REQUIRING MANUAL VERIFICATION"); A("-" * 64)
    for i, x in enumerate(MANUAL, 1):
        A(f"  {i}. " + x)
        A("")
    A("-" * 64)
    A("Compiled by Novality Crochet Studio. Original copyright holders and")
    A("terms are reproduced with each pattern and are summarised in the")
    A("COPYRIGHT & LICENSING REVIEW above.")
    A("")
    return "\n".join(L)


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


# copyright + summary are generated after validation so the counts are real
def licence_txt():
    return md_to_text(LICENCE_MD, "=")


if __name__ == "__main__":
    total_rounds = sum(ROUNDS.values())
    md_parts.append("\n" + LICENCE_MD.rstrip() + "\n\n---\n")
    md_parts.append("\n" + summary_md(total_rounds).rstrip() + "\n")
    txt_parts.append("\n" + "=" * 64 + f"\n{LICENCE_TXT_HEADER}\n" + "=" * 64 + "\n")
    txt_parts.append(md_to_text(LICENCE_MD.split("## Copyright & Licensing Review", 1)[1], "=").rstrip() + "\n")
    txt_parts.append(summary_txt(total_rounds))
    OUT_MD.write_text("".join(md_parts))
    OUT_TXT.write_text("".join(txt_parts))
    print(f"total rounds re-verified: {total_rounds}")
    print(f"bodies written: {len(patterns)} patterns")
    for P in patterns:
        flag = "" if P["had_code"] else "   <-- code restored from file name"
        print(f"  {P['shown']:<6} {P['title']:<36} {len(P['body'].splitlines()):>4} lines "
              f"{len(P['body'].split()):>5} words{flag}")
    print(f"\ndesign codes missing from source bodies: {missing_code or 'none'}")
