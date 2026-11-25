"""Copy the pre-rendered meme image to the output directory.

Standard library only, no network. The image entry.png lives in this
repository next to this program (rendered by render.py); both runs write
identical bytes.
"""
import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("missing entry.png next to main.py")
    dst = os.path.join(OUTPUT_DIR, "entry.png")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(src, dst)
    # Gate check: the image must stay a PNG of at most 1 MiB, 1024x1024.
    size = os.path.getsize(dst)
    if size > 1048576:
        raise SystemExit(f"entry.png too large for the gate: {size} bytes")
    print("wrote", dst, size, "bytes")


if __name__ == "__main__":
    main()
