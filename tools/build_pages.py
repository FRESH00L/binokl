# -*- coding: utf-8 -*-
"""Generator stron Binokl — wspólny navbar, stopka i układ naprzemiennych bloków.

Uruchamiać z katalogu głównego projektu:  python tools/build_pages.py
Generuje: index.html, o-nas.html, badanie-wzroku.html, oferta.html, opinie.html, kontakt.html
"""
import io

SITE = "https://www.binokl.com.pl/"

# ---------------------------------------------------------------- ikony i logo
LOGO = """<svg class="brand-logo" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true">
          <circle cx="13" cy="27" r="9"/><circle cx="35" cy="27" r="9"/><path d="M22 25.5c1.2-1.2 2.8-1.2 4 0"/><path d="M4 27c-1.2-3 0-9 4-10.5"/><path d="M44 27c1.2-3 0-9-4-10.5"/><circle cx="13" cy="27" r="3.4" fill="currentColor" stroke="none"/><circle cx="35" cy="27" r="3.4" fill="currentColor" stroke="none"/>
        </svg>"""

CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M9 16l2 2 4-4"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'
TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26"/></svg>'
STARS = '<div class="stars" aria-label="Ocena 5 na 5">' + STAR * 5 + '</div>'
SEND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/></svg>'
ROUTE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>'

MAPS_Q = "https://maps.google.com/?q=Wyszy%C5%84skiego+5a+Piekary+%C5%9Al%C4%85skie"
MAPS_EMBED = "https://maps.google.com/maps?q=Wyszy%C5%84skiego%205a%20Piekary%20%C5%9Al%C4%85skie&z=16&output=embed"

# ------------------------------------------------------------------- nawigacja
# Każda pozycja to jedna podstrona — dzięki temu w menu podświetla się dokładnie jedna.
NAV_ITEMS = [
    ("o-nas.html", "O nas"),
    ("badanie-wzroku.html", "Badanie wzroku"),
    ("oferta.html", "Oferta"),
    ("opinie.html", "Opinie"),
    ("kontakt.html", "Kontakt"),
]

ORG_LD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Optician",
    "@id": "https://www.binokl.com.pl/#organization",
    "name": "Binokl — Salon Optyczny",
    "legalName": "Binokl. Zakład optyczny. Mamys-Wróbel K.",
    "description": "Salon optyczny w Piekarach Śląskich. Komputerowe badanie wzroku, indywidualny dobór oprawek, okulary korekcyjne i przeciwsłoneczne, soczewki kontaktowe oraz serwis okularów.",
    "url": "https://www.binokl.com.pl/",
    "logo": "https://www.binokl.com.pl/assets/favicon.svg",
    "image": "https://www.binokl.com.pl/assets/img/og-image.jpg",
    "telephone": "+48327674462",
    "email": "optyk@binokl.com.pl",
    "priceRange": "$$",
    "currenciesAccepted": "PLN",
    "paymentAccepted": "Gotówka, Karta płatnicza",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Wyszyńskiego 5a",
      "addressLocality": "Piekary Śląskie",
      "postalCode": "41-940",
      "addressRegion": "śląskie",
      "addressCountry": "PL"
    },
    "geo": { "@type": "GeoCoordinates", "latitude": 50.38, "longitude": 18.95 },
    "hasMap": "https://maps.google.com/?q=Wyszy%C5%84skiego+5a+Piekary+%C5%9Al%C4%85skie",
    "openingHoursSpecification": [
      { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "10:00", "closes": "17:00" },
      { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "13:00" }
    ],
    "areaServed": [
      { "@type": "City", "name": "Piekary Śląskie" },
      { "@type": "City", "name": "Bytom" },
      { "@type": "City", "name": "Radzionków" },
      { "@type": "City", "name": "Tarnowskie Góry" }
    ],
    "hasOfferCatalog": {
      "@type": "OfferCatalog",
      "name": "Usługi optyczne",
      "itemListElement": [
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Komputerowe badanie wzroku" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Profesjonalny dobór oprawek" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Okulary korekcyjne" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Okulary przeciwsłoneczne" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Soczewki kontaktowe" } },
        { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Serwis i naprawa okularów" } }
      ]
    },
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "3", "bestRating": "5", "worstRating": "1" }
  }
  </script>
  <script type="application/ld+json">
  { "@context": "https://schema.org", "@type": "WebSite", "name": "Binokl — Salon Optyczny", "url": "https://www.binokl.com.pl/", "inLanguage": "pl-PL", "publisher": { "@id": "https://www.binokl.com.pl/#organization" } }
  </script>
