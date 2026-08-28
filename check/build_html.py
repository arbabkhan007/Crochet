"""Render the client pattern to a standalone, print-ready HTML file."""
import pathlib, markdown, re

import sys
if len(sys.argv) != 4:
    sys.exit("usage: build_html.py SOURCE.md OUTPUT.html \"Title\"")
SRC, OUT, TITLE = sys.argv[1], sys.argv[2], sys.argv[3]

md_text = pathlib.Path(SRC).read_text()
body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])

CSS = """
:root { --ink:#1a1a1a; --rule:#d8d2c8; --accent:#7a5230; }
* { box-sizing: border-box; }
body { font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
       color: var(--ink); line-height: 1.62; max-width: 46rem;
       margin: 0 auto; padding: 3rem 1.5rem 5rem; font-size: 17px;
       -webkit-font-smoothing: antialiased; }
h1 { font-size: 2.1rem; line-height: 1.15; margin: 0 0 .3rem; letter-spacing:-.01em; }
h1 + p, h1:first-of-type { }
h2 { font-size: 1.05rem; text-transform: uppercase; letter-spacing: .12em;
     color: var(--accent); margin: 2.6rem 0 .9rem; padding-bottom: .45rem;
     border-bottom: 1px solid var(--rule); }
h3 { font-size: 1.12rem; margin: 1.9rem 0 .6rem; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 2.4rem 0; }
p { margin: 0 0 1rem; }
strong { font-weight: 700; }
ul { padding-left: 1.3rem; margin: 0 0 1rem; }
li { margin-bottom: .3rem; }
table { border-collapse: collapse; width: 100%; margin: 1.2rem 0 1.6rem;
        font-size: .95rem; }
th, td { text-align: left; padding: .5rem .7rem; border-bottom: 1px solid var(--rule);
         vertical-align: top; }
th { font-size: .78rem; text-transform: uppercase; letter-spacing: .08em;
     color: var(--accent); border-bottom: 1.5px solid var(--accent); }
tbody tr:nth-child(even) { background: #faf7f2; }
blockquote { margin: 1.3rem 0; padding: .9rem 1.2rem; background: #faf7f2;
             border-left: 3px solid var(--accent); font-size: .96rem; }
blockquote p:last-child { margin-bottom: 0; }
code { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .9em; }
@media print {
  body { max-width: none; padding: 0; font-size: 11.5pt; }
  h2 { break-after: avoid; } h3 { break-after: avoid; }
  table, blockquote { break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
  @page { margin: 18mm 16mm; }
}
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE} — Novality Store</title>
<meta name="description" content="Crochet pattern: {TITLE}.">
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
out = pathlib.Path(OUT); out.parent.mkdir(exist_ok=True)
out.write_text(html)
print(f"wrote {out}  ({len(html)} bytes)")
# sanity: no raw markdown left behind
leftovers = re.findall(r'^\s*(\|.*\||#{1,3} |\*\*.+?\*\*$)', html, re.M)
print("raw markdown artifacts in output:", len(leftovers))
