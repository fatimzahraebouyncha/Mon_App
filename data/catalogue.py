"""Catalogue de démonstration de Muse.

Toutes les données « métier » vivent ici : catégories, pièces, collections,
stylistes, marques, quiz de style, badges, défis et récompenses.

Pour brancher une vraie API / base de données, il suffit de remplacer le
contenu de ce module : le reste de l'application consomme uniquement les
fonctions utilitaires exposées en bas de fichier.

``photo`` = identifiant d'une photo Unsplash (https://images.unsplash.com/photo-<id>).
Mettre ``None`` pour obtenir un dégradé généré automatiquement.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any, Iterable, Sequence

# ---------------------------------------------------------------------------
# Catégories du feed
# ---------------------------------------------------------------------------
CATEGORIES: list[dict[str, str]] = [
    {"key": "tout", "label": "Tout", "icon": "✨"},
    {"key": "vetements", "label": "Vêtements", "icon": "👗"},
    {"key": "modeste", "label": "Modeste", "icon": "🧕"},
    {"key": "hijabs", "label": "Hijabs", "icon": "🧣"},
    {"key": "abayas", "label": "Abayas", "icon": "🌙"},
    {"key": "kaftans", "label": "Kaftans", "icon": "🌺"},
    {"key": "chaussures", "label": "Chaussures", "icon": "👟"},
    {"key": "bijoux", "label": "Bijoux", "icon": "💎"},
    {"key": "manteaux", "label": "Manteaux", "icon": "🧥"},
    {"key": "sacs", "label": "Sacs", "icon": "👜"},
    {"key": "ongles", "label": "Ongles", "icon": "💅"},
    {"key": "accessoires", "label": "Accessoires", "icon": "🕶️"},
    {"key": "laine", "label": "Maille", "icon": "🧶"},
    {"key": "soiree", "label": "Soirée", "icon": "🌙"},
    {"key": "vintage", "label": "Vintage", "icon": "🕰️"},
]

CATEGORY_LABELS = {category["key"]: category["label"] for category in CATEGORIES}


# ---------------------------------------------------------------------------
# Photos de la ligne modeste (identifiants Unsplash vérifiés)
# ---------------------------------------------------------------------------
MODEST_PHOTOS: dict[str, str] = {
    # Hijabs & voiles
    "hijab_jersey": "1569245087840-dcf487ddbad5",
    "hijab_mousseline": "1571498521264-5fcaa7f8edf4",
    "hijab_satine": "1718913134925-a7054f3656a4",
    "hijab_imprime": "1651313950238-7f569c1fc2ba",
    "hijab_coffret": "1730355446798-661568ad2e89",
    "sous_hijab": "1609803384069-19f3e5a70e75",
    # Abayas
    "abaya_crete": "1760083545495-b297b1690672",
    "abaya_noire": "1772474587292-08b3e8932acd",
    "abaya_brodee": "1772474500365-c2c520545f44",
    "abaya_kimono": "1772474557170-4818d01d7bca",
    "abaya_ceremonie": "1532370436137-d9aaea5dab36",
    # Kaftans, takchitas, djellabas
    "kaftan_soie": "1629200468267-b926a7675ce2",
    "kaftan_lin": "1753192108753-81be0db2f7fe",
    "takchita": "1668028563825-f3b7138db3de",
    "kaftan_fete": "1728411187437-0de943a9bcfb",
    "djellaba_lin": "1753486986377-1395ccfb4a8a",
    # Tenues modestes
    "robe_longue": "1596783074918-c84cb06531ca",
    "robe_plissee": "1568251863885-adcac989de24",
    "robe_maxi": "1678534959653-b20b96150733",
    "ensemble_beige": "1552874869-5c39ec9288dc",
    "ensemble_sport": "1770803204288-31382ee0daec",
    "ensemble_noir": "1668028554854-245f8ccae15b",
    "robe_portefeuille": "1612722432474-b971cdcea546",
    "robe_satin": "1746366618558-e510b8067579",
    # Ambiances : collections, marques, stylistes, looks
    "cover_modeste": "1667844926432-7c53f4baa985",
    "cover_ceremonie": "1696318024580-58b55ed21ab6",
    "cover_tradition": "1619447019169-746572a5df47",
    "cover_boutique": "1657087097505-e395c02ab327",
    "cover_atelier": "1707978932202-751b08324daf",
    "cover_riad": "1517315403381-a12569a9da85",
    # Photos d'ouverture (bandeaux éditoriaux)
    "hero_modeste": "1673547991911-c8b25dde4b9b",
    "hero_monde": "1505339805025-a5ec452332d9",
    "portrait_vert": "1680970950875-fa09fd663717",
    "portrait_or": "1613062538918-016d7d19e5d1",
    "portrait_rose": "1505673271747-923ee579555c",
    "portrait_sable": "1634047112477-f91b7ab9b271",
    "souk_ambiance": "1629548572655-a97a8638e279",
    "salon_matelas": "1584339312444-6952d098e152",
}


# ---------------------------------------------------------------------------
# Pièces (feed, recherche, looks, garde-robe)
# ---------------------------------------------------------------------------
ITEMS: list[dict[str, Any]] = [
    # ----------------------------------------------------------- Vêtements
    {"id": "it_robe_soie", "title": "Robe midi en soie", "brand": "Maison Lior", "category": "vetements",
     "price": 1890, "old_price": 2350, "ratio": 0.72, "likes": 1284, "is_new": True,
     "tags": ["soirée", "fluide", "minimal"], "photo": "1487222477894-8943e31ef7b2",
     "colors": ["#B4604B", "#E8D8CB", "#2A211C"], "season": "Automne"},
    {"id": "it_blazer", "title": "Blazer oversize en laine", "brand": "Studio Nord", "category": "vetements",
     "price": 1490, "old_price": 1890, "ratio": 0.78, "likes": 2130, "is_new": True,
     "tags": ["bureau", "structuré", "minimal"], "photo": "1515886657613-9f3515b0c78f",
     "colors": ["#1A1512", "#B0A79C", "#F2EDE6"], "season": "Automne"},
    {"id": "it_chemise_lin", "title": "Chemise en lin lavé", "brand": "Casa Lino", "category": "vetements",
     "price": 690, "ratio": 0.82, "likes": 940,
     "tags": ["week-end", "neutre", "vacances"], "photo": "1475180098004-ca77a66827be",
     "colors": ["#F5EFE6", "#CBB9A4"], "season": "Été"},
    {"id": "it_pull_cachemire", "title": "Pull côtelé en cachemire", "brand": "Maison Solal", "category": "vetements",
     "price": 1290, "ratio": 0.75, "likes": 1580, "is_new": True,
     "tags": ["laine", "cocooning", "neutre"], "photo": "1551488831-00ddcb6c6bd3",
     "colors": ["#E3D7C9", "#9C8C7C", "#5C4B3D"], "season": "Hiver"},
    {"id": "it_robe_imprimee", "title": "Robe portefeuille imprimée", "brand": "Rio Vintage", "category": "vetements",
     "price": 890, "ratio": 0.72, "likes": 2210,
     "tags": ["vintage", "été", "romantique"], "photo": "1595777457583-95e059d581b8",
     "colors": ["#D9836A", "#F0DCC8"], "season": "Été"},
    {"id": "it_robe_noire", "title": "Robe noire asymétrique", "brand": "Atelier Perle", "category": "vetements",
     "price": 1720, "ratio": 0.7, "likes": 3120, "is_new": True,
     "tags": ["soirée", "minimal", "noir"], "photo": "1483985988355-763728e1935b",
     "colors": ["#12100F", "#3B3531"], "season": "Toutes saisons"},
    {"id": "it_top_satin", "title": "Top en satin drapé", "brand": "Velvet & Co", "category": "vetements",
     "price": 790, "ratio": 0.8, "likes": 760,
     "tags": ["soirée", "fluide", "romantique"], "photo": "1490481651871-ab68de25d43d",
     "colors": ["#E8CFC0", "#B98E7B"], "season": "Toutes saisons"},
    {"id": "it_combinaison", "title": "Combinaison fluide", "brand": "Studio Nord", "category": "vetements",
     "price": 1390, "ratio": 0.74, "likes": 1180,
     "tags": ["bureau", "minimal", "voyage"], "photo": "1479064555552-3ef4979f8908",
     "colors": ["#2F3A36", "#C8BFA9"], "season": "Printemps"},
    {"id": "it_robe_popeline", "title": "Robe chemise en popeline", "brand": "Casa Lino", "category": "vetements",
     "price": 980, "old_price": 1290, "ratio": 0.76, "likes": 640,
     "tags": ["bureau", "neutre", "vacances"], "photo": "1554568218-0f1715e72254",
     "colors": ["#F0EAE0", "#A9B3A1"], "season": "Printemps"},
    {"id": "it_pantalon_large", "title": "Pantalon large plissé", "brand": "Nordkapp", "category": "vetements",
     "price": 890, "ratio": 0.85, "likes": 1320,
     "tags": ["bureau", "street", "denim"], "photo": "1445205170230-053b83016050",
     "colors": ["#4B4A46", "#BCB4A5"], "season": "Toutes saisons"},
    {"id": "it_robe_dentelle", "title": "Robe en dentelle florale", "brand": "Rio Vintage", "category": "vetements",
     "price": 1560, "ratio": 0.7, "likes": 2870,
     "tags": ["romantique", "vintage", "soirée"], "photo": "1572804013309-59a88b7e92f1",
     "colors": ["#F7E4E4", "#C79AA4"], "season": "Printemps"},
    {"id": "it_ensemble_maille", "title": "Ensemble en maille côtelée", "brand": "Maison Solal", "category": "vetements",
     "price": 1450, "ratio": 0.78, "likes": 890,
     "tags": ["laine", "cocooning", "minimal"], "photo": "1441986300917-64674bd600d8",
     "colors": ["#DFD3C3", "#8D7C69"], "season": "Hiver"},

    # ----------------------------------------------------------- Manteaux
    {"id": "it_trench", "title": "Trench oversize beige", "brand": "Velvet & Co", "category": "manteaux",
     "price": 2190, "old_price": 2790, "ratio": 0.72, "likes": 3410, "is_new": True,
     "tags": ["tailoring", "classique", "mi-saison"], "photo": "1506630448388-4e683c67ddb0",
     "colors": ["#D8C3A5", "#7C6A55"], "season": "Automne"},
    {"id": "it_manteau_laine", "title": "Manteau long en laine", "brand": "Maison Lior", "category": "manteaux",
     "price": 2890, "ratio": 0.68, "likes": 1960, "is_new": True,
     "tags": ["classique", "tailoring", "hiver"], "photo": "1544022613-e87ca75a784a",
     "colors": ["#3B332C", "#B49B84"], "season": "Hiver"},
    {"id": "it_veste_jean", "title": "Veste en jean vintage", "brand": "Rio Vintage", "category": "manteaux",
     "price": 790, "ratio": 0.8, "likes": 1420,
     "tags": ["vintage", "denim", "street"], "photo": "1472851294608-062f824d29cc",
     "colors": ["#8AA3B8", "#DCE3E8"], "season": "Printemps"},
    {"id": "it_cape", "title": "Cape en cachemire", "brand": "Maison Solal", "category": "manteaux",
     "price": 2490, "ratio": 0.74, "likes": 720,
     "tags": ["cocooning", "laine", "classique"], "photo": "1441984904996-e0b6ba687e04",
     "colors": ["#C2B6A6", "#6B5F52"], "season": "Hiver"},

    # --------------------------------------------------------- Chaussures
    {"id": "it_sneakers_blanches", "title": "Sneakers minimalistes", "brand": "Nordkapp", "category": "chaussures",
     "price": 1190, "ratio": 0.9, "likes": 4210,
     "tags": ["street", "quotidien", "sport"], "photo": "1542291026-7eec264c27ff",
     "colors": ["#FFFFFF", "#E4E0DA"], "season": "Toutes saisons"},
    {"id": "it_bottines", "title": "Bottines en cuir", "brand": "Velvet & Co", "category": "chaussures",
     "price": 1790, "ratio": 0.86, "likes": 1890, "is_new": True,
     "tags": ["classique", "mi-saison", "tailoring"], "photo": "1560769629-975ec94e6a86",
     "colors": ["#5B3A2A", "#2B1D16"], "season": "Automne"},
    {"id": "it_mules", "title": "Mules à talon carré", "brand": "Atelier Perle", "category": "chaussures",
     "price": 1390, "ratio": 0.88, "likes": 980,
     "tags": ["soirée", "élégant", "romantique"], "photo": "1543163521-1bf539c55dd2",
     "colors": ["#C9A227", "#F0E4D4"], "season": "Été"},
    {"id": "it_sneakers_toile", "title": "Sneakers en toile", "brand": "Rio Vintage", "category": "chaussures",
     "price": 690, "ratio": 0.95, "likes": 2540,
     "tags": ["street", "été", "quotidien"], "photo": "1595950653106-6c9ebd614d3a",
     "colors": ["#F5F1E8", "#C0563F"], "season": "Été"},
    {"id": "it_baskets_retro", "title": "Baskets rétro colorées", "brand": "Nordkapp", "category": "chaussures",
     "price": 990, "old_price": 1290, "ratio": 0.92, "likes": 3320,
     "tags": ["street", "sport", "vintage"], "photo": "1600185365483-26d7a4cc7519",
     "colors": ["#E8B04B", "#4E6E81"], "season": "Toutes saisons"},
    {"id": "it_escarpins", "title": "Escarpins en daim", "brand": "Maison Lior", "category": "chaussures",
     "price": 1590, "ratio": 0.84, "likes": 840,
     "tags": ["soirée", "bureau", "élégant"], "photo": "1591047139829-d91aecb6caea",
     "colors": ["#1F1B18", "#7A6A5A"], "season": "Toutes saisons"},
    {"id": "it_baskets_pastel", "title": "Sneakers pastel", "brand": "Velvet & Co", "category": "chaussures",
     "price": 950, "ratio": 0.93, "likes": 1610,
     "tags": ["pastel", "quotidien", "street"], "photo": "1520639888713-7851133b1ed0",
     "colors": ["#EBD9E4", "#B7D4D0"], "season": "Printemps"},

    # ------------------------------------------------------------- Bijoux
    {"id": "it_bague_fine", "title": "Bague solitaire fine", "brand": "Atelier Perle", "category": "bijoux",
     "price": 2400, "ratio": 0.9, "likes": 1120,
     "tags": ["minimal", "or", "quotidien"], "photo": "1515562141207-7a88fb7ce338",
     "colors": ["#E7C873", "#F6EFE2"], "season": "Toutes saisons"},
    {"id": "it_boucles_dorees", "title": "Boucles d'oreilles dorées", "brand": "Atelier Perle", "category": "bijoux",
     "price": 650, "ratio": 0.88, "likes": 2240,
     "tags": ["or", "soirée", "romantique"], "photo": "1602173574767-37ac01994b2a",
     "colors": ["#D9B25F", "#FBF1D7"], "season": "Toutes saisons"},
    {"id": "it_creoles", "title": "Créoles martelées", "brand": "Maison Solal", "category": "bijoux",
     "price": 780, "ratio": 0.92, "likes": 1870,
     "tags": ["quotidien", "or", "street"], "photo": "1573408301185-9146fe634ad0",
     "colors": ["#C9A227", "#EFE3CB"], "season": "Toutes saisons"},
    {"id": "it_collier_plastron", "title": "Collier plastron doré", "brand": "Atelier Perle", "category": "bijoux",
     "price": 1290, "ratio": 0.8, "likes": 2650, "is_new": True,
     "tags": ["soirée", "or", "statement"], "photo": "1535632066927-ab7c9ab60908",
     "colors": ["#E0B657", "#4C3A22"], "season": "Toutes saisons"},
    {"id": "it_bracelet_jonc", "title": "Bracelet jonc empilable", "brand": "Velvet & Co", "category": "bijoux",
     "price": 890, "ratio": 0.9, "likes": 1340,
     "tags": ["minimal", "quotidien", "or"], "photo": "1599643478518-a784e5dc4c8f",
     "colors": ["#D8C08A", "#F4EEE2"], "season": "Toutes saisons"},
    {"id": "it_parure", "title": "Parure émeraude", "brand": "Maison Lior", "category": "bijoux",
     "price": 3200, "ratio": 0.86, "likes": 690,
     "tags": ["soirée", "statement", "élégant"], "photo": "1611591437281-460bfbe1220a",
     "colors": ["#2F6B57", "#E4D6B8"], "season": "Toutes saisons"},
    {"id": "it_montre_classique", "title": "Montre classique cuir", "brand": "Velvet & Co", "category": "bijoux",
     "price": 1990, "ratio": 0.94, "likes": 1520,
     "tags": ["classique", "bureau", "quotidien"], "photo": "1457972729786-0411a3b2b626",
     "colors": ["#6B4A32", "#F2EDE6"], "season": "Toutes saisons"},
    {"id": "it_montre_doree", "title": "Montre dorée fine", "brand": "Atelier Perle", "category": "bijoux",
     "price": 2490, "ratio": 0.92, "likes": 1060,
     "tags": ["or", "élégant", "bureau"], "photo": "1524805444758-089113d48a6d",
     "colors": ["#D9B45F", "#FBF3DF"], "season": "Toutes saisons"},

    # --------------------------------------------------------------- Sacs
    {"id": "it_sac_seau", "title": "Sac seau en cuir", "brand": "Velvet & Co", "category": "sacs",
     "price": 2490, "ratio": 0.85, "likes": 2410,
     "tags": ["classique", "cuir", "bureau"], "photo": "1548036328-c9fa89d128fa",
     "colors": ["#7A5334", "#D8C1A5"], "season": "Automne"},
    {"id": "it_sac_matlasse", "title": "Sac matelassé à chaîne", "brand": "Maison Lior", "category": "sacs",
     "price": 3200, "old_price": 3900, "ratio": 0.8, "likes": 3890, "is_new": True,
     "tags": ["soirée", "élégant", "statement"], "photo": "1584917865442-de89df76afd3",
     "colors": ["#1A1512", "#C9A227"], "season": "Toutes saisons"},
    {"id": "it_cabas", "title": "Cabas en cuir grainé", "brand": "Casa Lino", "category": "sacs",
     "price": 2890, "ratio": 0.82, "likes": 2150, "is_new": True,
     "tags": ["bureau", "quotidien", "cuir"], "photo": "1591561954557-26941169b49e",
     "colors": ["#C9A489", "#F1E5D8"], "season": "Toutes saisons"},
    {"id": "it_pochette", "title": "Pochette de soirée", "brand": "Atelier Perle", "category": "sacs",
     "price": 1490, "ratio": 0.88, "likes": 1180,
     "tags": ["soirée", "élégant", "minimal"], "photo": "1553062407-98eeb64c6a62",
     "colors": ["#3B3531", "#E7C873"], "season": "Toutes saisons"},
    {"id": "it_sac_dos", "title": "Sac à dos en toile", "brand": "Nordkapp", "category": "sacs",
     "price": 990, "ratio": 0.9, "likes": 1640,
     "tags": ["voyage", "street", "quotidien"], "photo": "1491637639811-60e2756cc1c7",
     "colors": ["#4C4A45", "#C2B49B"], "season": "Toutes saisons"},

    # -------------------------------------------------------------- Ongles
    {"id": "it_nails_nude", "title": "Nail art nude", "brand": "Studio Ongles", "category": "ongles",
     "price": 450, "ratio": 0.9, "likes": 3260,
     "tags": ["minimal", "bureau", "nude"], "photo": "1604654894610-df63bc536371",
     "colors": ["#EBD3C3", "#F7EFE8"], "season": "Toutes saisons"},
    {"id": "it_nails_french", "title": "French manucure revisitée", "brand": "Studio Ongles", "category": "ongles",
     "price": 390, "ratio": 0.92, "likes": 4120, "is_new": True,
     "tags": ["classique", "élégant", "nude"], "photo": "1632345031435-8727f6897d53",
     "colors": ["#FBF6F1", "#E8C7C0"], "season": "Toutes saisons"},
    {"id": "it_nails_terracotta", "title": "Ongles terracotta", "brand": "Studio Ongles", "category": "ongles",
     "price": 420, "ratio": 0.88, "likes": 2380,
     "tags": ["terracotta", "automne", "statement"], "photo": "1610992015732-2449b76344bc",
     "colors": ["#C0563F", "#E2A183"], "season": "Automne"},
    {"id": "it_nails_vernis", "title": "Vernis chatoyant", "brand": "Atelier Perle", "category": "ongles",
     "price": 350, "ratio": 0.94, "likes": 1560,
     "tags": ["soirée", "statement", "pastel"], "photo": "1519014816548-bf5fe059798b",
     "colors": ["#B9A6D1", "#EADFF5"], "season": "Toutes saisons"},
    {"id": "it_nails_perles", "title": "Nail art perles", "brand": "Studio Ongles", "category": "ongles",
     "price": 480, "ratio": 0.86, "likes": 2890,
     "tags": ["romantique", "soirée", "nude"], "photo": "1522337660859-02fbefca4702",
     "colors": ["#F2E6DE", "#D9BFB0"], "season": "Printemps"},
    {"id": "it_nails_baby", "title": "Baby boomer nacré", "brand": "Studio Ongles", "category": "ongles",
     "price": 460, "ratio": 0.9, "likes": 1980,
     "tags": ["nude", "élégant", "mariage"], "photo": "1613966802194-d46a163af70d",
     "colors": ["#F6E7E2", "#DCC5BC"], "season": "Toutes saisons"},

    # --------------------------------------------------------- Accessoires
    {"id": "it_lunettes_oversize", "title": "Lunettes oversize", "brand": "Rio Vintage", "category": "accessoires",
     "price": 1290, "ratio": 0.9, "likes": 2740,
     "tags": ["vintage", "été", "statement"], "photo": "1511499767150-a48a237f0083",
     "colors": ["#2B2320", "#C9A98B"], "season": "Été"},
    {"id": "it_lunettes_carrees", "title": "Lunettes carrées acétate", "brand": "Velvet & Co", "category": "accessoires",
     "price": 1450, "ratio": 0.92, "likes": 1290,
     "tags": ["bureau", "classique", "statement"], "photo": "1572635196237-14b3f281503f",
     "colors": ["#5B4433", "#E3D4C2"], "season": "Toutes saisons"},
    {"id": "it_lunettes_rondes", "title": "Lunettes rondes rétro", "brand": "Rio Vintage", "category": "accessoires",
     "price": 1100, "ratio": 0.94, "likes": 1760,
     "tags": ["vintage", "street", "été"], "photo": "1473496169904-658ba7c44d8a",
     "colors": ["#B08D57", "#F0E6D6"], "season": "Été"},
    {"id": "it_foulard", "title": "Foulard en soie imprimé", "brand": "Maison Lior", "category": "accessoires",
     "price": 790, "ratio": 0.86, "likes": 2210,
     "tags": ["romantique", "or", "élégant"], "photo": "1567401893414-76b7b1e5a7a5",
     "colors": ["#C0563F", "#EFD9C1"], "season": "Printemps"},
    {"id": "it_ceinture", "title": "Ceinture cuir tressé", "brand": "Casa Lino", "category": "accessoires",
     "price": 650, "ratio": 0.96, "likes": 830,
     "tags": ["cuir", "quotidien", "minimal"], "photo": "1512436991641-6745cdb1723f",
     "colors": ["#6B4A32", "#D8C1A5"], "season": "Toutes saisons"},
    {"id": "it_chapeau", "title": "Chapeau en feutre", "brand": "Rio Vintage", "category": "accessoires",
     "price": 890, "ratio": 0.88, "likes": 1450,
     "tags": ["vintage", "automne", "élégant"], "photo": "1523381210434-271e8be1f52b",
     "colors": ["#4A3B2E", "#CBB79A"], "season": "Automne"},

    # -------------------------------------------- Hijabs & voiles (Dar Basma)
    {"id": "it_hijab_jersey", "title": "Hijab en jersey premium", "brand": "Dar Basma", "category": "hijabs",
     "price": 149, "ratio": 0.72, "likes": 3180, "is_new": True,
     "tags": ["modeste", "quotidien", "hijab"], "photo": MODEST_PHOTOS["hijab_jersey"],
     "colors": ["#1A1512", "#C0563F", "#F2EDE6", "#5F6F52"], "season": "Toutes saisons"},
    {"id": "it_hijab_mousseline", "title": "Hijab en mousseline de soie", "brand": "Dar Basma", "category": "hijabs",
     "price": 219, "ratio": 0.75, "likes": 2540,
     "tags": ["modeste", "soirée", "hijab"], "photo": MODEST_PHOTOS["hijab_mousseline"],
     "colors": ["#E8D8CB", "#B4604B", "#7A8B8F"], "season": "Toutes saisons"},
    {"id": "it_hijab_satine", "title": "Hijab satiné de cérémonie", "brand": "Dar Basma", "category": "hijabs",
     "price": 259, "ratio": 0.7, "likes": 2960, "is_new": True,
     "tags": ["modeste", "mariage", "hijab"], "photo": MODEST_PHOTOS["hijab_satine"],
     "colors": ["#C9A227", "#F6EFE2", "#1A1512"], "season": "Toutes saisons"},
    {"id": "it_hijab_imprime", "title": "Hijab imprimé floral", "brand": "Dar Basma", "category": "hijabs",
     "price": 189, "ratio": 0.78, "likes": 1870,
     "tags": ["modeste", "été", "hijab"], "photo": MODEST_PHOTOS["hijab_imprime"],
     "colors": ["#C0563F", "#E0A86A", "#F0E4D4"], "season": "Printemps"},
    {"id": "it_hijab_coffret", "title": "Coffret 3 hijabs en coton", "brand": "Dar Basma", "category": "hijabs",
     "price": 299, "ratio": 0.8, "likes": 2210, "is_new": True,
     "tags": ["modeste", "quotidien", "hijab"], "photo": MODEST_PHOTOS["hijab_coffret"],
     "colors": ["#F5EFE6", "#8D7C69", "#2F6B57", "#C0563F"], "season": "Toutes saisons"},
    {"id": "it_sous_hijab", "title": "Bonnet sous-hijab en jersey", "brand": "Dar Basma", "category": "hijabs",
     "price": 79, "ratio": 0.85, "likes": 1420,
     "tags": ["modeste", "quotidien", "hijab"], "photo": MODEST_PHOTOS["sous_hijab"],
     "colors": ["#1A1512", "#CBB79A", "#B0A79C"], "season": "Toutes saisons"},

    # --------------------------------------------------- Abayas (Atelier Noor)
    {"id": "it_abaya_crete", "title": "Abaya dubai en crêpe", "brand": "Atelier Noor", "category": "abayas",
     "price": 690, "ratio": 0.68, "likes": 2680,
     "tags": ["modeste", "quotidien", "abaya"], "photo": MODEST_PHOTOS["abaya_crete"],
     "colors": ["#E3D7C9", "#1A1512", "#7A6A5A"], "season": "Toutes saisons"},
    {"id": "it_abaya_noire", "title": "Abaya noire fluide", "brand": "Atelier Noor", "category": "abayas",
     "price": 750, "ratio": 0.7, "likes": 3420, "is_new": True,
     "tags": ["modeste", "soirée", "abaya"], "photo": MODEST_PHOTOS["abaya_noire"],
     "colors": ["#12100F", "#3B3531"], "season": "Toutes saisons"},
    {"id": "it_abaya_brodee", "title": "Abaya brodée fil argent", "brand": "Atelier Noor", "category": "abayas",
     "price": 990, "ratio": 0.72, "likes": 1980,
     "tags": ["modeste", "mariage", "abaya"], "photo": MODEST_PHOTOS["abaya_brodee"],
     "colors": ["#12100F", "#C0C6CC"], "season": "Toutes saisons"},
    {"id": "it_abaya_kimono", "title": "Abaya kimono ceinturée", "brand": "Atelier Noor", "category": "abayas",
     "price": 890, "ratio": 0.7, "likes": 2340,
     "tags": ["modeste", "bureau", "abaya"], "photo": MODEST_PHOTOS["abaya_kimono"],
     "colors": ["#F2EDE6", "#1A1512", "#B08D57"], "season": "Printemps"},
    {"id": "it_abaya_ceremonie", "title": "Abaya de cérémonie dorée", "brand": "Atelier Noor", "category": "abayas",
     "price": 1290, "ratio": 0.66, "likes": 2810, "is_new": True,
     "tags": ["modeste", "mariage", "abaya"], "photo": MODEST_PHOTOS["abaya_ceremonie"],
     "colors": ["#1A1512", "#C9A227", "#6E4B3C"], "season": "Toutes saisons"},

    # ------------------------------ Kaftans, takchitas & djellabas (Dar Lalla)
    {"id": "it_kaftan_soie", "title": "Caftan marocain en soie", "brand": "Dar Lalla", "category": "kaftans",
     "price": 1590, "ratio": 0.68, "likes": 3120, "is_new": True,
     "tags": ["modeste", "mariage", "kaftan"], "photo": MODEST_PHOTOS["kaftan_soie"],
     "colors": ["#E8D8CB", "#C9A227", "#B4604B"], "season": "Toutes saisons"},
    {"id": "it_kaftan_lin", "title": "Kaftan léger en lin", "brand": "Dar Lalla", "category": "kaftans",
     "price": 950, "ratio": 0.7, "likes": 1740,
     "tags": ["modeste", "été", "kaftan"], "photo": MODEST_PHOTOS["kaftan_lin"],
     "colors": ["#9FD3C7", "#F2EDE6"], "season": "Été"},
    {"id": "it_takchita", "title": "Takchita de cérémonie (2 pièces)", "brand": "Dar Lalla", "category": "kaftans",
     "price": 2490, "ratio": 0.66, "likes": 2260,
     "tags": ["mariage", "kaftan", "statement"], "photo": MODEST_PHOTOS["takchita"],
     "colors": ["#7B2E3B", "#C9A227", "#2F6B57"], "season": "Toutes saisons"},
    {"id": "it_kaftan_fete", "title": "Caftan de fête brodé", "brand": "Dar Lalla", "category": "kaftans",
     "price": 1790, "ratio": 0.68, "likes": 2050,
     "tags": ["modeste", "mariage", "kaftan"], "photo": MODEST_PHOTOS["kaftan_fete"],
     "colors": ["#2F6B57", "#C9A227"], "season": "Toutes saisons"},
    {"id": "it_djellaba_lin", "title": "Djellaba moderne en lin", "brand": "Dar Lalla", "category": "kaftans",
     "price": 780, "ratio": 0.7, "likes": 1580,
     "tags": ["modeste", "quotidien", "kaftan"], "photo": MODEST_PHOTOS["djellaba_lin"],
     "colors": ["#F5EFE6", "#B0A79C"], "season": "Printemps"},

    # ----------------------------------------------------- Tenues modestes
    {"id": "it_robe_longue_modeste", "title": "Robe longue fluide", "brand": "Atelier Noor",
     "category": "vetements", "price": 590, "ratio": 0.7, "likes": 2480, "is_new": True,
     "tags": ["modeste", "quotidien", "fluide"], "photo": MODEST_PHOTOS["robe_longue"],
     "colors": ["#E8B9A8", "#F2EDE6"], "season": "Été"},
    {"id": "it_robe_plissee_modeste", "title": "Robe plissée à manches longues", "brand": "Studio Nord",
     "category": "vetements", "price": 690, "ratio": 0.72, "likes": 1930,
     "tags": ["modeste", "soirée", "fluide"], "photo": MODEST_PHOTOS["robe_plissee"],
     "colors": ["#B0A79C", "#3B3531"], "season": "Toutes saisons"},
    {"id": "it_robe_maxi_imprimee", "title": "Robe maxi imprimée", "brand": "Rio Vintage",
     "category": "vetements", "price": 550, "ratio": 0.7, "likes": 2140,
     "tags": ["modeste", "été", "romantique"], "photo": MODEST_PHOTOS["robe_maxi"],
     "colors": ["#B4604B", "#E8D8CB"], "season": "Été"},
    {"id": "it_ensemble_modeste", "title": "Ensemble modeste sable", "brand": "Casa Lino",
     "category": "vetements", "price": 650, "ratio": 0.72, "likes": 2670, "is_new": True,
     "tags": ["modeste", "quotidien", "neutre"], "photo": MODEST_PHOTOS["ensemble_beige"],
     "colors": ["#E3D7C9", "#CBB9A4"], "season": "Printemps"},
    {"id": "it_ensemble_sport_modeste", "title": "Ensemble sport modeste", "brand": "Nordkapp",
     "category": "vetements", "price": 490, "ratio": 0.75, "likes": 1830,
     "tags": ["modeste", "sport", "quotidien"], "photo": MODEST_PHOTOS["ensemble_sport"],
     "colors": ["#8B8078", "#B7D4D0"], "season": "Toutes saisons"},
    {"id": "it_ensemble_noir_modeste", "title": "Ensemble fluide noir", "brand": "Atelier Perle",
     "category": "vetements", "price": 720, "ratio": 0.7, "likes": 2210,
     "tags": ["modeste", "soirée", "noir"], "photo": MODEST_PHOTOS["ensemble_noir"],
     "colors": ["#12100F", "#3B3531"], "season": "Toutes saisons"},
    {"id": "it_robe_portefeuille_modeste", "title": "Robe portefeuille longue", "brand": "Maison Lior",
     "category": "vetements", "price": 620, "ratio": 0.7, "likes": 1690,
     "tags": ["modeste", "bureau", "élégant"], "photo": MODEST_PHOTOS["robe_portefeuille"],
     "colors": ["#E0A86A", "#F2EDE6"], "season": "Toutes saisons"},
    {"id": "it_robe_satin_modeste", "title": "Robe satinée couvrante", "brand": "Maison Lior",
     "category": "vetements", "price": 690, "ratio": 0.72, "likes": 2010,
     "tags": ["modeste", "soirée", "satin"], "photo": MODEST_PHOTOS["robe_satin"],
     "colors": ["#E7C9D3", "#C9A227"], "season": "Toutes saisons"},
]

ITEMS_BY_ID = {item["id"]: item for item in ITEMS}


# ---------------------------------------------------------------------------
# Nouvelles collections
# ---------------------------------------------------------------------------
COLLECTIONS: list[dict[str, Any]] = [
    {"id": "col_modeste", "name": "Modest Chic", "brand": "Atelier Noor", "pieces": 46,
     "photo": MODEST_PHOTOS["cover_modeste"], "tagline": "Abayas fluides, hijabs coordonnés, élégance discrète",
     "accent": "#6E4B3C", "tags": ["modeste", "abaya", "hijab"]},
    {"id": "col_automne", "name": "Automne Doré", "brand": "Maison Lior", "pieces": 24,
     "photo": "1506630448388-4e683c67ddb0", "tagline": "Cuirs patinés & laines douces",
     "accent": "#C0563F", "tags": ["tailoring", "classique", "terracotta"]},
    {"id": "col_minimal", "name": "Minimal Urbain", "brand": "Studio Nord", "pieces": 18,
     "photo": "1515886657613-9f3515b0c78f", "tagline": "Silhouettes nettes, matières nobles",
     "accent": "#2F3A36", "tags": ["minimal", "bureau", "neutre"]},
    {"id": "col_soie", "name": "Soie & Bijoux", "brand": "Atelier Perle", "pieces": 31,
     "photo": "1535632066927-ab7c9ab60908", "tagline": "Éclat discret pour les soirs d'hiver",
     "accent": "#C9A227", "tags": ["soirée", "or", "statement"]},
    {"id": "col_street", "name": "Street Luxe", "brand": "Nordkapp", "pieces": 22,
     "photo": "1542291026-7eec264c27ff", "tagline": "Le confort qui a du style",
     "accent": "#3B3531", "tags": ["street", "sport", "quotidien"]},
    {"id": "col_ete", "name": "Été Solaire", "brand": "Casa Lino", "pieces": 27,
     "photo": "1475180098004-ca77a66827be", "tagline": "Lin, paille et lumière",
     "accent": "#E0A86A", "tags": ["été", "vacances", "romantique"]},
    {"id": "col_ceremonie", "name": "Kaftans & Cérémonies", "brand": "Dar Lalla", "pieces": 38,
     "photo": MODEST_PHOTOS["cover_ceremonie"], "tagline": "Takchitas, caftans brodés et grandes occasions",
     "accent": "#7B2E3B", "tags": ["kaftan", "mariage", "statement"]},
    {"id": "col_medina", "name": "Riad & Médina", "brand": "Dar Basma", "pieces": 29,
     "photo": MODEST_PHOTOS["cover_riad"], "tagline": "Hijabs, lin lavé et couleurs du sud",
     "accent": "#C9A227", "tags": ["hijab", "modeste", "été"]},
]


# ---------------------------------------------------------------------------
# Stylistes
# ---------------------------------------------------------------------------
STYLISTS: list[dict[str, Any]] = [
    {"id": "st_camille", "name": "Camille Rousseau", "specialty": "Élégance minimaliste",
     "city": "Paris", "rating": 4.9, "reviews": 128, "price": 650,
     "photo": "1490481651871-ab68de25d43d", "tags": ["minimal", "bureau", "capsule"],
     "bio": "J'épure les garde-robes pour ne garder que l'essentiel, jamais le banal.",
     "slots": ["18:00", "19:30"]},
    {"id": "st_ines", "name": "Inès Bensalem", "specialty": "Streetwear & vintage",
     "city": "Lyon", "rating": 4.8, "reviews": 94, "price": 550,
     "photo": "1512436991641-6745cdb1723f", "tags": ["street", "vintage", "denim"],
     "bio": "Je chine, je détourne, je remixe : votre style unique existe déjà quelque part.",
     "slots": ["12:30", "17:00", "18:30"]},
    {"id": "st_marc", "name": "Marc-Antoine Lévy", "specialty": "Costume & tailoring",
     "city": "Paris", "rating": 5.0, "reviews": 156, "price": 800,
     "photo": "1506630448388-4e683c67ddb0", "tags": ["tailoring", "classique", "mariage"],
     "bio": "Une épaule bien tombée change tout. Je m'occupe du reste.",
     "slots": ["10:00", "16:00"]},
    {"id": "st_sofia", "name": "Sofia Marchetti", "specialty": "Mariage & cérémonie",
     "city": "Marseille", "rating": 4.7, "reviews": 71, "price": 700,
     "photo": "1487222477894-8943e31ef7b2", "tags": ["romantique", "mariage", "élégant"],
     "bio": "Des silhouettes qui se souviennent des grandes occasions.",
     "slots": ["11:00", "15:30", "19:00"]},
    {"id": "st_youssef", "name": "Youssef Ndiaye", "specialty": "Couleurs & imprimés",
     "city": "Lille", "rating": 4.9, "reviews": 63, "price": 500,
     "photo": "1441984904996-e0b6ba687e04", "tags": ["terracotta", "statement", "été"],
     "bio": "La couleur est un accessoire : je vous apprends à la porter.",
     "slots": ["13:00", "18:00"]},
    {"id": "st_lea", "name": "Léa Vidal", "specialty": "Garde-robe durable",
     "city": "Bordeaux", "rating": 4.8, "reviews": 112, "price": 600,
     "photo": "1551488831-00ddcb6c6bd3", "tags": ["capsule", "neutre", "laine"],
     "bio": "Moins de pièces, plus de tenues : le vestiaire qui dure des années.",
     "slots": ["09:30", "14:00", "17:30"]},
    {"id": "st_salma", "name": "Salma El Amrani", "specialty": "Mode modeste & hijab",
     "city": "Casablanca", "rating": 4.9, "reviews": 187, "price": 600,
     "photo": MODEST_PHOTOS["portrait_vert"], "tags": ["modeste", "hijab", "élégant"],
     "bio": "Je compose des tenues couvrantes et lumineuses : hijabs coordonnés, superpositions, matières fluides.",
     "slots": ["11:00", "15:00", "18:30"]},
    {"id": "st_hind", "name": "Hind Bennani", "specialty": "Abayas & cérémonies",
     "city": "Marrakech", "rating": 5.0, "reviews": 143, "price": 700,
     "photo": MODEST_PHOTOS["portrait_or"], "tags": ["abaya", "kaftan", "mariage"],
     "bio": "Takchitas, caftans et abayas de fête : je vous guide du choix des broderies aux retouches.",
     "slots": ["10:30", "14:30", "17:00"]},
]

#: Modes de rendez-vous proposés.
APPOINTMENT_MODES = ["Visioconférence", "En boutique", "À domicile"]

#: Motifs de consultation.
APPOINTMENT_TOPICS = [
    "Diagnostic de style",
    "Tri de garde-robe",
    "Look événement",
    "Personal shopping",
    "Capsule durable",
    "Conseil mode modeste",
    "Tenue de cérémonie",
]

#: Looks de la communauté (galerie d'inspiration, copiables en un clic).
COMMUNITY_LOOKS: list[dict[str, Any]] = [
    {"id": "cl_paris", "name": "Promenade parisienne", "author": "@leila.mode", "city": "Paris",
     "occasion": "Week-end", "likes": 842,
     "slots": {"haut": "it_chemise_lin", "bas": "it_pantalon_large", "chaussures": "it_sneakers_blanches",
               "manteau": "it_trench", "sac": "it_cabas", "bijou": "it_creoles"}},
    {"id": "cl_soir", "name": "Nuit dorée", "author": "@maya.style", "city": "Marseille",
     "occasion": "Soirée", "likes": 1264,
     "slots": {"haut": "it_robe_noire", "bas": "", "chaussures": "it_escarpins",
               "manteau": "", "sac": "it_pochette", "bijou": "it_collier_plastron"}},
    {"id": "cl_bureau", "name": "Bureau assumé", "author": "@ines.b", "city": "Lyon",
     "occasion": "Bureau", "likes": 598,
     "slots": {"haut": "it_blazer", "bas": "it_pantalon_large", "chaussures": "it_mules",
               "manteau": "it_manteau_laine", "sac": "it_sac_seau", "bijou": "it_montre_classique"}},
    {"id": "cl_ete", "name": "Été solaire", "author": "@casa.ines", "city": "Barcelone",
     "occasion": "Voyage", "likes": 733,
     "slots": {"haut": "it_robe_imprimee", "bas": "", "chaussures": "it_sneakers_toile",
               "manteau": "", "sac": "it_sac_dos", "bijou": "it_boucles_dorees"}},
    {"id": "cl_maille", "name": "Cocooning chic", "author": "@lea.vidal", "city": "Bordeaux",
     "occasion": "Quotidien", "likes": 421,
     "slots": {"haut": "it_pull_cachemire", "bas": "it_pantalon_large", "chaussures": "it_bottines",
               "manteau": "it_cape", "sac": "it_cabas", "bijou": "it_bracelet_jonc"}},
    {"id": "cl_vendredi", "name": "Vendredi chic", "author": "@salma.modeste", "city": "Casablanca",
     "occasion": "Quotidien", "likes": 1478,
     "slots": {"hijab": "it_hijab_satine", "haut": "it_abaya_kimono", "bas": "", "chaussures": "it_mules",
               "manteau": "", "sac": "it_sac_seau", "bijou": "it_creoles"}},
    {"id": "cl_ceremonie", "name": "Cérémonie dorée", "author": "@noor.kaftan", "city": "Fès",
     "occasion": "Mariage", "likes": 2130,
     "slots": {"hijab": "it_hijab_mousseline", "haut": "it_takchita", "bas": "", "chaussures": "it_escarpins",
               "manteau": "", "sac": "it_pochette", "bijou": "it_parure"}},
    {"id": "cl_riad", "name": "Balade au riad", "author": "@basma.marrakech", "city": "Marrakech",
     "occasion": "Week-end", "likes": 964,
     "slots": {"hijab": "it_hijab_jersey", "haut": "it_djellaba_lin", "bas": "", "chaussures": "it_sneakers_blanches",
               "manteau": "", "sac": "it_sac_dos", "bijou": "it_bracelet_jonc"}},
]


# ---------------------------------------------------------------------------
# Marques
# ---------------------------------------------------------------------------
BRANDS: list[dict[str, Any]] = [
    {"id": "br_lior", "name": "Maison Lior", "city": "Paris", "pieces": 148, "followers": 128400,
     "price_range": "2 000 MAD et plus", "style": "Tailoring contemporain", "photo": "1515886657613-9f3515b0c78f",
     "tags": ["tailoring", "classique", "soirée"], "is_new": False},
    {"id": "br_nord", "name": "Studio Nord", "city": "Copenhague", "pieces": 96, "followers": 96200,
     "price_range": "900 – 2 000 MAD", "style": "Minimalisme scandinave", "photo": "1479064555552-3ef4979f8908",
     "tags": ["minimal", "bureau", "neutre"], "is_new": True},
    {"id": "br_perle", "name": "Atelier Perle", "city": "Paris", "pieces": 210, "followers": 74300,
     "price_range": "2 000 MAD et plus", "style": "Joaillerie artisanale", "photo": "1602173574767-37ac01994b2a",
     "tags": ["or", "statement", "soirée"], "is_new": False},
    {"id": "br_nordkapp", "name": "Nordkapp", "city": "Oslo", "pieces": 132, "followers": 154800,
     "price_range": "900 – 2 000 MAD", "style": "Street premium", "photo": "1542291026-7eec264c27ff",
     "tags": ["street", "sport", "quotidien"], "is_new": True},
    {"id": "br_velvet", "name": "Velvet & Co", "city": "Milan", "pieces": 174, "followers": 210500,
     "price_range": "2 000 MAD et plus", "style": "Cuir & accessoires", "photo": "1560769629-975ec94e6a86",
     "tags": ["cuir", "classique", "élégant"], "is_new": False},
    {"id": "br_rio", "name": "Rio Vintage", "city": "Lisbonne", "pieces": 88, "followers": 51200,
     "price_range": "Moins de 900 MAD", "style": "Seconde main sélectionnée", "photo": "1473496169904-658ba7c44d8a",
     "tags": ["vintage", "denim", "été"], "is_new": False},
    {"id": "br_casa", "name": "Casa Lino", "city": "Barcelone", "pieces": 64, "followers": 43800,
     "price_range": "900 – 2 000 MAD", "style": "Lin & matières naturelles", "photo": "1475180098004-ca77a66827be",
     "tags": ["neutre", "vacances", "été"], "is_new": False},
    {"id": "br_solal", "name": "Maison Solal", "city": "Genève", "pieces": 58, "followers": 38700,
     "price_range": "2 000 MAD et plus", "style": "Maille haut de gamme", "photo": "1551488831-00ddcb6c6bd3",
     "tags": ["laine", "cocooning", "minimal"], "is_new": True},
    {"id": "br_basma", "name": "Dar Basma", "city": "Marrakech", "pieces": 74, "followers": 86200,
     "price_range": "Moins de 900 MAD", "style": "Hijabs & voiles premium", "photo": MODEST_PHOTOS["cover_boutique"],
     "tags": ["hijab", "modeste", "quotidien"], "is_new": True, "ships_worldwide": True},
    {"id": "br_noor", "name": "Atelier Noor", "city": "Casablanca", "pieces": 112, "followers": 104300,
     "price_range": "900 - 2 000 MAD", "style": "Abayas contemporaines", "photo": MODEST_PHOTOS["cover_atelier"],
     "tags": ["abaya", "modeste", "mariage"], "is_new": True, "ships_worldwide": True},
    {"id": "br_lalla", "name": "Dar Lalla", "city": "Fès", "pieces": 48, "followers": 57300,
     "price_range": "2 000 MAD et plus", "style": "Caftans & takchitas brodées",
     "photo": MODEST_PHOTOS["cover_tradition"], "tags": ["kaftan", "mariage", "statement"],
     "is_new": False, "ships_worldwide": True},
]

#: Note affichée sur les fiches marques (livraison internationale).
BRAND_SHIPPING = "🌍 Livraison partout dans le monde"


# ---------------------------------------------------------------------------
# Test de style (Explorer → Mon style)
# ---------------------------------------------------------------------------
STYLE_QUIZ: list[dict[str, Any]] = [
    {"id": "q_terrain", "question": "Votre terrain de jeu préféré ?", "icon": "🎯",
     "options": [
         {"label": "Le bureau", "tags": ["bureau", "minimal"]},
         {"label": "Les soirées", "tags": ["soirée", "tailoring"]},
         {"label": "Les week-ends", "tags": ["week-end", "bohème"]},
         {"label": "Les voyages", "tags": ["voyage", "street"]},
         {"label": "Les grandes occasions", "tags": ["mariage", "romantique"]},
         {"label": "Les réunions de famille", "tags": ["modeste", "mariage"]},
     ]},
    {"id": "q_palette", "question": "Votre palette idéale ?", "icon": "🎨",
     "options": [
         {"label": "Neutres sable & écru", "tags": ["neutre", "minimal"]},
         {"label": "Terracotta & or", "tags": ["terracotta", "bohème"]},
         {"label": "Pastel doux", "tags": ["pastel", "romantique"]},
         {"label": "Noir total", "tags": ["noir", "minimal"]},
         {"label": "Bleu nuit & cuir", "tags": ["classique", "tailoring"]},
         {"label": "Sable, or et vert sauge", "tags": ["modeste", "neutre"]},
     ]},
    {"id": "q_piece", "question": "Votre pièce signature ?", "icon": "⭐",
     "options": [
         {"label": "Blazer structuré", "tags": ["bureau", "tailoring"]},
         {"label": "Robe fluide", "tags": ["romantique", "soirée"]},
         {"label": "Jean & sneakers", "tags": ["street", "denim"]},
         {"label": "Manteau long", "tags": ["classique", "hiver"]},
         {"label": "Maille cocooning", "tags": ["laine", "cocooning"]},
         {"label": "Abaya ou caftan fluide", "tags": ["modeste", "abaya"]},
     ]},
    {"id": "q_budget", "question": "Votre budget par pièce ?", "icon": "💳",
     "options": [
         {"label": "Moins de 500 MAD", "tags": [], "budget": 500},
         {"label": "500 à 1 500 MAD", "tags": [], "budget": 1500},
         {"label": "1 500 à 3 000 MAD", "tags": [], "budget": 3000},
         {"label": "Peu importe, je craque", "tags": [], "budget": 100000},
     ]},
]

STYLE_RESULTS: list[dict[str, Any]] = [
    {"id": "sr_minimal", "name": "Élégance minimaliste", "icon": "🕊️",
     "description": "Des lignes nettes, des matières nobles et une palette maîtrisée. Vous cherchez la pièce juste, jamais l'accessoire de trop.",
     "tags": ["minimal", "neutre", "bureau"],
     "palette": ["#F2EDE6", "#C9B8A8", "#1A1512", "#B0A79C"],
     "tips": ["Misez sur des matières (laine, soie, lin) plutôt que sur des logos.",
              "Une seule pièce statement par tenue suffit.",
              "Achetez peu, mais coupez court : retouches systématiques."]},
    {"id": "sr_boheme", "name": "Bohème solaire", "icon": "🌞",
     "description": "Vous mélangez les textures, superposez les bijoux et laissez entrer la couleur. Votre style raconte le voyage.",
     "tags": ["bohème", "terracotta", "été"],
     "palette": ["#F7E7D3", "#E0A86A", "#C0563F", "#8C6B4F"],
     "tips": ["Superposez les bijoux dorés par deux ou trois.",
              "Osez les imprimés, mais gardez une base unie.",
              "Les matières naturelles réchauffent instantanément la silhouette."]},
    {"id": "sr_street", "name": "Street chic", "icon": "🛹",
     "description": "Le confort d'abord, mais jamais au détriment du style. Bases fortes, sneakers léchées, attitude assumée.",
     "tags": ["street", "sport", "denim"],
     "palette": ["#EDEDED", "#2F2F2F", "#C0563F", "#F2C14E"],
     "tips": ["Investissez dans des sneakers impeccables, elles font la tenue.",
              "Surpantalon large, choisissez un haut plus ajusté.",
              "Une pièce vintage par look crée la différence."]},
    {"id": "sr_classique", "name": "Néo-classique", "icon": "🎩",
     "description": "Tailoring, matières profondes et coupes impeccables. Vous aimez ce qui traverse les saisons.",
     "tags": ["classique", "tailoring", "mariage"],
     "palette": ["#F5F2EC", "#22303C", "#B08D57", "#7A6A5A"],
     "tips": ["Faites reprendre vos vestes : c'est le secret du tombé parfait.",
              "Deux tons profonds valent mieux que cinq tons moyens.",
              "Un cuir patiné vaut mille tendances."]},
    {"id": "sr_romantique", "name": "Pastel romantique", "icon": "🌸",
     "description": "Vous aimez la douceur, les détails délicats et les silhouettes fluides qui se déplacent avec vous.",
     "tags": ["romantique", "pastel", "soirée"],
     "palette": ["#FBEDF0", "#E7C9D3", "#C9A0B5", "#F6E3D9"],
     "tips": ["Mélangez deux pastels, pas plus.",
              "Ajoutez un bijou doré pour structurer la douceur.",
              "Osez le satin, même le jour."]},
    {"id": "sr_modeste", "name": "Élégance modeste", "icon": "🌙",
     "description": "Vous cherchez des coupes couvrantes, des matières nobles et une élégance discrète : "
                    "hijabs coordonnés, abayas fluides, caftans et robes longues composent votre vestiaire.",
     "tags": ["modeste", "abaya", "hijab", "mariage", "élégant"],
     "palette": ["#F2EDE6", "#C9A227", "#5F6F52", "#1A1512"],
     "tips": ["Coordonnez le hijab au ton dominant de la tenue.",
              "Une broderie suffit : gardez le reste uni.",
              "Crêpe, mousseline et lin tombent mieux que les synthétiques."]},
]


# ---------------------------------------------------------------------------
# Fidélité : niveaux, badges, défis, récompenses
# ---------------------------------------------------------------------------
LEVELS: list[tuple[int, str, str]] = [
    (0, "Curieuse", "🌟"),
    (300, "Connaisseuse", "💫"),
    (700, "Icône", "👑"),
    (1500, "Muse", "🦋"),
]

BADGES: list[dict[str, Any]] = [
    {"id": "bd_first_pin", "icon": "📍", "label": "Première épingle", "need": 1, "source": "saved"},
    {"id": "bd_looks", "icon": "📸", "label": "Créatrice de looks", "need": 3, "source": "looks"},
    {"id": "bd_wardrobe", "icon": "🚪", "label": "Dressing connecté", "need": 5, "source": "wardrobe"},
    {"id": "bd_quiz", "icon": "🧠", "label": "Style décodé", "need": 1, "source": "style_profile"},
    {"id": "bd_stylist", "icon": "🤝", "label": "Accompagnée", "need": 1, "source": "appointments"},
    {"id": "bd_wishlist", "icon": "🎁", "label": "Liste au clair", "need": 3, "source": "wishlist"},
]

CHALLENGES: list[dict[str, Any]] = [
    {"id": "ch_look", "icon": "📸", "label": "Créer 3 looks", "reward": 80, "need": 3, "source": "looks"},
    {"id": "ch_quiz", "icon": "🧠", "label": "Terminer le test de style", "reward": 50, "need": 1, "source": "style_profile"},
    {"id": "ch_wardrobe", "icon": "🚪", "label": "Ajouter 5 pièces à mon dressing", "reward": 60, "need": 5, "source": "wardrobe"},
    {"id": "ch_stylist", "icon": "🤝", "label": "Réserver un rendez-vous styliste", "reward": 120, "need": 1, "source": "appointments"},
    {"id": "ch_wishlist", "icon": "🎁", "label": "Compléter ma wishlist", "reward": 40, "need": 3, "source": "wishlist"},
]

REWARDS: list[dict[str, Any]] = [
    {"id": "rw_10", "icon": "🏷️", "label": "-10 % chez Maison Lior", "cost": 300, "code": "MUSE10"},
    {"id": "rw_nails", "icon": "💅", "label": "Nail art offert chez Studio Ongles", "cost": 500, "code": "NAILS-ON"},
    {"id": "rw_stylist", "icon": "👩‍🎨", "label": "Séance styliste offerte", "cost": 800, "code": "STYLE-GIFT"},
    {"id": "rw_silk", "icon": "🧣", "label": "Foulard en soie signature", "cost": 1200, "code": "SILK-MUSE"},
]


# ---------------------------------------------------------------------------
# Emplacements du créateur de looks
# ---------------------------------------------------------------------------
LOOK_SLOTS: list[dict[str, Any]] = [
    {"key": "hijab", "label": "Hijab / voile", "icon": "🧣", "categories": ["hijabs"]},
    {"key": "haut", "label": "Haut", "icon": "👚", "categories": ["vetements", "abayas", "kaftans"]},
    {"key": "bas", "label": "Bas", "icon": "👖", "categories": ["vetements"]},
    {"key": "chaussures", "label": "Chaussures", "icon": "👟", "categories": ["chaussures"]},
    {"key": "manteau", "label": "Couche", "icon": "🧥", "categories": ["manteaux", "abayas"]},
    {"key": "sac", "label": "Sac", "icon": "👜", "categories": ["sacs"]},
    {"key": "bijou", "label": "Bijou", "icon": "💎", "categories": ["bijoux"]},
]

LOOK_OCCASIONS = ["Quotidien", "Bureau", "Soirée", "Week-end", "Mariage", "Voyage"]

#: Pièces proposées pour créer un look (mix « vêtements » utilisables en haut/bas).
LOOK_LIBRARY: list[str] = [
    "it_blazer", "it_chemise_lin", "it_top_satin", "it_pull_cachemire", "it_robe_soie", "it_robe_noire",
    "it_combinaison", "it_robe_popeline", "it_ensemble_maille", "it_robe_dentelle", "it_robe_imprimee",
    "it_pantalon_large", "it_veste_jean", "it_trench", "it_manteau_laine", "it_cape",
    "it_sneakers_blanches", "it_bottines", "it_mules", "it_baskets_retro", "it_escarpins", "it_baskets_pastel",
    "it_sac_seau", "it_sac_matlasse", "it_cabas", "it_pochette", "it_sac_dos",
    "it_bague_fine", "it_boucles_dorees", "it_creoles", "it_collier_plastron", "it_montre_doree",
    # Ligne modeste
    "it_hijab_jersey", "it_hijab_mousseline", "it_hijab_satine", "it_hijab_imprime",
    "it_abaya_crete", "it_abaya_noire", "it_abaya_brodee", "it_abaya_kimono", "it_abaya_ceremonie",
    "it_kaftan_soie", "it_kaftan_lin", "it_takchita", "it_kaftan_fete", "it_djellaba_lin",
    "it_robe_longue_modeste", "it_robe_plissee_modeste", "it_robe_maxi_imprimee", "it_ensemble_modeste",
    "it_ensemble_sport_modeste", "it_ensemble_noir_modeste", "it_robe_portefeuille_modeste",
    "it_robe_satin_modeste",
]


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------
_FR_DAYS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]
_FR_MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août",
              "sept.", "oct.", "nov.", "déc."]


def get_item(item_id: str | None) -> dict[str, Any] | None:
    return ITEMS_BY_ID.get(item_id or "")


def items_from(ids: Iterable[str]) -> list[dict[str, Any]]:
    """Pièces correspondant à une liste d'identifiants (ordre conservé)."""
    resolved = [ITEMS_BY_ID[item_id] for item_id in ids if item_id in ITEMS_BY_ID]
    return resolved


