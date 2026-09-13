/* Galeria — karuzela + siatka.

   Listę zdjęć trzyma galeria/zdjecia.js (obiekt window.GALERIA), a pliki
   leżą w galeria/karuzela i galeria/galeria. Taki spis działa na każdym
   hostingu tak samo — GitHub Pages, zwykły serwer, a nawet plik otwarty
   z dysku — bo nie wymaga niczego po stronie serwera.

   Jak dodać zdjęcie: opis na górze galeria/zdjecia.js.

   Sekcja bez zdjęć chowa się sama. */

(function () {
  "use strict";

  const ROZSZERZENIA = /\.(jpe?g|png|webp|avif|gif)$/i;
  const FOLDERY = { karuzela: "galeria/karuzela/", siatka: "galeria/galeria/" };

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- lista zdjęć ---------- */

  const SPIS = window.GALERIA || {};

  // nazwa pliku → ścieżka; pełne adresy (http…) i podane ze ścieżką zostawiamy
  const sciezka = (folder, plik) => {
    const p = String(plik).trim();
    if (!p) return null;
    if (/^(https?:)?\/\//.test(p) || p.indexOf("/") !== -1) return p;
    return folder + encodeURIComponent(p);
  };

  const wczytaj = (folder, klucz) => {
    const wpisy = Array.isArray(SPIS[klucz]) ? SPIS[klucz] : [];
    return wpisy.map((plik) => sciezka(folder, plik)).filter(Boolean);
  };

  /* ---------- budowanie elementów ---------- */

  // 'dobor-oprawek.jpg' → 'dobór oprawek' (na tyle, na ile da się z nazwy pliku)
  const opisZNazwy = (src) => {
    const nazwa = decodeURIComponent(src.split("/").pop() || "");
    return nazwa
      .replace(ROZSZERZENIA, "")
      .replace(/^\d+[\s._-]+/, "")
      .replace(/[._-]+/g, " ")
      .trim();
  };

  // Galeria jest pod nagłówkiem podstrony, więc KAŻDE zdjęcie ładuje się
  // leniwie — przeglądarka pobiera tylko to, co użytkownik zaraz zobaczy.
  // Reszta dociąga się przy przewijaniu karuzeli i strony.
  const zdjecie = (src) => {
    const img = document.createElement("img");
    img.src = src;
    img.alt = opisZNazwy(src) || "Zdjęcie z salonu optycznego Binokl";
    img.loading = "lazy";
    img.decoding = "async";
    img.fetchPriority = "low";
    return img;
  };

  /* ---------- karuzela ---------- */

  function karuzela(sekcja, zdjecia) {
    const tor = sekcja.querySelector("[data-tor]");
    const kropki = sekcja.querySelector("[data-kropki]");
    const licznik = sekcja.querySelector("[data-licznik]");
    const wstecz = sekcja.querySelector("[data-wstecz]");
    const dalej = sekcja.querySelector("[data-dalej]");

    zdjecia.forEach((src, i) => {
      const slajd = document.createElement("div");
      slajd.className = "carousel-slide";
      slajd.appendChild(zdjecie(src));
      tor.appendChild(slajd);

      const kropka = document.createElement("button");
      kropka.type = "button";
      kropka.className = "carousel-dot";
      kropka.setAttribute("aria-label", "Zdjęcie " + (i + 1));
      kropka.addEventListener("click", () => idzDo(i));
      kropki.appendChild(kropka);
    });

    let aktualny = 0;
    const slajdy = () => Array.from(tor.children);

    const idzDo = (i) => {
      const cel = slajdy()[Math.max(0, Math.min(i, zdjecia.length - 1))];
      if (cel) tor.scrollTo({ left: cel.offsetLeft, behavior: prefersReduced ? "auto" : "smooth" });
    };

    // czy tor jest przewinięty do samego końca (z zapasem na zaokrąglenia)
    const naKoncu = () => tor.scrollLeft + tor.clientWidth >= tor.scrollWidth - 2;

    const odswiez = () => {
      // aktywny jest slajd najbliżej lewej krawędzi toru
      let najblizszy = 0;
      let dystans = Infinity;
      slajdy().forEach((s, i) => {
        const d = Math.abs(s.offsetLeft - tor.scrollLeft);
        if (d < dystans) { dystans = d; najblizszy = i; }
      });
      /* W pasku widać kilka zdjęć naraz, więc ostatnie slajdy nigdy nie dojadą
         do lewej krawędzi — przewijanie kończy się wcześniej. Bez tego licznik
         zatrzymywał się na 11/12 i ostatnia kropka była nieosiągalna. */
      if (naKoncu()) najblizszy = zdjecia.length - 1;
      aktualny = najblizszy;
      Array.from(kropki.children).forEach((k, i) => {
        k.classList.toggle("active", i === aktualny);
        k.setAttribute("aria-current", i === aktualny ? "true" : "false");
      });
      if (licznik) licznik.textContent = (aktualny + 1) + " / " + zdjecia.length;
      wstecz.disabled = aktualny === 0;
      dalej.disabled = aktualny === zdjecia.length - 1;
    };

    let czeka = false;
    tor.addEventListener("scroll", () => {
      if (czeka) return;
      czeka = true;
      requestAnimationFrame(() => { czeka = false; odswiez(); });
    }, { passive: true });

    wstecz.addEventListener("click", () => idzDo(aktualny - 1));
    dalej.addEventListener("click", () => idzDo(aktualny + 1));

    // po dociągnięciu zdjęć szerokości slajdów się zmieniają — przelicz stan
    window.addEventListener("resize", odswiez, { passive: true });
    tor.querySelectorAll("img").forEach((img) => {
      if (!img.complete) img.addEventListener("load", odswiez, { once: true });
    });

    sekcja.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") { e.preventDefault(); idzDo(aktualny - 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); idzDo(aktualny + 1); }
    });

    sekcja.hidden = false;
    odswiez();
  }

  /* ---------- siatka ---------- */

  function siatka(sekcja, zdjecia) {
    const box = sekcja.querySelector("[data-siatka]");
    zdjecia.forEach((src) => {
      const kafel = document.createElement("figure");
      kafel.className = "gal-item";
      kafel.appendChild(zdjecie(src));
      box.appendChild(kafel);
    });
    sekcja.hidden = false;
  }

  /* ---------- start ---------- */

  const sekcjaKaruzeli = document.getElementById("karuzela");
  const sekcjaSiatki = document.getElementById("siatka");
  const pustka = document.getElementById("galeriaPusta");
  if (!sekcjaKaruzeli && !sekcjaSiatki) return;

  const doSiatki = wczytaj(FOLDERY.siatka, "galeria");
  // pusta lista karuzeli = pokaż w niej zdjęcia z siatki, żeby sekcja nie znikła
  const doKaruzeli = wczytaj(FOLDERY.karuzela, "karuzela");
  const wKaruzeli = doKaruzeli.length ? doKaruzeli : doSiatki;

  if (sekcjaKaruzeli && wKaruzeli.length) karuzela(sekcjaKaruzeli, wKaruzeli);
  if (sekcjaSiatki && doSiatki.length) siatka(sekcjaSiatki, doSiatki);
  if (pustka && !wKaruzeli.length && !doSiatki.length) pustka.hidden = false;
})();
