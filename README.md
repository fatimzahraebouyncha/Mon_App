# Muse 🧣 — application de mode (mobile-first, inspirée de Pinterest)

Application de style et d'inspiration mode construite avec **Streamlit** : feed visuel en
mosaïque, découverte de son style, stylistes, marques, créateur de looks, dressing digital,
wishlist et programme de fidélité.

Ouverte **à tout le monde** : chaque personne crée son compte avec un **e-mail ou un numéro de
téléphone**, choisit son **pays** parmi tous ceux du monde, et les prix s'affichent en
**dirhams marocains (MAD)**. La ligne **mode modeste / hijab** (hijabs, abayas, kaftans,
takchitas, robes longues) est intégrée au catalogue, aux filtres, aux looks et aux stylistes.

L'interface est pensée **mobile d'abord** : colonne de contenu de 520 px maximum, barre de
navigation fixe en bas (🏠 Accueil · 🔍 Explorer · 👤 Mon compte), cartes arrondies, typographie
éditoriale et animations discrètes.

---

## 🚀 Lancer l'application

**Windows — le plus simple :**

```bat
run.bat
```

Le script crée l'environnement virtuel, installe les dépendances puis démarre l'application
sur <http://localhost:8501>.

**Manuellement :**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

> Astuce mobile : ouvrez l'URL sur votre téléphone (même réseau Wi-Fi) ou utilisez le mode
> responsive de votre navigateur. L'application est calibrée pour un affichage téléphone.
> Si le port 8501 est déjà pris : `--server.port 8600`.

---

## 🔐 Comptes & connexion

