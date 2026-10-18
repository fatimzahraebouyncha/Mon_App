"""Mon compte 👤 — garde-robe, wishlist, looks, récompenses et rendez-vous."""
from __future__ import annotations

import datetime as _dt

import streamlit as st

from core import auth, components, images, nav, state
from core.config import format_price
from data import catalogue, countries, seed
from views import common

TABS = ["Dressing", "Wishlist", "Looks", "Récompenses", "RDV"]
SEASONS = ["Toutes saisons", "Printemps", "Été", "Automne", "Hiver"]
PRIORITIES = ["haute", "moyenne", "basse"]
INTENTS = ["acheter", "offrir"]


# ---------------------------------------------------------------------------
# En-tête de profil
# ---------------------------------------------------------------------------
def _profile_header() -> None:
    profile = st.session_state.get("profile") or {}
    account = auth.current_user() or {}
    pieces, value, top_category = common.wardrobe_stats()
    contact = " · ".join(part for part in (account.get("email"), account.get("phone")) if part) or "Compte local"
    components.html(
        f'<div class="mp-panel" style="display:flex;gap:.85rem;align-items:center">'
        f'<div class="mp-avatar" style="width:56px;height:56px;font-size:1.5rem">{profile.get("avatar", "🦋")}</div>'
        f'<div style="min-width:0">'
        f'<p class="mp-card-title" style="font-size:1rem">{profile.get("name", "Moi")}</p>'
        f'<p class="mp-card-sub">{profile.get("handle", "@moi")} · {countries.label_for(profile.get("city"))}</p>'
        f'<p class="mp-card-sub">{contact}</p>'
        f'<p class="mp-card-sub">{profile.get("member_since", "")}</p>'
        f"</div></div>"
    )
    components.stat_row([
        (str(pieces), "pièces"),
        (str(len(state.bucket("looks"))), "looks"),
        (str(len(state.bucket("saved"))), "favoris"),
        (f'{int(st.session_state.get("points", 0))}', "points"),
    ])

    left, right = st.columns(2)
    with left:
        if components.button("🔐 Changer de compte", key="acct_switch", stretch=True):
            auth.logout()
            state.push_toast("Choisissez un compte pour continuer", "🔐")
            st.rerun()
    with right:
        if components.button("👋 Se déconnecter", key="acct_logout", stretch=True):
            auth.logout()
            state.push_toast("À bientôt !", "👋")
            st.rerun()

    with st.expander("✏️ Modifier mon profil"):
        columns = st.columns([2, 1])
        with columns[0]:
            name = st.text_input("Nom", value=profile.get("name", ""), key="pf_name")
            country = st.selectbox(
                "Pays",
                countries.NAMES,
                index=countries.index_of(profile.get("city") or account.get("country")),
                format_func=countries.label_for,
                key="pf_country",
            )
            bio = st.text_input("Bio", value=profile.get("bio", ""), key="pf_bio")
        with columns[1]:
            avatar = st.text_input("Emoji", value=profile.get("avatar", "🦋"), key="pf_avatar")
        left, right = st.columns(2)
        with left:
            if components.button("Enregistrer", key="pf_save", type="primary", stretch=True):
                st.session_state["profile"] = {
                    **profile, "name": name, "city": country, "bio": bio, "avatar": avatar,
                }
                auth.update_account(auth.user_id(), name=name, country=country)
                state.save_state()
                state.push_toast("Profil mis à jour", "✨")
        with right:
            if components.button("Exemple de démo", key="pf_demo_data", stretch=True):
                state.reset_state(seed.default_store())
                state.push_toast("Données de démonstration chargées", "🎬")
                st.rerun()

        components.html(
            '<div class="mp-auth-hint">Ce compte garde son dressing, sa wishlist et ses looks : '
            "une autre personne peut utiliser l'application sur le même appareil sans rien mélanger. "
            "Utilisez « Changer de compte » pour passer à un autre profil.</div>"
        )
        if components.button("Vider mes données", key="pf_clear", stretch=True):
            state.reset_state()
            state.push_toast("Votre espace a été vidé", "🧹")
            st.rerun()


