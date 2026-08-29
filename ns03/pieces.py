"""NS03 Axel the Axolotl — every round table, transcribed verbatim."""

# 1. Head, neck, body & tail — one continuous spiral
BODY = [
    ("R1",  "6 sc in MR",                 6,  "start at top of head"),
    ("R2",  "inc in each st around",      12, ""),
    ("R3",  "[1 sc, inc] x6",             18, ""),
    ("R4",  "[2 sc, inc] x6",             24, ""),
    ("R5",  "[3 sc, inc] x6",             30, ""),
    ("R6",  "[4 sc, inc] x6",             36, "head at full width"),
    ("R7",  "sc in each st around",       36, "eyes between R7/R8"),
    ("R8",  "sc in each st around",       36, ""),
    ("R9",  "sc in each st around",       36, "smile on R8-R9"),
    ("R10", "[4 sc, invdec] x6",          30, ""),
    ("R11", "[3 sc, invdec] x6",          24, "STUFF HEAD FIRMLY"),
    ("R12", "[2 sc, invdec] x6",          18, ""),
    ("R13", "sc in each st around",       18, "NECK - narrowest point"),
    ("R14", "[2 sc, inc] x6",             24, "body flares out"),
    ("R15", "[3 sc, inc] x6",             30, ""),
    ("R16", "[4 sc, inc] x6",             36, "body at full width"),
    ("R17", "sc in each st around",       36, "arms attach at R17-R18"),
    ("R18", "sc in each st around",       36, ""),
    ("R19", "sc in each st around",       36, ""),
    ("R20", "sc in each st around",       36, ""),
    ("R21", "sc in each st around",       36, ""),
    ("R22", "sc in each st around",       36, ""),
    ("R23", "[4 sc, invdec] x6",          30, ""),
    ("R24", "[3 sc, invdec] x6",          24, "FEET at R24-R25"),
    ("R25", "[2 sc, invdec] x6",          18, "stuff body LIGHTLY"),
    ("R26", "[1 sc, invdec] x6",          12, ""),
    ("R27", "sc in each st around",       12, "tail begins"),
    ("R28", "[2 sc, invdec] x3",           9, ""),
    ("R29", "sc in each st around",        9, ""),
    ("R30", "sc in each st around",        9, ""),
    ("R31", "sc in each st around",        9, ""),
    ("R32", "[1 sc, invdec] x3",           6, "light stuffing to here"),
    ("R33", "sc in each st around",        6, ""),
    ("R34", "sc in each st around",        6, ""),
    ("R35", "sc in each st around",        6, ""),
    ("R36", "sc in each st around",        6, "taper to tip"),
]

ARM = [
    ("R1", "6 sc in MR",            6, ""),
    ("R2", "sc in each st around",  6, ""),
    ("R3", "sc in each st around",  6, ""),
    ("R4", "sc in each st around",  6, ""),
    ("R5", "sc in each st around",  6, ""),
    ("R6", "sc in each st around",  6, ""),
]

FOOT = [
    ("R1", "6 sc in MR",            6, ""),
    ("R2", "[1 sc, inc] x3",        9, ""),
    ("R3", "sc in each st around",  9, ""),
    ("R4", "sc in each st around",  9, ""),
    ("R5", "[1 sc, invdec] x3",     6, ""),
]

GILL = [
    ("R1", "6 sc in MR",            6, ""),
    ("R2", "inc in each st around", 12, ""),
    ("R3", "sc in each st around",  12, ""),
    ("R4", "sc in each st around",  12, ""),
    ("R5", "[1 sc, invdec] x4",      8, ""),
]

ALL = {"body": (BODY, 1), "arm": (ARM, 2), "foot": (FOOT, 2), "gill": (GILL, 6)}

MM_ST = 4.5    # stated: 4.5 mm per stitch
MM_RND = 4.3   # stated: 4.3 mm per round
