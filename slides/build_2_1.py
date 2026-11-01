"""Section 2.1 as a Slides.com HTML export.

Stem-and-leaf plots, a line graph, and a bar graph.
Open index.html, or upload the zip.
"""

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE = Path("/Users/mac-mini/Downloads/slides_deck-8187f8-2")
OUT = ROOT / "2.1-graphs"
ZIP_PATH = ROOT / "2.1-graphs-slides.zip"
SLUG = "math117-2-1-graphs"

_n = 0


def bid():
    global _n
    _n += 1
    return f"{_n:012x}"


def backdrop():
    return (
        f'<div class="sl-block" data-block-type="drawing" data-block-id="{bid()}" '
        f'style="width:1280px;height:720px;left:0px;top:0px;">'
        f'<div class="sl-block-content" style="z-index:1;">'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" '
        f'viewBox="0 0 1280 720" preserveAspectRatio="none">'
        f'<rect width="1280" height="720" fill="#eef6f4"></rect></svg></div></div>'
    )


def text_block(inner, left, top, width, height=None, align="left", z=10):
    h = "auto" if height is None else f"{height}px"
    return (
        f'<div class="sl-block" data-block-type="text" data-block-id="{bid()}" '
        f'style="width:{width}px;left:{left}px;top:{top}px;height:{h};">'
        f'<div class="sl-block-content" data-placeholder-tag="p" '
        f'style="z-index:{z};text-align:{align};height:100%;">{inner}</div></div>'
    )


def drawing(svg, left, top, width, height):
    return (
        f'<div class="sl-block" data-block-type="drawing" data-block-id="{bid()}" '
        f'style="width:{width}px;height:{height}px;left:{left}px;top:{top}px;">'
        f'<div class="sl-block-content" style="z-index:12;">{svg}</div></div>'
    )


def section(blocks, notes=""):
    note = f'<aside class="notes">{notes}</aside>' if notes else ""
    return f'<section data-id="{bid()}">{"".join(blocks)}{note}</section>'


def kicker(text):
    return (
        '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;'
        f'letter-spacing:0.14em;text-transform:uppercase;">{text}</p>'
    )


def title(text, size=40):
    return (
        f'<h2 style="margin:10px 0 0;color:#1c242c;font-size:{size}px;line-height:1.12;'
        f'font-weight:650;letter-spacing:-0.03em;">{text}</h2>'
    )


def card_shell(inner, height):
    return (
        f'<div style="background:#ffffff;border:1px solid #e4e1da;border-radius:18px;'
        f'padding:22px 24px;height:{height}px;box-sizing:border-box;">{inner}</div>'
    )


def letter_badge(letter, filled=False):
    face = "background:#2a6f7a;color:#ffffff;" if filled else "background:#e7f3f4;color:#2a6f7a;"
    return (
        f'<div style="width:36px;height:36px;border-radius:50%;{face}'
        f'font-weight:700;font-size:18px;display:flex;align-items:center;'
        f'justify-content:center;flex:none;">{letter}</div>'
    )


def choice(letter, text, filled=False):
    border = "#2a6f7a" if filled else "#e4e1da"
    weight = "650" if filled else "600"
    return (
        f'<div style="display:flex;align-items:center;gap:12px;width:100%;background:#ffffff;'
        f'border:1.5px solid {border};border-radius:14px;padding:8px 14px;box-sizing:border-box;">'
        f'{letter_badge(letter, filled)}'
        f'<div style="color:#1c242c;font-size:20px;font-weight:{weight};line-height:1.25;">{text}</div>'
        f'</div>'
    )


def choice_stack(pairs, filled_letter=None, reveal=False):
    rows = []
    for letter, text in pairs:
        if reveal and letter == filled_letter:
            row = (
                '<div style="position:relative;">'
                f'{choice(letter, text, False)}'
                f'<div class="fragment" data-fragment-index="0" '
                f'style="position:absolute;left:0;top:0;width:100%;">{choice(letter, text, True)}</div>'
                '</div>'
            )
        else:
            row = choice(letter, text, letter == filled_letter)
        rows.append(f'<div style="margin-top:8px;">{row}</div>')
    return "".join(rows)