# ---------------------------------------------------------------------------
# Onglet « Dressing »
# ---------------------------------------------------------------------------
def _add_piece_form() -> None:
    with st.expander("➕ Ajouter une pièce à mon dressing"):
        columns = st.columns([2, 1])
        with columns[0]:
            title = st.text_input("Nom de la pièce", key="np_title", placeholder="Ex. Blazer en laine")
            brand = st.text_input("Marque", key="np_brand", placeholder="Ex. Maison Lior")
        with columns[1]:
            category = st.selectbox(
                "Catégorie",
                [item["key"] for item in catalogue.CATEGORIES if item["key"] != "tout"],
                format_func=lambda key: catalogue.CATEGORY_LABELS.get(key, key),
                key="np_category",
            )
            price = st.number_input("Prix (MAD)", min_value=0, max_value=30000, value=800, step=50, key="np_price")

        columns = st.columns(3)
        with columns[0]:
            color = st.text_input("Couleur", key="np_color", placeholder="Noir")
        with columns[1]:
            season = st.selectbox("Saison", SEASONS, key="np_season")
        with columns[2]:
            favorite = st.checkbox("Coup de cœur", key="np_fav")

        if components.button("Ajouter au dressing", key="np_save", type="primary", stretch=True, disabled=not title):
            state.add_entry("wardrobe", {
                "id": f"wd_{_dt.datetime.now().strftime('%H%M%S%f')[:12]}",
                "item_id": "",
                "title": title,
                "brand": brand,
                "category": category,
                "photo": None,
                "ratio": 0.82,
                "tags": [],
                "color": color,
                "season": season,
                "favorite": favorite,
                "wears": 0,
                "added": _dt.date.today().isoformat(),
                "source": "Ajout manuel",
                "price": float(price),
            })
            state.add_points(20)
            state.push_toast("Pièce ajoutée à votre dressing (+20 pts)", "👗")
            st.rerun()


def _dressing_tab() -> None:
    pieces, value, top_category = common.wardrobe_stats()
    components.stat_row([
        (str(pieces), "pièces"),
        (format_price(value), "valeur estimée"),
        (format_price(value / pieces) if pieces else "—", "prix moyen"),
        (top_category, "dominante"),
    ])
    _add_piece_form()

    entries = common.wardrobe_entries()
    if not entries:
        components.empty("🚪", "Votre dressing est vide : ajoutez une première pièce ou piochez dans le feed.")
        return

    categories = sorted({entry.get("category", "vetements") for entry in entries})
    filters = st.columns([1.6, 1])
    with filters[0]:
        category = st.selectbox(
            "Filtrer",
            ["toutes"] + categories,
            format_func=lambda key: "Toutes les catégories" if key == "toutes" else catalogue.CATEGORY_LABELS.get(key, key),
            key="wd_filter",
        )
    with filters[1]:
        sort = st.selectbox("Trier", ["Récentes", "Favorites", "Les plus portées"], key="wd_sort")

    selected = [entry for entry in entries if category == "toutes" or entry.get("category") == category]
    if sort == "Favorites":
        selected = [entry for entry in selected if entry.get("favorite")]
    elif sort == "Les plus portées":
        selected = sorted(selected, key=lambda entry: entry.get("wears", 0), reverse=True)

    components.section("Ma garde-robe digitale", f"{len(selected)} pièce{'s' if len(selected) > 1 else ''}")

    def actions(entry: dict):
        def toggle_favorite() -> None:
            state.update_entry("wardrobe", entry["id"], favorite=not entry.get("favorite"))
            state.push_toast(
                "Ajouté à vos coups de cœur" if not entry.get("favorite") else "Retiré de vos coups de cœur",
                "🧡",
            )

        def wear() -> None:
            state.update_entry("wardrobe", entry["id"], wears=int(entry.get("wears", 0)) + 1)
            state.push_toast(f"« {entry['title']} » portée une fois de plus", "👌")

        def remove() -> None:
            state.remove_entry("wardrobe", entry["id"])
            state.push_toast("Pièce retirée du dressing", "🗑️")

        return [
            ("🧡" if entry.get("favorite") else "🤍", "Coups de cœur", toggle_favorite),
            ("👌", "Marquer comme portée", wear),
            ("🗑️", "Retirer", remove),
        ]

    components.masonry(
        selected,
        lambda entry: components.product_card(common.as_catalogue_item(entry), "wd", actions=actions(entry)),
        columns=2,
    )


