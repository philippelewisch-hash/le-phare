# Guide de génération quotidienne — Le Phare

Ce document est la spécification autonome utilisée par l'agent planifié qui publie une nouvelle édition chaque jour. Il doit rester lisible sans le contexte d'aucune conversation passée.

## Objectif

Produire une nouvelle édition datée du site « Le Phare », un journal d'actualité entièrement rédigé par IA, avec quatre rubriques : International, Politique intérieure (France), Culture, Science. Archiver l'édition précédente. Publier (commit + push).

## Étapes à exécuter, dans l'ordre

### 1. Déterminer la date du jour

Utiliser la date réelle du jour (fuseau Europe/Paris), format `YYYY-MM-DD` pour les chemins, et en toutes lettres français pour l'affichage (ex. « mercredi 5 août 2026 »).

Si une édition existe déjà pour cette date dans `manifest.json`, ne pas dupliquer : mettre à jour cette édition existante plutôt que d'en créer une nouvelle.

### 2. Rechercher l'actualité du jour

Faire une recherche web dédiée pour chacune des quatre rubriques :
- Politique internationale (conflits en cours, diplomatie, UE, grandes puissances)
- Politique intérieure française (gouvernement, Assemblée nationale, partis, réformes)
- Culture (littérature, cinéma, musique, expositions, prix)
- Science (découvertes, espace, santé, environnement)

