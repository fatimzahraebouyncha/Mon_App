"""Accueil 🏠 — feed visuel, catégories, recommandations, nouvelles collections."""
from __future__ import annotations

import streamlit as st

from core import components, images, nav, state
from core.config import APP_TAGLINE, FEED_PAGE_SIZE
from data import catalogue
from views import common


# ---------------------------------------------------------------------------
# Barre supérieure
# ---------------------------------------------------------------------------
def _top_bar() -> None:
    profile = st.session_state.get("profile") or {}
    with st.container(key="topbar"):
        left, middle, right = st.columns([3.4, 1, 1], vertical_alignment="center")
        with left:
            components.html(
                f'<div class="mp-logo">Muse<em>.</em></div>'
                f'<div class="mp-muted" style="margin-top:-2px">{APP_TAGLINE}</div>'
            )
        with middle:
            if components.button("🔔", key="topbar_bell", help="Notifications"):
                state.push_toast("3 nouvelles pièces chez vos marques suivies", "💎")
                state.push_toast("Rappel : rendez-vous styliste dans 3 jours", "📅")
                state.push_toast("Votre avantage -10 % expire bientôt", "🎁")
        with right:
            if components.button(profile.get("avatar", "🦋"), key="topbar_avatar", help="Mon compte"):
                nav.goto("account")


def _search_bar() -> None:
    query = components.text_field(
        "Rechercher",
        "search_home",
        initial=st.session_state.get("search", ""),
        placeholder="🔍  Robe de soirée, sac en cuir, styliste…",
    )
    st.session_state["search"] = query


def _chips() -> None:
    def select(category: str) -> None:
        st.session_state["feed_category"] = category
        st.rerun()

    components.chips(
        catalogue.CATEGORIES,
        st.session_state.get("feed_category", "tout"),
        "feed",
        select,
    )


# ---------------------------------------------------------------------------
# Sections éditoriales
# ---------------------------------------------------------------------------
def _spotlight() -> None:
    featured = catalogue.COLLECTIONS[0]
    components.hero(
        "Nouvelle collection",
        f"{featured['name']} · {featured['brand']}",
        featured["tagline"],
        photo=images.banner(catalogue.MODEST_PHOTOS["hero_modeste"], seed="hero_modeste"),
    )
    left, right = st.columns([1.5, 1])
    with left:
        if components.button("Découvrir la collection", key="hero_cta", type="primary", stretch=True):
            st.session_state["feed_category"] = featured["tags"][0]
            state.push_toast(f"Collection « {featured['name']} » dans votre feed", "🧵")
            st.rerun()
    with right:
        if components.button("Voir les tendances", key="hero_more", stretch=True):
            st.session_state["feed_category"] = "tout"
            st.session_state["search"] = ""
            st.rerun()


def _for_you() -> None:
    profile = st.session_state.get("style_profile") or {}
    tags, budget = common.taste()
    subtitle = f"Style {profile['name']}" if profile else "D'après vos inspirations enregistrées"
    components.section("Pour vous", subtitle)

    if not profile:
        components.html(
            '<div class="mp-panel tint"><h4>🎯 Affinez vos recommandations</h4>'
            "<p>4 questions suffisent : votre feed, vos pièces et vos stylistes s'adaptent ensuite à votre style.</p></div>"
        )
        if components.button("Faire le test de style · 30 s", key="cta_quiz_home", type="primary", stretch=True):
            nav.goto("explore", explore_tab="Style")

    picks = catalogue.recommend(tags, limit=4, budget=budget)
    columns = st.columns(2, gap="small")
    for index, item in enumerate(picks):
        with columns[index % 2]:
            components.product_card(item, prefix=f"you{index}")


def _collections() -> None:
    components.section("Nouvelles collections", "Repérées pour vous cette semaine", more="Défilez →")

    def tile(collection: dict) -> None:
        with st.container(key=f"tile_col_{collection['id']}"):
            components.image(images.photo(collection["photo"], collection["id"], width=420, ratio=0.9))
            components.html(
                f'<div class="mp-card-body">'
                f'<p class="mp-card-title">{collection["name"]}</p>'
                f'<p class="mp-card-sub">{collection["brand"]} · {collection["pieces"]} pièces</p>'
                f'<p class="mp-card-sub">{collection["tagline"]}</p></div>'
            )
            if components.button("Voir la collection", key=f"col__{collection['id']}", stretch=True):
                st.session_state["feed_category"] = collection["tags"][0]
                st.session_state["search"] = ""
                state.push_toast(f"Collection « {collection['name']} » affichée", "🧵")
                st.rerun()

    components.hscroll("collections", catalogue.COLLECTIONS, tile)


def _feed() -> None:
    category = st.session_state.get("feed_category", "tout")
    query = st.session_state.get("search", "")
    signature = common.signature_of(category, query)
    if st.session_state.get("_feed_signature") != signature:
        st.session_state["_feed_signature"] = signature
        st.session_state["feed_limit"] = FEED_PAGE_SIZE

    items = catalogue.search(query, catalogue.by_category(category))
    label = catalogue.CATEGORY_LABELS.get(category, "Tout")
    detail = f"{len(items)} pièces · {label}"
    if query:
        detail += f" · « {query} »"
    components.section("Inspirations", detail)

    if not items:
        components.empty("🔍", "Aucune pièce ne correspond à cette recherche. Essayez un autre mot-clé.")
        return

    limit = int(st.session_state.get("feed_limit", FEED_PAGE_SIZE))
    components.masonry(items[:limit], lambda item: components.product_card(item, "feed"))

    remaining = len(items) - limit
    if remaining > 0:
        if components.button(f"Afficher plus ({remaining})", key="feed_more", stretch=True):
            st.session_state["feed_limit"] = limit + FEED_PAGE_SIZE
            st.rerun()


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
def render() -> None:
    _top_bar()
    _search_bar()
    _chips()
    _spotlight()
    _for_you()
    _collections()
    _feed()
