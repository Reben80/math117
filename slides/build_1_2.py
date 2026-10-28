"""Section 1.2 as a Slides.com HTML export.

Qualitative and quantitative data, then how a sample is chosen.
Open index.html, or upload the zip.
"""

import math
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE = Path("/Users/mac-mini/Downloads/slides_deck-8187f8-2")
OUT = ROOT / "1.2-data-sampling"
ZIP_PATH = ROOT / "1.2-data-sampling-slides.zip"
SLUG = "math117-1-2-data-sampling"

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


def num_card(num, heading, body, height=250):
    inner = (
        f'<p style="margin:0;color:#2a6f7a;font-size:22px;font-weight:650;'
        f'letter-spacing:-0.03em;line-height:1;">{num}</p>'
        f'<p style="margin:14px 0 0;color:#1c242c;font-size:26px;line-height:1.15;'
        f'font-weight:650;">{heading}</p>'
        f'<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">{body}</p>'
    )
    return card_shell(inner, height)


def label_card(label, heading, body, height=200):
    inner = (
        f'<p style="margin:0;color:#2a6f7a;font-size:13px;font-weight:700;'
        f'letter-spacing:0.12em;">{label}</p>'
        f'<p style="margin:12px 0 0;color:#1c242c;font-size:28px;line-height:1.1;'
        f'font-weight:650;">{heading}</p>'
        f'<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">{body}</p>'
    )
    return card_shell(inner, height)


def data_table(headers, rows):
    ths = "".join(
        '<th style="text-align:left;background:#2a6f7a;color:#ffffff;font-size:15px;'
        f'font-weight:650;letter-spacing:0.04em;padding:12px 16px;">{header}</th>'
        for header in headers
    )
    body = []
    for index, row in enumerate(rows):
        bg = "#ffffff" if index % 2 == 0 else "#f3f8f7"
        cells = []
        for value in row:
            cells.append(
                f'<td style="padding:11px 16px;border-bottom:1px solid #e4e1da;font-size:20px;'
                f'color:#1c242c;font-weight:500;background:{bg};">{value}</td>'
            )
        body.append(f'<tr>{"".join(cells)}</tr>')
    return (
        '<div style="border:1px solid #d5ddd9;border-radius:14px;overflow:hidden;">'
        '<table style="width:100%;border-collapse:collapse;">'
        f'<thead><tr>{ths}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
    )


def letter_badge(letter, filled=False):
    if filled:
        face = "background:#2a6f7a;color:#ffffff;"
    else:
        face = "background:#e7f3f4;color:#2a6f7a;"
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


