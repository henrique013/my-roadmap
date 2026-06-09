from __future__ import annotations

import re
import unicodedata


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def normalize_slug(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    if not text:
        raise ValueError("slug cannot be empty after normalization")
    return text


def validate_slug(value: str) -> str:
    if value in {".", ".."} or "/" in value or "\\" in value:
        raise ValueError(f"unsafe slug: {value!r}")
    if not SLUG_RE.match(value):
        raise ValueError(f"invalid slug: {value!r}")
    return value
