"""Explorer 🔍 — style, stylistes, marques, looks et recherche de pièces."""
from __future__ import annotations

import datetime as _dt

import streamlit as st

from core import components, images, nav, state
from core.config import format_price
from data import catalogue
from views import common

TABS = ["Style", "Stylistes", "Marques", "Looks", "Pièces"]

POPULAR_SEARCHES = [
    "Hijab en jersey", "Abaya brodée", "Kaftan de cérémonie",
    "Robe longue fluide", "Sac en cuir", "Baskets blanches", "Manteau en laine",
]


# ---------------------------------------------------------------------------
# Barre de recherche
# ---------------------------------------------------------------------------
def _apply_pending_tab() -> None:
    """Applique une bascule d'onglet demandée au run précédent (avant le sélecteur)."""
    wanted = st.session_state.pop("explore_wanted_tab", None)
    if wanted in TABS:
        st.session_state["explore_tab"] = wanted


def _go(tab: str) -> None:
    """Demande l'affichage d'un autre onglet d'Explorer."""
    st.session_state["explore_wanted_tab"] = tab
    st.rerun()


def _search() -> None:
    query = components.text_field(
        "Rechercher",
        "search_explore",
        initial=st.session_state.get("search", ""),
        placeholder="🔍  Une pièce, une marque, une matière…",
    )
    st.session_state["search"] = query

    if not query:
        def suggestion(word: str) -> None:
            st.session_state["search"] = word
            _go("Pièces")

        components.chips(
            [{"key": word, "label": word, "icon": "🔎"} for word in POPULAR_SEARCHES[:4]],
            "",
            "suggest",
            suggestion,
        )


# ---------------------------------------------------------------------------
# Onglet « Style » (test + profil)
# ---------------------------------------------------------------------------
def _quiz() -> None:
    nonce = st.session_state.get("quiz_nonce", 0)
    components.section("Trouver mon style", "4 questions · 30 secondes")

    answers: dict[str, str] = {}
    for question in catalogue.STYLE_QUIZ:
        options = [option["label"] for option in question["options"]]
        answers[question["id"]] = st.radio(
            f"{question['icon']}  {question['question']}",
            options,
            index=None,
            key=f"quiz__{question['id']}__{nonce}",
        )

    answered = sum(1 for value in answers.values() if value)
    st.progress(answered / len(catalogue.STYLE_QUIZ), text=f"{answered}/{len(catalogue.STYLE_QUIZ)} réponses")

    if components.button("Découvrir mon style", key="quiz_submit", type="primary", stretch=True,
                         disabled=answered < len(catalogue.STYLE_QUIZ)):
        _save_profile(answers)


def _save_profile(answers: dict[str, str]) -> None:
    tags: list[str] = []
    budget: float | None = None
    for question in catalogue.STYLE_QUIZ:
        chosen = answers.get(question["id"])
        option = next((opt for opt in question["options"] if opt["label"] == chosen), None)
        if not option:
            continue
        tags.extend(option.get("tags", []))
        if option.get("budget"):
            budget = float(option["budget"])

    best, best_score = catalogue.STYLE_RESULTS[0], -1
    for result in catalogue.STYLE_RESULTS:
        score = len(set(tags) & set(result["tags"]))
        if score > best_score:
            best, best_score = result, score

    st.session_state["style_profile"] = {
        "id": best["id"],
        "name": best["name"],
        "icon": best["icon"],
        "description": best["description"],
        "palette": best["palette"],
        "tips": best["tips"],
        "tags": tags,
        "budget": budget,
        "answers": answers,
        "created": _dt.date.today().isoformat(),
    }
    if "ch_quiz" not in st.session_state.get("challenges", {}):
        state.add_points(50)
        state.push_toast("Test terminé : +50 points de fidélité", "🧠")
    state.save_state()
    st.rerun()


