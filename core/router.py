"""Routeur : rend la page active puis la barre de navigation."""
from __future__ import annotations

from core import nav, state
from views import account, explore, home

VIEWS = {
    "home": home.render,
    "explore": explore.render,
    "account": account.render,
}


def render() -> None:
    page = nav.current_page()
    nav.page_transition()
    VIEWS[page]()
    nav.bottom_nav(page)
    state.flush_toasts()
