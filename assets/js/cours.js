(() => {
  const hub = document.getElementById("cours-hub");
  const lessonRoot = document.getElementById("cours-lesson");
  if (!hub && !lessonRoot) return;

  const params = new URLSearchParams(location.search);

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderBlock(block) {
    switch (block.type) {
      case "p":
        return block.text
          .split("\n\n")
          .map((para) => `<p>${esc(para)}</p>`)
          .join("");
      case "ul":
        return `<ul>${block.items.map((it) => `<li>${esc(it)}</li>`).join("")}</ul>`;
      case "ol":
        return `<ol>${block.items.map((it) => `<li>${esc(it)}</li>`).join("")}</ol>`;
      case "note":
        return `<p class="note">${esc(block.text)}</p>`;
      case "trap":
        return `<p class="exam-trap"><strong>Piège d'examen.</strong> ${esc(block.text)}</p>`;
      case "table":
        return `<div class="table-wrap"><table><thead><tr>${block.headers
          .map((h) => `<th>${esc(h)}</th>`)
          .join("")}</tr></thead><tbody>${block.rows
          .map((row) => `<tr>${row.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`)
          .join("")}</tbody></table></div>`;
      case "links":
        return `<p class="course-links">${block.items
          .map((it) => `<a href="${esc(it.href)}">${esc(it.label)}</a>`)
          .join(" · ")}</p>`;
      default: {
        const _exhaustive = block.type;
        return `<p class="muted">Bloc inconnu : ${esc(_exhaustive)}</p>`;
      }
    }
  }

  function themeById(data, id) {
    return data.themes.find((t) => t.id === id) || data.themes[0];
  }

  function lessonById(theme, id) {
    return theme.lessons.find((l) => l.id === id) || theme.lessons[0];
  }

  function renderHub(data) {
    hub.innerHTML = `
      <p class="kicker">Apprentissage</p>
      <h1>Le code moto, leçon par leçon</h1>
      <p class="lede">Sous-pages pour préparer un vrai ETM : règles, pièges, et ce que l'examinateur attend. ${data.lessonCount} leçons, 9 thèmes officiels plus le format de l'épreuve.</p>
      <p class="note">${esc(data.source.credit)} <a href="${esc(data.source.file)}">Ouvrir le PDF source</a>.</p>
      <div class="course-hub-grid">
        ${data.themes
          .map(
            (t) => `
          <article class="card">
            <p class="kicker">${t.code ? `Thème ${esc(t.code)}` : "Avant l'examen"}</p>
            <h2>${esc(t.title)}</h2>
            <p>${esc(t.blurb)}</p>
            <ol class="course-mini-toc">
              ${t.lessons
                .map(
                  (l) =>
                    `<li><a href="cours.html?t=${encodeURIComponent(t.id)}&amp;l=${encodeURIComponent(l.id)}">${esc(l.title)}</a></li>`
                )
                .join("")}
            </ol>
          </article>`
          )
          .join("")}
      </div>
      <div class="actions">
        <a class="btn btn-primary" href="quiz.html">Tester ensuite</a>
        <a class="btn btn-ghost" href="panneaux.html">Panneaux</a>
        <a class="btn btn-ghost" href="trajectoires.html">Trajectoires</a>
        <a class="btn btn-ghost" href="plateau.html">Plateau</a>
      </div>
    `;
  }

  function renderLesson(data) {
    const theme = themeById(data, params.get("t") || "epreuve");
    const current = lessonById(theme, params.get("l") || theme.lessons[0].id);
    const idx = theme.lessons.findIndex((l) => l.id === current.id);
    const prev = idx > 0 ? theme.lessons[idx - 1] : null;
    const next = idx < theme.lessons.length - 1 ? theme.lessons[idx + 1] : null;
    const quizHref = current.quiz
      ? `quiz.html?mode=run&cat=${encodeURIComponent(current.quiz)}&n=10&feedback=1`
      : "quiz.html";

    document.title = `${current.title} - Cours moto ETM 2026`;

    lessonRoot.innerHTML = `
      <div class="course-layout">
        <aside class="course-aside">
          <p class="kicker"><a href="apprendre.html">Tous les cours</a></p>
          <nav class="course-toc" aria-label="Leçons du thème">
            ${data.themes
              .map(
                (t) => `
              <details ${t.id === theme.id ? "open" : ""}>
                <summary>${t.code ? `${esc(t.code)} · ` : ""}${esc(t.title)}</summary>
                <ul>
                  ${t.lessons
                    .map((l) => {
                      const href = `cours.html?t=${encodeURIComponent(t.id)}&amp;l=${encodeURIComponent(l.id)}`;
                      const on = t.id === theme.id && l.id === current.id;
                      return `<li><a href="${href}" ${on ? 'aria-current="page"' : ""}>${esc(l.title)}</a></li>`;
                    })
                    .join("")}
                </ul>
              </details>`
              )
              .join("")}
          </nav>
        </aside>
        <article class="lesson course-article">
          <p class="kicker">${theme.code ? `Thème ${esc(theme.code)}` : "Épreuve"} · ${idx + 1}/${theme.lessons.length}</p>
          <h1>${esc(current.title)}</h1>
          <p class="lede">${esc(current.lede)}</p>
          ${current.blocks.map(renderBlock).join("")}
          <div class="actions">
            ${prev ? `<a class="btn btn-ghost" href="cours.html?t=${theme.id}&amp;l=${prev.id}">← ${esc(prev.title)}</a>` : `<a class="btn btn-ghost" href="apprendre.html">← Tous les cours</a>`}
            <a class="btn btn-primary" href="${quizHref}">S'entraîner</a>
            ${next ? `<a class="btn btn-ghost" href="cours.html?t=${theme.id}&amp;l=${next.id}">${esc(next.title)} →</a>` : `<a class="btn btn-ghost" href="apprendre.html">Sommaire</a>`}
          </div>
        </article>
      </div>
    `;
  }

  window.CodeMoto.loadCours()
    .then((data) => {
      if (hub) renderHub(data);
      if (lessonRoot) renderLesson(data);
    })
    .catch((err) => {
      const el = hub || lessonRoot;
      el.innerHTML = `<p class="note">Impossible de charger les cours. ${esc(err.message)}</p>`;
    });
})();
