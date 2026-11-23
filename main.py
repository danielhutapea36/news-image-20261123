#!/usr/bin/env python3
"""Reproduce the bundled front-page image for make.fun news-image-20261123.

The entry image (``entry.png``) is a 1024x1024 grayscale newspaper front
page, "WORLD NEWS — Monday 23 November 2026", with six panels covering
the day's stories: tankers hit in the Strait of Hormuz, the Russian
corvette Merkury sunk off Benghazi, deadly strikes in the Kyiv region,
COP31 closing without a deal, BepiColombo entering orbit around Mercury,
and the factory fire in Cikande, Indonesia.

This program does not regenerate the artwork. It takes the bundled
``entry.png`` that sits next to this script, validates it thoroughly
(PNG signature, size cap, pixel dimensions, SHA-256 digest), writes an
exact byte-for-byte copy into the output directory, and then reads the
copy back to prove it is identical to the source before printing a
short report. It uses only the Python standard library, touches no
network, and involves no randomness or timestamps, so repeated runs
produce identical bytes.

Usage::

    MAKEFUN_OUTPUT_DIR=/tmp/ni23-out python3 main.py
    python3 main.py --out-dir /tmp/ni23-out
    python3 main.py --verify-only        # check the source, write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import os
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"

# Fingerprint of the bundled image, recorded in README.md under "The image".
EXPECTED_SHA256 = (
    "26acfec885cbdcfe1c8ad4a69a986eb002a43d399361648fa43abdee9b9acf04"
)
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

# Competition cap: the reproduced file must stay under one mebibyte.
MAX_SIZE_BYTES = 1024 * 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


class ReproductionError(Exception):
    """Raised when the source image fails a check or the copy is unfaithful."""


def script_directory() -> Path:
    """Directory holding this script (and therefore the bundled image)."""
    return Path(__file__).resolve().parent


def resolve_output_dir(cli_value: str | None) -> Path:
    """Pick the output directory: CLI flag wins, then env var, then default.

    An explicitly set but empty $MAKEFUN_OUTPUT_DIR is treated as a
    configuration mistake rather than silently falling back to the
    default, so a typo in the environment is caught instead of writing
    the copy somewhere unexpected.
    """
    if cli_value:
        return Path(cli_value)
    env_value = os.environ.get(OUTPUT_ENV_VAR)
    if env_value is not None:
        if not env_value.strip():
            raise ReproductionError(
                f"{OUTPUT_ENV_VAR} is set but empty; unset it or give "
                "a directory"
            )
        return Path(env_value)
    return Path(DEFAULT_OUTPUT_DIR)


def build_parser() -> argparse.ArgumentParser:
    """Command-line parser for the reproducer."""
    parser = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "Validate the bundled entry.png and write an identical copy "
            "into the output directory."
        ),
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help=(
            "output directory (overrides $MAKEFUN_OUTPUT_DIR, "
            f"default {DEFAULT_OUTPUT_DIR})"
        ),
    )
    parser.add_argument(
        "--source",
        default=None,
        help="path to the source PNG (default: entry.png next to main.py)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="only validate the source image; do not write a copy",
    )
    return parser


def load_source(path: Path) -> bytes:
    """Read the source PNG, failing with a plain message when absent."""
    try:
        return path.read_bytes()
    except FileNotFoundError:
        raise ReproductionError(f"source image not found: {path}") from None
    except OSError as exc:
        raise ReproductionError(f"cannot read source image {path}: {exc}") from None


def check_signature(data: bytes) -> None:
    """Confirm the first eight bytes are the PNG signature."""
    if data[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise ReproductionError(
            "source is not a PNG file: bad signature "
            f"(first bytes are {data[:8]!r})"
        )


def check_size(data: bytes) -> None:
    """Enforce the one-mebibyte size cap on the source image."""
    if len(data) > MAX_SIZE_BYTES:
        raise ReproductionError(
            f"source image is {len(data)} bytes, over the "
            f"{MAX_SIZE_BYTES} byte cap"
        )


def read_dimensions(data: bytes) -> tuple[int, int]:
    """Parse width and height out of the PNG IHDR chunk.

    The IHDR chunk starts right after the 8-byte signature: 4 bytes of
    chunk length, 4 bytes of chunk type ("IHDR"), then width and height
    as big-endian unsigned 32-bit integers.
    """
    minimum = 8 + 4 + 4 + 8
    if len(data) < minimum:
        raise ReproductionError(
            f"source image is only {len(data)} bytes, too short for a PNG header"
        )
    chunk_type = data[12:16]
    if chunk_type != b"IHDR":
        raise ReproductionError(
            f"first PNG chunk is {chunk_type!r}, expected b'IHDR'"
        )
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_dimensions(width: int, height: int) -> None:
    """Require the exact 1024x1024 canvas the bounty entry was built on."""
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ReproductionError(
            f"source image is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )


def digest_hex(data: bytes) -> str:
    """SHA-256 hex digest of a byte string."""
    return hashlib.sha256(data).hexdigest()


def check_digest(data: bytes) -> str:
    """Require the source bytes to match the fingerprint in README.md."""
    actual = digest_hex(data)
    if actual != EXPECTED_SHA256:
        raise ReproductionError(
            "source image digest mismatch: "
            f"got {actual}, expected {EXPECTED_SHA256}"
        )
    return actual


def validate(data: bytes) -> tuple[int, int, str]:
    """Run every source check in order; return (width, height, digest)."""
    check_signature(data)
    check_size(data)
    width, height = read_dimensions(data)
    check_dimensions(width, height)
    digest = check_digest(data)
    return width, height, digest


def write_copy(data: bytes, out_dir: Path) -> Path:
    """Write the exact bytes into the output directory as entry.png."""
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        destination = out_dir / SOURCE_NAME
        destination.write_bytes(data)
    except OSError as exc:
        raise ReproductionError(
            f"cannot write copy into {out_dir}: {exc}"
        ) from None
    return destination


def confirm_copy(destination: Path, expected: bytes) -> None:
    """Read the copy back and prove it matches the source byte for byte."""
    try:
        written = destination.read_bytes()
    except OSError as exc:
        raise ReproductionError(
            f"cannot read back the copy at {destination}: {exc}"
        ) from None
    if written != expected:
        raise ReproductionError(
            f"copy at {destination} differs from the source "
            f"({len(written)} bytes written, {len(expected)} expected)"
        )


def human_size(num_bytes: int) -> str:
    """Render a byte count as a short human-readable string."""
    units = ("bytes", "KiB", "MiB")
    value = float(num_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "bytes":
                return f"{num_bytes} bytes"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{num_bytes} bytes"


def report(
    width: int, height: int, digest: str, num_bytes: int, destination: Path | None
) -> str:
    """One short multi-line report of what was validated and written."""
    lines = [
        f"validated {SOURCE_NAME}: {width}x{height}, "
        f"{human_size(num_bytes)}, sha256 {digest}",
    ]
    if destination is not None:
        lines.append(f"wrote identical copy to {destination}")
    else:
        lines.append("verify-only: no copy written")
    return "\n".join(lines)


def reproduce(out_dir: Path, source: Path, verify_only: bool) -> str:
    """Validate the source and, unless asked otherwise, reproduce it."""
    data = load_source(source)
    width, height, digest = validate(data)
    if verify_only:
        return report(width, height, digest, len(data), None)
    destination = write_copy(data, out_dir)
    confirm_copy(destination, data)
    return report(width, height, digest, len(data), destination)


def main(argv: list[str] | None = None) -> int:
    """Entry point: parse options, reproduce, print the report."""
    args = build_parser().parse_args(argv)
    base = script_directory()
    source = Path(args.source) if args.source else base / SOURCE_NAME
    try:
        # Resolving the output directory can fail too (an empty env var
        # is a configuration error), so it lives inside the same guard
        # as the reproduction itself.
        out_dir = resolve_output_dir(args.out_dir)
        print(reproduce(out_dir, source, args.verify_only))
    except ReproductionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
