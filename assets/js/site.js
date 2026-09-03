(() => {
  const nav = [
    ["index.html", "Accueil"],
    ["quiz.html", "Tests"],
    ["apprendre.html", "Cours"],
    ["panneaux.html", "Panneaux"],
    ["particularites.html", "Spécificités moto"],
    ["trajectoires.html", "Trajectoires"],
    ["plateau.html", "Plateau"],
    ["controles.html", "Contrôles"],
  ];

  const here = (document.body.dataset.page || "index") + ".html";

  function header() {
    return `
      <header class="site-header">
        <div class="wrap header-inner">
          <a class="brand" href="index.html">
            <span class="brand-mark" aria-hidden="true">A</span>
            Code Moto 2026
          </a>
          <nav aria-label="Navigation principale">
            ${nav
              .map(
                ([href, label]) =>
                  `<a href="${href}" ${href === here ? 'aria-current="page"' : ""}>${label}</a>`
              )
              .join("")}
          </nav>
        </div>
      </header>
    `;
  }

  function footer() {
    return `
      <footer class="site-footer">
        <div class="wrap">
          <p>Entraînement à l'épreuve théorique moto (ETM) 2026. Les notes ne sont pas enregistrées : fermer l'onglet efface le score.</p>
          <p>Questions originales d'entraînement, hors banque officielle. Images de panneaux : Wikimedia Commons (signalisation routière française). Vérifiez toujours le <a href="https://www.legifrance.gouv.fr/">Code de la route</a> et le site de la <a href="https://www.securite-routiere.gouv.fr/">Sécurité routière</a>.</p>
        </div>
      </footer>
    `;
  }

  const mountHeader = document.getElementById("site-header");
  const mountFooter = document.getElementById("site-footer");
  if (mountHeader) mountHeader.outerHTML = header();
  if (mountFooter) mountFooter.outerHTML = footer();

  window.CodeMoto = {
    shuffle(list) {
      const arr = [...list];
      for (let i = arr.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
      return arr;
    },
    async loadQuestions() {
      const res = await fetch("data/questions.json");
      if (!res.ok) throw new Error("Impossible de charger les questions.");
      return res.json();
    },
    async loadSigns() {
      const res = await fetch("data/signs.json?v=206");
      if (!res.ok) throw new Error("Impossible de charger les panneaux.");
      return res.json();
    },
  };
})();
