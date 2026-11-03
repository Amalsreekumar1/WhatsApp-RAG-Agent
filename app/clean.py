import unicodedata

CHILLU_MAP = {
    "\u0d23\u0d4d\u200d": "\u0d7a",
    "\u0d28\u0d4d\u200d": "\u0d7b",
    "\u0d30\u0d4d\u200d": "\u0d7c",
    "\u0d32\u0d4d\u200d": "\u0d7d",
    "\u0d33\u0d4d\u200d": "\u0d7e",
    "\u0d15\u0d4d\u200d": "\u0d7f",
}


def normalize(text):
    for old, new in CHILLU_MAP.items():
        text = text.replace(old, new)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


def match_key(text):
    return "".join(normalize(text).lower().split())