- Écran d'accueil : **« Se connecter »** (e-mail **ou** numéro de téléphone + mot de passe) et
  **« Créer un compte »** (nom, e-mail, téléphone — au moins l'un des deux —, pays, mot de passe).
- **Compte de démonstration** prêt à l'emploi : `sarah@muse.ma` · mot de passe `muse`
  (ou bouton « 🎬 Entrer dans le compte de démo »).
- **Plusieurs personnes sur le même appareil** : chaque compte garde son dressing, sa wishlist,
  ses looks, ses points et son pays. La liste « Comptes sur cet appareil » permet de choisir un
  compte (le mot de passe est demandé à la connexion) ; « 🔐 Changer de compte » et
  « 👋 Se déconnecter » sont dans **Mon compte**.
- Les mots de passe sont stockés hachés (PBKDF2 + sel) dans `data/user_store.json` — suffisant
  pour une démo locale ; brancher un vrai backend pour une mise en ligne (voir plus bas).
- À l'inscription, on choisit son **pays** (≈ 190 pays, drapeaux inclus) : il s'affiche sur le
  profil, et les marques indiquent une **livraison partout dans le monde**.

---

## 🧩 Les 3 pages

### 🏠 Accueil — le feed visuel
- Barre supérieure collante : logo, notifications, accès au compte.
- Recherche instantanée (titre, marque, matière, tag).
- **Catégories en pilules défilables** : Tout, Vêtements, **Modeste**, **Hijabs**, **Abayas**,
  **Kaftans**, Chaussures, Bijoux, Manteaux, Sacs, Ongles, Accessoires, Maille, Soirée, Vintage.
- **Bandeau collection** (Modest Chic · Atelier Noor) + carrousel **Nouvelles collections**
  défilable (Kaftans & Cérémonies, Riad & Médina, Automne Doré…).
- **Pour vous** : recommandations calculées depuis le test de style ou vos inspirations.
- **Feed en mosaïque** (2 colonnes, hauteurs variables) avec ❤️ coup de cœur, 🔖 enregistrer
  (+5 pts) et 🛍️ ajout à la wishlist — pagination « Afficher plus ».

### 🔍 Explorer — style, stylistes, marques, looks, pièces
- **Style** : test en 4 questions (progression visible) → profil de style avec palette, conseils
  et recommandations ajustées au budget. Six profils, dont **Élégance modeste**.
- **Stylistes** : fiches (note, ville, tarif **en MAD**, spécialités) et **réservation réelle** :
  créneaux sur les prochains jours, format (visio — partout dans le monde — / boutique /
  domicile), motif, note. Deux spécialistes de la mode modeste et des cérémonies.
- **Marques** : cartes de maisons à suivre (Dar Basma, Atelier Noor, Dar Lalla…) avec prix
  indicatifs en MAD, **livraison mondiale**, et accès direct à leurs pièces.
- **Looks** : **créateur de look** (7 emplacements, **hijab / voile** inclus) avec aperçu live,
  galerie communautaire copiable en un clic (looks voilés et de cérémonie), gestion de vos
  créations (publier, dupliquer, supprimer).
- **Pièces** : filtres catégorie / budget (MAD) / tri, recherche, résultats en mosaïque.

### 👤 Mon compte — l'espace personnel
- Profil modifiable (nom, **pays**, bio, avatar emoji), e-mail / téléphone affichés,
  statistiques, et gestion du compte (changer de compte, se déconnecter).
- **Dressing digital** : ajout de pièce, filtres, tri, marquage « portée », coups de cœur,
  indicateurs (valeur estimée, prix moyen, catégorie dominante), **Look du jour** généré
  automatiquement depuis votre garde-robe.
- **Wishlist** : articles à **acheter** ou à **offrir**, priorités, budget, note cadeau,
  bascule achat/cadeau, « déjà acheté » → la pièce part au dressing (+30 pts).
  En dessous : inspirations enregistrées et coups de cœur.
- **Looks** : vos créations et le look du jour.
- **Récompenses** : points, niveaux (Curieuse → Muse), badges, défis à valider, récompenses
  à échanger (codes promo).
- **RDV** : rendez-vous à venir et historique, reporter ou annuler.

---

## 🗂️ Structure du projet

```
mon_app/
├─ app.py                 # point d'entrée (config, thème, comptes, routage)
├─ run.bat                # lancement Windows en un clic
├─ requirements.txt
├─ .streamlit/config.toml # thème Streamlit (couleurs, toolbar minimal)
├─ assets/
│  ├─ styles.css          # design system complet (variables, cartes, nav basse, connexion…)
│  └─ cache/              # images téléchargées (généré, ignoré par git)
├─ core/
│  ├─ config.py           # nom, chemins, devise (MAD), profil & compte de démo
│  ├─ auth.py             # comptes : inscription, connexion, multi-comptes, hachage
│  ├─ state.py            # état de session + persistance par compte
│  ├─ images.py           # visuels : cache disque + dégradés de secours
│  ├─ theme.py            # injection du CSS + détection des API Streamlit
│  ├─ components.py       # cartes, mosaïque, chips, carrousels, boutons…
│  ├─ nav.py              # barre de navigation basse + navigation
│  └─ router.py           # rend la page active
├─ data/
│  ├─ catalogue.py        # pièces, collections, stylistes, marques, quiz, défis…
│  ├─ countries.py        # tous les pays (nom français + drapeau)
│  └─ seed.py             # données de démonstration du compte
└─ views/
   ├─ auth.py             # écran de connexion / création de compte
   ├─ common.py           # helpers partagés (goûts, stats, aperçus de looks)
   ├─ home.py             # 🏠 Accueil
   ├─ explore.py          # 🔍 Explorer
   └─ account.py          # 👤 Mon compte
```

---

## 🧠 Comment étendre l'application

| Besoin | Où intervenir |
| --- | --- |
| Ajouter des pièces, marques, stylistes | `data/catalogue.py` (listes `ITEMS`, `BRANDS`, `STYLISTS`) |
| Changer les catégories du feed | `data/catalogue.py` → `CATEGORIES` |
| Ajouter un pays | `data/countries.py` → `COUNTRIES` |
| Changer la devise | `core/config.py` → `CURRENCY` + `format_price()` |
| Ajouter un onglet dans Explorer | `views/explore.py` → `TABS` + fonction dédiée |
| Modifier une carte produit | `core/components.py` → `product_card()` |
| Changer les couleurs, arrondis, typos | `assets/styles.css` → variables `:root` |
| Remplacer les photos | champ `photo` (identifiant Unsplash) ou `None` pour un dégradé |
| Brancher une vraie base / API | remplacer les fonctions utilitaires de `data/catalogue.py` |
| Persistance & comptes | `core/auth.py` + `core/state.py` — aujourd'hui JSON local |

Les images sont téléchargées une seule fois puis mises en cache dans `assets/cache/`.
**Hors connexion**, l'application reste élégante : chaque visuel est remplacé par un dégradé
généré à la volée (Pillow).

Les comptes, dressings, wishlists, looks, rendez-vous et points sont enregistrés dans
`data/user_store.json` (fichier non versionné) : ils survivent au rechargement.
Depuis **Mon compte → Modifier mon profil** : « Exemple de démo » charge un vestiaire complet,
« Vider mes données » repart d'un espace vide.
Pour passer en production, remplacer `core/auth.py` (et le stockage JSON) par une API + base de
données : le reste de l'application ne change pas.

---

## ☁️ Mettre en ligne (GitHub + Streamlit Community Cloud)

**1. Pousser le dossier sur GitHub**

```powershell
git init -b main
git add -A
git commit -m "Muse — application de mode (MAD, multi-comptes, mode modeste)"
git remote add origin https://github.com/fatimzahraebouyncha/Mon_App.git
git push -u origin main
```

> À la première connexion, une fenêtre GitHub s'ouvre dans le navigateur : connectez-vous et
> autorisez l'accès (rien à recopier).

**2. Déployer**

1. Ouvrez <https://share.streamlit.io> et connectez-vous avec GitHub.
2. **Create app** → **Deploy a public app from GitHub**.
3. Renseignez :
   - **Repository** : `fatimzahraebouyncha/Mon_App`
   - **Branch** : `main`
   - **Main file path** : `app.py`
4. **Deploy** : l'application est en ligne au bout d'une minute environ.

Chaque `git push` sur `main` redéploie automatiquement la nouvelle version.

**Bon à savoir en ligne**

- `data/user_store.json` (comptes, dressings, wishlists, points) est écrit **dans le conteneur** :
  il tient pendant la vie de l'application, mais repart de zéro à chaque redéploiement. Pour une
  vraie mise en production multi-utilisateurs, remplacez `core/auth.py` (et le stockage JSON) par
  une base de données — le reste de l'application ne change pas.
- Les photos sont téléchargées au premier affichage puis mises en cache dans le conteneur
  (hors connexion, les dégradés prennent le relais).
- Le compte de démonstration `sarah@muse.ma` / `muse` est créé automatiquement au premier
  démarrage.

---

## 🎨 Direction artistique

- **Modèle éditorial « modest chic »** : chaque page s'ouvre sur une grande photo de mode
  (bandeau plein cadre, voile dégradé pour la lisibilité) — recadrage intelligent sur le
  visage grâce à `crop=faces,entropy` d'Unsplash.
- Fond ivoire `#FFFDFB`, surfaces blanches, texte encre `#1A1512`.
- Accent terracotta `#C0563F`, touches dorées `#C9A227`.
- Titres **Fraunces** (serif éditorial), textes **Inter** (sans-serif).
- Cartes `border-radius: 20px`, ombres douces, micro-animations à l'arrivée sur une page.
- Photos : bannière d'accueil (`MODEST_PHOTOS["hero_modeste"]`), écran de connexion
  (`hero_monde`), couvertures de collections, stylistes et pièces — remplacer un identifiant
  Unsplash suffit à changer un visuel (`None` → dégradé généré).

Bonne exploration ✨
