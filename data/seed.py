"""Données de démonstration injectées au premier lancement."""
from __future__ import annotations

import datetime as _dt
from typing import Any

from data import catalogue


def _iso(days_from_today: int) -> str:
    return (_dt.date.today() + _dt.timedelta(days=days_from_today)).isoformat()


def _wardrobe_entry(item_id: str, *, color: str, season: str, favorite: bool = False,
                    wears: int = 0, added: int = 0, source: str = "Achat") -> dict[str, Any]:
    item = catalogue.ITEMS_BY_ID[item_id]
    return {
        "id": f"wd_{item_id}",
        "item_id": item_id,
        "title": item["title"],
        "brand": item["brand"],
        "category": item["category"],
        "photo": item.get("photo"),
        "ratio": item.get("ratio", 0.78),
        "tags": item.get("tags", []),
        "color": color,
        "season": season,
        "favorite": favorite,
        "wears": wears,
        "added": _iso(-added),
        "source": source,
        "price": item.get("price", 0),
    }


def _wishlist_entry(item_id: str, *, intent: str, priority: str, note: str = "") -> dict[str, Any]:
    item = catalogue.ITEMS_BY_ID[item_id]
    return {
        "id": item_id,
        "title": item["title"],
        "brand": item["brand"],
        "category": item["category"],
        "photo": item.get("photo"),
        "ratio": item.get("ratio", 0.78),
        "price": float(item.get("price", 0)),
        "intent": intent,
        "priority": priority,
        "note": note,
    }


def default_store() -> dict[str, Any]:
    """État initial (déjà rempli pour que la démo soit vivante)."""
    return {
        "saved": ["it_trench", "it_collier_plastron", "it_hijab_satine", "it_abaya_noire",
                  "it_kaftan_soie", "it_nails_french", "it_cabas"],
        "liked": ["it_robe_noire", "it_sac_matlasse", "it_abaya_ceremonie", "it_baskets_retro",
                  "it_hijab_imprime"],
        "wardrobe": [
            _wardrobe_entry("it_trench", color="Camel", season="Automne", favorite=True, wears=12, added=180),
            _wardrobe_entry("it_pull_cachemire", color="Écru", season="Hiver", wears=8, added=120),
            _wardrobe_entry("it_sneakers_blanches", color="Blanc", season="Toutes saisons", wears=31, added=300),
            _wardrobe_entry("it_bague_fine", color="Or", season="Toutes saisons", favorite=True, wears=20, added=90),
            _wardrobe_entry("it_sac_seau", color="Cognac", season="Automne", wears=14, added=200),
            _wardrobe_entry("it_chemise_lin", color="Écru", season="Été", wears=6, added=60),
            _wardrobe_entry("it_bottines", color="Chocolat", season="Automne", favorite=True, wears=17, added=150),
            _wardrobe_entry("it_hijab_satine", color="Or", season="Toutes saisons", favorite=True, wears=23, added=110),
            _wardrobe_entry("it_abaya_kimono", color="Écru", season="Printemps", favorite=True, wears=9, added=45),
            _wardrobe_entry("it_kaftan_lin", color="Menthe", season="Été", wears=4, added=30),
        ],
        "wishlist": [
            _wishlist_entry("it_manteau_laine", intent="acheter", priority="haute", note="Pour les jours de grand froid."),
            _wishlist_entry("it_mules", intent="acheter", priority="moyenne"),
            _wishlist_entry("it_takchita", intent="acheter", priority="haute",
                            note="Pour le mariage de ma cousine à Fès."),
            _wishlist_entry("it_hijab_coffret", intent="acheter", priority="moyenne",
                            note="Coloris pour le quotidien."),
            _wishlist_entry("it_collier_plastron", intent="offrir", priority="haute", note="Anniversaire de Nadia en décembre."),
            _wishlist_entry("it_nails_french", intent="offrir", priority="basse"),
        ],
        "looks": [
            {"id": "lk_bureau", "name": "Bureau du lundi", "occasion": "Bureau", "created": _iso(-12),
             "public": True, "likes": 24, "note": "Blazer + bottines, mon combo efficace.",
             "slots": {"haut": "it_blazer", "bas": "it_pantalon_large", "chaussures": "it_bottines",
                       "manteau": "it_trench", "sac": "it_cabas", "bijou": "it_montre_doree"}},
            {"id": "lk_soiree", "name": "Dîner aux chandelles", "occasion": "Soirée", "created": _iso(-5),
             "public": False, "likes": 11, "note": "Noir total, bijoux dorés.",
             "slots": {"haut": "it_robe_noire", "bas": "", "chaussures": "it_escarpins",
                       "manteau": "", "sac": "it_pochette", "bijou": "it_boucles_dorees"}},
            {"id": "lk_vendredi", "name": "Vendredi au riad", "occasion": "Quotidien", "created": _iso(-3),
             "public": True, "likes": 37, "note": "Abaya ceinturée, hijab doré et mules confortables.",
             "slots": {"hijab": "it_hijab_satine", "haut": "it_abaya_kimono", "bas": "",
                       "chaussures": "it_mules", "manteau": "", "sac": "it_sac_seau",
                       "bijou": "it_creoles"}},
        ],
        "appointments": [
            {"id": "ap_demo_1", "stylist_id": "st_camille", "stylist_name": "Camille Rousseau",
             "date": _iso(3), "slot": "18:00", "mode": "Visioconférence", "topic": "Diagnostic de style",
             "note": "Revoir la garde-robe d'hiver.", "status": "À venir", "created": _iso(-2)},
            {"id": "ap_demo_2", "stylist_id": "st_marc", "stylist_name": "Marc-Antoine Lévy",
             "date": _iso(-21), "slot": "16:00", "mode": "En boutique", "topic": "Look événement",
             "note": "Tenue pour le gala.", "status": "Terminé", "created": _iso(-40)},
        ],
        "followed_brands": ["br_lior", "br_nordkapp", "br_perle"],
        "points": 260,
        "badges": ["bd_first_pin", "bd_wardrobe"],
        "challenges": {},
        "rewards_claimed": [],
    }
