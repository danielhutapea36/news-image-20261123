#!/usr/bin/env python3
"""World News — Monday 23 November 2026 (make.fun news-image-20261123).

The entry image is bundled next to this program as ``entry.png``.  This
program does one job: it places an exact, byte-for-byte copy of that
image at ``$MAKEFUN_OUTPUT_DIR/entry.png`` (``/output`` when the
variable is unset), after checking that the source really is the PNG
this entry ships.

Nothing is drawn, downloaded or randomised here.  The same input always
produces the same output, so running the program twice writes identical
bytes.  Any problem — a missing source, a wrong file type, a failed
copy — stops the run with exit code 1 and a plain-language message,
and never leaves a half-written file behind.
"""

import hashlib
import os
import sys

PNG_MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
SOURCE_FILENAME = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1048576  # the competition caps the image at 1 MiB


def fail(message):
    """Print an error to stderr and stop with a non-zero exit code."""
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def script_folder():
    """Absolute path of the directory holding this program."""
    return os.path.dirname(os.path.abspath(__file__))


def output_folder():
    """Where the entry must be written, from the environment."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not folder:
        fail("MAKEFUN_OUTPUT_DIR is set but empty")
    return folder


def digest(data):
    """SHA-256 hex digest of a bytes object."""
    return hashlib.sha256(data).hexdigest()


def png_dimensions(data):
    """Return (width, height) from a PNG's IHDR chunk, or None."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return (width, height)


def load_source():
    """Read and validate the bundled entry.png; return its bytes."""
    path = os.path.join(script_folder(), SOURCE_FILENAME)
    if not os.path.isfile(path):
        fail("source image not found next to main.py: " + path)
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("could not read " + path + ": " + str(exc))
    if data[:8] != PNG_MAGIC:
        fail("source image does not start with the PNG signature")
    if len(data) > MAX_BYTES:
        fail(
            "source image is %d bytes, over the 1 MiB cap" % len(data)
        )
    size = png_dimensions(data)
    if size is None:
        fail("source image has no readable PNG header")
    if size != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(
            "source image is %dx%d, expected %dx%d"
            % (size[0], size[1], EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    return data


def write_copy(data, folder):
    """Write the bytes to folder/entry.png and confirm the copy."""
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as exc:
        fail("could not create output folder " + folder + ": " + str(exc))
    target = os.path.join(folder, SOURCE_FILENAME)
    try:
        with open(target, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("could not write " + target + ": " + str(exc))
    try:
        with open(target, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        fail("could not read back " + target + ": " + str(exc))
    if written != data:
        fail("written copy differs from the source image")
    return target


def run():
    """Load the bundled image, copy it out, and report what was done."""
    image = load_source()
    target = write_copy(image, output_folder())
    print("wrote " + target)
    print("size: %d bytes" % len(image))
    print("sha256: " + digest(image))
    print("dimensions: %dx%d" % (EXPECTED_WIDTH, EXPECTED_HEIGHT))


if __name__ == "__main__":
    run()