def reveal_line(text):
    return (
        f'<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#2a6f7a;'
        f'font-size:16px;line-height:1.3;font-weight:650;">{text}</p>'
    )


def stem_svg(rows, heading, note, width=1152, height=460, compact=False):
    """rows: (stem, leaves as a string of digits, or 'gap')."""
    n = len(rows)
    top = 78 if not compact else 86
    bottom = height - (52 if note else 24)
    row_h = (bottom - top) / n
    leaf_size = 18 if not compact else 15
    stem_size = 20 if not compact else 16
    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="28" y="40" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        f'font-weight="700" letter-spacing="1.4">{heading}</text>',
    ]
    for i, (stem, leaves) in enumerate(rows):
        y = top + i * row_h + row_h * 0.72
        ink = "#5d6670" if leaves == "gap" else "#1c242c"
        parts.append(
            f'<text x="78" y="{y:.1f}" text-anchor="end" font-size="{stem_size}" fill="{ink}" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{stem}</text>'
        )
        if leaves == "gap":
            parts.append(
                f'<text x="108" y="{y:.1f}" font-size="15" fill="#5d6670" '
                f'font-family="Montserrat, sans-serif">no leaves</text>'
            )
            continue
        for j, digit in enumerate(leaves):
            parts.append(
                f'<text x="{108 + j * 22}" y="{y:.1f}" font-size="{leaf_size}" fill="#1c242c" '
                f'font-family="Montserrat, sans-serif">{digit}</text>'
            )
    parts.append(
        f'<line x1="92" y1="{top - 16}" x2="92" y2="{bottom - 6}" stroke="#2a6f7a" stroke-width="1.6"></line>'
    )
    if note:
        parts.append(
            f'<text x="28" y="{height - 18}" font-size="15" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{note}</text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" '
        f'viewBox="0 0 {width} {height}">' + "".join(parts) + "</svg>"
    )


EXAM_ROWS = [
    ("3", "3"),
    ("4", "299"),
    ("5", "355"),
    ("6", "1378899"),
    ("7", "2348"),
    ("8", "03888"),
    ("9", "0244446"),
    ("10", "0"),
]


def title_visual():
    svg = stem_svg(
        EXAM_ROWS,
        "FIRST EXAM",
        "Stem is the tens. Leaf is the ones.",
        width=460,
        height=500,
        compact=True,
    )
    return drawing(svg, 760, 110, 460, 500)


def line_graph():
    freqs = [2, 5, 8, 14, 7, 4]
    labels = ["0", "1", "2", "3", "4", "5"]
    left, gap, base, scale = 120, 160, 300, 200 / 14
    points = []
    for i, value in enumerate(freqs):
        x = left + i * gap
        y = base - value * scale
        points.append((x, y, value, labels[i]))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in points)
    parts = [
        '<rect x="0" y="0" width="1152" height="400" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<line x1="70" y1="{base}" x2="1040" y2="{base}" stroke="#1c242c" stroke-width="1.6"></line>',
        f'<polyline points="{poly}" fill="none" stroke="#2a6f7a" stroke-width="3"></polyline>',
    ]
    for x, y, value, label in points:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#2a6f7a"></circle>')
        parts.append(
            f'<text x="{x:.1f}" y="{y - 14:.1f}" text-anchor="middle" font-size="16" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{value}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{base + 28}" text-anchor="middle" font-size="16" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{label}</text>'
        )
    parts.append(
        '<text x="560" y="372" text-anchor="middle" font-size="15" fill="#5d6670" '
        'font-family="Montserrat, sans-serif">Times reminded per week</text>'
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 400">'
        + "".join(parts) + "</svg>"
    )
    return drawing(svg, 64, 145, 1152, 400)


