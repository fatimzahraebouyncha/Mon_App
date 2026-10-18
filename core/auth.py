"""Comptes utilisateurs de Muse : inscription, connexion, multi-comptes.

Tout est stocké localement dans ``data/user_store.json`` :

    {
      "version": 2,
      "active": "u_ab12",
      "users": {
        "u_ab12": {
          "id": "u_ab12",
          "name": "Sarah Belkacem",
          "email": "sarah@muse.ma",
          "phone": "+212661223344",
          "country": "Maroc",
          "password": "pbkdf2$<sel>$<empreinte>",
          "created": "2026-10-18",
          "demo": true,
          "data": { …dressing, wishlist, looks, points… }
        }
      }
    }

Chaque personne crée son compte avec son **e-mail ou son numéro de
téléphone**, choisit son pays (tous les pays du monde sont proposés) et
retrouve son dressing, sa wishlist et ses looks.

Pour une mise en production réelle, remplacer ce module par un backend
(API + base de données) : le reste de l'application ne change pas.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import secrets
import unicodedata
from typing import Any

import streamlit as st

from core.config import DEFAULT_COUNTRY, DEMO_ACCOUNT, STORE_PATH
from data import countries

STORAGE_VERSION = 2
MIN_PASSWORD = 4
MAX_ACCOUNTS = 40

AVATARS = ["🌸", "🦋", "🌙", "✨", "🌷", "🧣", "💎", "🫧", "🍃", "🌟", "💫", "🪷"]

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
_JUNK_RE = re.compile(r"[^\d+]")


# ---------------------------------------------------------------------------
# Stockage local
# ---------------------------------------------------------------------------
def _empty_store() -> dict[str, Any]:
    return {"version": STORAGE_VERSION, "active": None, "users": {}}


def _read() -> dict[str, Any]:
    """Lit le fichier de comptes (migration de l'ancien format incluse)."""
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        return _empty_store()
    if not isinstance(data, dict):
        return _empty_store()
    return _migrate(data)


def _write(store: dict[str, Any]) -> None:
    try:
        os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
        with open(STORE_PATH, "w", encoding="utf-8") as fh:
            json.dump(store, fh, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _migrate(data: dict[str, Any]) -> dict[str, Any]:
    """Ancien format (une seule utilisatrice) → format multi-comptes."""
    if isinstance(data.get("users"), dict):
        data.setdefault("version", STORAGE_VERSION)
        data.setdefault("active", None)
        return data

    legacy = {key: value for key, value in data.items() if key not in ("users", "version", "active")}
    store = _empty_store()
    user = _new_user(
        user_id=DEMO_ACCOUNT["id"],
        name=DEMO_ACCOUNT["name"],
        email=DEMO_ACCOUNT["email"],
        phone=DEMO_ACCOUNT["phone"],
        country=DEMO_ACCOUNT["country"],
        password=DEMO_ACCOUNT["password"],
        demo=True,
        data=legacy,
    )
    profile = legacy.get("profile")
    if isinstance(profile, dict):
        user["data"]["profile"] = {**user["data"].get("profile", {}), **profile}
    store["users"][user["id"]] = user
    store["active"] = user["id"]
    return store


# ---------------------------------------------------------------------------
# Fabrique de compte
# ---------------------------------------------------------------------------
def _hash_password(password: str) -> str:
    salt = secrets.token_hex(8)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 60_000)
    return f"pbkdf2${salt}${digest.hex()}"


def _verify_password(password: str, stored: str | None) -> bool:
    if not stored:
        return False
    try:
        scheme, salt, digest = stored.split("$")
        if scheme != "pbkdf2":
            return False
        check = hashlib.pbkdf2_hmac("sha256", (password or "").encode("utf-8"), salt.encode("utf-8"), 60_000)
        return secrets.compare_digest(check.hex(), digest)
    except Exception:
        return False


def slugify(text: str) -> str:
    """« Sarah Belkacem » → « sarah.belkacem » (pseudo)."""
    normalized = unicodedata.normalize("NFKD", text or "")
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    words = re.findall(r"[A-Za-z0-9]+", ascii_text.lower())
    return ".".join(words)[:24] or "muse"


def normalize_phone(value: str) -> str:
    """Garde les chiffres (et un éventuel « + » de tête)."""
    clean = _JUNK_RE.sub("", (value or "").strip())
    if clean.startswith("+"):
        return "+" + clean[1:]
    return clean


def _phone_key(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")


def identifier_of(user: dict[str, Any] | None) -> str:
    """E-mail si présent, sinon téléphone (identifiant de connexion)."""
    user = user or {}
    return str(user.get("email") or user.get("phone") or "")


def avatar_for(name: str) -> str:
    index = int(hashlib.md5((name or "muse").encode("utf-8")).hexdigest(), 16) % len(AVATARS)
    return AVATARS[index]


def _profile_for(name: str, country: str, avatar: str, *, starter: bool = False) -> dict[str, Any]:
    return {
        "name": name,
        "handle": "@" + slugify(name),
        "city": country or DEFAULT_COUNTRY,
        "avatar": avatar,
        "bio": "Nouvelle sur Muse ✨" if starter else "",
        "member_since": f"Membre depuis {_dt.date.today().year}",
    }


def profile_for_account(user: dict[str, Any] | None) -> dict[str, Any]:
    """Profil public (nom, avatar, ville) d'un compte."""
    user = user or {}
    stored = (user.get("data") or {}).get("profile")
    if isinstance(stored, dict) and stored:
        return dict(stored)
    name = str(user.get("name") or "Muse")
    return _profile_for(name, str(user.get("country") or DEFAULT_COUNTRY), avatar_for(name), starter=True)


def _new_user(
    *,
    user_id: str | None = None,
    name: str,
    email: str = "",
    phone: str = "",
    country: str = DEFAULT_COUNTRY,
    password: str,
    demo: bool = False,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    avatar = avatar_for(name)
    payload = dict(data or {})
    payload.setdefault("profile", _profile_for(name, country, avatar, starter=not demo))
    return {
        "id": user_id or f"u_{secrets.token_hex(4)}",
        "name": name.strip(),
        "email": (email or "").strip().lower(),
        "phone": normalize_phone(phone),
        "country": (country or DEFAULT_COUNTRY).strip(),
        "password": _hash_password(password),
        "created": _dt.date.today().isoformat(),
        "demo": bool(demo),
        "data": payload,
    }


def _demo_account(seed: dict[str, Any] | None) -> dict[str, Any]:
    return _new_user(
        user_id=DEMO_ACCOUNT["id"],
        name=DEMO_ACCOUNT["name"],
        email=DEMO_ACCOUNT["email"],
        phone=DEMO_ACCOUNT["phone"],
        country=DEMO_ACCOUNT["country"],
        password=DEMO_ACCOUNT["password"],
        demo=True,
        data=seed or {},
    )


# ---------------------------------------------------------------------------
# Cycle de vie
# ---------------------------------------------------------------------------
def bootstrap(seed: dict[str, Any] | None = None) -> None:
    """Prépare le fichier de comptes (compte de démo au premier lancement)."""
    store = _read()
    users = store.get("users")
    if not isinstance(users, dict) or not users:
        store = _empty_store()
        demo = _demo_account(seed)
        store["users"][demo["id"]] = demo
        store["active"] = demo["id"]
        _write(store)
    st.session_state.setdefault("_user_id", None)


def current_user() -> dict[str, Any] | None:
    """Compte connecté dans cette session (``None`` = écran de connexion)."""
    user_id = st.session_state.get("_user_id")
    if not user_id:
        return None
    return (_read().get("users") or {}).get(user_id)


def user_id() -> str | None:
    return (current_user() or {}).get("id")


def is_demo(user: dict[str, Any] | None = None) -> bool:
    target = user if user is not None else (current_user() or {})
    return bool(target.get("demo"))


def last_user_id() -> str | None:
    """Dernier compte utilisé (mis en avant sur l'écran de connexion)."""
    return _read().get("active")


# ---------------------------------------------------------------------------
# Comptes connus (appareil)
# ---------------------------------------------------------------------------
def accounts() -> list[dict[str, Any]]:
    """Résumés des comptes déjà créés sur cet appareil."""
    users = (_read().get("users") or {}).values()
    summaries = [
        {
            "id": user.get("id"),
            "name": user.get("name", ""),
            "identifier": identifier_of(user),
            "country": user.get("country", ""),
            "avatar": (user.get("data", {}).get("profile") or {}).get("avatar") or avatar_for(user.get("name", "")),
            "demo": bool(user.get("demo")),
        }
        for user in users
        if isinstance(user, dict)
    ]
    summaries.sort(key=lambda row: (not row["demo"], row["name"].lower()))
    return summaries


def find(identifier: str) -> dict[str, Any] | None:
    """Retrouve un compte par e-mail ou par numéro de téléphone."""
    raw = (identifier or "").strip()
    if not raw:
        return None
    wanted_email = raw.lower()
    wanted_phone = _phone_key(raw)
    for user in (_read().get("users") or {}).values():
        if not isinstance(user, dict):
            continue
        if user.get("email") and str(user["email"]).lower() == wanted_email:
            return user
        if wanted_phone and len(wanted_phone) >= 6 and _phone_key(user.get("phone")) == wanted_phone:
            return user
    return None


def _conflict(email: str, phone: str) -> str | None:
    """Message d'erreur si l'e-mail ou le téléphone est déjà utilisé."""
    if email and any(
        isinstance(user, dict) and str(user.get("email", "")).lower() == email
        for user in (_read().get("users") or {}).values()
    ):
        return "Un compte existe déjà avec cet e-mail."
    key = _phone_key(phone)
    if key and len(key) >= 6 and any(
        isinstance(user, dict) and _phone_key(user.get("phone")) == key
        for user in (_read().get("users") or {}).values()
    ):
        return "Un compte existe déjà avec ce numéro de téléphone."
    return None


# ---------------------------------------------------------------------------
# Inscription / connexion
# ---------------------------------------------------------------------------
def signup(
    *,
    name: str,
    email: str = "",
    phone: str = "",
    password: str,
    country: str = DEFAULT_COUNTRY,
) -> tuple[bool, str]:
    """Crée un compte (e-mail ou téléphone) et connecte la personne."""
    clean_name = (name or "").strip()
    clean_email = (email or "").strip().lower()
    clean_phone = normalize_phone(phone)
    country_name = (country or DEFAULT_COUNTRY).strip()

    if len(clean_name) < 2:
        return False, "Indiquez votre nom (2 caractères minimum)."
    if not clean_email and not clean_phone:
        return False, "Un e-mail ou un numéro de téléphone est nécessaire."
    if clean_email and not _EMAIL_RE.match(clean_email):
        return False, "Cet e-mail semble incorrect (exemple : nom@exemple.com)."
    if clean_phone and len(_phone_key(clean_phone)) < 8:
        return False, "Ce numéro de téléphone semble incomplet."
    if len(password or "") < MIN_PASSWORD:
        return False, f"Choisissez un mot de passe de {MIN_PASSWORD} caractères minimum."
    if len((_read().get("users") or {})) >= MAX_ACCOUNTS:
        return False, "Limite de comptes atteinte sur cet appareil."

    conflict = _conflict(clean_email, clean_phone)
    if conflict:
        return False, conflict

    store = _read()
    user = _new_user(
        name=clean_name,
        email=clean_email,
        phone=clean_phone,
        country=country_name,
        password=password,
    )
    store.setdefault("users", {})[user["id"]] = user
    store["active"] = user["id"]
    _write(store)
    _activate(user["id"])
    return True, f"Bienvenue {clean_name.split()[0]} ! Votre dressing vous attend."


def login(identifier: str, password: str) -> tuple[bool, str]:
    """Connexion par e-mail ou téléphone."""
    user = find(identifier)
    if not user:
        return False, "Aucun compte ne correspond à cet e-mail ou ce numéro."
    if not _verify_password(password or "", user.get("password")):
        return False, "Mot de passe incorrect."
    _activate(user["id"])
    first = str(user.get("name", "")).split()[0] if user.get("name") else ""
    return True, f"Bon retour {first} !" if first else "Bon retour !"


def login_demo() -> None:
    """Connexion en un clic au compte de démonstration."""
    _activate(DEMO_ACCOUNT["id"])


def _clear_transient() -> None:
    """Efface filtres et valeurs de widgets : une session qui change de compte repart propre."""
    keep = {"_toasts"}
    for key in list(st.session_state.keys()):
        if key in keep:
            continue
        try:
            st.session_state.pop(key, None)
        except Exception:
            pass


def logout() -> None:
    """Déconnecte la session (le compte reste enregistré)."""
    _clear_transient()
    st.session_state["_user_id"] = None
    st.session_state["_page"] = "home"


def _activate(user_id_value: str) -> None:
    """Connecte un compte et repart d'un état propre."""
    store = _read()
    if user_id_value not in (store.get("users") or {}):
        return
    store["active"] = user_id_value
    _write(store)
    _clear_transient()
    st.session_state["_user_id"] = user_id_value
    st.session_state["_page"] = "home"
    try:
        st.query_params.pop("page", None)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Données du compte (utilisées par core.state)
# ---------------------------------------------------------------------------
def user_data(user_id_value: str | None) -> dict[str, Any]:
    user = (_read().get("users") or {}).get(user_id_value or "")
    if not isinstance(user, dict):
        return {}
    data = user.get("data")
    return data if isinstance(data, dict) else {}


def save_user_data(user_id_value: str | None, payload: dict[str, Any]) -> None:
    if not user_id_value:
        return
    store = _read()
    users = store.get("users") or {}
    user = users.get(user_id_value)
    if not isinstance(user, dict):
        return
    user["data"] = payload
    store["active"] = user_id_value
    _write(store)


def update_account(user_id_value: str | None, **changes: Any) -> bool:
    """Met à jour les informations du compte (nom, pays…)."""
    store = _read()
    user = (store.get("users") or {}).get(user_id_value or "")
    if not isinstance(user, dict):
        return False
    for key, value in changes.items():
        if key == "phone":
            value = normalize_phone(str(value))
        if key in ("email", "name", "country", "phone"):
            user[key] = value
    _write(store)
    return True


def account_email_taken(email: str, except_id: str | None = None) -> bool:
    email = (email or "").strip().lower()
    if not email:
        return False
    for key, user in (_read().get("users") or {}).items():
        if key == except_id or not isinstance(user, dict):
            continue
        if str(user.get("email", "")).lower() == email:
            return True
    return False


def country_list() -> list[str]:
    """Tous les pays proposés à l'inscription."""
    return list(countries.NAMES)