def by_category(category: str, items: Sequence[dict] | None = None) -> list[dict[str, Any]]:
    """Filtre par catégorie principale (``tout`` = pas de filtre) ou par tag."""
    source = list(items if items is not None else ITEMS)
    if category == "tout":
        return source
    return [item for item in source if item["category"] == category or category in item.get("tags", [])]


def search(query: str, items: Sequence[dict] | None = None) -> list[dict[str, Any]]:
    """Recherche plein texte simple (titre, marque, tags, catégorie)."""
    source = list(items if items is not None else ITEMS)
    needle = (query or "").strip().lower()
    if not needle:
        return source
    words = [word for word in needle.replace(",", " ").split() if word]

    def score(item: dict) -> int:
        haystack = " ".join([
            item["title"], item["brand"], item.get("season", ""),
            CATEGORY_LABELS.get(item["category"], ""), " ".join(item.get("tags", [])),
        ]).lower()
        return sum(1 for word in words if word in haystack)

    return sorted((item for item in source if score(item)), key=score, reverse=True)


def trending(limit: int = 8) -> list[dict[str, Any]]:
    return sorted(ITEMS, key=lambda item: item.get("likes", 0), reverse=True)[:limit]


def new_arrivals(limit: int = 8) -> list[dict[str, Any]]:
    return [item for item in ITEMS if item.get("is_new")][:limit]


