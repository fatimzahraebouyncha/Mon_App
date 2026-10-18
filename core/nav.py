"""Navigation principale : barre inférieure fixe (mobile-first)."""
from __future__ import annotations

import streamlit as st

PAGES: list[dict[str, str]] = [
    {"key": "home", "label": "Accueil", "icon": "🏠"},
    {"key": "explore", "label": "Explorer", "icon": "🔍"},
    {"key": "account", "label": "Mon compte", "icon": "👤"},
]

PAGE_KEYS = [page["key"] for page in PAGES]


def current_page() -> str:
    """Page active : le query param ``?page=`` amorce, la session fait foi."""
    value = st.query_params.get("page", "")
    if isinstance(value, list):
        value = value[0] if value else ""
    param = str(value or "").strip().lower()
    stored = st.session_state.get("_page")

    if param in PAGE_KEYS and param != stored:
        st.session_state["_page"] = param
        return param
    if stored in PAGE_KEYS:
        return stored
    return param if param in PAGE_KEYS else "home"


def goto(page: str, **state_updates) -> None:
    """Change de page (et met éventuellement à jour des filtres de session)."""
    for key, value in state_updates.items():
        st.session_state[key] = value
    st.session_state["_page"] = page
    if st.query_params.get("page") != page:
        st.query_params["page"] = page
    st.rerun()


def bottom_nav(active: str) -> None:
    """Barre de navigation fixe en bas de l'écran (3 pages)."""
    with st.container(key="bottom_nav"):
        columns = st.columns(len(PAGES), gap="small")
        for column, page in zip(columns, PAGES):
            with column:
                clicked = st.button(
                    page["label"],
                    key=f"nav__{page['key']}",
                    type="primary" if page["key"] == active else "secondary",
                    help=page["label"],
                )
                if clicked and page["key"] != active:
                    goto(page["key"])


def page_transition() -> None:
    """Petite animation d'entrée, uniquement lors d'un changement de page."""
    page = current_page()
    if st.session_state.get("_last_page") != page:
        st.session_state["_last_page"] = page
        st.markdown(
            "<style>[data-testid='stMainBlockContainer']{animation:mpIn .45s cubic-bezier(.2,.7,.3,1)}</style>",
            unsafe_allow_html=True,
        )
