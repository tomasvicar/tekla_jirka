// Interaktivní prvky prezentace: další slovo, živý Markdown/HTML, kalkulačka tokenů.
(function () {
  const $ = (sel, root = document) => root.querySelector(sel);

  // --- jazykový model jako hračka: pravděpodobnosti dalšího slova (vymyšlené) ---
  const NEXT = {
    "Rostliny": { "rostly": 0.42, "ve": 0.23, "byly": 0.2, "kvetly": 0.15 },
    "rostly": { "pomaleji": 0.48, "rychle": 0.22, "ve": 0.18, "celý": 0.12 },
    "pomaleji": { "než": 0.61, "a": 0.21, "kvůli": 0.18 },
    "kvůli": { "soli": 0.55, "suchu": 0.35, "chybě": 0.1 },
    "než": { "kontrola": 0.52, "obvykle": 0.3, "mutant": 0.18 },
    "kontrola": { ".": 0.7, "a": 0.3 },
    "obvykle": { ".": 0.8, "a": 0.2 },
    "mutant": { ".": 0.6, "a": 0.4 },
    "ve": { "skleníku": 0.55, "stínu": 0.25, "tmě": 0.2 },
    "skleníku": { "rostly": 0.5, ".": 0.3, "kvetly": 0.2 },
    "stínu": { "rostly": 0.6, ".": 0.4 },
    "tmě": { "rostly": 0.7, ".": 0.3 },
    "byly": { "menší": 0.5, "zelené": 0.3, "vysoké": 0.2 },
    "menší": { "než": 0.6, "a": 0.4 },
    "zelené": { "a": 0.5, ".": 0.5 },
    "vysoké": { "247": 0.05, "a": 0.55, ".": 0.4 },
    "247": { "cm": 0.9, ".": 0.1 },
    "cm": { ".": 1 },
    "kvetly": { "dříve": 0.5, "ve": 0.2, ".": 0.3 },
    "dříve": { "než": 0.7, ".": 0.3 },
    "rychle": { "a": 0.4, ".": 0.6 },
    "celý": { "týden": 0.7, "měsíc": 0.3 },
    "týden": { ".": 0.7, "a": 0.3 },
    "měsíc": { ".": 1 },
    "a": { "kvetly": 0.4, "byly": 0.35, "rostly": 0.25 },
    "soli": { ".": 0.7, "a": 0.3 },
    "suchu": { ".": 0.7, "a": 0.3 },
    "chybě": { ".": 1 },
  };

  function nextWord(root) {
    let words = ["Rostliny"];
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
    $(".nw-reset", root).onclick = () => { words = ["Rostliny"]; render(); };
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
    ["Sazba 1 / 5 $", 1, 5],
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
