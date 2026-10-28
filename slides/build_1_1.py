"""Section 1.1 as a Slides.com HTML export.

Matches the downloaded deck: index.html, lib/, cream canvas, teal labels,
white cards. Open index.html, or upload the zip.
"""

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE = Path("/Users/mac-mini/Downloads/slides_deck-8187f8-2")
OUT = ROOT / "1.1-key-terms"
ZIP_PATH = ROOT / "1.1-key-terms-slides.zip"
SLUG = "math117-1-1-key-terms"

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


def term_cell(label, text):
    return (
        '<div style="background:#ffffff;border:1px solid #e4e1da;border-radius:16px;'
        'padding:16px 20px;box-sizing:border-box;">'
        f'<p style="margin:0;color:#2a6f7a;font-size:13px;font-weight:700;'
        f'letter-spacing:0.12em;">{label}</p>'
        f'<p style="margin:8px 0 0;color:#1c242c;font-size:22px;line-height:1.25;'
        f'font-weight:650;">{text}</p></div>'
    )


def term_grid(pairs):
    cells = "".join(term_cell(label, text) for label, text in pairs)
    return (
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">'
        f'{cells}</div>'
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
    gray = "#b7c4c2"
    teal = "#2a6f7a"
    dots = [
        (48, 78), (108, 58), (168, 86), (58, 142), (124, 128), (188, 156),
        (72, 206), (146, 214), (46, 268), (118, 286), (186, 258),
        (64, 348), (138, 372), (196, 338), (52, 424), (150, 430),
        (236, 72), (300, 52), (364, 78), (408, 58),
        (248, 408), (318, 388), (386, 424), (292, 452),
        (400, 300), (360, 248),
    ]
    sample = [(262, 196), (314, 178), (366, 208), (274, 256), (330, 246), (300, 308)]
    circles = []
    for x, y in dots:
        circles.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{gray}"></circle>')
    for x, y in sample:
        circles.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{teal}"></circle>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 460 500">
      <rect x="8" y="8" width="444" height="484" rx="22" fill="#ffffff" stroke="#e4e1da" stroke-width="1.6"></rect>
      <rect x="228" y="150" width="176" height="190" rx="16" fill="#e7f3f4" stroke="{teal}" stroke-width="1.8"></rect>
      {"".join(circles)}
      <text x="48" y="470" font-size="15" fill="#5d6670" font-family="Montserrat, sans-serif" font-weight="650">Population</text>
      <text x="316" y="136" text-anchor="middle" font-size="15" fill="{teal}" font-family="Montserrat, sans-serif" font-weight="700">Sample</text>
    </svg>'''
    return drawing(svg, 760, 110, 460, 500)


def sleep_plot():
    counts = [(5, 1), (5.5, 1), (6, 3), (6.5, 4), (7, 2), (8, 2), (9, 1)]

    def xpos(value):
        return 80 + (value - 5) / 4 * 940

    parts = [
        '<rect x="8" y="8" width="1084" height="360" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>',
        '<line x1="48" y1="268" x2="1052" y2="268" stroke="#1c242c" stroke-width="2.2"></line>',
        '<polygon points="1052,268 1038,261 1038,275" fill="#1c242c"></polygon>',
        '<polygon points="48,268 62,261 62,275" fill="#1c242c"></polygon>',
    ]
    for value, count in counts:
        px = xpos(value)
        label = str(int(value)) if value == int(value) else str(value)
        parts.append(
            f'<line x1="{px}" y1="268" x2="{px}" y2="280" stroke="#1c242c" stroke-width="1.6"></line>'
        )
        parts.append(
            f'<text x="{px}" y="304" text-anchor="middle" font-size="18" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{label}</text>'
        )
        for i in range(count):
            cy = 246 - i * 34
            parts.append(
                f'<circle cx="{px}" cy="{cy}" r="12" fill="#ffffff" stroke="#2a6f7a" stroke-width="2.4"></circle>'
            )
    parts.append(
        '<text x="550" y="344" text-anchor="middle" font-size="16" fill="#5d6670" '
        'font-family="Montserrat, sans-serif">hours of sleep</text>'
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1100 370">'
        + "".join(parts)
        + "</svg>"
    )
    return drawing(svg, 64, 168, 1152, 390)


def data_table(headers, rows, term_column=False):
    ths = "".join(
        '<th style="text-align:left;background:#2a6f7a;color:#ffffff;font-size:15px;'
        f'font-weight:650;letter-spacing:0.06em;padding:12px 16px;">{header}</th>'
        for header in headers
    )
    body = []
    for index, row in enumerate(rows):
        bg = "#ffffff" if index % 2 == 0 else "#f3f8f7"
        cells = []
        for col, value in enumerate(row):
            color = "#2a6f7a" if term_column and col == 0 else "#1c242c"
            weight = "650" if term_column and col == 0 else "500"
            cells.append(
                f'<td style="padding:11px 16px;border-bottom:1px solid #e4e1da;font-size:20px;'
                f'color:{color};font-weight:{weight};background:{bg};">{value}</td>'
            )
        body.append(f'<tr>{"".join(cells)}</tr>')
    return (
        '<div style="border:1px solid #d5ddd9;border-radius:14px;overflow:hidden;">'
        '<table style="width:100%;border-collapse:collapse;">'
        f'<thead><tr>{ths}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
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
            '<h1 style="margin:0;color:#1c242c;font-size:78px;line-height:0.98;'
            'font-weight:650;letter-spacing:-0.04em;">Key terms</h1>'
            '<p style="margin:22px 0 0;color:#1c242c;font-size:28px;line-height:1.3;">'
            'Statistics, probability, and the<br>language of every study</p>'
            '<p style="margin:18px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;'
            'letter-spacing:0.08em;">SECTION 1.1</p>',
            72, 214, 660,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 520, 560,
        ),
        title_visual(),
    ], notes=(
        "About 30 minutes, then section 1.2. The next slide is the book’s dot plot. "
        "Have the class record hours of sleep, to the nearest half hour, and compare their plot with Figure 1.2."
    )))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Figure 1.2")
            + title("Hours of sleep", 40)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">One class. Each dot is one student. '
            '5, 5.5, 6, 6, 6, 6.5, 6.5, 6.5, 6.5, 7, 7, 8, 8, 9.</p>',
            64, 28, 1150,
        ),
        sleep_plot(),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">The dots pile up between 6 and 7. '
            'Another class of the same size would not match this plot dot for dot.</p>',
            64, 590, 1150,
        ),
    ], notes="OpenStax Introductory Statistics 2e, Figure 1.2. Ask where the data cluster, and whether an English class would look the same."))

    out.append(section([
        backdrop(),
        text_block(kicker("Section 1.1") + title("Tell a parameter<br>from a statistic", 52), 72, 56, 1100),
        text_block(num_card("01", "Name the groups", "The population is everyone the question is about. The sample is the part you actually measure.", 150), 72, 250, 1100, 150),
        text_block(num_card("02", "Name the numbers", "The parameter describes the population. The statistic describes the sample, and it estimates the parameter.", 150), 72, 416, 1100, 150),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;">You will also name the variable, the data, and whether the number is a mean or a proportion.</p>',
            72, 590, 1100,
        ),
    ], notes=(
        "This is textbook section 1.1. Blackboard tags this section with learning outcome 1.2, "
        "compare a parameter with a statistic. Textbook section 1.2 has not started."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("The word") + title("Statistics has four jobs"), 72, 40, 1000),
        text_block(num_card("01", "Collect", "Gather the measurements.", 250), 64, 180, 276, 250),
        text_block(num_card("02", "Analyze", "Organize what you gathered.", 250), 356, 180, 276, 250),
        text_block(num_card("03", "Interpret", "Decide what the data is saying.", 250), 648, 180, 276, 250),
        text_block(num_card("04", "Present", "Show the result clearly.", 250), 940, 180, 276, 250),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">A calculator can do the arithmetic. <strong>Understanding the data is the point.</strong></p>',
            72, 500, 1100,
        ),
    ], notes="Do not linger. The assessed skill is the six labels, not this definition."))

    out.append(section([
        backdrop(),
        text_block(kicker("Two jobs") + title("Summarize, or conclude"), 72, 36, 1000),
        text_block(
            label_card(
                "DESCRIPTIVE",
                "Summarize what you have",
                "A graph, or a number such as an average. You are describing the data in front of you.",
                280,
            ),
            64, 170, 560, 280,
        ),
        text_block(
            label_card(
                "INFERENTIAL",
                "Say something about everyone",
                "Use a sample to estimate a population. Probability tells you how confident that estimate can be.",
                280,
            ),
            656, 170, 560, 280,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#5d6670;font-size:13px;font-weight:700;letter-spacing:0.12em;">PROBABILITY, IN ONE MINUTE</p>'
                '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">'
                'A fair coin has probability 1/2. A few tosses wander. Karl Pearson tossed a coin 24,000 times and got 12,012 heads.</p>',
                120,
            ),
            64, 480, 1152, 120,
        ),
    ], notes="Probability is a preview. The course returns to it later. Pearson: 24,000 tosses, 12,012 heads, about half."))

    words = [
        ("01", "Population", "The whole group the question is about."),
        ("02", "Parameter", "A number that describes that whole group."),
        ("03", "Sample", "The part of the group you actually measure."),
        ("04", "Statistic", "A number from the sample. It estimates the parameter."),
        ("05", "Variable", "The characteristic you record for one member. Written X."),
        ("06", "Data", "The values you get. One value is a datum."),
    ]
    positions = [(64, 156), (452, 156), (840, 156), (64, 420), (452, 420), (840, 420)]
    word_blocks = [backdrop(), text_block(kicker("Every study") + title("Six words"), 64, 28, 800)]
    for (num, heading, body), (x, y) in zip(words, positions):
        word_blocks.append(text_block(num_card(num, heading, body, 240), x, y, 376, 240))
    out.append(section(word_blocks, notes="Same six labels, every problem, in this order."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("One study")
            + title("School supplies, not including books", 36)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">First-year students. One hundred surveyed at random.</p>',
            64, 28, 1100,
        ),
        text_block(label_card("EVERYONE", "Population", "All first-year students at the college this term.", 200), 64, 175, 560, 200),
        text_block(label_card("THE NUMBER FOR EVERYONE", "Parameter", "The mean amount all of them spent on supplies.", 200), 656, 175, 560, 200),
        text_block(label_card("WHO YOU MEASURED", "Sample", "The 100 students who were surveyed.", 200), 64, 395, 560, 200),
        text_block(label_card("THE NUMBER YOU CALCULATED", "Statistic", "The mean amount those 100 students spent.", 200), 656, 395, 560, 200),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">The statistic estimates the parameter when the sample reflects the population.</p>',
            64, 620, 1150,
        ),
    ], notes=(
        "The problem says 100 first-year students were randomly surveyed. Use that as the sample. "
        "The printed solution says the sample could be one statistics section, and warns that section "
        "may not represent all first-year students. That warning belongs in section 1.2."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Section 1.1") + title("The sample has to look<br>like the population", 44), 64, 36, 1100),
        text_block(num_card(
            "01", "A school’s GPA",
            "You estimate it from some students. You do not open every transcript.",
            200,
        ), 64, 240, 370, 200),
        text_block(num_card(
            "02", "A national poll",
            "1,000 to 2,000 people stand in for the whole country.",
            200,
        ), 454, 240, 370, 200),
        text_block(num_card(
            "03", "A few cans",
            "A few 16-ounce cans stand in for the whole production run.",
            200,
        ), 844, 240, 370, 200),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">If the sample misses part of the population, the statistic is a weak estimate.</p>',
            64, 480, 1150,
        ),
    ], notes="Still section 1.1. How a sample is chosen is textbook section 1.2. This slide only says the sample must represent the population."))

    out.append(section([
        backdrop(),
        text_block(kicker("Same study") + title("The variable is not the data"), 64, 40, 1100),
        text_block(
            label_card(
                "VARIABLE",
                "X = the amount",
                "The amount one first-year student spent on supplies. A numerical variable has units, so you can average it. A categorical variable is a label, such as major or yes/no. Averaging the labels does not make sense.",
                420,
            ),
            64, 180, 560, 420,
        ),
        text_block(
            label_card(
                "DATA",
                "$150, $200, $225",
                "These are three of the values. X is the variable. 150 is one datum. The mean of all 100 values is the statistic.",
                420,
            ),
            656, 180, 560, 420,
        ),
    ]))

    out.append(section([
        backdrop(),
        text_block(kicker("Two kinds of number") + title("A mean, or a proportion"), 64, 36, 1100),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:13px;font-weight:700;letter-spacing:0.12em;">MEAN</p>'
                '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;font-weight:650;">For a numerical variable</p>'
                '<p style="margin:28px 0 0;color:#1c242c;font-size:32px;font-weight:650;letter-spacing:-0.03em;">86, &nbsp;75, &nbsp;92</p>'
                '<p style="margin:16px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">(86 + 75 + 92) / 3 = 84.3</p>'
                '<p style="margin:22px 0 0;color:#5d6670;font-size:18px;line-height:1.4;">In everyday speech, “average” means this mean.</p>',
                430,
            ),
            64, 175, 560, 430,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:13px;font-weight:700;letter-spacing:0.12em;">PROPORTION</p>'
                '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;font-weight:650;">For a yes / no split</p>'
                '<p style="margin:28px 0 0;color:#1c242c;font-size:32px;font-weight:650;letter-spacing:-0.03em;">22 men out of 40</p>'
                '<p style="margin:16px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">22 / 40 = 0.55</p>'
                '<p style="margin:22px 0 0;color:#5d6670;font-size:18px;line-height:1.4;">Either kind of number can be a parameter or a statistic. The difference is who it describes.</p>',
                430,
            ),
            656, 175, 560, 430,
        ),
    ]))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example · a proportion")
            + title("Malpractice suits", 40)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">An insurer selects 500 doctors at random from a professional directory.</p>',
            64, 32, 1140,
        ),
        text_block(term_grid([
            ("POPULATION", "All doctors listed in that directory"),
            ("PARAMETER", "The proportion who have been in a malpractice suit"),
            ("SAMPLE", "The 500 doctors selected"),
            ("STATISTIC", "That proportion inside the 500"),
            ("VARIABLE", "X = whether one doctor has been in a suit"),
            ("DATA", "Yes, or no"),
        ]), 64, 200, 1152),
    ]))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.3 · Table 1.1")
            + title("Crash test", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">75 cars, simple random sample. '
            'The question is the proportion of driver dummies who would have had a head injury.</p>',
            64, 24, 1150,
        ),
        text_block(
            data_table(
                ["Speed at which cars crashed", "Location of the dummies"],
                [["35 miles per hour", "Front seat"]],
            )
            + '<p style="margin:8px 0 16px;color:#5d6670;font-size:14px;letter-spacing:0.08em;">TABLE 1.1</p>'
            + data_table(
                ["Term", "In this study"],
                [
                    ["Population", "All cars with dummies in the front seat"],
                    ["Parameter", "The proportion who would have had a head injury"],
                    ["Sample", "The 75 cars"],
                    ["Statistic", "That proportion in the 75"],
                    ["Variable", "X = whether one dummy would have had a head injury"],
                    ["Data", "Yes, or no"],
                ],
                term_column=True,
            ),
            64, 168, 1152,
        ),
    ], notes="OpenStax Table 1.1. The table is the study’s criterion, not the data. The data are yes or no for each dummy."))

    out.append(section([
        backdrop(),
        text_block(kicker("Your turn") + title("Write all six", 56), 80, 70, 1000),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:30px;line-height:1.35;font-weight:650;">'
            'Knoll Academy wants the average amount families spend on school uniforms each year.</p>'
            '<p style="margin:22px 0 0;color:#1c242c;font-size:26px;line-height:1.4;">'
            'We randomly survey 100 families with children at the school. Three of them spent $65, $75, and $95.</p>',
            80, 230, 1080,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:22px;font-weight:650;">Pause here.</p>'
                '<p style="margin:8px 0 0;color:#1c242c;font-size:22px;">Population, parameter, sample, statistic, variable, data.</p>',
                100,
            ),
            80, 480, 700, 100,
        ),
    ], notes="Give them a minute. The next slide is the check."))

    out.append(section([
        backdrop(),
        text_block(kicker("Your turn") + title("Knoll Academy"), 64, 32, 1000),
        text_block(term_grid([
            ("POPULATION", "All families with children at Knoll Academy"),
            ("PARAMETER", "The mean amount all of those families spend on uniforms in a year"),
            ("SAMPLE", "The 100 families surveyed"),
            ("STATISTIC", "The mean amount those 100 families spent"),
            ("VARIABLE", "X = the amount one family spent on uniforms"),
            ("DATA", "65, 75, 95, and the rest of the amounts"),
        ]), 64, 170, 1152),
    ]))

    gpa_choices = [
        ("a", "All students who attended the college last year"),
        ("b", "The cumulative GPA of one student who graduated last year"),
        ("c", "3.65, 2.80, 1.50, 3.90"),
        ("d", "A group of last year’s graduates, randomly selected"),
        ("e", "The average GPA of all students who graduated last year"),
        ("f", "All students who graduated from the college last year"),
        ("g", "The average GPA of the graduates in the study"),
    ]
    gpa_prompts = [
        ("1", "Population"),
        ("2", "Statistic"),
        ("3", "Parameter"),
        ("4", "Sample"),
        ("5", "Variable"),
        ("6", "Data"),
    ]

    def match_prompts(pairs):
        rows = []
        for num, label in pairs:
            rows.append(
                '<div style="display:flex;align-items:center;gap:14px;background:#ffffff;'
                'border:1px solid #e4e1da;border-radius:14px;padding:12px 16px;margin-bottom:10px;">'
                f'{letter_badge(num)}'
                f'<div style="color:#1c242c;font-size:22px;font-weight:650;">{label}</div>'
                '</div>'
            )
        return "".join(rows)

    def answer_rows(rows):
        lines = []
        for letter, term, text in rows:
            lines.append(
                '<div style="display:flex;align-items:center;gap:16px;background:#ffffff;'
                'border:1px solid #e4e1da;border-radius:14px;padding:8px 16px;margin-bottom:8px;">'
                f'{letter_badge(letter, filled=True)}'
                f'<div style="width:150px;color:#1c242c;font-size:20px;font-weight:650;flex:none;">{term}</div>'
                f'<div style="color:#1c242c;font-size:20px;line-height:1.25;">{text}</div>'
                '</div>'
            )
        return "".join(lines)

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.2")
            + title("Match a letter", 40)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'A college wants the average cumulative GPA of students who graduated last year.</p>',
            64, 24, 1150,
        ),
        text_block(match_prompts(gpa_prompts), 64, 175, 460),
        text_block(choice_stack(gpa_choices), 548, 168, 668),
    ], notes=(
        "OpenStax Example 1.2. Answers next slide: 1f, 2g, 3e, 4d, 5b, 6c. "
        "The trap is a: attended last year is not the same as graduated."
    )))

    out.append(section([
        backdrop(),
        text_block(kicker("Example 1.2") + title("Graduates, not everyone who attended", 36), 64, 24, 1150),
        text_block(answer_rows([
            ("f", "Population", "All students who graduated from the college last year"),
            ("g", "Statistic", "The average GPA of the graduates in the study"),
            ("e", "Parameter", "The average GPA of all students who graduated last year"),
            ("d", "Sample", "A group of last year’s graduates, randomly selected"),
            ("b", "Variable", "The cumulative GPA of one student who graduated last year"),
            ("c", "Data", "3.65, 2.80, 1.50, 3.90"),
        ]), 64, 130, 1152),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">'
            'Letter a is a trap. Attended the college is wider than graduated.</p>',
            64, 650, 1150,
        ),
    ]))

    athlete_choices = [
        ("a", "The average height of athletes at the university"),
        ("b", "The average height of athletes in the survey"),
        ("c", "All athletes at the university"),
        ("d", "All students at the university"),
        ("e", "The height of one athlete"),
        ("f", "A group of athletes, randomly selected"),
        ("g", "1.82, 1.76, 1.69, 1.93"),
    ]
    out.append(section([
        backdrop(),
        text_block(
            kicker("Your turn · Try It 1.2")
            + title("Match a letter", 40)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">'
            'A survey studies the heights, in meters, of athletes at a university.</p>',
            64, 24, 1150,
        ),
        text_block(match_prompts(gpa_prompts), 64, 175, 460),
        text_block(choice_stack(athlete_choices), 548, 168, 668),
    ], notes="Answers next: 1c, 2b, 3a, 4f, 5e, 6g. The book writes item 2 as Statistics. Use statistic. Letter d is the trap."))

    out.append(section([
        backdrop(),
        text_block(kicker("Try It 1.2") + title("Athletes, not every student", 36), 64, 24, 1150),
        text_block(answer_rows([
            ("c", "Population", "All athletes at the university"),
            ("b", "Statistic", "The average height of athletes in the survey"),
            ("a", "Parameter", "The average height of athletes at the university"),
            ("f", "Sample", "A group of athletes, randomly selected"),
            ("e", "Variable", "The height of one athlete"),
            ("g", "Data", "1.82, 1.76, 1.69, 1.93"),
        ]), 64, 130, 1152),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">'
            'Letter d is a trap. All students is wider than all athletes.</p>',
            64, 650, 1150,
        ),
    ]))

    out.append(section([
        backdrop(),
        text_block(kicker("Watch these") + title("Where the labels get swapped"), 64, 36, 1100),
        text_block(num_card(
            "01", "The sample is not the population",
            "“Students in this class” is not “all math students.”",
            390,
        ), 64, 175, 370, 390),
        text_block(num_card(
            "02", "Parameter, then statistic",
            "The parameter is everyone. The statistic is the people you measured. A sample mean of 3.5 days is a statistic.",
            390,
        ), 454, 175, 370, 390),
        text_block(num_card(
            "03", "X is not a data value",
            "$150 is one datum, not the statistic. On a proportion, the data are yes and no.",
            390,
        ), 844, 175, 370, 390),
    ]))

    def question_block(number, prompt, pairs, answer, why):
        return (
            f'<p style="margin:0;color:#1c242c;font-size:22px;font-weight:650;">{number} &nbsp; {prompt}</p>'
            f'{choice_stack(pairs, answer, reveal=True)}'
            f'{reveal_line(why)}'
        )

    population = [
        ("A", "All students at the college"),
        ("B", "The students in her own classes"),
        ("C", "All math students at the college"),
    ]
    variable = [("A", "Variable"), ("B", "Statistic"), ("C", "Data")]
    statistic = [("A", "Parameter"), ("B", "Statistic"), ("C", "Variable")]

    out.append(section([
        backdrop(),
        text_block(
            kicker("Quick check")
            + title("Days absent", 36)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">'
            'Lake Tahoe Community College math students. The sample mean is 3.5 days. '
            'X = days absent for one math student.</p>',
            64, 18, 1150,
        ),
        text_block(question_block(
            "1", "The population is", population, "C", "Her own classes are a sample.",
        ), 64, 128, 1152),
        text_block(question_block(
            "2", "X is a", variable, "A", "X is days absent for one student.",
        ), 64, 420, 560),
        text_block(question_block(
            "3", "3.5 days is a", statistic, "B", "3.5 came from the sample.",
        ), 656, 420, 560),
    ], notes="One right-arrow shows every answer: 1C, 2A, 3B. Arrow again leaves the slide. This is homework 50–52."))

    out.append(section([
        backdrop(),
        text_block(kicker("Before section 1.2") + title("You can name the six terms<br>on a new study", 48), 72, 70, 1100),
        text_block(
            '<p style="margin:0 0 16px;color:#1c242c;font-size:26px;line-height:1.35;">You can tell a parameter from a statistic.</p>'
            '<p style="margin:0;color:#1c242c;font-size:26px;line-height:1.35;">You can tell a mean from a proportion.</p>',
            72, 280, 1000,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">NEXT</p>'
                '<p style="margin:10px 0 0;color:#1c242c;font-size:28px;font-weight:650;">1.2 &nbsp; Data, sampling, and variation</p>'
                '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">Qualitative and quantitative data, and how a sample is chosen.</p>',
                140,
            ),
            72, 420, 900, 140,
        ),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Practice: OpenStax homework 42–52. &nbsp; Introductory Statistics 2e.</p>',
            72, 600, 1000,
        ),
    ], notes="Homework 42–49 are the six labels. Four are means and four are proportions. 50–52 are the days-absent check you just did."))

    return out


SHELL = """<!DOCTYPE html>
<html class="sl-root decks export offline loaded">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover, minimal-ui">
<meta charset="utf-8">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>MATH 117 · 1.1 Key terms</title>
<link rel="stylesheet" type="text/css" href="lib/offline-v2.css">
</head>
<body class="reveal-viewport theme-font-montserrat theme-color-white-blue">
<div class="reveal">
<div class="slides">
{slides}
</div>
</div>
<script>
var SLConfig = {{"deck": {{"slug": "math117-1-1-key-terms", "title": "MATH 117 · 1.1 Key terms", "description": "Sampling and data. Definitions of statistics, probability, and key terms.", "width": 1280, "height": 720, "margin": 0.05, "theme_font": "montserrat", "theme_color": "white-blue", "center": false, "transition": "slide", "background_transition": "slide", "slide_count": {count}, "version": 2, "rtl": false, "should_loop": false, "shuffle": false, "navigation_mode": "default", "language": "en", "font_typekit": null, "font_google": null, "notes": {{}}}}}};
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
