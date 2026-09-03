#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Télécharge de nouveaux SVG Wikimedia et les ajoute au catalogue + quiz."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNS_DIR = ROOT / "assets" / "img" / "signs"
CREDIT = "Wikimedia Commons - signalisation routière française"
UA = "CodeMoto2026/1.0 (pedagogical ETM trainer; github.com/TB-Informatique/test-moto-2026)"

# code -> (family, title, detail, wikimedia filenames to try)
NEW: dict[str, tuple[str, str, str, list[str]]] = {
    # --- Danger : 29e + variantes IISR ---
    "A15a2": (
        "danger",
        "Passage d'animaux domestiques (bovins)",
        "A15a2 : vaches / bovins susceptibles de traverser. Même réflexe que A15a1 : ralentir, éviter l'écart brutal.",
        ["France road sign A15a2.svg"],
    ),
    "A21b": (
        "danger",
        "Débouché de cyclistes venant de gauche",
        "A21b : cyclistes pouvant déboucher depuis la gauche. Laisser de l'espace, allure réduite.",
        ["France road sign A21b.svg"],
    ),
    # --- Prescription B manquantes ---
    "B1j": (
        "interdiction",
        "Rappel de sens interdit sur bretelle",
        "B1j : rappel d'interdiction à contresens sur bretelle d'autoroute. Ne jamais s'y engager.",
        ["France road sign B1j.svg"],
    ),
    "B6a2": (
        "interdiction",
        "Stationnement interdit du 1er au 15",
        "B6a2 : côté concerné interdit du 1er au 15 du mois. Une moto y stationnée est verbalisable.",
        ["France road sign B6a2.svg"],
    ),
    "B6a3": (
        "interdiction",
        "Stationnement interdit du 16 à la fin du mois",
        "B6a3 : côté concerné interdit du 16 à la fin du mois.",
        ["France road sign B6a3.svg"],
    ),
    "B6b1": (
        "interdiction",
        "Entrée d'une zone à stationnement interdit",
        "B6b1 : zone entière à stationnement interdit, pas seulement le bord du panneau.",
        ["France road sign B6b1.svg"],
    ),
    "B6b3": (
        "interdiction",
        "Entrée d'une zone à stationnement à durée limitée (disque)",
        "B6b3 : dans la zone, stationner seulement la durée indiquée, disque visible.",
        ["France road sign B6b3.svg"],
    ),
    "B6b4": (
        "interdiction",
        "Entrée d'une zone à stationnement payant",
        "B6b4 : zone payante. Le panneau C1c localise un emplacement payant ponctuel.",
        ["France road sign B6b4.svg"],
    ),
    "B9c": (
        "interdiction",
        "Accès interdit aux véhicules à traction animale",
        "B9c : pictogramme attelage. Une moto n'est pas visée.",
        ["France road sign B9c.svg"],
    ),
    "B9e": (
        "interdiction",
        "Accès interdit aux voitures à bras",
        "B9e : voitures à bras. Ce n'est pas l'interdiction moto (B9h).",
        ["France road sign B9e.svg"],
    ),
    "B9i": (
        "interdiction",
        "Accès interdit aux véhicules tractant une caravane",
        "B9i : caravane / remorque > 250 kg. Une moto solo n'est pas visée.",
        ["France road sign B9i.svg"],
    ),
    "B10a": (
        "interdiction",
        "Limitation de longueur",
        "B10a : accès interdit si la longueur, chargement compris, dépasse la valeur. Une moto passe.",
        ["France road sign B10a.svg"],
    ),
    "B13a": (
        "interdiction",
        "Limitation de charge à l'essieu",
        "B13a : poids max sur un essieu. Concerne surtout les PL, pas une moto.",
        ["France road sign B13a.svg"],
    ),
    "B14-30": (
        "interdiction",
        "Limitation de vitesse à 30 km/h",
        "B14-30 : 30 km/h max à partir du panneau (hors logique de zone 30, qui est le B30).",
        ["France road sign B14 (30).svg", "B14 (30).svg"],
    ),
    "B14-70": (
        "interdiction",
        "Limitation de vitesse à 70 km/h",
        "B14-70 : 70 km/h max. Fréquent avant un danger ou en travaux.",
        ["France road sign B14 (70).svg", "B14 (70).svg"],
    ),
    "B15": (
        "interdiction",
        "Cédez le passage au sens inverse",
        "B15 : rond à flèches, vous devez laisser passer le sens opposé dans le rétrécissement. Le carré bleu C18 vous donne au contraire la priorité.",
        ["France road sign B15.svg"],
    ),
    "B17": (
        "interdiction",
        "Intervalle minimal entre véhicules",
        "B17 : garder au moins la distance indiquée. Utile en descente, tunnel, ou convoi.",
        ["France road sign B17.svg"],
    ),
    "B18c": (
        "interdiction",
        "Accès interdit aux TMD (toutes matières dangereuses)",
        "B18c : toutes marchandises dangereuses signalées TMD. Plus large que B18a (explosifs) ou B18b (polluants).",
        ["France road sign B18c.svg"],
    ),
    "B21-2": (
        "obligation",
        "Obligation de tourner à gauche avant le panneau",
        "B21-2 : flèche horizontale vers la gauche. Tourner avant le panneau.",
        ["France road sign B21-2.svg"],
    ),
    "B21a2": (
        "obligation",
        "Contournement obligatoire par la gauche",
        "B21a2 : passer à gauche de l'obstacle. Le passage à droite est le B21a1.",
        ["France road sign B21a2.svg"],
    ),
    "B21c1": (
        "obligation",
        "Direction obligatoire à droite",
        "B21c1 : à la prochaine intersection, tourner à droite.",
        ["France road sign B21c1.svg"],
    ),
    "B21c2": (
        "obligation",
        "Direction obligatoire à gauche",
        "B21c2 : à la prochaine intersection, tourner à gauche.",
        ["France road sign B21c2.svg"],
    ),
    "B21d1": (
        "obligation",
        "Directions obligatoires : tout droit ou à droite",
        "B21d1 : tout droit ou droite, pas à gauche.",
        ["France road sign B21d1.svg"],
    ),
    "B21d2": (
        "obligation",
        "Directions obligatoires : tout droit ou à gauche",
        "B21d2 : tout droit ou gauche, pas à droite.",
        ["France road sign B21d2.svg"],
    ),
    "B21e": (
        "obligation",
        "Directions obligatoires : à droite ou à gauche",
        "B21e : interdiction d'aller tout droit. Droite ou gauche seulement.",
        ["France road sign B21e.svg"],
    ),
    "B22c": (
        "obligation",
        "Chemin obligatoire pour cavaliers",
        "B22c : obligatoire pour les cavaliers. Une moto n'a pas à l'emprunter.",
        ["France road sign B22c.svg"],
    ),
    "B25": (
        "obligation",
        "Vitesse minimale obligatoire (ici 30 km/h)",
        "B25 : rond bleu, vitesse minimale. Ce n'est pas une limitation (B14, fond blanc cerclé de rouge).",
        ["France road sign B25 (30).svg"],
    ),
    "B27b": (
        "obligation",
        "Voie réservée aux tramways",
        "B27b : voie de tram. Une moto n'y circule pas.",
        ["France road sign B27b.svg"],
    ),
    "B34": (
        "interdiction",
        "Fin d'interdiction de dépasser (B3)",
        "B34 : fin du B3 (tous véhicules à moteur). Le B34a ne lève que l'interdiction faite aux PL.",
        ["France road sign B34.svg"],
    ),
    "B35": (
        "interdiction",
        "Fin d'interdiction des signaux sonores",
        "B35 : le klaxon redevient autorisé (hors agglomération, selon le code).",
        ["France road sign B35.svg"],
    ),
    "B39": (
        "interdiction",
        "Fin d'interdiction indiquée sur le panneau",
        "B39 : lève l'interdiction écrite sur un B19.",
        ["France road sign B39.svg"],
    ),
    "B43": (
        "obligation",
        "Fin de vitesse minimale obligatoire",
        "B43 : fin du B25. On peut à nouveau rouler plus lentement si le trafic l'impose.",
        ["France road sign B43 (30).svg"],
    ),
    "B45b": (
        "obligation",
        "Fin de voie réservée aux tramways",
        "B45b : fin du B27b.",
        ["France road sign B45b.svg"],
    ),
    "B49": (
        "obligation",
        "Fin d'obligation indiquée sur le panneau",
        "B49 : lève l'obligation écrite sur un B29.",
        ["France road sign B49.svg"],
    ),
    "B50a": (
        "interdiction",
        "Sortie de zone à stationnement interdit",
        "B50a : fin de la zone B6b1. Les règles générales de stationnement reprennent.",
        ["France road sign B50a.svg"],
    ),
    "B54": (
        "obligation",
        "Entrée d'une aire piétonne",
        "B54 : aire piétonne. Circulation moto interdite sauf riverains / livraison aux horaires, à allure piétonne.",
        ["France road sign B54.svg"],
    ),
    "B55": (
        "obligation",
        "Sortie d'une aire piétonne",
        "B55 : fin de l'aire piétonne. Les règles générales reprennent.",
        ["France road sign B55.svg"],
    ),
    "B56": (
        "interdiction",
        "Entrée de zone à circulation restreinte (ZCR)",
        "B56 : ZCR / ZFE selon arrêtés locaux. Vérifier si votre moto y est autorisée (Crit'Air).",
        ["France road sign B56.svg"],
    ),
    "B57": (
        "interdiction",
        "Sortie de zone à circulation restreinte",
        "B57 : fin de ZCR.",
        ["France road sign B57.svg"],
    ),
    "B58": (
        "obligation",
        "Entrée de zone d'équipements hivernaux",
        "B58 : pneus hiver ou chaînes obligatoires dans la zone, période hivernale. À moto, souvent mieux de ne pas partir.",
        ["France road sign B58.svg"],
    ),
    "B59": (
        "obligation",
        "Sortie de zone d'équipements hivernaux",
        "B59 : fin de l'obligation B58.",
        ["France road sign B59.svg"],
    ),
    # --- Indication C ---
    "C1c": (
        "indication",
        "Lieu aménagé pour le stationnement payant",
        "C1c : emplacement payant. Le C1b est le stationnement à durée limitée (disque).",
        ["France road sign C1c.svg"],
    ),
    "C3": (
        "indication",
        "Risque d'incendie",
        "C3 : risque d'incendie (forêt, friches). Ne pas jeter de cigarette, pas de feu.",
        ["France road sign C3.svg"],
    ),
    "C4b": (
        "indication",
        "Fin de vitesse conseillée",
        "C4b : la vitesse conseillée C4a cesse. La limitation réglementaire reste.",
        ["France road sign C4b (50).svg"],
    ),
    "C6": (
        "indication",
        "Arrêt d'autobus",
        "C6 : arrêt de bus. S'arrêter ou stationner dessus est interdit (marquage).",
        ["France road sign C6.svg"],
    ),
    "C9": (
        "indication",
        "Station d'autopartage",
        "C9 : places réservées aux véhicules labellisés autopartage.",
        ["France road sign C9.svg"],
    ),
    "C13c": (
        "indication",
        "Impasse avec issue piétonne",
        "C13c : pas d'issue pour une moto, seulement pour les piétons.",
        ["France road sign C13c.svg"],
    ),
    "C13d": (
        "indication",
        "Impasse avec issue piétons et cyclistes",
        "C13d : issue pour piétons et vélos, pas pour une moto.",
        ["France road sign C13d.svg"],
    ),
    "C20b": (
        "indication",
        "Traversée de voie de bus",
        "C20b : bus susceptibles de traverser. Ce n'est pas le tram (C20c) ni le passage piéton (C20a).",
        ["France road sign C20b.svg"],
    ),
    "C23": (
        "indication",
        "Stationnement réglementé pour caravanes",
        "C23 : emplacement pour caravanes / camping-cars, pas un parking moto générique.",
        ["France road sign C23.svg"],
    ),
    "C26b": (
        "indication",
        "Voie de détresse à gauche",
        "C26b : voie d'arrêt d'urgence en descente, côté gauche. C26a est à droite. Ce n'est pas une « fin » de voie.",
        ["France road sign C26b.svg"],
    ),
    "C62": (
        "indication",
        "Présignalisation d'une borne de ticket de péage",
        "C62 : avant un péage, annonce la borne de retrait de ticket. L'issue de secours est le CE30a / CE30b.",
        ["France road sign C62.svg"],
    ),
    "C64a": (
        "indication",
        "Paiement auprès d'un péagiste",
        "C64a : voie de péage avec un agent. Ce n'est pas une issue de secours (CE30a / CE30b).",
        ["France road sign C64a.svg"],
    ),
    "C108": (
        "indication",
        "Fin de route à accès réglementé",
        "C108 : fin du C107 (voie express). La limitation générale reprend.",
        ["France road sign C108.svg"],
    ),
    "C115": (
        "indication",
        "Voie verte",
        "C115 : voie verte, réservée aux usages non motorisés. Une moto n'y circule pas.",
        ["France road sign C115.svg"],
    ),
    "C116": (
        "indication",
        "Fin de voie verte",
        "C116 : fin de la voie verte C115.",
        ["France road sign C116.svg"],
    ),
    "C208": (
        "indication",
        "Fin d'autoroute",
        "C208 : fin du régime autoroutier (C207). Adapter vitesse et placement, souvent 110 puis 80.",
        ["France road sign C208.svg"],
    ),
    # --- Services ---
    "CE1": (
        "service",
        "Poste de secours",
        "CE1 : croix rouge. Poste de secours à proximité. En accident, 112 reste le réflexe. Ce n'est pas une station-service (CE15a).",
        ["France road sign CE1.svg"],
    ),
    "CE2a": (
        "service",
        "Poste d'appel d'urgence",
        "CE2a : borne SOS. En cas d'accident sur autoroute ou voie rapide, c'est le moyen privilégié pour alerter. Ce n'est pas un restaurant (CE16).",
        ["France road sign CE2a.svg"],
    ),
    "CE3a": (
        "service",
        "Informations touristiques",
        "CE3a : informations relatives aux services ou activités touristiques (point « i »). L'hôtel est le CE17.",
        ["France road sign CE3a.svg"],
    ),
    "CE4a": (
        "service",
        "Terrain de camping pour tentes",
        "CE4a : pictogramme tente. Camping pour tentes. Ce n'est pas un point d'information (CE3a).",
        ["France road sign CE4a.svg"],
    ),
    "CE12": (
        "service",
        "Toilettes ouvertes au public",
        "CE12 : pictogrammes homme et femme. Sanitaires publics. Le poste de secours est le CE1.",
        ["France road sign CE12.svg"],
    ),
    "CE15a": (
        "service",
        "Poste de carburant ouvert 7j/7 et 24h/24",
        "CE15a : station-service 24/24. Utile pour anticiper la réserve. Le camping tentes est le CE4a.",
        ["France road sign CE15a.svg"],
    ),
    "CE18": (
        "service",
        "Débit de boissons ou collations",
        "CE18 : bar / snack ouvert 7j/7. Ce ne sont pas des toilettes (CE12).",
        ["France road sign CE18.svg"],
    ),
    "CE27": (
        "service",
        "Point de détente",
        "CE27 : aire de repos / détente. La recharge électrique est le CE15i.",
        ["France road sign CE27.svg"],
    ),
    # --- Panonceaux (59 au total IISR ; sélection utile moto) ---
    "M1": (
        "panonceau",
        "Panonceau de distance",
        "M1 : le danger ou la prescription se trouve à la distance indiquée.",
        ["France road sign M1.svg"],
    ),
    "M2": (
        "panonceau",
        "Panonceau d'étendue",
        "M2 : la prescription s'applique sur la longueur indiquée.",
        ["France road sign M2.svg"],
    ),
    "M3a1": (
        "panonceau",
        "Panonceau de direction (flèche)",
        "M3a1 : précise la direction concernée par le panneau principal.",
        ["France road sign M3a1.svg"],
    ),
    "M4a": (
        "panonceau",
        "Panonceau véhicules de moins de 3,5 t",
        "M4a : pictogramme voiture. Le panneau principal s'applique aux véhicules légers (PTAC < 3,5 t). Les motos sont le M4c.",
        ["France road sign M4a.svg"],
    ),
    "M4b": (
        "panonceau",
        "Panonceau transports en commun",
        "M4b : pictogramme bus. S'applique aux transports en commun. Les cycles sont le M4d1.",
        ["France road sign M4b.svg"],
    ),
    "M4c": (
        "panonceau",
        "Panonceau motocyclettes",
        "M4c : pictogramme moto. Le panneau principal ne vise alors que les motocyclettes.",
        ["France road sign M4c.svg"],
    ),
    "M4f": (
        "panonceau",
        "Panonceau de tonnage",
        "M4f : l'interdiction (souvent B8) ne vise que les véhicules au-dessus du tonnage indiqué.",
        ["France road sign M4f.svg"],
    ),
    "M5": (
        "panonceau",
        "Panonceau de distance jusqu'à l'arrêt",
        "M5 : distance entre le signal et l'endroit où s'arrêter (STOP ou cédez-le-passage).",
        ["France road sign M5.svg"],
    ),
    "M6a": (
        "panonceau",
        "Panonceau de mise en fourrière",
        "M6a : pictogramme dépanneuse. Arrêt ou stationnement gênant, véhicule susceptible d'être mis en fourrière.",
        ["France road sign M6a.svg"],
    ),
    "M9d": (
        "panonceau",
        "Passage pour piétons surélevé",
        "M9d : complète un passage piéton (C20a / A13b) : le passage est surélevé. Ce n'est pas un « rappel ».",
        ["France road sign M9d.svg"],
    ),
    # --- Type SR (info sécurité routière) ---
    "SR3a": (
        "securite",
        "Contrôle automatisé de vitesse (annonce)",
        "SR3a : zone où la vitesse est contrôlée par radar. Ce n'est pas une limitation : le B14 ou la règle générale s'applique.",
        ["France road sign SR3a.svg"],
    ),
    "SR3d": (
        "securite",
        "Zone de contrôle",
        "SR3d : zone de contrôle (vitesse, voies réservées ou bruit selon le panonceau associé).",
        ["France road sign SR3d.svg"],
    ),
    "SR53a": (
        "securite",
        "Corridor de sécurité : ralentissez",
        "SR53a (arrêté 4 avril 2025) : véhicule arrêté sur BAU / accotement → ralentir. 1er des 3 panneaux, espacés de 300 m.",
        ["FR Road sign SR53a.svg"],
    ),
    "SR53b": (
        "securite",
        "Corridor de sécurité : changez de voie",
        "SR53b : si vous le pouvez, clignotant et changement de voie pour vous éloigner du véhicule arrêté.",
        ["FR Road sign SR53b.svg"],
    ),
    "SR53c": (
        "securite",
        "Respectez le corridor de sécurité",
        "SR53c : règle R.412-11-1. Ralentir, s'éloigner, changer de voie. Les 3 panneaux SR53 sont indissociables.",
        ["FR Road sign SR53c.svg"],
    ),
    "SR-interfile": (
        "securite",
        "Rappel des règles d'inter-files",
        "Panneau pédagogique rappelant l'inter-files (files de gauche, 50 km/h max). Ce n'est pas une autorisation en ville.",
        ["France road sign SR-interfile.svg"],
    ),
    # --- Temporaires (fond jaune) ---
    "AK4": (
        "temporaire",
        "Chaussée glissante (temporaire)",
        "AK4 : danger temporaire, fond jaune. Gravillons, pluie de chantier, film gras. Allure réduite, moto droite.",
        ["France road sign AK4.svg"],
    ),
    "AK14": (
        "temporaire",
        "Autres dangers (temporaire)",
        "AK14 : danger temporaire non pictogrammé. Un panonceau KM9 précise souvent (gravillons, boue…).",
        ["France road sign AK14.svg"],
    ),
    "AK17": (
        "temporaire",
        "Feux tricolores (temporaire)",
        "AK17 : feux de chantier. Anticiper un orange / rouge, surtout si le sol est frais.",
        ["France road sign AK17.svg"],
    ),
    "AK30": (
        "temporaire",
        "Accident (temporaire)",
        "AK30 : accident. Ralentir, corridor de sécurité si un véhicule est sur le bord, pas de rubbernecking.",
        ["France road sign AK30.svg"],
    ),
}