"""


def head(title, desc, slug, extra_ld="", preload_hero=False):
    canonical = SITE if slug == "index.html" else SITE + slug
    hero = ('  <link rel="preload" as="image" href="assets/img/ph-hero.jpg" fetchpriority="high" />\n'
            if preload_hero else "")
    return """<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <title>%s</title>
  <meta name="description" content="%s" />
  <meta name="author" content="Binokl — Salon Optyczny" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="geo.region" content="PL-24" />
  <meta name="geo.placename" content="Piekary Śląskie" />
  <meta name="theme-color" content="#33322E" />
  <link rel="canonical" href="%s" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Binokl — Salon Optyczny" />
  <meta property="og:locale" content="pl_PL" />
  <meta property="og:title" content="%s" />
  <meta property="og:description" content="%s" />
  <meta property="og:url" content="%s" />
  <meta property="og:image" content="https://www.binokl.com.pl/assets/img/og-image.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://www.binokl.com.pl/assets/img/og-image.jpg" />

  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="assets/favicon.svg" />
  <link rel="manifest" href="site.webmanifest" />

  <link rel="preload" href="assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="assets/fonts/hanken-latin.woff2" as="font" type="font/woff2" crossorigin />
%s  <link rel="stylesheet" href="css/styles.css" />

%s</head>

<body>
  <a class="skip-link" href="#tresc">Przejdź do treści</a>
""" % (title, desc, canonical, title, desc, canonical, hero, extra_ld)


def nav():
    links = "\n".join('          <li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV_ITEMS)
    mob = "\n".join('        <li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV_ITEMS)
    return """
  <header class="nav" id="nav">
    <div class="wrap nav-inner">
      <a class="brand" href="index.html" aria-label="Binokl — strona główna">
        %s
        <span><span class="brand-name">Binokl</span><span class="brand-sub">Zakład optyczny</span></span>
      </a>

      <nav aria-label="Nawigacja główna">
        <ul class="nav-links" id="navLinks">
%s
        </ul>
      </nav>

      <div class="nav-right">
        <a class="btn btn-accent nav-cta" href="kontakt.html">%s Zarezerwuj wizytę</a>
        <button class="nav-toggle" id="navToggle" aria-label="Menu" aria-expanded="false" aria-controls="navMobile">
          <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
          <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>
        </button>
      </div>
    </div>

    <div class="nav-mobile" id="navMobile">
      <ul>
%s
        <li class="cta"><a class="btn btn-accent" href="kontakt.html">Zarezerwuj wizytę</a></li>
      </ul>
    </div>
  </header>