# ---------------------------------------------------------------------------
# Onglet « Wishlist »
# ---------------------------------------------------------------------------
def _add_wish_form() -> None:
    with st.expander("➕ Ajouter une envie"):
        left, right = st.columns([2, 1])
        with left:
            title = st.text_input("Article", key="wl_title", placeholder="Ex. Manteau en laine")
            brand = st.text_input("Marque / boutique", key="wl_brand", placeholder="Maison Lior")
        with right:
            price = st.number_input("Prix (MAD)", min_value=0, max_value=30000, value=1200, step=50, key="wl_price")
            intent = st.selectbox("Pour", INTENTS, format_func=str.capitalize, key="wl_intent")
        columns = st.columns([1.2, 1, 1])
        with columns[0]:
            category = st.selectbox(
                "Catégorie",
                [item["key"] for item in catalogue.CATEGORIES if item["key"] != "tout"],
                format_func=lambda key: catalogue.CATEGORY_LABELS.get(key, key),
                key="wl_category",
            )
        with columns[1]:
            priority = st.selectbox("Priorité", PRIORITIES, format_func=str.capitalize, key="wl_priority")
        with columns[2]:
            note = st.text_input("Note", key="wl_note", placeholder="Pour qui ?")

        if components.button("Ajouter à la wishlist", key="wl_save", type="primary", stretch=True, disabled=not title):
            state.add_entry("wishlist", {
                "id": f"wl_{_dt.datetime.now().strftime('%H%M%S%f')[:12]}",
                "title": title,
                "brand": brand,
                "price": float(price),
                "photo": None,
                "ratio": 0.82,
                "category": category,
                "intent": intent,
                "priority": priority,
                "note": note,
            })
            state.push_toast("Ajouté à votre wishlist", "🛍️")
            st.rerun()


def _wishlist_cards() -> None:
    entries = state.bucket("wishlist")
    if not entries:
        components.empty("🎁", "Votre wishlist est vide : enregistrez une pièce depuis le feed ou ajoutez-la ici.")
        return

    order = {"haute": 0, "moyenne": 1, "basse": 2}
    entries = sorted(entries, key=lambda entry: order.get(entry.get("priority", "moyenne"), 1))
    components.masonry(entries, _wishlist_card, columns=2)


def _wishlist_card(entry: dict) -> None:
    item = common.as_catalogue_item(entry)
    intent = entry.get("intent", "acheter")
    badge = "Acheter" if intent == "acheter" else "À offrir"
    badge_class = "accent" if intent == "offrir" else "ok"
    entry_id = entry["id"]

    with st.container(key=f"card_wl_{entry_id}"):
        components.image(images.photo(entry.get("photo"), entry_id, width=520, ratio=float(entry.get("ratio", 0.82))))
        note = f'<p class="mp-card-sub">{entry["note"]}</p>' if entry.get("note") else ""
        components.html(
            f'<div class="mp-card-body">'
            f'<p class="mp-card-title">{entry["title"]}</p>'
            f'<p class="mp-card-sub">{entry.get("brand", "")} · <span class="mp-price">{format_price(entry.get("price"))}</span></p>'
            f'<p class="mp-card-sub">{components.tags([badge, entry.get("priority", "moyenne").capitalize()], badge_class)}{note}</p>'
            f"</div>"
        )

        def toggle_intent() -> None:
            state.update_entry("wishlist", entry_id, intent="offrir" if intent == "acheter" else "acheter")
            st.rerun()

        def toggle_favorite() -> None:
            state.toggle("liked", entry.get("item_id") or entry_id)
            state.push_toast("Coup de cœur mis à jour", "❤️")

        def mark_bought() -> None:
            state.remove_entry("wishlist", entry_id)
            state.add_entry("wardrobe", {
                **{key: entry.get(key) for key in ("item_id", "title", "brand", "category", "photo", "ratio", "price")},
                "id": f"wd_{entry_id}",
                "tags": [],
                "color": "",
                "season": "Toutes saisons",
                "favorite": True,
                "wears": 0,
                "added": _dt.date.today().isoformat(),
                "source": "Wishlist",
            })
            state.add_points(30)
            state.push_toast("Pièce rangée dans votre dressing (+30 pts)", "🎉")
            st.rerun()

        def remove() -> None:
            state.remove_entry("wishlist", entry_id)
            state.push_toast("Retiré de la wishlist", "🗑️")

        columns = st.columns(4, gap="small")
        with columns[0]:
            if components.button("🎁", key=f"wl_intent__{entry_id}", help="Basculer achat / cadeau", stretch=True):
                toggle_intent()
        with columns[1]:
            if components.button("🧡", key=f"wl_fav__{entry_id}", help="Coup de cœur", stretch=True):
                toggle_favorite()
        with columns[2]:
            if components.button("✅", key=f"wl_bought__{entry_id}", help="Déjà acheté : ranger au dressing", stretch=True):
                mark_bought()
        with columns[3]:
            if components.button("🗑️", key=f"wl_del__{entry_id}", help="Retirer", stretch=True):
                remove()


