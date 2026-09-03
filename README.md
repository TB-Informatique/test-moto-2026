# test-moto-2026

Site statique d'entraînement à l'**épreuve théorique moto (ETM) 2026**.

- Questions **aléatoires**, mixte ou **par catégorie**
- **Note à la fin**, **sans sauvegarde** (rien n'est stocké)
- Pages de cours, catalogue de **panneaux**, particularités moto
- Images de signalisation : [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:SVG_road_signs_in_France)

## Lancer en local

Ouvrir le dossier avec un petit serveur HTTP (le `fetch` des JSON ne fonctionne pas en `file://`) :

```bash
python3 -m http.server 8080
```

Puis : <http://127.0.0.1:8080>

## GitHub Pages

Publier la branche `main` (racine du dépôt) comme site Pages.

Les titres officiels des panneaux sont dans `data/signs.json` (référentiel IISR).
Ne pas régénérer les JSON avec `scripts/build_data.py` : ce script a un encodage
corrompu. Pour réaligner catalogue et questions : `python3 scripts/audit_fix_signs.py`.

Les questions sont des items d'entraînement originaux, pas la banque officielle de l'examen.