""" % (LOGO, links, CAL, mob)


FOOTER = """
  <footer class="footer">
    <div class="wrap footer-inner">
      <div class="footer-grid">
        <div>
          <a class="brand" href="index.html">
            %s
            <span><span class="brand-name">Binokl</span><span class="brand-sub">Zakład optyczny</span></span>
          </a>
          <p class="footer-about">Kameralny salon optyczny w Piekarach Śląskich. Komputerowe badanie wzroku i indywidualny dobór oprawek — od 30 lat w tym samym miejscu.</p>
        </div>
        <nav>
          <h4>Nawigacja</h4>
          <ul>
            <li><a href="o-nas.html">O nas</a></li>
            <li><a href="badanie-wzroku.html">Badanie wzroku</a></li>
            <li><a href="oferta.html">Oferta</a></li>
            <li><a href="opinie.html">Opinie</a></li>
            <li><a href="kontakt.html">Kontakt</a></li>
          </ul>
        </nav>
        <div>
          <h4>Kontakt</h4>
          <ul class="footer-contact">
            <li>%s<span>Wyszyńskiego 5a, Piekary Śląskie</span></li>
            <li>%s<a href="tel:+48327674462">32 767 44 62</a></li>
            <li>%s<a href="mailto:optyk@binokl.com.pl">optyk@binokl.com.pl</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; <span id="year">2026</span> Binokl — Salon Optyczny. Wszelkie prawa zastrzeżone.</p>
        <nav><a href="polityka-prywatnosci.html">Polityka prywatności</a></nav>
      </div>
    </div>
  </footer>

  <script src="js/main.js" defer></script>
</body>
</html>
""" % (LOGO, PIN, TEL, MAIL)


def page_head(crumb, title, lead):
    return """
    <section class="page-head tex-brick grain">
      <div class="wrap">
        <nav class="crumbs" aria-label="Ścieżka nawigacji">
          <a href="index.html">Strona główna</a><span class="sep">/</span><span>%s</span>
        </nav>
        <h1 class="page-title fade-in">%s</h1>
        <p class="page-lead fade-in" style="animation-delay:.12s">%s</p>
      </div>
    </section>
""" % (crumb, title, lead)


def alt_row(img, alt, body, eager=False):
    """Jeden naprzemienny blok: zdjęcie w jednej kolumnie, opis w drugiej."""
    loading = "" if eager else ' loading="lazy"'
    return """      <div class="alt-row reveal">
        <div class="alt-media">
          <img src="assets/img/%s.jpg" alt="%s" width="1400" height="1050"%s />
        </div>
        <div class="alt-body">
%s
        </div>
      </div>
""" % (img, alt, loading, body)


def alt_section(rows, klass="alt section--light"):
    return '\n    <section class="%s">\n      <div class="wrap">\n%s      </div>\n    </section>\n' % (
        klass, "".join(rows))


def cta_band(title, text):
    return """
    <section class="cta-band tex-brick grain">
      <div class="wrap">
        <div>
          <h2>%s</h2>
          <p>%s</p>
        </div>
        <div class="actions">
          <a class="btn btn-accent" href="kontakt.html">%s Umów badanie</a>
          <a class="btn btn-ghost" href="tel:+48327674462">%s 32 767 44 62</a>
        </div>
      </div>
    </section>
""" % (title, text, CAL, TEL)


def write(slug, html):
    io.open(slug, "w", encoding="utf-8", newline="\n").write(html)
    print("napisano %-22s %6d B" % (slug, len(html)))


def page(slug, title, desc, body, extra_ld="", preload_hero=False):
    write(slug, head(title, desc, slug, extra_ld, preload_hero) + nav()
          + '\n  <main id="tresc">\n' + body + '\n  </main>\n' + FOOTER)


# ============================================================ STRONA GŁÓWNA
PILLARS = [
    ("o-nas.html", "O nas", "pillar--graphite"),
    ("badanie-wzroku.html", "Badanie wzroku", "pillar--accent"),
    ("kontakt.html", "Kontakt", "pillar--stone"),
]
pillars = "\n".join("""      <a class="pillar %s" href="%s">
        <h2>%s</h2>
        <span class="go">%s</span>
      </a>""" % (cls, href, name, ARROW) for href, name, cls in PILLARS)

index_body = """
    <section class="hero">
      <div class="hero-img">
        <img src="assets/img/ph-hero.jpg" alt="Ekspozycja oprawek okularowych w salonie optycznym Binokl" width="2000" height="1125" fetchpriority="high" />
      </div>
      <h1 class="hero-motto fade-in">
        <span class="m1">Zobacz ostro</span>
        <span class="m2">w pełnych barwach</span>
      </h1>
    </section>

    <nav class="pillars" aria-label="Główne działy">
