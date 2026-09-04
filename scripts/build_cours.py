#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère data/cours.json — leçons ETM, plan du livre PDF, textes rédigés pour l'examen."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def p(*paras: str) -> dict:
    return {"type": "p", "text": "\n\n".join(paras)}


def ul(*items: str) -> dict:
    return {"type": "ul", "items": list(items)}


def ol(*items: str) -> dict:
    return {"type": "ol", "items": list(items)}


def note(text: str) -> dict:
    return {"type": "note", "text": text}


def trap(text: str) -> dict:
    return {"type": "trap", "text": text}


def table(headers: list[str], rows: list[list[str]]) -> dict:
    return {"type": "table", "headers": headers, "rows": rows}


def links(*pairs: tuple[str, str]) -> dict:
    return {"type": "links", "items": [{"href": h, "label": l} for h, l in pairs]}


def lesson(lid: str, title: str, lede: str, blocks: list, quiz: str = "") -> dict:
    return {"id": lid, "title": title, "lede": lede, "quiz": quiz, "blocks": blocks}


THEMES = [
    {
        "id": "epreuve",
        "code": "",
        "title": "L'épreuve ETM",
        "blurb": "40 questions, 35/40, 30 €, 5 ans. Ce n'est plus le code voiture.",
        "lessons": [
            lesson(
                "format",
                "Format 2026 : ce qui tombe vraiment",
                "L'ETM n'est pas un QCM de culture générale. C'est une épreuve de situations : on vous demande ce que vous faites, pas seulement le nom d'un panneau.",
                [
                    p(
                        "40 questions, environ 30 minutes, en centre agréé (La Poste, SGS, etc.). Il faut 35 bonnes réponses : 5 fautes maximum. Chaque passage coûte 30 €. La réussite est valable 5 ans pour présenter le plateau puis la circulation (5 présentations max).",
                        "La réforme de 2026 concerne surtout l'organisation des sessions (identité, fraude), pas le barème. L'ETM reste à 40 questions. Le permis B ne dispense plus de cette épreuve.",
                    ),
                    ul(
                        "Au moins une bonne réponse, parfois plusieurs. Le nombre de bonnes réponses n'est pas affiché, contrairement au code voiture.",
                        "Environ 20 secondes après la lecture audio. Pas de bouton « valider » le jour J : le temps passe, la question suivante arrive.",
                        "Trois regards : vous conduisez, vous observez, vous analysez un danger. Sauf mention contraire, on suppose un permis depuis plus de 3 ans.",
                    ),
                    trap(
                        "Piège classique : répondre trop vite sur une question à plusieurs bonnes réponses, ou traiter l'ETM comme le code auto. Relisez « toujours », « jamais », « obligatoire »."
                    ),
                    links(
                        ("quiz.html?mode=run&n=40&feedback=0", "Examen blanc 40 questions"),
                        ("quiz.html?mode=run&n=20&feedback=1&situations=1", "20 situations rédigées"),
                    ),
                ],
            ),
            lesson(
                "permis",
                "A1, A2, A : qui passe quoi",
                "L'ETM est le même pour A1, A2 et A. Seule la pratique change.",
                [
                    table(
                        ["Permis", "Âge", "Véhicule"],
                        [
                            ["A1", "16 ans", "Jusqu'à 125 cm³ / 11 kW"],
                            ["A2", "18 ans", "Jusqu'à 35 kW et 0,2 kW/kg"],
                            ["A", "24 ans en accès direct, ou 2 ans de A2 + formation 7 h", "Sans limite de puissance"],
                        ],
                    ),
                    p(
                        "Titulaire du B depuis plus de 2 ans : formation 7 h pour un 125 cm³, sans ETM. Ce n'est pas un examen, mais ce n'est pas le permis A2.",
                        "Il faut un numéro NEPH (ANTS) pour réserver. Pièce d'identité originale le jour J, pas une photocopie.",
                    ),
                    trap("Confondre la passerelle B → 125 et le permis A2. La passerelle ne donne pas le droit de passer l'A2 sans ETM si vous visez plus tard une A2/A."),
                ],
            ),
        ],
    },
    {
        "id": "circulation",
        "code": "C",
        "title": "La circulation",
        "blurb": "Priorités, giratoires, vitesses, files, corridor. Le gros du barème.",
        "lessons": [
            lesson(
                "signalisation",
                "Lire un panneau en 3 secondes",
                "À l'examen, on ne vous demande pas de réciter l'IISR. On vous demande ce que le panneau vous impose à moto.",
                [
                    table(
                        ["Famille", "Forme / couleur", "Effet"],
                        [
                            ["Danger (A)", "Triangle pointe en haut, fond blanc, listel rouge", "Avertit : on ralentit, on ne « gagne » pas du temps"],
                            ["Interdiction (B)", "Rond blanc, listel rouge", "Interdit une action ou un accès"],
                            ["Obligation (B bleu)", "Rond bleu", "Impose une direction, une allure mini, une voie"],
                            ["Indication (C)", "Carré / rectangle bleu", "Informe : parking, sens unique, tunnel…"],
                            ["Services (CE)", "Carré blanc, bordure bleue", "Service à proximité (secours, carburant, camping…)"],
                            ["Fin d'interdiction", "Rond blanc, barre noire (B31)", "Fin des interdictions temporaires, pas « interdiction formelle »"],
                        ],
                    ),
                    p(
                        "Les marquages ont la même force : ligne continue = ne pas franchir ; zigzag jaune près d'un passage piéton = stationnement interdit ; flèches au sol = direction imposée dans la voie.",
                        "Feu rouge = arrêt. Orange fixe = arrêt si on peut le faire sans danger. Un feu pour bus ou tram ne vous concerne que s'il s'applique à votre voie.",
                    ),
                    trap(
                        "Un rond blanc barré de noir (B31) n'est pas une interdiction : c'est la fin des interdictions. L'interdiction marchandises est le camion cerclé de rouge (B8)."
                    ),
                    links(("panneaux.html", "Catalogue des panneaux"), ("cours.html?t=circulation&l=priorites", "Les priorités")),
                ],
                "signalisation",
            ),
            lesson(
                "priorites",
                "Priorités : droite, STOP, cédez, route prioritaire",
                "Sans panneau, c'est la priorité à droite. Tout le reste est une exception signalée.",
                [
                    ul(
                        "Priorité à droite : intersection sans signalisation. On cède à celui qui vient de droite, moto ou voiture.",
                        "Cédez-le-passage (AB3a, triangle pointe en bas) : ralentir, s'engager sans gêner. Pas d'arrêt obligatoire si la voie est libre, mais l'allure doit permettre l'arrêt.",
                        "STOP (AB4) : arrêt complet, roues arrêtées, avant la ligne. Un « quasi-stop » (pied à terre sans arrêt) est une faute d'examen.",
                        "Losange jaune (AB6) : vous êtes sur une route prioritaire jusqu'au losange barré (AB7).",
                        "Rétrécissement : B15 (rond, flèches) = vous cédez au sens inverse. C18 (carré bleu) = vous passez.",
                    ),
                    trap("AB5 n'est pas « cédez au sens inverse » : c'est le signal avancé d'un STOP. Le cédez au sens inverse est le B15."),
                    links(("panneaux.html", "Voir AB3a, AB4, AB6, B15"), ("cours.html?t=circulation&l=giratoires", "Giratoires")),
                ],
                "circulation",
            ),
            lesson(
                "giratoires",
                "Giratoires : entrée, voies, clignotant",
                "On cède à ceux déjà dans l'anneau. On ne coupe pas, on ne s'arrête pas au milieu.",
                [
                    ol(
                        "Ralentir, observer à gauche. Panneau habituel : cédez-le-passage + AB25 (giratoire).",
                        "S'insérer dans un trou, pas « au feeling ». À moto on est moins visible : un regard ne suffit pas, il faut un créneau.",
                        "Voie de droite pour les premières sorties, voie intérieure pour un 3/4 tour ou un tour complet, si plusieurs voies existent.",
                        "Clignotant droit pour sortir, de préférence après la sortie précédente. Si vous ratez la vôtre : on continue, on ne recule pas.",
                    ),
                    p("Dans l'anneau, un motard collé à l'îlot se fait couper à la sortie. On se place tôt, on signale, on surveille l'angle mort droit."),
                    trap("La priorité à droite ne s'applique pas « contre » l'anneau. Ceux qui sont déjà engagés passent, sauf fléchage local contraire."),
                ],
                "circulation",
            ),
            lesson(
                "vitesse",
                "Limitations, pluie, permis probatoire",
                "Les plafonds moto sont les mêmes que voiture. Ce qui change, c'est la distance d'arrêt et l'adhérence.",
                [
                    table(
                        ["Réseau", "Temps sec (permis définitif)", "Pluie ou permis probatoire"],
                        [
                            ["Agglomération", "50 (30 en zone 30, 20 en zone de rencontre)", "50 / 30 / 20 inchangés"],
                            ["Hors agglo bidirectionnelle", "80, parfois 90 par arrêté", "80"],
                            ["2×2 voies / voie express", "110", "100"],
                            ["Autoroute", "130", "110"],
                        ],
                    ),
                    p(
                        "Visibilité inférieure à 50 m (brouillard, pluie battante) : 50 km/h partout, autoroute comprise.",
                        "Un panneau C4a (vitesse conseillée) n'est pas une limitation. Un B25 bleu est une vitesse minimale, pas un max.",
                    ),
                    trap("Sous la pluie, 130 n'existe plus. Beaucoup répondent 120 : la bonne valeur autoroute mouillée est 110."),
                ],
                "circulation",
            ),
            lesson(
                "placement",
                "Se placer pour être vu",
                "Le bon placement n'est pas « au milieu parce que c'est plus fun ». C'est : être vu, voir, et garder une porte de sortie.",
                [
                    ul(
                        "En file : légèrement décalé, pas dans l'angle mort du véhicule de devant, assez loin pour freiner.",
                        "Avant un virage : extérieur de sa voie, sans mordre la ligne. On ouvre le champ, on ne prend pas le sens inverse.",
                        "En ville : éviter de raser les portières (dooring) et les rétros des files à l'arrêt.",
                        "Sur 2×2 voies hors inter-files : une voie, une file. On ne « danse » pas entre deux voitures.",
                    ),
                    p("Si vous ne voyez pas le chauffeur d'un PL dans son rétro, il ne vous voit pas. On avance ou on recule dans le champ du rétro, on ne reste pas collé."),
                    links(("trajectoires.html", "Trajectoire de sécurité"), ("particularites.html", "Particularités moto")),
                ],
                "circulation",
            ),
            lesson(
                "arret-stationnement",
                "Arrêt, stationnement, gênant, très gênant",
                "Arrêt = temps nécessaire pour prendre ou déposer. Stationnement = le reste. À moto, « je m'arrête une minute » est souvent un stationnement.",
                [
                    ul(
                        "Interdit de s'arrêter / stationner : trottoir utile aux piétons, passage piéton, piste cyclable, voie de bus, BAU, devant une issue, zigzag jaune.",
                        "Très gênant (fourrière possible) : passage piéton, trottoir, piste, place PMR, arrêt de bus, emplacement de secours.",
                        "Sens interdit : on ne s'y engage pas, même « juste pour se garer ».",
                        "Un 2RM n'a pas le droit de circuler sur le trottoir pour éviter un bouchon.",
                    ),
                    trap("Un panneau B6a1 (stationnement interdit) n'interdit pas forcément un arrêt très court pour déposer quelqu'un, sauf B6d (arrêt et stationnement interdits) ou marquage plus strict."),
                ],
                "circulation",
            ),
            lesson(
                "depassement",
                "Croiser et dépasser à moto",
                "On ne dépasse que si on voit, on est vu, et on peut se rabattre sans couper.",
                [
                    ul(
                        "Interdit : ligne continue, virage / côte sans visibilité, intersection, passage à niveau, B3.",
                        "Cycliste : 1 m en agglo, 1,50 m hors agglo. On peut empiéter une ligne discontinue pour le faire, pas une continue.",
                        "Poids lourd : on s'écarte (aspiration, déport d'air), on ne reste pas à sa hauteur, on accélère franchement puis on se rabat tôt.",
                        "Croisement étroit : si B15, on s'arrête. Sinon on serre sa droite, on ralentit, on se tient prêt à poser le pied.",
                    ),
                    trap("Dépasser un cycliste en chevauchant une ligne continue est une infraction, même « pour lui laisser 1,50 m »."),
                ],
                "circulation",
            ),
            lesson(
                "interfiles",
                "Inter-files et corridor de sécurité",
                "Deux règles 2025 qui tombent tout le temps. Ce n'est pas « on se faufile partout ».",
                [
                    p("Circulation inter-files (R.412-11-3), depuis le 11 janvier 2025 :"),
                    ul(
                        "Autoroutes et routes à chaussées séparées, au moins 2 voies par sens, VMA légale ≥ 70 km/h même si elle a été abaissée (le périphérique parisien à 50 reste dans le champ).",
                        "Circulation dense, files ininterrompues. Entre les deux files les plus à gauche seulement.",
                        "50 km/h max, 30 km/h si une file est à l'arrêt. On ne dépasse pas un autre 2RM déjà en inter-files.",
                        "Interdit hors de ces axes : centre-ville, 2×1 voie, nationale sans terre-plein.",
                    ),
                    p("Corridor de sécurité (R.412-11-1) : véhicule arrêté sur le bord avec feux de détresse ou spéciaux. On ralentit, on s'éloigne, on change de voie si on le peut. Trois panneaux SR53 le rappellent."),
                    links(("particularites.html", "Détail inter-files + SR53"), ("panneaux.html", "Panneaux SR53")),
                ],
                "circulation",
            ),
        ],
    },
    {
        "id": "conducteur",
        "code": "L",
        "title": "Le conducteur",
        "blurb": "Alcool 0,2 en probatoire, fatigue, téléphone, distances.",
        "lessons": [
            lesson(
                "alcool",
                "Alcool, stupéfiants, médicaments",
                "À moto, 0,2 g/l suffit à faire perdre l'équilibre. L'examen aime les seuils et le pictogramme.",
                [
                    table(
                        ["Situation", "Seuil sang", "Air expiré"],
                        [
                            ["Permis définitif", "0,5 g/l", "0,25 mg/l"],
                            ["Permis probatoire (A1/A2/A)", "0,2 g/l", "0,10 mg/l"],
                            ["Stupéfiants", "Zéro", "Zéro"],
                        ],
                    ),
                    p(
                        "0,2 g/l, c'est souvent un verre. En probatoire, « un verre ça passe » est faux.",
                        "Médicament : pictogramme jaune/orange = prudence, lire la notice. Pictogramme rouge = ne pas conduire. Un antibiotique anodin + un somnifère = cumul.",
                    ),
                    trap("Le seuil moto n'est pas plus bas que la voiture. En revanche le permis A/A2 est probatoire : c'est 0,2, pas 0,5."),
                ],
                "conducteur",
            ),
            lesson(
                "distances",
                "Distances de sécurité et d'arrêt",
                "Distance d'arrêt = réaction + freinage. À moto, tout ce qui allonge l'un ou l'autre se paie cash.",
                [
                    p(
                        "Temps de réaction moyen : environ 1 seconde. À 50 km/h c'est déjà 14 m avant de commencer à freiner. À 90 km/h, environ 25 m.",
                        "Intervalle : 2 secondes minimum sur route sèche, plus sous la pluie, derrière un PL, en descente, de nuit. La règle des traits : au moins 2 bandes de ligne discontinue.",
                    ),
                    ul(
                        "Pluie, surtout les premières minutes (film gras) : distances × 1,5 à × 2.",
                        "Pneu lisse, charge, passager, freins chauds : le freinage s'allonge encore.",
                        "ABS : aide à ne pas bloquer la roue, ne sauve pas sur gravillons ou peinture mouillée.",
                    ),
                    trap("On ne freine pas fort moto penchée. On redresse, on freine droit, ou on diminue l'allure avant le virage."),
                    links(("trajectoires.html", "Quand freiner / pencher"), ("controles.html", "État des pneus et freins")),
                ],
                "conducteur",
            ),
            lesson(
                "fatigue",
                "Fatigue, vigilance, nuit",
                "La fatigue à moto n'est pas « je bâille ». C'est un écart de trajectoire, un oubli de rétro, un freinage trop tard.",
                [
                    ul(
                        "Signes : paupières lourdes, fixité du regard, oublis de clignotant, chaleur dans le casque, micro-sommeil.",
                        "Réflexe : aire, café ne remplace pas 20 minutes d'arrêt réel, hydratation, retirer le casque à l'arrêt.",
                        "Nuit : feux de croisement, visière propre, allure qui permet l'arrêt dans le faisceau. Les distances sont sous-estimées.",
                        "Téléphone tenu, oreillette dans le casque, GPS à tapoter : infraction et perte d'équilibre.",
                    ),
                    trap("« Je connais la route, je peux rouler fatigué. » C'est exactement le profil des sorties de route de fin de week-end."),
                ],
                "conducteur",
            ),
            lesson(
                "communication",
                "Communiquer : clignotant, regard, klaxon",
                "À moto on n'a pas de carrosserie pour « montrer » une intention. Le clignotant et le placement font le travail.",
                [
                    ul(
                        "Clignotant : assez tôt pour être lu, coupé dès que la manœuvre est finie. Un clignotant oublié après un giratoire attire une voiture dans votre voie.",
                        "Regard + légèrement tourner la tête : le rétro ne suffit pas. Angle mort avant tout changement de file.",
                        "Klaxon : danger immédiat seulement. Ce n'est pas un klaxon de colère ni un « bonjour » en agglo de nuit.",
                        "Appel de phare : pour signaler une présence, pas pour « pousser » celui de devant.",
                    ),
                    trap("Un clignotant allumé n'est pas une priorité. Il annonce, il n'autorise pas à couper."),
                ],
                "conducteur",
            ),
            lesson(
                "maitrise",
                "Maîtrise : regard, équilibre, allure",
                "On conduit où l'on regarde. On ne fixe pas l'obstacle.",
                [
                    ol(
                        "Scanner : loin, rétros, angles morts, sol. Une fois ne suffit pas.",
                        "Allure qui permet l'arrêt sur la distance visible.",
                        "Moto droite pour freiner fort ; regard et appui pour tourner.",
                        "Gaz, frein, embrayage : un seul gros changement à la fois en situation glissante.",
                    ),
                    p("Analyse de l'environnement : météo, revêtement, usagers cachés (haie, camion, bus). Un enfant entre deux voitures n'apparaît qu'à 10 m."),
                    links(("plateau.html", "Le plateau entraîne ces réflexes"), ("cours.html?t=route&l=adherence", "Lire le sol")),
                ],
                "conducteur",
            ),
        ],
    },
    {
        "id": "usagers",
        "code": "U",
        "title": "Les autres usagers",
        "blurb": "SMIDSY, angles morts, piétons, PL, bus, prioritaires.",
        "lessons": [
            lesson(
                "vulnerables",
                "Piétons, cyclistes, enfants, PMR",
                "Un piéton engagé est prioritaire. Un enfant n'a pas de trajectoire rationnelle.",
                [
                    ul(
                        "Passage piéton sans feux : on s'apprête à s'arrêter dès qu'un piéton manifeste l'intention de traverser.",
                        "École, parc, arrêt de bus : allure qui permet l'arrêt, klaxon inutile et souvent interdit.",
                        "Cycliste / trottinette : on les traite comme des usagers lents imprévisibles, distance latérale, pas de slalom.",
                        "Cavalier : on dépasse large, on ne klaxonne pas. Animal : on freine progressivement, on ne fait pas d'écart brutal.",
                    ),
                    trap("Klaxonner un enfant ou un cavalier « pour le prévenir » est souvent le geste qui le fait surgir ou cabrer."),
                ],
                "usagers",
            ),
            lesson(
                "angles-morts",
                "SMIDSY et angles morts des PL",
                "« Sorry Mate I Didn't See You » : une voiture tourne à gauche en vous ayant regardé sans vous voir.",
                [
                    p(
                        "C'est le scénario n°1 des chocs moto en agglo. Le conducteur croit la voie libre. Vous étiez dans un angle, derrière un poteau, ou trop vite pour son cerveau.",
                        "Réflexe : arriver en se couvrant le levier, phare allumé, placement visible, ne pas doubler un PL à sa droite au feu, ne pas rester le long d'un bus qui va redémarrer.",
                    ),
                    ul(
                        "Camion / bus : si vous ne voyez pas le chauffeur, reculez ou avancez. Jamais collé à la cabine.",
                        "Portières : 1 m d'écart le long des voitures stationnées.",
                        "Tourne-à-gauche d'en face : on ne se fie pas à son clignotant. On prépare l'évitement.",
                    ),
                    links(("particularites.html", "Être vu"), ("assets/img/illustrations/angle-mort.svg", "Schéma angle mort")),
                ],
                "usagers",
            ),
            lesson(
                "autres-2rm",
                "Les autres deux-roues",
                "Scooter, 125, moto de route, trio : même code, gabarits et allures différents.",
                [
                    ul(
                        "Un scooter peut s'arrêter plus court, un GT dépasse plus vite. On ne suppose pas que « c'est comme moi ».",
                        "Groupe : chacun garde ses distances, on ne double pas en éventail, on ne se parle pas au guidon.",
                        "Inter-files : un seul 2RM à la fois entre deux files. On ne double pas celui déjà engagé.",
                        "Cyclo / trottinette électrique : souvent à droite, parfois sur piste. On les traite comme vulnérables, pas comme des obstacles.",
                    ),
                    trap("« On est entre motards, on se comprend. » L'examen attend la même règle pour tous, pas la camaraderie."),
                ],
                "usagers",
            ),
            lesson(
                "lourds",
                "PL, bus, tram, prioritaires",
                "Un bus à l'arrêt, portes ouvertes : on s'attend à un piéton. Un tram a un gabarit et des rails.",
                [
                    ul(
                        "Bus : ne pas le dépasser à l'arrêt côté portes. Voie de bus : interdite sauf panonceau.",
                        "Tram : rails glissants, les franchir le plus perpendiculairement possible, sans freiner dessus.",
                        "Prioritaire (feu + sirène) : on se range sans tout bloquer, on ne le « suit » pas au rouge.",
                        "Convoi / convoi exceptionnel : on ne le double pas à la légère, on obéit aux personnels.",
                    ),
                    trap("Un feu tricolore reste le feu. Un prioritaire ne vous autorise pas à griller le rouge « pour lui laisser la place » en vous engageant n'importe comment."),
                ],
                "usagers",
            ),
        ],
    },
    {
        "id": "divers",
        "code": "D",
        "title": "Notions diverses",
        "blurb": "Papiers, FVA, CT, passager, catégories de permis.",
        "lessons": [
            lesson(
                "papiers",
                "Papiers, assurance FVA, contrôle technique",
                "Depuis 2024, plus de vignette verte à exhiber. L'assurance se vérifie dans le FVA.",
                [
                    ul(
                        "À avoir : permis, certificat d'immatriculation. Un mémo assureur reste utile, plus obligatoire à coller.",
                        "FVA : fichier des véhicules assurés. Un contrôle peut vérifier l'assurance sans carte verte.",
                        "Contrôle technique des 2RM : déployé depuis 2024, selon date de 1re mise en circulation. Une moto non soumise aujourd'hui le sera.",
                        "Panne : gilet à porter dès que l'on est à pied, se mettre derrière une glissière, alerter (112, borne).",
                    ),
                    trap("« Je n'ai plus besoin d'assurance puisque plus de carte verte » est faux. L'assurance reste obligatoire, seul le justificatif papier a changé."),
                ],
                "divers",
            ),
            lesson(
                "passager",
                "Passager, charge, objets",
                "Un passager n'est pas un sac. Il change l'assiette, le freinage et la trajectoire.",
                [
                    ul(
                        "Places homologuées, repose-pieds, poignées. Casque et gants CE pour les deux.",
                        "Consigne : il suit le regard et le corps, il ne se penche pas à contre-sens, pieds toujours sur les repose-pieds.",
                        "Masses constructeur : PTAC, charge max. Un top-case mal fixé déporte au freinage.",
                        "Rien qui dépasse ou qui flotte (sangle, sac). Un objet sur la chaussée fait chuter le suivant.",
                    ),
                    trap("Le passager n'a pas besoin d'être mentionné sur le permis, mais la moto doit être prévue pour deux. Un strapontin bricolé = non."),
                ],
                "divers",
            ),
            lesson(
                "prevention",
                "Accidents fréquents et conduite préventive",
                "Les causes reviennent : vitesse inadaptée, angle mort, alcool, perte d'adhérence, inattention.",
                [
                    ol(
                        "Allure qui permet l'arrêt sur ce qu'on voit.",
                        "Se rendre visible (placement, feux, couleur, pas l'inter-files en ville).",
                        "Couvrir les commandes aux abords d'un danger (école, giratoire, PL).",
                        "Ne pas rouler pour « se prouver » : l'ETM note l'attitude autant que la règle.",
                    ),
                    p("Conduite de nuit et week-end : mix fatigue + alcool d'autrui. On double la marge, on ne joue pas au justicier."),
                ],
                "divers",
            ),
        ],
    },
    {
        "id": "mecanique",
        "code": "M",
        "title": "Mécanique et équipements de la moto",
        "blurb": "Pneus, chaîne, freins, feux, liquides. Le tour avant de partir.",
        "lessons": [
            lesson(
                "pneus-freins",
                "Pneus, freins, feux",
                "Deux empreintes de la largeur d'une carte bancaire : tout passe par là.",
                [
                    ul(
                        "Pneus : pression à froid (notice), témoin d'usure, coupures, hernies. Un pneu avant lisse = on ne part pas.",
                        "Freins : niveau, fuite, disque strié, levier spongieux, feu stop qui s'allume. Avant + arrière se complètent.",
                        "Feux : croisement, route, stop, clignotants, plaque. Un stop HS et on se fait rentrer dedans.",
                        "Rétros : deux, réglés, non cassés. Ils doivent montrer l'arrière, pas seulement le coude.",
                    ),
                    links(("controles.html", "Contrôles pas à pas")),
                ],
                "mecanique",
            ),
            lesson(
                "liquides-chaine",
                "Huile, chaîne, carburant",
                "Une chaîne trop lâche saute. Trop tendue, elle use tout.",
                [
                    ul(
                        "Huile : niveau hublot / jauge, moto droite. Trop bas = grippage. Trop haut = embrayage qui patine sur certains modèles.",
                        "Chaîne : jeu constructeur, graissage, alignement, joints. Bruit sec = sèche.",
                        "Carburant : réserve anticipée, surtout hors agglo. Une panne sur BAU est un accident en puissance.",
                        "Liquide de frein : niveau entre min et max, liquide sombre = à prévoir.",
                    ),
                    trap("On ne « tend pas au feeling ». Un doigt de jeu au point le plus tendu, selon la notice, pas au pif."),
                ],
                "mecanique",
            ),
            lesson(
                "modifs",
                "Modifications et éclairage",
                "Ce qui n'est pas homologué n'est pas « plus safe ». C'est souvent illégal et ça ment à l'examen.",
                [
                    ul(
                        "Échappement non homologué : bruit, pollution, verbalisation, assurance qui discute après un choc.",
                        "Phares additionnels, rubans LED : autorisés seulement s'ils respectent le code (éblouissement, couleur).",
                        "Feux obligatoires en circulation : croisement au moins. Beaucoup de motos imposent le feu allumé jour et nuit.",
                        "On ne débride pas une A2 pour « aller plus vite jusqu'à l'A ».",
                    ),
                ],
                "mecanique",
            ),
        ],
    },
    {
        "id": "protection",
        "code": "P",
        "title": "Équipements de protection",
        "blurb": "Obligatoire vs recommandé : le piège n°1 du thème P.",
        "lessons": [
            lesson(
                "obligatoire",
                "Ce qui est obligatoire",
                "Casque homologué attaché + gants CE, conducteur et passager. Le reste est recommandé… et vital.",
                [
                    ul(
                        "Casque : ECE 22.05 ou 22.06, à votre taille, jugulaire attachée. Jet ou intégral : les deux peuvent être homologués ; l'intégral protège le visage.",
                        "Gants : certification CE EN 13594, pour les deux. Des gants de ski ne suffisent pas à l'examen.",
                        "Gilet / équipement rétro : à bord, à porter dès que l'on est à pied sur la chaussée (panne, accident). Hors agglo de nuit / visibilité réduite : dispositif rétro pour être vu.",
                    ),
                    trap("« Le blouson est obligatoire. » Faux en circulation (sauf règles locales / exam pratique qui exige une tenue). À l'ETM : obligatoire = casque + gants (+ gilet à utiliser à pied)."),
                    links(("particularites.html", "Frontière obligatoire / recommandé")),
                ],
                "protection",
            ),
            lesson(
                "recommande",
                "Blouson, pantalon, bottes, airbag",
                "Le bitume râpe en quelques mètres. Un t-shirt à 40 km/h n'est pas une armure.",
                [
                    ul(
                        "Blouson / pantalon : abrasion, coques épaules / coudes / genoux, idéalement CE.",
                        "Bottes : montantes, qui tiennent la cheville. Des baskets = fracture classique.",
                        "Dorsale : souvent dans le blouson ou séparée.",
                        "Airbag (gilet ou intégré) : se déclenche à la chute, protège thorax / cervicales. Recommandé, de plus en plus exigé en plateau par les écoles.",
                    ),
                    p("L'examen aime la phrase : recommandé n'est pas facultatif pour votre peau. On choisit l'équipement pour le trajet (autoroute, pluie, nuit), pas pour la photo."),
                ],
                "protection",
            ),
        ],
    },
    {
        "id": "environnement",
        "code": "E",
        "title": "L'environnement",
        "blurb": "Bruit, éco-conduite, déchets sur la chaussée, restrictions.",
        "lessons": [
            lesson(
                "eco",
                "Éco-conduite à moto",
                "Ce n'est pas « rouler à 40 partout ». C'est anticiper pour moins freiner, moins gazer, moins user.",
                [
                    ul(
                        "Allure stable, rapports adaptés, pression des pneus juste.",
                        "Moteur au ralenti 10 minutes dans un bouchon : on coupe si on est vraiment à l'arrêt durable.",
                        "Entretien : une chaîne sèche et un filtre encrassé consomment et polluent.",
                        "Covoiturage / moins de trajets inutiles : le thème E aime aussi le comportement, pas seulement le pot catalytique.",
                    ),
                ],
                "environnement",
            ),
            lesson(
                "bruit",
                "Bruit, pollution, restrictions",
                "Un pot non homologué n'est pas un style. C'est une infraction et une nuisance.",
                [
                    ul(
                        "Échappement homologué, silencieux en place. Les contrôles de bruit existent.",
                        "Accélérations inutiles en agglo, nuit, zone sensible : faute d'attitude à l'ETM.",
                        "Pics de pollution / ZCR (B56) : un 2RM n'est pas automatiquement exonéré. On lit le panonceau.",
                        "Stationner sur un espace vert, une dune, une voie pompiers : non.",
                    ),
                    trap("« C'est une moto, Crit'Air ne me concerne pas. » Faux dès qu'une zone l'inclut. On lit B56 / B57 et le panonceau."),
                ],
                "environnement",
            ),
            lesson(
                "chaussee",
                "Ce qu'on laisse sur la route",
                "Un gant, une sangle, une bouteille : le suivant chute.",
                [
                    p("On ne jette rien. On ramasse ce qui peut tomber de la moto (bagage, sangle). En zone naturelle, on reste sur la chaussée, on ne coupe pas à travers la faune."),
                    p("Huile, gazole, liquide de refroidissement sur la chaussée : on signale si on en voit une flaque, on ne freine pas dessus."),
                ],
                "environnement",
            ),
        ],
    },
    {
        "id": "secours",
        "code": "S",
        "title": "Premiers secours",
        "blurb": "P.A.S., 112, casque, PLS, RCP, DAE.",
        "lessons": [
            lesson(
                "pas",
                "Protéger, alerter, secourir",
                "On ne crée pas un second accident. La zone d'abord, le soin ensuite.",
                [
                    ol(
                        "Protéger : gilet, se mettre à l'abri (glissière), faire ralentir / dévier, triangle si utile et sans se faire écraser. Sur autoroute on ne danse pas au milieu des voies.",
                        "Alerter : 112 (Europe), 15 SAMU, 18 pompiers, 17 police, 114 si on ne peut pas parler. Lieu précis, nombre de victimes, nature, dégagement ou non.",
                        "Secourir : dans la limite de ce qu'on sait. On ne déplace un blessé que si un danger vital l'impose (incendie, écrasement).",
                    ),
                    trap("Courir vers le blessé au milieu de l'autoroute « pour l'aider » : vous devenez la deuxième victime. D'abord la zone."),
                ],
                "secours",
            ),
            lesson(
                "casque-pls",
                "Casque, inconscience, PLS, hémorragie",
                "On ne retire le casque que si les voies aériennes l'exigent.",
                [
                    ul(
                        "Conscient, casque en place, il respire : on le rassure, on stabilise la tête, on ne lui retire pas le casque « pour qu'il ait de l'air ».",
                        "Inconscient qui respire : PLS, après avoir libéré les voies si besoin. Le casque se retire si on ne peut pas maintenir la respiration autrement.",
                        "Ne respire pas : alerte, massage cardiaque, DAE dès qu'il est là.",
                        "Hémorragie : compression directe, gants si possible, pas de garrot de bricolage sauf formation.",
                    ),
                    p("Choc : pâleur, sueur, soif, agitation. On allonge, on couvre, on n'a pas à boire, on surveille la conscience."),
                ],
                "secours",
            ),
            lesson(
                "rcp-dae",
                "RCP et défibrillateur",
                "30 compressions, 2 insufflations si on est formé. Sinon compressions seules, profondes, au milieu du thorax.",
                [
                    p(
                        "Le DAE parle. On colle les électrodes, on n'effleure plus la victime pendant l'analyse et le choc. On reprend le massage entre les chocs.",
                        "Gants, lunettes : on évite le sang. On ne « désinfecte » pas une plaie grave avec de l'alcool à brûler : on protège et on attend les secours.",
                    ),
                    links(("https://www.securite-routiere.gouv.fr/", "Sécurité routière")),
                ],
                "secours",
            ),
        ],
    },
    {
        "id": "route",
        "code": "R",
        "title": "La route",
        "blurb": "Sol, autoroute, nuit, pluie, trajectoire.",
        "lessons": [
            lesson(
                "types",
                "Types de routes et règles",
                "Agglo, hors agglo, voie express, autoroute : le régime change, le sol aussi.",
                [
                    ul(
                        "Agglomération : panneau EB10 (nom de commune) = 50 km/h même sans B14, piétons, priorités à droite fréquentes.",
                        "Hors agglo : 80 (parfois 90), animaux, virages, revêtement inégal.",
                        "Voie express / accès réglementé (C107) : souvent 110, accès limité, pas une autoroute.",
                        "Autoroute (C207) : 130/110, insertion, BAU, interdiction de s'arrêter hors urgence, pas de piétons ni cyclos.",
                    ),
                    links(("panneaux.html", "EB10, C107, C207, C208")),
                ],
                "route",
            ),
            lesson(
                "zones-danger",
                "Zones de danger : écoles, travaux, PN, chantiers",
                "Un panneau A13a (enfants) ou AK14 (travaux) n'est pas décoratif : l'allure doit permettre l'arrêt.",
                [
                    ul(
                        "École, sortie d'établissement : 30 souvent, piétons imprévisibles, cars à l'arrêt.",
                        "Travaux (AK14, B14 temporaire) : sol dégradé, gravillons, sens alterné, ouvriers. On respecte la limitation temporaire, même « trop basse ».",
                        "Passage à niveau : arrêt si les feux clignotent / barrières. On ne s'engage que si on peut libérer complètement. Rails = adhérence nulle en biais.",
                        "Chantier / déviation : suivre la signalisation temporaire, plus prioritaire que l'ancienne.",
                    ),
                    trap("Franchir un PN « ça va passer » pendant que la barrière descend est une faute grave, pas un calcul de temps."),
                    links(("panneaux.html", "AK14, A13a, A7, G1")),
                ],
                "route",
            ),
            lesson(
                "autoroute",
                "Autoroute : insertion, BAU, péage, tunnel",
                "On s'insère à la vitesse du flux, on ne s'arrête pas sur la bretelle « pour attendre ».",
                [
                    ul(
                        "Insertion : rétro, angle mort, accélération dans la voie d'insertion, pas dans la voie de droite déjà occupée.",
                        "BAU : urgence seulement. Gilet, derrière la glissière, moto le plus à droite possible.",
                        "Péage : file adaptée, allure très réduite, sol souvent lisse / rainuré. On ne zigzag pas entre les barrières.",
                        "Tunnel : feux de croisement, lunettes de soleil enlevées, distance, pas de demi-tour, issues de secours repérées (CE30).",
                    ),
                    trap("S'arrêter sur la BAU « pour consulter le GPS » est une faute grave, pas une pause."),
                ],
                "route",
            ),
            lesson(
                "adherence",
                "Lire le sol : pluie, rails, peinture, gravillons",
                "À moto le sol est votre unique contact. On le lit comme un tableau de bord.",
                [
                    ul(
                        "Pluie : premières minutes = film gras. Peinture, plaques, rails, zébras = patinoire.",
                        "Rails de tram / PN : les franchir le plus droit possible, sans freiner ni accélérer dessus.",
                        "Gravillons, terre, feuilles, gazole : on lâche les angles, on évite les à-coups.",
                        "Dos-d'âne / plateau : allure réduite, trajectoire perpendiculaire, fesses légèrement décollées.",
                    ),
                    links(("trajectoires.html", "Trajectoire et phases"), ("controles.html", "Pneus adaptés")),
                ],
                "route",
            ),
            lesson(
                "meteo",
                "Nuit, brouillard, neige, vent",
                "On adapte l'allure à ce qu'on voit, pas à ce que dit le dernier panneau 130.",
                [
                    ul(
                        "Nuit : croisement, visière propre, se méfier des usagers sans feu.",
                        "Brouillard < 50 m : 50 km/h, brouillard arrière si la moto en a, pas les feux de route (mur blanc).",
                        "Neige / verglas : souvent la bonne décision est de ne pas partir. Chaînes / pneus hiver : rares et peu adaptés à beaucoup de motos.",
                        "Vent : ponts, sorties de tranchée, dépassement de PL. On tient le guidon, on ne se braque pas.",
                    ),
                    trap("Feux de route dans le brouillard : ça n'aide pas, ça éblouit en retour. Croisement + allure 50 si visibilité < 50 m."),
                ],
                "route",
            ),
        ],
    },
]


def main() -> None:
    n_lessons = sum(len(t["lessons"]) for t in THEMES)
    payload = {
        "source": {
            "title": "Livre Code Moto ETM 2026",
            "credit": "Plan et matières d'après le PDF déposé dans assets/ebook_moto_1781723509.pdf (TestPermis.fr). Textes des leçons rédigés pour ce site, orientés examen 2026.",
            "file": "assets/ebook_moto_1781723509.pdf",
        },
        "themes": THEMES,
        "lessonCount": n_lessons,
    }
    dest = ROOT / "data" / "cours.json"
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {dest} themes={len(THEMES)} lessons={n_lessons}")


if __name__ == "__main__":
    main()