def _wishlist_tab() -> None:
    total, to_buy, to_gift = common.wishlist_stats()
    components.stat_row([
        (str(total), "envies"),
        (format_price(to_buy), "à acheter"),
        (format_price(to_gift), "à offrir"),
    ])
    _add_wish_form()

    components.section("Ma wishlist", "Priorités hautes en premier")
    _wishlist_cards()

    saved_ids = state.ids("saved")
    components.section("Inspirations enregistrées", f"{len(saved_ids)} pièce{'s' if len(saved_ids) > 1 else ''}")
    saved_items = catalogue.items_from(saved_ids)
    if saved_items:
        components.masonry(saved_items, lambda item: components.product_card(item, "saved"), columns=2)
    else:
        components.empty("🔖", "Enregistrez une inspiration depuis le feed pour la retrouver ici.")

    liked_ids = state.ids("liked")
    components.section("Mes coups de cœur", f"{len(liked_ids)} pièce{'s' if len(liked_ids) > 1 else ''}")
    liked_items = catalogue.items_from(liked_ids)
    if liked_items:
        components.masonry(liked_items, lambda item: components.product_card(item, "liked"), columns=2)
    else:
        components.empty("❤️", "Touchez le cœur d'une pièce pour la garder de côté.")


# ---------------------------------------------------------------------------
# Onglet « Looks »
# ---------------------------------------------------------------------------
def _look_of_the_day() -> None:
    pieces = common.wardrobe_entries()
    if len(pieces) < 2:
        return
    seed = int(_dt.date.today().strftime("%Y%m%d"))
    by_category: dict[str, list[dict]] = {}
    for entry in pieces:
        by_category.setdefault(entry.get("category", "vetements"), []).append(entry)

    slots = [("vetements", "Haut/Bas"), ("chaussures", "Chaussures"), ("sacs", "Sac"),
             ("manteaux", "Couche"), ("bijoux", "Bijou"), ("accessoires", "Accessoire")]
    chosen: list[dict] = []
    for index, (category, _label) in enumerate(slots):
        options = by_category.get(category)
        if options:
            chosen.append(options[(seed + index) % len(options)])
        if len(chosen) >= 4:
            break
    if not chosen:
        return

    components.section("Look du jour", "Généré depuis votre dressing")
    columns = st.columns(len(chosen), gap="small")
    for column, entry in zip(columns, chosen):
        with column:
            components.image(images.photo(entry.get("photo"), entry["id"], width=240, ratio=float(entry.get("ratio", 0.82))))
    names = " · ".join(entry["title"] for entry in chosen)
    components.html(f'<div class="mp-muted" style="margin:.3rem .1rem 0">{names}</div>')

    if components.button("Enregistrer ce look", key="lotd_save", type="primary", stretch=True):
        look_slots = {slot["key"]: "" for slot in catalogue.LOOK_SLOTS}
        mapping = {"vetements": "haut", "chaussures": "chaussures", "sacs": "sac",
                   "manteaux": "manteau", "bijoux": "bijou", "accessoires": "haut"}
        for entry in chosen:
            slot_key = mapping.get(entry.get("category", "vetements"), "haut")
            if entry.get("item_id") and not look_slots.get(slot_key):
                look_slots[slot_key] = entry["item_id"]
        state.add_entry("looks", {
            "id": f"lk_lotd_{_dt.date.today().isoformat()}",
            "name": f"Look du {_dt.date.today().strftime('%d/%m')}",
            "occasion": "Quotidien",
            "created": _dt.date.today().isoformat(),
            "public": False,
            "likes": 0,
            "note": "Généré depuis ma garde-robe",
            "slots": look_slots,
        })
        state.add_points(15)
        state.push_toast("Look du jour enregistré (+15 pts)", "📸")
        st.rerun()