FIX_EXISTING = {
    "C1b": (
        "indication",
        "Lieu aménagé pour le stationnement à durée limitée (disque)",
        "C1b (IISR) : stationnement gratuit à durée limitée, contrôle par disque. Le payant est le C1c.",
    ),
    "C5": (
        "indication",
        "Station de taxis",
        "C5 : emplacement de taxis. Ce n'est pas le stationnement payant (C1c).",
    ),
    "A9": (
        "danger",
        "Débouché de transports en commun",
        "A9 historique (bus / tram). L'IISR distingue désormais A9a (bus) et A9b (tram). Rails : franchir perpendiculairement, sans freiner.",
    ),
}

FAMILIES = {
    "danger": "Danger",
    "priorite": "Priorité",
    "interdiction": "Interdiction",
    "obligation": "Obligation",
    "indication": "Indication",
    "service": "Services",
    "localisation": "Localisation",
    "panonceau": "Panonceaux",
    "securite": "Sécurité routière",
    "temporaire": "Temporaires",
}

DISTRACTORS = [
    "Sens interdit",
    "Stop",
    "Cédez le passage",
    "Limitation de vitesse à 50 km/h",
    "Accès interdit aux motocyclettes",
    "Début d'autoroute",
    "Entrée d'une zone 30",
    "Passage pour piétons",
    "Fin de toutes les interdictions précédemment signalées",
    "Circulation dans les deux sens",
    "Voie réservée aux bus",
    "Stationnement interdit",
    "Fin d'autoroute",
    "Corridor de sécurité : ralentissez",
]


