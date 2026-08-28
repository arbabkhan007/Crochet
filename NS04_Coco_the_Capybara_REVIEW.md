# Pattern review — NS04 "Coco the Capybara" (Novality Store)

Verified computationally. Scripts: `check/verify_coco.py` (stitch arithmetic),
`check/verify_geometry.py` (gauge / leg placement / height / face),
`check/verify_materials.py` (stuffing, leg join, ear placement).

## Verdict

**The stitch arithmetic is flawless.** 36 rounds across 4 pieces, every bracketed
count reproduced exactly, 0 mismatches. The gauge is internally consistent to
three independent checks. This is a competently built pattern.

**Three substantive problems**, all in the numbers the pattern asserts about
itself rather than in the instructions: leg placement does not match its own
"90 degrees" claim, the stated height contradicts the standing-on-legs design,
and the leg-join instructions contradict each other.

---

## 1. Stitch arithmetic — PASS (36/36)

```
LEG (make 4)      8 rounds  0 mismatch
EAR (make 2)      3 rounds  0 mismatch
MUZZLE (make 1)   5 rounds  0 mismatch
BODY & HEAD      20 rounds  0 mismatch
                 36 rounds  0 stitch-count mismatches
```

Every increase/decrease group consumes exactly the stitches available and
produces exactly the stated count. Body R4's asymmetric layout
(`3 sc, [1 sc, inc] x3, 3 sc, [1 sc, inc] x3`) also totals 24 correctly.

## 2. Gauge — PASS (3/3 checks)

| Claim | Computed | |
|---|---|---|
| 36 sc round = 52 mm diameter | 36 x 4.5 = 162 mm; 162 / pi = **51.6 mm** | OK |
| 8 rnd leg = 34 mm | 8 x 4.3 = **34.4 mm** | OK |
| Join at R4-R5 = "17-21 mm above base" | 4 x 4.3 = **17.2**, 5 x 4.3 = **21.5** | OK |

Framing gauge as "36 sc around measures 52 mm when stuffed" is unusual but
better than a flat swatch for amigurumi — it is directly testable mid-project.

---

# ISSUES, most serious first

## A. Leg placement is not "roughly 90 deg" — it is a bowtie  (correctness)

The pattern states: *"This places the four legs at roughly 90° to each other."*

Computed from the instructions as written:

- **R4 back legs** (24-st round): centres 10.5 sts one way, 13.5 the other
  = **157.5° and 202.5°**, not 90°.
- **R5 front legs** (30-st round): `2 sc, leg/3, 12 sc, leg/3, to end`
  = **exactly 180° apart**, diametrically opposite.
- **Front vs back**: a front leg sits only 3 sts (~13.5 mm) behind a back leg
  on one side and ~12 sts (~54 mm) on the other.

Footprint spans: left-right 67.5 mm, front-back 20.2 mm — a **3.3 : 1 ratio**.
Coco will stand, but on a narrow bowtie, and will be tippy front-to-back.
That matters more here than usual, because section 3 makes standing the whole
point of the design.

**Suggested fix** — keep R4 as printed, change R5 to:

> **R5** — front legs: work 2 sc, join a leg over the next 3 sc, work **6 sc**,
> join a leg over the next 3 sc, work **13 sc** to the end of the round (30).

`2 + 3 + 6 + 3 + 13 = 30`, so the count is unchanged. This puts the front legs
roughly midway between the back legs left-to-right and gives a front-back span
of ~9 sts (~40 mm) instead of ~4.5 — a near-square footprint.

## B. Stated height (8.5 cm) contradicts the standing-on-legs design  (correctness)

The pattern's own numbers:

```
leg length                = 8 x 4.3 = 34.4 mm
highest join point (R5)   = 5 x 4.3 = 21.5 mm above body base
=> body base floats         34.4 - 21.5 = 12.9 mm above the table
body base -> top of head  = 20 x 4.3 = 86.0 mm
TOTAL standing height     = 98.9 mm
stated finished size      = 85 mm       -> overstated by 13.9 mm (16%)
```

The 8.5 cm figure is correct **only if the legs are decorative and the belly
rests on the table**. But the pattern says the opposite, twice: the 34 mm leg
*"puts the foot flat on the table with room to spare"*, and the closing photo
caption is *"Coco standing square on all four legs."* Both cannot hold.

Pick one and make the pattern agree:
- **Standing Coco** → finished size becomes **~10 cm** tall; or
- **8.5 cm Coco** → legs join at R1-R2 and shorten to ~5 rounds, which then
  invalidates the whole of section 3 ("Why the legs join so low").

