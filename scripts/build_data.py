#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère data/signs.json et data/questions.json pour le site Code Moto 2026.

Ne pas régénérer les JSON depuis ce script : l'encodage est corrompu et les
titres officiels IISR sont maintenus dans data/signs.json (voir
scripts/audit_fix_signs.py).
"""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNS_DIR = ROOT / "assets" / "img" / "signs"
OUT_DIR = ROOT / "data"

SIGNS = [
    ("A1a", "danger", "Virage à droite", "Annonce un virage serré vers la droite. À moto : ralentir avant le virage, se placer à l'extérieur, regarder la sortie."),
    ("A1b", "danger", "Virage à gauche", "Annonce un virage serré vers la gauche. Risque de collision avec un véhicule en sens inverse si la trajectoire coupe l'axe."),
    ("A1c", "danger", "Succession de virages, premier à droite", "Série de virages dont le premier est à droite. Adapter l'allure dès le premier, sans accélérer entre deux courbes."),
    ("A1d", "danger", "Succession de virages, premier à gauche", "Série de virages dont le premier est à gauche. La visibilité et l'adhérence peuvent changer d'une courbe à l'autre."),
    ("A2a", "danger", "Cassis ou dos-d'âne", "Déformation de la chaussée. À moto, lever légèrement les fesses, relâcher les freins et garder l'assiette stable."),
    ("A2b", "danger", "Ralentisseur de type dos-d'âne", "Ralentisseur volontaire. Franchir droit, sans angle, à allure réduite pour ne pas décoller la roue avant."),
    ("A3", "danger", "Chaussée rétrécie", "La chaussée se rétrécit des deux côtés. Anticiper, serrer sa droite et éviter les dépassements."),
    ("A3a", "danger", "Chaussée rétrécie par la droite", "Rétrécissement côté droit. Un obstacle ou un véhicule peut vous contraindre à vous déporter."),
    ("A3b", "danger", "Chaussée rétrécie par la gauche", "Rétrécissement côté gauche. Surveiller le trafic opposé et garder une marge de sécurité."),
    ("A4", "danger", "Chaussée glissante", "Adhérence réduite (pluie, verglas, gravillons, feuilles). Allonger les distances et éviter les à-coups."),
    ("A6", "danger", "Pont mobile", "Le pont peut s'ouvrir. S'arrêter si le feu ou la barrière l'impose, jamais s'engager au dernier moment."),
    ("A7", "danger", "Passage à niveau avec barrières", "Voie ferrée protégée par des barrières. Ne jamais s'engager si le feu clignote ou si les barrières bougent."),
    ("A8", "danger", "Passage à niveau sans barrières", "Voie ferrée sans barrière. S'arrêter, regarder et écouter avant de s'engager. Un train peut arriver vite."),
    ("A9", "danger", "Traversée de voies de tramway", "Rails très glissants pour une moto. Les franchir le plus perpendiculairement possible, sans freiner dessus."),
    ("A13a", "danger", "Endroit fréquenté par les enfants", "Proximité d'une école, d'un parc ou d'un arrêt. Réduire l'allure : un enfant peut surgir."),
    ("A13b", "danger", "Passage pour piétons", "Annonce un passage piéton. Un piéton engagé est prioritaire, même hors des clous en agglomération s'il a commencé à traverser."),
    ("A14", "danger", "Autres dangers", "Danger non précisé par un autre panneau. Le panonceau éventuellement associé précise le risque."),
    ("A15a1", "danger", "Passage d'animaux domestiques", "Animaux de ferme susceptibles de traverser. Freiner progressivement, klaxonner avec mesure si besoin."),
    ("A15b", "danger", "Passage d'animaux sauvages", "Risque de collision avec un animal. La nuit, ralentir et se méfier des abords boisés."),
    ("A15c", "danger", "Passage de cavaliers", "Cavaliers possibles. Les dépasser largement, à allure réduite, sans klaxonner brutalement."),
    ("A16", "danger", "Descente dangereuse", "Pente importante. Utiliser le frein moteur, éviter de rester freiné en continu (échauffement)."),
    ("A17", "danger", "Remontée (montée)", "Montée. Anticiper un véhicule lent, garder de la puissance disponible et ne pas coller le précédent."),
    ("A18", "danger", "Circulation dans les deux sens", "Fin d'un tronçon à sens unique : on retrouve des véhicules en face. Se rabattre à droite."),
    ("A19", "danger", "Risque de chute de pierres", "Pierres ou éboulis possibles sur la chaussée. Éviter de coller le bas-côté et surveiller le sol."),
    ("A20", "danger", "Débouché sur un quai ou une berge", "La route se termine sur l'eau. Vitesse très réduite, aucun écart."),
    ("A21", "danger", "Débouché de cyclistes provenant de droite ou de gauche", "Cyclistes susceptibles de déboucher. Laisser de l'espace et adapter l'allure."),
    ("A23", "danger", "Circulation de véhicules dans les deux sens", "Annonce un trafic bidirectionnel après un rétrécissement ou des travaux."),
    ("A24", "danger", "Projection de gravillons", "Gravillons projetés : adhérence très mauvaise à moto. Lever l'allure, éviter d'incliner et de freiner fort."),
    ("AB1", "priorite", "Intersection où vous êtes prioritaire", "Les usagers des autres routes doivent vous céder le passage. Rester prudent : ils peuvent ne pas vous voir."),
    ("AB2", "priorite", "Intersection avec priorité à droite", "Vous n'êtes pas prioritaire : appliquer la priorité à droite, sauf signalisation contraire."),
    ("AB3a", "priorite", "Cédez le passage", "Triangle pointe en bas : laisser passer les usagers de la route rencontrée, sans nécessairement s'arrêter si la voie est libre."),
    ("AB3b", "priorite", "Cédez le passage au carrefour à sens giratoire", "À l'approche d'un giratoire, céder le passage aux usagers déjà engagés dans l'anneau."),
    ("AB4", "priorite", "Stop", "Arrêt obligatoire au STOP, même si la voie paraît libre. Marquer un temps d'arrêt avant de s'engager."),
    ("AB5", "priorite", "Cédez le passage à la circulation venant en sens inverse", "Le rétrécissement vous oblige à laisser passer les véhicules d'en face."),
    ("AB6", "priorite", "Route prioritaire", "Losange jaune : vous circulez sur une route prioritaire jusqu'à indication contraire."),
    ("AB7", "priorite", "Fin de route prioritaire", "Losange jaune barré : vous perdez la priorité. Souvent suivi d'un STOP ou d'un cédez-le-passage."),
    ("AB25", "priorite", "Carrefour à sens giratoire", "Annonce un rond-point. Céder le passage aux usagers déjà dans l'anneau (sauf signalisation locale contraire)."),
    ("B0", "interdiction", "Circulation interdite dans les deux sens", "Aucun véhicule ne peut s'engager, dans aucun sens."),
    ("B1", "interdiction", "Sens interdit", "Interdiction d'emprunter la voie dans ce sens. L'autre sens peut rester autorisé."),
    ("B2a", "interdiction", "Interdiction de tourner à gauche", "Tourner à gauche est interdit à la prochaine intersection."),
    ("B2b", "interdiction", "Interdiction de tourner à droite", "Tourner à droite est interdit à la prochaine intersection."),
    ("B2c", "interdiction", "Interdiction de faire demi-tour", "Le demi-tour est interdit à cet endroit."),
    ("B3", "interdiction", "Interdiction de dépasser les véhicules à moteur", "Dépassement interdit. Rester derrière, même si le véhicule précédent est lent."),
    ("B3a", "interdiction", "Interdiction de dépasser pour les véhicules de plus de 3,5 t", "Concerne les poids lourds. Une moto n'est pas visée par cette interdiction spécifique."),
    ("B4", "interdiction", "Accès interdit aux véhicules tractant une caravane", "Interdiction aux attelages caravane / remorque visés."),
    ("B5a", "interdiction", "Accès interdit aux poids lourds", "Interdiction aux véhicules de transport de marchandises au-delà du tonnage indiqué."),
    ("B5b", "interdiction", "Accès interdit aux véhicules de transport de marchandises", "Concerne les véhicules affectés au transport de marchandises."),
    ("B5c", "interdiction", "Accès interdit aux véhicules transportant des marchandises dangereuses", "Interdiction aux transports de matières dangereuses (plaque orange)."),
    ("B6a1", "interdiction", "Stationnement interdit", "Stationner est interdit. Un arrêt momentané pour prendre ou déposer peut rester possible selon le cas."),
    ("B6d", "interdiction", "Arrêt et stationnement interdits", "Ni s'arrêter, ni stationner. Un motard ne peut pas s'y arrêter « juste une minute »."),
    ("B8", "interdiction", "Fin de toutes les interdictions précédemment signalées", "Met fin aux interdictions prescrites par des panneaux ronds à fond blanc (sauf limitations permanentes)."),
    ("B9a", "interdiction", "Accès interdit aux piétons", "Les piétons ne peuvent pas s'engager. Une moto n'est pas un piéton."),
    ("B9b", "interdiction", "Accès interdit aux cycles", "Interdiction aux vélos. Une moto n'est pas un cycle."),
    ("B9f", "interdiction", "Accès interdit aux véhicules agricoles à moteur", "Concerne les engins agricoles, pas les motos de tourisme."),
    ("B9g", "interdiction", "Acces interdit aux cyclomoteurs", "B9g : cyclomoteurs (<= 50 cm3). Une moto n'est pas un cyclomoteur."),
    ("B9h", "interdiction", "Acces interdit aux motocyclettes", "B9h : pictogramme moto. Interdiction aux motocyclettes, toute cylindree."),
    ("B7a", "interdiction", "Acces interdit aux vehicules a moteur", "B7a : tous les vehicules a moteur, moto comprise."),
    ("B11", "interdiction", "Limitation de largeur", "B11 : largeur maximale, chargement compris. Une moto passe presque toujours."),
    ("B12", "interdiction", "Limitation de hauteur (ici 3,5 m)", "B12 : hauteur maximale. L'interdiction moto est le B9h."),
    ("B13", "interdiction", "Limitation de tonnage", "B13 : poids total autorise. L'interdiction a tous les vehicules a moteur est le B7a."),
    ("B14-50", "interdiction", "Limitation de vitesse à 50 km/h", "Vitesse maximale 50 km/h, souvent en agglomération ou en travaux."),
    ("B14-80", "interdiction", "Limitation de vitesse à 80 km/h", "Vitesse maximale 80 km/h. C'est aussi la limite générale hors agglo sur beaucoup de bidirectionnelles."),
    ("B14-90", "interdiction", "Limitation de vitesse à 90 km/h", "Vitesse maximale 90 km/h, parfois par dérogation départementale hors agglomération."),
    ("B14-110", "interdiction", "Limitation de vitesse à 110 km/h", "Vitesse maximale 110 km/h : voies rapides, ou autoroute sous la pluie / permis probatoire."),
    ("B14-130", "interdiction", "Limitation de vitesse à 130 km/h", "Vitesse maximale 130 km/h : autoroute par temps sec pour un conducteur confirmé."),
    ("B16", "obligation", "Vitesse minimale obligatoire", "Il est interdit de rouler en dessous de la vitesse indiquée, sauf nécessité (embouteillage, conditions)."),
    ("B18a", "interdiction", "Accès interdit aux véhicules dont la largeur, chargement compris, dépasse la largeur indiquée", "Gabarit en largeur. Une moto passe presque toujours, mais pas un véhicule large."),
    ("B18b", "interdiction", "Accès interdit aux véhicules dont la hauteur, chargement compris, dépasse la hauteur indiquée", "Gabarit en hauteur (pont, tunnel)."),
    ("B19", "interdiction", "Accès interdit aux véhicules dont le poids total autorisé dépasse le tonnage indiqué", "Limitation de poids. Une moto légère n'est en général pas concernée."),
    ("B21-1", "obligation", "Contournement obligatoire par la droite", "Obstacle à contourner par la droite (îlot, terre-plein)."),
    ("B21a1", "obligation", "Direction obligatoire à droite", "Obligation de tourner à droite."),
    ("B21b", "obligation", "Direction obligatoire à gauche", "Obligation de tourner à gauche."),
    ("B22a", "obligation", "Piste ou bande obligatoire pour cycles et cyclomoteurs", "Obligatoire pour vélos et cyclomoteurs. Une moto n'a pas à l'emprunter."),
    ("B22b", "obligation", "Fin de piste ou bande obligatoire pour cycles", "Fin de l'obligation pour les cycles."),
    ("B26", "obligation", "Chaînes à neige obligatoires sur au moins deux roues motrices", "Équipements spéciaux hiver. À moto, la neige impose souvent de ne pas partir."),
    ("B27a", "obligation", "Voie réservée aux véhicules des services réguliers de transport en commun", "Voie de bus. Une moto ne peut l'emprunter que si un panonceau l'y autorise."),
    ("B29", "obligation", "Autres obligations", "Obligation particulière précisée par un panonceau (exemple : feux allumés)."),
    ("B31", "obligation", "Fin d'obligation", "Met fin à une obligation précédemment signalée."),
    ("B33-50", "interdiction", "Fin de limitation de vitesse à 50 km/h", "La limite à 50 km/h cesse. La limitation générale de la route reprend."),
    ("B34a", "interdiction", "Fin d'interdiction de dépasser", "Le dépassement redevient autorisé si les autres règles le permettent."),
    ("B41", "obligation", "Entrée de zone 30", "Vitesse limitée à 30 km/h dans toute la zone, jusqu'au panneau de sortie."),
    ("B42", "obligation", "Fin de zone 30", "Sortie de zone 30. La limitation générale reprend (souvent 50 en agglo)."),
    ("B44", "obligation", "Entrée de zone de rencontre", "Vitesse 20 km/h, piétons autorisés sur la chaussée et prioritaires."),
    ("B45a", "obligation", "Fin de zone de rencontre", "Fin du régime 20 km/h et de la priorité piétonne généralisée sur chaussée."),
    ("C1a", "indication", "Lieu aménagé pour le stationnement", "Parking. Le stationnement d'une moto y est autorisé selon le marquage."),
    ("C1b", "indication", "Lieu aménagé pour le stationnement à durée limitée", "Stationnement à durée limitée (disque ou horodateur selon le cas)."),
    ("C5", "indication", "Stationnement payant", "Le stationnement est payant. Une moto n'est pas toujours exonérée."),
    ("C8", "indication", "Stationnement unilatéral à alternance semi-mensuelle", "Côté de stationnement selon la quinzaine."),
    ("C12", "indication", "Circulation à sens unique", "Sens unique. On ne doit pas rencontrer de véhicule en face."),
    ("C13a", "indication", "Impasse", "Voie sans issue. Inutile d'y entrer pour « traverser »."),
    ("C13b", "indication", "Impasse avec une issue pour les piétons", "Sans issue pour les véhicules, mais les piétons peuvent sortir."),
    ("C14", "indication", "Vitesse conseillée", "Allure recommandée, pas une limitation. En cas de danger, elle est souvent trop élevée pour une moto."),
    ("C18", "indication", "Conditions particulières de circulation sur la voie d'entrée", "Présignalisation de conditions sur une bretelle ou une voie."),
    ("C20a", "indication", "Passage pour piétons", "Localise un passage piéton. Ralentir et être prêt à s'arrêter."),
    ("C20c", "indication", "Passage pour piétons surélevé", "Passage piéton sur un plateau. Franchir droit, sans angle."),
    ("C24a", "indication", "Surélévation de chaussée", "Plateau ou dos-d'âne. À moto : allure réduite, trajectoire perpendiculaire."),
    ("C24b", "indication", "Ralentisseur", "Dispositif ralentisseur. Ne pas le prendre en biais."),
    ("C50", "indication", "Voie de détresse", "Voie d'arrêt d'urgence en descente pour véhicules en perte de freins."),
    ("C107", "indication", "Début d'autoroute", "Entrée d'autoroute : 130 km/h par temps sec (110 sous la pluie ou en permis probatoire)."),
    ("C111", "indication", "Début de route à accès réglementé", "Voie rapide / express, souvent limitée à 110 km/h."),
    ("C112", "indication", "Fin de route à accès réglementé", "Sortie de voie rapide : la limitation générale reprend, souvent 80 km/h."),
    ("C114", "indication", "Fin de piste ou bande cyclable conseillée", "C114 : fin de l'amenagement cyclable conseille. Interdiction velo = B9b."),
    ("C207", "indication", "Issue de secours", "Indique une issue de secours (tunnel)."),
    ("CE14", "service", "Poste d'appel d'urgence / téléphone", "Borne d'appel. En cas d'accident sur autoroute, c'est le moyen privilégié pour alerter."),
    ("CE26", "service", "Poste de dépannage", "Garage ou dépannage à proximité."),
    ("CE50", "service", "Aire de covoiturage", "Stationnement dédié au covoiturage."),
    ("EB10", "localisation", "Entrée d'agglomération", "Le nom de la commune sur fond blanc vaut limitation à 50 km/h, même sans panneau 50."),
    ("EB20", "localisation", "Sortie d'agglomération", "Panneau barré : fin d'agglomération. La limitation hors agglo reprend (souvent 80 km/h)."),
    ("M9z", "panonceau", "Panonceau d'indications diverses", "Complète un panneau principal (distance, catégorie de véhicules, horaires)."),
]

CATEGORIES = {
    "signalisation": {"label": "Signalisation", "theme": "R", "blurb": "Panneaux, marquages et ce qu'ils imposent à moto."},
    "route": {"label": "La route", "theme": "R", "blurb": "Adhérence, pièges au sol, météo, trajectoire."},
    "circulation": {"label": "La circulation", "theme": "C", "blurb": "Priorités, vitesses, dépassements, inter-files."},
    "conducteur": {"label": "Le conducteur", "theme": "L", "blurb": "Alcool, fatigue, vigilance, état physique."},
    "usagers": {"label": "Les autres usagers", "theme": "U", "blurb": "Angles morts, piétons, PL, visibilité du motard."},
    "divers": {"label": "Notions diverses", "theme": "D", "blurb": "Papiers, assurance, panne, contrôle technique."},
    "mecanique": {"label": "Mécanique et vérifications", "theme": "M", "blurb": "Pneus, chaîne, freins, éclairage, contrôles."},
    "protection": {"label": "Équipements de protection", "theme": "P", "blurb": "Casque, gants, gilet, protections recommandées."},
    "environnement": {"label": "Environnement", "theme": "E", "blurb": "Bruit, pollution, éco-conduite deux-roues."},
    "secours": {"label": "Premiers secours", "theme": "S", "blurb": "Protéger, alerter, secourir, casque et accident."},
}


def q(qid, category, question, choices, correct, explanation, image=None, image_alt="", multi=False):
    item = {
        "id": qid,
        "category": category,
        "theme": CATEGORIES[category]["theme"],
        "question": question,
        "choices": [{"id": chr(97 + i), "text": c} for i, c in enumerate(choices)],
        "correct": list(correct) if isinstance(correct, (list, tuple)) else [correct],
        "explanation": explanation,
        "multi": bool(multi) or (len(correct) > 1 if isinstance(correct, (list, tuple)) else False),
    }
    if image:
        item["image"] = image
        item["imageAlt"] = image_alt
        item["imageCredit"] = "Wikimedia Commons - signalisation routière française"
    return item


def sign_path(code: str) -> str:
    return f"assets/img/signs/{code}.svg"


def behavior_for(code, family, title, detail, rng):
    mapping = {
        "AB4": (
            "Face à ce panneau, que devez-vous faire ?",
            [
                "Marquer l'arrêt, même si aucun véhicule n'arrive",
                "Ralentir sans forcément s'arrêter si la voie est libre",
                "Klaxonner puis s'engager",
                "S'arrêter seulement la nuit",
            ],
            "a",
            "Le STOP impose un arrêt obligatoire, puis de s'engager quand la voie est libre.",
        ),
        "AB3a": (
            "Ce panneau vous impose-t-il l'arrêt ?",
            [
                "Non, seulement de céder le passage si un usager arrive",
                "Oui, arrêt obligatoire dans tous les cas",
                "Oui, mais seulement en agglomération",
                "Non, il indique une route prioritaire",
            ],
            "a",
            "Le cédez-le-passage n'impose l'arrêt que si un usager arrive. Le STOP, lui, impose toujours l'arrêt.",
        ),
        "EB10": (
            "Dès ce panneau, quelle limitation s'applique, sauf indication contraire ?",
            ["50 km/h", "30 km/h", "70 km/h", "80 km/h"],
            "a",
            "L'entrée d'agglomération vaut 50 km/h même sans panneau rond « 50 ».",
        ),
        "EB20": (
            "Ce panneau signifie :",
            [
                "Sortie d'agglomération : la limitation hors agglo reprend",
                "Entrée d'agglomération : 50 km/h",
                "Fin d'autoroute",
                "Début de zone 30",
            ],
            "a",
            "Le panneau de commune barré marque la sortie d'agglomération.",
        ),
        "B12": (
            "Que signifie ce panneau ?",
            [
                "Une limitation de hauteur a 3,5 m",
                "L'acces est interdit aux motocyclettes",
                "L'acces est interdit aux cyclomoteurs",
                "Une limitation de vitesse a 35 km/h",
            ],
            "a",
            "B12 = hauteur maximale 3,5 m. L'interdiction aux motos est le B9h.",
        ),
        "B9h": (
            "Ce panneau concerne-t-il une motocyclette ?",
            [
                "Oui, l'acces est interdit aux motocyclettes",
                "Non, il vise seulement les cyclomoteurs",
                "Non, il vise les velos",
                "Oui, mais seulement les motos de plus de 125 cm3",
            ],
            "a",
            "Le pictogramme moto (B9h) barre l'acces aux motocyclettes, quelle que soit la cylindree.",
        ),
        "B1": (
            "Pouvez-vous emprunter cette voie à moto ?",
            [
                "Non, c'est un sens interdit",
                "Oui, les deux-roues y sont autorisés",
                "Oui, en dessous de 30 km/h",
                "Oui, uniquement de jour",
            ],
            "a",
            "Le sens interdit s'applique à tous les véhicules, moto comprise, sauf panonceau contraire.",
        ),
        "AB6": (
            "Sur une route signalée par ce losange, vous êtes :",
            [
                "Prioritaire jusqu'à un panneau de fin ou une autre prescription",
                "Toujours tenu à la priorité à droite",
                "Dans une zone 30",
                "Sur une autoroute",
            ],
            "a",
            "Le losange jaune indique une route prioritaire.",
        ),
        "B44": (
            "En zone de rencontre, la vitesse maximale est de :",
            ["20 km/h", "30 km/h", "50 km/h", "Allure du pas uniquement pour les motos"],
            "a",
            "Zone de rencontre : 20 km/h, piétons prioritaires y compris sur la chaussée.",
        ),
        "B41": (
            "En zone 30, un motard peut-il rouler à 50 km/h s'il n'y a personne ?",
            [
                "Non, la limite est 30 km/h dans toute la zone",
                "Oui, si la chaussée est dégagée",
                "Oui, hors heures d'école",
                "Oui, car la moto est plus étroite",
            ],
            "a",
            "La zone 30 s'applique à tous les véhicules, tout le temps, jusqu'au panneau de fin.",
        ),
        "C107": (
            "Ce panneau annonce :",
            [
                "Le début d'une autoroute",
                "Une route nationale prioritaire",
                "Une zone 30",
                "Un parking relais",
            ],
            "a",
            "Le « A » blanc sur fond bleu marque l'entrée d'autoroute.",
        ),
        "A4": (
            "À moto, face à une chaussée glissante, le bon réflexe est :",
            [
                "Réduire l'allure et éviter les à-coups de frein ou de gaz",
                "Se mettre sur l'angle pour mieux mordre",
                "Freiner uniquement de l'avant",
                "Augmenter légèrement la vitesse pour plus de stabilité",
            ],
            "a",
            "L'adhérence chute : on allonge les distances et on lisse la conduite.",
        ),
        "A9": (
            "Comment franchir des rails de tramway à moto ?",
            [
                "Le plus perpendiculairement possible, sans freiner dessus",
                "En suivant le rail pour plus de guidage",
                "En inclinant fortement pour raccourcir",
                "En accélérant à fond pour « sauter » le rail",
            ],
            "a",
            "Le rail est un piège d'adhérence. Angle proche de 90°, allure stable, pas de freinage sur le métal.",
        ),
        "A24": (
            "Sur une zone de gravillons, à moto il faut :",
            [
                "Garder la moto droite, allure réduite, sans à-coups",
                "Incliner pour que le pneu « coupe » le gravier",
                "Freiner fort de l'avant pour nettoyer la bande de roulement",
                "Suivre exactement les traces d'un poids lourd",
            ],
            "a",
            "Les gravillons font patiner. On reste droit et souple sur les commandes.",
        ),
        "B6d": (
            "Ce panneau interdit :",
            [
                "L'arrêt et le stationnement",
                "Seulement le stationnement de plus de 5 minutes",
                "Seulement le stationnement des voitures",
                "La circulation des motos",
            ],
            "a",
            "Croix rouge : ni arrêt, ni stationnement, pour tous les véhicules.",
        ),
        "B3": (
            "Ce panneau vous interdit :",
            [
                "De dépasser un véhicule à moteur",
                "De dépasser un cycliste uniquement",
                "De changer de file à l'arrêt",
                "De klaxonner",
            ],
            "a",
            "Interdiction de dépasser les véhicules à moteur. Un cycliste n'est pas un véhicule à moteur.",
        ),
    }
    spec = mapping.get(code)
    if not spec:
        return None
    question, choices, correct, expl = spec
    return q("tmp", "signalisation", question, choices, correct, expl, sign_path(code), title)


def knowledge_questions():
    items = []

    def add(cat, question, choices, correct, expl, image=None, alt="", multi=False):
        items.append(q(f"{cat}-{len(items)+1:03d}", cat, question, choices, correct, expl, image, alt, multi))

    # --- ROUTE ---
    add("route", "Sur chaussée mouillée, la distance de freinage d'une moto :",
        ["Est nettement plus longue qu'à sec", "Reste identique grâce aux pneus moto", "Est plus courte car la moto est légère", "Ne change que la nuit"],
        "a", "L'eau réduit l'adhérence. La distance de freinage s'allonge fortement, surtout au début de la pluie (film gras).")
    add("route", "Les plaques d'égout, bandes blanches et rails sont dangereux à moto surtout :",
        ["Quand ils sont humides, car ils deviennent très glissants", "Uniquement en virage à gauche", "Uniquement à plus de 90 km/h", "Jamais, le pneu moto les « avale »"],
        "a", "Les surfaces peintes ou métalliques perdent presque toute adhérence sous la pluie.")
    add("route", "La trajectoire de sécurité dans un virage consiste à :",
        ["Ralentir avant, se placer à l'extérieur, regarder la sortie, puis se replacer", "Couper la corde comme sur circuit", "Freiner fort en pleine inclinaison", "Rester au milieu de la chaussée sans regarder"],
        "a", "Extérieur ? visibilité maximale ? replacer. On ne coupe pas la corde sur route ouverte.",
        "assets/img/illustrations/trajectoire.svg", "Schéma de trajectoire de sécurité")
    add("route", "Pourquoi ne doit-on pas « couper la corde » sur route ?",
        ["On empiète sur la voie opposée et on voit moins loin dans le virage", "Cela use trop le pneu arrière", "C'est interdit seulement sur autoroute", "Cela fait caler le moteur"],
        "a", "La trajectoire circuit expose au choc frontal et cache la sortie du virage.")
    add("route", "Des feuilles mortes sur la chaussée :",
        ["Peuvent cacher un trou et glisser comme de la glace", "Améliorent l'adhérence", "Ne concernent que les voitures", "Imposent seulement d'allumer le warning"],
        "a", "Feuilles = piège d'adhérence et de masquage. On traite comme une chaussée glissante.")
    add("route", "En cas de visibilité inférieure à 50 mètres (brouillard dense) :",
        ["La vitesse maximale est de 50 km/h sur toutes les routes", "On peut rester à 130 km/h sur autoroute si les feux sont allumés", "La limite passe à 90 km/h", "Il n'y a pas de règle, seulement un conseil"],
        "a", "Visibilité < 50 m : 50 km/h partout, autoroute comprise.")
    add("route", "Le « film gras » en début de pluie est dû :",
        ["Au mélange eau + hydrocarbures déposés sur la chaussée", "À une illusion d'optique", "Uniquement au savon des stations de lavage", "Au refroidissement des pneus"],
        "a", "Les premières minutes de pluie sont souvent les plus glissantes.")
    add("route", "Pour franchir un dos-d'âne à moto :",
        ["Arriver droit, allure réduite, alléger l'avant, ne pas freiner dessus", "Le prendre en biais pour « lisser »", "Accélérer pour que la suspension l'absorbe", "Se coucher sur le réservoir et freiner"],
        "a", "Un dos-d'âne pris en biais ou freiné peut faire chuter.")
    add("route", "Les bandes de rumble strips / rumble (bandes rugueuses) :",
        ["Peuvent déstabiliser la moto : on les évite si possible", "Sont faites pour augmenter l'adhérence moto", "Doivent être suivies pour se guider", "Interdisent la circulation des deux-roues"],
        "a", "Les bandes rugueuses secouent la direction. On les évite sans faire d'écart brutal.")
    add("route", "La nuit, un motard est plus vulnérable car :",
        ["Il est moins visible et juge plus mal les distances", "Les phares moto sont interdits", "Le code impose 30 km/h", "Les rétroviseurs ne fonctionnent plus"],
        "a", "Petite signature visuelle + fatigue + contraste. Gilet, feux, allure adaptée.")
    add("route", "Sur une chaussée déformée (ornières, nid-de-poule), le bon choix est :",
        ["Allure réduite, regard loin, éviter de braquer dans le trou", "Se jeter dans l'ornière pour « se caler »", "Freiner d'urgence dans le trou", "Fermer les yeux et accélérer"],
        "a", "On ralentit avant l'obstacle et on le franchit droit.")
    add("route", "Un vent latéral violent, surtout au débouché d'un camion ou d'un pont :",
        ["Peut déporter la moto : on anticipe en fermant les gaz et en se préparant", "N'a aucun effet grâce à l'effet gyroscopique", "Oblige à se coucher côté vent", "Impose d'arrêter au milieu de la voie"],
        "a", "Le souffle d'un PL ou un vent de travers décale la moto. On se prépare au coup de raffale.")
    add("route", "En descente longue, pour préserver les freins :",
        ["Utiliser le frein moteur (rapport inférieur) et des freinages brefs", "Rester freiné en continu sur le levier", "Passer au point mort", "Couper le contact"],
        "a", "Le freinage continu échauffe liquide et plaquettes. Le frein moteur aide.")
    add("route", "Un marquage au sol (flèches, zébras) mouillé :",
        ["Est glissant : on évite de freiner ou d'incliner dessus", "Offre plus de grip qu'un enrobé", "Doit être suivi en y collant le pneu", "Interdit le passage des motos"],
        "a", "La peinture routière est un savon dès qu'elle est humide.")
    add("route", "La position sur la voie en ligne droite, hors dépassement, vise surtout à :",
        ["Être vu et voir, tout en gardant une marge vers les portes et les nids-de-poule", "Coller la ligne médiane en permanence", "Rouler dans le caniveau", "Changer de position toutes les 2 secondes"],
        "a", "Le placement « de visibilité » n'est pas le milieu systématique ni le bas-côté.")
    add("route", "Un animal traverse : le réflexe à moto est :",
        ["Freiner en restant le plus droit possible, klaxonner si utile, éviter l'écart brutal", "Se jeter dans le fossé immédiatement", "Accélérer pour passer avant", "Coucher la moto volontairement"],
        "a", "Un écart brutal à moto fait souvent plus de dégâts que le petit animal.")
    add("route", "En travaux, une chaussée en gravillons ou fraisage :",
        ["Impose une allure très réduite et une moto droite", "Peut se passer à allure normale si on est léger", "N'est dangereuse que pour les voitures", "Autorise à dépasser par la droite"],
        "a", "Le fraisage et les gravillons sont parmi les pièges les plus chutogènes.")
    add("route", "Le regard à moto « tire » la trajectoire. Donc dans un virage on regarde :",
        ["Loin, vers la sortie du virage", "Le bord immédiat de la roue avant", "Le rétroviseur gauche en continu", "Le compteur"],
        "a", "On va où l'on regarde. Fixer l'obstacle, c'est le viser.")
    add("route", "Une flaque d'eau stagnante peut cacher :",
        ["Un nid-de-poule et provoquer un aquaplaning", "Un radar", "Une priorité à droite", "Un passage piéton"],
        "a", "On ne fonce pas dans une flaque : on ne sait pas ce qu'il y a dessous.")
    add("route", "Par grand froid, l'adhérence :",
        ["Baisse (pneus froids, possible verglas d'ombre)", "Augmente car l'air est plus dense", "Ne change pas", "N'est un sujet que sous 0 °C strict à l'ombre"],
        "a", "Pneus sous-gonflés à froid, bitume froid, plaques de verglas à l'ombre : triple piège.")

    # --- CIRCULATION ---
    add("circulation", "En France, le seuil de réussite de l'ETM (code moto) est :",
        ["35 bonnes réponses sur 40", "32/40", "40/40", "30/40"],
        "a", "Format 2026 inchangé : 40 questions, 5 fautes maximum, environ 30 minutes.")
    add("circulation", "Les limitations de vitesse d'une moto sont-elles plus basses que celles d'une voiture ?",
        ["Non, les limites générales sont les mêmes", "Oui, -20 km/h partout", "Oui, uniquement hors agglo", "Oui, uniquement sur autoroute"],
        "a", "Moto et voiture partagent les mêmes maxima légaux, sauf signalisation particulière.")
    add("circulation", "Hors agglomération, sur une route bidirectionnelle sans séparateur, la limite générale est souvent :",
        ["80 km/h (90 km/h sur certaines sections départementales)", "110 km/h", "70 km/h pour les motos", "130 km/h"],
        "a", "80 km/h depuis 2018, avec dérogations à 90 km/h selon les départements et sections.")
    add("circulation", "Sur autoroute par temps sec, conducteur confirmé :",
        ["130 km/h", "110 km/h", "150 km/h", "90 km/h"],
        "a", "130 km/h par temps sec. 110 sous la pluie, et 110 aussi en permis probatoire.")
    add("circulation", "Sous la pluie, sur une autoroute limitée à 130 par temps sec :",
        ["110 km/h", "130 km/h si les pneus sont neufs", "100 km/h", "90 km/h"],
        "a", "Pluie : 110 sur autoroute 130, 100 sur 2×2 voies 110. L'agglo reste à 50.")
    add("circulation", "Un conducteur en permis probatoire sur autoroute (temps sec) est limité à :",
        ["110 km/h", "130 km/h", "90 km/h", "80 km/h"],
        "a", "Permis de moins de 3 ans (ou 2 ans après conduite accompagnée) : 110 / 100 / 80.")
    add("circulation", "La circulation inter-files est autorisée en France depuis le 11 janvier 2025 :",
        ["Sur autoroutes et 2×2 voies séparées, VMA 70 à 130 km/h, sous conditions", "Partout, y compris en centre-ville", "Uniquement en Île-de-France", "Uniquement la nuit"],
        "a", "Décret du 9 janvier 2025 : pratique encadrée, pas une liberté totale.",
        "assets/img/illustrations/interfiles.svg", "Schéma de circulation inter-files")
    add("circulation", "En inter-files, la vitesse maximale du motard est de :",
        ["50 km/h, et 30 km/h si une des files est à l'arrêt", "70 km/h", "80 km/h", "La même que la file la plus rapide"],
        "a", "50 km/h max. 30 km/h si une file est à l'arrêt. On reprend sa place dès que ça fluidifie.")
    add("circulation", "L'inter-files se pratique :",
        ["Entre les deux files les plus à gauche", "Entre n'importe quelles files", "Uniquement à droite, près de la bande d'arrêt d'urgence", "Sur la bande d'arrêt d'urgence"],
        "a", "Toujours entre les deux files les plus à gauche. Interdit de dépasser un autre 2RM déjà en CIF.")
    add("circulation", "Peut-on pratiquer l'inter-files en agglo sur une rue à une voie ?",
        ["Non", "Oui, à 30 km/h", "Oui, si les voitures sont à l'arrêt", "Oui, le week-end"],
        "a", "Hors des voiries 2×2 (ou assimilées) séparées par un TPC, c'est interdit.")
    add("circulation", "Au STOP :",
        ["Arrêt obligatoire, puis s'engager si la voie est libre", "Ralentir suffit si personne n'arrive", "Un deux-roues peut « filer » car il tient moins de place", "S'arrêter seulement si un radar est visible"],
        "a", "L'arrêt au STOP n'est pas optionnel.")
    add("circulation", "En l'absence de signalisation, à une intersection en France :",
        ["Priorité à droite", "Priorité à gauche", "Le plus gros véhicule passe", "Le plus rapide passe"],
        "a", "Règle générale : priorité à droite, sauf cédez-le-passage, STOP, feux, route prioritaire, giratoire.")
    add("circulation", "Dans un giratoire à la française, on cède le passage :",
        ["Aux usagers déjà engagés dans l'anneau", "À ceux qui arrivent à droite à l'extérieur", "À personne, on est prioritaire en y entrant", "Uniquement aux poids lourds"],
        "a", "Cédez-le-passage à l'anneau. On signale sa sortie et on ne s'arrête pas dans l'anneau sans nécessité.")
    add("circulation", "Pour dépasser à moto hors agglo, il faut notamment :",
        ["Une visibilité suffisante, aucun marquage interdit, et une accélération franche puis un rabattement sûr", "Klaxonner d'abord, c'est obligatoire", "Toujours dépasser par la droite", "Coller le véhicule 1 mètre avant de déboîter"],
        "a", "On ne reste pas dans l'angle mort. On s'écarte, on accélère, on se rabat sans couper.")
    add("circulation", "La distance de sécurité derrière un véhicule, par temps sec, est souvent enseignée comme :",
        ["Au moins 2 secondes (davantage à moto et sous la pluie)", "Un mètre par km/h", "La longueur de la moto", "Inutile à moto car on freine mieux"],
        "a", "2 secondes minimum. À moto, on augmente encore : on n'a pas de carrosserie.")
    add("circulation", "Dépasser un cycliste :",
        ["En le serrant, on risque de le déstabiliser : il faut un écart latéral important", "1 cm suffit, le casque protège", "On peut le frôler en agglo", "Il faut klaxonner longuement juste derrière"],
        "a", "La loi impose un écart d'au moins 1 m en agglo et 1,50 m hors agglo lors du dépassement d'un cycliste.")
    add("circulation", "Un feu orange :",
        ["S'arrêter si on peut le faire sans danger ; sinon s'engager car s'arrêter serait plus dangereux", "Accélérer pour passer coûte que coûte", "S'arrêter même si un véhicule nous colle et que le freinage serait un choc", "Ignorer, le orange n'existe pas pour les motos"],
        "a", "Orange = arrêt sauf si l'arrêt crée un danger plus grand.")
    add("circulation", "Franchir une ligne continue pour dépasser :",
        ["Est interdit (sauf cas très encadrés, ex. obstacle immobile)", "Est autorisé à moto car on est étroit", "Est autorisé sous 50 km/h", "Est autorisé si on met le clignotant"],
        "a", "La ligne continue interdit le franchissement. L'étroitesse de la moto ne crée pas d'exception.")
    add("circulation", "Sur autoroute, la bande d'arrêt d'urgence :",
        ["Est réservée à l'arrêt d'urgence, pas à la circulation ni à l'inter-files", "Peut servir à dépasser", "Est une voie pour motos lentes", "Sert de file de droite supplémentaire"],
        "a", "Circuler sur la BAU est une infraction, sauf nécessité absolue.")
    add("circulation", "Le clignotant à moto :",
        ["Doit être mis assez tôt, et coupé après la manuvre", "Est facultatif car on est visible", "Ne se met qu'en agglo", "Remplace le contrôle dans les angles morts"],
        "a", "Signaler ? avoir le droit. Contrôle visuel + clignotant.")
    add("circulation", "Stationner une moto sur un trottoir :",
        ["Est interdit sauf aménagement ou autorisation locale", "Est toujours autorisé si la moto est sur la béquille", "Est obligatoire pour ne pas gêner les voitures", "Est autorisé la nuit"],
        "a", "Le trottoir est pour les piétons. Sauf arrêté local, on ne s'y gare pas.")
    add("circulation", "Un radar pédagogique (smiley) :",
        ["N'est pas une limitation : on respecte le panneau de prescription", "Autorise 10 km/h de plus", "Remplace le code de la route", "Oblige à s'arrêter"],
        "a", "Seuls les panneaux de prescription s'imposent. Le smiley informe.")
    add("circulation", "En agglo, sauf signalisation contraire, la vitesse max est :",
        ["50 km/h", "70 km/h", "30 km/h partout en France depuis 2026", "80 km/h"],
        "a", "50 km/h. De nombreuses villes ont des zones 30, mais ce n'est pas encore la règle nationale unique.")
    add("circulation", "Doubler par la droite un véhicule qui n'est pas à l'arrêt et n'est pas en file :",
        ["Est interdit", "Est recommandé à moto", "Est obligatoire en inter-files ville", "Est autorisé si on klaxonne"],
        "a", "On dépasse par la gauche. L'inter-files n'est pas un dépassement par la droite en ville.")
    add("circulation", "Lorsque le trafic se fluidifie en inter-files (files > 50 km/h) :",
        ["On doit reprendre une place dans une voie", "On peut rester entre les files à 90 km/h", "On se met sur la BAU", "On s'arrête"],
        "a", "La CIF cesse dès que le flux n'est plus saturé / lent.")

    # --- CONDUCTEUR ---
    add("conducteur", "Le taux d'alcoolémie maximal autorisé pour un conducteur confirmé est :",
        ["0,5 g/l de sang (0,25 mg/l d'air expiré)", "0,8 g/l", "0,2 g/l", "1,0 g/l"],
        "a", "0,5 g/l pour un permis définitif. 0,2 g/l en permis probatoire et pour certains conducteurs de transport.")
    add("conducteur", "En permis probatoire, le taux d'alcool maximal est :",
        ["0,2 g/l de sang (quasi zéro verre)", "0,5 g/l", "0,8 g/l", "Aucun, l'alcool est interdit seulement aux moins de 18 ans"],
        "a", "0,2 g/l : un seul verre peut suffire à dépasser. Le plus sûr est zéro alcool.")
    add("conducteur", "Alcool + moto, le vrai danger spécifique est :",
        ["L'équilibre, le temps de réaction et la prise de risque se dégradent très vite", "L'alcool n'a d'effet qu'en voiture", "L'alcool améliore la relaxation et donc l'inclinaison", "Seuls les spiritueux comptent, pas la bière"],
        "a", "À moto, un léger trouble de l'équilibre suffit à chuter.")
    add("conducteur", "Cannabis, médicaments somnolents, fatigue :",
        ["Interdisent ou rendent dangereuse la conduite, même « pour un court trajet »", "Sont sans effet sur une moto automatique", "Sont compensés par le café", "Ne concernent que la nuit"],
        "a", "Stupéfiants = infraction. Médicaments pictogramme rouge = ne pas conduire.")
    add("conducteur", "Le temps de réaction moyen d'un conducteur vigilant est d'environ :",
        ["1 seconde", "0,1 seconde", "5 secondes", "10 secondes"],
        "a", "Environ 1 s. À 50 km/h, on parcourt déjà ~14 m avant de commencer à freiner.")
    add("conducteur", "Téléphoner en tenant le combiné à moto :",
        ["Est interdit et particulièrement dangereux", "Est autorisé à l'arrêt au feu", "Est autorisé avec un casque Bluetooth non homologué n'importe comment", "Est recommandé pour le GPS vocal"],
        "a", "Le combiné en main est interdit. Même un kit, à moto, capte trop d'attention.")
    add("conducteur", "La fatigue à moto se manifeste souvent par :",
        ["Coups de volant/guidon, paupières lourdes, retards de freinage", "Une envie d'accélérer", "Une meilleure concentration", "Une baisse du régime moteur"],
        "a", "Dès les signes, on s'arrête. Le café ne « soigne » pas une dette de sommeil.")
    add("conducteur", "Un trajet « de 2 km pour rentrer » après un verre de trop :",
        ["Est illégal et tout aussi dangereux : la chute peut arriver au premier rond-point", "Est toléré par le code", "N'est dangereux qu'après 10 km", "Est plus sûr à moto qu'en voiture"],
        "a", "La majorité des accidents alcool ont lieu près du lieu de consommation.")
    add("conducteur", "Porter des lunettes de vue si on en a besoin :",
        ["Est obligatoire pour conduire si le permis le mentionne", "Est facultatif à moto grâce au visière", "Est interdit sous le casque", "N'est utile que la nuit"],
        "a", "Mention du permis = obligation. Une visière ne corrige pas la myopie.")
    add("conducteur", "Un médicament avec pictogramme rouge (niveau 3) :",
        ["Contre-indique la conduite", "Autorise la conduite de jour", "Autorise la moto mais pas la voiture", "N'a d'effet que 5 minutes"],
        "a", "Niveau 3 : ne pas conduire. Niveau 2 : être très prudent. Lire la notice.")
    add("conducteur", "Le stress ou la colère au guidon :",
        ["Augmentent les prises de risque et les erreurs de trajectoire", "Améliorent le temps de réaction", "Sont sans effet sur une moto", "Sont un motif de priorité"],
        "a", "On décélère, on respire, on ne « règle » rien dans le trafic.")
    add("conducteur", "Écouter de la musique très fort dans le casque :",
        ["Masque les sirènes, klaxons et le moteur : à éviter", "Est obligatoire pour rester éveillé", "Améliore la concentration", "Est exigé par l'ETM"],
        "a", "Entendre l'environnement fait partie de la sécurité à moto.")
    add("conducteur", "Conduire après une nuit blanche :",
        ["Peut équivaloir à une alcoolémie dangereuse en termes de vigilance", "N'a d'effet qu'après 4 heures de route", "Est compensé par l'adrénaline moto", "Est plus sûr car il y a moins de monde à 5 h"],
        "a", "La privation de sommeil dégrade le jugement comme l'alcool.")
    add("conducteur", "Un motard novice doit particulièrement :",
        ["Anticiper plus, viser des marges plus grandes, refuser la précipitation", "Imiter les trajectoires des plus rapides", "Rouler sans gants « pour le feeling »", "Désactiver l'ABS s'il y en a un"],
        "a", "L'ETM et la pratique visent la conduite défensive, pas la performance.")
    add("conducteur", "Le permis A2 limite la moto à :",
        ["35 kW (47,5 ch) et un rapport puissance/poids ? 0,2 kW/kg", "125 cm³ uniquement", "15 kW", "Aucune limite de puissance"],
        "a", "A2 dès 18 ans : 35 kW max. Le A « plein » vient après 2 ans et une formation.")

    # --- USAGERS ---
    add("usagers", "La règle d'or de l'angle mort d'un PL :",
        ["Si vous ne voyez pas le chauffeur dans son rétroviseur, il ne vous voit pas", "Le chauffeur voit toujours une moto", "L'angle mort n'existe qu'à droite", "Klaxonner suffit à se rendre visible"],
        "a", "On ne stagne jamais le long d'un camion.",
        "assets/img/illustrations/angle-mort.svg", "Angles morts d'un poids lourd")
    add("usagers", "Pour être vu d'une voiture qui s'apprête à tourner :",
        ["Éviter l'angle mort, se décaler, s'attendre à ce qu'elle ne vous ait pas vu", "Coller son pare-chocs", "Passer très vite pour « surprendre »", "Compter sur la couleur noire du blouson"],
        "a", "« SMIDSY » : Sorry Mate I Didn't See You. On conduit comme si on était invisible.")
    add("usagers", "Un piéton s'engage sur un passage :",
        ["Il est prioritaire : on s'arrête", "On accélère pour passer avant", "On le contourne par la gauche sans ralentir", "Il n'est prioritaire que s'il a un gilet"],
        "a", "Passage piéton = priorité au piéton engagé ou qui manifeste l'intention d'après le contexte, et obligation de prudence.")
    add("usagers", "Un enfant au bord du trottoir :",
        ["Peut surgir : on couvre le frein et on réduit l'allure", "Est toujours tenu par un adulte", "N'est un risque que près des écoles", "On klaxonne longuement en continu"],
        "a", "L'enfant ne maîtrise pas le danger. Allure qui permet l'arrêt.")
    add("usagers", "Cohabiter avec un cycliste :",
        ["Écart latéral, pas de souffle de dépassement, pas de klaxon agressif", "Le coller pour qu'il se décale", "Le dépasser dans un virage sans visibilité", "Lui passer sous le nez au feu"],
        "a", "Le cycliste est vulnérable. 1 m / 1,50 m d'écart selon agglo / hors agglo.")
    add("usagers", "Un bus s'arrête pour des voyageurs :",
        ["Des piétons peuvent traverser devant ou derrière : grande prudence", "On le double toujours à fond", "On se faufile à droite du trottoir", "Le bus n'a jamais la priorité"],
        "a", "En agglo, des règles spécifiques existent selon que le bus quitte un arrêt. Dans tous les cas, prudence maximale.")
    add("usagers", "Les feux de jour / feux de croisement à moto :",
        ["Aident à être vu, mais ne dispensent pas d'un bon placement", "Rendent invisible l'angle mort des autres", "Sont interdits le jour", "Remplacent le gilet"],
        "a", "Être éclairé ? être vu. Placement + couleur claire + anticipation.")
    add("usagers", "Un véhicule ouvre sa portière (dooring) :",
        ["Risque majeur en ville : on ne rase pas la file de voitures stationnées", "N'arrive jamais du côté passager", "Est un risque seulement pour les vélos", "Se règle en accélérant"],
        "a", "On laisse une marge égale à une portière le long des voitures garées.")
    add("usagers", "Un piéton malvoyant ou une personne âgée :",
        ["Peut mettre plus de temps : on attend qu'il ait fini de traverser", "On le presse au klaxon", "On le contourne de très près", "Il doit courir, c'est le code"],
        "a", "La patience fait partie de la sécurité routière.")
    add("usagers", "Se faufiler entre deux files de voitures en centre-ville hors cadre légal CIF :",
        ["Est interdit et très accidentogène (portières, piétons, angles morts)", "Est un droit du motard", "Est obligatoire pour fluidifier", "Est autorisé à 20 km/h"],
        "a", "L'inter-files légal ne couvre pas les rues urbaines classiques.")
    add("usagers", "Un poids lourd à l'approche d'un giratoire :",
        ["Peut empiéter largement : on ne se colle pas à sa droite", "Tourne toujours court", "Voit parfaitement sa roue arrière droite", "Doit nous laisser 2 mètres par la loi du plus faible"],
        "a", "On laisse au PL la place de ses roues arrière. Jamais à l'intérieur du virage d'un semi.")
    add("usagers", "Klaxonner :",
        ["Sert à prévenir d'un danger, pas à exprimer sa colère", "Est autorisé la nuit en ville pour « réveiller »", "Est obligatoire avant chaque dépassement", "Remplace le freinage"],
        "a", "Usage abusif = infraction. Un coup bref pour alerter, pas une fusillade.")
    add("usagers", "Un animal d'assistance ou un cavalier :",
        ["On ralentit fortement, large écart, pas de bruit brutal", "On accélère pour passer vite", "On doit klaxonner pour écarter l'animal", "On les dépasse comme une voiture"],
        "a", "Un cheval peut cabrer. Allure réduite, large, silencieux.")
    add("usagers", "La meilleure couleur de blouson pour être vu :",
        ["Couleurs claires ou fluo, contrastées", "Noir mat intégral", "Camouflage", "Transparent"],
        "a", "Le noir est élégant et peu visible. Le fluo sauve des vies le jour.")
    add("usagers", "À un passage à niveau, un motard doit :",
        ["Ne jamais s'engager si les feux clignotent, même « pour passer juste avant »", "Se faufiler sous la barrière", "Suivre une voiture qui force", "S'arrêter sur les rails pour mieux voir"],
        "a", "Un train ne peut pas vous éviter. En cas de calage sur les voies : on évacue la moto et on s'éloigne.")

    # --- DIVERS ---
    add("divers", "Pour circuler, une moto doit notamment être couverte par :",
        ["Une assurance responsabilité civile au minimum", "Une assurance tous risques obligatoire", "Aucune assurance si on reste sous 50 km/h", "La seule carte grise"],
        "a", "La RC est obligatoire. L'attestation / vignette doit pouvoir être présentée.")
    add("divers", "Documents à pouvoir présenter :",
        ["Permis, certificat d'immatriculation (ou copie), attestation d'assurance", "Seulement le permis", "Seulement une photo des papiers sur le téléphone, c'est toujours suffisant", "Le manuel d'atelier"],
        "a", "En pratique : permis + carte grise + assurance. Le téléphone peut aider mais n'a pas valeur dans tous les contrôles.")
    add("divers", "Le contrôle technique des deux-roues motorisés :",
        ["A été mis en place progressivement à partir de 2024 selon l'âge du véhicule", "N'existe pas en France", "Ne concerne que les 125", "Est annuel dès la sortie d'usine"],
        "a", "Le CT moto est entré en vigueur. Périodicité et échéances dépendent de la date de 1re mise en circulation.")
    add("divers", "En cas de panne sur autoroute, le motard :",
        ["Se gare le plus à droite, enfile le gilet, derrière la glissière si possible, et utilise la borne", "Reste sur sa moto, feux allumés, sur la voie de gauche", "Marche au milieu des voies pour être vu", "Répare sur la voie de droite"],
        "a", "Protéger d'abord. Le gilet jaune est fait pour ça.")
    add("divers", "Le triangle de pré-signalisation :",
        ["N'est pas adapté/obligatoire comme en voiture pour une moto ; le gilet et l'éloignement priment", "Doit être posé à 1 m de la moto", "Remplace l'appel des secours", "Est interdit"],
        "a", "On se met en sécurité, gilet, derrière une glissière, on alerte. On ne reste pas exposé pour « bien placer » un triangle.")
    add("divers", "Transporter un passager à moto :",
        ["Il doit avoir les pieds sur les repose-pieds, casque et gants, et la moto doit être homologuée 2 places", "Un enfant peut s'asseoir sur le réservoir", "Le passager n'a pas besoin de casque s'il tient le conducteur", "C'est interdit en A2"],
        "a", "Places homologuées, équipements obligatoires pour les deux, reposes-pieds.")
    add("divers", "Un passager mineur :",
        ["Doit pouvoir poser les pieds sur les repose-pieds ; un siège adapté peut être nécessaire", "Peut voyager debout sur les cale-pieds", "Est interdit jusqu'à 16 ans dans tous les cas", "N'a pas besoin de casque avant 12 ans"],
        "a", "Pieds sur les repose-pieds + casque homologué à sa taille. Pas de « bébé entre les bras ».")
    add("divers", "L'ETM est-elle exigée si l'on a déjà le permis B ?",
        ["Oui, plus de dispense : l'ETM est obligatoire pour A1/A2/A", "Non, le permis B de moins de 5 ans suffit", "Non, si on a plus de 10 ans de permis B", "Seulement pour le permis A"],
        "a", "Depuis 2020, code auto et code moto sont distincts. En 2026, tout candidat A1/A2/A passe l'ETM.")
    add("divers", "La validité de l'ETM une fois obtenue :",
        ["5 ans pour passer la pratique", "6 mois", "1 an", "Illimitée"],
        "a", "5 ans pour réussir le plateau et la circulation.")
    add("divers", "Le coût réglementé d'un passage de l'ETM est de l'ordre de :",
        ["30  par tentative", "Gratuit", "150 ", "10 "],
        "a", "30  à chaque passage, en centre agréé.")
    add("divers", "Permis A1 :",
        ["Motos jusqu'à 125 cm³ et 11 kW, dès 16 ans", "Toutes cylindrées dès 16 ans", "35 kW dès 16 ans", "Voiturettes"],
        "a", "A1 = 125 cm³ / 11 kW. A2 = 35 kW dès 18 ans.")
    add("divers", "Une plaque d'immatriculation moto :",
        ["Doit être lisible, homologuée, éclairée la nuit", "Peut être pliée pour faire « racing »", "Est facultative sur piste ouverte à la circulation", "Peut être cachée par un sacoche"],
        "a", "Plaque illisible = infraction. Pas de cache « fumé ».")
    add("divers", "Modifier un échappement pour le rendre très bruyant :",
        ["Est illégal (homologation, bruit, pollution) et verbalisable", "Est obligatoire pour être entendu", "Est toléré le week-end", "N'est un problème que hors agglo"],
        "a", "Ligne non homologuée = infraction, contrôle technique, et fléau pour l'image des motards.")
    add("divers", "Conduire une 125 cm³ avec le seul permis B :",
        ["Exige une formation de 7 h (sauf permis B avant 1980 selon les règles en vigueur)", "Est libre sans formation", "Exige l'ETM + permis A2", "Est interdit"],
        "a", "La formation 7 h n'est pas le permis moto. L'ETM + A1/A2 est un autre parcours.")
    add("divers", "En cas d'accident matériel sans blessé, on :",
        ["Remplit un constat, on ne quitte pas les lieux sans échanger, on se met en sécurité", "On part si on est pressé", "On attend la police dans tous les cas avant de bouger la moto même sur une voie rapide", "On avoue forcément par SMS seulement"],
        "a", "Sécurité des personnes d'abord, puis constat. Sur voie rapide, se protéger avant tout.")

    # --- MECANIQUE ---
    add("mecanique", "Avant de partir, un contrôle utile des pneus comprend :",
        ["Pression à froid, usure (témoins), coupures, objets incrustés", "Seulement la couleur de la gomme", "Un coup d'il une fois par an", "Le pneu avant seulement"],
        "a", "Pression à froid. Un pneu sous-gonflé chauffe, guide mal et peut éclater.")
    add("mecanique", "Un pneu moto sous-gonflé :",
        ["Allonge le freinage, chauffe et rend la direction imprecise", "Améliore le confort donc la sécurité", "Est recommandé sous la pluie", "N'a d'effet que sur autoroute"],
        "a", "Pression = sécurité n°1. On suit les préconisations du constructeur.")
    add("mecanique", "La chaîne de transmission :",
        ["Doit être lubrifiée, avec un jeu conforme, ni trop tendue ni trop lâche", "Doit être le plus tendue possible", "Se change uniquement à 100 000 km", "N'existe que sur les scooters"],
        "a", "Chaîne sèche = usure et casse. Trop tendue = roulements. Trop lâche = risque de saut.")
    add("mecanique", "Un témoin de frein / niveau de liquide bas :",
        ["Interdit de partir tant que ce n'est pas vérifié", "Peut attendre le prochain entretien annuel", "S'éteint tout seul en roulant", "Ne concerne que l'ABS"],
        "a", "Freins = vie. Fuite ou plaquettes finies = on ne roule pas.")
    add("mecanique", "L'ABS à moto :",
        ["Aide à éviter le blocage de roue, mais ne raccourcit pas magiquement sur graviers", "Autorise à freiner plus tard dans tous les cas", "Fonctionne très bien sur les gravillons", "Remplace l'apprentissage du freinage"],
        "a", "L'ABS est un filet, pas une excuse pour arriver trop vite.")
    add("mecanique", "Freinage d'urgence à moto :",
        ["Redresser, transférer, freiner des deux trains avec dosage, regard loin", "Frein arrière seul", "Jeter la moto pour glisser comme au cinéma", "Couper le contact"],
        "a", "Le frein avant fournit l'essentiel de la puissance, mais le dosage et l'arrière comptent. Pas d'angle.")
    add("mecanique", "Les feux (croisement, stop, clignotants) :",
        ["Se vérifient avant chaque départ", "Se vérifient chez le concessionnaire seulement", "Sont optionnels de jour", "Le stop n'est pas obligatoire à moto"],
        "a", "Une ampoule stop grillée = se faire rentrer dedans.")
    add("mecanique", "Le réglage des leviers et rétroviseurs :",
        ["Doit permettre un accès immédiat sans décroiser les mains ni le buste", "Est cosmétique", "Les rétros se règlent en roulant à 90", "On peut n'avoir qu'un rétro"],
        "a", "Deux rétros, bien réglés, leviers à portée. C'est du contrôle, pas du confort.")
    add("mecanique", "Une moto qui « broute » à l'accélération peut indiquer :",
        ["Une panne d'alimentation, un filtre, des bougies : on ne part pas en long trajet", "Un comportement normal à froid indéfiniment", "Qu'il faut monter dans les tours", "Un pneu trop gonflé uniquement"],
        "a", "On diagnostique à l'arrêt. Une panne au milieu d'une intersection est un accident en puissance.")
    add("mecanique", "Charger des sacoches trop lourd à l'arrière :",
        ["Allège l'avant, allonge le freinage, altère la direction", "Rend la moto plus plantée donc plus sûre", "N'a d'effet qu'au-delà de 200 km/h", "Compense un passager léger"],
        "a", "Respecter la charge max. Répartir, sangler, vérifier la pression (souvent + arrière).")
    add("mecanique", "L'éclairage : de nuit ou tunnel, on utilise :",
        ["Les feux de croisement (ou route hors croisement)", "Position seulement", "Les warnings en roulant", "Rien, le catadioptre suffit"],
        "a", "Croisement par défaut. Route dès que personne en face. Warnings = danger/arrêt, pas un mode de circulation.")
    add("mecanique", "Un témoin ABS ou moteur allumé après le démarreur :",
        ["Impose de consulter : un aide à la sécurité peut être inactif", "Est décoratif", "S'ignore si la moto avance", "Signifie qu'il faut rouler plus vite pour l'éteindre"],
        "a", "Un voyant rouge/orange persistant = pas un détail.")
    add("mecanique", "La béquille latérale :",
        ["Doit remonter et, sur beaucoup de motos, couper le moteur si elle reste sortie", "Peut rester sortie en roulant « pour le style »", "Remplace le frein de parking", "S'utilise en virage comme appui"],
        "a", "Partir béquille sortie = chute immédiate. Vérifier le cut-off.")
    add("mecanique", "Huile moteur : un niveau trop bas :",
        ["Peut détruire le moteur et faire caler au pire moment", "Améliore les performances", "N'est un souci que sur circuit", "Se voit uniquement à l'odeur"],
        "a", "Contrôle à froid ou selon notice, moto droite.")
    add("mecanique", "Un pneu usé jusqu'aux témoins :",
        ["Doit être changé : adhérence et évacuation d'eau insuffisantes", "Peut encore faire 10 000 km s'il est cher", "Se change seulement l'avant", "Est plus sûr sous la pluie car plus dur"],
        "a", "Témoins atteints = réforme. La pluie révèle les pneus lisses.")

    # --- PROTECTION ---
    add("protection", "Les équipements strictement obligatoires pour circuler à moto sont :",
        ["Casque homologué + gants certifiés CE, pour conducteur et passager", "Casque seulement", "Casque, blouson airbag et bottes", "Gilet airbag uniquement"],
        "a", "Obligatoire : casque + gants CE. Le gilet HV doit être à bord. Le reste est vital mais recommandé.",
        "assets/img/illustrations/equipement.svg", "Équipements du motard")
    add("protection", "Un casque non attaché :",
        ["C'est comme ne pas en avoir : infraction et inutile en choc", "Protège quand même par sa masse", "Est autorisé sous 50 km/h", "Est autorisé pour le passager"],
        "a", "Jugulaire bouclée, bien réglée. Un casque qui s'envole ne protège personne.")
    add("protection", "Norme de casque courante pour un casque neuf :",
        ["ECE 22.06 (les 22.05 restent visibles sur d'anciens casques encore utilisables selon leur état)", "CE jouet", "ISO 9001 seulement", "DOT uniquement sans ECE en Europe"],
        "a", "En Europe, homologation ECE. La 22.06 est la plus récente.")
    add("protection", "Les gants doivent porter :",
        ["Le marquage CE (norme EN 13594)", "Un logo de marque de course", "Rien, le cuir suffit", "Un QR code assurance"],
        "a", "Sans CE, ce n'est pas un gant « code ». Amende et point en cas de contrôle.")
    add("protection", "Le gilet de haute visibilité :",
        ["Doit être présent à bord et porté en cas d'arrêt d'urgence sur la chaussée", "Doit être porté en roulant en permanence sous peine de 6 points", "Est facultatif même en panne", "Remplace le casque la nuit"],
        "a", "À bord = obligatoire. Porté dès qu'on est à pied près de la chaussée.")
    add("protection", "Blouson, pantalon, bottes, dorsale :",
        ["Fortement recommandés (abrasion, fractures) mais pas imposés par le code comme le casque", "Inutiles en ville", "Interdits l'été", "Obligatoires uniquement sur autoroute"],
        "a", "L'ETM teste la nuance obligatoire / recommandé. La peau ne résiste pas au bitume.")
    add("protection", "Un casque intégral par rapport à un jet :",
        ["Protège le menton, zone souvent touchée à moto", "Protège moins car plus lourd", "Est interdit en A2", "Est réservé à la piste"],
        "a", "La majorité des chocs visent le visage. L'intégral est le meilleur compromis route.")
    add("protection", "Une visière rayée ou teintée très sombre la nuit :",
        ["Baisse la vision : à changer / relevée selon l'homologation", "Est plus sûre contre les phares", "Est obligatoire", "Filtre aussi l'alcoolémie"],
        "a", "Visibilité = sécurité. Visière de nuit claire, propre, antibuée.")
    add("protection", "Un airbag moto (gilet ou blouson) :",
        ["Réduit les lésions thorax/cou mais ne remplace ni casque ni gants", "Dispense du casque", "Est obligatoire depuis 2026", "Ne sert que sur circuit"],
        "a", "Excellent complément, pas un substitut aux obligations légales.")
    add("protection", "Prêter son casque à un passager :",
        ["Il doit être à sa taille, homologué, attaché ; un casque trop grand s'enlève au choc", "N'importe quel casque fait l'affaire", "Un casque vélo suffit sous 50 km/h", "Le passager peut tenir le casque à la main"],
        "a", "Taille et jugulaire. Un casque qui tourne ou tombe ne sert à rien.")
    add("protection", "Rouler en t-shirt l'été :",
        ["Légal si casque + gants, mais une chute à 40 km/h râpe la peau sur des mètres", "Est plus sûr car on a moins chaud donc plus lucide", "Est interdit par le code", "N'est dangereux qu'au-dessus de 90 km/h"],
        "a", "Le bitume brûle aussi à 40 km/h. Un blouson été aéré reste une armure.")
    add("protection", "Des chaussures montantes :",
        ["Protègent cheville et levier de vitesse ; les tongs sont une aberration", "Les tongs sont acceptées sous 50 km/h", "Les baskets filet suffisent toujours", "Les bottes sont interdites en A1"],
        "a", "Recommandé : chaussure qui tient la cheville. Obligatoire : non, mais le levier rentre dans un orteil nu.")
    add("protection", "Un casque après un choc violent (même tombé de la table parfois) :",
        ["Doit être réformé : la coque peut être fissurée invisiblement", "Se tape pour « rebondir » et reprend du service", "Se recouvre d'un sticker", "Se prête au passager"],
        "a", "Un casque, c'est une fois. Après un vrai choc, on le change.")
    add("protection", "L'homologation du casque se vérifie :",
        ["Sur l'étiquette intérieure (E suivi d'un numéro, circulaire)", "Sur la couleur", "Sur le prix", "Si le vendeur le dit oralement"],
        "a", "Étiquette ECE dans la calotte. Pas d'étiquette = pas d'homologation.")
    add("protection", "Amende typique pour défaut de casque :",
        ["Contravention de 4e classe et retrait de points", "Un simple rappel oral", "Une immobilisation sans amende", "Rien si on a les gants"],
        "a", "Casque : 4e classe + 3 points. Gants : 3e classe + 1 point.")

    # --- ENVIRONNEMENT ---
    add("environnement", "Un échappement « ouvert » en agglo :",
        ["Est une nuisance sonore verbalisable et fatigue les riverains", "Est un droit du motard pour être entendu", "Réduit le CO2", "Est obligatoire près des écoles"],
        "a", "Le bruit n'augmente pas la sécurité de façon proportionnelle ; il crée du rejet et des PV.")
    add("environnement", "L'éco-conduite à moto, c'est notamment :",
        ["Anticiper, éviter les accélérations inutiles, entretenir la chaîne et la pression", "Rester au régime max", "Couper le moteur en descente en roue libre, contact coupé", "Gonfler les pneus au double"],
        "a", "Souplesse = moins de conso, moins d'usure, moins de chutes.")
    add("environnement", "Jeter un masque / un gant / un déchet depuis la moto :",
        ["Est une infraction (abandon de déchets) et un danger pour les autres", "Est toléré à la campagne", "Est un droit si c'est biodégradable", "N'est verbalisable que sur autoroute"],
        "a", "On rentre avec ses déchets. Un objet sur la chaussée peut faire chuter un autre motard.")
    add("environnement", "Laisser tourner le moteur à l'arrêt longtemps :",
        ["Pollue et peut être sanctionné ; inutile pour « chauffer » des minutes entières", "Est obligatoire pour l'huile", "Chauffe mieux les pneus que de rouler souple", "Est demandé par l'ETM"],
        "a", "On part souple quelques kilomètres : pneus et moteur montent en température.")
    add("environnement", "La pression des pneus correcte :",
        ["Réduit la conso et l'usure, et améliore la sécurité", "N'a d'effet que sur le confort", "Augmente toujours la pollution", "Est un mythe de constructeur"],
        "a", "Éco et sécu vont ensemble sur ce point.")
    add("environnement", "Stationner sur un espace vert / une piste cyclable :",
        ["Est généralement interdit et dégrade l'espace commun", "Est un privilège deux-roues", "Est autorisé 5 minutes", "Est obligatoire pour ne pas prendre une place auto"],
        "a", "On cherche un emplacement autorisé. Les motos n'ont pas de droit de « grimper le trottoir ».")
    add("environnement", "Laver sa moto :",
        ["Évite de laisser couler hydrocarbures dans les égouts : un tapis / une station adaptés aident", "Se fait au jet haute pression sur les roulements sans précaution", "Impose le détergent le plus fort", "Est interdit"],
        "a", "L'entretien propre fait partie du respect de l'environnement.")
    add("environnement", "Choisir un itinéraire moins bruyant la nuit :",
        ["Est une forme de respect et limite les conflits", "Est ridicule, le code impose le chemin le plus court", "Oblige à prendre l'autoroute", "N'a de sens qu'en 125"],
        "a", "On peut rouler juste sans réveiller tout un quartier.")
    add("environnement", "Un filtre à air encrassé et une carburation mal réglée :",
        ["Augmentent pollution et conso", "Rendent la moto plus « verte »", "N'ont d'effet que sur le bruit", "Améliorent le couple"],
        "a", "L'entretien moteur est aussi écologique.")
    add("environnement", "Partager une aire d'autoroute :",
        ["On ne laisse pas d'huile au sol, on ne crie pas les gaz", "On fait un burnout pour « chauffer »", "On jette les gants usés dans les buissons", "On occupe 6 places auto « pour la moto »"],
        "a", "Le motard est un usager comme les autres, avec un impact parfois plus visible.")

    # --- SECOURS ---
    add("secours", "La conduite à tenir face à un accident :",
        ["Protéger, Alerter, Secourir (P.A.S.)", "Secourir d'abord, même au milieu de l'autoroute", "Filmer avant tout", "Déplacer immédiatement le blessé vers le fossé dans tous les cas"],
        "a", "On ne crée pas un second accident. D'abord la protection de la zone.")
    add("secours", "Protéger, concrètement :",
        ["Baliser, gilet, arrêter le trafic si besoin, couper le contact des véhicules", "Se garer n'importe comment sur la voie de gauche", "Rassembler les curieux au milieu", "Enlever tout de suite le casque de toutes les victimes"],
        "a", "Zone sûre > tout le reste. Sur autoroute : derrière la glissière.")
    add("secours", "Alerter : quel numéro d'urgence européen ?",
        ["112 (et 18 pompiers, 15 SAMU, 17 police)", "119 seulement", "113", "101"],
        "a", "112 fonctionne dans toute l'UE, même sans crédit / hors réseau opérateur parfois.")
    add("secours", "En appelant les secours, on précise surtout :",
        ["Lieu précis, nature du problème, nombre de victimes, circonstances, rappels possibles", "Seulement « y a un accident »", "Le prénom du blessé", "La cylindrée de la moto"],
        "a", "Le lieu (borne, PR, commune) est la donnée n°1.")
    add("secours", "Retirer le casque d'un motard blessé :",
        ["Uniquement si les voies aériennes l'exigent (et idéalement à deux, en maintenant la tête)", "Toujours, immédiatement", "Jamais, dans absolument tous les cas", "Seulement s'il est débouclé à moitié"],
        "a", "On ne retire pas le casque « pour voir ». Exception : victime qui ne respire pas / vomissements / nécessité vitale.")
    add("secours", "Une victime consciente, traumatisme possible :",
        ["On la parle, on la couvre, on ne la fait pas se relever « pour voir »", "On lui donne à boire", "On lui retire la bottine pour masser", "On la assoit de force"],
        "a", "Suspicion de traumatisme : on immobilise, on rassure, on attend les pros.")
    add("secours", "Saignement abondant :",
        ["Compression directe avec un linge, gants si possible, alerter", "Garrot d'abord dans tous les cas", "Alcool sur la plaie", "Asperger d'eau en continu"],
        "a", "Compression > tout. Le garrot est un geste enseigné pour des cas extrêmes.")
    add("secours", "Une victime ne respire pas, après protection et alerte :",
        ["Réanimation : massage cardiaque (et DEA si disponible)", "On attend sans rien faire 10 minutes", "On lui jette de l'eau au visage", "On lui donne un comprimé personnel"],
        "a", "Massage au centre de la poitrine, 100-120 / min. Le DEA guide la voix.")
    add("secours", "Brûlé (pot, pot d'échappement, bitume chaud) :",
        ["Refroidir à l'eau tiède/froide, ne pas percer les cloques, alerter si étendu", "Mettre du beurre", "Percer les cloques", "Retirer un vêtement collé en le déchirant à vif"],
        "a", "Eau, pas de graisse, pas de dentifrice. Les vêtements collés : les secours s'en chargent.")
    add("secours", "Position latérale de sécurité (PLS) :",
        ["Victime inconsciente qui respire, après bilan, pour libérer les voies aériennes", "Victime qui ne respire pas", "Fracture du rachis certaine, on tourne vite seul", "Systématique même si la victime parle et veut s'asseoir"],
        "a", "Inconscient + respire = PLS. Pas de PLS si RCP en cours.")
    add("secours", "Le rôle d'un témoin motard n'est PAS :",
        ["Déplacer une victime polytraumatisée « pour la mettre au frais » sans nécessité vitale", "Protéger la zone", "Alerter le 112", "Rassurer et couvrir"],
        "a", "On ne bouge une victime que si un danger vital immédiat l'exige (incendie, voie).")
    add("secours", "Un DEA (défibrillateur) :",
        ["S'utilise dès qu'il est disponible sur un adulte inconscient qui ne respire pas", "Est réservé aux médecins", "Doit être branché sur une victime consciente qui parle", "Remplace le massage"],
        "a", "Allumer, coller, écouter. Continuer le massage entre les chocs.")
    add("secours", "En tunnel, alerter :",
        ["Niches de sécurité, bornes, consignes affichées : on ne fait pas demi-tour en moto au milieu", "On fait demi-tour toutes voies", "On reste dans le tube à filmer", "On s'arrête dans la voie de gauche"],
        "a", "Suivre la signalisation d'évacuation. Les bornes joignent les secours du tunnel.")
    add("secours", "Une hémorragie + une moto au milieu de la voie :",
        ["On protège d'abord le lieu (ou on extrait si écrasement imminent), puis on soigne", "On soigne au milieu des voies en priorisant la plaie uniquement", "On recule la victime en la tirant par le casque", "On attend 20 minutes pour « ne pas aggraver » même si un PL arrive"],
        "a", "Le second choc (se faire rentrer dedans) tue autant que le premier. P.A.S.")
    add("secours", "Couvrir une victime :",
        ["Limite l'hypothermie, même l'été (choc)", "Est inutile", "Se fait avec de l'eau froide en continu", "Empêche les secours de travailler donc à éviter"],
        "a", "Couverture de survie, blouson, parole. Le choc refroidit.")

    # Extra particularités / sécurité mix
    add("circulation", "Un panneau B27a (voie de bus) sans panonceau moto :",
        ["La moto n'a pas le droit d'y circuler", "Toutes les motos y sont autorisées", "Seulement les 125", "Seulement en inter-files"],
        "a", "Sauf mention « motos autorisées » ou équivalent local, la voie de bus n'est pas pour nous.",
        sign_path("B27a"), "Voie réservée aux transports en commun")
    add("circulation", "Ce panneau d'entrée d'autoroute implique, par temps sec et permis définitif :",
        ["130 km/h max, 110 sous la pluie", "110 dans tous les cas", "90 km/h", "Pas de limite"],
        "a", "C107 = autoroute. 130 / 110 pluie / 110 probatoire.",
        sign_path("C107"), "Début d'autoroute")
    add("route", "Ce panneau doit vous faire :",
        ["Ralentir avant le virage et préparer une trajectoire de sécurité", "Accélérer pour « tendre » la moto", "Couper la corde", "Regarder le compteur"],
        "a", "Virage annoncé = allure réglée avant l'inclinaison.",
        sign_path("A1a"), "Virage à droite")
    add("protection", "Ce panneau vous concerne-t-il en moto de plus de 50 cm³ ?",
        ["Non, il vise les cyclomoteurs", "Oui, toutes les motos", "Oui, seulement les A2", "Oui, seulement sans ABS"],
        "a", "B9g = cyclomoteurs. Une moto n'est pas un cyclomoteur.",
        sign_path("B9g"), "Interdiction cyclomoteurs")
    add("usagers", "Face à ce panneau, un motard :",
        ["Réduit l'allure et se prépare à s'arrêter pour les piétons", "Accélère pour passer avant les piétons", "Klaxonne en continu", "Emprunte le trottoir"],
        "a", "Passage piétons annoncé : on couvre le frein.",
        sign_path("A13b"), "Passage pour piétons")
    add("divers", "Ce panneau :",
        ["Interdit l'accès aux motocyclettes", "Interdit les voitures seulement", "Interdit les vélos", "Indique une voie moto obligatoire"],
        "a", "B9h = motos interdites. Fréquent sur chemins, parcs, certaines allées.",
        sign_path("B9h"), "Accès interdit aux motocyclettes")

    # More circulation / security
    add("circulation", "À un feu tricolore en panne (éteint) :",
        ["L'intersection se traite comme non régulée : prudence, souvent priorité à droite", "On passe comme si c'était vert", "On s'arrête 3 minutes", "Les motos passent les premières"],
        "a", "Feu éteint = plus de régulation. On s'approche comme d'un carrefour dangereux.")
    add("circulation", "Un fléchage au sol dans une voie :",
        ["Impose la direction : on ne change plus de file au dernier moment", "Est indicatif seulement", "Concerne les voitures, pas les motos", "Autorise le contre-sens"],
        "a", "Marquage de direction dans l'intersection = on le suit.")
    add("conducteur", "Le cannabis peut rester détectable et :",
        ["La conduite après usage est un délit, avec dépistage possible", "N'est un problème que le soir même si on « ne sent plus rien »", "Est autorisé en dessous d'un verre de vin", "N'affecte que la voiture"],
        "a", "Zéro stupéfiant au guidon. Contrôle salivaire fréquent.")
    add("mecanique", "Freiner en virage, moto inclinée :",
        ["Risque de tomber : on freine avant, on relâche, on incline", "Est le meilleur moyen de rattraper une entrée trop vite", "Est recommandé par l'ABS sur graviers", "Se fait uniquement de l'avant à fond"],
        "a", "On règle l'allure avant le virage. Un freinage appuyé sur l'angle dérobe la roue.")
    add("route", "La trajectoire de sécurité exige-t-elle de chevaucher la ligne médiane ?",
        ["Non, on reste dans sa voie", "Oui, pour mieux voir", "Oui, en virage à gauche seulement", "Oui, hors agglo"],
        "a", "On ouvre la visibilité DANS sa voie, sans prendre celle d'en face.")
    add("usagers", "Un véhicule indique un changement de direction mais ne l'exécute pas encore :",
        ["On ne dépasse pas du côté où il a signalé", "On accélère dans le trou", "On le double à toucher", "On se met devant pour « l'aider »"],
        "a", "Le clignotant de l'autre est une information de danger, pas une invitation.")
    add("secours", "Numéro 18 :",
        ["Pompiers", "SAMU", "Police", "Urgences européennes uniquement"],
        "a", "18 pompiers, 15 SAMU, 17 police, 112 unique européen.")
    add("environnement", "Une accélération brutale à un feu, pour « le plaisir » :",
        ["Augmente bruit, conso, usure, et le risque d'être percuté ou de cabrer", "Est un exercice d'éco-conduite", "Chauffe correctement les pneus en 2 mètres", "Est demandée à l'examen pratique"],
        "a", "On part proprement. Le plateau n'est pas un dragster.")
    add("divers", "L'examen pratique moto (hors ETM) comporte notamment :",
        ["Des épreuves hors circulation (plateau) puis la circulation", "Uniquement un oral sur les panneaux", "Uniquement l'autoroute", "Un QCM de mécanique chez le concessionnaire"],
        "a", "ETM d'abord, puis plateau (parcours, freinage, slalom) et circulation.")
    add("protection", "Un tour de jugulaire mal réglé (trop lâche) :",
        ["Le casque peut s'arracher à l'impact", "Est plus confortable donc plus sûr", "Est obligatoire en été", "Compense un casque trop petit"],
        "a", "Deux doigts max sous la sangle, boucle verrouillée.")
    add("circulation", "En agglo, klaxonner pour « saluer » un autre motard :",
        ["N'est pas l'usage prévu du klaxon (signal de danger)", "Est obligatoire entre motards", "Remplace le clignotant", "Est exigé la nuit"],
        "a", "Un petit geste de la botte est plus correct qu'un coup de klaxon en ville.")
    add("route", "Un passage sur un marquage de passage piéton mouillé, moto inclinée :",
        ["Très glissant : on le franchit le plus droit possible", "La peinture accroche mieux que le bitume", "On accélère pour « gratter »", "On freine à fond dessus"],
        "a", "Les bandes blanches = patinoire humide.")
    add("mecanique", "Le feu de stop s'allume quand :",
        ["On actionne le levier avant et/ou la pédale arrière", "Uniquement le levier avant", "Uniquement au point mort", "Automatiquement au-dessous de 20 km/h"],
        "a", "Les deux commandes doivent allumer le stop. À vérifier avant de partir.")
    # Additional batch for volume
    extra = [
        ("circulation", "Chevaucher une ligne discontinue pour dépasser :",
         ["Est autorisé si toutes les autres conditions de dépassement sont réunies", "Est toujours interdit", "Est autorisé même avec une ligne continue en face dans tous les cas", "Est réservé aux voitures"],
         "a", "Ligne discontinue = franchissable. On vérifie visibilité, vitesse, face à face."),
        ("circulation", "Un véhicule vient en face, phares à fond :",
         ["On ne fixe pas les phares, on vise le bas-côté droit, on ralentit si besoin", "On répond en plein phare en continu", "On ferme les yeux", "On se décale à gauche"],
         "a", "On se guide sur la ligne de droite / bas-côté, visière propre."),
        ("route", "L'aquaplaning à moto :",
         ["La roue avant peut décrocher : on relâche, on ne braque pas, on attend le grip", "On contre-braque fort", "On freine à fond de l'avant", "Cela n'existe pas à moto"],
         "a", "Pneus en bon état, allure réduite dans les ornières d'eau."),
        ("conducteur", "Après un repas copieux et un verre de vin :",
         ["L'alcoolémie peut encore dépasser 0,5 g/l : on ne prend pas le guidon « au feeling »", "Le fromage annule l'alcool", "On est plus performant", "C'est moins grave à moto qu'en voiture"],
         "a", "Le feeling ment. Éthylotest, conducteur désigné, transports."),
        ("usagers", "Un taxi ou un VTC s'arrête brusquement :",
         ["Portière, piéton : on couvre toujours le frein en ville", "On le rase pour passer", "On le double à droite sur le trottoir", "Il a toujours tort donc on insiste"],
         "a", "En ville, chaque véhicule peut s'arrêter pour un client."),
        ("divers", "Le permis moto international / conduire à l'étranger :",
         ["Les règles et équipements peuvent changer : on se renseigne avant", "Le code français s'applique partout", "Le casque n'est jamais obligatoire hors France", "L'inter-files est mondial"],
         "a", "Chaque pays a ses règles (gants, feux, péages, alcool)."),
        ("mecanique", "Un levier d'embrayage spongieux ou qui va au guidon :",
         ["Peut indiquer un défaut : on ne part pas sans vérifier", "Est normal sur toutes les motos neuves", "Se règle en accélérant", "N'existe que sur les 125"],
         "a", "Commande = sécurité. Câble, durit, niveau."),
        ("protection", "Un écran solaire (crème) dans les yeux à cause de la sueur :",
         ["Gêne visuelle : on s'arrête pour rincer, on choisit des produits adaptés", "On continue, le casque protège les yeux", "On enlève le casque en roulant", "On accélère pour faire du vent"],
         "a", "Tout ce qui gêne la vue impose l'arrêt."),
        ("environnement", "Le choix d'une moto récente Euro 5 :",
         ["Réduit généralement les émissions par rapport à un modèle très ancien mal entretenu", "Pollue forcément plus qu'un tank des années 70", "Dispense du respect des riverains", "Autorise un échappement ouvert"],
         "a", "La norme aide, le comportement aussi."),
        ("secours", "Une victime hystérique ou en crise de panique après une chute :",
         ["On parle calmement, on protège, on n'aggrave pas en la secouant", "On la gifle « pour la calmer »", "On lui donne de l'alcool", "On part, ce n'est pas grave"],
         "a", "Choc psychologique fréquent. Calme, protection, alerte."),
        ("circulation", "S'insérer sur autoroute depuis la bretelle :",
         ["S'accélérer sur la voie d'insertion, signaler, s'insérer sans forcer, adapter", "S'arrêter au bout de la bretelle et attendre", "S'insérer à 50 km/h sur la voie de gauche", "Couper toutes les files d'un coup"],
         "a", "La voie d'insertion sert à atteindre la vitesse du flux."),
        ("route", "Une plaque de gazole au sol (arc-en-ciel) :",
         ["Extrêmement glissante : on évite, on reste droit", "Améliore le glissement utile", "N'existe plus depuis 2010", "Se traverse en inclinant plus"],
         "a", "Hydrocarbures = patinoire. Surtout aux ronds-points de stations."),
        ("conducteur", "La conduite sous ordonnance d'anxiolytiques :",
         ["Souvent incompatible : lire la notice et demander au médecin", "Est plus sûre car on est zen", "N'est un sujet que pour les poids lourds", "Est recommandée avant l'ETM"],
         "a", "Beaucoup de psychotropes ont un pictogramme conduite."),
        ("usagers", "Un groupe de motards :",
         ["Chacun reste responsable : on ne « colle » pas, on n'imite pas une prise de risque", "Le premier du groupe a tous les droits", "On peut brûler un feu si le précédent l'a passé", "La file de motos est un seul véhicule"],
         "a", "Pas de responsabilité collective magique. Un feu rouge reste rouge."),
        ("divers", "Perdre un point / un permis :",
         ["Conduire malgré une invalidation est un délit", "On peut finir le trajet du jour", "La moto n'est pas concernée par le permis à points", "Les gants évitent le retrait de points"],
         "a", "Solde 0 = plus le droit de conduire, moto comprise."),
        ("mecanique", "Le feu antibrouillard arrière (s'il existe) :",
         ["Brouillard / neige / forte pluie, pas une nuit claire", "S'allume toute la nuit", "Remplace le stop", "Est interdit à moto"],
         "a", "Comme en voiture : ne pas éblouir par temps clair."),
        ("protection", "Porter un sac à dos mal sanglé :",
         ["Peut déstabiliser et gêner un airbag / dorsale : on serre, on charge raisonnablement", "Est plus sûr qu'une valise", "Doit battre dans le vent pour l'équilibre", "Remplace le gilet HV"],
         "a", "Charge proche du corps, sangles réglées."),
        ("secours", "Brûlures d'essence sur la peau :",
         ["Retirer les vêtements imprégnés si possible, rincer, alerter, pas de flamme à proximité", "Frotter avec du sable", "Sécher près du pot", "Mettre du gel hydroalcoolique"],
         "a", "Essence + pot = incendie. Sécurité incendie d'abord."),
        ("circulation", "Un stop à la française « à l'américaine » (ralentir sans arrêter) :",
         ["Est une infraction, même à moto, même à 3 h du matin", "Est toléré pour les deux-roues", "Est autorisé hors agglo", "Est autorisé s'il n'y a pas de caméra"],
         "a", "Arrêt complet. Pieds à terre, moto immobile."),
        ("route", "La première pluie après plusieurs jours secs :",
         ["Est la plus glissante", "Lave immédiatement tout, donc adhérence max", "N'affecte que les voitures", "Autorise +20 km/h car moins de monde"],
         "a", "Film gras. On lâche 10-20 km/h de plus que la simple règle « pluie » si besoin."),
    ]
    for row in extra:
        add(*row)

    return items


def build_behavior_questions():
    rng = random.Random(7)
    out = []
    n = 1
    for code, family, title, detail in SIGNS:
        b = behavior_for(code, family, title, detail, rng)
        if b:
            b["id"] = f"sigb-{n:03d}"
            out.append(b)
            n += 1
    return out


def build_sign_id_questions():
    rng = random.Random(2026)
    titles = [t for _, _, t, _ in SIGNS]
    out = []
    for i, (code, family, title, detail) in enumerate(SIGNS, start=1):
        distractors = rng.sample([t for t in titles if t != title], 3)
        choices = [title] + distractors
        rng.shuffle(choices)
        correct = chr(97 + choices.index(title))
        out.append(
            q(
                f"sig-{i:03d}",
                "signalisation",
                "Que signifie ce panneau ?",
                choices,
                correct,
                detail,
                sign_path(code),
                title,
            )
        )
    return out


def main():
    signs = []
    for code, family, title, detail in SIGNS:
        signs.append({
            "code": code,
            "family": family,
            "title": title,
            "detail": detail,
            "image": sign_path(code),
        })

    questions = build_sign_id_questions() + build_behavior_questions() + knowledge_questions()
    # unique ids already; shuffle stable
    rng = random.Random(1)
    rng.shuffle(questions)

    categories = [
        {"id": k, **v, "count": sum(1 for q in questions if q["category"] == k)}
        for k, v in CATEGORIES.items()
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "signs.json").write_text(
        json.dumps({"signs": signs, "families": {
            "danger": "Danger",
            "priorite": "Priorité",
            "interdiction": "Interdiction",
            "obligation": "Obligation",
            "indication": "Indication",
            "service": "Services",
            "localisation": "Localisation",
            "panonceau": "Panonceaux",
        }}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "questions.json").write_text(
        json.dumps({"categories": categories, "questions": questions}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"signs={len(signs)} questions={len(questions)}")
    from collections import Counter
    print(Counter(q["category"] for q in questions))


if __name__ == "__main__":
    main()
