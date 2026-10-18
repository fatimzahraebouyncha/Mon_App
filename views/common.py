"""Helpers partagés par les trois pages (goûts, stats, aperçus de looks)."""
from __future__ import annotations

from collections import Counter
from typing import Any, Sequence

import streamlit as st

from core import components, images, state
from data import catalogue


# ---------------------------------------------------------------------------
# Goûts & statistiques
# ---------------------------------------------------------------------------
def taste() -> tuple[list[str], float | None]:
    """Tags de style dominants et budget, déduits du profil ou de l'activité."""
    profile = st.session_state.get("style_profile") or {}
    tags = list(profile.get("tags") or [])
    budget = profile.get("budget")

    if not tags:
        pool = catalogue.items_from(state.ids("saved") + state.ids("liked"))
        pool += catalogue.items_from([entry.get("item_id") for entry in state.bucket("wardrobe") if entry.get("item_id")])
        for item in pool:
            tags.extend(item.get("tags", []))
    return [tag for tag, _ in Counter(tags).most_common(6)], budget


def wardrobe_stats() -> tuple[int, float, str]:
    entries = state.bucket("wardrobe")
    total = sum(float(entry.get("price") or 0) for entry in entries)
    if entries:
        top = Counter(entry.get("category", "vetements") for entry in entries).most_common(1)[0][0]
        top_label = catalogue.CATEGORY_LABELS.get(top, "—")
    else:
        top_label = "—"
    return len(entries), total, top_label


def wishlist_stats() -> tuple[int, float, float]:
    entries = state.bucket("wishlist")
    to_buy = sum(float(entry.get("price") or 0) for entry in entries if entry.get("intent") == "acheter")
    to_gift = sum(float(entry.get("price") or 0) for entry in entries if entry.get("intent") == "offrir")
    return len(entries), to_buy, to_gift


def signature_of(*parts: Any) -> str:
    return "|".join(str(part) for part in parts)


# ---------------------------------------------------------------------------
# Pièces & looks
# ---------------------------------------------------------------------------
def wardrobe_entries() -> list[dict[str, Any]]:
    return [entry for entry in state.bucket("wardrobe") if isinstance(entry, dict)]


def title_block(title: str, subtitle: str = "") -> None:
    """Titre de page (typo éditoriale)."""
    sub = f'<div class="mp-sub">{subtitle}</div>' if subtitle else ""
    components.html(f'<div style="margin:.25rem .1rem .55rem"><h2 class="mp-display">{title}</h2>{sub}</div>')


def as_catalogue_item(entry: dict[str, Any], *, details: bool = False) -> dict[str, Any]:
    """Vue « catalogue » d'une pièce de dressing ou d'une envie."""
    label = " · ".join(part for part in (entry.get("brand", ""), entry.get("color", "")) if part)
    tags = list(entry.get("tags", []))[:2]
    if details:
        tags = [tag for tag in (entry.get("season", ""), f'{entry.get("wears", 0)}× porté') if tag and tag != "× porté"]
    return {
        "id": entry.get("id") or entry.get("item_id") or "piece",
        "title": entry.get("title", "Pièce"),
        "brand": entry.get("brand", ""),
        "category": entry.get("category", "vetements"),
        "price": float(entry.get("price") or 0),
        "old_price": None,
        "ratio": entry.get("ratio", 0.8),
        "photo": entry.get("photo"),
        "tags": tags,
        "label": label or entry.get("brand", ""),
    }


def look_items(look: dict[str, Any]) -> list[dict[str, Any]]:
    slots = look.get("slots") or {}
    return catalogue.items_from([slot for slot in slots.values() if slot])


def look_preview(look: dict[str, Any], *, caption: bool = True) -> None:
    """Aperçu : vignettes côte à côte + intitulés."""
    items = look_items(look)[:4]
    if not items:
        components.empty("🧵", "Ce look n'a pas encore de pièce.")
        return
    columns = st.columns(len(items), gap="small")
    for column, item in zip(columns, items):
        with column:
            components.image(images.for_item(item, width=240))
    if caption:
        names = " · ".join(item["title"] for item in items[:4])
        components.html(f'<div class="mp-muted" style="margin:.28rem .1rem 0">{names}</div>')


def options_for_slot(slot: dict[str, Any], include_wardrobe: bool = True) -> list[dict[str, Any]]:
    """Pièces proposées pour un emplacement du créateur de looks."""
    options = catalogue.items_from(catalogue.LOOK_LIBRARY)
    wanted = set(slot.get("categories", []))
    filtered = [item for item in options if item["category"] in wanted] if wanted else options
    if include_wardrobe:
        for entry in wardrobe_entries():
            item = catalogue.get_item(entry.get("item_id")) or as_catalogue_item(entry)
            if item["id"] not in {option["id"] for option in filtered}:
                filtered.append(item)
    return filtered


def appointment_status_color(status: str) -> str:
    return {"À venir": "ok", "Terminé": "", "Annulé": "accent"}.get(status, "")


def looks_gallery(title: str = "Mes looks") -> None:
    """Galerie des looks créés, avec actions publier / dupliquer / supprimer."""
    import datetime as _dt

    looks = state.bucket("looks")
    components.section(title, f"{len(looks)} création{'s' if len(looks) > 1 else ''}")
    if not looks:
        components.empty("🧵", "Aucun look pour l'instant : composez le premier depuis l'onglet Looks d'Explorer.")
        return

    for look in looks:
        with st.container(key=f"tile_look_{look['id']}"):
            components.html(
                f'<div class="mp-card-body">'
                f'<p class="mp-card-title">{look["name"]}</p>'
                f'<p class="mp-card-sub">{look.get("occasion", "")} · créé le {look.get("created", "")} · '
                f'{"Public" if look.get("public") else "Privé"}'
                + (f' · ❤️ {look["likes"]}' if look.get("likes") else "")
                + "</p></div>"
            )
            look_preview(look, caption=False)
            left, middle, right = st.columns(3, gap="small")
            with left:
                if components.button("Partager" if look.get("public") else "Publier",
                                     key=f"share__{look['id']}", stretch=True):
                    published = not look.get("public")
                    state.update_entry("looks", look["id"], public=published)
                    if published:
                        state.add_points(10)
                        state.push_toast("Look publié dans votre galerie (+10 pts)", "🌍")
                    st.rerun()
            with middle:
                if components.button("Dupliquer", key=f"dup__{look['id']}", stretch=True):
                    copy = dict(look)
                    copy["id"] = f"lk_{_dt.datetime.now().strftime('%H%M%S%f')[:12]}"
                    copy["name"] = f"{look['name']} (copie)"
                    copy["created"] = _dt.date.today().isoformat()
                    copy["public"] = False
                    copy["likes"] = 0
                    state.add_entry("looks", copy)
                    state.push_toast("Look dupliqué", "🧬")
                    st.rerun()
            with right:
                if components.button("Supprimer", key=f"del__{look['id']}", stretch=True):
                    state.remove_entry("looks", look["id"])
                    state.push_toast("Look supprimé", "🗑️")
                    st.rerun()
