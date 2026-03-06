"""imghdr shim that prefers Pillow when available.

This module implements a `what()` function with the same basic
semantics as the stdlib `imghdr.what`. If Pillow (`PIL`) is
installed, it uses `PIL.Image` to detect the image format reliably.
If Pillow is not available, it falls back to a lightweight header
inspection implementation.
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
    """Detect image type.

    `file` may be a filename (str / os.PathLike) or a file-like object
    with a `read()` method.
    """
    # Prefer Pillow if available — it's more reliable for many formats.
    try:
        from PIL import Image
    except Exception:
        Image = None

    # If file is a path, open it.
    if isinstance(file, (str, os.PathLike)):
        path = os.fspath(file)
        if Image is not None:
            try:
                with Image.open(path) as im:
                    fmt = im.format
                    return fmt.lower() if fmt else None
            except Exception:
                pass
        # fallback to header
        try:
            with open(path, "rb") as f:
                header = _read_header(f)
                return _header_detect(header)
        except Exception:
            return None

    # file-like object
    if hasattr(file, "read"):
        if Image is not None:
            try:
                # PIL expects a file-like object with read/seek
                # keep current position
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
                # reset pointer and try header detection
                try:
                    if hasattr(file, "seek"):
                        file.seek(0)
                except Exception:
                    pass
        # header fallback
        header = _read_header(file)
        return _header_detect(header)

    return None


__all__ = ["what"]
