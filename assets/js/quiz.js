(() => {
  const params = new URLSearchParams(location.search);
  const root = document.getElementById("quiz-root");
  if (!root) return;

  const state = {
    mode: params.get("mode") || "setup",
    category: params.get("cat") || "",
    count: Number(params.get("n") || 40),
    feedback: params.get("feedback") !== "0",
    index: 0,
    answers: [],
    questions: [],
    selected: [],
    locked: false,
    data: null,
  };

  function el(html) {
    const t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }

  function startUrl(opts) {
    const u = new URL("quiz.html", location.href);
    u.search = new URLSearchParams(opts).toString();
    return u.pathname.split("/").pop() + u.search;
  }

  function renderSetup(data) {
    const cats = data.categories
      .map(
        (c) => `
        <button class="cat-btn" type="button" data-cat="${c.id}">
          <strong>${c.label}</strong>
          <small>${c.count} questions · ${c.blurb}</small>
        </button>`
      )
      .join("");

    root.innerHTML = `
      <section class="quiz-shell">
        <p class="kicker">Lancer un test</p>
        <h1>Questions tirées au hasard</h1>
        <p class="lede">Choisissez un examen blanc mixte, une catégorie, ou un mix personnalisé. Le score s'affiche à la fin et n'est pas sauvegardé.</p>

        <div class="card" style="margin:18px 0">
          <h2>Examen blanc ETM</h2>
          <p class="muted">40 questions toutes catégories, comme le jour J. 35/40 pour viser la réussite. Pas de correction avant la fin.</p>
          <div class="actions">
            <a class="btn btn-primary" href="${startUrl({
              mode: "run",
              n: "40",
              feedback: "0",
            })}">Lancer 40 questions mixtes</a>
            <a class="btn btn-ghost" href="${startUrl({
              mode: "run",
              n: "20",
              feedback: "1",
            })}">Série mixte 20 questions, avec correction</a>
          </div>
        </div>

        <h2>Par catégorie</h2>
        <p class="muted">10 questions aléatoires dans le thème choisi, avec correction immédiate.</p>
        <div class="grid" id="cats">${cats}</div>

        <div class="card" style="margin-top:22px">
          <h2>Mix personnalisé</h2>
          <label for="n">Nombre de questions (toutes catégories)</label>
          <input id="n" type="number" min="5" max="${data.questions.length}" value="30" style="margin:10px 12px 0 0;padding:10px;border-radius:10px;border:1px solid var(--line);background:var(--bg-2);color:var(--ink);width:120px">
          <div class="actions">
            <button class="btn btn-primary" id="mix-go" type="button">Démarrer le mix</button>
          </div>
        </div>
      </section>
    `;

    root.querySelectorAll("[data-cat]").forEach((btn) => {
      btn.addEventListener("click", () => {
        location.href = startUrl({
          mode: "run",
          cat: btn.dataset.cat,
          n: "10",
          feedback: "1",
        });
      });
    });
    root.querySelector("#mix-go").addEventListener("click", () => {
      const n = root.querySelector("#n").value;
      location.href = startUrl({ mode: "run", n, feedback: "1" });
    });
  }

  function pickQuestions(data) {
    let pool = data.questions;
    if (state.category) {
      pool = pool.filter((q) => q.category === state.category);
    }
    const n = Math.min(Math.max(state.count, 1), pool.length);
    return window.CodeMoto.shuffle(pool).slice(0, n).map((q) => ({
      ...q,
      choices: window.CodeMoto.shuffle(q.choices),
    }));
  }

  function isCorrect(question, selected) {
    const want = [...question.correct].sort().join(",");
    const got = [...selected].sort().join(",");
    return want === got;
  }

  function renderQuestion() {
    const q = state.questions[state.index];
    const total = state.questions.length;
    const pct = Math.round((state.index / total) * 100);
    const cat = state.data.categories.find((c) => c.id === q.category);
    const multi = q.multi || q.correct.length > 1;
    const img = q.image
      ? `<figure class="q-image"><img src="${q.image}" alt="${q.imageAlt || ""}"><figcaption class="muted" style="font-size:.8rem;margin-top:8px">${q.imageCredit || ""}</figcaption></figure>`
      : "";

    root.innerHTML = `
      <section class="quiz-shell">
        <p class="kicker">${state.feedback ? "Entraînement" : "Examen blanc"} · ${cat ? cat.label : q.category}</p>
        <div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap">
          <strong>Question ${state.index + 1} / ${total}</strong>
          <span class="muted">${multi ? "Plusieurs réponses possibles" : "Une seule réponse"}</span>
        </div>
        <div class="progress" aria-hidden="true"><span style="width:${pct}%"></span></div>
        <article class="question">
          <h1 style="font-size:1.45rem">${q.question}</h1>
          ${img}
          <div class="choices" role="${multi ? "group" : "radiogroup"}">
            ${q.choices
              .map(
                (c) =>
                  `<button class="choice" type="button" data-id="${c.id}" aria-pressed="false">${c.text}</button>`
              )
              .join("")}
          </div>
          <div class="actions">
            <button class="btn btn-primary" id="validate" type="button">Valider</button>
            <a class="btn btn-ghost" href="quiz.html">Abandonner</a>
          </div>
          <p id="explain" class="note hidden"></p>
        </article>
      </section>
    `;

    state.selected = [];
    state.locked = false;
    const buttons = [...root.querySelectorAll(".choice")];
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        if (state.locked) return;
        if (multi) {
          const on = btn.getAttribute("aria-pressed") === "true";
          btn.setAttribute("aria-pressed", on ? "false" : "true");
        } else {
          buttons.forEach((b) => b.setAttribute("aria-pressed", "false"));
          btn.setAttribute("aria-pressed", "true");
        }
        state.selected = buttons
          .filter((b) => b.getAttribute("aria-pressed") === "true")
          .map((b) => b.dataset.id);
      });
    });

    root.querySelector("#validate").addEventListener("click", () => {
      if (!state.selected.length) return;
      const ok = isCorrect(q, state.selected);
      if (state.locked) {
        next();
        return;
      }
      state.answers.push({
        id: q.id,
        selected: [...state.selected],
        ok,
      });
      state.locked = true;
      if (state.feedback) {
        buttons.forEach((b) => {
          if (q.correct.includes(b.dataset.id)) b.classList.add("is-correct");
          else if (state.selected.includes(b.dataset.id)) b.classList.add("is-wrong");
        });
        const box = root.querySelector("#explain");
        box.classList.remove("hidden");
        box.textContent = (ok ? "Correct. " : "Incorrect. ") + q.explanation;
        root.querySelector("#validate").textContent =
          state.index + 1 === total ? "Voir le score" : "Question suivante";
      } else {
        next();
      }
    });
  }

  function next() {
    state.index += 1;
    if (state.index >= state.questions.length) renderResult();
    else renderQuestion();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function renderResult() {
    const total = state.questions.length;
    const good = state.answers.filter((a) => a.ok).length;
    const pct = Math.round((good / total) * 100);
    const exam = total === 40 && !state.category;
    const passed = exam ? good >= 35 : pct >= 80;
    const byCat = {};
    state.questions.forEach((q, i) => {
      byCat[q.category] ||= { ok: 0, n: 0 };
      byCat[q.category].n += 1;
      if (state.answers[i]?.ok) byCat[q.category].ok += 1;
    });
    const rows = Object.entries(byCat)
      .map(([id, v]) => {
        const label = state.data.categories.find((c) => c.id === id)?.label || id;
        return `<tr><th>${label}</th><td>${v.ok}/${v.n}</td></tr>`;
      })
      .join("");
    const wrong = state.questions
      .map((q, i) => ({ q, a: state.answers[i] }))
      .filter((x) => x.a && !x.a.ok)
      .map(({ q, a }) => {
        const chosen = q.choices
          .filter((c) => a.selected.includes(c.id))
          .map((c) => c.text)
          .join(" ; ");
        const right = q.choices
          .filter((c) => q.correct.includes(c.id))
          .map((c) => c.text)
          .join(" ; ");
        return `<article>
          <h3>${q.question}</h3>
          <p><strong>Votre réponse :</strong> ${chosen || "-"}</p>
          <p><strong>Bonne réponse :</strong> ${right}</p>
          <p class="muted">${q.explanation}</p>
        </article>`;
      })
      .join("");

    root.innerHTML = `
      <section class="quiz-shell">
        <div class="result">
          <p class="kicker">Score - non enregistré</p>
          <p class="score-big ${passed ? "pass" : "fail"}">${good}/${total}</p>
          <p>${pct} % · ${
            exam
              ? passed
                ? "Seuil ETM atteint (35/40)."
                : "Sous le seuil ETM (35/40)."
              : passed
                ? "Bonne maîtrise de cette série."
                : "Encore un peu de révision."
          }</p>
          <p class="muted">Rien n'est sauvegardé sur cet appareil ni en ligne.</p>
          <div class="actions" style="justify-content:center">
            <button class="btn btn-primary" id="again" type="button">Rejouer un tirage aléatoire</button>
            <a class="btn btn-ghost" href="quiz.html">Autre mode</a>
            <a class="btn btn-ghost" href="apprendre.html">Revoir le cours</a>
          </div>
        </div>
        <div class="table-wrap" style="margin-top:22px">
          <table>
            <thead><tr><th>Catégorie</th><th>Score</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
        <h2>Questions manquées</h2>
        <div class="review">${wrong || "<p class='muted'>Aucune erreur. Beau travail.</p>"}</div>
      </section>
    `;
    root.querySelector("#again").addEventListener("click", () => {
      state.index = 0;
      state.answers = [];
      state.questions = pickQuestions(state.data);
      renderQuestion();
    });
  }

  async function init() {
    try {
      const data = await window.CodeMoto.loadQuestions();
      state.data = data;
      if (state.mode !== "run") {
        renderSetup(data);
        return;
      }
      state.questions = pickQuestions(data);
      if (!state.questions.length) {
        root.innerHTML = "<p>Aucune question dans cette catégorie.</p>";
        return;
      }
      renderQuestion();
    } catch (err) {
      root.innerHTML = `<p>Erreur de chargement : ${err.message}</p>`;
    }
  }

  init();
})();
