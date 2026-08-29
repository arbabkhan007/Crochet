"""NS06 Momo the Loaf Cat — round tables, transcribed verbatim from the pattern."""

# 1. Body, worked on an oval base (foundation ch 9)
BODY = [
    ("Rnd 1",  "sc in 2nd ch from hook, sc in next 6, 3 sc in last ch, "
               "sc in next 6, 2 sc in last loop", 18, "worked around both sides"),
    ("Rnd 2",  "inc, 6 sc, inc x3, 6 sc, inc x2",  24, ""),
    ("Rnd 3",  "sc, inc, 6 sc, [sc, inc] x3, 6 sc, [sc, inc] x2", 30, ""),
    ("Rnd 4",  "2 sc, inc, 6 sc, [2 sc, inc] x3, 6 sc, [2 sc, inc] x2", 36,
               "base at full size"),
    ("Rnd 5",  "BLO sc around",         36, "ridge = the base edge"),
    ("Rnd 6",  "sc in each st around",  36, ""),
    ("Rnd 7",  "sc in each st around",  36, "eyes at Rnd 7-8"),
    ("Rnd 8",  "sc in each st around",  36, ""),
    ("Rnd 9",  "sc in each st around",  36, "stuff firmly from here"),
    ("Rnd 10", "[4 sc, dec] x6",        30, ""),
    ("Rnd 11", "[3 sc, dec] x6",        24, "ears worked onto Rnd 11"),
    ("Rnd 12", "[2 sc, dec] x6",        18, ""),
    ("Rnd 13", "[sc, dec] x6",          12, "top up the stuffing"),
    ("Rnd 14", "dec x6",                 6, ""),
]
FOUNDATION = 9   # ch 9

# 2. Ears — flat rows worked directly onto the head
EAR = [
    ("Row 1", "sc in next 5",   5, "ch 1, turn"),
    ("Row 2", "dec, sc, dec",   3, "ch 1, turn"),
    ("Row 3", "dec, sc",        2, "ear tip"),
]

# 3. Tail — worked off the body fabric
TAIL = [
    ("Rnd 1", "4 sc in MR",           4, "worked into the body fabric"),
    ("Rnd 2", "sc in each st around", 4, ""),
    ("Rnd 3", "sc in each st around", 4, ""),
    ("Rnd 4", "sc in each st around", 4, ""),
    ("Rnd 5", "sc in each st around", 4, ""),
    ("Rnd 6", "sc in each st around", 4, ""),
    ("Rnd 7", "sc in each st around", 4, ""),
    ("Rnd 8", "sc in each st around", 4, ""),
]

ALL = {"body": (BODY, 1), "ear": (EAR, 2), "tail": (TAIL, 1)}

MM_ST  = 4.5
MM_RND = 4.3

# claimed dimensions
CLAIM = dict(length=75.0, width=55.0, height=45.0,
             base_length=75.0, base_width=55.0, wall_height=43.0,
             polyfill=20.0, yarn=30.0)
