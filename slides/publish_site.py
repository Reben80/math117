"""Publish the lecture decks as a GitHub Pages site.

One shared lib folder, then a page for each section.
Run from the course folder: python3 slides/publish_site.py
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "slides"
DOCS = ROOT / "docs"
LIB_SOURCE = SLIDES / "1.1-key-terms" / "lib"

DECKS = [
    ("1.1-key-terms", "1.1", "Key terms", "Statistics, probability, and the six words in every study."),
    ("1.2-data-sampling", "1.2", "Data and sampling", "Words or numbers, and how the sample is chosen."),
    ("1.3-frequency", "1.3", "Frequency tables", "Nominal, ordinal, interval, ratio, and how often each value shows up."),
    ("1.4-experiments", "1.4", "Experiments and ethics", "An observational study, or a study that assigns the treatment."),
]


def rewrite(html):
    return (
        html.replace('href="lib/', 'href="../lib/')
        .replace("src=\"lib/", "src=\"../lib/")
        .replace("fonts_url = 'lib/fonts/'", "fonts_url = '../lib/fonts/'")
    )


def landing():
    cards = []
    for folder, number, name, blurb in DECKS:
        cards.append(
            f'<a class="card" href="{folder}/">'
            f'<p class="num">Section {number}</p>'
            f'<h2>{name}</h2>'
            f'<p>{blurb}</p>'
            f'</a>'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MATH 117 · Lecture decks</title>
<link rel="stylesheet" href="lib/fonts/montserrat/montserrat.css">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: #eef6f4;
    color: #1c242c;
    font-family: Montserrat, sans-serif;
  }}
  main {{
    max-width: 980px;
    margin: 0 auto;
    padding: 72px 28px 96px;
  }}
  .badge {{
    display: inline-block;
    background: #2a6f7a;
    color: #fff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.12em;
    padding: 6px 12px;
  }}
  .course {{
    margin: 0 0 0 12px;
    color: #5d6670;
    font-size: 18px;
  }}
  h1 {{
    margin: 22px 0 0;
    font-size: 56px;
    line-height: 0.98;
    letter-spacing: -0.04em;
    font-weight: 700;
  }}
  .lead {{
    margin: 18px 0 0;
    max-width: 640px;
    font-size: 20px;
    line-height: 1.4;
  }}
  .who {{
    margin: 28px 0 0;
    color: #5d6670;
    font-size: 16px;
  }}
  h3 {{
    margin: 56px 0 8px;
    color: #2a6f7a;
    font-size: 14px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }}
  .unit {{
    margin: 0;
    font-size: 28px;
    letter-spacing: -0.03em;
  }}
  .when {{
    margin: 6px 0 0;
    color: #5d6670;
  }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 22px;
  }}
  .card {{
    display: block;
    background: #fff;
    border: 1px solid #e4e1da;
    border-radius: 18px;
    padding: 22px 24px;
    text-decoration: none;
    color: inherit;
  }}
  .card:hover {{ border-color: #2a6f7a; }}
  .num {{
    margin: 0;
    color: #2a6f7a;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }}
  .card h2 {{
    margin: 8px 0 0;
    font-size: 26px;
    letter-spacing: -0.03em;
  }}
  .card p:last-child {{
    margin: 8px 0 0;
    color: #5d6670;
    font-size: 16px;
    line-height: 1.4;
  }}
  .next {{
    margin-top: 28px;
    color: #5d6670;
    font-size: 16px;
  }}
  @media (max-width: 720px) {{
    h1 {{ font-size: 40px; }}
    .grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<main>
  <p><span class="badge">MATH 117</span><span class="course">Elements of Statistics</span></p>
  <h1>Lecture decks</h1>
  <p class="lead">Open a section to follow along in class.</p>
  <p class="who">Prof. Rebin Muhammad · Montgomery College · Fall 2026, second half</p>
  <h3>Now</h3>
  <p class="unit">Unit 1 · Sampling and Data</p>
  <p class="when">October 28 – November 1 · OpenStax Introductory Statistics 2e, sections 1.1–1.4</p>
  <div class="grid">
    {"".join(cards)}
  </div>
  <p class="next">Unit 2, descriptive statistics, will be added here for November 2–6.</p>
</main>
</body>
</html>
"""


def main():
    if not LIB_SOURCE.is_dir():
        raise SystemExit(f"missing deck library: {LIB_SOURCE}")
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(LIB_SOURCE, DOCS / "lib", ignore=shutil.ignore_patterns(".DS_Store"))
    (DOCS / ".nojekyll").write_text("")
    (DOCS / "index.html").write_text(landing())
    for folder, _number, _name, _blurb in DECKS:
        source = SLIDES / folder
        if not (source / "index.html").is_file():
            raise SystemExit(f"missing deck: {source}")
        target = DOCS / folder
        target.mkdir()
        (target / "index.html").write_text(rewrite((source / "index.html").read_text()))
        for child in source.iterdir():
            if child.name in ("index.html", "lib") or child.name.startswith("."):
                continue
            dest = target / child.name
            if child.is_dir():
                shutil.copytree(child, dest, ignore=shutil.ignore_patterns(".DS_Store"))
            else:
                shutil.copy2(child, dest)
    print(f"site {DOCS}")
    print(f"decks {len(DECKS)}")


if __name__ == "__main__":
    main()
