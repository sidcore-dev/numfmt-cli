# numfmt-cli

A small, dependency-free tool that formats large numbers with
human-readable suffixes (`1234567` -> `1.2M`) and parses them back
(`1.2M` -> `1200000`) — in either direction, auto-detected from the input.

## Why

Reading `1234567890` at a glance is harder than reading `1.2B`. This
converts either way in one command, picking the direction for you: a bare
number gets a suffix, a suffixed number gets expanded.

## Install

```bash
pip install .
```

This installs a `numfmt-cli` command on your PATH.

## Usage

```bash
numfmt-cli 1234567            # number -> human
numfmt-cli 1.2M                # human -> number
numfmt-cli 1234567 --precision 3
```

Example output:

```
$ numfmt-cli 1234567
1.2M
$ numfmt-cli 1.2M
1200000
$ numfmt-cli 2300000000
2.3B
```

### Supported suffixes

| Suffix | Meaning   |
|--------|-----------|
| `K`    | thousand  |
| `M`    | million   |
| `B`    | billion   |
| `T`    | trillion  |

Suffixes are case-insensitive on input (`1.2m` works the same as `1.2M`).
Numbers under 1000 are printed with no suffix.

### Options

| Flag              | Description                                                     |
|-------------------|--------------------------------------------------------------------|
| `--precision N`   | Decimal places to show when formatting a number to human-readable form (default: 1) |

### Exit codes

| Code | Meaning                          |
|------|-----------------------------------|
| 0    | Converted successfully              |
| 2    | Input wasn't a recognizable number  |

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
