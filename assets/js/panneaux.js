(() => {
  const root = document.getElementById("signs-root");
  if (!root) return;
  const modal = document.getElementById("sign-modal");

  let data = null;
  let family = "all";

  function render() {
    const families = data.families;
    const chips = ["all", ...Object.keys(families)]
      .map((id) => {
        const label = id === "all" ? "Tous" : families[id];
        return `<button class="chip" type="button" data-family="${id}" aria-pressed="${
          family === id
        }">${label}</button>`;
      })
      .join("");
    const list = data.signs.filter((s) => family === "all" || s.family === family);
    root.innerHTML = `
      <div class="filters">${chips}</div>
      <p class="muted">${list.length} panneaux</p>
      <div class="sign-grid">
        ${list
          .map(
            (s) => `
          <button class="sign-card" type="button" data-code="${s.code}">
            <img src="${s.image}" alt="${s.title}">
            <strong>${s.code}</strong>
            <span class="muted">${s.title}</span>
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
      <img src="${s.image}" alt="${s.title}" style="width:160px;background:#fff;border-radius:12px;padding:8px">
      <h3>${s.code} - ${s.title}</h3>
      <p>${s.detail}</p>
      <p class="muted">Famille : ${data.families[s.family]} · source image Wikimedia Commons</p>
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