def recommend(tags: Sequence[str], limit: int = 6, budget: float | None = None) -> list[dict[str, Any]]:
    """Recommande des pièces à partir de tags de style (profil de style)."""
    wanted = set(tags or [])

    def score(item: dict) -> tuple[int, int]:
        overlap = len(wanted & set(item.get("tags", [])))
        affordable = 1 if (budget is None or item.get("price", 0) <= budget) else 0
        return overlap + affordable, item.get("likes", 0)

    ranked = sorted(ITEMS, key=score, reverse=True)
    if budget:
        affordable = [item for item in ranked if item.get("price", 0) <= budget]
        if len(affordable) >= limit:
            return affordable[:limit]
    return ranked[:limit]


def stylist(stylist_id: str | None) -> dict[str, Any] | None:
    return next((item for item in STYLISTS if item["id"] == stylist_id), None)


def brand(brand_id: str | None) -> dict[str, Any] | None:
    return next((item for item in BRANDS if item["id"] == brand_id), None)


def brand_by_name(name: str) -> dict[str, Any] | None:
    return next((item for item in BRANDS if item["name"] == name), None)


def upcoming_slots(stylist_id: str, count: int = 6, start_offset: int = 1) -> list[dict[str, str]]:
    """Prochaines disponibilités (dates réelles à partir de demain)."""
    person = stylist(stylist_id)
    hours = (person or {}).get("slots", ["18:00"])
    today = _dt.date.today()
    slots: list[dict[str, str]] = []
    day = start_offset
    index = 0
    while len(slots) < count and day < start_offset + 14:
        current = today + _dt.timedelta(days=day)
        if current.weekday() != 6:  # pas de créneaux le dimanche
            hour = hours[index % len(hours)]
            slots.append({
                "key": f"{current.isoformat()}T{hour}",
                "date": current.isoformat(),
                "label": f"{_FR_DAYS[current.weekday()]} {current.day} {_FR_MONTHS[current.month - 1]} · {hour}",
                "short": f"{_FR_DAYS[current.weekday()]} {current.day} {_FR_MONTHS[current.month - 1]}",
                "hour": hour,
            })
            index += 1
        day += 1
    return slots


def level_for(points: int) -> tuple[dict[str, Any], dict[str, Any] | None, float]:
    """Niveau courant, niveau suivant et progression (0 → 1)."""
    current = {"name": LEVELS[0][1], "icon": LEVELS[0][2], "threshold": LEVELS[0][0]}
    following: dict[str, Any] | None = None
    for threshold, name, icon in LEVELS:
        if points >= threshold:
            current = {"name": name, "icon": icon, "threshold": threshold}
    for threshold, name, icon in LEVELS:
        if threshold > current["threshold"]:
            following = {"name": name, "icon": icon, "threshold": threshold}
            break
    if following is None:
        return current, None, 1.0
    span = following["threshold"] - current["threshold"]
    progress = (points - current["threshold"]) / span if span else 1.0
    return current, following, max(0.0, min(1.0, progress))


def progress_value(source: str) -> int:
    """Valeur de progression d'un badge/défi à partir de l'état de session."""
    import streamlit as st

    if source == "style_profile":
        return 1 if st.session_state.get("style_profile") else 0
    value = st.session_state.get(source, [])
    if isinstance(value, dict):
        return len(value)
    return len(value or [])
