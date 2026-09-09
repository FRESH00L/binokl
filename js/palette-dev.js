/* =========================================================================
   PRZEŁĄCZNIK PALET — NARZĘDZIE DEWELOPERSKIE
   Pływający przycisk, który podmienia wariant kolorów na żywo, bez edycji
   arkusza. Warianty czyta z css/styles.css (także te zakomentowane), więc
   zawsze pokazuje to, co naprawdę jest w pliku — nic tu nie duplikujemy.

   Warianty bierze z js/palette-data.js (zrzut arkusza generowany przez
   python tools/palette_data.py, odświeżany też przy build_pages.py). Jeśli
   fetch arkusza się uda — localhost albo GitHub Pages — nadpisuje je świeżym
   odczytem z pliku, więc lokalne zmiany widać bez regeneracji zrzutu.

   Działa wszędzie, także na GitHub Pages; wyłącza się przez ?palette-dev=0.
   Trwały wybór wariantu robi się dalej przez: python tools/palette.py N
   ========================================================================= */
(function () {
  "use strict";

  const params = new URLSearchParams(location.search);
  const forced = params.get("palette-dev");
  if (forced === "0") return;

  const CSS_URL = document.querySelector('link[rel="stylesheet"][href*="styles.css"]')?.getAttribute("href")
                  || "css/styles.css";
  const STORE = "binokl-palette-dev";

  /* --- Wyciąga warianty z arkusza: nagłówek „WARIANT n — NAZWA” + blok :root --- */
  function parseVariants(css) {
    const head = /WARIANT\s+(\d+)\s+—\s+([^\n(]+)/g;
    const out = [];
    let m;
    while ((m = head.exec(css))) {
      const start = css.indexOf(":root", m.index);
      if (start < 0) continue;
      const open = css.indexOf("{", start);
      const close = css.indexOf("}", open);
      if (open < 0 || close < 0) continue;
      const vars = {};
      const decl = /(--[\w-]+)\s*:\s*([^;]+);/g;
      let d;
      while ((d = decl.exec(css.slice(open + 1, close)))) vars[d[1]] = d[2].trim();
      if (Object.keys(vars).length) {
        // Aktywny jest ten blok, który nie leży wewnątrz komentarza — dopisek
        // „(aktywny)” w nagłówku bywa nieaktualny, więc na niego nie patrzymy.
        const before = css.slice(0, start);
        const active = before.lastIndexOf("/*") < before.lastIndexOf("*/");
        out.push({ n: Number(m[1]), name: m[2].trim(), vars, active });
      }
      head.lastIndex = close;
    }
    return out;
  }

  function apply(variant) {
    const root = document.documentElement;
    root.removeAttribute("style");
    if (!variant) return;
    for (const [k, v] of Object.entries(variant.vars)) root.style.setProperty(k, v);
  }

  /* --- Panel (w shadow DOM, żeby style strony na niego nie wpływały) --- */
  function buildUI(variants) {
    const host = document.createElement("div");
    host.id = "palette-dev";
    host.style.cssText = "position:fixed;left:16px;bottom:16px;z-index:99999";
    const sh = host.attachShadow({ mode: "open" });
    sh.innerHTML = `
      <style>
        :host { all: initial; }
        * { box-sizing: border-box; font: 500 12px/1.35 ui-sans-serif, system-ui, sans-serif; }
        .btn { display:flex; align-items:center; gap:8px; padding:9px 13px; border-radius:999px;
               border:1px solid rgba(255,255,255,.18); background:#16171A; color:#F6F5F2;
               cursor:pointer; box-shadow:0 6px 20px rgba(0,0,0,.3); }
        .btn:hover { background:#26282B; }
        .dot { width:10px; height:10px; border-radius:50%; background:#B98A3C; }
        .panel { display:none; margin-bottom:10px; padding:10px; width:250px; border-radius:12px;
                 background:#16171A; color:#F6F5F2; box-shadow:0 12px 34px rgba(0,0,0,.4);
                 border:1px solid rgba(255,255,255,.14); }
        .panel.open { display:block; }
        .hd { display:flex; justify-content:space-between; opacity:.6; text-transform:uppercase;
              letter-spacing:.08em; font-size:10px; margin:2px 2px 8px; }
        .item { display:flex; align-items:center; gap:9px; width:100%; text-align:left; padding:7px 8px;
                margin-bottom:3px; border:0; border-radius:8px; background:transparent; color:inherit; cursor:pointer; }
        .item:hover { background:rgba(255,255,255,.08); }
        .item[aria-current="true"] { background:rgba(255,255,255,.14); }
        .sw { display:flex; flex:0 0 auto; border-radius:5px; overflow:hidden;
              outline:1px solid rgba(255,255,255,.2); outline-offset:-1px; }
        .sw i { display:block; width:11px; height:20px; }
        .nm { flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
        .num { opacity:.5; font-variant-numeric:tabular-nums; }
        .ft { margin:8px 2px 2px; opacity:.5; font-size:10px; line-height:1.4; }
        .err { padding:4px 2px; color:#E0925C; }
      </style>
      <div class="panel" part="panel"></div>
      <button class="btn" type="button" aria-expanded="false"><span class="dot"></span><span class="lbl">Paleta</span></button>`;

    const panel = sh.querySelector(".panel");
    const btn = sh.querySelector(".btn");
    const dot = sh.querySelector(".dot");
    const lbl = sh.querySelector(".lbl");

    btn.addEventListener("click", () => {
      const open = panel.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
    });

    if (!variants.length) {
      panel.innerHTML = `<div class="err">Brak palet. Wygeneruj zrzut arkusza:<br>
        <code>python tools/palette_data.py</code></div>`;
      panel.classList.add("open");
      return host;
    }

    const base = variants.find((v) => v.active) || variants[0];
    const items = [];

    const select = (v, persist) => {
      apply(v === base ? null : v);
      items.forEach((el) => el.setAttribute("aria-current", String(Number(el.dataset.n) === v.n)));
      dot.style.background = v.vars["--accent"] || v.vars["--graphite"] || "#B98A3C";
      lbl.textContent = "Paleta " + v.n;
      if (persist) localStorage.setItem(STORE, String(v.n));
    };

    panel.innerHTML = `<div class="hd"><span>Wariant kolorów</span><span>dev</span></div>`;
    variants.forEach((v) => {
      const el = document.createElement("button");
      el.type = "button";
      el.className = "item";
      el.dataset.n = String(v.n);
      const keys = ["--concrete", "--graphite", "--accent", "--wood-2"];
      el.innerHTML = `<span class="sw">${keys.map((k) => `<i style="background:${v.vars[k] || "transparent"}"></i>`).join("")}</span>
                      <span class="nm">${v.name}</span><span class="num">${v.n}</span>`;
      el.addEventListener("click", () => select(v, true));
      panel.appendChild(el);
      items.push(el);
    });
    const ft = document.createElement("div");
    ft.className = "ft";
    ft.textContent = "Podgląd tylko w przeglądarce. Na stałe: python tools/palette.py N";
    panel.appendChild(ft);

    const saved = Number(localStorage.getItem(STORE));
    select(variants.find((v) => v.n === saved) || base, false);
    return host;
  }

  /* Zrzut z js/palette-data.js to podstawa (działa też przez file://),
     a udany odczyt arkusza tylko go podmienia na świeższy. */
  const bundled = Array.isArray(window.__BINOKL_PALETTES) ? window.__BINOKL_PALETTES : [];

  const start = (variants) => {
    const ui = buildUI(variants.length ? variants : bundled);
    if (document.body) document.body.appendChild(ui);
    else document.addEventListener("DOMContentLoaded", () => document.body.appendChild(ui));
  };

  fetch(CSS_URL, { cache: "no-store" })
    .then((r) => (r.ok ? r.text() : ""))
    .then(parseVariants)
    .catch(() => [])
    .then(start);
})();