def _style_profile_view() -> None:
    profile = st.session_state.get("style_profile") or {}
    components.section("Mon style", f"Défini le {profile.get('created', '—')}")
    tips = "".join(f"<li>{tip}</li>" for tip in profile.get("tips", []))
    components.html(
        f'<div class="mp-panel">'
        f'<div class="mp-eyebrow">Votre profil</div>'
        f'<h4 style="font-size:1.18rem;margin:.3rem 0 .35rem">{profile.get("icon", "✨")} {profile.get("name", "")}</h4>'
        f'<p>{profile.get("description", "")}</p>'
        f'<ul style="margin:.6rem 0 0;padding-left:1.05rem;font-size:.78rem;color:var(--ink-2)">{tips}</ul>'
        f"</div>"
    )
    components.swatches(profile.get("palette", []))

    tags, budget = common.taste()
    components.section("Pièces qui vous ressemblent",
                       f"Budget indicatif : {format_price(budget)}" if budget else None)
    picks = catalogue.recommend(tags, limit=4, budget=budget)
    columns = st.columns(2, gap="small")
    for index, item in enumerate(picks):
        with columns[index % 2]:
            components.product_card(item, prefix=f"style{index}")

    left, right = st.columns(2)
    with left:
        if components.button("Refaire le test", key="quiz_restart", stretch=True):
            st.session_state["style_profile"] = {}
            st.session_state["quiz_nonce"] = st.session_state.get("quiz_nonce", 0) + 1
            state.save_state()
            st.rerun()
    with right:
        if components.button("Voir mon feed", key="quiz_to_feed", type="primary", stretch=True):
            nav.goto("home")


def _style_tab() -> None:
    if st.session_state.get("style_profile"):
        _style_profile_view()
    else:
        _quiz()
        components.panel(
            "Comment ça marche",
            "Vos réponses définissent une palette, des matières et un budget. Le feed, les recommandations "
            "et les stylistes proposés s'ajustent ensuite automatiquement.",
            tone="tint",
        )


# ---------------------------------------------------------------------------
# Onglet « Stylistes »
# ---------------------------------------------------------------------------
def _stylists_tab() -> None:
    components.section("Stylistes", "Séance en visio (partout dans le monde) ou en boutique")
    active = st.session_state.get("booking_stylist")

    for person in catalogue.STYLISTS:
        with st.container(key=f"stylist_{person['id']}"):
            photo_col, info_col = st.columns([1, 2.6], vertical_alignment="center")
            with photo_col:
                with st.container(key=f"round_stylist_{person['id']}"):
                    components.image(images.square(person["photo"], person["id"], size=220))
            with info_col:
                components.html(
                    f'<p class="mp-card-title" style="font-size:.94rem">{person["name"]}</p>'
                    f'<p class="mp-card-sub">⭐ {person["rating"]} · {person["reviews"]} avis · {person["city"]}</p>'
                    f'<p class="mp-card-sub">{person["specialty"]} · <b>{format_price(person["price"])}</b>/séance</p>'
                    f'<p class="mp-card-sub">{components.tags(person["tags"][:3])}</p>'
                )
            components.html(f'<div class="mp-muted" style="margin:.1rem .15rem .3rem">« {person["bio"]} »</div>')
            if components.button(
                "Réserver" if active != person["id"] else "Fermer les créneaux",
                key=f"book__{person['id']}",
                type="primary" if active != person["id"] else "secondary",
                stretch=True,
            ):
                st.session_state["booking_stylist"] = None if active == person["id"] else person["id"]
                st.rerun()

        if active == person["id"]:
            _booking_form(person)


def _booking_form(person: dict) -> None:
    slots = catalogue.upcoming_slots(person["id"])
    with st.container(key=f"booking_panel_{person['id']}"):
        components.html(
            f'<div class="mp-panel tint"><h4>📅 Réserver avec {person["name"].split()[0]}</h4>'
            f'<p>Choisissez un créneau, un format et le motif de la séance.</p></div>'
        )
        labels = {slot["key"]: slot["label"] for slot in slots}
        chosen = st.radio(
            "Créneaux disponibles",
            [slot["key"] for slot in slots],
            format_func=lambda key: labels.get(key, key),
            key=f"slot__{person['id']}",
        )
        mode = st.selectbox("Format", catalogue.APPOINTMENT_MODES, key=f"mode__{person['id']}")
        topic = st.selectbox("Motif", catalogue.APPOINTMENT_TOPICS, key=f"topic__{person['id']}")
        note = st.text_area("Note pour la styliste (optionnel)", key=f"note__{person['id']}", height=70)

        if components.button("Confirmer le rendez-vous", key=f"confirm__{person['id']}", type="primary", stretch=True):
            slot = next((item for item in slots if item["key"] == chosen), slots[0])
            created = state.add_entry("appointments", {
                "id": f"ap_{person['id']}_{slot['date']}_{slot['hour']}".replace(":", ""),
                "stylist_id": person["id"],
                "stylist_name": person["name"],
                "date": slot["date"],
                "slot": slot["hour"],
                "mode": mode,
                "topic": topic,
                "note": note,
                "status": "À venir",
                "created": _dt.date.today().isoformat(),
            })
            if created:
                state.add_points(40)
                state.push_toast(f"Rendez-vous confirmé avec {person['name']} (+40 pts)", "📅")
            else:
                state.push_toast("Ce créneau est déjà dans vos rendez-vous", "📅")
            st.session_state["booking_stylist"] = None
            st.rerun()


