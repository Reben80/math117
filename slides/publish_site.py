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

# unit, folder, section number, name, blurb
DECKS = [
    ("1", "1.1-key-terms", "1.1", "Key terms", "Statistics, probability, and the six words in every study."),
    ("1", "1.2-data-sampling", "1.2", "Data and sampling", "Words or numbers, and how the sample is chosen."),
    ("1", "1.3-frequency", "1.3", "Frequency tables", "Nominal, ordinal, interval, ratio, and how often each value shows up."),
    ("1", "1.4-experiments", "1.4", "Experiments and ethics", "An observational study, or a study that assigns the treatment."),
    ("2", "2.1-graphs", "2.1", "Stem-and-leaf plots", "A small list, kept whole. Then a line graph and a bar graph."),
    ("2", "2.2-histograms", "2.2", "Histograms", "Bars that touch, for a long list of measurements."),
    ("2", "2.3-location", "2.3", "Quartiles", "Percentiles, quartiles, and the IQR."),
    ("2", "2.4-boxplots", "2.4", "Box plots", "The five-number summary as a picture."),
    ("2", "2.5-center", "2.5", "Center", "Mean, median, and mode."),
    ("2", "2.6-skewness", "2.6", "Skewness", "How the mean rides the tail."),
    ("2", "2.7-spread", "2.7", "Standard deviation", "How far the values sit from the mean."),
    ("3", "12.1-lines", "12.1", "Linear equations", "The line y = a + bx, before any data."),
    ("3", "12.2-scatter", "12.2", "Scatter plots", "One point for each pair, and the direction it shows."),
    ("3", "12.3-regression", "12.3", "The regression line", "The least-squares line, r, and r squared."),
    ("3", "12.5-prediction", "12.5", "Prediction", "Use the line inside the data. Stop outside it."),
]

# Dates and sections follow the Fall 2026 second-half calendar.
# Homework, the unit test, and the discussion are due on the last day of each unit.
WEEKS = [
    ("October 28 – November 1", "Unit 1 · Sampling and Data", "OpenStax Introductory Statistics 2e, sections 1.1–1.4", "Homework, test, and discussion due November 1", "1"),
    ("November 2 – 6", "Unit 2 · Descriptive Statistics", "OpenStax Introductory Statistics 2e, sections 2.1–2.7", "Homework, test, and discussion due November 6", "2"),
    ("November 7 – 9", "Unit 3 · Linear Regression and Correlation", "OpenStax Introductory Statistics 2e, sections 12.1–12.3 and 12.5", "Homework, test, and discussion due November 9", "3"),
    ("November 10 – 11", "Exam 1", "Units 1, 2, and 3", "", ""),
    ("November 12 – 16", "Unit 4 · Normal Distribution, CLT", "OpenStax Introductory Statistics 2e, sections 6.1, 6.2, and 7.1", "Homework, test, and discussion due November 16", ""),
    ("November 17 – 19", "Unit 5 · Confidence Intervals", "OpenStax Introductory Statistics 2e, sections 8.1–8.3", "Homework, test, and discussion due November 19", ""),
    ("November 20 – 21", "Unit S1 · Bootstrap Confidence Intervals", "Introduction to Modern Statistics, chapter 12", "Homework, test, and discussion due November 21", ""),
    ("November 22 – 23", "Exam 2", "Units 4 and 5. Unit S1 is not on this exam.", "", ""),
    ("November 24 – 28", "Unit 6 · Hypothesis Testing, introduction", "OpenStax Introductory Statistics 2e, sections 9.1–9.4", "Homework, test, and discussion due November 28", ""),
    ("November 29 – December 1", "Unit 7 · Hypothesis testing for proportions", "OpenStax Introductory Statistics 2e, sections 9.5 and 10.3", "Homework, test, and discussion due December 1", ""),
    ("December 2 – 5", "Unit 8 · Hypothesis testing for means", "OpenStax Introductory Statistics 2e, sections 9.5, 10.1, and 10.4", "Homework, test, and discussion due December 5", ""),
]


