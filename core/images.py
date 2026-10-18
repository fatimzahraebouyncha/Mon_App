"""Chargement des visuels avec cache disque + repli élégant hors connexion.

Stratégie :
1. L'image distante (Unsplash) est téléchargée une fois puis mise en cache
   dans ``assets/cache`` → les lancements suivants sont instantanés.
2. Si le réseau est absent (ou l'image supprimée), on génère un dégradé
   harmonieux avec Pillow pour garder une interface soignée.
"""
from __future__ import annotations

import hashlib
import io
import os
import urllib.request
import zlib
import struct

import streamlit as st

from core.config import CACHE_DIR

UNSPLASH_BASE = "https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&h={h}&q=72"

# Palettes des visuels de secours (chaudes, cohérentes avec le thème)
_PALETTES = [
    ((244, 233, 221), (206, 168, 138)),
    ((238, 226, 216), (176, 138, 122)),
    ((232, 220, 214), (140, 106, 96)),
    ((245, 238, 226), (198, 160, 116)),
    ((236, 224, 226), (168, 122, 130)),
    ((226, 228, 222), (134, 148, 122)),
    ((232, 226, 240), (140, 130, 168)),
    ((248, 240, 232), (196, 154, 122)),
]


# ---------------------------------------------------------------------------
# Utilitaires bas niveau
# ---------------------------------------------------------------------------
def _digest(text: str, size: int = 16) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:size]


def unsplash_url(photo_id: str, width: int, height: int) -> str:
    """Construit l'URL Unsplash redimensionnée (crop automatique)."""
    return UNSPLASH_BASE.format(pid=photo_id, w=int(width), h=int(height))


def unsplash_banner_url(photo_id: str, width: int, height: int) -> str:
    """URL Unsplash d'un bandeau : recadrage intelligent sur les visages."""
    return unsplash_url(photo_id, width, height) + "&crop=faces,entropy"


def _cache_file(url: str) -> str:
    return os.path.join(CACHE_DIR, _digest(url) + ".bin")


def _download(url: str) -> bytes | None:
    """Télécharge (et met en cache disque) une image. ``None`` si indisponible."""
    if not url:
        return None
    path = _cache_file(url)
    if os.path.exists(path):
        try:
            with open(path, "rb") as fh:
                data = fh.read()
            if data:
                return data
        except OSError:
            pass
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Muse app)"})
        with urllib.request.urlopen(request, timeout=6) as response:
            data = response.read()
        if not data:
            return None
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(data)
        except OSError:
            pass
        return data
    except Exception:  # réseau, DNS, 404, timeout…
        return None


def _tiny_png(rgb: tuple[int, int, int]) -> bytes:
    """PNG 1x1 uni (repli ultime si Pillow n'est pas disponible)."""

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw = b"\x00" + bytes(rgb)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def gradient(seed: str, width: int, height: int) -> bytes:
    """Visuel de remplacement : dégradé doux + formes translucides."""
    idx = int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16) % len(_PALETTES)
    top, bottom = _PALETTES[idx]
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except Exception:
        mix = tuple((top[i] + bottom[i]) // 2 for i in range(3))
        return _tiny_png(mix)

    width, height = max(int(width), 24), max(int(height), 24)
    image = Image.new("RGB", (width, height), top)
    draw = ImageDraw.Draw(image, "RGBA")
    for y in range(height):
        t = y / max(height - 1, 1)
        draw.line(
            [(0, y), (width, y)],
            fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)),
        )

    grain = int(hashlib.md5((seed + "forms").encode()).hexdigest(), 16)
    for step in range(3):
        radius = width * (0.34 - step * 0.07)
        cx = (grain >> (step * 5) & 0xFF) / 255 * width
        cy = (grain >> (step * 7 + 3) & 0xFF) / 255 * height
        alpha = 34 - step * 9
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=(255, 255, 255, alpha),
        )
    draw.line([(0, height * 0.62), (width, height * 0.38)], fill=(255, 255, 255, 40), width=2)
    image = image.filter(ImageFilter.GaussianBlur(0.6))

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=84)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False, max_entries=400)
def bytes_for(url: str, width: int, height: int, seed: str) -> bytes:
    """Octets de l'image (réseau → cache disque → dégradé généré)."""
    data = _download(url)
    if data:
        return data
    return gradient(seed, width, height)


def photo(photo_id: str | None, seed: str, width: int = 520, ratio: float = 0.78) -> bytes:
    """Visuel d'une pièce (``ratio`` = largeur / hauteur)."""
    height = int(round(width / max(ratio, 0.3)))
    url = unsplash_url(photo_id, width, height) if photo_id else ""
    return bytes_for(url, width, height, seed)


def square(photo_id: str | None, seed: str, size: int = 220) -> bytes:
    """Visuel carré (avatars stylistes, marques…)."""
    return photo(photo_id, seed, width=size, ratio=1.0)


def for_item(item: dict, width: int = 520) -> bytes:
    """Visuel d'un élément du catalogue (dict avec ``photo`` et ``ratio``)."""
    return photo(item.get("photo"), item.get("id", "item"), width=width, ratio=float(item.get("ratio", 0.78)))


def banner(photo_id: str | None, width: int = 760, height: int = 430, seed: str = "banner") -> bytes:
    """Grande photo d'ouverture (bandeau éditorial, recadrée sur le sujet)."""
    url = unsplash_banner_url(photo_id, width, height) if photo_id else ""
    return bytes_for(url, width, height, seed)


def cache_dir_size() -> int:
    """Taille approximative du cache disque (en octets)."""
    total = 0
    if not os.path.isdir(CACHE_DIR):
        return 0
    for name in os.listdir(CACHE_DIR):
        path = os.path.join(CACHE_DIR, name)
        if os.path.isfile(path):
            try:
                total += os.path.getsize(path)
            except OSError:
                continue
    return total
