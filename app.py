"""Muse — application de mode inspirée de Pinterest.

Point d'entrée Streamlit : ``streamlit run app.py``

Comptes : chaque personne se connecte (ou crée son compte) avec un e-mail ou un
numéro de téléphone. Trois pages accessibles ensuite depuis la barre de
navigation basse :

    🏠 Accueil  — feed visuel, catégories, recommandations, collections
    🔍 Explorer — style, stylistes, marques, looks, recherche de pièces
    👤 Mon compte — dressing, wishlist, looks, récompenses, rendez-vous
"""
from __future__ import annotations

import streamlit as st

from core import auth, router, state
from core.config import APP_ICON, APP_NAME, APP_TAGLINE
from core.theme import inject_theme
from data import seed
from views import auth as auth_view

st.set_page_config(
    page_title=f"{APP_NAME} · {APP_TAGLINE}",
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 1. Feuille de style de l'application (design system complet)
inject_theme()

# 2. Comptes : fichier data/user_store.json (compte de démo créé au 1er lancement)
auth.bootstrap(seed.default_store())

if not auth.current_user():
    # 3a. Personne n'est connecté → écran de connexion / création de compte
    auth_view.render()
else:
    # 3b. Espace du compte connecté + rendu de la page active
    state.init_state(seed.default_store() if auth.is_demo() else None)
    router.render()