def bar_graph():
    labels = ["10–19", "20–29", "30–39", "40–49", "50+"]
    values = [32.5, 29.5, 16.4, 13.9, 7.1]
    left, width, gap, base, scale = 110, 120, 70, 300, 210 / 32.5
    parts = [
        '<rect x="0" y="0" width="1152" height="400" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<line x1="70" y1="{base}" x2="1080" y2="{base}" stroke="#1c242c" stroke-width="1.6"></line>',
    ]
    for i, (label, value) in enumerate(zip(labels, values)):
        h = value * scale
        x = left + i * (width + gap)
        y = base - h
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{width}" height="{h:.1f}" rx="8" fill="#2a6f7a"></rect>'
        )
        parts.append(
            f'<text x="{x + width / 2:.1f}" y="{y - 12:.1f}" text-anchor="middle" font-size="18" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{value:g}%</text>'
        )
        parts.append(
            f'<text x="{x + width / 2:.1f}" y="{base + 30}" text-anchor="middle" font-size="18" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{label}</text>'
        )
    parts.append(
        '<text x="576" y="372" text-anchor="middle" font-size="15" fill="#5d6670" '
        'font-family="Montserrat, sans-serif">Age group</text>'
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 400">'
        + "".join(parts) + "</svg>"
    )
    return drawing(svg, 64, 145, 1152, 400)