def title_visual():
    pie = wedges(230, 200, 118, [(59.1, "#2a6f7a"), (40.9, "#d7ebe8")], labels=False)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 460 500">
      <rect x="8" y="8" width="444" height="484" rx="22" fill="#ffffff" stroke="#e4e1da" stroke-width="1.6"></rect>
      <text x="36" y="48" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="700" letter-spacing="1.6">ONE COLLEGE</text>
      {pie}
      <circle cx="70" cy="372" r="9" fill="#2a6f7a"></circle>
      <text x="92" y="378" font-size="18" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">Part-time, 59%</text>
      <circle cx="70" cy="412" r="9" fill="#d7ebe8" stroke="#2a6f7a" stroke-width="1.5"></circle>
      <text x="92" y="418" font-size="18" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">Full-time, 41%</text>
      <text x="70" y="460" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">De Anza, one spring</text>
    </svg>'''
    return drawing(svg, 760, 110, 460, 500)


def pareto_chart():
    rows = [
        ("Asian", 36.1, False),
        ("White", 24.5, False),
        ("Hispanic/Latino", 17.1, False),
        ("Other/Unknown", 9.6, True),
        ("Black", 5.8, False),
        ("Filipino", 5.3, False),
        ("Pacific Islander", 1.0, False),
        ("Native American", 0.6, False),
    ]
    parts = [
        '<rect x="0" y="0" width="1152" height="430" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>'
    ]
    for i, (name, pct, missing) in enumerate(rows):
        y = 16 + i * 51
        width = pct / 36.1 * 620
        color = "#1c242c" if missing else "#2a6f7a"
        parts.append(
            f'<text x="20" y="{y + 30}" font-size="16" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{name}</text>'
        )
        parts.append(
            f'<rect x="230" y="{y + 8}" width="{width:.1f}" height="28" rx="6" fill="{color}"></rect>'
        )
        parts.append(
            f'<text x="{238 + width:.1f}" y="{y + 28}" font-size="16" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{pct:.1f}%</text>'
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 430">'
        + "".join(parts)
        + "</svg>"
    )
    return drawing(svg, 64, 145, 1152, 430)


def _polar(cx, cy, radius, deg):
    rad = math.radians(deg - 90)
    return cx + radius * math.cos(rad), cy + radius * math.sin(rad)


def wedges(cx, cy, radius, slices, labels=True):
    """slices: (percent, color) starting at 12 o'clock, clockwise."""
    parts = []
    angle = 0
    for pct, color in slices:
        sweep = pct / 100 * 360
        if sweep >= 359.9:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{color}"></circle>')
            break
        x1, y1 = _polar(cx, cy, radius, angle)
        x2, y2 = _polar(cx, cy, radius, angle + sweep)
        large = 1 if sweep > 180 else 0
        parts.append(
            f'<path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {radius} {radius} 0 {large} 1 '
            f'{x2:.1f} {y2:.1f} Z" fill="{color}"></path>'
        )
        if labels and pct >= 12:
            lx, ly = _polar(cx, cy, radius * 0.62, angle + sweep / 2)
            ink = "#ffffff" if color == "#2a6f7a" else "#1c242c"
            parts.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="18" fill="{ink}" '
                f'font-family="Montserrat, sans-serif" font-weight="650">{pct:g}%</text>'
            )
        angle += sweep
    return "".join(parts)


def college_pies():
    parts = [
        '<rect x="0" y="0" width="1152" height="430" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>'
    ]
    pies = [
        (290, "De Anza", [(59.1, "#2a6f7a"), (40.9, "#d7ebe8")]),
        (860, "Foothill", [(71.4, "#2a6f7a"), (28.6, "#d7ebe8")]),
    ]
    for cx, name, slices in pies:
        parts.append(
            f'<text x="{cx}" y="42" text-anchor="middle" font-size="22" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{name}</text>'
        )
        parts.append(wedges(cx, 210, 130, slices))
    parts.append(
        '<rect x="430" y="380" width="18" height="18" rx="4" fill="#2a6f7a"></rect>'
        '<text x="456" y="395" font-size="16" fill="#1c242c" font-family="Montserrat, sans-serif">Part-time</text>'
        '<rect x="580" y="380" width="18" height="18" rx="4" fill="#d7ebe8" stroke="#c5ddd8"></rect>'
        '<text x="606" y="395" font-size="16" fill="#1c242c" font-family="Montserrat, sans-serif">Full-time</text>'
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 430">'
        + "".join(parts) + "</svg>"
    )
    return drawing(svg, 64, 145, 1152, 430)


def college_bars():
    values = [
        ("De Anza", [("9,200", 9200, "#d7ebe8"), ("13,296", 13296, "#2a6f7a")]),
        ("Foothill", [("4,059", 4059, "#d7ebe8"), ("10,124", 10124, "#2a6f7a")]),
    ]
    top, base, scale = 50, 330, 300 / 14000
    parts = [
        '<rect x="0" y="0" width="1152" height="420" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<line x1="120" y1="{base}" x2="1040" y2="{base}" stroke="#1c242c" stroke-width="1.6"></line>',
    ]
    for tick in (0, 4000, 8000, 12000):
        y = base - tick * scale
        parts.append(f'<line x1="110" y1="{y:.1f}" x2="1040" y2="{y:.1f}" stroke="#e4e1da" stroke-width="1"></line>')
        parts.append(
            f'<text x="100" y="{y + 5:.1f}" text-anchor="end" font-size="14" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{tick // 1000 if tick else 0}k</text>'
        )
    group_x = [280, 720]
    for gx, (name, bars) in zip(group_x, values):
        for i, (label, value, color) in enumerate(bars):
            h = value * scale
            x = gx + i * 90
            y = base - h
            ink = "#ffffff" if color == "#2a6f7a" else "#1c242c"
            parts.append(f'<rect x="{x}" y="{y:.1f}" width="72" height="{h:.1f}" rx="6" fill="{color}"></rect>')
            parts.append(
                f'<text x="{x + 36}" y="{y - 8:.1f}" text-anchor="middle" font-size="16" fill="#1c242c" '
                f'font-family="Montserrat, sans-serif" font-weight="650">{label}</text>'
            )
        parts.append(
            f'<text x="{gx + 81}" y="368" text-anchor="middle" font-size="20" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{name}</text>'
        )
    parts.append(
        '<rect x="430" y="390" width="16" height="16" rx="3" fill="#d7ebe8" stroke="#c5ddd8"></rect>'
        '<text x="454" y="404" font-size="15" fill="#1c242c" font-family="Montserrat, sans-serif">Full-time</text>'
        '<rect x="580" y="390" width="16" height="16" rx="3" fill="#2a6f7a"></rect>'
        '<text x="604" y="404" font-size="15" fill="#1c242c" font-family="Montserrat, sans-serif">Part-time</text>'
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 420">'
        + "".join(parts) + "</svg>"
    )
    return drawing(svg, 64, 150, 1152, 420)


def overlap_bars():
    rows = [("Under 25", 61.0), ("Transfer", 48.6), ("Full-time", 40.9), ("Everyone", 100)]
    top, base, scale = 36, 300, 250 / 100
    parts = [
        '<rect x="0" y="0" width="1152" height="380" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<line x1="70" y1="{base}" x2="1100" y2="{base}" stroke="#1c242c" stroke-width="1.6"></line>',
    ]
    for i, (name, pct) in enumerate(rows):
        h = pct * scale
        x = 120 + i * 250
        y = base - h
        color = "#1c242c" if name == "Everyone" else "#2a6f7a"
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="120" height="{h:.1f}" rx="8" fill="{color}"></rect>')
        parts.append(
            f'<text x="{x + 60}" y="{y - 10:.1f}" text-anchor="middle" font-size="18" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{pct:g}%</text>'
        )
        parts.append(
            f'<text x="{x + 60}" y="340" text-anchor="middle" font-size="16" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif">{name}</text>'
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 380">'
        + "".join(parts) + "</svg>"
    )
    return drawing(svg, 64, 200, 1152, 380)


def kind_pictures():
    parts = [
        '<rect x="0" y="0" width="540" height="430" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>',
        '<text x="36" y="40" font-size="14" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="700">FIGURE 1.3 · QUALITATIVE</text>',
        '<text x="36" y="72" font-size="22" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">Class year</text>',
        wedges(168, 230, 110, [(66, "#2a6f7a"), (18, "#8fbfc4"), (11, "#d7ebe8"), (5, "#1c242c")], labels=False),
    ]
    legend = [("First-year", "#2a6f7a"), ("Sophomore", "#8fbfc4"), ("Junior", "#d7ebe8"), ("Senior", "#1c242c")]
    for i, (name, color) in enumerate(legend):
        y = 150 + i * 36
        parts.append(f'<rect x="320" y="{y}" width="16" height="16" rx="4" fill="{color}"></rect>')
        parts.append(
            f'<text x="346" y="{y + 14}" font-size="16" fill="#1c242c" font-family="Montserrat, sans-serif">{name}</text>'
        )
    parts.append(
        '<rect x="572" y="0" width="580" height="430" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>'
        '<text x="608" y="40" font-size="14" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="700">FIGURE 1.4 · QUANTITATIVE</text>'
        '<text x="608" y="72" font-size="22" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">Credit hours</text>'
    )
    heights = [240, 565, 730, 625, 240]
    base, scale = 360, 250 / 800
    left = 640
    parts.append(f'<line x1="630" y1="{base}" x2="1100" y2="{base}" stroke="#1c242c" stroke-width="1.5"></line>')
    for i, value in enumerate(heights):
        h = value * scale
        x = left + i * 86
        y = base - h
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="86" height="{h:.1f}" fill="#5aa8b4" stroke="#ffffff" stroke-width="1.5"></rect>')
    for i, label in enumerate(["10", "13", "16", "19", "22", "25"]):
        x = left + i * 86
        parts.append(
            f'<text x="{x}" y="386" text-anchor="middle" font-size="14" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{label}</text>'
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 430">'
        + "".join(parts) + "</svg>"
    )
    return drawing(svg, 64, 150, 1152, 430)


def dot_rows(pattern):
    rows = []
    for line in pattern:
        cells = []
        for on in line:
            color = "#2a6f7a" if on else "#d5e0de"
            cells.append(
                f'<div style="width:18px;height:18px;border-radius:50%;background:{color};"></div>'
            )
        rows.append(
            '<div style="display:flex;gap:8px;margin-top:10px;">' + "".join(cells) + "</div>"
        )
    return "".join(rows)


def sample_card(label, heading, pattern, height=390):
    return card_shell(
        f'<p style="margin:0;color:#2a6f7a;font-size:13px;font-weight:700;letter-spacing:0.12em;">{label}</p>'
        f'<p style="margin:8px 0 0;color:#1c242c;font-size:22px;font-weight:650;">{heading}</p>'
        f'<div style="margin-top:18px;">{dot_rows(pattern)}</div>',
        height,
    )


def slides():
    out = []

    out.append(section([
        backdrop(),
        text_block(
            '<p style="margin:0;">'
            '<span style="color:#ffffff;background:#2a6f7a;padding:6px 12px;'
            'letter-spacing:0.12em;font-weight:700;font-size:16px;">MATH 117</span>'
            '<span style="color:#5d6670;font-size:20px;"> &nbsp; Unit 1 · Sampling and Data</span>'
            '</p>',
            72, 150, 660,
        ),
        text_block(
            '<h1 style="margin:0;color:#1c242c;font-size:64px;line-height:0.98;'
            'font-weight:650;letter-spacing:-0.04em;">Data and<br>sampling</h1>'
            '<p style="margin:22px 0 0;color:#1c242c;font-size:26px;line-height:1.3;">'
            'What kind of data, and how<br>the sample was chosen</p>'
            '<p style="margin:18px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;'
            'letter-spacing:0.08em;">SECTION 1.2</p>',
            72, 214, 660,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 560, 560,
        ),
        title_visual(),
    ], notes=(
        "Section 1.2. Blackboard tags this section with learning outcomes 1.1 and 1.4. "
        "Levels of measurement are textbook section 1.3, even though Blackboard also lists that outcome here. "
        "About 35 minutes after section 1.1."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Section 1.2") + title("Two questions"), 72, 48, 1100),
        text_block(num_card(
            "01", "What kind of data?",
            "Qualitative, or quantitative. If it is quantitative, discrete or continuous.",
            230,
        ), 72, 200, 540, 230),
        text_block(num_card(
            "02", "How was the sample chosen?",
            "Simple random, stratified, cluster, systematic, or convenience.",
            230,
        ), 656, 200, 540, 230),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;">A statistic is only useful when the sample looks like the population.</p>',
            72, 500, 1100,
        ),
    ], notes="Blackboard: LO 1.1 is the first question. LO 1.4 is the second. Do not call this section 1.3 or 1.4."))

    out.append(section([
        backdrop(),
        text_block(kicker("The kind of data") + title("Words, or numbers"), 64, 36, 1100),
        text_block(label_card(
            "QUALITATIVE",
            "A category",
            "Hair color, blood type, the car someone drives. Described by words or letters. An average hair color does not make sense. A letter grade, A through F, is qualitative too.",
            360,
        ), 64, 170, 560, 360),
        text_block(label_card(
            "QUANTITATIVE",
            "A number",
            "Money, pulse, weight, the number of students in a class. Quantitative data come from counting or measuring. The next slide splits them in two.",
            360,
        ), 656, 170, 560, 360),
    ], notes=(
        "Book note: quiz scores can be collected as numbers and reported as A, B, C, D, or F. "
        "The scores are quantitative. The letters are qualitative."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Quantitative data") + title("Count, or measure"), 64, 36, 1100),
        text_block(label_card(
            "DISCRETE",
            "A count",
            "Phone calls in a day: 0, 1, 2, or 3. Only certain numbers are possible. You do not receive 2.4 calls.",
            300,
        ), 64, 180, 560, 300),
        text_block(label_card(
            "CONTINUOUS",
            "A measurement",
            "Length of a call: 2.4, 7.5, or 11.0 minutes. Fractions and decimals are allowed. Length, weight, and time are the usual examples.",
            300,
        ), 656, 180, 560, 300),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">A phrase that starts with “the number of” is usually discrete.</p>',
            64, 540, 1100,
        ),
    ], notes="Example 1.5 is books in a backpack: 3, 4, 2, 1, discrete. Example 1.6 is the weights: 6.2, 7, 6.8, 9.1, 4.3, continuous."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Two pictures")
            + title("A category, or a measurement", 40),
            64, 24, 1100,
        ),
        kind_pictures(),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:18px;">'
            'Figure 1.3 is class year, qualitative. Figure 1.4 is credit hours, quantitative. '
            'The book does not print the pie percents or the bar heights.</p>',
            64, 600, 1150,
        ),
    ], notes="The pie wedges follow the shape of Figure 1.3. Do not treat them as measured percents. The histogram follows the shape of Figure 1.4. Credit hours in bins are quantitative."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.7")
            + title("One shopping trip, three kinds", 40),
            64, 28, 1150,
        ),
        text_block(num_card(
            "01", "Discrete",
            "Three cans of soup, two packages of nuts, four vegetables, two desserts. You counted them.",
            340,
        ), 64, 170, 370, 340),
        text_block(num_card(
            "02", "Continuous",
            "The soup weighs 19 ounces, 14.1 ounces, and 19 ounces. Weight is measured.",
            340,
        ), 454, 170, 370, 340),
        text_block(num_card(
            "03", "Qualitative",
            "Tomato bisque, lentil, walnuts, broccoli. The names are categories.",
            340,
        ), 844, 170, 370, 340),
    ], notes="Try It 1.7 is the same task with nails, oil, and screws. Types are qualitative. A count of boxes is discrete. 2 kg, 4 L, and 5 kg are continuous."))

    sort_items = [
        ("a", "The number of pairs of shoes you own"),
        ("b", "The type of car you drive"),
        ("c", "The distance from home to the grocery store"),
        ("d", "The number of classes you take per year"),
        ("e", "The type of calculator you use"),
        ("f", "The weights of dogs at a shelter"),
        ("g", "The number of correct answers on a quiz"),
        ("h", "IQ scores"),
    ]
    left_items = "".join(
        f'<div style="margin-top:8px;">{choice(letter, text)}</div>'
        for letter, text in sort_items[:4]
    )
    right_items = "".join(
        f'<div style="margin-top:8px;">{choice(letter, text)}</div>'
        for letter, text in sort_items[4:]
    )
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.9 · your turn")
            + title("Sort eight", 40)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">'
            'Write qualitative, discrete, or continuous.</p>',
            64, 24, 1150,
        ),
        text_block(left_items, 64, 175, 560),
        text_block(right_items, 656, 175, 560),
    ], notes="Answers next. a, d, g discrete. c, f, h continuous. b, e qualitative. IQ is the one that starts an argument. The book calls it continuous."))

    def pile(label, lines):
        rows = "".join(
            f'<p style="margin:10px 0 0;color:#1c242c;font-size:20px;line-height:1.3;">{line}</p>'
            for line in lines
        )
        return card_shell(
            f'<p style="margin:0;color:#2a6f7a;font-size:13px;font-weight:700;letter-spacing:0.12em;">{label}</p>'
            + rows,
            380,
        )

    out.append(section([
        backdrop(),
        text_block(kicker("Example 1.9") + title("Three piles", 40), 64, 28, 800),
        text_block(pile("QUALITATIVE", [
            "b &nbsp; Type of car",
            "e &nbsp; Type of calculator",
        ]), 64, 150, 370, 380),
        text_block(pile("DISCRETE", [
            "a &nbsp; Number of pairs of shoes",
            "d &nbsp; Number of classes per year",
            "g &nbsp; Number of correct answers",
        ]), 454, 150, 370, 380),
        text_block(pile("CONTINUOUS", [
            "c &nbsp; Distance to the store",
            "f &nbsp; Weights of dogs",
            "h &nbsp; IQ scores",
        ]), 844, 150, 370, 380),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">IQ is continuous in the book. The score is a measurement, not a count.</p>',
            64, 560, 1150,
        ),
    ]))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Table 1.3")
            + title("Compare the percent", 40)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">'
            'De Anza and Foothill, most recent spring quarter. The colleges are different sizes.</p>',
            64, 24, 1150,
        ),
        text_block(label_card(
            "DE ANZA · PART-TIME",
            "59.1%",
            "13,296 of 22,496 students",
            150,
        ), 64, 155, 560, 150),
        text_block(label_card(
            "FOOTHILL · PART-TIME",
            "71.4%",
            "10,124 of 14,183 students",
            150,
        ), 656, 155, 560, 150),
        text_block(
            data_table(
                ["", "De Anza", "De Anza %", "Foothill", "Foothill %"],
                [
                    ["Full-time", "9,200", "40.9%", "4,059", "28.6%"],
                    ["Part-time", "13,296", "59.1%", "10,124", "71.4%"],
                    ["Total", "22,496", "100%", "14,183", "100%"],
                ],
            ),
            64, 330, 1152,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'De Anza has more part-time students. Foothill has the larger part-time share.</p>',
            64, 560, 1150,
        ),
    ], notes="OpenStax Table 1.3. Percents let you compare groups that do not have the same total. Raw counts go the other way from the shares."))

    out.append(section([
        backdrop(),
        text_block(kicker("Qualitative data") + title("Three ways to show it"), 64, 36, 1100),
        text_block(num_card(
            "01", "Pie chart",
            "Each wedge is a category. The size matches the percent. The wedges have to add to 100%.",
            340,
        ), 64, 180, 370, 340),
        text_block(num_card(
            "02", "Bar graph",
            "The length of the bar matches the count or the percent. Bars can be vertical or horizontal.",
            340,
        ), 454, 180, 370, 340),
        text_block(num_card(
            "03", "Pareto chart",
            "A bar graph sorted from largest to smallest. Sorting makes the biggest category obvious.",
            340,
        ), 844, 180, 370, 340),
    ], notes="Example 1.10: a pie of first-years, sophomores, juniors, and seniors is qualitative data. There is no single best graph. It depends on the question."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Figure 1.5")
            + title("Same students, as pies", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">Part-time is the dark wedge. The percents in each pie add to 100%.</p>',
            64, 20, 1150,
        ),
        college_pies(),
    ], notes="Ask which college has the larger part-time share. The eye sees it faster here than in the table. Figure 1.5."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Figure 1.6")
            + title("Same students, as bars", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">These are the counts. De Anza’s part-time bar is taller. Foothill’s part-time share is larger.</p>',
            64, 20, 1150,
        ),
        college_bars(),
    ], notes="Figure 1.6. The book asks which picture, pie or bar, makes the comparison easier. Both are fair. The pie compares shares. The bar compares counts."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Table 1.5 · a Pareto chart")
            + title("Sorted, largest first", 36)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Ethnicity at De Anza. The dark bar is Other/Unknown, 9.6%, left out of the first table.</p>',
            64, 20, 1150,
        ),
        pareto_chart(),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:18px;">'
            'Other/Unknown is larger than Black, Filipino, Pacific Islander, and Native American.</p>',
            64, 600, 1150,
        ),
    ], notes=(
        "Table 1.5 sums to 22,044 of 24,382 students, 90.4%. Other/Unknown is 2,338 students, 9.6%. "
        "Figures 1.9 and 1.10 in the book. A Pareto chart sorts the bars."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("When a pie chart fails") + title("The pieces have to make one whole"), 64, 32, 1150),
        text_block(label_card(
            "MORE THAN 100%",
            "150.5%",
            "Full-time 40.9%. Intend to transfer 48.6%. Under age 25, 61.0%. A student can be in all three. Use a bar graph.",
            320,
        ), 64, 175, 560, 320),
        text_block(label_card(
            "LESS THAN 100%",
            "90.4%",
            "The ethnicity table left out Other/Unknown. The listed groups are not the whole college. Put the missing group back, or use a bar graph.",
            320,
        ), 656, 175, 560, 320),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">A pie chart needs every category, and each person in only one of them.</p>',
            64, 560, 1150,
        ),
    ], notes="Table 1.4 is the 150.5% example. Table 1.5 is the missing category. Both are De Anza."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Figure 1.7")
            + title("Three facts, not three slices", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'A student can be under 25, planning to transfer, and full-time. The dark bar is everyone.</p>',
            64, 20, 1150,
        ),
        overlap_bars(),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">40.9 + 48.6 + 61.0 = 150.5. A pie chart cannot hold that.</p>',
            64, 600, 1100,
        ),
    ], notes="Figure 1.7. The book draws all four bars in one color and includes All students at 100%. The dark bar here is that reference."))

    methods = [
        ("01", "Simple random", "Every group of the same size is equally likely. Put the names in a hat."),
        ("02", "Stratified", "Split into groups. Take some people from every group."),
        ("03", "Cluster", "Split into groups. Pick some groups, and take everyone in them."),
        ("04", "Systematic", "Start at random, then take every nth person. Every 50th name in a list of 20,000."),
        ("05", "Convenience", "Whoever is easy to reach. Shoppers already in the store. This one can be biased."),
    ]
    method_rows = []
    for num, name, text in methods:
        method_rows.append(
            '<div style="display:flex;align-items:center;gap:16px;background:#ffffff;'
            'border:1px solid #e4e1da;border-radius:14px;padding:10px 16px;margin-bottom:8px;">'
            f'{letter_badge(num)}'
            f'<div style="width:180px;color:#1c242c;font-size:20px;font-weight:650;flex:none;">{name}</div>'
            f'<div style="color:#5d6670;font-size:18px;line-height:1.3;">{text}</div>'
            '</div>'
        )
    out.append(section([
        backdrop(),
        text_block(kicker("Sampling") + title("Five ways to choose", 40), 64, 22, 800),
        text_block("".join(method_rows), 64, 130, 1152),
    ], notes=(
        "In a random sample, each person starts with an equal chance. Convenience is the one that is not random. "
        "The book’s calculator demo is randInt(0, 30) for a class of 31. Skip the button sequence unless someone asks."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Picture it") + title("Who gets picked", 40), 64, 24, 1000),
        text_block(sample_card(
            "SIMPLE RANDOM",
            "A few, scattered",
            [
                [0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 0, 0, 0],
                [0, 0, 1, 0, 1],
            ],
            300,
        ), 64, 150, 270, 300),
        text_block(sample_card(
            "STRATIFIED",
            "Some from each row",
            [
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0],
            ],
            300,
        ), 354, 150, 270, 300),
        text_block(sample_card(
            "CLUSTER",
            "Everyone in two rows",
            [
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
            ],
            300,
        ), 644, 150, 270, 300),
        text_block(sample_card(
            "SYSTEMATIC",
            "Every third person",
            [
                [1, 0, 0, 1, 0, 0, 1, 0],
            ],
            300,
        ), 934, 150, 270, 300),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">Teal is in the sample. Gray is not.</p>',
            64, 480, 800,
        ),
    ], notes="Each row is a group, except the systematic picture, which is one list. Convenience is whoever is already standing there. It does not have a pattern, so it is not drawn."))

    out.append(section([
        backdrop(),
        text_block(kicker("The mix-up") + title("Some from every group,<br>or everyone from some groups", 40), 64, 32, 1150),
        text_block(label_card(
            "STRATIFIED",
            "Some from each",
            "25 first-years, 25 sophomores, 25 juniors, 25 seniors. Every class year is in the sample.",
            280,
        ), 64, 220, 560, 280),
        text_block(label_card(
            "CLUSTER",
            "All from some",
            "Pick two class years at random. Then take every student in those two years. The other years are out.",
            280,
        ), 656, 220, 560, 280),
    ], notes="Same groups, opposite move. Stratified: a few from all groups. Cluster: all of a few groups."))

    scenarios = [
        ("a", "25 students from each class year"),
        ("b", "A random start, then every 50th student"),
        ("c", "75 students, each one equally likely"),
        ("d", "Two class years at random, then every student in them"),
        ("e", "The first 100 students outside the library"),
    ]
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.11")
            + title("Name the method", 40)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">'
            'San Jose State undergraduates. Each student is asked what they paid in tuition.</p>',
            64, 24, 1150,
        ),
        text_block(
            "".join(
                f'<div style="margin-top:8px;">{choice(letter, text)}</div>'
                for letter, text in scenarios
            ),
            64, 175, 900,
        ),
    ], notes="Answers: a stratified, b systematic, c simple random, d cluster, e convenience."))

    answers = [
        ("a", "Stratified", "25 from each class year"),
        ("b", "Systematic", "Every 50th student after a random start"),
        ("c", "Simple random", "Each student equally likely"),
        ("d", "Cluster", "Every student in two randomly chosen years"),
        ("e", "Convenience", "Whoever was outside the library"),
    ]
    answer_rows = []
    for letter, method, text in answers:
        answer_rows.append(
            '<div style="display:flex;align-items:center;gap:16px;background:#ffffff;'
            'border:1px solid #e4e1da;border-radius:14px;padding:10px 16px;margin-bottom:8px;">'
            f'{letter_badge(letter, filled=True)}'
            f'<div style="width:210px;color:#1c242c;font-size:22px;font-weight:650;flex:none;">{method}</div>'
            f'<div style="color:#5d6670;font-size:20px;">{text}</div>'
            '</div>'
        )
    out.append(section([
        backdrop(),
        text_block(kicker("Example 1.11") + title("Five methods", 40), 64, 24, 800),
        text_block("".join(answer_rows), 64, 140, 1152),
    ], notes=(
        "Extra, Example 1.12, if the class is fast: soccer ages stratified; all HR staff in five companies cluster; "
        "50 public and 50 private teachers stratified; every third cancer patient systematic; "
        "50 random numbers simple random; algebra classmates convenience. "
        "Try It 1.12, 50 from each class year, is stratified."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Replacement") + title("Can the same person<br>be picked twice?", 44), 64, 36, 1100),
        text_block(label_card(
            "WITH REPLACEMENT",
            "The name goes back",
            "That person can be chosen again. This is the theoretical random sample.",
            250,
        ), 64, 230, 560, 250),
        text_block(label_card(
            "WITHOUT REPLACEMENT",
            "The name stays out",
            "Surveys are done this way. For a large population and a small sample, the two are nearly the same.",
            250,
        ), 656, 230, 560, 250),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">The difference matters when the population is small.</p>',
            64, 540, 1100,
        ),
    ]))

    out.append(section([
        backdrop(),
        text_block(kicker("What can go wrong") + title("Three different problems"), 64, 32, 1100),
        text_block(num_card(
            "01", "Sampling error",
            "Comes from using a sample. A larger sample makes it smaller. It never disappears.",
            340,
        ), 64, 170, 370, 340),
        text_block(num_card(
            "02", "Nonsampling error",
            "A bad question, a broken counter, a missed person. A larger sample does not fix it.",
            340,
        ), 454, 170, 370, 340),
        text_block(num_card(
            "03", "Bias",
            "Some people are less likely to be chosen. A large biased sample is still biased. Call-in surveys are biased.",
            340,
        ), 844, 170, 370, 340),
    ], notes="Mailed surveys that come back on their own favor whoever bothers to answer. Better if the researcher selects who is asked."))

    checks = [
        ("01", "Representative", "A sample that misses part of the population gives results that are not valid."),
        ("02", "Self-selected", "Call-in surveys and volunteers. People choose to respond."),
        ("03", "Sample size", "Small samples can mislead. Crash tests and rare conditions are the exception."),
        ("04", "Nonresponse", "The people who answer often have the strong opinions."),
        ("05", "The wording", "A question can push the answer. The book calls this undue influence."),
        ("06", "Cause", "Two things can move together because of a third. Related is not caused."),
        ("07", "Who paid", "Read a self-interest study on the work. Do not assume it is good or bad."),
        ("08", "Confounding", "Several factors are tangled, so you cannot separate their effects."),
    ]
    check_blocks = [backdrop(), text_block(kicker("Critical evaluation") + title("Before you trust the study", 36), 64, 22, 1000)]
    for index, (num, heading, body) in enumerate(checks):
        col = index % 4
        row = index // 4
        x = 64 + col * 296
        y = 145 + row * 250
        check_blocks.append(text_block(
            card_shell(
                f'<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:650;">{num}</p>'
                f'<p style="margin:10px 0 0;color:#1c242c;font-size:20px;font-weight:650;">{heading}</p>'
                f'<p style="margin:8px 0 0;color:#5d6670;font-size:15px;line-height:1.3;">{body}</p>',
                230,
            ),
            x, y, 280, 230,
        ))
    out.append(section(check_blocks, notes=(
        "The book also lists misleading graphs: a bad scale, missing categories, no context. "
        "Discuss if time: honor students are a bad sample for the campus GPA. "
        "Every 20th child at one supermarket is not all children under 10. "
        "Twenty people in Central Park are not commuters in general. "
        "A simple random sample of 100 Massachusetts hospitals does match a question about hospitals in that state."
    )))

    spend_rows = [
        ("01", "Chemistry class", "Convenience. Several are also in calculus. Book bills run high. Biased."),
        ("02", "Every fifth senior in a PE class", "Systematic, but only senior citizens. Book bills run low. Biased."),
        ("03", "One student from each of 10 fields", "Simple random inside each field. Unbiased, and still small."),
    ]
    spend = []
    for num, heading, body in spend_rows:
        spend.append(
            '<div style="display:flex;gap:16px;align-items:flex-start;background:#ffffff;'
            'border:1px solid #e4e1da;border-radius:16px;padding:16px 18px;margin-bottom:12px;">'
            f'{letter_badge(num)}'
            f'<div><p style="margin:0;color:#1c242c;font-size:22px;font-weight:650;">{heading}</p>'
            f'<p style="margin:6px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">{body}</p></div>'
            '</div>'
        )
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.13")
            + title("What part-time students spend on books", 32)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'ABC College. 10,000 part-time students. Ten people in each sample.</p>',
            64, 22, 1150,
        ),
        text_block("".join(spend), 64, 160, 1152),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">A bigger sample does not repair a biased method.</p>',
            64, 580, 1100,
        ),
    ], notes=(
        "Chemistry amounts: 128, 87, 173, 116, 130, 204, 147, 189, 93, 153. "
        "Senior PE: 50, 40, 36, 15, 50, 100, 40, 53, 22, 22. "
        "Ten fields: 180, 50, 150, 85, 260, 75, 180, 200, 200, 150. "
        "The third sample is unbiased. The book still wants a larger sample."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Variation") + title("Two honest samples can disagree"), 64, 32, 1100),
        text_block(label_card(
            "THE CANS",
            "Not exactly 16 ounces",
            "15.8, 16.1, 15.2, 14.8, 15.8, 15.9, 16.0, 15.5. Measuring, and filling, both vary.",
            280,
        ), 64, 175, 560, 280),
        text_block(label_card(
            "TWO SLEEP STUDIES",
            "500 students each",
            "Doreen takes every nth student. Jung takes whole groups. The averages will differ. Neither one is wrong.",
            280,
        ), 656, 175, 560, 280),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'Roll a die 20 times, then 20 times again. The two counts will differ. Both can be right.</p>',
            64, 520, 1150,
        ),
    ], notes=(
        "Tables 1.8 and 1.9 are the die experiment, if you have dice. "
        "A later chapter explains why a random sample of about 1,200 to 1,500 can be enough for a national poll. "
        "A large sample can still be biased. Call-in polls are the example."
    )))

    tickets = [("A", "Qualitative"), ("B", "Quantitative discrete"), ("C", "Quantitative continuous")]
    body_fat = [("A", "Qualitative"), ("B", "Quantitative discrete"), ("C", "Quantitative continuous")]
    principal = [("A", "Simple random"), ("B", "Stratified"), ("C", "Cluster")]

    def question_block(number, prompt, pairs, answer, why):
        return (
            f'<p style="margin:0 0 4px;min-height:56px;color:#1c242c;font-size:22px;font-weight:650;line-height:1.25;">{number} &nbsp; {prompt}</p>'
            f'{choice_stack(pairs, answer, reveal=True)}'
            f'{reveal_line(why)}'
        )

    out.append(section([
        backdrop(),
        text_block(kicker("Quick check") + title("Name it", 40), 64, 24, 800),
        text_block(question_block(
            "1", "Tickets sold to a concert", tickets, "B", "You count tickets. 2.4 is impossible.",
        ), 64, 140, 370),
        text_block(question_block(
            "2", "Percent of body fat", body_fat, "C", "Body fat is measured, not counted.",
        ), 454, 140, 370),
        text_block(question_block(
            "3", "50 from each class year", principal, "B", "Some students from every year.",
        ), 844, 140, 370),
    ], notes="One right-arrow shows every answer: 1B, 2C, 3B. Arrow again leaves the slide. Homework 53 and 54. Try It 1.12 is the principal."))

    out.append(section([
        backdrop(),
        text_block(kicker("Before section 1.3") + title("You can name the data<br>and the sample", 48), 72, 64, 1100),
        text_block(
            '<p style="margin:0 0 14px;color:#1c242c;font-size:26px;line-height:1.35;">Qualitative, discrete, or continuous.</p>'
            '<p style="margin:0;color:#1c242c;font-size:26px;line-height:1.35;">Simple random, stratified, cluster, systematic, or convenience.</p>',
            72, 270, 1100,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">NEXT</p>'
                '<p style="margin:10px 0 0;color:#1c242c;font-size:28px;font-weight:650;">1.3 &nbsp; Frequency tables and levels of measurement</p>'
                '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">Nominal, ordinal, interval, and ratio. Then relative frequency.</p>',
                150,
            ),
            72, 430, 1000, 150,
        ),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Practice: OpenStax homework 53–79. &nbsp; Introductory Statistics 2e.</p>',
            72, 620, 1100,
        ),
    ], notes="Homework 53–64 are data types. 65–79 are sampling, bias, and variation. 71–73 are the sampling-method items."))

    return out


SHELL = """<!DOCTYPE html>
<html class="sl-root decks export offline loaded">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover, minimal-ui">
<meta charset="utf-8">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>MATH 117 · 1.2 Data and sampling</title>
<link rel="stylesheet" type="text/css" href="lib/offline-v2.css">
</head>
<body class="reveal-viewport theme-font-montserrat theme-color-white-blue">
<div class="reveal">
<div class="slides">
{slides}
</div>
</div>
<script>
var SLConfig = {{"deck": {{"slug": "math117-1-2-data-sampling", "title": "MATH 117 · 1.2 Data and sampling", "description": "Qualitative and quantitative data, and how a sample is chosen.", "width": 1280, "height": 720, "margin": 0.05, "theme_font": "montserrat", "theme_color": "white-blue", "center": false, "transition": "slide", "background_transition": "slide", "slide_count": {count}, "version": 2, "rtl": false, "should_loop": false, "shuffle": false, "navigation_mode": "default", "language": "en", "font_typekit": null, "font_google": null, "notes": {{}}}}}};
SLConfig.fonts_url = 'lib/fonts/';
</script>
<script src="lib/reveal.js"></script>
<script src="lib/reveal-plugins.js"></script>
<script src="lib/offline.js"></script>
<script>
Reveal.initialize({{
width: 1280,
height: 720,
margin: 0.05,
hash: true,
controls: true,
progress: true,
mouseWheel: false,
showNotes: false,
slideNumber: false,
fragmentInURL: true,
autoSlide: 0,
autoSlideStoppable: true,
autoAnimateMatcher: SL.deck.AutoAnimate.matcher,
center: false,
shuffle: false,
loop: false,
rtl: false,
navigationMode: "default",
transition: "slide",
backgroundTransition: "slide",
plugins: [ RevealZoom, RevealNotes, RevealMarkdown, RevealHighlight ]
}});
</script>
</body>
</html>
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
        dirs = sorted({
            path.parent.relative_to(OUT).as_posix()
            for path in OUT.rglob("*")
            if path.is_file()
        })
        for folder in dirs:
            if folder in ("", "."):
                continue
            zf.writestr(zipfile.ZipInfo(folder + "/"), "")
        for path in sorted(OUT.rglob("*")):
            if path.name == ".DS_Store" or not path.is_file():
                continue
            zf.write(path, path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
    print(f"slides {len(parts)}")
    print(f"index {'index.html' in names}")
    print(f"lib {'lib/offline-v2.css' in names}")
    print(f"zip {ZIP_PATH}")
    print(f"bytes {ZIP_PATH.stat().st_size}")


if __name__ == "__main__":
    main()