def _looks_tab() -> None:
    _look_of_the_day()
    common.looks_gallery()


# ---------------------------------------------------------------------------
# Onglet « Récompenses »
# ---------------------------------------------------------------------------
def _rewards_tab() -> None:
    points = int(st.session_state.get("points", 0))
    current, following, progress = catalogue.level_for(points)
    components.html(
        f'<div class="mp-panel"><div class="mp-eyebrow">Programme fidélité</div>'
        f'<h4 style="font-size:1.25rem;margin:.3rem 0 .2rem">{current["icon"]} {current["name"]}</h4>'
        f'<p>{points} points cumulés'
        + (f' · encore {following["threshold"] - points} points pour devenir {following["name"]} {following["icon"]}' if following else " · niveau maximum atteint")
        + "</p></div>"
    )
    st.progress(progress, text=f'Progression vers {following["name"]}' if following else "Niveau maximal")

    components.section("Badges", f"{sum(1 for badge in catalogue.BADGES if catalogue.progress_value(badge['source']) >= badge['need'])}/{len(catalogue.BADGES)} débloqués")
    components.badge_cloud([
        (badge["icon"], badge["label"], catalogue.progress_value(badge["source"]) >= badge["need"])
        for badge in catalogue.BADGES
    ])

    components.section("Défis en cours", "Gagnez des points en un geste")
    claimed = state.phonebook("challenges")
    for challenge in catalogue.CHALLENGES:
        progress_value = catalogue.progress_value(challenge["source"])
        done = progress_value >= challenge["need"]
        is_claimed = bool(claimed.get(challenge["id"]))
        ratio = min(1.0, progress_value / challenge["need"]) if challenge["need"] else 1.0
        with st.container(key=f"tile_ch_{challenge['id']}"):
            components.html(
                f'<div class="mp-card-body"><div class="mp-challenge">'
                f'<div class="ic">{challenge["icon"]}</div>'
                f'<div style="flex:1"><p class="mp-card-title">{challenge["label"]}</p>'
                f'<p class="mp-card-sub">{progress_value}/{challenge["need"]} · +{challenge["reward"]} pts</p></div>'
                f"</div></div>"
            )
            st.progress(ratio)
            if is_claimed:
                components.html('<p class="mp-card-sub" style="margin:.15rem .15rem .4rem">✅ Défi validé, points crédités</p>')
            elif components.button(
                f"Valider · +{challenge['reward']} pts" if done else "En cours…",
                key=f"ch_btn__{challenge['id']}",
                type="primary" if done else "secondary",
                stretch=True,
                disabled=not done,
            ):
                claimed[challenge["id"]] = True
                state.add_points(int(challenge["reward"]))
                state.save_state()
                state.push_toast(f"Défi validé : +{challenge['reward']} points", "🏅")
                st.rerun()

    components.section("Récompenses", "Échangez vos points")
    claimed_rewards = state.bucket("rewards_claimed")
    for reward in catalogue.REWARDS:
        affordable = points >= reward["cost"]
        owned = reward["id"] in claimed_rewards
        with st.container(key=f"tile_rw_{reward['id']}"):
            components.html(
                f'<div class="mp-card-body"><div class="mp-challenge">'
                f'<div class="ic">{reward["icon"]}</div>'
                f'<div style="flex:1"><p class="mp-card-title">{reward["label"]}</p>'
                f'<p class="mp-card-sub">{reward["cost"]} points'
                + (f' · code <b>{reward["code"]}</b>' if owned else "")
                + "</p></div></div></div>"
            )
            if not owned:
                if components.button(
                    "Échanger" if affordable else f"Il manque {reward['cost'] - points} pts",
                    key=f"rw_btn__{reward['id']}",
                    type="primary" if affordable else "secondary",
                    stretch=True,
                    disabled=not affordable,
                ):
                    if state.spend_points(int(reward["cost"])):
                        state.bucket("rewards_claimed").append(reward["id"])
                        state.save_state()
                        state.push_toast(f"Récompense obtenue · code {reward['code']}", "🎉")
                        st.rerun()


