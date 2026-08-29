"""NS01 Hamish the Highland Cow — every round table, transcribed verbatim."""

HEAD = [
    ("Rnd 1",  "6 sc in MR",            6,  ""),
    ("Rnd 2",  "inc in each st around", 12, ""),
    ("Rnd 3",  "[sc, inc] x6",          18, ""),
    ("Rnd 4",  "[2 sc, inc] x6",        24, ""),
    ("Rnd 5",  "[3 sc, inc] x6",        30, ""),
    ("Rnd 6",  "[4 sc, inc] x6",        36, "fringe row 3"),
    ("Rnd 7",  "[5 sc, inc] x6",        42, "fringe row 2 / horns"),
    ("Rnd 8",  "[6 sc, inc] x6",        48, "fringe row 1 / ears"),
    ("Rnd 9",  "sc in each st around",  48, "eyes at Rnd 9-10"),
    ("Rnd 10", "[6 sc, dec] x6",        42, ""),
    ("Rnd 11", "[5 sc, dec] x6",        36, ""),
    ("Rnd 12", "[4 sc, dec] x6",        30, "stuff firmly, flatten front to back"),
    ("Rnd 13", "[3 sc, dec] x6",        24, ""),
    ("Rnd 14", "[2 sc, dec] x6",        18, ""),
    ("Rnd 15", "[sc, dec] x6",          12, "last pinch of stuffing"),
    ("Rnd 16", "dec x6",                 6, ""),
]

MUZZLE = [
    ("Rnd 1",  "6 sc in MR",            6,  ""),
    ("Rnd 2",  "inc in each st around", 12, ""),
    ("Rnd 3",  "[sc, inc] x6",          18, ""),
    ("Rnd 4",  "[2 sc, inc] x6",        24, ""),
    ("Rnd 5",  "[3 sc, inc] x6",        30, ""),
    ("Rnd 6",  "sc in each st around",  30, ""),
    ("Rnd 7",  "sc in each st around",  30, ""),
    ("Rnd 8",  "sc in each st around",  30, ""),
    ("Rnd 9",  "[3 sc, dec] x6",        24, "rim = 35 mm across"),
]

BODY = [
    ("Rnd 1",  "6 sc in MR",            6,  ""),
    ("Rnd 2",  "inc in each st around", 12, ""),
    ("Rnd 3",  "[sc, inc] x6",          18, ""),
    ("Rnd 4",  "[2 sc, inc] x6",        24, ""),
    ("Rnd 5",  "[3 sc, inc] x6",        30, ""),
    ("Rnd 6",  "[4 sc, inc] x6",        36, ""),
    ("Rnd 7",  "[5 sc, inc] x6",        42, ""),
    ("Rnd 8",  "[6 sc, inc] x6",        48, "front legs join at Rnd 8-9"),
    ("Rnd 9",  "sc in each st around",  48, ""),
    ("Rnd 10", "sc in each st around",  48, "body at full width, 70 mm"),
    ("Rnd 11", "sc in each st around",  48, ""),
    ("Rnd 12", "sc in each st around",  48, ""),
    ("Rnd 13", "sc in each st around",  48, ""),
    ("Rnd 14", "[6 sc, dec] x6",        42, ""),
    ("Rnd 15", "sc in each st around",  42, ""),
    ("Rnd 16", "[5 sc, dec] x6",        36, ""),
    ("Rnd 17", "[4 sc, dec] x6",        30, "stuff firmly, pack the base"),
    ("Rnd 18", "[3 sc, dec] x6",        24, ""),
    ("Rnd 19", "[2 sc, dec] x6",        18, "leave neck OPEN"),
]

