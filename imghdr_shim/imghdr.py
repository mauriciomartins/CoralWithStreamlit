"""Installable imghdr shim module.

This is the same detection logic used by the project's top-level `imghdr.py` shim,
but packaged here as a top-level module so `import imghdr` works after installation.
"""
from __future__ import annotations

import os
from typing import Optional

_MAX_HEADER = 64


def _read_header(fp) -> bytes:
    try:
        pos = None
        if hasattr(fp, "seek"):
            try:
                pos = fp.tell()
            except Exception:
                pos = None
        data = fp.read(_MAX_HEADER)
        if pos is not None:
            try:
                fp.seek(pos)
            except Exception:
                pass
        return data or b""
    except Exception:
        return b""


def _header_detect(header: bytes) -> Optional[str]:
    if header.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if header.startswith(b"BM"):
        return "bmp"
    if header.startswith(b"II\x2A\x00") or header.startswith(b"MM\x00\x2A"):
        return "tiff"
    if header.startswith(b"RIFF") and len(header) >= 12 and header[8:12] == b"WEBP":
        return "webp"
    if header.startswith(b"P4"):
        return "pbm"
    if header.startswith(b"P5"):
        return "pgm"
    if header.startswith(b"P6"):
        return "ppm"
    if header.startswith(b"RGB"):
        return "rgb"
    return None


def what(file: object) -> Optional[str]:
    try:
        from PIL import Image
    except Exception:
        Image = None

    if isinstance(file, (str, os.PathLike)):
        path = os.fspath(file)
        if Image is not None:
            try:
                with Image.open(path) as im:
                    fmt = im.format
                    return fmt.lower() if fmt else None
            except Exception:
                pass
        try:
            with open(path, "rb") as f:
                header = _read_header(f)
                return _header_detect(header)
        except Exception:
            return None

    if hasattr(file, "read"):
        if Image is not None:
            try:
                pos = None
                if hasattr(file, "tell"):
                    try:
                        pos = file.tell()
                    except Exception:
                        pos = None
                im = Image.open(file)
                fmt = im.format
                try:
                    im.close()
                except Exception:
                    pass
                if pos is not None:
                    try:
                        file.seek(pos)
                    except Exception:
                        pass
                return fmt.lower() if fmt else None
            except Exception:
                try:
                    if hasattr(file, "seek"):
                        file.seek(0)
                except Exception:
                    pass
        header = _read_header(file)
        return _header_detect(header)

    return None


__all__ = ["what"]