## C. Leg-join instructions contradict each other  (clarity)

- Legs: *"flatten only the top 3 sts"*
- Assembly: *"make sure the flattened top of each leg is caught fully in the round"*

A 9-stitch tube flattens to an edge ~5 stitches across. The body round joins 3
stitches, so **2 edge stitches of every leg go unjoined** — a small hole at each
of four joins. The two sentences only reconcile if the maker pinches the entire
9-stitch top down to a 3-stitch strip. Say that explicitly:

> Pinch the whole 9-stitch top flat into a narrow strip about 3 stitches wide,
> then join those 3 stitches to the body. The remaining leg stitches bunch
> inside the join — this is what makes the leg look plump.

## D. Muzzle and eye rows overlap, but the text says "below"  (clarity)

Muzzle is pinned *"over R12-R14"*; eyes are embroidered *"at R13-R14"*. Two of
the muzzle's three rows sit under the eyes, yet the text says the muzzle sits
*"slightly below the eye line."* Give the muzzle its own rows (e.g. R11-R13)
or move the eyes to R14-R15.

Spacing itself is workable, but tight: eyes 6 sts apart = 27.0 mm on a 51.6 mm
head (60° of arc), muzzle diameter 17.2 mm → **4.9 mm clearance** from muzzle
edge to nearest eye. The pattern's own justification ("wider and they wrap
around the sides") is sound.

## E. Ears are placed too far around the sides  (aesthetic)

Sewn *"at R15-R16, about 7 stitches apart."* R16 is a 30-stitch round
(43.0 mm diameter), so 7 sts = 31.5 mm = **84° around the head** — essentially
the side of the head. Capybara ears sit on top. **4-5 stitches apart** keeps
them visible from the front, which is what the "angled slightly outward" note
implies.

## F. Hook size conflict  (minor, correctness)

Materials: **3.5 mm**. Troubleshooting: *"Go down to a 3.0 mm hook. Loose gauge
on 3.5 mm is the usual cause."* The troubleshooting entry concedes the
recommended hook is too loose. Settle on 3.0 mm, or reword to *"if your tension
is loose, drop to 3.0 mm."*

## G. "Fully baby-safe" is an unqualified claim  (liability)

Stated twice. Embroidered eyes are genuinely safer than safety eyes, but a
polyfill-stuffed toy with a sewn-on muzzle and sewn-on ears is not
automatically baby-safe — that depends on meeting a toy-safety standard
(ASTM F963 / EN 71), not on omitting plastic eyes. Recommend: *"No safety eyes
— the face is embroidered"* and drop the baby-safe claim, or add
*"not tested to toy-safety standards; decorative use."*

## H. Polyfill quantity is ~3x the volume  (minor)

Stuffed volume computes to **~125 cm3**. Firmly packed polyester fibre runs
roughly 30-60 kg/m3, so Coco holds **~4-8 g**. Pattern states **15 g**. Harmless
(you buy a bag, not a gram count) but it signals the figure was never measured.

## I. R5 leaves its final stitch count implicit  (clarity)

`2 sc, join leg over 3 sc, 12 sc, join leg over 3 sc, work to the end (30)` —
`2+3+12+3 = 20`, so **10 stitches are never named**. Every other round states
its count. Print `...then 10 sc to the end of the round (30)`.

## J. Missing from Abbreviations / techniques  (minor)

- **BLO, FLO** are not used anywhere, so nothing is missing there — but
  **Rnd** is used in section 3 ("Rnd 4 and Rnd 5") without being defined.
- The two-layer leg join is the single hardest thing in this pattern and is
  **absent from the "core techniques" list**, which covers only magic ring and
  spiral. It deserves an entry with a photo.
- Skill level says **Advanced beginner**; joining a flattened tube through two
  layers mid-round is usually graded **intermediate**.

## K. Editorial  (cosmetic)

Run-together words throughout: `expression,and`, `muzzleand`, `oncethe`,
`thereis`, `itagainst`, `sewanything`, `madefrom`, `isstrictly`. Also
`Face yarn  Worsted #4 or DK` — DK is a different weight and will change the
embroidery's appearance; pick one.

---

## What is genuinely good

- Zero arithmetic errors across 36 rounds — most published amigurumi patterns
  have at least one.
- Gauge stated three ways that all agree, and stated in a form a maker can
  actually test mid-project.
- Section 3 ("Why the legs join so low") explains the *reasoning*, which is
  rare and genuinely useful — the diagnosis is right even though the height
  figure beside it is not.
- Troubleshooting section is specific and causal, not filler.
- Spiral-round instruction with a stitch-marker reminder is correct and
  consistently applied.
