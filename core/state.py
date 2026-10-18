"""État de session de Muse : valeurs par défaut, persistance par compte, helpers.

Chaque compte connecté possède son propre espace (dressing, wishlist, looks,
points…) : ``init_state`` charge les données du compte actif et ``save_state``
les réécrit dans ``data/user_store.json`` (via :mod:`core.auth`).
"""
from __future__ import annotations

import copy
from typing import Any, Iterable

import streamlit as st

from core import auth
from core.config import DEFAULT_PROFILE

# ---------------------------------------------------------------------------
# Schéma d'état
# ---------------------------------------------------------------------------
DEFAULT_STATE: dict[str, Any] = {
    # Collections utilisateur
    "saved": [],            # inspirations enregistrées (favoris du feed)
    "liked": [],            # coups de cœur (❤️)
    "wardrobe": [],         # garde-robe digitale
    "wishlist": [],         # envies / cadeaux
    "looks": [],            # looks créés
    "appointments": [],     # rendez-vous stylistes
    "followed_brands": [],  # marques suivies
    "style_profile": {},    # résultat du test de style
    "points": 0,            # fidélité
    "badges": [],           # badges obtenus
    "challenges": {},       # {id_defi: True}
    "rewards_claimed": [],  # récompenses échangées
    # Navigation / filtres (non persistés)
    "feed_category": "tout",
    "explore_tab": "Style",
    "account_tab": "Dressing",
    "search": "",
    "profile": dict(DEFAULT_PROFILE),
}

#: Champs écrits dans ``data/user_store.json`` entre deux lancements.
PERSISTED: tuple[str, ...] = (
    "saved", "liked", "wardrobe", "wishlist", "looks", "appointments",
    "followed_brands", "style_profile", "points", "badges", "challenges",
    "rewards_claimed", "profile",
)

_EMPTY = (None, "", [], {})


# ---------------------------------------------------------------------------
# Cycle de vie
# ---------------------------------------------------------------------------
def init_state(seed: dict[str, Any] | None = None) -> None:
    """Charge l'espace du compte connecté (et les données de démo du 1er lancement)."""
    account_id = auth.user_id()
    if st.session_state.get("_initialized") and st.session_state.get("_state_user") == account_id:
        return

    stored = auth.user_data(account_id)
    account = auth.current_user() or {}
    for key, default in DEFAULT_STATE.items():
        value = stored.get(key) if key in stored else None
        if value in _EMPTY:
            value = copy.deepcopy(default)
        st.session_state[key] = value

    if not stored and seed:
        for key, value in seed.items():
            if st.session_state.get(key) in _EMPTY:
                st.session_state[key] = copy.deepcopy(value)

    if account:
        st.session_state["profile"] = auth.profile_for_account(account)

    st.session_state["_state_user"] = account_id
    st.session_state["_initialized"] = True


def save_state() -> None:
    """Persiste l'espace du compte actif sur disque (silencieux en cas d'échec)."""
    account_id = st.session_state.get("_state_user") or auth.user_id()
    if not account_id:
        return
    payload: dict[str, Any] = {}
    for key in PERSISTED:
        value = st.session_state.get(key)
        payload[key] = list(value) if isinstance(value, set) else copy.deepcopy(value)
    auth.save_user_data(account_id, payload)


def reset_state(seed: dict[str, Any] | None = None) -> None:
    """Vide l'espace du compte (ou le recharge avec les données de démo)."""
    account_id = auth.user_id()
    auth.save_user_data(account_id, copy.deepcopy(seed) if seed else {})
    for key in PERSISTED:
        st.session_state.pop(key, None)
    st.session_state["_initialized"] = False


# ---------------------------------------------------------------------------
# Helpers de lecture / écriture
# ---------------------------------------------------------------------------
def bucket(key: str) -> list:
    """Retourne une collection de session (créée au besoin)."""
    if not isinstance(st.session_state.get(key), list):
        st.session_state[key] = []
    return st.session_state[key]


def phonebook(key: str) -> dict:
    if not isinstance(st.session_state.get(key), dict):
        st.session_state[key] = {}
    return st.session_state[key]


def contains(key: str, value: str) -> bool:
    return value in bucket(key)


def toggle(key: str, value: str) -> bool:
    """Ajoute/retire une valeur. Retourne ``True`` si elle est désormais présente."""
    items = bucket(key)
    if value in items:
        items.remove(value)
        save_state()
        return False
    items.insert(0, value)
    save_state()
    return True


def ids(key: str) -> list[str]:
    return list(bucket(key))


def add_entry(key: str, entry: dict, *, unique_on: str | None = "id") -> bool:
    """Ajoute un dict dans une collection. ``False`` si déjà présent."""
    items = bucket(key)
    if unique_on and entry.get(unique_on) is not None:
        if any(item.get(unique_on) == entry[unique_on] for item in items):
            return False
    items.insert(0, entry)
    save_state()
    return True


def remove_entry(key: str, entry_id: str, field: str = "id") -> bool:
    items = bucket(key)
    for index, item in enumerate(items):
        if isinstance(item, dict) and item.get(field) == entry_id:
            del items[index]
            save_state()
            return True
    return False


def update_entry(key: str, entry_id: str, **changes: Any) -> bool:
    for item in bucket(key):
        if isinstance(item, dict) and item.get("id") == entry_id:
            item.update(changes)
            save_state()
            return True
    return False


def add_points(amount: int) -> None:
    st.session_state["points"] = int(st.session_state.get("points", 0)) + int(amount)
    save_state()


def spend_points(amount: int) -> bool:
    current = int(st.session_state.get("points", 0))
    if current < amount:
        return False
    st.session_state["points"] = current - int(amount)
    save_state()
    return True


# ---------------------------------------------------------------------------
# Notifications différées (affichées en fin de rendu par le routeur)
# ---------------------------------------------------------------------------
def push_toast(message: str, icon: str = "✨") -> None:
    st.session_state.setdefault("_toasts", []).append((icon, message))


def flush_toasts() -> None:
    pending: list[Iterable] = st.session_state.get("_toasts") or []
    st.session_state["_toasts"] = []
    for icon, message in pending:
        try:
            st.toast(message, icon=icon)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Accès catalogue ↔ collections utilisateur
# ---------------------------------------------------------------------------
def entry_ids(key: str, field: str = "id") -> set[str]:
    return {item.get(field) for item in bucket(key) if isinstance(item, dict)}
