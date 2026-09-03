#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aligne catalogue + questions sur les codes officiels IISR (Wikimedia)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREDIT = "Wikimedia Commons - signalisation routière française"

# code -> (family, title, detail)
OFFICIAL: dict[str, tuple[str, str, str]] = {
    "A1a": ("danger", "Virage à droite", "Annonce un virage serré vers la droite. À moto : ralentir avant le virage, se placer à l'extérieur, regarder la sortie."),
    "A1b": ("danger", "Virage à gauche", "Annonce un virage serré vers la gauche. Risque de collision avec un véhicule en sens inverse si la trajectoire coupe l'axe."),
    "A1c": ("danger", "Succession de virages, premier à droite", "Série de virages dont le premier est à droite. Adapter l'allure dès le premier, sans accélérer entre deux courbes."),
    "A1d": ("danger", "Succession de virages, premier à gauche", "Série de virages dont le premier est à gauche. La visibilité et l'adhérence peuvent changer d'une courbe à l'autre."),
    "A2a": ("danger", "Cassis ou dos-d'âne", "Déformation de la chaussée. À moto, lever légèrement les fesses, relâcher les freins et garder l'assiette stable."),
    "A2b": ("danger", "Ralentisseur de type dos-d'âne", "Ralentisseur volontaire. Franchir droit, sans angle, à allure réduite pour ne pas décoller la roue avant."),
    "A3": ("danger", "Chaussée rétrécie", "La chaussée se rétrécit des deux côtés. Anticiper, serrer sa droite et éviter les dépassements."),
    "A3a": ("danger", "Chaussée rétrécie par la droite", "Rétrécissement côté droit. Un obstacle ou un véhicule peut vous contraindre à vous déporter."),
    "A3b": ("danger", "Chaussée rétrécie par la gauche", "Rétrécissement côté gauche. Surveiller le trafic opposé et garder une marge de sécurité."),
    "A4": ("danger", "Chaussée glissante", "Adhérence réduite (pluie, verglas, gravillons, feuilles). Allonger les distances et éviter les à-coups."),
    "A6": ("danger", "Pont mobile", "Le pont peut s'ouvrir. S'arrêter si le feu ou la barrière l'impose, jamais s'engager au dernier moment."),
    "A7": ("danger", "Passage à niveau avec barrières", "Voie ferrée protégée par des barrières. Ne jamais s'engager si le feu clignote ou si les barrières bougent."),
    "A8": ("danger", "Passage à niveau sans barrières", "Voie ferrée sans barrière. S'arrêter, regarder et écouter avant de s'engager. Un train peut arriver vite."),
    "A9": ("danger", "Débouché de véhicules des transports en commun", "A9 : bus ou tram susceptibles de déboucher. Les rails de tram sont très glissants : les franchir le plus perpendiculairement possible, sans freiner dessus."),
    "A13a": ("danger", "Endroit fréquenté par les enfants", "Proximité d'une école, d'un parc ou d'un arrêt. Réduire l'allure : un enfant peut surgir."),
    "A13b": ("danger", "Passage pour piétons", "Annonce un passage piéton. Un piéton engagé est prioritaire."),
    "A14": ("danger", "Autres dangers", "Danger non précisé par un autre panneau. Le panonceau éventuellement associé précise le risque."),
    "A15a1": ("danger", "Passage d'animaux domestiques", "Animaux de ferme susceptibles de traverser. Freiner progressivement, klaxonner avec mesure si besoin."),
    "A15b": ("danger", "Passage d'animaux sauvages", "Risque de collision avec un animal. La nuit, ralentir et se méfier des abords boisés."),
    "A15c": ("danger", "Passage de cavaliers", "Cavaliers possibles. Les dépasser largement, à allure réduite, sans klaxonner brutalement."),
    "A16": ("danger", "Descente dangereuse", "Pente importante. Utiliser le frein moteur, éviter de rester freiné en continu (échauffement)."),
    "A17": ("danger", "Feux tricolores", "A17 : annonce des feux de circulation. Ce n'est pas une montée. Anticiper un feu orange ou rouge, surtout si l'adhérence est mauvaise."),
    "A18": ("danger", "Circulation dans les deux sens", "Fin d'un tronçon à sens unique : on retrouve des véhicules en face. Se rabattre à droite."),
    "A19": ("danger", "Risque de chute de pierres", "Pierres ou éboulis possibles sur la chaussée. Éviter de coller le bas-côté et surveiller le sol."),
    "A20": ("danger", "Débouché sur un quai ou une berge", "La route se termine sur l'eau. Vitesse très réduite, aucun écart."),
    "A21": ("danger", "Débouché de cyclistes", "Cyclistes susceptibles de déboucher. Laisser de l'espace et adapter l'allure."),
    "A23": ("danger", "Aire de danger aérien", "A23 : pictogramme d'avion. Risque lié à un aérodrome (bruit, surprise). Ce n'est pas le double sens (A18)."),
    "A24": ("danger", "Vent latéral", "A24 : manche à air. Risque de déport, surtout au passage d'un PL ou en sortie de tranchée. Tenir fermement le guidon."),
    "AB1": ("priorite", "Intersection où vous êtes prioritaire", "Les usagers des autres routes doivent vous céder le passage. Rester prudent : ils peuvent ne pas vous voir."),
    "AB2": ("priorite", "Intersection avec priorité à droite", "Vous n'êtes pas prioritaire : appliquer la priorité à droite, sauf signalisation contraire."),
    "AB3a": ("priorite", "Cédez le passage", "Triangle pointe en bas : laisser passer les usagers de la route rencontrée, sans nécessairement s'arrêter si la voie est libre."),
    "AB3b": ("priorite", "Cédez le passage (signal avancé)", "AB3b : signal avancé d'un cédez-le-passage (AB3a). Souvent avant un giratoire : céder aux usagers déjà engagés. Le panneau de giratoire est le AB25."),
    "AB4": ("priorite", "Stop", "Arrêt obligatoire au STOP, même si la voie paraît libre. Marquer un temps d'arrêt avant de s'engager."),
    "AB5": ("priorite", "Signal avancé d'un STOP", "AB5 : annonce un AB4 (STOP) plus loin. Ce n'est pas céder au sens inverse (B15, rond à flèches)."),
    "AB6": ("priorite", "Route prioritaire", "Losange jaune : vous circulez sur une route prioritaire jusqu'à indication contraire."),
    "AB7": ("priorite", "Fin de route prioritaire", "Losange jaune barré : vous perdez la priorité. Souvent suivi d'un STOP ou d'un cédez-le-passage."),
    "AB25": ("priorite", "Carrefour à sens giratoire", "Annonce un rond-point. Céder le passage aux usagers déjà dans l'anneau (sauf signalisation locale contraire)."),
    "B0": ("interdiction", "Circulation interdite dans les deux sens", "Aucun véhicule ne peut s'engager, dans aucun sens."),
    "B1": ("interdiction", "Sens interdit", "Interdiction d'emprunter la voie dans ce sens. L'autre sens peut rester autorisé."),
    "B2a": ("interdiction", "Interdiction de tourner à gauche", "Tourner à gauche est interdit à la prochaine intersection."),
    "B2b": ("interdiction", "Interdiction de tourner à droite", "Tourner à droite est interdit à la prochaine intersection."),
    "B2c": ("interdiction", "Interdiction de faire demi-tour", "Le demi-tour est interdit à cet endroit."),
    "B3": ("interdiction", "Interdiction de dépasser les véhicules à moteur", "Dépassement interdit. Rester derrière, même si le véhicule précédent est lent."),
    "B3a": ("interdiction", "Interdiction de dépasser pour les véhicules de plus de 3,5 t", "Concerne les poids lourds. Une moto n'est pas visée par cette interdiction spécifique."),
    "B4": ("interdiction", "Arrêt à la douane", "B4 : arrêt obligatoire au poste de douane. Ce n'est pas une interdiction aux caravanes."),
    "B5a": ("interdiction", "Arrêt au poste de gendarmerie", "B5a : arrêt obligatoire au poste de gendarmerie. L'interdiction aux poids lourds est un autre panneau (camion cerclé de rouge)."),
    "B5b": ("interdiction", "Arrêt au poste de police", "B5b : inscription POLICE. Arrêt obligatoire. Ce n'est pas une interdiction aux marchandises."),
    "B5c": ("interdiction", "Arrêt au poste de péage", "B5c : arrêt au péage. Ce n'est pas une interdiction TMD."),
    "B6a1": ("interdiction", "Stationnement interdit", "Stationner est interdit. Un arrêt momentané pour prendre ou déposer peut rester possible selon le cas."),
    "B6d": ("interdiction", "Arrêt et stationnement interdits", "Ni s'arrêter, ni stationner. Un motard ne peut pas s'y arrêter « juste une minute »."),
    "B7a": ("interdiction", "Accès interdit aux véhicules à moteur sauf cyclomoteurs", "B7a : voitures et motos interdites ; les cyclomoteurs peuvent passer. Tous les moteurs interdits = B7b."),
    "B7b": ("interdiction", "Accès interdit à tous les véhicules à moteur", "B7b : aucun véhicule à moteur, moto comprise. À ne pas confondre avec B7a (sauf cyclomoteurs)."),
    "B8": ("interdiction", "Accès interdit aux véhicules de transport de marchandises", "B8 : pictogramme camion, fond blanc cerclé de rouge. La fin de toutes les interdictions est le B31 (fond blanc, barre noire)."),
    "B9a": ("interdiction", "Accès interdit aux piétons", "Les piétons ne peuvent pas s'engager. Une moto n'est pas un piéton."),
    "B9b": ("interdiction", "Accès interdit aux cycles", "B9b : rond blanc cerclé de rouge, pictogramme vélo. Seule vraie interdiction aux vélos."),
    "B9d": ("interdiction", "Accès interdit aux véhicules agricoles à moteur", "B9d : pictogramme tracteur. Les motos de tourisme ne sont pas des véhicules agricoles."),
    "B9f": ("interdiction", "Accès interdit aux véhicules de transport en commun", "B9f : pictogramme bus. Ce n'est pas l'interdiction aux agricoles (B9d)."),
    "B9g": ("interdiction", "Accès interdit aux cyclomoteurs", "B9g : interdiction aux cyclomoteurs (≤ 50 cm³). Une moto de cylindrée supérieure n'est pas un cyclomoteur."),
    "B9h": ("interdiction", "Accès interdit aux motocyclettes", "B9h : pictogramme moto. L'accès est interdit aux motocyclettes et motocyclettes légères, quelle que soit la cylindrée."),
    "B11": ("interdiction", "Limitation de largeur", "Accès interdit aux véhicules dont la largeur, chargement compris, dépasse la valeur indiquée. Une moto passe presque toujours."),
    "B12": ("interdiction", "Limitation de hauteur (ici 3,5 m)", "B12 : accès interdit si la hauteur, chargement compris, dépasse 3,5 m. L'interdiction moto est le B9h."),
    "B13": ("interdiction", "Limitation de tonnage", "B13 : accès interdit aux véhicules dont le poids total autorisé dépasse le tonnage indiqué."),
    "B14-50": ("interdiction", "Limitation de vitesse à 50 km/h", "Vitesse maximale 50 km/h, souvent en agglomération ou en travaux."),
    "B14-80": ("interdiction", "Limitation de vitesse à 80 km/h", "Vitesse maximale 80 km/h. C'est aussi la limite générale hors agglo sur beaucoup de bidirectionnelles."),
    "B14-90": ("interdiction", "Limitation de vitesse à 90 km/h", "Vitesse maximale 90 km/h, parfois par dérogation départementale hors agglomération."),
    "B14-110": ("interdiction", "Limitation de vitesse à 110 km/h", "Vitesse maximale 110 km/h : voies rapides, ou autoroute sous la pluie / permis probatoire."),
    "B14-130": ("interdiction", "Limitation de vitesse à 130 km/h", "Vitesse maximale 130 km/h : autoroute par temps sec pour un conducteur confirmé."),
    "B16": ("interdiction", "Signaux sonores interdits", "B16 : klaxon interdit, sauf danger imminent. La vitesse minimale obligatoire est le B25."),
    "B18a": ("interdiction", "Accès interdit aux véhicules transportant des matières explosives ou inflammables", "B18a vise les transports TMD explosifs / inflammables."),
    "B18b": ("interdiction", "Accès interdit aux véhicules transportant des matières polluant les eaux", "B18b vise les transports susceptibles de polluer les eaux."),
    "B19": ("interdiction", "Autres interdictions (inscription sur le panneau)", "B19 : l'interdiction est écrite sur le panneau. Ce n'est pas une limite de poids (B13)."),
    "B21-1": ("obligation", "Obligation de tourner à droite avant le panneau", "B21-1 : flèche horizontale vers la droite. Tourner à droite avant le panneau. Le contournement d'un îlot est le B21a1."),
    "B21a1": ("obligation", "Contournement obligatoire par la droite", "B21a1 : flèche qui contourne. Passer à droite de l'obstacle (îlot, terre-plein)."),
    "B21b": ("obligation", "Direction obligatoire tout droit", "B21b : flèche vers le haut. Aller tout droit. Ce n'est pas un tourne-à-gauche."),
    "B22a": ("obligation", "Piste ou bande obligatoire pour cycles", "Obligatoire pour les cycles. Une moto n'a pas à l'emprunter."),
    "B22b": ("obligation", "Chemin obligatoire pour piétons", "B22b : rond bleu, pictogramme piéton. La fin de piste cyclable obligatoire est le B40."),
    "B26": ("obligation", "Chaînes à neige obligatoires", "Équipements spéciaux hiver sur au moins deux roues motrices. À moto, la neige impose souvent de ne pas partir."),
    "B27a": ("obligation", "Voie réservée aux véhicules des services réguliers de transport en commun", "Voie de bus. Une moto ne peut l'emprunter que si un panonceau l'y autorise."),
    "B29": ("obligation", "Autres obligations", "Obligation particulière précisée par un panonceau (exemple : feux allumés)."),
    "B30": ("interdiction", "Entrée d'une zone 30", "B30 : rectangle « ZONE » + 30. Vitesse limitée à 30 km/h dans toute la zone. Ce n'est pas un rond bleu (fin d'obligation)."),
    "B31": ("interdiction", "Fin de toutes les interdictions précédemment signalées", "B31 : fond blanc, barre noire. Met fin aux interdictions temporaires des panneaux ronds à fond blanc. L'interdiction marchandises est le B8."),
    "B33-50": ("interdiction", "Fin de limitation de vitesse à 50 km/h", "La limite à 50 km/h cesse. La limitation générale de la route reprend."),
    "B34a": ("interdiction", "Fin d'interdiction de dépasser", "Le dépassement redevient autorisé si les autres règles le permettent."),
    "B40": ("obligation", "Fin de piste ou bande obligatoire pour cycles", "B40 : rond bleu vélo barré de rouge. Fin de l'obligation B22a."),
    "B41": ("obligation", "Fin de chemin obligatoire pour piétons", "B41 : rond bleu piéton barré. Ce n'est pas l'entrée de zone 30 (B30, rectangle ZONE 30)."),
    "B42": ("obligation", "Fin de chemin obligatoire pour cavaliers", "B42 : rond bleu cavalier barré. La fin de zone 30 est le B51."),
    "B44": ("obligation", "Fin de l'obligation de chaînes à neige", "B44 : chaînes barrées. Ce n'est pas la zone de rencontre (B52)."),
    "B45a": ("obligation", "Fin de voie réservée aux transports en commun", "B45 : bus barré. La fin de zone de rencontre est le B53."),
    "B51": ("interdiction", "Sortie de zone 30", "B51 : rectangle de sortie de zone. La limitation générale reprend (souvent 50 en agglo)."),
    "B52": ("obligation", "Entrée d'une zone de rencontre", "B52 : rectangle « ZONE DE RENCONTRE ». Vitesse 20 km/h, piétons autorisés sur la chaussée et prioritaires."),
    "B53": ("obligation", "Sortie de zone de rencontre", "B53 : fin du régime 20 km/h et de la priorité piétonne généralisée sur chaussée."),
    "C1a": ("indication", "Lieu aménagé pour le stationnement", "Parking. Le stationnement d'une moto y est autorisé selon le marquage."),
    "C1b": ("indication", "Lieu aménagé pour le stationnement à durée limitée (disque)", "C1b (IISR) : stationnement gratuit à durée limitée, contrôle par disque. Le payant est le C1c."),
    "C4a": ("indication", "Vitesse conseillée (ici 50 km/h)", "C4a : allure recommandée, pas une limitation. En cas de danger, elle est souvent trop élevée pour une moto."),
    "C5": ("indication", "Station de taxis", "C5 : emplacement de taxis. Ce n'est pas le stationnement payant (C1c)."),
    "C8": ("indication", "Place d'arrêt d'urgence", "C8 : emplacement pour s'arrêter en cas d'urgence. Ce n'est pas le stationnement alterné."),
    "C12": ("indication", "Circulation à sens unique", "Sens unique. On ne doit pas rencontrer de véhicule en face."),
    "C13a": ("indication", "Impasse", "Voie sans issue. Inutile d'y entrer pour « traverser »."),
    "C13b": ("indication", "Présignalisation d'une impasse", "C13b : impasse plus loin (souvent à une intersection). L'impasse avec issue piétonne est le C13c."),
    "C14": ("indication", "Praticabilité de la section de route", "C14 : état d'un col ou d'une section (ouvert, enneigé, fermé). Ce n'est pas une vitesse conseillée (C4a)."),
    "C18": ("indication", "Priorité par rapport au sens inverse", "C18 : dans le rétrécissement, vous passez avant le sens opposé. L'inverse (céder) est le B15."),
    "C20a": ("indication", "Passage pour piétons", "Localise un passage piéton. Ralentir et être prêt à s'arrêter."),
    "C20c": ("indication", "Traversée de voies de tramways", "C20c : rails de tram. À moto, les franchir le plus perpendiculairement possible. Le passage piéton surélevé n'est pas ce code."),
    "C24a": ("indication", "Conditions de circulation applicables à une voie", "C24a : indique ce qui s'applique à une voie (vitesse, affectation). Ce n'est pas un dos-d'âne (C27)."),
    "C24b": ("indication", "Affectation de voies", "C24b : plusieurs voies avec des règles différentes. Ce n'est pas un ralentisseur."),
    "C26a": ("indication", "Voie de détresse à droite", "C26a : voie d'arrêt d'urgence en descente, côté droit, pour un véhicule en perte de freins."),
    "C27": ("indication", "Surélévation de chaussée", "C27 : plateau ou dos-d'âne annoncé. À moto : allure réduite, trajectoire perpendiculaire."),
    "C28": ("indication", "Réduction du nombre de voies", "C28 : rabattement d'une voie. Anticiper, surtout près d'un PL."),
    "C50": ("indication", "Indications diverses", "C50 : mention écrite (aire de chaînage, etc.). La voie de détresse est le C26a."),
    "C107": ("indication", "Route à accès réglementé", "C107 : pictogramme voiture, fond bleu. Voie express / accès réglementé, souvent 110 km/h. Le début d'autoroute est le C207."),
    "C111": ("indication", "Entrée de tunnel", "C111 : pictogramme de tunnel. Allumer les feux, retirer les lunettes de soleil, surveiller l'écart."),
    "C112": ("indication", "Sortie de tunnel", "C112 : tunnel barré. Sortie de tunnel : reprendre ses distances, méfiance à l'éblouissement."),
    "C113": ("indication", "Piste ou bande cyclable conseillée et réservée aux cycles", "C113 : carré bleu. Voie conseillée, pas obligatoire. L'obligation est le rond bleu B22a."),
    "C114": ("indication", "Fin de piste ou bande cyclable conseillée", "C114 : carré bleu vélo barré de rouge = FIN de l'aménagement cyclable conseillé. L'interdiction aux cycles est le B9b."),
    "C207": ("indication", "Début d'autoroute", "C207 : pictogramme d'autoroute. 130 km/h par temps sec (110 sous la pluie ou en permis probatoire)."),
    "CE14": ("service", "Installations accessibles aux personnes à mobilité réduite", "CE14 : pictogramme fauteuil. Accessibilité PMR. La borne d'appel est le CE2a."),
    "CE26": ("service", "Station de gonflage gratuite", "CE26 : gonflage hors station-service, usage gratuit. Le dépannage est le CE28."),
    "CE50": ("service", "Installations ou services divers", "CE50 : mention « AUTRES », service sans idéogramme dédié. Le covoiturage est le CE52."),
    "EB10": ("localisation", "Entrée d'agglomération", "Le nom de la commune sur fond blanc vaut limitation à 50 km/h, même sans panneau 50."),
    "EB20": ("localisation", "Sortie d'agglomération", "Panneau barré : fin d'agglomération. La limitation hors agglo reprend (souvent 80 km/h)."),
    "M9z": ("panonceau", "Panonceau d'indications diverses", "Complète un panneau principal (distance, catégorie de véhicules, horaires)."),
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
]


