(() => {
  const X0 = 56;
  const Y0 = 78;
  const TW = 1068;
  const TH = 300;
  const M = TW / 130;
  const x = (meters) => X0 + meters * M;
  const y = (frac) => Y0 + frac * TH;

  const C6 = 52;
  const C5 = C6 - 15.75;
  const C4 = C6 - 19.65;
  const SLALOM = [52.5, 70, 87.5, 105];
  const C7 = SLALOM[2];

  const V_WALK = 1.15;
  const V_SLOW = 1.05;
  const V_TURN = 2.4;
  const V40 = 40 / 3.6;
  const V50 = 50 / 3.6;

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

  const PATHS = {
    poussette: `M${x(1).toFixed(1)} ${Y_MID.toFixed(1)} H${x(5).toFixed(1)}`,
    poussetteBack: `M${x(5).toFixed(1)} ${Y_MID.toFixed(1)} H${x(1).toFixed(1)}`,
    lent:
      slalomD([x(8), Y_MID], [x(10), x(16), x(22)], [x(28), Y_MID], y(0.32), y(0.68)) +
      ` L${x(35).toFixed(1)} ${Y_MID.toFixed(1)}`,
    freinage:
      `M${x(35).toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` C${x(42).toFixed(1)} ${Y_MID.toFixed(1)} ${x(46).toFixed(1)} ${Y_LO.toFixed(1)} ${x(50).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` L${x(118).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` C${x(124).toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` C${RIGHT.toFixed(1)} ${Y_HI.toFixed(1)} ${x(118).toFixed(1)} ${Y_HI.toFixed(1)} ${x(108).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(C6).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(C5).toFixed(1)} ${Y_HI.toFixed(1)}`,
    passager:
      `M${x(36).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` C${x(28).toFixed(1)} ${Y_HI.toFixed(1)} ${x(22).toFixed(1)} ${Y_LO.toFixed(1)} ${x(16).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` C${x(12).toFixed(1)} ${Y_LO.toFixed(1)} ${x(10).toFixed(1)} ${Y_MID.toFixed(1)} ${x(8).toFixed(1)} ${Y_MID.toFixed(1)}`,
    slalom:
      slalomD([x(12), Y_LO], SLALOM.map(x), [x(118), Y_LO], Y_LO, Y_HI) +
      ` C${x(124).toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_LO.toFixed(1)} ${RIGHT.toFixed(1)} ${Y_MID.toFixed(1)}`,
    evitement:
      `M${RIGHT.toFixed(1)} ${Y_MID.toFixed(1)}` +
      ` C${RIGHT.toFixed(1)} ${Y_HI.toFixed(1)} ${x(118).toFixed(1)} ${Y_HI.toFixed(1)} ${x(108).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` L${x(C6 + 2).toFixed(1)} ${Y_HI.toFixed(1)}` +
      ` C${x(C6).toFixed(1)} ${Y_HI.toFixed(1)} ${x(C6 - 3).toFixed(1)} ${Y_LO.toFixed(1)} ${x(C6 - 8).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` L${x(20).toFixed(1)} ${Y_LO.toFixed(1)}` +
      ` C${x(16).toFixed(1)} ${Y_LO.toFixed(1)} ${x(14).toFixed(1)} ${Y_MID.toFixed(1)} ${x(12).toFixed(1)} ${Y_MID.toFixed(1)}`,
  };

  const STEPS = [
    {
      id: "poussette",
      num: "1 / 6",
      title: "Poussette — sans moteur",
      type: "Porte 1,20 m, avant puis arrière (~4 m)",
      color: "#94a3b8",
      pathId: "path-poussette",
      twoWay: true,
      backPathId: "path-poussette-back",
      cues: [
        { t: 0, action: "walk", text: "Porte 1,20 m. Moteur coupé. Poussez au pas (~4 km/h) jusqu’à ce que la roue arrière passe les cônes." },
        { t: 0.42, action: "look", text: "Stop. Regardez derrière. Reculez au même pas : la roue avant doit repasser la porte. Puis béquille." },
      ],
      panel: {
        trajectoire: "Aller A→B (~4 m) par la porte, puis reculer B→A. Pas un couloir de 12 m.",
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
      type: "S entre piquets, chrono (1)→(2), arrêt au cône bleu (4)",
      color: "#38bdf8",
      pathId: "path-lent",
      cues: [
        { t: 0, action: "clutch", text: "Départ zone A. Patinage + frein arrière. Chrono portes 1→2 : ≥ 16 s = A (environ 17 m, ~4 km/h)." },
        { t: 0.35, action: "look", text: "Ne fixez pas le piquet : visez l’intervalle suivant. On reste dans les 6 m." },
        { t: 0.7, action: "clutch", text: "Couloir lent, puis arrêt au point 4 : roue avant avant le cône bleu." },
      ],
      panel: {
        trajectoire: "S à piquets (~17 m), pas un slalom de 5 cônes. Puis couloir et stop au bleu n°4.",
        gaz: "Micro-gaz de ralenti. On n’accélère pas pour rattraper un plot.",
        frein: "Frein AR seulement. Frein AV = plonge + pied à terre.",
        attention: "≥ 16 s = A, 14–16 s = B, < 14 s = C. Pied hors zone = B.",
        difficulte: "Fixer le piquet, à-coups d’embrayage, vouloir aller trop vite.",
        train: "3 portes à 1,20 m. Passer en comptant jusqu’à 16.",
      },
    },
    {
      id: "freinage",
      num: "3 / 6",
      title: "Freinage d’urgence",
      type: "Demi-tour, ligne droite, 50 km/h au C6",
      color: "#ef4444",
      pathId: "path-freinage",
      cues: [
        { t: 0, action: "look", text: "Du point 4 : demi-tour sans dépasser le 1er cône du slalom (17,50 m), puis on va chercher le bout." },
        { t: 0.22, action: "gas", text: "Demi-tour au bout. 3e rapport. On construit 50 km/h — l’animation accélère vraiment ici." },
        { t: 0.72, action: "look", text: "Radar C6 : 50 km/h min (A2 sans marge). On ne freine PAS avant cette ligne." },
        { t: 0.82, action: "brake", text: "Après C6 : avant + arrière. Arrêt avant C5 (15,75 m) ou C4 (+3,90 m si humide)." },
      ],
      panel: {
        trajectoire: "Demi-tour, ligne droite, freinage après C6, stop avant C5 (15,75 m) ou C4 (19,65 m si humide).",
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
      type: "Montée après freinage, lent, descente aux piquets",
      color: "#a78bfa",
      pathId: "path-passager",
      cues: [
        { t: 0, action: "clutch", text: "Stop après freinage = A. Le passager monte. Départ tout doux (~4 km/h) : 80 kg de plus." },
        { t: 0.4, action: "look", text: "Même regard loin. La moto tourne plus lourde : on anticipe plus tôt." },
        { t: 0.8, action: "gas", text: "Filet de gaz. Immobiliser en B (porte piquets / cônes) : le passager descend." },
      ],
      panel: {
        trajectoire: "De la zone de freinage jusqu’à la porte de piquets B, à l’allure du lent.",
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
      type: "4 plots à 17,50 m, 40 km/h au C7 (3e plot)",
      color: "#f97316",
      pathId: "path-slalom",
      cues: [
        { t: 0, action: "gas", text: "3e rapport avant le 1er plot. On construit 40 km/h — nettement plus vite que la poussette." },
        { t: 0.45, action: "look", text: "C7 = 3e plot ≥ 40 km/h (A2 sans marge). Regard au-delà du dernier plot." },
        { t: 0.82, action: "look", text: "Demi-tour en bout (25 m après le 4e plot). On ne fonce pas déjà vers l’évitement." },
      ],
      panel: {
        trajectoire: "4 cônes orange, 17,50 m d’entraxe. C7 au 3e. Le bleu n’en fait pas partie.",
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
      cues: [
        { t: 0, action: "gas", text: "Retour en ligne. On reconstruit 50 km/h avant C6. Un seul évitement, pas un slalom." },
        { t: 0.45, action: "look", text: "Regard dans le trou de passage, pas sur le cône d’évitement." },
        { t: 0.58, action: "look", text: "Un appui franc, on redresse. Toucher ce cône = C." },
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
  const speedEl = root.querySelector("#live-speed");
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

  function piquet(cx, cy) {
    return el("rect", { x: cx - 2.5, y: cy - 14, width: 5, height: 28, rx: 1, fill: "#e2e8f0" });
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
    trackLayer.appendChild(el("text", { x: X0, y: Y0 + TH + 18, fill: "#94a3b8", "font-size": 11, "font-family": "system-ui,sans-serif" }, "0 m · A"));
    trackLayer.appendChild(el("text", { x: X0 + TW - 48, y: Y0 + TH + 18, fill: "#94a3b8", "font-size": 11, "font-family": "system-ui,sans-serif" }, "130 m · B"));
    trackLayer.appendChild(el("text", { x: X0 - 8, y: Y0 + TH / 2, fill: "#94a3b8", "font-size": 11, "font-family": "system-ui,sans-serif", "text-anchor": "end" }, "6 m"));
    const boxX = x(8);
    const boxW = x(16) - x(8);
    trackLayer.appendChild(el("rect", { x: boxX, y: y(0.34), width: boxW, height: y(0.66) - y(0.34), fill: "#3b82f6", opacity: 0.14 }));
  }

  function buildMarks() {
    [y(0.4), y(0.6)].forEach((sy) => marksLayer.appendChild(cone(x(4), sy, "#f97316")));
    [[10, 0.32], [10, 0.52], [16, 0.48], [16, 0.68], [22, 0.32], [22, 0.52]].forEach(([m, f]) => {
      marksLayer.appendChild(piquet(x(m), y(f)));
    });
    SLALOM.forEach((m) => marksLayer.appendChild(cone(x(m), Y_LO + 2, "#f97316")));
    marksLayer.appendChild(cone(x(C6 - 5), Y_LO, "#3b82f6"));
    [
      [x(9), y(0.36)],
      [x(15), y(0.36)],
      [x(9), y(0.64)],
      [x(15), y(0.64)],
    ].forEach(([cx, cy]) => marksLayer.appendChild(cone(cx, cy, "#3b82f6")));
    marksLayer.appendChild(cone(x(35), Y_MID, "#3b82f6"));
    marksLayer.appendChild(el("text", { x: x(35) + 10, y: Y_MID - 10, fill: "#93c5fd", "font-size": 11, "font-family": "system-ui,sans-serif", "font-weight": 700 }, "4"));
    marksLayer.appendChild(el("text", { x: x(1), y: Y_MID - 18, fill: "#cbd5e1", "font-size": 11, "font-family": "system-ui,sans-serif", "font-weight": 700 }, "A"));
    marksLayer.appendChild(el("text", { x: x(5.2), y: Y_MID - 18, fill: "#cbd5e1", "font-size": 11, "font-family": "system-ui,sans-serif", "font-weight": 700 }, "B"));
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

  function setSpeed(mps) {
    if (!speedEl) return;
    const kmh = Math.max(0, mps) * 3.6;
    speedEl.textContent = `${kmh.toFixed(0)} km/h`;
    speedEl.dataset.fast = kmh >= 30 ? "1" : "0";
  }

  function cueAt(step, t) {
    let current = step.cues[0];
    for (const cue of step.cues) {
      if (t >= cue.t) current = cue;
    }
    return current;
  }

  function placeBikeOn(path, frac) {
    const len = path.getTotalLength();
    const p = path.getPointAtLength(Math.min(1, Math.max(0, frac)) * Math.max(len, 1));
    bike.setAttribute("cx", p.x.toFixed(1));
    bike.setAttribute("cy", p.y.toFixed(1));
  }

  function stopPlay() {
    playing = false;
    cancelAnimationFrame(raf);
    playBtn.textContent = "Lire l’animation";
    playBtn.setAttribute("aria-pressed", "false");
  }

  function pathMeters(path, from, to) {
    return (path.getTotalLength() * (to - from)) / M;
  }

  function segDuration(lenM, v0, v1) {
    return (2 * lenM) / (v0 + v1);
  }

  function motionPlan(step, path, back) {
    const len = path.getTotalLength() / M;
    if (step.id === "poussette") {
      return [
        { path, from: 0, to: 1, v0: V_WALK, v1: V_WALK },
        { pause: 1.5 },
        { path: back, from: 0, to: 1, v0: V_WALK, v1: V_WALK },
      ];
    }
    if (step.id === "lent" || step.id === "passager") {
      return [{ path, from: 0, to: 1, v0: V_SLOW, v1: V_SLOW }];
    }
    if (step.id === "freinage") {
      const brake = Math.min(0.2, 15.75 / len);
      const hold = 0.1;
      const turn = 0.3;
      return [
        { path, from: 0, to: turn, v0: V_TURN, v1: V_TURN },
        { path, from: turn, to: 1 - brake - hold, v0: 5, v1: V50 },
        { path, from: 1 - brake - hold, to: 1 - brake, v0: V50, v1: V50 },
        { path, from: 1 - brake, to: 1, v0: V50, v1: 0.5 },
      ];
    }
    if (step.id === "slalom") {
      return [
        { path, from: 0, to: 0.22, v0: 6, v1: V40 },
        { path, from: 0.22, to: 0.82, v0: V40, v1: V40 },
        { path, from: 0.82, to: 1, v0: V40, v1: V_TURN },
      ];
    }
    return [
      { path, from: 0, to: 0.2, v0: 8, v1: V50 },
      { path, from: 0.2, to: 0.55, v0: V50, v1: V50 },
      { path, from: 0.55, to: 0.72, v0: V50, v1: 10 },
      { path, from: 0.72, to: 1, v0: 10, v1: 0.6 },
    ];
  }

  function compilePlan(raw) {
    return raw.map((item) => {
      if (item.pause) return { pause: item.pause, duration: item.pause, v0: 0, v1: 0 };
      const lenM = pathMeters(item.path, item.from, item.to);
      const duration = segDuration(lenM, item.v0, item.v1);
      return { ...item, lenM, duration };
    });
  }

  function renderOverview() {
    panel.innerHTML = `
      <p class="kicker">Parcours 1 · piste 130 × 6 m</p>
      <h2>Le plateau vu de dessus</h2>
      <p>Tracé pédagogique calé sur le guide d’évaluation : C6→C5 = 15,75 m, slalom <strong>4 plots × 17,50 m</strong>, C7 au 3e plot. L’animation avance à des <strong>vitesses réelles</strong> (marche ≈ 4 km/h, slalom 40, freinage 50).</p>
      <div class="phase-grid">
        ${STEPS.map((s) => `<article class="phase-card" style="border-top:4px solid ${s.color}"><h3>${s.num} ${s.title.split("—")[0]}</h3><p>${s.type}</p></article>`).join("")}
      </div>
      <p class="note">Abscisses C4–C7 : reconstruction fiche (C6 ≈ 52 m depuis A). Le plan du centre d’examen fait foi. Parcours 2 = miroir.</p>
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
    setSpeed(0);
    if (i < 0) {
      bike.setAttribute("visibility", "hidden");
      playBtn.disabled = true;
      caption.textContent = "Vue d’ensemble : 6 tracés. Les animations vont au pas, à 40 ou à 50 km/h — plus à la même vitesse.";
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
    if (index < 0) showView(0);
    const step = STEPS[index];
    if (!step) return;
    if (playing) {
      stopPlay();
      return;
    }
    const path = document.getElementById(step.pathId);
    const back = step.twoWay ? document.getElementById(step.backPathId) : null;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const plan = compilePlan(motionPlan(step, path, back));
    const total = plan.reduce((sum, item) => sum + item.duration, 0);
    playing = true;
    playBtn.textContent = "Pause";
    playBtn.setAttribute("aria-pressed", "true");
    let seg = 0;
    let t0 = performance.now();
    const tick = (now) => {
      if (!playing) return;
      const item = plan[seg];
      if (!item) {
        const last = step.cues[step.cues.length - 1];
        caption.textContent = last.text;
        setBadge(last.action);
        setSpeed(0);
        stopPlay();
        return;
      }
      const scale = reduce ? 0.08 : 1;
      const u = (now - t0) / (item.duration * 1000 * scale);
      const elapsed = plan.slice(0, seg).reduce((s, it) => s + it.duration, 0) + Math.min(1, u) * item.duration;
      const cue = cueAt(step, elapsed / total);
      caption.textContent = cue.text;
      setBadge(cue.action);
      if (item.pause) {
        setSpeed(0);
        if (u >= 1) {
          seg += 1;
          t0 = now;
        }
        raf = requestAnimationFrame(tick);
        return;
      }
      const clamped = Math.min(1, Math.max(0, u));
      const v = item.v0 + (item.v1 - item.v0) * clamped;
      const distFrac = item.lenM < 0.2
        ? clamped
        : (item.v0 * clamped * item.duration + 0.5 * (item.v1 - item.v0) * item.duration * clamped * clamped) / item.lenM;
      const frac = item.from + (item.to - item.from) * Math.min(1, distFrac);
      placeBikeOn(item.path, frac);
      setSpeed(v);
      if (item.path !== path) item.path.setAttribute("opacity", "1");
      if (u >= 1) {
        placeBikeOn(item.path, item.to);
        seg += 1;
        t0 = now;
      }
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
