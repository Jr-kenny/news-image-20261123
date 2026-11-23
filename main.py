#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261123 (Python 3.13, stdlib only).

Writes the composed front-page image shipped beside this file to
/output/entry.png. The image is stored base64-encoded as entry.png.b64
(the repository holds text); decoding reproduces the exact PNG bytes.
Deterministic: same input bytes, same output bytes.
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(HERE, "entry.png.b64")

# Fail loudly (rather than writing a partial output) if the image is missing.
if not os.path.isfile(SRC):
    raise SystemExit("entry.png.b64 not found beside main.py")

os.makedirs(OUT_DIR, exist_ok=True)
with open(SRC, "rb") as f:
    data = base64.b64decode(f.read())
# The decoded bytes must be the PNG the repository holds; refuse anything else.
if data[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("entry.png.b64 does not decode to a PNG")
with open(os.path.join(OUT_DIR, "entry.png"), "wb") as f:
    f.write(data)