def sign_obj(code: str) -> dict:
    family, title, detail = OFFICIAL[code]
    return {
        "code": code,
        "family": family,
        "title": title,
        "detail": detail,
        "image": f"assets/img/signs/{code}.svg",
    }


def write_signs() -> None:
    # Les ajouts Wikimedia (corridor SR53, B manquants, etc.) vivent dans add_new_signs.NEW.
    extra: dict[str, tuple[str, str, str]] = {}
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from add_new_signs import NEW, FAMILIES as NEW_FAM  # type: ignore
        extra = {c: (a, b, d) for c, (a, b, d, _fn) in NEW.items()}
        FAMILIES.update(NEW_FAM)
    except Exception:
        extra = {}
    merged = dict(OFFICIAL)
    merged.update(extra)
    order = list(merged.keys())
    payload = {
        "signs": [
            {
                "code": c,
                "family": merged[c][0],
                "title": merged[c][1],
                "detail": merged[c][2],
                "image": f"assets/img/signs/{c}.svg",
            }
            for c in order
        ],
        "families": FAMILIES,
    }
    (ROOT / "data" / "signs.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"signs.json: {len(order)} panneaux")


def set_correct_text(q: dict, text: str, explanation: str | None = None, alt: str | None = None) -> None:
    correct_ids = set(q.get("correct") or [])
    used = {c["text"] for c in q["choices"]}
    for c in q["choices"]:
        if c["id"] in correct_ids:
            c["text"] = text
        elif c["text"] == text:
            for d in DISTRACTORS:
                if d != text and d not in used:
                    c["text"] = d
                    used.add(d)
                    break
    if explanation:
        q["explanation"] = explanation
    if alt:
        q["imageAlt"] = alt


def make_ident(qid: str, code: str, extra_choices: list[str] | None = None) -> dict:
    family, title, detail = OFFICIAL[code]
    cat_theme = {
        "danger": ("signalisation", "R"),
        "priorite": ("signalisation", "R"),
        "interdiction": ("signalisation", "R"),
        "obligation": ("signalisation", "R"),
        "indication": ("signalisation", "R"),
        "service": ("signalisation", "R"),
        "localisation": ("signalisation", "R"),
        "panonceau": ("signalisation", "R"),
        "securite": ("signalisation", "R"),
        "temporaire": ("signalisation", "R"),
    }[family]
    extras = extra_choices or []
    choices_txt = [title]
    for d in extras + DISTRACTORS:
        if d != title and d not in choices_txt:
            choices_txt.append(d)
        if len(choices_txt) == 4:
            break
    letters = "abcd"
    return {
        "id": qid,
        "category": cat_theme[0],
        "theme": cat_theme[1],
        "question": "Que signifie ce panneau ?",
        "choices": [{"id": letters[i], "text": t} for i, t in enumerate(choices_txt)],
        "correct": ["a"],
        "explanation": detail,
        "multi": False,
        "image": f"assets/img/signs/{code}.svg",
        "imageAlt": title,
        "imageCredit": CREDIT,
    }


def patch_questions() -> None:
    path = ROOT / "data" / "questions.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    qs = data["questions"]
    by_id = {q["id"]: q for q in qs}

    # Remap images when the stem assumed a wrong meaning
    remaps = {
        "circulation-147": ("C207", "Début d'autoroute"),
        "sigb-013": ("C207", "Début d'autoroute"),
        "sigb-011": ("B30", "Entrée d'une zone 30"),
        "sigb-012": ("B52", "Entrée d'une zone de rencontre"),
    }
    for qid, (code, alt) in remaps.items():
        q = by_id[qid]
        q["image"] = f"assets/img/signs/{code}.svg"
        q["imageAlt"] = alt

    # Behavioral question that used A24 as gravillons
    wind = by_id["sigb-003"]
    wind["question"] = "Face à ce panneau de vent latéral, à moto il faut :"
    set_correct_text(
        wind,
        "Ralentir, tenir fermement le guidon et anticiper un déport au passage d'un PL",
        "A24 annonce un vent latéral. Le souffle d'un poids lourd ou une sortie de tranchée peut déporter la moto.",
        "Vent latéral",
    )
    # Make sure wrong choices stay plausible
    for c in wind["choices"]:
        if c["id"] not in set(wind["correct"]):
            continue
    existing_wrong = [c for c in wind["choices"] if c["id"] not in set(wind["correct"])]
    replacements = [
        "Accélérer pour passer plus vite dans la rafale",
        "Se mettre en travers pour offrir moins de prise au vent",
        "Relâcher le guidon pour que la moto se recentre seule",
    ]
    for c, txt in zip(existing_wrong, replacements):
        c["text"] = txt

    # Auto-fix identification questions tied to a catalog image
    ident_prompts = {
        "Que signifie ce panneau ?",
        "Quel panneau interdit vraiment l'accès aux vélos ?",
    }
    skipped = []
    updated = 0
    for q in qs:
        img = q.get("image") or ""
        if not img.startswith("assets/img/signs/"):
            continue
        code = Path(img).stem
        if code not in OFFICIAL:
            skipped.append((q["id"], code, "code inconnu"))
            continue
        title, detail = OFFICIAL[code][1], OFFICIAL[code][2]
        if q["question"] == "Que signifie ce panneau ?":
            set_correct_text(q, title, detail, title)
            updated += 1
        else:
            # keep behavioral questions; just refresh alt if it still matches the sign
            if q["id"] not in remaps and q.get("imageAlt") and code in OFFICIAL:
                # Only refresh alt when the question is about this sign's official meaning
                pass

    # Targeted alt/explanation for remaining sign-linked behavior Qs
    extras = {
        "sigb-010": ("Limitation de hauteur à 3,5 m", None),
        "sig-b9b": (None, None),
        "sig-c114-barre": (None, None),
        "sigb-b9h": ("Accès interdit aux motocyclettes", None),
        "sig-b9h": ("Accès interdit aux motocyclettes", None),
        "protection-149": ("Accès interdit aux cyclomoteurs", None),
        "divers-151": ("Accès interdit aux motocyclettes", None),
        "usagers-150": ("Passage pour piétons", None),
        "route-148": ("Virage à droite", None),
        "circulation-146": ("Voie réservée aux bus", None),
        "sigb-001": ("Chaussée glissante", None),
        "sigb-002": ("Débouché de transports en commun / rails", None),
        "sigb-004": ("Cédez le passage", None),
        "sigb-005": ("Stop", None),
        "sigb-006": ("Route prioritaire", None),
        "sigb-007": ("Sens interdit", None),
        "sigb-008": ("Interdiction de dépasser", None),
        "sigb-009": ("Arrêt et stationnement interdits", None),
        "sigb-014": ("Entrée d'agglomération", None),
        "sigb-015": ("Sortie d'agglomération", None),
        "circulation-147": (
            "Début d'autoroute",
            "C207 (pictogramme d'autoroute). Par temps sec et permis définitif : 130 km/h, 110 sous la pluie. C107 est la route à accès réglementé.",
        ),
        "sigb-013": (
            "Début d'autoroute",
            "C207 = début d'autoroute. C107 (voiture sur fond bleu) est une route à accès réglementé, pas une autoroute.",
        ),
        "sigb-011": (
            "Entrée d'une zone 30",
            "B30 (rectangle ZONE 30). La limite est 30 km/h dans toute la zone, même si la rue paraît vide.",
        ),
        "sigb-012": (
            "Entrée d'une zone de rencontre",
            "B52. En zone de rencontre la vitesse maximale est 20 km/h ; les piétons sont prioritaires sur la chaussée.",
        ),
    }
    for qid, (alt, expl) in extras.items():
        q = by_id[qid]
        if alt:
            q["imageAlt"] = alt
        if expl:
            q["explanation"] = expl

    # Ensure circulation-147 still has the right answer after image change
    set_correct_text(
        by_id["circulation-147"],
        "130 km/h max, 110 sous la pluie",
        by_id["circulation-147"]["explanation"],
        "Début d'autoroute",
    )
    set_correct_text(
        by_id["sigb-013"],
        "Le début d'une autoroute",
        by_id["sigb-013"]["explanation"],
        "Début d'autoroute",
    )

    new_qs = [
        make_ident("sig-107", "B7a", ["Accès interdit à tous les véhicules à moteur", "Accès interdit aux cyclomoteurs"]),
        make_ident("sig-108", "B7b", ["Accès interdit aux véhicules à moteur sauf cyclomoteurs", "Sens interdit"]),
        make_ident("sig-109", "B9d", ["Accès interdit aux véhicules de transport en commun", "Accès interdit aux motocyclettes"]),
        make_ident("sig-110", "B30", ["Fin de chemin obligatoire pour piétons", "Limitation de vitesse à 30 km/h hors zone"]),
        make_ident("sig-111", "B40", ["Fin de piste ou bande cyclable conseillée", "Accès interdit aux cycles"]),
        make_ident("sig-112", "B51", ["Entrée d'une zone 30", "Fin de chemin obligatoire pour cavaliers"]),
        make_ident("sig-113", "B52", ["Fin de l'obligation de chaînes à neige", "Entrée d'une zone 30"]),
        make_ident("sig-114", "B53", ["Fin de voie réservée aux transports en commun", "Entrée d'une zone de rencontre"]),
        make_ident("sig-115", "C26a", ["Indications diverses", "Place d'arrêt d'urgence"]),
        make_ident("sig-116", "C27", ["Conditions de circulation applicables à une voie", "Cassis ou dos-d'âne"]),
        make_ident("sig-117", "C4a", ["Praticabilité de la section de route", "Limitation de vitesse à 50 km/h"]),
        {
            "id": "sigb-016",
            "category": "signalisation",
            "theme": "R",
            "question": "Ce panneau (voiture sur fond bleu) annonce-t-il une autoroute ?",
            "choices": [
                {"id": "a", "text": "Non : c'est une route à accès réglementé (C107). L'autoroute est le C207"},
                {"id": "b", "text": "Oui, on peut rouler à 130 km/h"},
                {"id": "c", "text": "Oui, mais seulement sous la pluie"},
                {"id": "d", "text": "C'est une issue de secours de tunnel"},
            ],
            "correct": ["a"],
            "explanation": "C107 = route à accès réglementé (souvent 110 km/h). C207 = début d'autoroute (130 km/h par temps sec).",
            "multi": False,
            "image": "assets/img/signs/C107.svg",
            "imageAlt": "Route à accès réglementé",
            "imageCredit": CREDIT,
        },
        {
            "id": "sigb-017",
            "category": "signalisation",
            "theme": "R",
            "question": "Dans un tunnel annoncé par ce panneau, un motard doit surtout :",
            "choices": [
                {"id": "a", "text": "Allumer les feux, garder ses distances et retirer les lunettes de soleil"},
                {"id": "b", "text": "Éteindre les feux pour ne pas éblouir"},
                {"id": "c", "text": "Accélérer pour sortir plus vite"},
                {"id": "d", "text": "Circuler sur la bande d'arrêt d'urgence"},
            ],
            "correct": ["a"],
            "explanation": "C111 = entrée de tunnel. Feux allumés, allure stable, pas de dépassement hasardeux, attention à l'éblouissement à la sortie.",
            "multi": False,
            "image": "assets/img/signs/C111.svg",
            "imageAlt": "Entrée de tunnel",
            "imageCredit": CREDIT,
        },
    ]

    existing_ids = {q["id"] for q in qs}
    added = 0
    for nq in new_qs:
        if nq["id"] not in existing_ids:
            qs.append(nq)
            added += 1

    # Recount categories
    counts: dict[str, int] = {}
    for q in qs:
        counts[q["category"]] = counts.get(q["category"], 0) + 1
    for cat in data["categories"]:
        cat["count"] = counts.get(cat["id"], 0)

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"questions: {len(qs)} (ident mises à jour: {updated}, ajoutées: {added})")
    if skipped:
        print("skipped:", skipped)


