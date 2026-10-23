"""Stáhne písma graferů z balíčků Fontsource (jsDelivr) do fonts/ a vytvoří fonts/fonts.css.

Stránky tak nenačítají nic z Google Fonts ani jiných cizích serverů. Spustit jednou, nebo když přibude řez.
Použití:  python _nastroje/stahni_pisma.py
"""
import os, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "fonts")
CDN = "https://cdn.jsdelivr.net/npm/@fontsource/{pkg}@5/"
# (balíček, rodina v CSS, váhy, styl)
FACES = [
    ("ibm-plex-sans", "IBM Plex Sans", [400, 500, 600], "normal"),
    ("ibm-plex-mono", "IBM Plex Mono", [400, 500], "normal"),
    ("stix-two-text", "STIX Two Text", [400, 500], "normal"),
    ("stix-two-text", "STIX Two Text", [400, 500], "italic"),
]
SUBSETS = ("latin-ext", "latin")


def get(url):
    with urllib.request.urlopen(url) as r:
        return r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    rules = []
    for pkg, family, weights, style in FACES:
        for w in weights:
            css = get(CDN.format(pkg=pkg) + (f"{w}.css" if style == "normal" else f"{w}-italic.css")).decode()
            for block in re.findall(r"@font-face\s*{[^}]*}", css):
                m = re.search(r"url\(\./files/([^)]+?-(latin-ext|latin)-\d+-\w+\.woff2)\)", block)
                if not m or m.group(2) not in SUBSETS:
                    continue
                name = m.group(1)
                rng = re.search(r"unicode-range:\s*([^;]+);", block).group(1).strip()
                path = os.path.join(OUT, name)
                if not os.path.exists(path):
                    data = get(CDN.format(pkg=pkg) + "files/" + name)
                    if data[:4] != b"wOF2":
                        raise SystemExit(f"{name} není woff2")
                    open(path, "wb").write(data)
                rules.append(f"@font-face {{ font-family: \"{family}\"; font-style: {style}; font-weight: {w}; "
                             f"font-display: swap; src: url(\"{name}\") format(\"woff2\"); unicode-range: {rng}; }}")
    head = "/* Písma graferů (IBM Plex Sans a Mono, STIX Two Text; licence SIL Open Font License), z balíčků Fontsource. */\n"
    open(os.path.join(OUT, "fonts.css"), "w", encoding="utf-8", newline="\n").write(head + "\n".join(rules) + "\n")
    print(f"fonts.css: {len(rules)} pravidel")


if __name__ == "__main__":
    main()
