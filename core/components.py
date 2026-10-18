"""Composants d'interface réutilisables (mobile-first, style Pinterest)."""
from __future__ import annotations

import base64
from typing import Any, Callable, Iterable, Sequence

import streamlit as st

from core import images, state
from core.config import format_price
from core.theme import supports

_IMG_STRETCH = supports(st.image, "width")
_BTN_STRETCH = supports(st.button, "width")

MAX_TAGS = 2


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------
def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def _fit_image() -> dict[str, Any]:
    return {"width": "stretch"} if _IMG_STRETCH else {"use_container_width": True}


def _fit_button() -> dict[str, Any]:
    return {"width": "stretch"} if _BTN_STRETCH else {"use_container_width": True}


def image(data: bytes, caption: str | None = None) -> None:
    st.image(data, caption=caption, **_fit_image())


def button(
    label: str,
    key: str,
    *,
    type: str = "secondary",
    help: str | None = None,
    icon: str | None = None,
    stretch: bool = False,
    disabled: bool = False,
) -> bool:
    kwargs: dict[str, Any] = {"key": key, "type": type, "help": help, "disabled": disabled}
    if icon:
        kwargs["icon"] = icon
    if stretch:
        kwargs.update(_fit_button())
    return st.button(label, **kwargs)


def segmented(options: Sequence[str], key: str, default: str | None = None) -> str:
    """Sélecteur segmenté (repli radio si la version de Streamlit est ancienne)."""
    fallback = default or options[0]
    kwargs: dict[str, Any] = {"key": key, "label_visibility": "collapsed"}
    if key not in st.session_state:
        kwargs["default"] = fallback
    if hasattr(st, "segmented_control"):
        value = st.segmented_control("navigation", list(options), **kwargs)
        return value or fallback
    kwargs.pop("default", None)
    return st.radio("navigation", list(options), horizontal=True, **kwargs)


def text_field(
    label: str,
    key: str,
    *,
    initial: str = "",
    placeholder: str | None = None,
    label_visibility: str = "collapsed",
) -> str:
    """Champ texte qui n'écrase pas la saisie utilisateur lors des reruns."""
    kwargs: dict[str, Any] = {"key": key, "placeholder": placeholder, "label_visibility": label_visibility}
    if key not in st.session_state:
        kwargs["value"] = initial
    return st.text_input(label, **kwargs)


# ---------------------------------------------------------------------------
# Blocs de mise en page
# ---------------------------------------------------------------------------
def section(title: str, subtitle: str | None = None, more: str | None = None) -> None:
    sub = f'<div class="mp-sub">{subtitle}</div>' if subtitle else ""
    extra = f'<span class="mp-more">{more}</span>' if more else ""
    html(f'<div class="mp-section"><div><h3>{title}</h3>{sub}</div>{extra}</div>')


def hero(
    eyebrow: str,
    title: str,
    text: str,
    deco: str = "🧥",
    photo: bytes | None = None,
    extra_class: str = "",
) -> None:
    """Bandeau d'ouverture : dégradé (défaut) ou grande photo éditoriale."""
    if photo:
        encoded = base64.b64encode(photo).decode("ascii")
        html(
            f'<div class="mp-hero photo {extra_class}" '
            f"style=\"background-image:url('data:image/jpeg;base64,{encoded}')\">"
            f'<div class="mp-hero-inner"><div class="mp-eyebrow">{eyebrow}</div>'
            f"<h2>{title}</h2><p>{text}</p></div></div>"
        )
        return
    html(
        f'<div class="mp-hero {extra_class}"><span class="mp-hero-shape"></span>'
        f'<span class="mp-hero-deco">{deco}</span>'
        f'<div class="mp-eyebrow">{eyebrow}</div><h2>{title}</h2><p>{text}</p></div>'
    )


def panel(title: str, text: str, tone: str = "") -> None:
    html(f'<div class="mp-panel {tone}"><h4>{title}</h4><p>{text}</p></div>')


def empty(icon: str, text: str) -> None:
    html(f'<div class="mp-empty"><div>{icon}</div><p>{text}</p></div>')


def stat_row(items: Iterable[tuple[str, str]]) -> None:
    cells = "".join(f'<div class="mp-stat"><b>{value}</b><span>{label}</span></div>' for value, label in items)
    html(f'<div class="mp-stats">{cells}</div>')


def tags(items: Sequence[str], extra: str = "") -> str:
    return "".join(f'<span class="mp-tag {extra}">{item}</span>' for item in items)


def swatches(colors: Sequence[str]) -> None:
    dots = "".join(f'<span class="mp-swatch" style="background:{color}"></span>' for color in colors)
    html(f'<div class="mp-swatches">{dots}</div>')


def badge_cloud(items: Sequence[tuple[str, str, bool]], extra_class: str = "") -> None:
    """``items`` = (emoji, libellé, obtenu)."""
    blocks = []
    for emoji, label, earned in items:
        cls = "earned" if earned else "off"
        blocks.append(f'<div class="mp-badge {cls}"><span>{emoji}</span><span>{label}</span></div>')
    html(f'<div class="mp-badges {extra_class}">{"".join(blocks)}</div>')


def hscroll(key: str, items: Sequence[Any], render_tile: Callable[[Any], None]) -> None:
    """Carrousel horizontal (défilement latéral au doigt / à la souris)."""
    if not items:
        return
    with st.container(key=f"hscroll_{key}"):
        columns = st.columns(len(items), gap="small")
        for column, item in zip(columns, items):
            with column:
                render_tile(item)