# ---------------------------------------------------------------------------
# Onglet « Marques »
# ---------------------------------------------------------------------------
def _brand_tab_view(brand: dict) -> None:
    followed = brand["id"] in state.bucket("followed_brands")
    with st.container(key=f"tile_brand_{brand['id']}"):
        components.image(images.square(brand["photo"], f"br_{brand['id']}", size=360))
        components.html(
            f'<div class="mp-card-body">'
            f'<p class="mp-card-title">{brand["name"]} {"" if not brand.get("is_new") else "· 🆕"}</p>'
            f'<p class="mp-card-sub">{brand["style"]} · {brand["city"]}</p>'
            f'<p class="mp-card-sub">{brand["price_range"]} · {brand["pieces"]} pièces · '
            f'{brand["followers"] / 1000:.0f}k abonnés</p>'
            f'<p class="mp-card-sub" style="margin-top:.3rem">{components.tags(brand["tags"][:2])}</p>'
            f'<p class="mp-card-sub" style="margin-top:.2rem">{catalogue.BRAND_SHIPPING}</p>'
            f"</div>"
        )
        left, right = st.columns([1, 1.3])
        with left:
            if components.button("Suivi" if followed else "Suivre", key=f"follow__{brand['id']}",
                                 type="secondary" if followed else "primary", stretch=True):
                now_followed = state.toggle("followed_brands", brand["id"])
                state.push_toast(
                    f"Vous suivez {brand['name']}" if now_followed else f"{brand['name']} retirée de vos suivis",
                    "💫",
                )
                st.rerun()
        with right:
            if components.button("Voir les pièces", key=f"browse__{brand['id']}", stretch=True):
                st.session_state["search"] = brand["name"]
                _go("Pièces")


def _brands_tab() -> None:
    components.section("Marques", f"{len(catalogue.BRANDS)} maisons à découvrir")
    components.masonry(catalogue.BRANDS, _brand_tab_view, columns=2)


# ---------------------------------------------------------------------------
# Onglet « Looks »
# ---------------------------------------------------------------------------
def _look_builder() -> None:
    components.section("Créer un look", "Composez, nommez, enregistrez")
    nonce = st.session_state.get("look_nonce", 0)

    columns = st.columns(2, gap="small")
    for index, slot in enumerate(catalogue.LOOK_SLOTS):
        options = common.options_for_slot(slot)
        keys = ["—"] + [item["id"] for item in options]
        labels = {item["id"]: item["title"] for item in options}
        with columns[index % 2]:
            st.selectbox(
                f"{slot['icon']} {slot['label']}",
                keys,
                format_func=lambda key, labels=labels: labels.get(key, "—"),
                key=f"build__{slot['key']}__{nonce}",
            )

    name = st.text_input("Nom du look", key=f"build_name__{nonce}", placeholder="Ex. Bureau du lundi")
    occasion = st.selectbox("Occasion", catalogue.LOOK_OCCASIONS, key=f"build_occ__{nonce}")

    chosen = {slot["key"]: st.session_state.get(f"build__{slot['key']}__{nonce}", "—") for slot in catalogue.LOOK_SLOTS}
    pieces = catalogue.items_from([value for value in chosen.values() if value and value != "—"])
    if pieces:
        components.section("Aperçu", f"{len(pieces)} pièce{'s' if len(pieces) > 1 else ''}")
        preview_columns = st.columns(len(pieces), gap="small")
        for column, item in zip(preview_columns, pieces):
            with column:
                components.image(images.for_item(item, width=200))

    left, right = st.columns([1.2, 1])
    with left:
        if components.button("Enregistrer le look", key=f"build_save__{nonce}", type="primary", stretch=True,
                             disabled=not pieces):
            look = {
                "id": f"lk_{_dt.datetime.now().strftime('%H%M%S')}",
                "name": name.strip() or f"Look {occasion.lower()}",
                "occasion": occasion,
                "created": _dt.date.today().isoformat(),
                "public": False,
                "likes": 0,
                "note": "",
                "slots": {key: ("" if value == "—" else value) for key, value in chosen.items()},
            }
            state.add_entry("looks", look)
            state.add_points(15)
            state.push_toast(f"Look « {look['name']} » enregistré (+15 pts)", "📸")
            st.session_state["look_nonce"] = nonce + 1
            st.rerun()
    with right:
        if components.button("Vider", key=f"build_clear__{nonce}", stretch=True):
            st.session_state["look_nonce"] = nonce + 1
            st.rerun()


