"""NS07 Pocket Positivity Trio — round tables, transcribed verbatim."""

SUNNY_CENTRE = [
    ("Rnd 1", "6 sc in MR",            6,  ""),
    ("Rnd 2", "inc in each st around", 12, ""),
    ("Rnd 3", "[sc, inc] x6",          18, ""),
    ("Rnd 4", "sc in each st around",  18, ""),
    ("Rnd 5", "[sc, dec] x6",          12, "stuff lightly"),
    ("Rnd 6", "dec x6",                 6, ""),
]
SUNNY_PETALS = [
    ("Rnd 1", "[sl st in next st, (sc, hdc, sc) in next st] x9", 36,
     "each repeat takes 2 sts - closes all 18"),
]

WADDLE_BODY = [
    ("Rnd 1",  "6 sc in MR",            6,  ""),
    ("Rnd 2",  "inc in each st around", 12, ""),
    ("Rnd 3",  "[sc, inc] x6",          18, ""),
    ("Rnd 4",  "sc in each st around",  18, "eyes at Rnd 4-5"),
    ("Rnd 5",  "sc in each st around",  18, ""),
    ("Rnd 6",  "sc in each st around",  18, ""),
    ("Rnd 7",  "[2 sc, inc] x6",        24, "body widens"),
    ("Rnd 8",  "sc in each st around",  24, ""),
    ("Rnd 9",  "sc in each st around",  24, ""),
    ("Rnd 10", "[2 sc, dec] x6",        18, "stuff firmly"),
    ("Rnd 11", "[sc, dec] x6",          12, ""),
    ("Rnd 12", "dec x6",                 6, ""),
]
WADDLE_WING = [
    ("Rnd 1", "4 sc in MR",            4, ""),
    ("Rnd 2", "[sc, inc] x2",          6, ""),
    ("Rnd 3", "sc in each st around",  6, ""),
    ("Rnd 4", "sc in each st around",  6, ""),
]

SPUD = [
    ("Rnd 1",  "sc in 2nd ch from hook, sc in next 4, 3 sc in last ch, "
               "sc in next 4, 2 sc in last loop", 14, "worked around both sides"),
    ("Rnd 2",  "inc, 4 sc, inc x3, 4 sc, inc x2", 20, ""),
    ("Rnd 3",  "sc in each st around",  20, ""),
    ("Rnd 4",  "sc in each st around",  20, "eyes at Rnd 4-5"),
    ("Rnd 5",  "sc in each st around",  20, ""),
    ("Rnd 6",  "sc in each st around",  20, "stuff firmly"),
    ("Rnd 7",  "[3 sc, dec] x4",        16, ""),
    ("Rnd 8",  "[2 sc, dec] x4",        12, ""),
    ("Rnd 9",  "[sc, dec] x4",           8, ""),
    ("Rnd 10", "dec x4",                 4, ""),
]
SPUD_FOUNDATION = 7   # ch 7

# chest patch is an oval around ch 6 -> 12 st; beak is a flat triangle
WADDLE_CHEST = [
    ("Rnd 1", "1 sc, 3 sc, 3 sc in one st, 3 sc, 2 sc in one st", 12, "around ch 6"),
    ("Rnd 2", "inc, 3 sc, inc x3, 3 sc, inc x2", 18, ""),
]
WADDLE_BEAK = [
    ("Rnd 1", "3 sc in one st", 3, "in 2nd ch from hook"),
    ("Rnd 2", "inc x3", 6, ""),
    ("Rnd 3", "sc in each st around", 6, ""),
]

ALL = {
    "sunny centre":  (SUNNY_CENTRE, 1),
    "sunny petals":  (SUNNY_PETALS, 1),
    "waddle body":   (WADDLE_BODY, 1),
    "waddle wing":   (WADDLE_WING, 2),
    "spud":          (SPUD, 1),
    "waddle chest":  (WADDLE_CHEST, 1),
    "waddle beak":   (WADDLE_BEAK, 1),
}

MM_ST  = 3.5
MM_RND = 3.2

CLAIM = dict(sunny=45.0, waddle=50.0, spud=55.0, trio_tall=50.0,
             centre=20.0, polyfill=10.0,
             yarn={"yellow": 6, "brown": 3, "black": 6, "white": 4,
                   "orange": 2, "light brown": 7})
