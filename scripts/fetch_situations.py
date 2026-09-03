#!/usr/bin/env python3
"""Ne plus télécharger de photos Commons pour le quiz.

Le matching par mots-clés a collé des images sans rapport (y compris un
tableau d'uniformes nazis sur une question « feu rouge »). On n'invente
plus de visuel : les QCM sit-* sont des scénarios texte ; un SVG officiel
n'est ajouté que si la question porte sur ce panneau.
"""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "Refus : ne pas scraper Wikimedia pour illustrer les QCM.\n"
        "Les photos « au réel » mal choisies enseignent la mauvaise chose.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