def _community_looks() -> None:
    components.section("Looks de la communauté", "Inspirez-vous, copiez, adaptez")

    def tile(look: dict) -> None:
        cover = catalogue.get_item(look["slots"].get("haut")) or catalogue.get_item(next(iter(look["slots"].values())))
        with st.container(key=f"tile_clook_{look['id']}"):
            if cover:
                components.image(images.for_item(cover, width=420))
            components.html(
                f'<div class="mp-card-body"><p class="mp-card-title">{look["name"]}</p>'
                f'<p class="mp-card-sub">{look["author"]} · {look["city"]}</p>'
                f'<p class="mp-card-sub">❤️ {look["likes"]} · {components.tags([look["occasion"]], "gold")}</p></div>'
            )
            if components.button("Copier ce look", key=f"clone__{look['id']}", stretch=True):
                state.add_entry("looks", {
                    "id": f"lk_{look['id']}",
                    "name": f"{look['name']} (inspiré)",
                    "occasion": look["occasion"],
                    "created": _dt.date.today().isoformat(),
                    "public": False,
                    "likes": 0,
                    "note": f"D'après {look['author']}",
                    "slots": dict(look["slots"]),
                })
                state.push_toast("Look copié dans vos créations", "🪄")
                st.rerun()

    components.hscroll("community", catalogue.COMMUNITY_LOOKS, tile)


def _looks_tab() -> None:
    _look_builder()
    _community_looks()
    common.looks_gallery()


# ---------------------------------------------------------------------------
# Onglet « Pièces »
# ---------------------------------------------------------------------------
def _pieces_tab() -> None:
    query = st.session_state.get("search", "")
    filters = st.columns([1.2, 1.4])
    with filters[0]:
        category = st.selectbox(
            "Catégorie",
            ["tout"] + [item["key"] for item in catalogue.CATEGORIES if item["key"] != "tout"],
            format_func=lambda key: catalogue.CATEGORY_LABELS.get(key, "Tout"),
            key="explore_category",
        )
    with filters[1]:
        sort = st.selectbox("Trier par", ["Pertinence", "Nouveautés", "Prix croissant", "Les plus aimées"],
                            key="explore_sort")
    budget = st.slider("Budget maximum", 200, 5000, 5000, step=100, key="explore_budget",
                       format="%d MAD")

    items = catalogue.search(query, catalogue.by_category(category))
    items = [item for item in items if float(item.get("price") or 0) <= budget]
    if sort == "Nouveautés":
        items = [item for item in items if item.get("is_new")] + [item for item in items if not item.get("is_new")]
    elif sort == "Prix croissant":
        items = sorted(items, key=lambda item: item.get("price") or 0)
    elif sort == "Les plus aimées":
        items = sorted(items, key=lambda item: item.get("likes", 0), reverse=True)

    label = catalogue.CATEGORY_LABELS.get(category, "Tout")
    detail = f"{len(items)} résultats · {label}"
    if query:
        detail += f" · « {query} »"
    components.section("Pièces", detail)

    if not items:
        components.empty("🔍", "Rien à afficher avec ces filtres. Élargissez le budget ou changez de catégorie.")
        return
    components.masonry(items[:24], lambda item: components.product_card(item, "explore"))


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
def render() -> None:
    _apply_pending_tab()
    common.title_block("Explorer", "Votre style, vos stylistes, vos marques")
    _search()
    tab = components.segmented(TABS, "explore_tab", "Style")
    if tab == "Stylistes":
        _stylists_tab()
    elif tab == "Marques":
        _brands_tab()
    elif tab == "Looks":
        _looks_tab()
    elif tab == "Pièces":
        _pieces_tab()
    else:
        _style_tab()