# ---------------------------------------------------------------------------
# Onglet « Rendez-vous »
# ---------------------------------------------------------------------------
def _appointment_card(appointment: dict) -> None:
    status = appointment.get("status", "À venir")
    entries = state.bucket("appointments")
    with st.container(key=f"tile_ap_{appointment['id']}"):
        components.html(
            f'<div class="mp-card-body"><p class="mp-card-title">{appointment.get("stylist_name", "Styliste")}</p>'
            f'<p class="mp-card-sub">{appointment.get("date", "")} · {appointment.get("slot", "")} · '
            f'{appointment.get("mode", "")}</p>'
            f'<p class="mp-card-sub">{appointment.get("topic", "")} · '
            f'{components.tags([status], common.appointment_status_color(status))}</p>'
            + (f'<p class="mp-card-sub">« {appointment["note"]} »</p>' if appointment.get("note") else "")
            + "</div>"
        )
        if status != "À venir":
            return
        left, right = st.columns(2)
        with left:
            if components.button("Reporter", key=f"ap_postpone__{appointment['id']}", stretch=True):
                current_date = _dt.date.fromisoformat(appointment["date"])
                new_date = max(current_date, _dt.date.today()) + _dt.timedelta(days=7)
                for entry in entries:
                    if entry["id"] == appointment["id"]:
                        entry["date"] = new_date.isoformat()
                        entry["status"] = "À venir"
                state.save_state()
                state.push_toast(f"Rendez-vous reporté au {new_date.strftime('%d/%m')}", "📆")
                st.rerun()
        with right:
            if components.button("Annuler", key=f"ap_cancel__{appointment['id']}", stretch=True):
                state.update_entry("appointments", appointment["id"], status="Annulé")
                state.push_toast("Rendez-vous annulé", "❌")
                st.rerun()


def _appointments_tab() -> None:
    entries = state.bucket("appointments")
    upcoming = [entry for entry in entries if entry.get("status") == "À venir"]
    history = [entry for entry in entries if entry.get("status") != "À venir"]
    components.stat_row([
        (str(len(upcoming)), "à venir"),
        (str(len(history)), "historique"),
        (f'{int(st.session_state.get("points", 0))}', "points"),
    ])

    if components.button("Réserver avec un styliste", key="ap_book", type="primary", stretch=True):
        nav.goto("explore", explore_tab="Stylistes")

    components.section("Rendez-vous à venir", "Visio, boutique ou à domicile")
    if upcoming:
        for appointment in upcoming:
            _appointment_card(appointment)
    else:
        components.empty("📅", "Aucun rendez-vous programmé : nos stylistes ont des créneaux cette semaine.")

    if history:
        components.section("Historique", f"{len(history)} séance{'s' if len(history) > 1 else ''}")
        for appointment in history:
            _appointment_card(appointment)


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
def render() -> None:
    _profile_header()
    tab = components.segmented(TABS, "account_tab", "Dressing")
    if tab == "Dressing":
        _dressing_tab()
    elif tab == "Wishlist":
        _wishlist_tab()
    elif tab == "Looks":
        _looks_tab()
    elif tab == "Récompenses":
        _rewards_tab()
    else:
        _appointments_tab()