def slides():
    out = []
    out.append(section([
        backdrop(),
        text_block(
            '<p style="margin:0;">'
            '<span style="color:#ffffff;background:#2a6f7a;padding:6px 12px;'
            'letter-spacing:0.12em;font-weight:700;font-size:16px;">MATH 117</span>'
            '<span style="color:#5d6670;font-size:20px;"> &nbsp; Unit 2 · Descriptive statistics</span></p>',
            72, 148, 680, 48,
        ),
        text_block(
            '<h1 style="margin:0;color:#1c242c;font-size:60px;line-height:0.98;font-weight:650;'
            'letter-spacing:-0.04em;">Stem-and-leaf<br>plots</h1>'
            '<p style="margin:22px 0 0;color:#1c242c;font-size:24px;line-height:1.3;">'
            'A small list, kept whole.<br>Then a line graph, and a bar graph.</p>'
            '<p style="margin:18px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;letter-spacing:0.08em;">SECTION 2.1</p>',
            72, 214, 660,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 540, 560,
        ),
        title_visual(),
    ], notes=(
        "Unit 2, first graphs. About 25 minutes, then section 2.2 if the hour is for graphs. "
        "A stemplot is for a small list. A histogram, next section, is the tool once the list gets long."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Section 2.1") + title("Three pictures"), 72, 48, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:22px;font-weight:650;">01</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Stem-and-leaf</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Every value stays on the page. Use it when the list is short.</p>',
            250,
        ), 72, 190, 360, 250),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:22px;font-weight:650;">02</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Line graph</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">A point for each value, connected. The height is how often it happened.</p>',
            250,
        ), 456, 190, 360, 250),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:22px;font-weight:650;">03</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Bar graph</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Separate bars, one per category. The bars do not touch.</p>',
            250,
        ), 840, 190, 360, 250),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">A graph shows where the data cluster, and where they thin out.</p>',
            72, 500, 1100,
        ),
    ], notes="Descriptive statistics is this chapter: display the data, then describe the center and the spread. Graph first, then calculate."))

    out.append(section([
        backdrop(),
        text_block(kicker("A stem-and-leaf plot") + title("Split the last digit"), 72, 40, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The number</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:40px;font-weight:650;">23</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;">Stem 2. Leaf 3.</p>',
            200,
        ), 72, 190, 360, 200),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The score</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:40px;font-weight:650;">94</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;">Stem 9. Leaf 4.</p>',
            200,
        ), 456, 190, 360, 200),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The decimal</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:40px;font-weight:650;">9.3</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;">Stem 9. Leaf 3.</p>',
            200,
        ), 840, 190, 360, 200),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">Write the stems down the page, smallest at the top. '
            'Write the leaves in increasing order beside their stem.</p>',
            72, 440, 1100,
        ),
    ], notes=(
        "432 has stem 43 and leaf 2. 5,432 has stem 543 and leaf 2. "
        "100 on the exam plot has stem 10 and leaf 0. You do not need those on the slide."
    )))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.1")
            + title("Thirty-one exam scores", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Professor Dean, spring pre-calculus, first exam. The list was already sorted.</p>',
            64, 18, 1150,
        ),
        drawing(stem_svg(EXAM_ROWS, "STEM  |  LEAF", "A leaf of 4 beside stem 9 is the score 94.", 1152, 500), 64, 130, 1152, 500),
    ], notes=(
        "Scores: 33, 42, 49, 49, 53, 55, 55, 61, 63, 67, 68, 68, 69, 69, 72, 73, 74, 78, "
        "80, 83, 88, 88, 88, 90, 92, 94, 94, 94, 94, 96, 100. Count them: 31. "
        "Optional if the class is fast, Try It 2.1, Park City basketball, 30 games: "
        "stem 3 leaves 22348, stem 4 leaves 022346778889, stem 5 leaves 00122234677, stem 6 leaves 01. "
        "The scores cluster in the 40s and 50s."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Example 2.1") + title("Where the scores sit", 44), 72, 48, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">THE CLUSTER</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:32px;font-weight:650;">60s through 90s</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Most of the class landed there. The 30s and 40s are thin.</p>',
            240,
        ), 72, 190, 540, 240),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">THE HIGH SCORES</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:32px;font-weight:650;">8 of 31</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Scores in the 90s or 100. That is about 26% of the class.</p>',
            240,
        ), 656, 190, 540, 240),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">The plot still shows every score. A bar graph would hide the 94s inside one bar.</p>',
            72, 490, 1100,
        ),
    ], notes="8/31 is about 0.258, which the book calls approximately 26%. The eight scores are 90, 92, 94, 94, 94, 94, 96, and 100."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.2")
            + title("One distance sits alone", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Kilometers from home to a supermarket. The leaf is the digit after the decimal.</p>',
            64, 16, 1150,
        ),
        drawing(
            stem_svg(
                [
                    ("1", "15"),
                    ("2", "357"),
                    ("3", "23358"),
                    ("4", "025578"),
                    ("5", "56"),
                    ("6", "57"),
                    ("7–11", "gap"),
                    ("12", "3"),
                ],
                "STEM  |  LEAF",
                "12.3 may be an outlier. The other values concentrate at 3 and 4 km.",
                1152,
                500,
            ),
            64, 125, 1152, 500,
        ),
    ], notes=(
        "Data: 1.1, 1.5, 2.3, 2.5, 2.7, 3.2, 3.3, 3.3, 3.5, 3.8, 4.0, 4.2, 4.5, 4.5, 4.7, 4.8, 5.5, 5.6, 6.5, 6.7, 12.3. "
        "Twenty-one values. The book prints empty stems from 7 through 11 so the gap shows. "
        "An outlier does not fit the pattern. It may be a recording mistake, such as 50 written for 500, or it may be real. "
        "Outliers return later in the chapter. Try It 2.2, miles to campus, has 8.0 as the value to discuss."
    )))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.4 · a line graph")
            + title("How often each answer came up", 36)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Forty parents. How many times a week must you remind a teenager to do chores?</p>',
            64, 16, 1150,
        ),
        line_graph(),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">The points are connected. The peak is 3 reminders, said by 14 of the 40 parents. The frequencies add to 40.</p>',
            64, 560, 1150,
        ),
    ], notes="Table 2.7. Frequencies 2, 5, 8, 14, 7, 4 for 0 through 5 reminders. Try It 2.4 is car repairs in a year: frequencies 7, 10, 14, 9 for 0 through 3 visits. Same kind of graph."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.5 · a bar graph")
            + title("The bars stay apart", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Percent of U.S. TikTok users in each age group.</p>',
            64, 16, 1150,
        ),
        bar_graph(),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">Ages 10–19 are the largest share, 32.5%. A gap between bars means these are categories, not one measured scale.</p>',
            64, 560, 1150,
        ),
    ], notes=(
        "Table 2.9: 10–19 is 32.5%, 20–29 is 29.5%, 30–39 is 16.4%, 40–49 is 13.9%, 50+ is 7.1%. "
        "The percents add to 99.4 because of rounding. "
        "Try It 2.5, Park City: children 19%, working-age adults 43%, retirees 38%. "
        "Example 2.6, high school graduates in 2030: Northeast 16.1%, Midwest 21.6%, South 39.0%, West 23.3%. "
        "A histogram, section 2.2, is the graph whose bars touch."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Which picture") + title("Match the graph to the job"), 72, 36, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.1em;">KEEP EVERY VALUE</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;font-weight:650;">Stem-and-leaf</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">The 31 exam scores. You can still read 94.</p>',
            220,
        ), 72, 180, 360, 220),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.1em;">CONNECT THE COUNTS</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;font-weight:650;">Line graph</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">Reminders per week. The height is the frequency.</p>',
            220,
        ), 456, 180, 360, 220),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.1em;">SEPARATE THE CATEGORIES</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;font-weight:650;">Bar graph</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">Age groups. Leave a gap between the bars.</p>',
            220,
        ), 840, 180, 360, 220),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">Look for the cluster, and for any value that sits alone.</p>',
            72, 460, 1100,
        ),
    ], notes="Side-by-side stemplots, Example 2.3, compare presidential age at inauguration and at death. Leave that off unless a student asks. It is a comparison, not a new kind of graph."))

    stem_q = [("A", "9"), ("B", "4"), ("C", "94")]
    outlier_q = [("A", "A typical distance"), ("B", "An outlier"), ("C", "The stem")]
    picture_q = [("A", "The bars touch"), ("B", "The bars are separate"), ("C", "The points are connected")]

    def question_block(number, prompt, pairs, answer, why):
        return (
            f'<p style="margin:0 0 4px;min-height:56px;color:#1c242c;font-size:22px;font-weight:650;line-height:1.25;">{number} &nbsp; {prompt}</p>'
            f'{choice_stack(pairs, answer, reveal=True)}'
            f'{reveal_line(why)}'
        )

    out.append(section([
        backdrop(),
        text_block(kicker("Quick check") + title("Name it", 40), 64, 20, 800),
        text_block(question_block(
            "1", "The stem of 94 is", stem_q, "A", "The leaf is the last digit.",
        ), 64, 130, 370),
        text_block(question_block(
            "2", "12.3 km is", outlier_q, "B", "The others cluster at 3 and 4 km.",
        ), 454, 130, 370),
        text_block(question_block(
            "3", "The TikTok graph is a bar graph because", picture_q, "B", "A line graph connects the points.",
        ), 844, 130, 370),
    ], notes="One right-arrow shows every answer: 1A, 2B, 3B. Arrow again leaves the slide. Homework 74 and 75."))

    out.append(section([
        backdrop(),
        text_block(kicker("Before section 2.2") + title("You can read a small plot", 48), 72, 70, 1100),
        text_block(
            '<p style="margin:0 0 14px;color:#1c242c;font-size:26px;line-height:1.35;">Split a number into a stem and a leaf.</p>'
            '<p style="margin:0 0 14px;color:#1c242c;font-size:26px;line-height:1.35;">See the cluster, and a value that sits alone.</p>'
            '<p style="margin:0;color:#1c242c;font-size:26px;line-height:1.35;">Tell a line graph from a bar graph.</p>',
            72, 230, 1000,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">NEXT</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:28px;font-weight:650;">2.2 &nbsp; Histograms</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">Bars that touch, for a long list of measurements.</p>',
            130,
        ), 72, 430, 980, 130),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Practice: OpenStax homework 74 and 75.</p>',
            72, 590, 800,
        ),
    ], notes=(
        "Homework 74 is ten chemistry scores: 77, 78, 76, 81, 86, 51, 79, 82, 84, 99. "
        "Stem 5 leaf 1, stem 7 leaves 6789, stem 8 leaves 1246, stem 9 leaf 9. "
        "51 and 99 are the scores a student might call outliers. "
        "Item 75 is a stemplot of the percent never married, by state."
    )))

    return out