def verify() -> None:
    signs = json.loads((ROOT / "data" / "signs.json").read_text(encoding="utf-8"))["signs"]
    data = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
    qs = data["questions"]
    by_code = {s["code"]: s for s in signs}
    missing_img = []
    for s in signs:
        if not (ROOT / s["image"]).exists():
            missing_img.append(s["code"])
    print("images manquantes:", missing_img or "aucune")

    mismatches = []
    for q in qs:
        img = q.get("image") or ""
        if not img.startswith("assets/img/signs/"):
            continue
        code = Path(img).stem
        if code not in by_code:
            mismatches.append((q["id"], code, "pas dans catalogue"))
            continue
        if q["question"] != "Que signifie ce panneau ?":
            continue
        title = by_code[code]["title"]
        correct_ids = set(q["correct"])
        got = [c["text"] for c in q["choices"] if c["id"] in correct_ids]
        if got != [title]:
            mismatches.append((q["id"], code, f"attendu {title!r} obtenu {got}"))
        if not (ROOT / img).exists():
            mismatches.append((q["id"], code, "fichier image absent"))
    print("ident mismatches:", len(mismatches))
    for row in mismatches[:30]:
        print(" ", row)

    # spot-check remaps
    for qid, want in {
        "circulation-147": "C207",
        "sigb-013": "C207",
        "sigb-011": "B30",
        "sigb-012": "B52",
        "sig-096": "C107",
        "sig-100": "C207",
        "sig-075": "B31",
        "sig-051": "B8",
        "sig-022": "A17",
        "sig-069": "B21b",
    }.items():
        q = next(x for x in qs if x["id"] == qid)
        stem = Path(q["image"]).stem
        ok = next(c["text"] for c in q["choices"] if c["id"] in set(q["correct"]))
        print(f"  {qid}: img={stem} (want {want}) | {ok[:70]}")


if __name__ == "__main__":
    write_signs()
    patch_questions()
    verify()
