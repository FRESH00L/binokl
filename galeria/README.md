# Galeria zdjęć

Podstronę `galeria.html` zasilają dwa foldery i jeden plik z listą:

```
galeria/
  karuzela/     zdjęcia do karuzeli (pierwsza sekcja)
  galeria/      zdjęcia do siatki (druga sekcja)
  zdjecia.js    lista nazw plików — decyduje, co się wyświetla
```

## Jak dodać zdjęcie — dwa kroki

**1. Wrzuć plik do folderu**

- do karuzeli → `galeria/karuzela/`
- do siatki → `galeria/galeria/`

Obsługiwane formaty: `.jpg`, `.jpeg`, `.png`, `.webp`, `.avif`, `.gif`.

**2. Dopisz nazwę pliku do `zdjecia.js`**

Otwórz `galeria/zdjecia.js` w zwykłym notatniku i dopisz linijkę do
właściwej listy — nazwa w cudzysłowie, przecinek na końcu:

```js
  galeria: [
    "image7.jpeg",
    "image8.jpeg",
    "nowe-zdjecie.jpg",     ← dopisana linijka
  ],
```

Zapisz plik i wgraj oba (zdjęcie + `zdjecia.js`) na serwer. Gotowe.

## Jak usunąć zdjęcie

Skasuj jego linijkę z `zdjecia.js`. Sam plik możesz zostawić albo usunąć.

## O czym pamiętać

- **Nazwa musi się zgadzać co do znaku** — razem z rozszerzeniem i wielkością
  liter. `Foto1.JPG` to dla serwera co innego niż `foto1.jpg`. To najczęstsza
  przyczyna „zdjęcie się nie pokazuje”.
- **Kolejność linijek = kolejność zdjęć** na stronie. Chcesz przestawić —
  przestaw linijki.
- **Przecinek na końcu każdej linijki**, także ostatniej. Brak przecinka
  między pozycjami wyłączy całą galerię.
- **Nazwa pliku robi za opis zdjęcia** dla czytników ekranu i Google:
  `dobor-oprawek.jpg` czyta się jako „dobor oprawek”. Warto nazywać pliki
  opisowo zamiast zostawiać `IMG_2841.jpg`.
- **Rozmiar** — zdjęcia idą do przeglądarki takie, jakie są. Warto zmniejszyć
  je do ok. 2000 px szerokości, żeby strona się nie wlokła.

## Rozmiar plików

Zdjęcia idą do przeglądarki takie, jakie leżą w folderze. Prosto z telefonu
potrafią mieć 4–5 MB, a na stronie i tak wyświetlają się w kadrze poniżej
2000 px — warto je przed wrzuceniem zmniejszyć do ok. 2000 px dłuższego boku.

Zdjęcia wgrane do tej pory zostały już zmniejszone (31 MB → 7,4 MB).
Oryginały leżą w `galeria/_oryginaly/` — ten folder nie jest nigdzie
wyświetlany, można go trzymać jako kopię albo skasować.

## Puste listy

Jeśli lista `karuzela` zostanie pusta, karuzela pokaże zdjęcia z listy
`galeria` — sekcja nie zniknie. Jeśli obie listy są puste, na stronie
wyświetla się informacja „Galeria jest w przygotowaniu”.

## Dlaczego trzeba dopisywać nazwy

Strona jest statyczna, a przeglądarka nie potrafi sama zajrzeć do folderu
na serwerze i sprawdzić, co w nim leży. Automatyczne wykrywanie plików
wymagałoby PHP albo skryptu budującego — a te nie działają na GitHub Pages.
Lista w `zdjecia.js` to jedyne rozwiązanie, które zachowuje się identycznie
na GitHub Pages, na zwykłym hostingu i przy pliku otwartym z dysku.