SHELL = """<!DOCTYPE html>
<html class="sl-root decks export offline loaded">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover, minimal-ui">
<meta charset="utf-8">
<title>MATH 117 · 2.1 Stem-and-leaf plots</title>
<link rel="stylesheet" type="text/css" href="lib/offline-v2.css">
</head>
<body class="reveal-viewport theme-font-montserrat theme-color-white-blue">
<div class="reveal"><div class="slides">
{slides}
</div></div>
<script>
var SLConfig = {{"deck": {{"slug": "math117-2-1-graphs", "title": "MATH 117 · 2.1 Stem-and-leaf plots", "description": "Stem-and-leaf plots, line graphs, and bar graphs.", "width": 1280, "height": 720, "margin": 0.05, "theme_font": "montserrat", "theme_color": "white-blue", "center": false, "transition": "slide", "background_transition": "slide", "slide_count": {count}, "version": 2, "rtl": false, "should_loop": false, "shuffle": false, "navigation_mode": "default", "language": "en", "font_typekit": null, "font_google": null, "notes": {{}}}}}};
SLConfig.fonts_url = 'lib/fonts/';
</script>
<script src="lib/reveal.js"></script>
<script src="lib/reveal-plugins.js"></script>
<script src="lib/offline.js"></script>
<script>
Reveal.initialize({{
width: 1280, height: 720, margin: 0.05, hash: true, controls: true, progress: true,
mouseWheel: false, showNotes: false, slideNumber: false, fragmentInURL: true,
autoSlide: 0, autoSlideStoppable: true, autoAnimateMatcher: SL.deck.AutoAnimate.matcher,
center: false, shuffle: false, loop: false, rtl: false, navigationMode: "default",
transition: "slide", backgroundTransition: "slide",
plugins: [ RevealZoom, RevealNotes, RevealMarkdown, RevealHighlight ]
}});
</script>
</body></html>
"""