Rédiger 2 à 4 articles originaux par rubrique (reformulation dans ses propres mots — jamais de copier-coller de plus de 15 mots consécutifs d'une source, jamais de paroles de chanson). Chaque article cite ses sources en bas avec des liens.

Ton journalistique, factuel, neutre. Pas de sensationnalisme. Si une info est incertaine ou controversée, le signaler.

**Avant de rédiger, appliquer impérativement la règle de vérification des sources décrite en fin de document.**

### 3. Créer le dossier d'archive du jour

Créer `editions/YYYY-MM-DD/` contenant 5 fichiers : `index.html`, `international.html`, `france.html`, `culture.html`, `science.html`.

Conventions pour ces fichiers (copier la structure d'une édition existante dans `editions/`, par exemple `editions/2026-08-05/`, et l'adapter) :
- `<link rel="stylesheet" href="../../style.css">`
- Le lien du logo « LE PHARE » dans le masthead pointe vers `../../index.html`
- La nav interne (La Une / International / Politique intérieure / Culture / Archives / Science) pointe vers les fichiers du même dossier, sauf « Archives » qui pointe vers `../../archives.html`
- Juste après `</nav>`, insérer la bannière `.archive-notice` (voir un fichier existant pour le HTML exact) avec la date du jour et les liens `../../index.html` (édition du jour) et `../../archives.html`
- Respecter les classes CSS existantes (`.article`, `.tag`, `.dek`, `.byline`, `.sources`, `.front-lead`, `.rubric-grid`, `.section-title`) — ne pas inventer de nouvelles classes sans les ajouter aussi à `style.css`
- Chaque article a `<p class="byline">Le Phare — Rédigé par IA</p>`

### 4. Mettre à jour les pages racine (l'édition « du jour »)

Écraser `index.html`, `international.html`, `france.html`, `culture.html`, `science.html` à la racine du dépôt avec le contenu de la nouvelle édition (identique au contenu de `editions/YYYY-MM-DD/`, mais avec les chemins relatifs habituels de la racine : `href="style.css"`, `href="index.html"`, etc., et SANS la bannière `.archive-notice`).

Mettre à jour la date affichée dans le bandeau du masthead (`Édition du <jour> <date>`) sur les 5 pages racine ET sur `archives.html`.

### 5. Mettre à jour `manifest.json`

Ajouter (ou mettre à jour si l'édition du jour existe déjà) une entrée en **tête de liste** (ordre antéchronologique) :

```json
{
  "date": "YYYY-MM-DD",
  "path": "editions/YYYY-MM-DD/index.html",
  "headline": "Titre du grand article international du jour",
  "summary": "Une phrase résumant les 4 sujets phares du jour, un par rubrique."
}
```

Ne jamais supprimer d'entrées existantes.

### 6. Régénérer `archives.html`

Reconstruire entièrement le bloc entre `<!-- EDITIONS-LIST-START -->` et `<!-- EDITIONS-LIST-END -->` à partir de `manifest.json`, dans l'ordre antéchronologique (plus récent en haut), un `.edition-row` par entrée :

```html
<div class="edition-row">
  <span class="edition-date">5 août 2026</span>
  <span class="edition-headline"><a href="editions/2026-08-05/index.html">Titre</a></span>
</div>
```

### 7. Éléments d'application mobile (PWA) — à préserver sur CHAQUE page racine

Le site est installable comme application sur téléphone (PWA). Sur les 6 pages racine (`index.html`, `international.html`, `france.html`, `culture.html`, `science.html`, `archives.html`), le `<head>` doit toujours contenir, en plus du `<title>` et du lien vers `style.css` :

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<link rel="manifest" href="app.webmanifest">
<meta name="theme-color" content="#1a1a1a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Le Phare">
<link rel="icon" href="icons/favicon.ico">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<script src="app.js" defer></script>
```

Juste après `</nav>` (la nav du haut) sur ces mêmes 6 pages, conserver la barre de navigation basse mobile, avec `class="active"` sur le lien de la page courante :

```html
<nav class="bottom-nav">
  <div class="wrap">
    <a href="index.html">La Une</a>
    <a href="international.html">Intl.</a>
    <a href="france.html">France</a>
    <a href="culture.html">Culture</a>
    <a href="science.html">Science</a>
    <a href="archives.html">Archives</a>
  </div>
</nav>
```

**Ne pas mettre ces deux liens dans le `<footer>`** — sur mobile, la barre de navigation basse fixe (`.bottom-nav`) recouvre le bas du pied de page, qui n'a pas de marge réservée pour elle (seul `<main>` en a une), rendant ces liens inaccessibles au clic. C'est un bug corrigé le 15 août 2026 : ils doivent être placés dans le `<header class="masthead">`, juste après le dernier paragraphe de présentation (`.ai-note` sur `index.html`, `.baseline` sur les 5 autres pages), avant la fermeture du `<div class="wrap">` :

```html
<p class="install-link install-link-top"><a href="installer.html">Installer Le Phare sur votre téléphone</a> · <a href="abonnement.html">Recevoir les annonces du Phare</a></p>
```

Ces éléments ne s'appliquent PAS aux pages archivées dans `editions/YYYY-MM-DD/` (elles restent de simples pages web, sans balises PWA).

### 7bis. Page `abonnement.html` et service d'inscription

Le fichier `abonnement.html` (formulaire d'inscription aux annonces, avec désinscription) est une page statique fixe : ne jamais la régénérer ni la modifier automatiquement. Le formulaire poste vers `https://lephare-stats.167.233.247.14.sslip.io/subscribe` (service externe, hors de ce dépôt) — ne pas toucher à cette URL.

### 8. Pixel de mesure d'audience (à inclure sur CHAQUE page, racine et édition archivée)

Juste avant `</body>`, sur chacune des 5 pages racine et des 5 pages de `editions/YYYY-MM-DD/`, insérer :

```html
<img src="https://lephare-stats.167.233.247.14.sslip.io/collect.gif?page=SLUG" width="1" height="1" style="position:absolute;visibility:hidden" alt="" loading="eager">
```

où `SLUG` vaut `accueil` (pour `index.html`), `international`, `france`, `culture`, `science` ou `archives` selon la page. Ne pas modifier cette URL. Vérifier aussi que le pied de page de chaque page racine et de `archives.html` contient bien la phrase : « Ce site mesure sa fréquentation (adresse IP, localisation approximative, page consultée) à des fins statistiques internes ; ces données ne sont ni publiées, ni partagées avec des tiers hormis le service de géolocalisation utilisé pour situer les visites sur une carte. » — si elle manque, l'ajouter à la fin du dernier paragraphe du `<footer>`.

### 9. Ne jamais toucher

- `style.css` (sauf si une nouvelle classe est strictement nécessaire — dans ce cas l'ajouter sans casser l'existant)
- Le contenu des dossiers `editions/` des jours précédents (ils sont figés définitivement)
- Ce fichier `GENERATION-GUIDE.md`
- L'URL du pixel de mesure d'audience
- Les fichiers `app.webmanifest`, `sw.js`, `app.js`, `installer.html`, `abonnement.html`, et le dossier `icons/`

### 10. Publier

```
git add -A
git commit -m "Édition du <date>"
git push
```

## Règle de vérification des sources

Cette règle a été ajoutée après une erreur réelle : un article publié le 11 août 2026 sur l'exécution de Marzieh Nieri en Iran omettait que son mari avait été tué durant l'altercation et qu'elle avait été condamnée pour meurtre. Rien n'était faux ; un élément essentiel manquait. L'article avait été rédigé à partir du seul résumé d'un moteur de recherche, sans que la source soit ouverte. Les règles ci-dessous visent ce type de défaillance.

### A. Ne jamais rédiger depuis un résumé seul

Un extrait de résultat de recherche ne suffit jamais à écrire un article. Pour chaque article, **ouvrir au moins une source réelle** (outil de récupération de page) et rédiger à partir de son contenu. Le résumé d'un moteur sert à repérer un sujet, pas à le traiter.

### B. Recoupement obligatoire — deux sources indépendantes

Deux sources indépendantes l'une de l'autre (pas deux reprises de la même dépêche) sont exigées pour :

- toute affaire judiciaire ou pénale, toute condamnation, toute personne nommément mise en cause
- tout bilan humain : morts, blessés, disparus, personnes déplacées
- toute accusation portée contre une personne, une organisation ou un État
- tout chiffre présenté comme un record, une statistique ou une évolution
- toute information concernant une personne privée

Si le recoupement est impossible, deux choix seulement : renoncer au sujet, ou l'écrire en attribuant explicitement l'information à son unique source (« selon X, seule source disponible à ce stade »).

**Le critère qui engendre cette liste** — et qui permet de l'étendre aux cas qu'elle ne prévoit pas : recouper dès que la source primaire est partie prenante des faits, ou qu'aucune institution n'a intérêt ni les moyens d'en restituer l'intégralité. Concrètement, c'est le cas lorsque l'auteur du communiqué est aussi l'auteur des faits (armée, police, entreprise mise en cause, gouvernement jugeant ses propres agents), lorsque l'État concerné ne publie ni statistiques ni motivations de jugement et que l'information ne circule donc que par des organisations engagées, ou lorsqu'une des parties conteste publiquement les faits. Si un sujet ne figure pas dans la liste ci-dessus mais relève de ce critère, le recouper quand même.

### C. Source unique admise, mais attribuée

Une source unique suffit lorsqu'elle est l'autorité primaire sur le fait rapporté : communiqué officiel, décision de justice publiée, publication scientifique, programmation d'un événement par son organisateur, données d'un institut de mesure. Dans ce cas, la nommer dans le corps du texte, et non seulement en pied d'article.

### D. Signaler les divergences plutôt que trancher

Lorsque deux sources donnent des versions ou des chiffres différents, **ne jamais choisir silencieusement la plus commode**. Exposer l'écart dans le texte et indiquer qui affirme quoi.

### E. Qualifier les sources engagées

Les organisations militantes, partis, gouvernements et groupes d'opposition peuvent être cités, mais leur nature doit être précisée au lecteur (« organisation liée à l'opposition en exil », « selon le ministère »). Ne jamais présenter leurs chiffres comme neutres.

### F. Chercher ce qui manque, pas seulement ce qui est faux

Avant de publier un article, se poser explicitement la question : *que s'est-il passé d'autre dans cette affaire que mon texte ne dit pas ?* Un récit cohérent et sourcé peut induire gravement en erreur par omission. C'est le cas le plus difficile à détecter et le plus fréquent.

### G. Corriger à visage découvert

Si une erreur est constatée après publication, ne jamais réécrire silencieusement. Corriger le texte et ajouter en tête d'article une mention datée précisant ce qui était erroné ou manquant, et ce qui a été modifié. Cette mention reste dans l'édition archivée.

## Ton, déontologie, transparence

- Chaque page garde sa mention « Rédigé par IA » et le pied de page rappelant que le site est une démonstration expérimentale, sans vérification humaine du fond, à recouper avec la presse professionnelle.
- Ne jamais présenter une information non vérifiée comme certaine.
- Toujours citer les sources utilisées en bas de chaque article.