def chips(options: Sequence[dict[str, str]], active: str, key_prefix: str, on_select: Callable[[str], None]) -> None:
    """Catégories en pilules, défilables horizontalement."""
    with st.container(key=f"chips_{key_prefix}"):
        columns = st.columns(len(options), gap="small")
        for column, option in zip(columns, options):
            with column:
                clicked = button(
                    f"{option['icon']} {option['label']}",
                    key=f"chip__{key_prefix}__{option['key']}",
                    type="primary" if option["key"] == active else "secondary",
                )
                if clicked and option["key"] != active:
                    on_select(option["key"])


def masonry(items: Sequence[dict], render_card: Callable[[dict], None], columns: int = 2) -> None:
    """Disposition en mosaïque : répartition des cartes par hauteur cumulée."""
    if not items:
        return
    buckets: list[list[dict]] = [[] for _ in range(columns)]
    heights = [0.0] * columns
    for item in items:
        target = heights.index(min(heights))
        buckets[target].append(item)
        ratio = float(item.get("ratio", 0.78) or 0.78)
        heights[target] += 1.0 / max(ratio, 0.3) + 0.42  # + hauteur du bloc texte
    grid = st.columns(columns, gap="small")
    for column, bucket in zip(grid, buckets):
        with column:
            for item in bucket:
                render_card(item)


def action_bar(item: dict, prefix: str, actions: Sequence[tuple[str, str, Callable[[], None]]]) -> None:
    """Rangée d'actions au bas d'une carte : ``(emoji, aide, callback)``."""
    if not actions:
        return
    columns = st.columns(len(actions), gap="small")
    for index, (column, (label, tooltip, callback)) in enumerate(zip(columns, actions)):
        with column:
            clicked = button(label, key=f"act__{prefix}__{item['id']}__{index}", help=tooltip, stretch=True)
            if clicked:
                callback()


# ---------------------------------------------------------------------------
# Carte produit
# ---------------------------------------------------------------------------
def _price_html(item: dict) -> str:
    price = item.get("price")
    old = item.get("old_price")
    if not price:
        return '<span class="mp-tag gold">Sur demande</span>'
    html_price = f'<span class="mp-price">{format_price(price)}</span>'
    if old:
        html_price += f"<s>{format_price(old)}</s>"
    return html_price


def product_card(
    item: dict,
    prefix: str,
    *,
    actions: Sequence[tuple[str, str, Callable[[], None]]] | None = None,
    show_tags: bool = True,
) -> None:
    """Carte visuelle : image, titre, marque, prix, puis actions."""
    with st.container(key=f"card_{prefix}_{item['id']}"):
        if item.get("is_new"):
            html('<span class="mp-ribbon">Nouveau</span>')
        image(images.for_item(item))

        item_tags = list(item.get("tags", []))[:MAX_TAGS]
        tags_html = ""
        if show_tags and item_tags:
            tags_html = f'<div class="mp-card-sub" style="margin-top:.28rem">{tags(item_tags)}</div>'
        label = item.get("label") or item.get("brand", "")
        html(
            f'<div class="mp-card-body">'
            f'<p class="mp-card-title">{item["title"]}</p>'
            f'<p class="mp-card-sub">{label} · {_price_html(item)}</p>'
            f"{tags_html}"
            f"</div>"
        )
        action_bar(item, prefix, actions if actions is not None else default_actions(item))


def default_actions(item: dict) -> list[tuple[str, str, Callable[[], None]]]:
    """Actions par défaut d'une carte : j'aime, enregistrer, wishlist."""
    item_id = item["id"]

    def toggle_like() -> None:
        liked = state.toggle("liked", item_id)
        state.push_toast("Ajouté à vos coups de cœur" if liked else "Retiré de vos coups de cœur", "❤️")

    def toggle_save() -> None:
        saved = state.toggle("saved", item_id)
        if saved:
            state.add_points(5)
            state.push_toast("Enregistré dans vos inspirations (+5 pts)", "🔖")
        else:
            state.push_toast("Retiré de vos inspirations", "🔖")

    def add_to_wishlist() -> None:
        created = state.add_entry("wishlist", wishlist_entry(item))
        state.push_toast("Ajouté à votre wishlist" if created else "Déjà dans votre wishlist", "🛍️")

    liked = state.contains("liked", item_id)
    saved = state.contains("saved", item_id)
    in_wishlist = any(entry.get("id") == item_id for entry in state.bucket("wishlist"))
    return [
        ("❤️" if liked else "🤍", "J'aime", toggle_like),
        ("🔖" if saved else "📑", "Enregistrer l'inspiration", toggle_save),
        ("✅" if in_wishlist else "🛍️", "Ajouter à ma wishlist", add_to_wishlist),
    ]


def wishlist_entry(item: dict, *, intent: str = "acheter", priority: str = "moyenne") -> dict:
    """Transforme une pièce du catalogue en ligne de wishlist."""
    return {
        "id": item["id"],
        "title": item["title"],
        "brand": item.get("brand", ""),
        "price": float(item.get("price") or 0),
        "photo": item.get("photo"),
        "ratio": float(item.get("ratio", 0.78) or 0.78),
        "category": item.get("category", "vetements"),
        "intent": intent,
        "priority": priority,
        "note": "",
    }
