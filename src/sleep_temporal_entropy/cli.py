"""Command-line interface for Sleep Temporal Entropy."""

import argparse
import json
from typing import Optional, Sequence

from .core import calculate_sleep_temporal_entropy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate Sleep Temporal Entropy from an NSRR-style XML annotation."
    )
    parser.add_argument("annotation", help="Path to an NSRR-style XML annotation file.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    result = calculate_sleep_temporal_entropy(args.annotation)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
