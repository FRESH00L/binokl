# -*- coding: utf-8 -*-
"""Pobiera docelowe zdjęcia-placeholdery z Unsplash do assets/img/ i zapisuje listę źródeł.

Uruchamiać z katalogu głównego projektu:  python tools/fetch_placeholders.py
Po dostarczeniu zdjęć salonu wystarczy podmienić pliki ph-*.jpg (te same nazwy i proporcje).
"""
import os
import urllib.request
from PIL import Image

# nazwa docelowa -> (unsplash photo id, szerokość, docelowe proporcje w/h)
PHOTOS = {
    "ph-hero":            ("1717968368233-6c739dc4c4f4", 2000, 16 / 9),
    "ph-salon":           ("1659622056242-464f9e970009", 1400, 4 / 3),
    "ph-wnetrze":         ("1782834294716-8e28c18bdba6", 1400, 4 / 3),
    "ph-salon-cb":        ("1762529370626-010dd9eaedf9", 1400, 4 / 3),
    "ph-oprawki":         ("1615468822882-4828d2602857", 1400, 4 / 3),
    "ph-dobor":           ("1577410114274-ef015b5b6d29", 1400, 4 / 3),
    "ph-foropter":        ("1616163477138-508df4131a38", 1400, 4 / 3),
    "ph-oprawa-probna":   ("1539036776273-021ec1d78bec", 1400, 4 / 3),
    "ph-tablica":         ("1517948430535-1e2469d314fe", 1400, 4 / 3),
    "ph-korekcyjne":      ("1591076482161-42ce6da69f67", 1400, 4 / 3),
    "ph-przeciwsloneczne":("1577803645773-f96470509666", 1400, 4 / 3),
    "ph-soczewki":        ("1582143434535-eba55a806718", 1400, 4 / 3),
    "ph-klientka":        ("1604781099561-c70393a38a6d", 1400, 4 / 3),
    "ph-klient":          ("1621072156002-e2fccdc0b176", 1400, 4 / 3),
    "ph-witryna":         ("1716085486999-a95e807377d4", 1400, 4 / 3),
    "ph-lada":            ("1746723391801-1a24f7a57730", 1400, 4 / 3),
}

OUT = os.path.join("assets", "img")
TMP = os.path.join("tools", "tmp")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)


def crop_to(im, ratio):
    w, h = im.size
    if w / h > ratio:
        new_w = int(h * ratio)
        box = ((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h)
    else:
        new_h = int(w / ratio)
        box = (0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h)
    return im.crop(box)


rows = []
for name, (pid, width, ratio) in PHOTOS.items():
    url = "https://images.unsplash.com/photo-%s?w=%d&q=80" % (pid, width)
    raw = os.path.join(TMP, name + ".src")
    if not os.path.exists(raw):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(raw, "wb").write(urllib.request.urlopen(req, timeout=40).read())
    im = Image.open(raw).convert("RGB")
    im = crop_to(im, ratio)
    if im.width > width:
        im = im.resize((width, int(width / ratio)), Image.LANCZOS)
    dest = os.path.join(OUT, name + ".jpg")
    im.save(dest, quality=74, optimize=True, progressive=True)
    rows.append((name, im.width, im.height, os.path.getsize(dest) // 1024, pid))
    print("%-22s %4dx%-4d %4d kB" % (name, im.width, im.height, os.path.getsize(dest) // 1024))

with open(os.path.join("tools", "PLACEHOLDERS.md"), "w", encoding="utf-8") as f:
    f.write("# Zdjęcia-placeholdery (Unsplash)\n\n")
    f.write("Wszystkie pliki `assets/img/ph-*.jpg` to tymczasowe zdjęcia z Unsplash.\n")
    f.write("Podmiana: wgraj własne zdjęcie pod tą samą nazwą i w tych samych proporcjach.\n\n")
    f.write("| plik | rozmiar | waga | źródło |\n|---|---|---|---|\n")
    for name, w, h, kb, pid in rows:
        f.write("| `%s.jpg` | %dx%d | %d kB | https://unsplash.com/photos/%s |\n" % (name, w, h, kb, pid))
