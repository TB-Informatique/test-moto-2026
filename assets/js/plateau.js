(() => {
  const STEPS = [
    {
      id: "poussette",
      num: "1 / 6",
      title: "Poussette — sans moteur",
      type: "Ligne droite guidée, avant puis arrière",
      duration: 7000,
      path: "M90 150 H340",
      backPath: "M340 150 H90",
      twoWay: true,
      color: "#94a3b8",
      cones: [
        { x: 340, y: 118, color: "#f97316" },
        { x: 340, y: 182, color: "#f97316" },
      ],
      stakes: [
        { x: 80, y: 118 },
        { x: 80, y: 182 },
      ],
      cues: [
        { t: 0, action: "walk", text: "Moto droite, regard vers B. Poussez jusqu’à ce que la roue arrière passe les cônes." },
        { t: 0.5, action: "look", text: "Stop court. Regardez derrière, puis reculez : la roue avant doit repasser les cônes." },
      ],
      panel: {
        trajectoire: "Ligne entre les piquets. Avant A→B (roue AR au-delà), arrière B→A (roue AV au-delà). Béquille à la fin.",
        gaz: "Aucun : moteur coupé. Le « gaz » ici, c’est vos jambes, sans à-coups.",
        frein: "Aucun. Si ça part, on rattrape le guidon, on ne lâche pas.",
        attention: "Équilibrer AVANT de bouger. Regard où vous allez, pas sur le phare. 3 essais.",
        difficulte: "Perdre l’équilibre à l’arrêt, braquer trop, reculer de travers et toucher un piquet.",
        train: "Allée plane, gants. Avant / arrière 20 fois d’affilée sans poser autre chose que les pieds de marche.",
      },
    },
    {
      id: "lent",
      num: "2 / 6",
      title: "Allure réduite — seul",
      type: "Slalom lent (trajectoire en S)",
      duration: 10000,
      path: "M70 190 C120 190 130 140 170 140 S220 190 260 190 S310 140 350 140 S400 190 440 190 S490 140 530 140 S590 190 650 190",
      color: "#38bdf8",
      cones: [170, 260, 350, 440, 530].map((x) => ({ x, y: 108, color: "#f97316" })),
      cues: [
        { t: 0, action: "clutch", text: "Patinage + un doigt de frein arrière. Plus c’est lent, mieux c’est (≥ 16 s = A)." },
        { t: 0.15, action: "look", text: "Ne fixez pas le cône : il attire la roue. Visez l’intervalle suivant." },
        { t: 0.45, action: "gas", text: "Un filet de gaz pour ne pas caler — jamais un coup de poignet." },
        { t: 0.7, action: "clutch", text: "On rouvre l’embrayage au millimètre. Le frein avant reste interdit ici." },
      ],
      panel: {
        trajectoire: "S large entre 5 cônes. On reste dans le couloir, sans pied, sans marche arrière.",
        gaz: "Micro-gaz constant pour le ralenti. On n’accélère pas pour rattraper un cône.",
        frein: "Frein AR seulement, pour poser la moto. Frein AV = plonge + pied à terre.",
        attention: "Chrono (1)→(2) : ≥ 16 s = A, 14–16 s = B, < 14 s = C. Regard loin, buste souple.",
        difficulte: "Fixer le cône, relâcher l’embrayage par à-coups, se raidir, vouloir aller trop vite.",
        train: "Gobelets à 2,50 m. Objectif : le plus lent possible, 8 passages sans pied. Comptez à voix haute.",
      },
    },
    {
      id: "freinage",
      num: "3 / 6",
      title: "Freinage d’urgence",
      type: "Ligne droite — construire puis stopper",
      duration: 6000,
      path: "M70 160 L650 160",
      color: "#22c55e",
      radarX: 400,
      stopBox: { x: 560, w: 90 },
      cues: [
        { t: 0, action: "gas", text: "Dès le départ : 3e rapport, on construit 50 km/h. Pas un sprint à la dernière seconde." },
        { t: 0.55, action: "look", text: "Radar C6 : 50 km/h minimum (A2 sans marge). On ne freine PAS avant cette ligne." },
        { t: 0.62, action: "brake", text: "Après C6 : avant fort + arrière, buste bas, regard au fond de la zone d’arrêt." },
      ],
      panel: {
        trajectoire: "Ligne droite. On ne slalome pas. Arrêt : roue avant dans la zone, avant la ligne de fin.",
        gaz: "Avant C6 uniquement. On vise 50 au compteur AU radar, pas après.",
        frein: "Seulement après C6. Roue arrière au sol (stoppie = B). Trop long ou trop tôt = C.",
        attention: "Vitesse insuffisante = C. Anticiper le frein avant la ligne = C.",
        difficulte: "Arriver à 46 km/h, ou freiner trop tard et sortir de la boîte.",
        train: "Un plot « radar » + une boîte d’arrêt. Répéter jusqu’à 50 AU plot ET arrêt DANS la boîte.",
      },
    },
    {
      id: "passager",
      num: "4 / 6",
      title: "Allure réduite — avec passager",
      type: "Lent + demi-tour, assiette changée",
      duration: 9000,
      path: "M650 190 C560 190 500 130 400 130 S260 190 160 190 S110 150 90 120",
      color: "#a78bfa",
      cones: [
        { x: 400, y: 108, color: "#f97316" },
        { x: 260, y: 108, color: "#f97316" },
      ],
      cues: [
        { t: 0, action: "clutch", text: "Départ tout doux : 80 kg de plus. Embrayage + frein AR. Le passager ne parle pas du tracé." },
        { t: 0.35, action: "look", text: "Même regard loin qu’en solo. La moto tourne plus « lourde » : on anticipe plus tôt." },
        { t: 0.7, action: "gas", text: "Filet de gaz pour ne pas caler dans le demi-tour. Immobiliser, le passager descend." },
      ],
      panel: {
        trajectoire: "Parcours lent indiqué jusqu’à l’arrêt B, souvent un demi-tour / passage de piquets.",
        gaz: "Encore plus dosé qu’en solo. Un à-coup fait poser les pieds.",
        frein: "Frein AR encore plus utile : ça cale l’arrière alourdi.",
        attention: "Passager : 2 mains aux poignées, pieds sur les repose-pieds. S’il dicte le tracé = C.",
        difficulte: "Départ en charge, oubli du poids au demi-tour, passager qui se penche à contretemps.",
        train: "Sac lesté d’abord, puis un passager calme. 10 départs arrêtés sans à-coup.",
      },
    },
    {
      id: "slalom",
      num: "5 / 6",
      title: "Slalom à allure normale",
      type: "S rapide, gaz stable",
      duration: 7000,
      path: "M70 190 C120 190 130 140 170 140 S230 190 270 190 S330 140 370 140 S430 190 470 190 S560 190 650 120",
      color: "#f97316",
      cones: [170, 270, 370, 470].map((x) => ({ x, y: 108, color: "#f97316" })),
      radarX: 300,
      cues: [
        { t: 0, action: "gas", text: "3e rapport avant le 1er cône. On construit 40 km/h, gaz stable." },
        { t: 0.35, action: "look", text: "C7 ≥ 40 km/h (A2 sans marge). Regard au-delà du dernier plot, pas sur le cône." },
        { t: 0.75, action: "look", text: "Demi-tour en bout : on relâche un peu, on place, on ne fonce pas déjà vers l’évitement." },
      ],
      panel: {
        trajectoire: "S entre les cônes orange (le bleu n’en fait pas partie), puis demi-tour en bout de piste.",
        gaz: "Stable dans le slalom. On ne coupe pas les gaz à chaque cône.",
        frein: "Pas de gros frein dans les plots. Un léger AR si ça élargit, puis on replace.",
        attention: "Moins de 40 km/h au C7 = C. Toucher un cône (hors évitement) = B.",
        difficulte: "Arriver trop lent, ou regarder le cône et le prendre. Anticiper l’évitement trop tôt.",
        train: "Même slalom, compteur visible. 40 au 3e cône, 8 fois d’affilée, sans toucher.",
      },
    },
    {
      id: "evitement",
      num: "6 / 6",
      title: "Évitement",
      type: "Un appui franc, puis arrêt dans la boîte",
      duration: 6500,
      path: "M70 160 C280 160 360 160 400 160 C460 160 470 100 530 100 C590 100 600 160 650 160",
      color: "#22c55e",
      radarX: 360,
      cones: [
        { x: 500, y: 128, color: "#3b82f6" },
        { x: 560, y: 128, color: "#3b82f6" },
        { x: 620, y: 188, color: "#3b82f6" },
        { x: 660, y: 188, color: "#3b82f6" },
        { x: 620, y: 132, color: "#3b82f6" },
        { x: 660, y: 132, color: "#3b82f6" },
      ],
      stopBox: { x: 600, w: 80 },
      cues: [
        { t: 0, action: "gas", text: "On reconstruit 50 km/h avant C6. Un seul évitement, pas un slalom." },
        { t: 0.45, action: "look", text: "Regard dans le trou de passage, pas sur le cône bleu." },
        { t: 0.62, action: "look", text: "Un appui, on redresse." },
        { t: 0.78, action: "brake", text: "Puis on freine pour finir entre les quatre cônes bleus." },
      ],
      panel: {
        trajectoire: "Ligne, un déport, retour, arrêt dans le carré bleu. Le cône d’évitement est sacré.",
        gaz: "Jusqu’au C6 (≥ 50, marge +5). Ensuite on stabilise, on ne réaccélère pas dans l’appui.",
        frein: "Après l’évitement, pour l’arrêt. Freiner pendant l’appui = glisse ou cône = C.",
        attention: "Cône d’évitement touché = C. Arrêt hors zone = C. Sortie de piste = C.",
        difficulte: "Hésiter (deux appuis), regarder le cône, ou arriver à 42 km/h.",
        train: "Un plot « porte », un radar fictif. 50 au plot, un seul appui, arrêt dans un carré craie.",
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

  const pills = root.querySelector("#step-pills");
  const caption = root.querySelector("#live-caption");
  const badges = root.querySelector("#live-badges");
  const panel = root.querySelector("#step-panel");
  const playBtn = root.querySelector("#play-step");
  const prevBtn = root.querySelector("#prev-step");
  const nextBtn = root.querySelector("#next-step");
  const pathEl = root.querySelector("#run-path");
  const bike = root.querySelector("#bike-dot");
  const extras = root.querySelector("#scene-extras");
  const svg = root.querySelector("#plateau-svg");

  let index = 0;
  let raf = 0;
  let playing = false;

  function setBadge(action) {
    badges.querySelectorAll("[data-action]").forEach((el) => {
      el.setAttribute("aria-pressed", el.dataset.action === action ? "true" : "false");
    });
  }

  function cueAt(step, t) {
    let current = step.cues[0];
    for (const cue of step.cues) {
      if (t >= cue.t) current = cue;
    }
    return current;
  }

  function placeBike(path, t) {
    const len = path.getTotalLength();
    const p = path.getPointAtLength(Math.min(1, Math.max(0, t)) * len);
    bike.setAttribute("cx", p.x.toFixed(1));
    bike.setAttribute("cy", p.y.toFixed(1));
  }

  function drawExtras(step) {
    extras.replaceChildren();
    const ns = "http://www.w3.org/2000/svg";
    (step.cones || []).forEach((c) => {
      const poly = document.createElementNS(ns, "polygon");
      poly.setAttribute("points", `${c.x},${c.y} ${c.x - 8},${c.y + 16} ${c.x + 8},${c.y + 16}`);
      poly.setAttribute("fill", c.color);
      extras.appendChild(poly);
    });
    (step.stakes || []).forEach((s) => {
      const r = document.createElementNS(ns, "rect");
      r.setAttribute("x", s.x - 3);
      r.setAttribute("y", s.y);
      r.setAttribute("width", "6");
      r.setAttribute("height", "28");
      r.setAttribute("rx", "1");
      r.setAttribute("fill", "#cbd5e1");
      extras.appendChild(r);
    });
    if (step.radarX) {
      const line = document.createElementNS(ns, "line");
      line.setAttribute("x1", step.radarX);
      line.setAttribute("x2", step.radarX);
      line.setAttribute("y1", "70");
      line.setAttribute("y2", "210");
      line.setAttribute("stroke", "#fbbf24");
      line.setAttribute("stroke-width", "2");
      line.setAttribute("stroke-dasharray", "6 5");
      extras.appendChild(line);
      const tx = document.createElementNS(ns, "text");
      tx.setAttribute("x", step.radarX + 8);
      tx.setAttribute("y", "66");
      tx.setAttribute("fill", "#fbbf24");
      tx.setAttribute("font-size", "12");
      tx.setAttribute("font-family", "system-ui,sans-serif");
      tx.setAttribute("font-weight", "700");
      tx.textContent = "Radar";
      extras.appendChild(tx);
    }
    if (step.stopBox) {
      const rect = document.createElementNS(ns, "rect");
      rect.setAttribute("x", step.stopBox.x);
      rect.setAttribute("y", "70");
      rect.setAttribute("width", step.stopBox.w);
      rect.setAttribute("height", "140");
      rect.setAttribute("fill", "#22c55e");
      rect.setAttribute("opacity", "0.16");
      extras.appendChild(rect);
    }
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

  function stopPlay() {
    playing = false;
    cancelAnimationFrame(raf);
    playBtn.textContent = "Lire l’animation";
    playBtn.setAttribute("aria-pressed", "false");
  }

  function showStep(i, t = 0) {
    index = (i + STEPS.length) % STEPS.length;
    const step = STEPS[index];
    stopPlay();
    pathEl.setAttribute("d", step.path);
    pathEl.setAttribute("stroke", step.color);
    drawExtras(step);
    placeBike(pathEl, t);
    const cue = cueAt(step, t);
    caption.textContent = cue.text;
    setBadge(cue.action);
    renderPanel(step);
    pills.querySelectorAll("button").forEach((btn, n) => {
      btn.setAttribute("aria-current", n === index ? "step" : "false");
    });
    svg.setAttribute("aria-label", `${step.title}. ${step.type}.`);
  }

  function play() {
    const step = STEPS[index];
    if (playing) {
      stopPlay();
      return;
    }
    playing = true;
    playBtn.textContent = "Pause";
    playBtn.setAttribute("aria-pressed", "true");
    const start = performance.now();
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const dur = reduce ? 1 : step.duration;

    const tick = (now) => {
      const t = (now - start) / dur;
      if (t >= 1) {
        if (step.twoWay) {
          pathEl.setAttribute("d", step.backPath);
        }
        placeBike(pathEl, 1);
        const last = step.cues[step.cues.length - 1];
        caption.textContent = last.text;
        setBadge(last.action);
        stopPlay();
        return;
      }
      if (step.twoWay) {
        if (t < 0.5) {
          pathEl.setAttribute("d", step.path);
          placeBike(pathEl, t * 2);
        } else {
          pathEl.setAttribute("d", step.backPath);
          placeBike(pathEl, (t - 0.5) * 2);
        }
      } else {
        placeBike(pathEl, t);
      }
      const cue = cueAt(step, t);
      caption.textContent = cue.text;
      setBadge(cue.action);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
  }

  STEPS.forEach((step, i) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip";
    btn.textContent = `${i + 1}. ${step.title.split("—")[0].trim()}`;
    btn.addEventListener("click", () => showStep(i));
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

  prevBtn.addEventListener("click", () => showStep(index - 1));
  nextBtn.addEventListener("click", () => showStep(index + 1));
  playBtn.addEventListener("click", play);

  showStep(0);
})();
