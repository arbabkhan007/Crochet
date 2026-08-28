"""Render a pattern .md to a client-ready PDF.

Usage: build_pdf.py SOURCE.md OUTPUT.pdf "Short title"

Pure-Python path: markdown -> HTML -> fpdf2. No system libraries required
(WeasyPrint cannot run here: libpango/libcairo are unavailable and the Debian
mirrors are unreachable, so apt cannot install them).
"""
import sys, re, pathlib, markdown
from fpdf import FPDF

FONTDIR = "/usr/share/fonts/truetype/dejavu/"

CSS = """
<style>
h1 { color: #7a5230; font-size: 20pt; }
h2 { color: #7a5230; font-size: 11pt; }
h3 { color: #333333; font-size: 10pt; }
p, li { font-size: 9pt; color: #1a1a1a; }
th { background-color: #7a5230; color: #ffffff; font-size: 8pt; }
td { border: 0.4px solid #d8d2c8; font-size: 8.5pt; }
blockquote { color: #444444; font-size: 8.5pt; }
code { font-family: DejaVuMono; font-size: 8pt; }
</style>
"""


INLINE_IN_CELL = re.compile(r'</?(?:strong|em|code|b|i)\b[^>]*>', re.I)


def strip_inline_in_cells(html):
    """fpdf2's HTML parser rejects nested tags inside <td>/<th>. Table cells in
    these patterns carry no meaning in their bolding, so flatten it and keep the
    text. Inline markup elsewhere is untouched."""
    def cell(m):
        return m.group(1) + INLINE_IN_CELL.sub("", m.group(2)) + m.group(3)
    return re.compile(r'(<t[dh]\b[^>]*>)(.*?)(</t[dh]>)', re.S | re.I).sub(cell, html)


class PatternPDF(FPDF):
    def __init__(self, short_title):
        super().__init__(format="A4")
        self.short_title = short_title

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(140, 130, 118)
        self.cell(0, 6, f"Novality Store  \u00b7  {self.short_title}",
                  align="L")
        self.cell(0, 6, f"Page {self.page_no()}", align="R", new_x="LMARGIN",
                  new_y="NEXT")
        self.set_draw_color(216, 210, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-14)
        self.set_font("DejaVu", "", 7)
        self.set_text_color(150, 140, 128)
        self.cell(0, 6,
                  "\u00a9 Novality Store \u00b7 Creation Studio  \u2014  "
                  "personal use and small-batch finished sales",
                  align="C")


def build(src, out, short_title):
    md_text = pathlib.Path(src).read_text()
    body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])

    pdf = PatternPDF(short_title)
    pdf.set_margin(16)
    pdf.set_title(short_title)
    pdf.set_author("Novality Store \u00b7 Creation Studio")
    pdf.set_creator("Novality Store")
    pdf.set_subject("Crochet pattern")

    # This box has no oblique DejaVu, so italic maps back to roman.
    pdf.add_font("DejaVu", "",   FONTDIR + "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B",  FONTDIR + "DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I",  FONTDIR + "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "BI", FONTDIR + "DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVuMono", "",  FONTDIR + "DejaVuSansMono.ttf")
    pdf.add_font("DejaVuMono", "B", FONTDIR + "DejaVuSansMono-Bold.ttf")

    pdf.set_font("DejaVu", "", 9)
    pdf.add_page()
    pdf.write_html(CSS + strip_inline_in_cells(body))

    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(out)
    return pdf.pages_count


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("usage: build_pdf.py SOURCE.md OUTPUT.pdf \"Short title\"")
    pages = build(sys.argv[1], sys.argv[2], sys.argv[3])
    size = pathlib.Path(sys.argv[2]).stat().st_size
    print(f"wrote {sys.argv[2]}  ({size:,} bytes, {pages} pages)")
