"""Sestaví stránky ukázek ze zdrojů v _zdroje/ do <název>/index.html.

Zdroj je stránka bez hlavičky dokumentu (stejný soubor jde publikovat i jako Artifact v Claude). Sestavení doplní
doctype, popis a náhled odkazu pro sdílení, ikonky a místo Google Fonts vlastní písma z fonts/ (nic z cizích serverů).
Použití:  python _nastroje/sestav.py
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://matika.vojtakloud.com"
# název složky: (zdroj, popis pro vyhledávače a sdílení, obrázek náhledu)
PAGES = {
    "konformni-zobrazeni": ("konformni-zobrazeni.html",
                            "Nakresli do roviny křivky a vektory, zadej komplexní funkci a sleduj, jak se grid přenese. "
                            "Holomorfní funkce drží úhly, protipříklady ne.",
                            "media/nahled-konformni-zobrazeni.png"),
}


def build(slug, src, desc, image):
    s = open(os.path.join(ROOT, "_zdroje", src), encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    # Google Fonts pryč, místo nich vlastní písma
    s = re.sub(r'<link rel="preconnect"[^>]*>\n?', "", s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '<link rel="stylesheet" href="../fonts/fonts.css">', s)
    e = html.escape
    head = f"""<!doctype html>
<html lang="cs">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/{slug}/">
<meta property="og:image" content="{SITE}/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.ico" sizes="any">
<link rel="icon" href="../media/favicon-32.png" type="image/png">
<link rel="apple-touch-icon" href="../media/apple-touch-icon.png">
"""
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    out = os.path.join(ROOT, slug, "index.html")
    open(out, "w", encoding="utf-8", newline="\n").write(head + s.rstrip("\n") + "\n</html>\n")
    print(f"{slug}/index.html ({os.path.getsize(out) / 1000:.0f} kB)")


if __name__ == "__main__":
    for slug, (src, desc, image) in PAGES.items():
        build(slug, src, desc, image)
