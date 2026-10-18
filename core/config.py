"""Configuration globale de l'application Muse.

Tout ce qui est « réglable » (nom, chemins, profil par défaut, colonnes de la
mosaïque, options de thème) vit ici afin de garder le reste du code stable.
"""
from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# Identité de l'application
# ---------------------------------------------------------------------------
APP_NAME = "Muse"
APP_ICON = "🧣"
APP_TAGLINE = "Votre dressing infini"

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT, "assets")
CACHE_DIR = os.path.join(ASSETS_DIR, "cache")
CSS_PATH = os.path.join(ASSETS_DIR, "styles.css")
DATA_DIR = os.path.join(ROOT, "data")
STORE_PATH = os.path.join(DATA_DIR, "user_store.json")

# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------
MAX_WIDTH = 520        # largeur « mobile » de la colonne de contenu
MASONRY_COLS = 2       # Pinterest mobile = 2 colonnes
FEED_PAGE_SIZE = 12

# ---------------------------------------------------------------------------
# Devise (dirham marocain) et pays
# ---------------------------------------------------------------------------
CURRENCY = "MAD"
DEFAULT_COUNTRY = "Maroc"


def format_price(value: float | int | str | None, suffix: str | None = None) -> str:
    """Formate un montant en dirhams : ``1 250 MAD``."""
    try:
        amount = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "—"
    text = f"{amount:,.0f}".replace(",", "\u202f")
    return f"{text} {suffix or CURRENCY}"


# ---------------------------------------------------------------------------
# Profil utilisateur (démo — modifiable depuis « Mon compte »)
# ---------------------------------------------------------------------------
DEFAULT_PROFILE = {
    "name": "Sarah Belkacem",
    "handle": "@sarah.style",
    "city": "Maroc",
    "avatar": "🦋",
    "bio": "Mode modeste, belles matières et lignes simples.",
    "member_since": "Membre depuis 2024",
}

#: Compte de démonstration créé au premier lancement (connexion en un clic).
DEMO_ACCOUNT = {
    "id": "u_demo",
    "name": "Sarah Belkacem",
    "email": "sarah@muse.ma",
    "phone": "+212 6 61 22 33 44",
    "country": "Maroc",
    "password": "muse",
    "demo": True,
}
