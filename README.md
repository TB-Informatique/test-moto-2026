# Code Moto 2026

Site statique d'entraînement à l'**épreuve théorique moto (ETM) 2026**, plus des pages de pratique (trajectoires, plateau, contrôles).

**Site en ligne :** [https://tb-informatique.github.io/test-moto-2026/](https://tb-informatique.github.io/test-moto-2026/)

Questions **aléatoires**, mixte ou **par catégorie**. **Note à la fin**, **sans sauvegarde** (rien n'est stocké).

## Pages

| Page | Lien |
| --- | --- |
| Accueil | [index.html](https://tb-informatique.github.io/test-moto-2026/) |
| Tests / examen blanc | [quiz.html](https://tb-informatique.github.io/test-moto-2026/quiz.html) |
| Cours (9 thèmes ETM) | [apprendre.html](https://tb-informatique.github.io/test-moto-2026/apprendre.html) |
| Catalogue des panneaux | [panneaux.html](https://tb-informatique.github.io/test-moto-2026/panneaux.html) |
| Particularités moto | [particularites.html](https://tb-informatique.github.io/test-moto-2026/particularites.html) |
| Trajectoires de sécurité | [trajectoires.html](https://tb-informatique.github.io/test-moto-2026/trajectoires.html) |
| Plateau (hors circulation) | [plateau.html](https://tb-informatique.github.io/test-moto-2026/plateau.html) |
| Contrôles moto | [controles.html](https://tb-informatique.github.io/test-moto-2026/controles.html) |

Dépôt : [github.com/TB-Informatique/test-moto-2026](https://github.com/TB-Informatique/test-moto-2026)

## Lancer en local

Le `fetch` des JSON ne fonctionne pas en `file://` :

```bash
python3 -m http.server 8080
```

Puis : <http://127.0.0.1:8080>

## Données

- Questions : `data/questions.json` (items d'entraînement originaux, hors banque officielle)
- Panneaux : `data/signs.json` (titres IISR) + `assets/img/signs/`
- Images de signalisation : [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:SVG_road_signs_in_France)

Ne pas régénérer les JSON avec `scripts/build_data.py` (encodage corrompu). Pour réaligner catalogue et questions : `python3 scripts/audit_fix_signs.py`.

## GitHub Pages

Le site est publié depuis la branche `main` (racine du dépôt) :

[https://tb-informatique.github.io/test-moto-2026/](https://tb-informatique.github.io/test-moto-2026/)
