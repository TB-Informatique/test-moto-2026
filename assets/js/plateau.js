(() => {
  const X0 = 56;
  const Y0 = 78;
  const TW = 1068;
  const TH = 300;
  const M = TW / 130;
  const x = (meters) => X0 + meters * M;
  const y = (frac) => Y0 + frac * TH;
  const C4 = 16;
  const C5 = 19.9;
  const C6 = 35.65;
  const C7 = 74;

  function slalomD(start, cones, end, yLo, yHi) {
    const pts = [start];
    cones.forEach((cx, i) => {
      pts.push([cx, i % 2 === 0 ? yLo : yHi]);
    });
    pts.push(end);
    let d = `M${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
    for (let i = 1; i < pts.length; i += 1) {
      const prev = pts[i - 1];
      const cur = pts[i];
      const midX = (prev[0] + cur[0]) / 2;
      d += ` C${midX.toFixed(1)} ${prev[1].toFixed(1)} ${midX.toFixed(1)} ${cur[1].toFixed(1)} ${cur[0].toFixed(1)} ${cur[1].toFixed(1)}`;
    }
    return d;
  }

  const Y_LO = y(0.78);
  const Y_HI = y(0.22);
  const Y_MID = y(0.5);
  const RIGHT = x(126);
  const LEFT_A = x(8);

  const slowConesM = [48, 56, 64, 72, 80];
  const fastConesM = [58, 66, 74, 82, 90];

  const PATHS = {
    poussette: `M${x(4).toFixed(1)} ${Y_MID.toFixed(1)} H${x(16).toFixed(1)}`,
    poussetteBack: `M${x(16).toFixed(1)} ${Y_MID.toFixed(1)} H${x(4).toFixed(1)}`,
    lent:
      slalomD([LEFT_A, Y_LO], slowConesM.map(x), [x(118), Y_LO], Y_LO, Y_HI) +
      ` C${x(124).toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` C${RIGHT.toFixed(1)} ${Y_HI.toFixed(1)} ${x(118).toFixed(1)} ${Y_HI.toFixed(1)} ${x(110).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(42).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` C${x(38).toFixed(1)} ${Y_HI.toFixed(1)} ${x(36).toFixed(1)} ${Y_MID.toFixed(1)} ${x(40).toFixed(1)} ${Y_MID.toFixed(1)}`,
    freinage:
      `M${x(40).toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` C${x(48).toFixed(1)} ${Y_MID.toFixed(1)} ${x(52).toFixed(1)} ${Y_LO.toFixed(1)} ${x(70).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` L${x(118).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` C${x(124).toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` C${RIGHT.toFixed(1)} ${Y_HI.toFixed(1)} ${x(118).toFixed(1)} ${Y_HI.toFixed(1)} ${x(108).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(C6).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(C5 + 0.4).toFixed(1)} ${Y_HI.toFixed(1)}`,
    passager:
      `M${x(20).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` C${x(28).toFixed(1)} ${Y_HI.toFixed(1)} ${x(36).toFixed(1)} ${Y_LO.toFixed(1)} ${x(52).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` C${x(62).toFixed(1)} ${Y_LO.toFixed(1)} ${x(62).toFixed(1)} ${Y_HI.toFixed(1)} ${x(48).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(10).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` C${x(6).toFixed(1)} ${Y_HI.toFixed(1)} ${x(5).toFixed(1)} ${Y_MID.toFixed(1)} ${x(10).toFixed(1)} ${Y_MID.toFixed(1)}`,
    slalom:
      slalomD([x(12), Y_LO], fastConesM.map(x), [x(118), Y_LO], Y_LO, Y_HI) +
      ` C${x(124).toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_MID.toFixed(1)}`,
    evitement:
      `M${RIGHT.toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` C${RIGHT.toFixed(1)} ${Y_HI.toFixed(1)} ${x(118).toFixed(1)} ${Y_HI.toFixed(1)} ${x(108).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(C6 + 4).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` C${x(C6).toFixed(1)} ${Y_HI.toFixed(1)} ${x(C6 - 2).toFixed(1)} ${Y_LO.toFixed(1)} ${x(C6 - 8).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` C${x(C6 - 14).toFixed(1)} ${Y_LO.toFixed(1)} ${x(24).toFixed(1)} ${Y_LO.toFixed(1)} ${x(18).toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` L${x(12).toFixed(1)} ${Y_MID.toFixed(1)}`,
  };

  const STEPS = [
    {
      id: "poussette",
      num: "1 / 6",
      title: "Poussette — sans moteur",
      type: "Couloir de guidage, avant puis arrière",
      color: "#94a3b8",
      pathId: "path-poussette",
      twoWay: true,
      backPathId: "path-poussette-back",
      duration: 8000,
      cues: [
        { t: 0, action: "walk", text: "Couloir entre les 4 piquets. Moto droite, regard vers B. Avancez jusqu’à ce que la roue arrière passe les cônes." },
        { t: 0.5, action: "look", text: "Stop. Regardez derrière. Reculez : la roue avant doit repasser les cônes. Puis béquille." },
      ],
      panel: {
        trajectoire: "Ligne dans le couloir (~1,5 m). Avant A→B (roue AR au-delà), arrière B→A (roue AV au-delà).",
        gaz: "Aucun : moteur coupé.",
        frein: "Aucun. On rattrape le guidon si ça part.",
        attention: "Équilibrer avant de bouger. 3 essais. Regard où vous allez.",
        difficulte: "Perdre l’équilibre à l’arrêt, braquer trop, reculer de travers.",
        train: "Allée plane, gants. 20 allers-retours sans poser autre chose que les pieds de marche.",
      },
    },
    {
      id: "lent",
      num: "2 / 6",
      title: "Allure réduite — seul",
      type: "Slalom lent, demi-tour, arrêt au cône bleu (4)",
      color: "#38bdf8",
      pathId: "path-lent",
      duration: 14000,
      cues: [
        { t: 0, action: "clutch", text: "Départ zone A. Patinage + frein arrière. Chrono (1)→(2) : plus c’est lent, mieux c’est (≥ 16 s = A)." },
        { t: 0.18, action: "look", text: "Ne fixez pas le cône : visez l’intervalle suivant. On reste dans les 6 m." },
        { t: 0.45, action: "gas", text: "Filet de gaz pour ne pas caler. Demi-tour au bout de piste, toujours au pas." },
        { t: 0.78, action: "clutch", text: "Retour. Arrêt au point 4 : roue avant entre les lignes, avant le cône bleu." },
      ],
      panel: {
        trajectoire: "S lent entre les cônes, demi-tour en bout, retour, stop au bleu n°4. Pas de marche arrière.",
        gaz: "Micro-gaz de ralenti. On n’accélère pas pour rattraper un cône.",
        frein: "Frein AR seulement. Frein AV = plonge + pied à terre.",
        attention: "≥ 16 s = A, 14–16 s = B, < 14 s = C. Pied hors zone = B.",
        difficulte: "Fixer le cône, à-coups d’embrayage, vouloir aller trop vite.",
        train: "Gobelets à ~2,50 m. 8 passages sans pied, en comptant à voix haute.",
      },
    },
    {
      id: "freinage",
      num: "3 / 6",
      title: "Freinage d’urgence",
      type: "Demi-tour, ligne droite, 50 km/h au C6",
      color: "#ef4444",
      pathId: "path-freinage",
      duration: 10000,
      cues: [
        { t: 0, action: "look", text: "Du point 4 : demi-tour sans dépasser le 1er cône du slalom, puis on va chercher le bout de piste." },
        { t: 0.28, action: "gas", text: "Demi-tour au bout. 3e rapport. On construit 50 km/h — pas un sprint à la dernière seconde." },
        { t: 0.68, action: "look", text: "Radar C6 : 50 km/h min (A2 sans marge). On ne freine PAS avant cette ligne." },
        { t: 0.76, action: "brake", text: "Après C6 : avant + arrière, buste bas. Arrêt avant C5 (sec) ou C4 (humide). Roue AR au sol." },
      ],
      panel: {
        trajectoire: "Demi-tour, ligne droite sur la largeur de piste, freinage après C6, stop avant C5 (15,75 m) ou C4 (+3,90 m si humide).",
        gaz: "Avant C6 uniquement. 50 au radar, pas après.",
        frein: "Seulement après C6. Stoppie = B. Trop long ou trop tôt = C.",
        attention: "Vitesse insuffisante = C. Doigts qui ferment le levier avant C6 = C.",
        difficulte: "Arriver à 46 km/h, ou dépasser C5.",
        train: "Un plot « C6 » + une boîte C5. 50 AU plot et arrêt AVANT la boîte.",
      },
    },
    {
      id: "passager",
      num: "4 / 6",
      title: "Allure réduite — avec passager",
      type: "Montée en A, lent, descente en B (piquets)",
      color: "#a78bfa",
      pathId: "path-passager",
      duration: 11000,
      cues: [
        { t: 0, action: "clutch", text: "Stop après freinage = A. Le passager monte. Départ tout doux : 80 kg de plus. Il ne parle pas du tracé." },
        { t: 0.35, action: "look", text: "Même regard loin. La moto tourne plus lourde : on anticipe plus tôt." },
        { t: 0.75, action: "gas", text: "Filet de gaz dans le demi-tour. Immobiliser en B après les piquets : le passager descend." },
      ],
      panel: {
        trajectoire: "De A (arrêt freinage) jusqu’à la porte de piquets B, à l’allure du lent.",
        gaz: "Encore plus dosé qu’en solo.",
        frein: "Frein AR pour caler l’arrière alourdi.",
        attention: "2 mains aux poignées, pieds sur les repose-pieds. Dicter le tracé = C.",
        difficulte: "Départ en charge, passager qui se penche à contretemps.",
        train: "Sac lesté, puis un passager calme. 10 départs sans à-coup.",
      },
    },
    {
      id: "slalom",
      num: "5 / 6",
      title: "Slalom à allure normale",
      type: "S rapide, 40 km/h au C7, demi-tour",
      color: "#f97316",
      pathId: "path-slalom",
      duration: 8000,
      cues: [
        { t: 0, action: "gas", text: "Après la descente du passager. 3e rapport avant le 1er cône. On construit 40 km/h, gaz stable." },
        { t: 0.42, action: "look", text: "C7 ≥ 40 km/h (A2 sans marge). Regard au-delà du dernier plot, pas sur le cône." },
        { t: 0.82, action: "look", text: "Demi-tour en bout. On ne fonce pas déjà vers l’évitement : un temps à la fois." },
      ],
      panel: {
        trajectoire: "S entre les cônes orange (le bleu n’en fait pas partie), puis demi-tour au bout des 130 m.",
        gaz: "Stable dans les plots. On ne coupe pas à chaque cône.",
        frein: "Pas de gros frein dans le slalom.",
        attention: "< 40 km/h au C7 = C. Cône touché (hors évitement) = B.",
        difficulte: "Arriver trop lent, ou regarder le cône et le prendre.",
        train: "Même slalom, 40 au 3e cône, 8 fois sans toucher.",
      },
    },
    {
      id: "evitement",
      num: "6 / 6",
      title: "Évitement",
      type: "Retour, 50 km/h au C6, un appui, stop dans les bleus",
      color: "#22c55e",
      pathId: "path-evitement",
      duration: 8000,
      cues: [
        { t: 0, action: "gas", text: "Retour en ligne. On reconstruit 50 km/h avant C6 (marge +5). Un seul évitement, pas un slalom." },
        { t: 0.4, action: "look", text: "Regard dans le trou de passage, pas sur le cône d’évitement." },
        { t: 0.55, action: "look", text: "Un appui franc, on redresse. Toucher ce cône = C." },
        { t: 0.78, action: "brake", text: "Puis on freine pour finir entre les quatre cônes bleus." },
      ],
      panel: {
        trajectoire: "Ligne, un déport après C6, retour, arrêt dans le rectangle bleu.",
        gaz: "Jusqu’au C6. On ne réaccélère pas dans l’appui.",
        frein: "Après l’évitement. Freiner penché = glisse ou cône.",
        attention: "Cône d’évitement = C. Hors zone / sortie de piste = C.",
        difficulte: "Deux appuis, regarder le cône, ou arriver à 42 km/h.",
        train: "50 au plot, un seul appui, arrêt dans un carré craie.",
      },
    },
  ];

  const ACTION_LABEL = {
    walk: "Pousser",
    clutch: "Patinage",
    gas: "Accélérer",
    brake: "Freiner",
    look: "Regard",
  };

  const root = document.getElementById("plateau-player");
  if (!root) return;

  const NS = "http://www.w3.org/2000/svg";
  const pills = root.querySelector("#step-pills");
  const caption = root.querySelector("#live-caption");
  const badges = root.querySelector("#live-badges");
  const panel = root.querySelector("#step-panel");
  const playBtn = root.querySelector("#play-step");
  const prevBtn = root.querySelector("#prev-step");
  const nextBtn = root.querySelector("#next-step");
  const svg = root.querySelector("#plateau-svg");
  const trackLayer = root.querySelector("#track-layer");
  const pathsLayer = root.querySelector("#paths-layer");
  const marksLayer = root.querySelector("#marks-layer");
  const bike = root.querySelector("#bike-dot");

  let index = -1;
  let raf = 0;
  let playing = false;

  function el(name, attrs, text) {
    const node = document.createElementNS(NS, name);
    Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, String(v)));
    if (text) node.textContent = text;
    return node;
  }

  function cone(cx, cy, color) {
    return el("polygon", {
      points: `${cx},${cy - 9} ${cx - 7},${cy + 7} ${cx + 7},${cy + 7}`,
      fill: color,
    });
  }

  function buildTrack() {
    trackLayer.appendChild(el("rect", { x: 0, y: 0, width: 1180, height: 500, rx: 14, fill: "#121821" }));
    trackLayer.appendChild(el("rect", { x: X0, y: Y0, width: TW, height: TH, rx: 6, fill: "#3d4654", stroke: "#94a3b8", "stroke-width": 2 }));
    [C4, C5, C6, C7].forEach((m, i) => {
      const label = ["C4", "C5", "C6", "C7"][i];
      const px = x(m);
      trackLayer.appendChild(el("line", { x1: px, y1: Y0, x2: px, y2: Y0 + TH, stroke: "#fbbf24", "stroke-width": 1.6, "stroke-dasharray": "7 5" }));
      trackLayer.appendChild(el("text", { x: px + 4, y: Y0 - 8, fill: "#fbbf24", "font-size": 12, "font-family": "system-ui,sans-serif", "font-weight": 700 }, label));
    });
    trackLayer.appendChild(el("text", { x: X0, y: Y0 + TH + 18, fill: "#94a3b8", "font-size": 11, "font-family": "system-ui,sans-serif" }, "0 m"));
    trackLayer.appendChild(el("text", { x: X0 + TW - 36, y: Y0 + TH + 18, fill: "#94a3b8", "font-size": 11, "font-family": "system-ui,sans-serif" }, "130 m"));
    trackLayer.appendChild(el("text", { x: X0 - 8, y: Y0 + TH / 2, fill: "#94a3b8", "font-size": 11, "font-family": "system-ui,sans-serif", "text-anchor": "end" }, "6 m"));
    const boxX = x(8);
    const boxW = x(20) - x(8);
    trackLayer.appendChild(el("rect", { x: boxX, y: y(0.32), width: boxW, height: y(0.68) - y(0.32), fill: "#3b82f6", opacity: 0.14 }));
  }

  function buildMarks() {
    [
      [x(4), y(0.38)],
      [x(4), y(0.62)],
      [x(16), y(0.38)],
      [x(16), y(0.62)],
    ].forEach(([sx, sy]) => {
      marksLayer.appendChild(el("rect", { x: sx - 3, y: sy - 12, width: 6, height: 24, rx: 1, fill: "#e2e8f0" }));
    });
    slowConesM.forEach((m) => marksLayer.appendChild(cone(x(m), Y_LO + 2, "#f97316")));
    fastConesM.forEach((m) => marksLayer.appendChild(cone(x(m), Y_HI - 2, "#f97316")));
    marksLayer.appendChild(cone(x(C6 - 6), Y_LO, "#3b82f6"));
    [
      [x(9), y(0.34)],
      [x(19), y(0.34)],
      [x(9), y(0.66)],
      [x(19), y(0.66)],
    ].forEach(([cx, cy]) => marksLayer.appendChild(cone(cx, cy, "#3b82f6")));
    marksLayer.appendChild(cone(x(40), Y_MID, "#3b82f6"));
    marksLayer.appendChild(el("text", { x: x(40) + 10, y: Y_MID - 10, fill: "#93c5fd", "font-size": 11, "font-family": "system-ui,sans-serif", "font-weight": 700 }, "4"));
    marksLayer.appendChild(el("text", { x: x(5), y: Y_MID - 16, fill: "#cbd5e1", "font-size": 11, "font-family": "system-ui,sans-serif", "font-weight": 700 }, "A / B"));
  }

  function buildPaths() {
    const defs = [
      ["path-poussette", PATHS.poussette, "#94a3b8"],
      ["path-poussette-back", PATHS.poussetteBack, "#94a3b8"],
      ["path-lent", PATHS.lent, "#38bdf8"],
      ["path-freinage", PATHS.freinage, "#ef4444"],
      ["path-passager", PATHS.passager, "#a78bfa"],
      ["path-slalom", PATHS.slalom, "#f97316"],
      ["path-evitement", PATHS.evitement, "#22c55e"],
    ];
    defs.forEach(([id, d, color]) => {
      pathsLayer.appendChild(el("path", {
        id,
        d,
        fill: "none",
        stroke: color,
        "stroke-width": 5,
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        class: "plateau-trace",
      }));
    });
  }

  function setBadge(action) {
    badges.querySelectorAll("[data-action]").forEach((node) => {
      node.setAttribute("aria-pressed", node.dataset.action === action ? "true" : "false");
    });
  }

  function cueAt(step, t) {
    let current = step.cues[0];
    for (const cue of step.cues) {
      if (t >= cue.t) current = cue;
    }
    return current;
  }

  function placeBikeOn(path, t) {
    const len = path.getTotalLength();
    const p = path.getPointAtLength(Math.min(1, Math.max(0, t)) * Math.max(len, 1));
    bike.setAttribute("cx", p.x.toFixed(1));
    bike.setAttribute("cy", p.y.toFixed(1));
  }

  function stopPlay() {
    playing = false;
    cancelAnimationFrame(raf);
    playBtn.textContent = "Lire l’animation";
    playBtn.setAttribute("aria-pressed", "false");
  }

  function renderOverview() {
    panel.innerHTML = `
      <p class="kicker">Parcours 1 · piste 130 × 6 m</p>
      <h2>Le plateau vu de dessus</h2>
      <p>Tous les tracés sont superposés, chacun sa couleur, dans l’ordre officiel. Choisissez une étape (ou Suivant) : il ne reste que ce tracé, et l’animation le suit.</p>
      <div class="phase-grid">
        ${STEPS.map((s) => `<article class="phase-card" style="border-top:4px solid ${s.color}"><h3>${s.num} ${s.title.split("—")[0]}</h3><p>${s.type}</p></article>`).join("")}
      </div>
      <p class="note">C6→C5 = 15,75 m (freinage sec). C5→C4 = 3,90 m de plus si la piste est humide. C7 = 40 km/h (slalom), C6 = 50 km/h (freinage et évitement). Schéma pédagogique : le plan du centre d’examen fait foi.</p>
    `;
  }

  function renderPanel(step) {
    panel.innerHTML = `
      <p class="kicker">${step.num} · ${step.type}</p>
      <h2>${step.title}</h2>
      <div class="phase-grid">
        <article class="phase-card"><h3>Trajectoire</h3><p>${step.panel.trajectoire}</p></article>
        <article class="phase-card gas"><h3>Quand accélérer</h3><p>${step.panel.gaz}</p></article>
        <article class="phase-card brake"><h3>Quand freiner</h3><p>${step.panel.frein}</p></article>
        <article class="phase-card lean"><h3>Points d’attention</h3><p>${step.panel.attention}</p></article>
        <article class="phase-card"><h3>Grosse difficulté</h3><p class="danger-line">${step.panel.difficulte}</p></article>
        <article class="phase-card"><h3>Comment s’entraîner</h3><p>${step.panel.train}</p></article>
      </div>
    `;
  }

  function showView(i) {
    stopPlay();
    index = i;
    const traces = [...pathsLayer.querySelectorAll(".plateau-trace")];
    traces.forEach((p) => {
      p.classList.remove("is-active");
      p.setAttribute("opacity", i < 0 ? "0.95" : "0.1");
    });
    pills.querySelectorAll("button").forEach((btn, n) => {
      btn.setAttribute("aria-current", n === i + 1 ? "step" : "false");
    });
    if (i < 0) {
      bike.setAttribute("visibility", "hidden");
      playBtn.disabled = true;
      caption.textContent = "Vue d’ensemble : les 6 tracés officiels, chacun sa couleur. Suivant pour commencer à la poussette.";
      setBadge("");
      renderOverview();
      svg.setAttribute("aria-label", "Plateau 130 mètres sur 6, tous les tracés.");
      return;
    }
    const step = STEPS[i];
    const path = document.getElementById(step.pathId);
    path.setAttribute("opacity", "1");
    path.classList.add("is-active");
    if (step.twoWay) {
      document.getElementById(step.backPathId).setAttribute("opacity", "0.35");
    }
    bike.setAttribute("visibility", "visible");
    playBtn.disabled = false;
    placeBikeOn(path, 0);
    const cue = cueAt(step, 0);
    caption.textContent = cue.text;
    setBadge(cue.action);
    renderPanel(step);
    svg.setAttribute("aria-label", `${step.title}. ${step.type}.`);
  }

  function play() {
    if (index < 0) {
      showView(0);
    }
    const step = STEPS[index];
    if (!step) return;
    if (playing) {
      stopPlay();
      return;
    }
    playing = true;
    playBtn.textContent = "Pause";
    playBtn.setAttribute("aria-pressed", "true");
    const path = document.getElementById(step.pathId);
    const back = step.twoWay ? document.getElementById(step.backPathId) : null;
    const start = performance.now();
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const dur = reduce ? 1 : step.duration;
    const tick = (now) => {
      const t = (now - start) / dur;
      if (t >= 1) {
        if (back) {
          placeBikeOn(back, 1);
        } else {
          placeBikeOn(path, 1);
        }
        const last = step.cues[step.cues.length - 1];
        caption.textContent = last.text;
        setBadge(last.action);
        stopPlay();
        return;
      }
      if (step.twoWay && back) {
        if (t < 0.5) {
          placeBikeOn(path, t * 2);
        } else {
          back.setAttribute("opacity", "1");
          placeBikeOn(back, (t - 0.5) * 2);
        }
      } else {
        placeBikeOn(path, t);
      }
      const cue = cueAt(step, t);
      caption.textContent = cue.text;
      setBadge(cue.action);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
  }

  buildTrack();
  buildPaths();
  buildMarks();

  const overviewBtn = document.createElement("button");
  overviewBtn.type = "button";
  overviewBtn.className = "chip";
  overviewBtn.textContent = "Vue d’ensemble";
  overviewBtn.addEventListener("click", () => showView(-1));
  pills.appendChild(overviewBtn);

  STEPS.forEach((step, i) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip";
    btn.textContent = `${i + 1}. ${step.title.split("—")[0].trim()}`;
    btn.style.borderColor = step.color;
    btn.addEventListener("click", () => showView(i));
    pills.appendChild(btn);
  });

  ["walk", "clutch", "gas", "brake", "look"].forEach((action) => {
    const span = document.createElement("span");
    span.className = `live-badge live-badge-${action}`;
    span.dataset.action = action;
    span.setAttribute("aria-pressed", "false");
    span.textContent = ACTION_LABEL[action];
    badges.appendChild(span);
  });

  prevBtn.addEventListener("click", () => showView(index <= 0 ? -1 : index - 1));
  nextBtn.addEventListener("click", () => {
    if (index >= STEPS.length - 1) showView(-1);
    else showView(index + 1);
  });
  playBtn.addEventListener("click", play);

  showView(-1);
})();
