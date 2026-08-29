"""NS09 Shelby the Sea Turtle Bag Charm — round tables, transcribed verbatim."""

SHELL = [
    ("Rnd 1", "6 sc in MR",            6,  ""),
    ("Rnd 2", "inc in each st around", 12, ""),
    ("Rnd 3", "[sc, inc] x6",          18, ""),
    ("Rnd 4", "[2 sc, inc] x6",        24, ""),
    ("Rnd 5", "BLO sc around",         24, "rim ridge"),
    ("Rnd 6", "sc in each st around",  24, ""),
]

UNDERSIDE = [
    ("Rnd 1", "6 sc in MR",            6,  ""),
    ("Rnd 2", "inc in each st around", 12, ""),
    ("Rnd 3", "[sc, inc] x6",          18, ""),
    ("Rnd 4", "[2 sc, inc] x6",        24, "flat disc, matches the shell"),
]

# Rnd 5 is worked into Rnd 4 of the underside: five clusters, each into ONE stitch
BUMPS = ("3 sc, (sc, hdc, hdc, sc) in next st, 4 sc, (sc, hdc, sc) in next st, "
         "3 sc, (sc, hdc, sc) in next st, 4 sc, (sc, hdc, sc) in next st, "
         "3 sc, (sc, hdc, sc) in next st, 2 sc")
BUMPS_ROW = [("Rnd 5", BUMPS, 35, "head + 4 flippers")]

# the pattern's own claim about that round
BUMPS_CLAIM = dict(consumed=24, produced=35,
                   plain_runs=[3, 4, 3, 4, 3, 2],
                   note="3 + 1 + 4 + 1 + 3 + 1 + 4 + 1 + 3 + 1 + 2 = 24")

ALL = {"shell": (SHELL, 1), "underside": (UNDERSIDE + BUMPS_ROW, 1)}

MM_ST  = 3.5
MM_RND = 3.2

CLAIM = dict(across_flippers=60.0, length=45.0, depth=20.0,
             polyfill=3.0, shell_yarn=5.0, body_yarn=4.0)
