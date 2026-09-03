#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Réinjecte les QCM sit-* dans questions.json, sans photo scrapée."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from situation_bank import all_items

ROOT = Path(__file__).resolve().parents[1]
QPATH = ROOT / "data/questions.json"

# Schémas IISR déjà dans le catalogue uniquement.
SIGN_FOR = {
    "sit-c05": ("assets/img/signs/AB4.svg", "Panneau STOP (AB4)"),
    "sit-c06": ("assets/img/signs/AB3a.svg", "Cédez le passage (AB3a)"),
    "sit-c07": ("assets/img/signs/B15.svg", "Cédez le passage au sens inverse (B15)"),
    "sit-c16": ("assets/img/signs/B27a.svg", "Voie réservée aux transports en commun (B27a)"),
    "sit-c20": ("assets/img/signs/B1.svg", "Sens interdit (B1)"),
    "sit-c21": ("assets/img/signs/B30.svg", "Entrée d'une zone 30 (B30)"),
    "sit-s01": ("assets/img/signs/EB10.svg", "Entrée d'agglomération (EB10)"),
    "sit-s02": ("assets/img/signs/AK14.svg", "Autres dangers temporaire (AK14)"),
    "sit-s03": ("assets/img/signs/SR3a.svg", "Contrôle automatisé de vitesse (SR3a)"),
    "sit-s07": ("assets/img/signs/C208.svg", "Fin d'autoroute (C208)"),
    "sit-s08": ("assets/img/signs/A15b.svg", "Passage d'animaux sauvages (A15b)"),
    "sit-s11": ("assets/img/signs/SR53c.svg", "Corridor de sécurité (SR53c)"),
}
CREDIT = "Wikimedia Commons - signalisation routière française"


def main() -> None:
    data = json.loads(QPATH.read_text(encoding="utf-8"))
    data["questions"] = [q for q in data["questions"] if not str(q.get("id", "")).startswith("sit-")]

    added = []
    for item in all_items():
        q = {
            k: item[k]
            for k in ("id", "category", "theme", "question", "choices", "correct", "explanation", "multi")
        }
        mapped = SIGN_FOR.get(item["id"])
        if mapped:
            q["image"], q["imageAlt"] = mapped
            q["imageCredit"] = CREDIT
        added.append(q)

    data["questions"].extend(added)
    counts = Counter(q["category"] for q in data["questions"])
    for cat in data["categories"]:
        cat["count"] = counts.get(cat["id"], 0)

    QPATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("added", len(added), "with official svg", sum(1 for q in added if q.get("image")))
    print("total", len(data["questions"]), dict(counts))


if __name__ == "__main__":
    main()
