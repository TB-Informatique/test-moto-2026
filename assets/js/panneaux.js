(() => {
  const root = document.getElementById("signs-root");
  if (!root) return;
  const modal = document.getElementById("sign-modal");

  let data = null;
  let family = "all";

  function esc(value) {
    return String(value).replace(/[&<>"']/g, (ch) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[ch]));
  }

  function natKey(code) {
    return String(code).split(/(\d+)/).map((part, i) => (i % 2 ? part.padStart(5, "0") : part.toLowerCase())).join("");
  }

  function ordered(list) {
    const families = Object.keys(data.families);
    return [...list].sort((a, b) => {
      const fa = families.indexOf(a.family);
      const fb = families.indexOf(b.family);
      if (fa !== fb) return fa - fb;
      return natKey(a.code).localeCompare(natKey(b.code));
    });
  }

  function render() {
    const families = data.families;
    const chips = ["all", ...Object.keys(families)]
      .map((id) => {
        const label = id === "all" ? "Tous" : families[id];
        const n = id === "all" ? data.signs.length : data.signs.filter((s) => s.family === id).length;
        return `<button class="chip" type="button" data-family="${esc(id)}" aria-pressed="${
          family === id
        }">${esc(label)} (${n})</button>`;
      })
      .join("");
    const list = ordered(data.signs.filter((s) => family === "all" || s.family === family));
    root.innerHTML = `
      <div class="filters">${chips}</div>
      <p class="muted">${list.length} panneaux affichés, avec image</p>
      <div class="sign-grid">
        ${list
          .map(
            (s) => `
          <button class="sign-card" type="button" data-code="${esc(s.code)}">
            <img src="${esc(s.image)}" alt="${esc(s.title)}" loading="lazy">
            <strong>${esc(s.code)}</strong>
            <span class="muted">${esc(s.title)}</span>
          </button>`
          )
          .join("")}
      </div>
    `;
    root.querySelectorAll("[data-family]").forEach((btn) => {
      btn.addEventListener("click", () => {
        family = btn.dataset.family;
        render();
      });
    });
    root.querySelectorAll(".sign-card").forEach((btn) => {
      btn.addEventListener("click", () => open(btn.dataset.code));
    });
  }

  function open(code) {
    const s = data.signs.find((x) => x.code === code);
    if (!s) return;
    modal.hidden = false;
    modal.querySelector(".modal-card").innerHTML = `
      <img src="${esc(s.image)}" alt="${esc(s.title)}" style="width:160px;background:#fff;border-radius:12px;padding:8px">
      <h3>${esc(s.code)} — ${esc(s.title)}</h3>
      <p>${esc(s.detail)}</p>
      <p class="muted">Famille : ${esc(data.families[s.family])} · source image Wikimedia Commons</p>
      <button class="btn btn-primary" type="button" data-close>Fermer</button>
    `;
    modal.querySelector("[data-close]").addEventListener("click", () => {
      modal.hidden = true;
    });
  }

  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.hidden = true;
  });

  window.CodeMoto.loadSigns().then((json) => {
    data = json;
    render();
  });
})();
