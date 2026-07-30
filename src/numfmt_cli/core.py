"""Core parsing and formatting logic for numfmt-cli."""
from __future__ import annotations

import re

SUFFIX_FACTORS: dict[str, float] = {
    "K": 1_000,
    "M": 1_000_000,
    "B": 1_000_000_000,
    "T": 1_000_000_000_000,
}

# Largest suffix first, so formatting picks the biggest one that fits.
_ORDERED_SUFFIXES = sorted(SUFFIX_FACTORS.items(), key=lambda pair: pair[1], reverse=True)

_PARSE_RE = re.compile(r"([+-]?\d+(?:\.\d+)?)\s*([KMBTkmbt]?)")


def format_number(value: float, precision: int = 1) -> str:
    """Format a number with a human-readable suffix (1234567 -> "1.2M").

    Values under 1000 are printed as plain integers with no suffix.
    `precision` controls the number of decimal places shown for suffixed
    values (default 1).
    """
    negative = value < 0
    magnitude = abs(value)

    for suffix, factor in _ORDERED_SUFFIXES:
        if magnitude >= factor:
            scaled = magnitude / factor
            sign = "-" if negative else ""
            return f"{sign}{scaled:.{precision}f}{suffix}"

    sign = "-" if negative else ""
    return f"{sign}{int(round(magnitude))}"


def parse_number(text: str) -> int:
    """Parse a human-readable number ("1.2M") back into an integer ("1200000").

    Supported suffixes (case-insensitive) are K, M, B, and T. Raises
    ValueError if the string isn't a recognizable number.
    """
    if text is None:
        raise ValueError("value must not be None")
    stripped = text.strip()
    match = _PARSE_RE.fullmatch(stripped)
    if not match or not match.group(1):
        raise ValueError(f"not a valid number: {text!r}")

    amount = float(match.group(1))
    suffix = match.group(2).upper()
    factor = SUFFIX_FACTORS.get(suffix, 1)
    return int(round(amount * factor))