def api_file_url(filename: str) -> str | None:
    title = "File:" + filename
    qs = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        }
    )
    req = urllib.request.Request(
        f"https://commons.wikimedia.org/w/api.php?{qs}",
        headers={"User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if page.get("missing") is not None:
            return None
        infos = page.get("imageinfo") or []
        if infos:
            return infos[0].get("url")
    return None


def download(filename: str, dest: Path) -> bool:
    url = api_file_url(filename)
    if not url:
        return False
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())
    return dest.stat().st_size > 200


def fetch_all() -> list[str]:
    SIGNS_DIR.mkdir(parents=True, exist_ok=True)
    ok: list[str] = []
    failed: list[str] = []
    # Also refresh C1b from Wikimedia so it matches IISR (disque, not payant)
    extras = {"C1b": ["France road sign C1b.svg"]}
    todo = {**{c: NEW[c][3] for c in NEW}, **extras}
    for i, (code, names) in enumerate(todo.items(), 1):
        dest = SIGNS_DIR / f"{code}.svg"
        got = False
        for name in names:
            try:
                if download(name, dest):
                    print(f"  OK {code:12} ← {name}")
                    got = True
                    break
            except Exception as exc:
                print(f"  .. {code} {name}: {exc}")
            time.sleep(0.15)
        if got:
            ok.append(code)
        else:
            failed.append(code)
            print(f"  FAIL {code}")
        if i % 8 == 0:
            time.sleep(0.4)
    print(f"téléchargés {len(ok)}, échecs {failed}")
    return [c for c in NEW if c in ok and (SIGNS_DIR / f"{c}.svg").exists()]


def merge_catalog(available: list[str]) -> int:
    path = ROOT / "data" / "signs.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    by_code = {s["code"]: s for s in data["signs"]}
    for code, (family, title, detail) in FIX_EXISTING.items():
        if code in by_code:
            by_code[code]["family"] = family
            by_code[code]["title"] = title
            by_code[code]["detail"] = detail
    added = 0
    for code in available:
        family, title, detail, _ = NEW[code]
        obj = {
            "code": code,
            "family": family,
            "title": title,
            "detail": detail,
            "image": f"assets/img/signs/{code}.svg",
        }
        if code in by_code:
            by_code[code] = obj
        else:
            data["signs"].append(obj)
            by_code[code] = obj
            added += 1
    data["families"] = FAMILIES
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalogue : {len(data['signs'])} panneaux (+{added})")
    return len(data["signs"])


def make_ident(qid: str, code: str) -> dict:
    family, title, detail, _ = NEW[code]
    choices_txt = [title]
    for d in DISTRACTORS:
        if d != title and d not in choices_txt:
            choices_txt.append(d)
        if len(choices_txt) == 4:
            break
    return {
        "id": qid,
        "category": "signalisation",
        "theme": "R",
        "question": "Que signifie ce panneau ?",
        "choices": [{"id": letter, "text": t} for letter, t in zip("abcd", choices_txt)],
        "correct": ["a"],
        "explanation": detail,
        "multi": False,
        "image": f"assets/img/signs/{code}.svg",
        "imageAlt": title,
        "imageCredit": CREDIT,
    }


def patch_questions(available: list[str]) -> None:
    path = ROOT / "data" / "questions.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    qs = data["questions"]
    by_id = {q["id"]: q for q in qs}

    # Fix C1b identification
    if "sig-083" in by_id:
        q = by_id["sig-083"]
        title = FIX_EXISTING["C1b"][1]
        for c in q["choices"]:
            if c["id"] in q["correct"]:
                c["text"] = title
            elif c["text"] == title:
                c["text"] = "Lieu aménagé pour le stationnement payant"
        q["explanation"] = FIX_EXISTING["C1b"][2]
        q["imageAlt"] = title

    extra_behavior = [
        {
            "id": "sig-corridor-1",
            "category": "signalisation",
            "theme": "R",
            "question": "Ces trois panneaux SR53 (arrêté d'avril 2025) rappellent le corridor de sécurité. Que devez-vous faire ?",
            "choices": [
                {"id": "a", "text": "Ralentir, vous éloigner, changer de voie si possible (R.412-11-1)"},
                {"id": "b", "text": "Accélérer pour dépasser vite le véhicule arrêté"},
                {"id": "c", "text": "Vous arrêter sur la bande d'arrêt d'urgence pour aider"},
                {"id": "d", "text": "Klaxonner et rester collé à droite"},
            ],
            "correct": ["a"],
            "explanation": "SR53a/b/c, indissociables, tous les 300 m. Ralentir, s'écarter, changer de voie si on le peut. Obligatoire dès qu'un véhicule a les feux de détresse ou spéciaux sur le bord.",
            "multi": False,
            "image": "assets/img/signs/SR53c.svg",
            "imageAlt": "Respectez le corridor de sécurité",
            "imageCredit": CREDIT,
        },
        {
            "id": "sig-m4a-1",
            "category": "signalisation",
            "theme": "R",
            "question": "Un panneau de prescription est complété par ce panonceau M4a. À qui s'applique-t-il ?",
            "choices": [
                {"id": "a", "text": "Aux véhicules de moins de 3,5 t"},
                {"id": "b", "text": "À tous les véhicules"},
                {"id": "c", "text": "Aux cycles seulement"},
                {"id": "d", "text": "Aux motocyclettes uniquement"},
            ],
            "correct": ["a"],
            "explanation": "M4a = pictogramme voiture, véhicules de PTAC < 3,5 t. Les motocyclettes sont le M4c.",
            "multi": False,
            "image": "assets/img/signs/M4a.svg",
            "imageAlt": "Panonceau véhicules de moins de 3,5 t",
            "imageCredit": CREDIT,
        },
        {
            "id": "sig-b25-1",
            "category": "signalisation",
            "theme": "R",
            "question": "Ce panneau bleu indique :",
            "choices": [
                {"id": "a", "text": "Une vitesse minimale obligatoire"},
                {"id": "b", "text": "Une limitation maximale à 30 km/h"},
                {"id": "c", "text": "Une vitesse conseillée"},
                {"id": "d", "text": "L'entrée d'une zone 30"},
            ],
            "correct": ["a"],
            "explanation": "B25 = rond bleu = obligation (vitesse mini). Le max 30 est un B14 fond blanc, la zone 30 est le rectangle B30.",
            "multi": False,
            "image": "assets/img/signs/B25.svg",
            "imageAlt": "Vitesse minimale obligatoire",
            "imageCredit": CREDIT,
        },
        {
            "id": "sig-c208-1",
            "category": "circulation",
            "theme": "C",
            "question": "Ce panneau annonce :",
            "choices": [
                {"id": "a", "text": "La fin d'autoroute : le régime 130 km/h cesse"},
                {"id": "b", "text": "Le début d'autoroute"},
                {"id": "c", "text": "Une route à accès réglementé (voie express)"},
                {"id": "d", "text": "Un tunnel"},
            ],
            "correct": ["a"],
            "explanation": "C208 = autoroute barrée = fin. C207 = début. C107/C108 = accès réglementé.",
            "multi": False,
            "image": "assets/img/signs/C208.svg",
            "imageAlt": "Fin d'autoroute",
            "imageCredit": CREDIT,
        },
    ]

    existing = {q["id"] for q in qs}
    added = 0
    n = 200
    for code in available:
        qid = f"sig-{n}"
        while qid in existing:
            n += 1
            qid = f"sig-{n}"
        qs.append(make_ident(qid, code))
        existing.add(qid)
        added += 1
        n += 1
    for q in extra_behavior:
        if q["id"] not in existing and Path(ROOT / q["image"]).exists():
            qs.append(q)
            existing.add(q["id"])
            added += 1

    counts: dict[str, int] = {}
    for q in qs:
        counts[q["category"]] = counts.get(q["category"], 0) + 1
    for cat in data["categories"]:
        cat["count"] = counts.get(cat["id"], 0)

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"questions : {len(qs)} (ajoutées {added})")


if __name__ == "__main__":
    available = fetch_all()
    merge_catalog(available)
    patch_questions(available)