def main():
    if not SAMPLE.is_dir():
        raise SystemExit(f"missing sample export: {SAMPLE}")
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SAMPLE / "lib", OUT / "lib", ignore=shutil.ignore_patterns(".DS_Store"))
    parts = slides()
    html = SHELL.format(slides="\n".join(parts), count=len(parts))
    if "2696400" in html:
        raise SystemExit("deck still contains a Slides.com user id")
    asset = OUT / SLUG
    asset.mkdir()
    (asset / "mark.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 8">'
        '<circle cx="4" cy="4" r="3" fill="#2a6f7a"></circle></svg>\n'
    )
    html = html.replace(
        "</section>",
        f'<img alt="" data-src="{SLUG}/mark.svg" '
        f'style="width:1px;height:1px;position:absolute;left:0;top:0;opacity:0;"></section>',
        1,
    )
    (OUT / "index.html").write_text(html)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        dirs = sorted({p.parent.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file()})
        for folder in dirs:
            if folder not in ("", "."):
                zf.writestr(zipfile.ZipInfo(folder + "/"), "")
        for path in sorted(OUT.rglob("*")):
            if path.name == ".DS_Store" or not path.is_file():
                continue
            zf.write(path, path.relative_to(OUT).as_posix())
    print(f"slides {len(parts)}")
    print(f"zip {ZIP_PATH}")


if __name__ == "__main__":
    main()
