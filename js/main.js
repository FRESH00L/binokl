
(function () {
  "use strict";

  const nav = document.getElementById("nav");
  const navToggle = document.getElementById("navToggle");
  const navMobile = document.getElementById("navMobile");
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Rok w stopce --- */
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* --- Sticky navbar --- */
  const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 24);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* --- Menu mobilne --- */
  const closeNav = () => { navMobile.classList.remove("open"); navToggle.setAttribute("aria-expanded", "false"); };
  const toggleNav = () => {
    const isOpen = navMobile.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  };
  if (navToggle) navToggle.addEventListener("click", toggleNav);
  navMobile.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeNav));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && navMobile.classList.contains("open")) { closeNav(); navToggle.focus(); }
  });

  /* --- Scroll reveal --- */
  const revealEls = document.querySelectorAll(".reveal");
  if (prefersReduced || !("IntersectionObserver" in window)) {
    revealEls.forEach((el) => el.classList.add("in"));
    document.querySelectorAll(".fade-in").forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) { entry.target.classList.add("in"); obs.unobserve(entry.target); }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
    // fade-in (eyebrow / hero animacje z animation-delay) uruchamiamy od razu
    document.querySelectorAll(".fade-in").forEach((el) => el.classList.add("in"));
  }

  /* --- Aktywny link nawigacji wg aktualnej podstrony --- */
  const here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("#navLinks a, #navMobile a").forEach((a) => {
    const target = (a.getAttribute("href") || "").split("#")[0];
    if (target && target === here) a.classList.add("active");
  });

  /* --- Formularz kontaktowy: statyczny → mailto ---
     (Strona jest statyczna, więc wysyłamy przez klienta pocztowego.
      Aby zamiast tego wysyłać na serwer, podłącz np. Formspree/Basin
      i zamień poniższą logikę na fetch do endpointu.) */
  const form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const get = (n) => (form.elements[n] ? form.elements[n].value.trim() : "");
      const name = get("name"), phone = get("phone"), email = get("email"), message = get("message");
      const subject = encodeURIComponent(`Zapytanie ze strony — ${name || "klient"}`);
      const body = encodeURIComponent(
        `Imię i nazwisko: ${name}\nTelefon: ${phone}\nE-mail: ${email}\n\nWiadomość:\n${message}`
      );
      window.location.href = `mailto:optyk@binokl.com.pl?subject=${subject}&body=${body}`;

      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        const original = btn.innerHTML;
        btn.innerHTML = "Otwieram program pocztowy…";
        btn.disabled = true;
        setTimeout(() => { btn.innerHTML = original; btn.disabled = false; }, 4000);
      }
    });
  }
})();
