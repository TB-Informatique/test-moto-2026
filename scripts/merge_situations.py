#!/usr/bin/env python3
"""Ajoute les QCM situations au questions.json (UTF-8, sans rebuild)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from situation_bank import all_items

ROOT = Path(__file__).resolve().parents[1]
QPATH = ROOT / "data/questions.json"
CRED = ROOT / "assets/img/situations/credits.json"
IMG = ROOT / "assets/img/situations"

FALLBACK = {
    "carrefour-giratoire": ["rondpoint", "carrefour"],
    "deux-roues-feu": ["feux", "moto-ville", "interfiles"],
    "cedez-inverse": ["cedez", "chaussee-etroite", "double-sens"],
    "interfiles": ["file-autoroute", "circulation-dense", "moto-ville"],
    "corridor": ["chantier", "travaux-panneau", "panne"],
    "radar-panneau": ["radar", "travaux-panneau"],
    "fin-autoroute": ["autoroute", "sortie"],
    "equip-pluie": ["pluie", "moto-route"],
    "gants-moto": ["casque", "moto-equipement"],
    "bottes-moto": ["casque", "moto-equipement"],
    "casque-ouvert": ["casque"],
    "frein-disque": ["pneu", "moto-garee"],
    "retro-moto": ["moto-garee", "casque"],
    "huile-moteur": ["chaine", "moto-garee"],
    "controle-technique": ["controle", "essence"],
    "alcool-controle": ["controle"],
    "telephone-volant": ["controle", "bouchon-ville"],
    "fatigue-autoroute": ["aire-service", "autoroute"],
    "eclairage-defaut": ["nuit"],
    "secours-accident": ["accident", "samu"],
    "gilet": ["gilet-secours", "triangle"],
    "rails": ["tram", "passage-pn"],
    "prioritaire": ["samu", "secours-accident"],
    "faune": ["animal"],
    "zone-nature": ["virage", "animal"],
    "pollution": ["bouchon-ville", "circulation-dense"],
    "priorite-droite": ["carrefour", "cedez"],
    "ligne-discontinue": ["ligne-continue", "marquage"],
    "stationnement-genant": ["parking", "double-file"],
    "porte-ouverte": ["pieton-ville", "parking"],
    "travaux-pieton": ["chantier", "travaux-panneau"],
    "velo-ville": ["velo"],
}


def resolve(slug: str, credits: dict) -> str | None:
    if slug in credits and (IMG / f"{slug}.jpg").exists():
        return slug
    for alt in FALLBACK.get(slug, []):
        if alt in credits and (IMG / f"{alt}.jpg").exists():
            return alt
    # last resort: any existing jpg
    return None


def main() -> None:
    credits = json.loads(CRED.read_text(encoding="utf-8")) if CRED.exists() else {}
    data = json.loads(QPATH.read_text(encoding="utf-8"))
    data["questions"] = [q for q in data["questions"] if not str(q.get("id", "")).startswith("sit-")]

    added = []
    missing = []
    for item in all_items():
        slug = resolve(item["slug"], credits)
        if not slug:
            missing.append(item["slug"])
            continue
        meta = credits[slug]
        q = {k: item[k] for k in ("id", "category", "theme", "question", "choices", "correct", "explanation", "multi")}
        q["image"] = meta["file"]
        q["imageAlt"] = item["imageAlt"]
        q["imageCredit"] = meta["credit"]
        added.append(q)

    data["questions"].extend(added)
    counts = Counter(q["category"] for q in data["questions"])
    for cat in data["categories"]:
        cat["count"] = counts.get(cat["id"], 0)

    QPATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("added", len(added), "missing slugs", missing)
    print("total", len(data["questions"]), dict(counts))


if __name__ == "__main__":
    main()
