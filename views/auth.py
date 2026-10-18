"""Écran de connexion et de création de compte (Muse, ouverte à tout le monde).

Chaque personne crée son compte avec son **e-mail ou son numéro de téléphone**
et choisit son pays : toutes les régions du monde sont proposées.
"""
from __future__ import annotations

import streamlit as st

from core import auth, components, images, state
from core.config import APP_TAGLINE, DEFAULT_COUNTRY, DEMO_ACCOUNT
from data import catalogue, countries

MODES = ["Se connecter", "Créer un compte"]


# ---------------------------------------------------------------------------
# En-tête
# ---------------------------------------------------------------------------
def _header() -> None:
    components.html(
        f'<div class="mp-auth-head"><div class="mp-logo">Muse<em>.</em></div>'
        f'<div class="mp-muted">{APP_TAGLINE}</div></div>'
    )
    components.hero(
        "Bienvenue",
        "Votre style, partout dans le monde",
        "Créez votre compte avec un e-mail ou un numéro de téléphone : dressing, wishlist, "
        "looks et rendez-vous vous suivent. Hijabs, abayas, kaftans, tenues modestes et toutes "
        "les pièces qui vous ressemblent.",
        photo=images.banner(catalogue.MODEST_PHOTOS["hero_monde"], seed="hero_monde"),
        extra_class="mp-auth-hero",
    )
    components.html(
        '<div class="mp-panel tint"><h4>🌍 Tout le monde est bienvenu</h4>'
        "<p>Choisissez votre pays à l'inscription : les prix sont affichés en dirhams (MAD) "
        "et nos stylistes vous reçoivent en visioconférence, où que vous soyez.</p></div>"
    )


# ---------------------------------------------------------------------------
# Connexion
# ---------------------------------------------------------------------------
def _login_form() -> None:
    nonce = st.session_state.get("auth_nonce", 0)
    prefill = st.session_state.pop("auth_prefill", "")

    components.section("Se connecter", "Votre dressing vous attend")
    identifier = components.text_field(
        "E-mail ou téléphone",
        f"login_id__{nonce}",
        initial=prefill,
        placeholder="📧 nom@exemple.com   ·   📱 +212 6 12 34 56 78",
    )
    password = st.text_input(
        "Mot de passe",
        key=f"login_pw__{nonce}",
        type="password",
        placeholder="Votre mot de passe",
    )

    if components.button(
        "Se connecter",
        key=f"login_go__{nonce}",
        type="primary",
        stretch=True,
        disabled=not identifier or not password,
    ):
        ok, message = auth.login(identifier, password)
        if ok:
            state.push_toast(message, "👋")
            st.rerun()
        else:
            st.error(message)

    components.html(
        f'<div class="mp-auth-hint">Compte de démonstration : <b>{DEMO_ACCOUNT["email"]}</b> · '
        f'mot de passe <b>{DEMO_ACCOUNT["password"]}</b></div>'
    )
    if components.button("🎬 Entrer dans le compte de démo", key="login_demo", stretch=True):
        auth.login_demo()
        state.push_toast("Compte de démo chargé : bonne visite !", "✨")
        st.rerun()


# ---------------------------------------------------------------------------
# Inscription
# ---------------------------------------------------------------------------
def _signup_form() -> None:
    nonce = st.session_state.get("auth_nonce", 0)

    components.section("Créer mon compte", "E-mail **ou** téléphone : au moins l'un des deux")
    name = st.text_input("Nom complet", key=f"su_name__{nonce}", placeholder="Ex. Salma El Amrani")

    columns = st.columns(2)
    with columns[0]:
        email = st.text_input("E-mail", key=f"su_email__{nonce}", placeholder="nom@exemple.com")
    with columns[1]:
        phone = st.text_input("Téléphone", key=f"su_phone__{nonce}", placeholder="+212 6 12 34 56 78")

    country = st.selectbox(
        "Pays",
        countries.NAMES,
        index=countries.index_of(DEFAULT_COUNTRY),
        format_func=countries.label_for,
        key=f"su_country__{nonce}",
    )

    columns = st.columns(2)
    with columns[0]:
        password = st.text_input("Mot de passe", key=f"su_pw__{nonce}", type="password",
                                 placeholder="4 caractères minimum")
    with columns[1]:
        confirm = st.text_input("Confirmer", key=f"su_pw2__{nonce}", type="password",
                                placeholder="Répétez le mot de passe")

    if components.button("Créer mon compte", key=f"su_go__{nonce}", type="primary", stretch=True):
        if password != confirm:
            st.error("Les deux mots de passe ne correspondent pas.")
        else:
            ok, message = auth.signup(
                name=name, email=email, phone=phone, password=password, country=country,
            )
            if ok:
                state.push_toast(message, "🎉")
                st.rerun()
            else:
                st.error(message)

    components.html(
        '<div class="mp-auth-hint">Votre compte est enregistré sur cet appareil : '
        "vous pourrez vous reconnecter avec votre e-mail ou votre numéro, et prêter "
        "l'application à une autre personne sans mélanger vos dressings.</div>"
    )


# ---------------------------------------------------------------------------
# Comptes déjà créés sur l'appareil
# ---------------------------------------------------------------------------
def _use_account(identifier: str) -> None:
    """Prépare la connexion à un compte de l'appareil (appliqué au run suivant)."""
    st.session_state["auth_prefill"] = identifier
    st.session_state["auth_nonce"] = st.session_state.get("auth_nonce", 0) + 1
    st.session_state["auth_wanted_mode"] = "Se connecter"
    st.rerun()


def _apply_pending_switch() -> None:
    """Bascule l'onglet demandé au run précédent (avant création du sélecteur)."""
    wanted = st.session_state.pop("auth_wanted_mode", None)
    if wanted in MODES:
        st.session_state["auth_mode"] = wanted


def _device_accounts() -> None:
    accounts = auth.accounts()
    if not accounts:
        return
    last = auth.last_user_id()
    components.section("Comptes sur cet appareil", f"{len(accounts)} compte(s) enregistré(s)")

    for account in accounts[:6]:
        flags = []
        if account.get("demo"):
            flags.append("démo")
        if account.get("id") == last:
            flags.append("dernier utilisé")
        suffix = f" · {' · '.join(flags)}" if flags else ""
        with st.container(key=f"tile_acct_{account['id']}"):
            left, right = st.columns([2.3, 1], vertical_alignment="center")
            with left:
                components.html(
                    '<div class="mp-account-row">'
                    f'<span class="mp-account-avatar">{account.get("avatar", "🌸")}</span>'
                    f'<span class="mp-account-txt"><b>{account.get("name", "")}</b>'
                    f'<small>{countries.label_for(account.get("country"))} · '
                    f'{account.get("identifier", "")}{suffix}</small></span></div>'
                )
            with right:
                if components.button("Utiliser", key=f"use_acct__{account['id']}", stretch=True):
                    _use_account(str(account.get("identifier", "")))

    components.html(
        '<div class="mp-muted" style="margin:.1rem .15rem .3rem">'
        "Le mot de passe du compte choisi est demandé à la connexion. "
        "Pour une nouvelle personne, utilisez « Créer un compte ».</div>"
    )


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
def render() -> None:
    _apply_pending_switch()
    _header()
    mode = components.segmented(MODES, "auth_mode", "Se connecter")
    if mode == "Créer un compte":
        _signup_form()
    else:
        _login_form()
    _device_accounts()
    components.html(
        '<div class="mp-auth-foot">Muse · démo locale — les comptes sont enregistrés dans '
        '<code>data/user_store.json</code> sur cet appareil.</div>'
    )
