# Matika na hraní

Interaktivní ukázky ke Škole matiky. Web: https://matika.vojtakloud.com. Autor Vojtěch Kloud.

- `index.html`: rozcestník. Nová ukázka = nový `<a class="item">` v seznamu (obrázek 1200 × 630 v `media/`).
- `<název>/index.html`: stránky ukázek, sestavené skriptem `python _nastroje/sestav.py` ze zdrojů v `_zdroje/`.
  Zdroj je stránka bez hlavičky dokumentu; sestavení doplní popis, náhled odkazu, ikonky a vlastní písma.
- `fonts/`: písma uložená u stránky (Raleway, Space Grotesk, IBM Plex Sans a Mono, STIX Two Text; SIL Open Font
  License). Písma graferů stáhne `python _nastroje/stahni_pisma.py`. Stránky nic nenačítají z cizích serverů,
  nemají cookies ani analytiku.
- `CNAME`: `matika.vojtakloud.com` (DNS u Webglobe: CNAME `matika` → `vojtaklojta.github.io.`).

Složky začínající podtržítkem GitHub Pages nezveřejňuje.
