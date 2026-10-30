// Interaktivní prvky prezentace: další slovo, živý Markdown/HTML, kalkulačka tokenů.
(function () {
  const $ = (sel, root = document) => root.querySelector(sel);

  // --- jazykový model jako hračka: pravděpodobnosti dalšího slova (vymyšlené) ---
  const START = "Nosník";
  const NEXT = {
    "Nosník": { "IPE": 0.45, "je": 0.25, "nad": 0.18, "byl": 0.12 },
    "IPE": { "300": 0.5, "240": 0.32, "360": 0.18 },
    "300": { "unese": 0.38, "je": 0.32, "z": 0.2, ".": 0.1 },
    "240": { "je": 0.45, "unese": 0.3, "z": 0.25 },
    "360": { "je": 0.5, "z": 0.3, ".": 0.2 },
    "unese": { "120": 0.45, "85": 0.35, "bezpečně": 0.15, "247": 0.05 },
    "bezpečně": { "120": 0.6, "85": 0.4 },
    "120": { "kN": 0.9, ".": 0.1 },
    "85": { "kN": 0.9, ".": 0.1 },
    "247": { "kN": 0.95, ".": 0.05 },
    "kN": { ".": 0.8, "a": 0.2 },
    "je": { "posouzen": 0.4, "z": 0.25, "přetížen": 0.2, "kotven": 0.15 },
    "posouzen": { "podle": 0.6, ".": 0.4 },
    "podle": { "Eurokódu": 0.5, "ČSN": 0.4, "citu": 0.1 },
    "Eurokódu": { ".": 0.7, "a": 0.3 },
    "ČSN": { ".": 0.7, "a": 0.3 },
    "citu": { ".": 1 },
    "přetížen": { "o": 0.55, ".": 0.45 },
    "kotven": { "do": 0.7, ".": 0.3 },
    "do": { "sloupu": 0.6, "zdi": 0.4 },
    "sloupu": { ".": 0.8, "a": 0.2 },
    "zdi": { ".": 1 },
    "z": { "oceli": 0.6, "S355": 0.4 },
    "oceli": { "S355": 0.6, "S235": 0.4 },
    "S355": { ".": 0.6, "a": 0.4 },
    "S235": { ".": 0.6, "a": 0.4 },
    "nad": { "otvorem": 0.6, "vraty": 0.4 },
    "otvorem": { "je": 0.6, ".": 0.4 },
    "vraty": { "je": 0.7, ".": 0.3 },
    "byl": { "posouzen": 0.4, "prodloužen": 0.35, "odstraněn": 0.25 },
    "prodloužen": { "o": 0.75, ".": 0.25 },
    "o": { "200": 0.5, "50": 0.35, "15": 0.15 },
    "200": { "mm": 1 },
    "50": { "mm": 1 },
    "15": { "%": 0.6, "mm": 0.4 },
    "%": { ".": 1 },
    "mm": { ".": 0.8, "a": 0.2 },
    "odstraněn": { ".": 1 },
    "a": { "je": 0.45, "unese": 0.3, "byl": 0.25 },
  };

  function nextWord(root) {
    let words = [START];
    const text = $(".nw-text", root), bars = $(".nw-bars", root);
    function render() {
      text.innerHTML = words.map((w, i) =>
        `<span class="${i === words.length - 1 && i > 0 ? "nw-new" : ""}">${w}</span>`).join(" ");
      bars.innerHTML = "";
      const last = words[words.length - 1];
      const opts = NEXT[last];
      if (last === "." || !opts || words.length > 14) {
        bars.innerHTML = '<div class="nw-done">Konec věty. Zkuste „Znovu“.</div>';
        return;
      }
      Object.entries(opts).sort((a, b) => b[1] - a[1]).forEach(([w, p]) => {
        const row = document.createElement("button");
        row.className = "nw-row";
        row.innerHTML = `<span class="nw-w">${w}</span><span class="nw-bar" style="width:${p * 100}%"></span><span class="nw-p">${Math.round(p * 100)} %</span>`;
        row.onclick = () => { words.push(w); render(); };
        bars.appendChild(row);
      });
    }
    function pick(greedy) {
      const opts = NEXT[words[words.length - 1]];
      if (!opts) return;
      const e = Object.entries(opts);
      if (greedy) { words.push(e.sort((a, b) => b[1] - a[1])[0][0]); }
      else {
        let r = Math.random();
        for (const [w, p] of e) { r -= p; if (r <= 0) { words.push(w); break; } }
        if (r > 0) words.push(e[0][0]);
      }
      render();
    }
    $(".nw-greedy", root).onclick = () => pick(true);
    $(".nw-random", root).onclick = () => pick(false);
    $(".nw-reset", root).onclick = () => { words = [START]; render(); };
    render();
  }

  // --- živý Markdown ---
  function liveMarkdown(root) {
    const src = $("textarea", root), out = $(".live-out", root);
    const update = () => {
      out.innerHTML = window.marked ? window.marked.parse(src.value)
        : "<p>(náhled se načítá…)</p>";
    };
    src.addEventListener("input", update);
    update();
    if (!window.marked) setTimeout(update, 1500);
  }

  // --- živé HTML ---
  function liveHtml(root) {
    const src = $("textarea", root), out = $("iframe", root);
    const update = () => { out.srcdoc = src.value; };
    src.addEventListener("input", update);
    update();
  }

  // --- kalkulačka tokenů ---
  // Ilustrační sazby za milion tokenů, nikoli ceník konkrétních modelů.
  const PRICES = [
    ["Sazba 3 / 15 $", 3, 15],
    ["Sazba 5 / 25 $", 5, 25],
  ];

  function tokens(root) {
    const turns = $(".tk-turns", root), per = $(".tk-per", root), runs = $(".tk-runs", root);
    const out = $(".tk-out", root);
    const fmt = n => n.toLocaleString("cs-CZ");
    function update() {
      const n = +turns.value, k = +per.value * 1000, r = +runs.value;
      $(".tk-turns-v", root).textContent = n;
      $(".tk-per-v", root).textContent = per.value + " tis.";
      $(".tk-runs-v", root).textContent = r;
      const input = k * n * (n + 1) / 2;     // každý krok posílá celou konverzaci znovu
      const output = 2000 * n;
      const costs = PRICES.map(([m, pi, po]) => [m, r * (input * pi + output * po) / 1e6]);
      const max = Math.max(...costs.map(c => c[1]), 0.01);
      out.innerHTML =
        `<div class="tk-sum">Vstup: <b>${fmt(input)}</b> tokenů · výstup: <b>${fmt(output)}</b> tokenů` +
        ` (jeden úkol)</div>` +
        costs.map(([m, c]) => `<div class="tk-row"><span class="tk-m">${m}</span>` +
          `<span class="tk-bar" style="width:${(c / max) * 100}%"></span>` +
          `<span class="tk-c">${c === 0 ? "zdarma" : c.toLocaleString("cs-CZ", { style: "currency", currency: "USD" })}</span></div>`).join("");
    }
    [turns, per, runs].forEach(el => el.addEventListener("input", update));
    update();
  }

  function init() {
    document.querySelectorAll(".nw").forEach(nextWord);
    document.querySelectorAll(".live-md").forEach(liveMarkdown);
    document.querySelectorAll(".live-html").forEach(liveHtml);
    document.querySelectorAll(".tk").forEach(tokens);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
