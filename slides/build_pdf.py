"""Build slides/deck.html and slides/plausible-is-not-correct.pdf from slides/src/.

Each file in slides/src/ holds one 1920x1080 <section>; deck.json gives the order.
PDF export uses headless Google Chrome:  python slides/build_pdf.py
"""
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
deck = json.loads((SRC / "deck.json").read_text())

head = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{deck['title']}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
  @page {{ size: 1920px 1080px; margin: 0; }}
  html, body {{ margin: 0; padding: 0; background: #FFFFFF; }}
  section {{ position: relative; box-sizing: border-box; width: 1920px; height: 1080px;
             overflow: hidden; page-break-after: always; break-after: page; }}
  section h1, section h2, section h3, section p, section ul, section ol, section hr {{ margin: 0; }}
  section hr {{ border: 0; }}
  section table {{ border-collapse: collapse; width: 100%; }}
  section th, section td {{ padding: 0.35em 0.6em; border-bottom: 1px solid #D0D7DE; vertical-align: top; }}
  section th {{ border-bottom: 2px solid #1B1F24; }}
  aside {{ display: none; }}
</style></head><body>
"""
slides = [(SRC / f"{sid}.html").read_text() for sid in deck["order"]]
html = head + "\n".join(slides) + "\n</body></html>\n"
out_html = HERE / "deck.html"
out_html.write_text(html)
print("wrote", out_html, f"({len(slides)} slides)")

chrome = next((p for p in [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser"),
] if p and Path(p).exists()), None)
if chrome is None:
    raise SystemExit("Google Chrome/Chromium not found; open deck.html in a browser and print to PDF.")
pdf = HERE / "plausible-is-not-correct.pdf"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=10000", f"--print-to-pdf={pdf}", out_html.as_uri()], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("wrote", pdf)
