# -*- coding: utf-8 -*-
"""Przełącznik wariantu kolorystycznego w css/styles.css.

Użycie (z katalogu głównego projektu):
    python tools/palette.py         — pokazuje, który wariant jest aktywny
    python tools/palette.py 4       — włącza wariant 4, resztę komentuje

Skrypt działa na blokach opisanych w arkuszu jako „WARIANT n —”: odkomentowuje
wybrany, komentuje pozostałe i przenosi dopisek „(aktywny)” w nagłówku.
Można też edytować plik ręcznie — skrypt jest tylko skrótem.
"""
import io
import re
import sys

CSS = 'css/styles.css'
END_MARK = '/* ---------- TOKENY POCHODNE'
HEAD_RE = re.compile(r'^\s+WARIANT (\d) — ')


def load():
    return io.open(CSS, encoding='utf-8').read().split('\n')


def blocks(lines):
    """Zwraca listę (numer, indeks_linii_nagłówka, indeks_pierwszej_linii_za_blokiem)."""
    heads = []
    for i, line in enumerate(lines):
        m = HEAD_RE.match(line)
        if m:
            heads.append((int(m.group(1)), i))
        if line.startswith(END_MARK):
            heads.append((None, i))
    out = []
    for (num, start), (_, nxt) in zip(heads, heads[1:]):
        if num is not None:
            out.append((num, start, nxt))
    return out


def normalize(lines, start, end):
    """Zdejmuje z bloku wszystkie znaczniki komentarza — także dopisane w tej samej
    linii co deklaracja (np. „/* :root {” albo „} */”). Opis wariantu zostaje."""
    kept = []
    for line in lines[start:end]:
        if line.strip() in ('/*', '*/'):
            continue
        if 'WARIANT' not in line and '-----' not in line and '=====' not in line:
            stripped = line.lstrip()
            if stripped.startswith('/*'):
                line = stripped[2:].lstrip()
            if line.rstrip().endswith('*/'):
                line = line.rstrip()[:-2].rstrip()
            if not line.strip() and stripped:
                continue
        kept.append(line)
    return kept


def comment(body):
    """Otacza deklarację :root znacznikami komentarza."""
    out = []
    opened = False
    for line in body:
        if not opened and line.strip().startswith(':root'):
            out.append('/*')
            opened = True
        out.append(line)
        if opened and line.strip() == '}':
            out.append('*/')
            opened = False
    return out


def main():
    lines = load()
    found = blocks(lines)
    if not found:
        raise SystemExit('nie znalazłem bloków WARIANT n — w ' + CSS)

    if len(sys.argv) < 2:
        for num, start, end in found:
            body = normalize(lines, start, end)
            state = 'aktywny' if any(l.strip().startswith(':root') for l in body) and \
                '/*' not in [l.strip() for l in lines[start:end]] else 'zakomentowany'
            print('wariant %d: %s' % (num, state))
        return

    want = int(sys.argv[1])
    if want not in [n for n, _, _ in found]:
        raise SystemExit('brak wariantu %d (dostępne: %s)' % (want, [n for n, _, _ in found]))

    out = lines[:found[0][1]]
    for num, start, end in found:
        body = normalize(lines, start, end)
        body = [re.sub(r'\s+\(aktywny\)', '', l) if HEAD_RE.match(l) else l for l in body]
        if num == want:
            body = [l.rstrip() + '   (aktywny)' if HEAD_RE.match(l) else l for l in body]
        else:
            body = comment(body)
        out.extend(body)
    out.extend(lines[found[-1][2]:])

    io.open(CSS, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    print('włączono wariant', want)


main()
