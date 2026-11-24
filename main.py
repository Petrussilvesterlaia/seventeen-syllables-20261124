"""Seventeen Syllables of Debugging.

Writes one original haiku about debugging to /output/entry.txt and
validates the result itself: exactly three non-empty lines, 1-200
characters in total, 5-7-5 syllables per line, no control characters,
and a read-back check that the file holds exactly what was written.
Deterministic: every run produces byte-identical output.
"""

import os
import re

OUTPUT_PATH = "/output/entry.txt"

HAIKU = (
    "The stack trace points down\n"
    "a hundred frames of my code\n"
    "they point back at me"
)

# Words whose syllable count a plain vowel-group scan gets wrong.
_EXCEPTIONS = {
    "hundred": 2,
}

_VOWELS = "aeiouy"


def count_syllables(word):
    """Count the syllables of one English word (standard counting)."""
    w = word.lower().strip(".,;:!?\"'()")
    if not w:
        return 0
    if w in _EXCEPTIONS:
        return _EXCEPTIONS[w]
    # Count groups of adjacent vowels, then drop silent endings: a
    # trailing "e" (trace, code) and a silent "-es" plural (frames).
    groups = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("es") and groups > 1:
        stem = w[:-2]
        if stem and stem[-1] not in "sxzcg" and not stem.endswith(("ch", "sh")):
            groups -= 1
    elif w.endswith("e") and groups > 1:
        groups -= 1
    # A trailing "-ed" after a consonant other than t/d is silent.
    if w.endswith("ed") and len(w) > 2 and w[-3] not in "td" + _VOWELS:
        groups -= 1
    return max(groups, 1)


def line_syllables(line):
    return sum(count_syllables(word) for word in line.split())


def main():
    lines = HAIKU.split("\n")

    # The haiku must be exactly three non-empty lines.
    assert len(lines) == 3, f"expected 3 lines, got {len(lines)}"
    assert all(line.strip() for line in lines), "empty line in haiku"

    # Total length: 1 to 200 characters (gate limit).
    assert 1 <= len(HAIKU) <= 200, f"total length {len(HAIKU)} out of range"

    # The 5-7-5 shape, checked line by line.
    expected = (5, 7, 5)
    counts = [line_syllables(line) for line in lines]
    for i, (got, want) in enumerate(zip(counts, expected), start=1):
        assert got == want, f"line {i}: {got} syllables, expected {want}"

    # No control characters (tabs, carriage returns and the like).
    assert not any(ord(ch) < 32 and ch != "\n" for ch in HAIKU), \
        "control character in haiku"

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)

    # Read the file back and confirm it holds exactly what was written.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        assert f.read() == HAIKU, "read-back differs from written text"

    print(HAIKU)
    print(f"total characters: {len(HAIKU)}")
    print(f"syllables per line: {counts[0]}-{counts[1]}-{counts[2]}")


if __name__ == "__main__":
    main()
