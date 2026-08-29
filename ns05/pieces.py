"""NS05 Little Duck Plushie — every instruction row exactly as published,
plus the finished-size and materials claims the pattern makes."""

# gauge as the pattern states it: super-bulky chenille (#6) on a 4.5 mm hook
MM_ST = 8.0
MM_RND = 7.0

BODY = [
    ("R1",  "6 sc in MR", 6, ""),
    ("R2",  "inc in each st around", 12, ""),
    ("R3",  "[sc, inc] x6", 18, ""),
    ("R4",  "[2 sc, inc] x6", 24, ""),
    ("R5",  "[3 sc, inc] x6", 30, "body at full width"),
    ("R6",  "sc in each st around", 30, "wings attach at R6-R9"),
    ("R7",  "sc in each st around", 30, ""),
    ("R8",  "sc in each st around", 30, ""),
    ("R9",  "sc in each st around", 30, ""),
    ("R10", "[3 sc, dec] x6", 24, ""),
    ("R11", "sc in each st around", 24, ""),
    ("R12", "[2 sc, dec] x6", 18, "begin stuffing the body firmly"),
    ("R13", "[2 sc, inc] x6", 24, ""),
    ("R14", "[3 sc, inc] x6", 30, "head begins"),
    ("R15", "sc in each st around", 30, ""),
    ("R16", "sc in each st around", 30, "eyes between R16 & R17"),
    ("R17", "sc in each st around", 30, ""),
    ("R18", "sc in each st around", 30, "beak across R16-R18"),
    ("R19", "sc in each st around", 30, ""),
    ("R20", "[3 sc, dec] x6", 24, ""),
    ("R21", "[2 sc, dec] x6", 18, "stuff the head, shaping the cheeks evenly"),
    ("R22", "[sc, dec] x6", 12, "add the final small pieces of stuffing"),
    ("R23", "dec x6", 6, ""),
]

WING = [
    ("R1", "6 sc in MR", 6, ""),
    ("R2", "inc in each st around", 12, ""),
    ("R3", "sc in each st around", 12, ""),
    ("R4", "sc in each st around", 12, ""),
]
WING_CLOSE = 6          # "sc 6 sts across both layers to close the edge"

# Beak is worked around both sides of a starting chain of 5.
#   side one:  sc in chs 4,3,2 then 3 sc in ch 1   -> 6 sts, 4 chains touched
#   side two:  sc in chs 2,3,4 then 2 sc in ch 5   -> 5 sts, 4 chains touched
BEAK_CHAIN = 5
BEAK = [
    ("Rnd 1", "3 sc, 3 sc in one st, 3 sc, 2 sc in one st", 11, "around ch 5"),
    ("Rnd 2", "inc, 2 sc, inc, 2 sc, inc, 2 sc, inc, sc", 15, ""),
]

ALL = {
    "body & head": (BODY, 1),
    "wing":        (WING, 2),
    "beak":        (BEAK, 1),
}

CLAIM = dict(
    tall=160.0,          # "About 16 cm / 6.25 in tall"
    wide=75.0,           # "7.5 cm / 3 in wide"
    tall_in=6.25,
    wide_in=3.0,
    dk_tall_lo=100.0,    # "For a smaller 10-12 cm duck, work ... in DK ... on 3.0 mm"
    dk_tall_hi=120.0,
    yarn_body_lo=55.0,   # "yellow, ~55-75 g"
    yarn_body_hi=75.0,
    swatch_st=12,
    chunky_tall=200.0,   # "at 10 mm per stitch this pattern finishes near 20 cm"
    eye_gap_lo=7, eye_gap_hi=8,
)
