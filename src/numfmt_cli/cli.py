"""Command-line entry point for numfmt-cli."""
from __future__ import annotations

import argparse
import sys
from typing import TextIO

from .core import format_number, parse_number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="numfmt-cli",
        description="Format large numbers with human-readable suffixes (1234567 -> 1.2M) "
        "and parse them back, auto-detecting direction from the input.",
    )
    parser.add_argument(
        "value",
        help="A bare number (e.g. 1234567) or a suffixed number (e.g. 1.2M, 3B, 500K)",
    )
    parser.add_argument(
        "--precision", type=int, default=1,
        help="Decimal places to show when formatting a number to human-readable form (default: 1)",
    )
    return parser


def _is_bare_number(text: str) -> bool:
    try:
        float(text.strip())
        return True
    except ValueError:
        return False


def main(argv: "list[str] | None" = None, out: "TextIO | None" = None, err: "TextIO | None" = None) -> int:
    out = out if out is not None else sys.stdout
    err = err if err is not None else sys.stderr

    parser = build_parser()
    args = parser.parse_args(argv)
    value = args.value

    if _is_bare_number(value):
        n = float(value)
        print(format_number(n, args.precision), file=out)
        return 0

    try:
        n = parse_number(value)
    except ValueError as exc:
        print(f"numfmt-cli: error: {exc}", file=err)
        return 2

    print(n, file=out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