# oval belly patch: foundation ch 9, worked around both sides of the chain
BELLY = [
    ("Rnd 1",  "sc in 2nd ch from hook, sc in next 6, 3 sc in last ch, "
               "sc in next 6, 2 sc in last loop", 18, "worked around both sides"),
    ("Rnd 2",  "inc, 6 sc, inc x3, 6 sc, inc x2",  24, ""),
    ("Rnd 3",  "sc, inc, 6 sc, [sc, inc] x3, 6 sc, [sc, inc] x2", 30, ""),
    ("Rnd 4",  "2 sc, inc, 6 sc, [2 sc, inc] x3, 6 sc, [2 sc, inc] x2", 36, ""),
]
BELLY_FOUNDATION = 9   # ch 9

LEG = [
    ("Rnd 1",  "6 sc in MR",            6,  "Yarn C"),
    ("Rnd 2",  "inc in each st around", 12, ""),
    ("Rnd 3",  "[sc, inc] x6",          18, ""),
    ("Rnd 4",  "sc in each st around",  18, ""),
    ("Rnd 5",  "sc in each st around",  18, ""),
    ("Rnd 6",  "BLO sc around",         18, "change to Yarn A - ridge = colour line"),
    ("Rnd 7",  "sc in each st around",  18, ""),
    ("Rnd 8",  "[sc, dec] x6",          12, "stuff hoof firmly"),
    ("Rnd 9",  "sc in each st around",  12, ""),
    ("Rnd 10", "sc in each st around",  12, ""),
    ("Rnd 11", "sc in each st around",  12, ""),
    ("Rnd 12", "sc in each st around",  12, ""),
    ("Rnd 13", "sc in each st around",  12, "upper leg light"),
    ("Rnd 14", "[2 sc, dec] x3",         9, ""),
    ("Rnd 15", "sc in each st around",   9, ""),
    ("Rnd 16", "sc in each st around",   9, ""),
]
LEG_YARN_A_FROM = 6     # Rnd 6 onward is Yarn A

EAR_INNER = [
    ("Rnd 1", "6 sc in MR",            6,  ""),
    ("Rnd 2", "[sc, inc] x3",          9,  ""),
    ("Rnd 3", "[2 sc, inc] x3",        12, ""),
]
EAR_OUTER = [
    ("Rnd 1", "6 sc in MR",            6,  ""),
    ("Rnd 2", "[sc, inc] x3",          9,  ""),
    ("Rnd 3", "[2 sc, inc] x3",        12, ""),
    ("Rnd 4", "sc in each st around",  12, "worked through both layers"),
    ("Rnd 5", "sc in each st around",  12, ""),
    ("Rnd 6", "[2 sc, dec] x3",         9, ""),
    ("Rnd 7", "sc in each st around",   9, ""),
]

HORN = [
    ("Rnd 1", "4 sc in MR",            4, ""),
    ("Rnd 2", "[sc, inc] x2",          6, ""),
    ("Rnd 3", "sc in each st around",  6, ""),
    ("Rnd 4", "sc in each st around",  6, ""),
    ("Rnd 5", "[2 sc, inc] x2",        8, ""),
    ("Rnd 6", "sc in each st around",  8, ""),
    ("Rnd 7", "sc in each st around",  8, ""),
]

ALL = {
    "head":      (HEAD, 1),
    "muzzle":    (MUZZLE, 1),
    "body":      (BODY, 1),
    "belly":     (BELLY, 1),
    "leg":       (LEG, 4),
    "ear inner": (EAR_INNER, 2),
    "ear outer": (EAR_OUTER, 2),
    "horn":      (HORN, 2),
}

MM_ST  = 4.55    # stated: 4.55 mm per stitch  (11 sc = 5 cm)
MM_RND = 4.17    # stated: 4.17 mm per round   (12 rnd = 5 cm)

SCARF = dict(ch=61, hdc_row1=60, hdc_row2=60)
FRINGE = dict(strands=44, cut_cm=14, rows={"Rnd 8": 48, "Rnd 7": 42, "Rnd 6": 36})
TAIL = dict(strands=6, cut_cm=22, groups=3, per_group=4)
