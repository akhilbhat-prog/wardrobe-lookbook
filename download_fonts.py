"""Download the viewer's Google Fonts for offline use.

Fetches the Google Fonts CSS, saves each referenced woff2 into static/fonts/, and writes
static/fonts/fonts.css with the URLs rewritten to local /static/fonts/ paths. Run once on a
machine with internet; the results get bundled so the packaged app needs no network.
"""
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "static", "fonts")

# Same families/weights the viewer CSS uses (static instances; optical-size axis dropped).
CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Bodoni+Moda:ital,wght@0,400;0,500;1,500"
    "&family=Archivo:wght@400;500;600&display=swap"
)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    os.makedirs(FONT_DIR, exist_ok=True)
    css = fetch(CSS_URL).decode("utf-8")
    urls = sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", css)))
    print(f"found {len(urls)} woff2 files")
    for u in urls:
        name = u.rsplit("/", 1)[-1]
        with open(os.path.join(FONT_DIR, name), "wb") as f:
            f.write(fetch(u))
        css = css.replace(u, f"/static/fonts/{name}")
    with open(os.path.join(FONT_DIR, "fonts.css"), "w", encoding="utf-8") as f:
        f.write(css)
    print(f"wrote {len(urls)} fonts + fonts.css to static/fonts/")


if __name__ == "__main__":
    main()