%s
    </nav>

    <section class="strip" aria-label="Godziny otwarcia i dane kontaktowe">
      <div class="wrap strip-inner">
        <div class="strip-item">
          %s
          <div>
            <p class="t1">Otwarte</p>
            <p class="t2">Pon–Pt 10:00–17:00<br>Sobota 10:00–13:00</p>
          </div>
        </div>
        <div class="strip-item">
          %s
          <div>
            <p class="t1">Telefon</p>
            <p class="t2"><a href="tel:+48327674462">32 767 44 62</a></p>
          </div>
        </div>
        <div class="strip-item">
          %s
          <div>
            <p class="t1">Adres</p>
            <p class="t2"><a href="%s" target="_blank" rel="noopener noreferrer">Wyszyńskiego 5a<br>Piekary Śląskie</a></p>
          </div>
        </div>
      </div>
    </section>
""" % (pillars, CLOCK, TEL, PIN, MAPS_Q)

page("index.html",
     "Binokl — Salon Optyczny Piekary Śląskie | Badanie wzroku",
     "Salon optyczny w Piekarach Śląskich. Komputerowe badanie wzroku, indywidualny dobór oprawek, okulary korekcyjne i przeciwsłoneczne oraz soczewki kontaktowe.",
     index_body, extra_ld=ORG_LD, preload_hero=True)


# ==================================================================== O NAS
POINTS = [
    "Indywidualny dobór szkieł do każdej wady i stylu życia",
    "Nowoczesny sprzęt diagnostyczny i doświadczenie w trudnych korekcjach",
    "Spokojna, kameralna atmosfera bez pośpiechu i bez sprzedażowej presji",
    "Serwis okularów kupionych u nas i poza salonem",
]
points_html = "\n".join(
    '            <li><span class="tick">%s</span><span>%s</span></li>' % (TICK, p) for p in POINTS)

o_nas = page_head(
    "O nas", "O nas",
    "Zakład optyczny prowadzony w Piekarach Śląskich od ponad 30 lat. Badanie, dobór szkieł i regulację oprawek wykonuje u nas ta sama osoba — od pierwszej rozmowy do odbioru okularów."
) + alt_section([
    alt_row("ph-salon", "Wnętrze salonu optycznego Binokl z ekspozycją oprawek", """          <span class="eyebrow"><span class="line"></span>Kim jesteśmy</span>
          <h2>Zakład, który stoi tu od 30 lat</h2>
          <p>Binokl to niewielki salon przy Wyszyńskiego 5a — jedna sala, jedno stanowisko badania i ekspozycja, którą można spokojnie obejrzeć bez tłoku. Przez trzydzieści lat pracy przy tym samym warsztacie zebrało się doświadczenie, którego nie zastąpi automat: wyczucie, jak oprawka osiądzie na nosie i jak zachowa się szkło progresywne u kogoś, kto cały dzień patrzy w monitor.</p>
          <p>Obsługujemy Piekary Śląskie oraz okolice — Bytom, Radzionków i Tarnowskie Góry.</p>""", eager=True),
    alt_row("ph-wnetrze", "Kameralne wnętrze salonu z drewnianymi meblami", """          <span class="eyebrow"><span class="line"></span>Jak pracujemy</span>
          <h2>Jedna wizyta, jedna osoba</h2>
          <p>Badanie wykonujemy po umówieniu, żeby nikt nie czekał w kolejce i żeby nie trzeba było się spieszyć. Cały proces prowadzi jedna osoba: rozmowa o tym, do czego potrzebujesz okularów, badanie, przymiarki, a po kilku dniach odbiór i regulacja.</p>
          <p>Jeśli coś w gotowych okularach przeszkadza — wracasz i poprawiamy. To część usługi, nie dodatkowa wizyta.</p>"""),
    alt_row("ph-oprawki", "Rząd oprawek okularowych na ekspozycji", """          <span class="eyebrow"><span class="line"></span>Nasze zasady</span>
          <h2>Dobór, nie sprzedaż</h2>
          <p>Nie namawiamy na najdroższe szkła. Mówimy wprost, kiedy tańsze rozwiązanie wystarczy, a kiedy warto dopłacić — i kiedy zamiast okularów potrzebna jest wizyta u lekarza.</p>
          <ul class="alt-list">
