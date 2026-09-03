(() => {
  const diagRoot = document.getElementById("chaine-diag");
  const ritualRoot = document.getElementById("huile-ritual");
  const greaseRoot = document.getElementById("chaine-grease");
  if (!diagRoot || !ritualRoot || !greaseRoot) return;

  const DIAG = {
    sale: {
      title: "Sale — on ne graisse pas comme ça",
      text: "Croûte noire, sable, sel, après la pluie : le grit devient une pâte abrasive si vous vaporisez par-dessus. Nettoyer, essuyer, sécher, puis seulement graisser.",
    },
    seche: {
      title: "Sèche mais propre — graissage seul",
      text: "Couleur mate, un peu de bruit, pas de grit. Un passage de graisse sur le brin du bas, roue qui tourne, essuyer l’excès. Inutile de tout démonter.",
    },
    ok: {
      title: "OK — on note le prochain contrôle",
      text: "Brillante, souple, jeu dans la fourchette du manuel. Revoir vers 500–800 km, ou juste après la prochaine pluie.",
    },
    usee: {
      title: "Usée — on remplace le kit",
      text: "Points durs, allongement hors cote, dents de pignon en crochet : régler ne suffit plus. Chaîne + pignons ensemble. Une chaîne neuve sur un pignon usé s’use tout de suite.",
    },
  };

  const out = diagRoot.querySelector("#diag-out");
  diagRoot.querySelectorAll("[data-etat]").forEach((btn) => {
    btn.addEventListener("click", () => {
      diagRoot.querySelectorAll("[data-etat]").forEach((b) => b.setAttribute("aria-pressed", "false"));
      btn.setAttribute("aria-pressed", "true");
      const item = DIAG[btn.dataset.etat];
      out.innerHTML = `<h3>${item.title}</h3><p>${item.text}</p>`;
    });
  });

  const GREASE = [
    "Moto stable, moteur froid, gants. Si elle est sale : d’abord le nettoyage.",
    "Produit adapté, brosse souple, on tourne la roue. On enlève le grit, on n’essaie pas de la chromer.",
    "Essuyer, laisser sécher. Graisse sur crasse = pâte à poncer les galets.",
    "Spray sur le brin inférieur, côté galets, en faisant tourner. Pas sur le pneu, pas sur le disque.",
    "Essuyer l’excès. Attendre quelques minutes avant de partir fort.",
  ];
  let g = 0;
  const gText = greaseRoot.querySelector("#grease-text");
  const gStep = greaseRoot.querySelector("#grease-step");
  function showGrease() {
    gText.textContent = GREASE[g];
    gStep.textContent = `Geste ${g + 1} / ${GREASE.length}`;
  }
  greaseRoot.querySelector("#grease-next").addEventListener("click", () => {
    g = (g + 1) % GREASE.length;
    showGrease();
  });
  greaseRoot.querySelector("#grease-prev").addEventListener("click", () => {
    g = (g - 1 + GREASE.length) % GREASE.length;
    showGrease();
  });
  showGrease();

  const OIL = [
    "Moteur à température normale, puis 2 à 3 minutes d’arrêt : l’huile redescend.",
    "Moto verticale — pas sur la béquille latérale, le hublot ment.",
    "Hublot : le trait entre MIN et MAX. Jauge : essuyer, reposer à fond, relire.",
    "Or / ambré = normal. Noir pailleté ou odeur de brûlé = vidange. Trop plein aussi dangereux que trop bas.",
  ];
  let o = 0;
  const oText = ritualRoot.querySelector("#oil-text");
  const oStep = ritualRoot.querySelector("#oil-step");
  function showOil() {
    oText.textContent = OIL[o];
    oStep.textContent = `Étape ${o + 1} / ${OIL.length}`;
  }
  ritualRoot.querySelector("#oil-next").addEventListener("click", () => {
    o = (o + 1) % OIL.length;
    showOil();
  });
  ritualRoot.querySelector("#oil-prev").addEventListener("click", () => {
    o = (o - 1 + OIL.length) % OIL.length;
    showOil();
  });
  showOil();
})();