def rewrite(html):
    return (
        html.replace('href="lib/', 'href="../lib/')
        .replace("src=\"lib/", "src=\"../lib/")
        .replace("fonts_url = 'lib/fonts/'", "fonts_url = '../lib/fonts/'")
    )


def landing():
    cards_by_unit = {}
    for unit, folder, number, name, blurb in DECKS:
        cards_by_unit.setdefault(unit, []).append(
            f'<a class="card" href="{folder}/">'
            f'<p class="num">Section {number}</p>'
            f'<h2>{name}</h2>'
            f'<p>{blurb}</p>'
            f'</a>'
        )
    weeks = []
    for dates, title, source, due, unit in WEEKS:
        exam = title.startswith("Exam")
        klass = "week exam" if exam else "week"
        due_html = f'<p class="due">{due}</p>' if due else ""
        cards = cards_by_unit.get(unit, [])
        decks_html = f'<div class="grid">{"".join(cards)}</div>' if cards else ""
        weeks.append(
            f'<li class="{klass}">'
            f'<p class="dates">{dates}</p>'
            f'<div>'
            f'<h2>{title}</h2>'
            f'<p class="src">{source}</p>'
            f'{due_html}'
            f'{decks_html}'
            f'</div>'
            f'</li>'
        )
    schedule = "".join(weeks)
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
  .note {{
    margin: 8px 0 0;
    color: #5d6670;
    font-size: 16px;
  }}
  .cal {{
    list-style: none;
    margin: 18px 0 0;
    padding: 0;
  }}
  .week {{
    display: grid;
    grid-template-columns: 210px 1fr;
    gap: 8px 28px;
    background: #fff;
    border: 1px solid #e4e1da;
    border-radius: 18px;
    padding: 22px 24px;
    margin-top: 12px;
  }}
  .week.exam {{
    background: #e7f3f4;
  }}
  .dates {{
    margin: 4px 0 0;
    color: #2a6f7a;
    font-size: 15px;
    font-weight: 700;
  }}
  .week h2 {{
    margin: 0;
    font-size: 22px;
    letter-spacing: -0.03em;
  }}
  .src, .due {{
    margin: 6px 0 0;
    color: #5d6670;
    font-size: 15px;
    line-height: 1.45;
  }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 18px;
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
  footer {{
    margin-top: 64px;
    padding-top: 8px;
    border-top: 1px solid #d5e0de;
  }}
  footer h3 {{
    margin-top: 28px;
  }}
  footer p {{
    margin: 0;
    max-width: 720px;
    color: #5d6670;
    font-size: 16px;
    line-height: 1.55;
  }}
  footer p + p {{
    margin-top: 12px;
  }}
  footer a {{
    color: #2a6f7a;
  }}
  @media (max-width: 720px) {{
    h1 {{ font-size: 40px; }}
    .week, .grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<main>
  <p><span class="badge">MATH 117</span><span class="course">Elements of Statistics</span></p>
  <h1>Lecture decks</h1>
  <p class="lead">Follow the calendar below. Open a section to follow along in class.</p>
  <p class="who">Prof. Rebin Muhammad · Montgomery College · Fall 2026, second half · CRN 22470</p>
  <p class="note">October 28 – December 20. Subject to changes announced on Blackboard.</p>
  <h3>Calendar</h3>
  <p class="note">A unit shows its sections once the decks are ready.</p>
  <ol class="cal">
    {schedule}
  </ol>
  <footer>
    <h3>The book</h3>
    <p>These decks follow <a href="https://openstax.org/details/books/introductory-statistics-2e">Introductory Statistics 2e</a>. Unit S1 follows <a href="https://openintrostat.github.io/ims/">Introduction to Modern Statistics</a>.</p>
    <h3>Calculators</h3>
    <p><a href="https://www.desmos.com/calculator">Desmos</a></p>
    <p><a href="https://lock5stat.com/StatKey/">StatKey</a></p>
  </footer>
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
    for _unit, folder, _number, _name, _blurb in DECKS:
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