%s
          </ul>""" % points_html),
]) + cta_band(
    "Wpadnij na badanie",
    "Wystarczy telefon albo krótka wiadomość — dobierzemy termin, w którym salon jest wolny tylko dla Ciebie.")

page("o-nas.html", "O nas — Binokl, Salon Optyczny w Piekarach Śląskich",
     "Zakład optyczny Binokl w Piekarach Śląskich — 30 lat praktyki, indywidualny dobór szkieł i oprawek, kameralna atmosfera bez pośpiechu.",
     o_nas)


# =========================================================== BADANIE WZROKU
SERVICE_LD = """  <script type="application/ld+json">
  { "@context": "https://schema.org", "@type": "Service", "serviceType": "Komputerowe badanie wzroku",
    "provider": { "@id": "https://www.binokl.com.pl/#organization" },
    "areaServed": ["Piekary Śląskie", "Bytom", "Radzionków", "Tarnowskie Góry"],
    "url": "https://www.binokl.com.pl/badanie-wzroku.html" }
  </script>
"""

STEPS = [
    ("ph-tablica", "Okulary próbne przed tablicą do badania ostrości wzroku", "01",
     "Rozmowa o tym, do czego potrzebujesz okularów",
     ["Zaczynamy od pytań: ile godzin dziennie patrzysz w ekran, czy prowadzisz samochód po zmroku, "
      "czy dotychczasowe okulary gdzieś uwierają, jak dawno były zmieniane. Odpowiedzi decydują później o typie szkieł."],
     ""),
    ("ph-foropter", "Foropter — urządzenie do doboru mocy szkieł korekcyjnych", "02",
     "Komputerowe badanie wzroku",
     ["Sprzęt diagnostyczny daje punkt wyjścia, a właściwą korekcję ustalamy krok po kroku — sprawdzając kolejne "
      "moce szkieł, aż obraz będzie ostry i wygodny dla obu oczu jednocześnie."],
     "ok. 20 minut"),
    ("ph-oprawa-probna", "Oprawa próbna założona podczas badania wzroku", "03",
     "Przymiarki i dobór oprawek",
     ["Wybieramy oprawkę pasującą do korekcji, kształtu twarzy i sposobu noszenia. Przy mocniejszych wadach kształt "
      "oprawki wpływa na grubość szkła — mówimy o tym od razu, przed zamówieniem, a nie przy odbiorze."],
     ""),
    ("ph-dobor", "Optyk prezentujący oprawki przed tablicą okulistyczną", "04",
     "Odbiór, regulacja i serwis",
     ["Gotowe okulary dopasowujemy na miejscu: zauszniki, nosek, kąt oprawy. Jeśli po kilku dniach noszenia coś "
      "przeszkadza, wracasz i regulujemy ponownie.",
      "Serwisujemy też okulary kupione gdzie indziej — regulacja, wymiana zauszników, lutowanie, wymiana soczewek."],
     "regulacja na miejscu"),
]
step_rows = []
for i, (img, alt, no, title, paras, meta) in enumerate(STEPS):
    body = '          <span class="alt-no">%s</span>\n          <h2>%s</h2>\n' % (no, title)
    body += "\n".join("          <p>%s</p>" % p for p in paras)
    if meta:
        body += '\n          <span class="alt-meta">%s</span>' % meta
    step_rows.append(alt_row(img, alt, body, eager=(i == 0)))

badanie = page_head(
    "Badanie wzroku", "Badanie wzroku",
    "Komputerowa diagnostyka, dobór oprawek i serwis okularów — wszystko w jednym miejscu, w trakcie jednej wizyty. Zwykle mieścimy się w godzinie."
) + alt_section(step_rows) + cta_band(
    "Zarezerwuj termin badania",
    "Badanie wykonujemy po umówieniu, żeby nikt nie czekał w kolejce. Zadzwoń lub zostaw wiadomość — odezwiemy się z propozycją godziny.")

page("badanie-wzroku.html", "Badanie wzroku Piekary Śląskie — Binokl, Salon Optyczny",
     "Komputerowe badanie wzroku w Piekarach Śląskich: przebieg wizyty krok po kroku, dobór oprawek, regulacja i serwis okularów.",
     badanie, extra_ld=SERVICE_LD)


# =================================================================== OFERTA
OFFERS = [
    ("ph-korekcyjne", "Okulary korekcyjne z lekką oprawką", "Okulary korekcyjne",
     ["Lekkie oprawki i nowoczesne szkła dopasowane do wady oraz trybu życia. Szkła jednoogniskowe, biurowe i "
      "progresywne, z powłokami antyrefleksyjnymi i utwardzającymi.",
      "Przy pracy przy ekranie dobieramy szkła z filtrem światła niebieskiego lub osobną parę do biurka — "
      "podpowiemy, co w Twoim przypadku ma sens."]),
    ("ph-przeciwsloneczne", "Okulary przeciwsłoneczne z ochroną UV", "Okulary przeciwsłoneczne",
     ["Pełna ochrona UV w wydaniu, które nie idzie na kompromis ze stylem. Okulary gotowe oraz wykonane z korekcją, "
      "również w wersji polaryzacyjnej — dla kierowców i osób pracujących w silnym słońcu."]),
    ("ph-soczewki", "Soczewki kontaktowe", "Soczewki kontaktowe",
     ["Soczewki jednodniowe i miesięczne znanych producentów, wraz z doborem parametrów i nauką bezpiecznego "
      "zakładania oraz pielęgnacji.",
      "Do soczewek dobieramy też płyny i akcesoria; przy pierwszym zakupie pokazujemy całą procedurę na miejscu."]),
]
offer_rows = []
for i, (img, alt, title, paras) in enumerate(OFFERS):
    body = "          <h2>%s</h2>\n" % title + "\n".join("          <p>%s</p>" % p for p in paras)
    offer_rows.append(alt_row(img, alt, body, eager=(i == 0)))

oferta = page_head(
    "Oferta", "Oferta",
    "Okulary korekcyjne, przeciwsłoneczne i soczewki kontaktowe. Wszystko dobierane na miejscu, po badaniu i przymiarce."
) + alt_section(offer_rows) + cta_band(
    "Chcesz zobaczyć oprawki na sobie?",
    "Przymiarka nic nie kosztuje i nie zobowiązuje. Wpadnij w godzinach otwarcia albo umów się na spokojny termin.")

page("oferta.html", "Oferta — okulary i soczewki | Binokl, Piekary Śląskie",
     "Oferta salonu Binokl: okulary korekcyjne, okulary przeciwsłoneczne z ochroną UV oraz soczewki kontaktowe jednodniowe i miesięczne.",
     oferta)


# =================================================================== OPINIE
REVIEWS = [
    ("ph-klientka", "Klientka salonu przymierzająca oprawki przy ekspozycji", "A", "Aleksandra K.", "Klientka salonu",
     "Najlepszy optyk, do jakiego trafiłam. Pani idealnie dobrała oprawki, tłumacząc, na co dokładnie zwrócić uwagę "
     "przy danej wadzie. Jestem zachwycona i polecam z całego serca!"),
    ("ph-klient", "Klient w okularach korekcyjnych", "B", "Bartek K.", "Klient salonu",
     "Świetny optyk, w którym nie tylko znajdziesz ciekawe oprawki, ale dowiesz się bardzo dużo na temat doboru "
     "odpowiednich szkieł. Chyba nigdzie nie traktują tak fajnie klienta jak tutaj!"),
    ("ph-salon-cb", "Wnętrze salonu optycznego podczas obsługi klientów", "A", "Agata A.", "Stała klientka",
     "Za każdym razem jesteśmy bardzo zadowoleni z doboru oprawek jak i szkieł. Fachowa pomoc nie tylko przy zakupie, "
     "ale również podczas awarii."),
]
review_rows = []
for i, (img, alt, initial, name, role, text) in enumerate(REVIEWS):
    body = """          %s
          <p class="quote">&bdquo;%s&rdquo;</p>
          <div class="who">
            <span class="avatar">%s</span>
            <div><p class="name">%s</p><p class="role">%s</p></div>
          </div>""" % (STARS, text, initial, name, role)
    review_rows.append(alt_row(img, alt, body, eager=(i == 0)))

REVIEW_LD = """  <script type="application/ld+json">
  { "@context": "https://schema.org", "@type": "Optician", "@id": "https://www.binokl.com.pl/#organization",
    "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "3", "bestRating": "5", "worstRating": "1" },
    "review": [
      { "@type": "Review", "author": { "@type": "Person", "name": "Aleksandra K." }, "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }, "reviewBody": "Najlepszy optyk, do jakiego trafiłam. Pani idealnie dobrała oprawki, tłumacząc, na co dokładnie zwrócić uwagę przy danej wadzie." },
      { "@type": "Review", "author": { "@type": "Person", "name": "Bartek K." }, "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }, "reviewBody": "Świetny optyk, w którym nie tylko znajdziesz ciekawe oprawki, ale dowiesz się bardzo dużo na temat doboru odpowiednich szkieł." },
      { "@type": "Review", "author": { "@type": "Person", "name": "Agata A." }, "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }, "reviewBody": "Za każdym razem jesteśmy bardzo zadowoleni z doboru oprawek jak i szkieł. Fachowa pomoc nie tylko przy zakupie, ale również podczas awarii." }
    ] }
  </script>
"""

opinie = page_head(
    "Opinie", "Opinie",
    "Ocena 5,0 na 5 w Google. Poniżej trzy opinie, które klienci wystawili salonowi."
) + alt_section(review_rows) + cta_band(
    "Przekonaj się sam",
    "Umów badanie albo wpadnij obejrzeć oprawki — bez zobowiązań i bez pośpiechu.")

page("opinie.html", "Opinie klientów — Binokl, Salon Optyczny Piekary Śląskie",
     "Opinie klientów salonu optycznego Binokl w Piekarach Śląskich — ocena 5,0 na 5 w Google.",
     opinie, extra_ld=REVIEW_LD)


# ================================================================== KONTAKT
contact_body = """          <span class="eyebrow"><span class="line"></span>Dane kontaktowe</span>
          <h2>Wyszyńskiego 5a, Piekary Śląskie</h2>
          <div class="contact-cards" style="margin-top:1.5rem">
            <a class="contact-card" href="{maps}" target="_blank" rel="noopener noreferrer">
              <span class="ic">{pin}</span>
              <span><span class="t1">Adres</span><span class="t2">Wyszyńskiego 5a<br>41-940 Piekary Śląskie</span></span>
            </a>
            <a class="contact-card" href="tel:+48327674462">
              <span class="ic">{tel}</span>
              <span><span class="t1">Telefon</span><span class="t2">32 767 44 62</span></span>
            </a>
            <a class="contact-card full" href="mailto:optyk@binokl.com.pl">
              <span class="ic">{mail}</span>
              <span><span class="t1">E-mail</span><span class="t2">optyk@binokl.com.pl</span></span>
            </a>
          </div>
          <div class="hours-box">
            <div class="hd">{clock}<h3>Godziny otwarcia</h3></div>
            <dl>
              <div class="row"><dt>Poniedziałek – Piątek</dt><dd>10:00 – 17:00</dd></div>
              <div class="row"><dt>Sobota</dt><dd>10:00 – 13:00</dd></div>
              <div class="row"><dt>Niedziela</dt><dd class="closed">Zamknięte</dd></div>
            </dl>
          </div>""".format(maps=MAPS_Q, pin=PIN, tel=TEL, mail=MAIL, clock=CLOCK)

form_body = """          <span class="eyebrow"><span class="line"></span>Zapytanie</span>
          <h2>Napisz do nas</h2>
          <div class="form-box" style="margin-top:1.5rem">
            <h3>Szybki kontakt</h3>
            <p class="desc">Zostaw wiadomość — oddzwonimy i zaproponujemy dogodny termin.</p>
            <form id="contactForm" novalidate>
              <div class="form-row">
                <div class="field"><label for="name">Imię i nazwisko</label><input id="name" name="name" type="text" placeholder="Jan Kowalski" required /></div>
                <div class="field"><label for="phone">Telefon</label><input id="phone" name="phone" type="tel" placeholder="600 000 000" required /></div>
              </div>
              <div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" placeholder="jan@example.com" /></div>
              <div class="field"><label for="message">Wiadomość</label><textarea id="message" name="message" rows="4" placeholder="Chciałbym umówić się na badanie wzroku…"></textarea></div>
              <label class="consent" for="consent">
                <input id="consent" name="consent" type="checkbox" required />
                <span>Wyrażam zgodę na przetwarzanie moich danych osobowych w celu obsługi zapytania. Administrator: Binokl. Zakład optyczny. Mamys-Wróbel K. Szczegóły w <a href="polityka-prywatnosci.html">Polityce prywatności</a>.</span>
              </label>
              <button type="submit" class="btn btn-primary">Wyślij zapytanie {send}</button>
            </form>
          </div>""".format(send=SEND)

kontakt = page_head(
    "Kontakt", "Kontakt",
    "Umów się na badanie wzroku albo po prostu wpadnij obejrzeć nowe oprawki. Zadzwoń, napisz lub przyjdź w godzinach otwarcia."
) + alt_section([
    alt_row("ph-witryna", "Witryna i wejście do salonu optycznego", contact_body, eager=True),
    alt_row("ph-lada", "Lada w salonie optycznym Binokl", form_body),
]) + """
    <section class="map-section section--light" id="dojazd">
      <div class="wrap">
        <span class="eyebrow"><span class="line"></span>Jak do nas trafić</span>
        <h2 style="margin-top:0.9rem;font-size:clamp(1.8rem,3.2vw,2.7rem);font-weight:700;letter-spacing:-0.035em">Znajdziesz nas w centrum Piekar Śląskich</h2>
        <div class="map-frame tex-wood reveal" style="margin-top:2rem">
          <iframe title="Mapa — salon optyczny Binokl, Wyszyńskiego 5a, Piekary Śląskie"
            src="{embed}"
            loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
          <div class="map-card">
            <div class="map-card-inner">
              <div style="display:flex;align-items:center;gap:1rem">
                <span class="ic">{pin}</span>
                <div><p class="name">Salon Optyczny Binokl</p><p class="addr">Wyszyńskiego 5a, Piekary Śląskie</p></div>
              </div>
              <a class="btn btn-primary" href="{maps}" target="_blank" rel="noopener noreferrer">{route} Wyznacz trasę</a>
            </div>
          </div>
        </div>
      </div>
    </section>
""".format(embed=MAPS_EMBED, pin=PIN, maps=MAPS_Q, route=ROUTE)

page("kontakt.html", "Kontakt — Binokl, Salon Optyczny Piekary Śląskie",
     "Salon optyczny Binokl: Wyszyńskiego 5a, Piekary Śląskie. Telefon 32 767 44 62, godziny otwarcia, mapa i formularz kontaktowy.",
     kontakt)
