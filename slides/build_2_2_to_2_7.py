"""Sections 2.2 through 2.7 as Slides.com HTML exports.

Every count, quartile, and dollar amount on a student slide is taken from
OpenStax Introductory Statistics 2e. Figures are redrawn. A few try-its
are on the slides so a 60–80 minute class has a problem to work.
"""

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE = Path("/Users/mac-mini/Downloads/slides_deck-8187f8-2")

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


def qblock(number, prompt, pairs, answer, why):
    return (
        f'<p style="margin:0 0 4px;min-height:72px;color:#1c242c;font-size:20px;'
        f'font-weight:650;line-height:1.25;">{number} &nbsp; {prompt}</p>'
        f'{choice_stack(pairs, answer, reveal=True)}'
        f'{reveal_line(why)}'
    )


def quick(heading, triples, notes):
    blocks = [
        backdrop(),
        text_block(kicker("Quick check") + title(heading, 40), 64, 18, 1100),
    ]
    for i, (prompt, pairs, answer, why) in enumerate(triples):
        blocks.append(text_block(qblock(str(i + 1), prompt, pairs, answer, why), 64 + i * 390, 130, 370))
    return section(blocks, notes)


def svg_wrap(inner, width, height):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" '
        f'viewBox="0 0 {width} {height}">{inner}</svg>'
    )


def histogram(pairs, width, height, heading):
    left, right, top, bottom = 48, 20, 58, 52
    n = len(pairs)
    plot_w = width - left - right
    plot_h = height - top - bottom
    vmax = max(v for _, v in pairs) or 1
    bw = plot_w / n
    value_size = 16 if width > 700 else 13
    label_size = 15 if width > 700 else 12
    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="24" y="34" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        f'font-weight="700" letter-spacing="1.2">{heading}</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{width - right}" y2="{top + plot_h}" '
        f'stroke="#d5e0de" stroke-width="1.4"></line>',
    ]
    for i, (lab, val) in enumerate(pairs):
        h = val / vmax * (plot_h - 8)
        x = left + i * bw
        y = top + plot_h - h
        parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{bw + 0.6:.2f}" height="{max(h, 1):.2f}" '
            f'fill="#5aa8b4"></rect>'
        )
        parts.append(
            f'<text x="{x + bw / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="{value_size}" '
            f'fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="700">{val}</text>'
        )
        parts.append(
            f'<text x="{x + bw / 2:.1f}" y="{height - 18}" text-anchor="middle" font-size="{label_size}" '
            f'fill="#5d6670" font-family="Montserrat, sans-serif">{lab}</text>'
        )
    return svg_wrap("".join(parts), width, height)


def polygon(width=1152, height=390):
    pts = [(44.5, 0), (54.5, 5), (64.5, 10), (74.5, 30), (84.5, 40), (94.5, 15), (104.5, 0)]
    left, right, top, bottom = 64, 28, 48, 46
    plot_w = width - left - right
    plot_h = height - top - bottom
    xmin, xmax, ymax = 44.5, 104.5, 40

    def X(v):
        return left + (v - xmin) / (xmax - xmin) * plot_w

    def Y(v):
        return top + (1 - v / ymax) * plot_h

    path = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts)
    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        '<text x="24" y="30" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        'font-weight="700" letter-spacing="1.2">CALCULUS FINALS · FREQUENCY</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{width - right}" y2="{top + plot_h}" '
        f'stroke="#d5e0de" stroke-width="1.4"></line>',
        f'<polyline points="{path}" fill="none" stroke="#2a6f7a" stroke-width="3"></polyline>',
    ]
    for x, y in pts:
        parts.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="5" fill="#2a6f7a"></circle>')
        if y:
            parts.append(
                f'<text x="{X(x):.1f}" y="{Y(y) - 12:.1f}" text-anchor="middle" font-size="16" '
                f'fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="700">{y}</text>'
            )
        parts.append(
            f'<text x="{X(x):.1f}" y="{height - 16}" text-anchor="middle" font-size="14" '
            f'fill="#5d6670" font-family="Montserrat, sans-serif">{x}</text>'
        )
    return svg_wrap("".join(parts), width, height)


def series_svg(width=1152, height=280):
    """Shape only. No consumer-price numbers are invented on the picture."""
    pts = [(80, 190), (200, 170), (320, 150), (440, 156), (560, 120), (680, 108), (800, 90), (960, 70)]
    path = " ".join(f"{x},{y}" for x, y in pts)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#2a6f7a"></circle>' for x, y in pts)
    inner = (
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>'
        '<text x="24" y="32" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        'font-weight="700" letter-spacing="1.2">TIME ON THE HORIZONTAL AXIS</text>'
        f'<line x1="70" y1="210" x2="1040" y2="210" stroke="#d5e0de" stroke-width="1.4"></line>'
        f'<polyline points="{path}" fill="none" stroke="#2a6f7a" stroke-width="3"></polyline>'
        f'{dots}'
        '<text x="560" y="248" text-anchor="middle" font-size="16" fill="#5d6670" '
        'font-family="Montserrat, sans-serif">month</text>'
        '<text x="36" y="120" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">index</text>'
    )
    return svg_wrap(inner, width, height)


def box_svg(vmin, q1, med, q3, vmax, ticks, width=1152, height=250, heading=""):
    left, right = 72, 36
    span = vmax - vmin
    shift = (height * 0.46 - 132) if height > 320 else 0
    axis_y = 132 + shift

    def X(v):
        return left + (v - vmin) / span * (width - left - right)

    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="24" y="32" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        f'font-weight="700" letter-spacing="1.2">{heading}</text>',
        f'<line x1="{X(vmin):.1f}" y1="{axis_y}" x2="{X(vmax):.1f}" y2="{axis_y}" '
        f'stroke="#2a6f7a" stroke-width="3"></line>',
        f'<line x1="{X(vmin):.1f}" y1="{78 + shift:.1f}" x2="{X(vmin):.1f}" y2="{186 + shift:.1f}" stroke="#2a6f7a" stroke-width="3"></line>',
        f'<line x1="{X(vmax):.1f}" y1="{78 + shift:.1f}" x2="{X(vmax):.1f}" y2="{186 + shift:.1f}" stroke="#2a6f7a" stroke-width="3"></line>',
        f'<rect x="{X(q1):.1f}" y="{86 + shift:.1f}" width="{X(q3) - X(q1):.1f}" height="92" '
        f'fill="#d7ebe8" stroke="#2a6f7a" stroke-width="2"></rect>',
        f'<line x1="{X(med):.1f}" y1="{86 + shift:.1f}" x2="{X(med):.1f}" y2="{178 + shift:.1f}" stroke="#1c242c" '
        f'stroke-width="3" stroke-dasharray="7 5"></line>',
    ]
    for value, lab in ticks:
        parts.append(
            f'<text x="{X(value):.1f}" y="{214 + shift:.1f}" text-anchor="middle" font-size="15" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{lab}</text>'
        )
    return svg_wrap("".join(parts), width, height)


def opening(h1, subtitle, section_label, visual, notes):
    return section([
        backdrop(),
        text_block(
            '<p style="margin:0;">'
            '<span style="color:#ffffff;background:#2a6f7a;padding:6px 12px;'
            'letter-spacing:0.12em;font-weight:700;font-size:16px;">MATH 117</span>'
            '<span style="color:#5d6670;font-size:20px;"> &nbsp; Unit 2 · Descriptive statistics</span></p>',
            72, 148, 680, 48,
        ),
        text_block(
            f'<h1 style="margin:0;color:#1c242c;font-size:58px;line-height:0.98;font-weight:650;'
            f'letter-spacing:-0.04em;">{h1}</h1>'
            f'<p style="margin:22px 0 0;color:#1c242c;font-size:24px;line-height:1.3;">{subtitle}</p>'
            f'<p style="margin:18px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;'
            f'letter-spacing:0.08em;">{section_label}</p>',
            72, 214, 640,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 540, 560,
        ),
        visual,
    ], notes)


def closing(kicker_text, heading, lines, nxt, practice, notes):
    body = "".join(
        f'<p style="margin:0 0 14px;color:#1c242c;font-size:26px;line-height:1.35;">{line}</p>'
        for line in lines
    )
    return section([
        backdrop(),
        text_block(kicker(kicker_text) + title(heading, 46), 72, 56, 1100),
        text_block(body, 72, 210, 1080),
        text_block(card_shell(
            f'<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">NEXT</p>'
            f'<p style="margin:10px 0 0;color:#1c242c;font-size:28px;font-weight:650;">{nxt[0]}</p>'
            f'<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">{nxt[1]}</p>',
            130,
        ), 72, 430, 1080, 130),
        text_block(
            f'<p style="margin:0;color:#5d6670;font-size:18px;">{practice}</p>',
            72, 590, 900,
        ),
    ], notes)


def slides_22():
    out = []
    soccer = [(str(a), b) for a, b in zip(
        [60, 62, 64, 66, 68, 70, 72, 74],
        [5, 3, 15, 40, 17, 12, 7, 1],
    )]
    out.append(opening(
        "Histograms",
        "Bars that touch, for a long list<br>of measurements.",
        "SECTION 2.2",
        drawing(histogram(soccer, 460, 500, "100 SOCCER PLAYERS"), 760, 110, 460, 500),
        "About 20 minutes, then quartiles if the hour is still on graphs. "
        "This is the same 100 heights as section 1.3. The new work is how the bars are built. "
        "A stemplot was the tool for the 31 exam scores. A histogram is the tool once the list is long.",
    ))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Frequency and relative frequency")
            + title("A count, and a count divided by n", 36),
            64, 28, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Frequency</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;line-height:1.25;">How many times the value happens.</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;">Three students scored from 90% to 100%.</p>',
            230,
        ), 64, 180, 540, 230),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Relative frequency</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;line-height:1.25;">The count divided by n.</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;">3 / 40 = 0.075, which is 7.5%.</p>',
            230,
        ), 640, 180, 560, 230),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The bars of a histogram touch. A bar graph of categories leaves a gap. '
            'Use a histogram once the list is long. A common rule of thumb is about 100 values or more.</p>',
            64, 460, 1150,
        ),
    ], notes=(
        "Book sentence: RF = f/n. English class, f = 3, n = 40, RF = 0.075. "
        "90 to 100 percent are measurements, so a histogram fits. "
        "Choose 5 to 15 classes. A rough guide some people use is about the square root of n bars. "
        "The square root of 150 is about 12. The book still lets you choose."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.7 · continuous heights")
            + title("Start just below the smallest value", 36),
            64, 24, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.4;">'
            'Smallest height 60. Start at 59.95.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.4;">'
            'Largest height 74. End at 74.05.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.4;">'
            'Eight bars. Width (74.05 − 59.95) / 8 = 1.7625.</p>'
            '<p style="margin:12px 0 0;color:#2a6f7a;font-size:24px;font-weight:650;line-height:1.4;">'
            'Round the width up to 2.</p>',
            250,
        ), 64, 170, 1150, 250),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The extra decimal keeps a height off the boundary line. Rounding up can go against ordinary rounding, '
            'and that is allowed. A height on the left edge belongs to that bar. A height on the right edge belongs to the next bar. '
            'More than one correct histogram is possible.</p>',
            64, 460, 1150,
        ),
    ], notes=(
        "Same 100 players as Table 1.13. Continuous, to the nearest half inch. "
        "Boundaries: 59.95, 61.95, 63.95, 65.95, 67.95, 69.95, 71.95, 73.95, 75.95. "
        "The book notes that a width of 1.76 would also work. "
        "If every value is a whole number and the smallest is 2, the book starts at 1.5. "
        "If the most precise value is 6.1 and it is the smallest, start at 6.05."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.7")
            + title("The bars share their edges", 40),
            64, 16, 1150,
        ),
        drawing(histogram(soccer, 1152, 400, "HEIGHT IN INCHES · FREQUENCY"), 64, 130, 1152, 400),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'Each bar is 2 inches wide, from 59.95 to 75.95. Forty of the 100 players are in the bar at 66. '
            'The book’s figure shows relative frequency, so that bar is 0.40. The shape is the same either way.</p>',
            64, 560, 1150,
        ),
    ], notes=(
        "Counts: 5, 3, 15, 40, 17, 12, 7, 1. Relative frequencies: 0.05, 0.03, 0.15, 0.40, 0.17, 0.12, 0.07, 0.01. "
        "60 through 61.5 are in the first bar. 63.5 is in the second. 64 through 64.5 are in the third. "
        "66 through 67.5 are in the fourth. 68 through 69.5 are in the fifth. "
        "70 through 71 are in the sixth. 72 through 73.5 are in the seventh. 74 is in the eighth. "
        "Try It 2.7 is 50 shoe sizes, six bars. Leave it unless someone asks to build a second histogram."
    )))
    books = [("1", 11), ("2", 10), ("3", 16), ("4", 6), ("5", 5), ("6", 2)]
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.8 · counted books")
            + title("A histogram can be made of counts", 36),
            64, 16, 1150,
        ),
        drawing(histogram(books, 1152, 390, "BOOKS BOUGHT · 50 PART-TIME STUDENTS"), 64, 140, 1152, 390),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'The bars still touch. Start at 0.5 and end at 6.5, so each count sits in the middle of a bar of width 1. '
            'The bar for 3 books runs from 2.5 to 3.5. Sixteen of the 50 students bought three books.</p>',
            64, 555, 1150,
        ),
    ], notes=(
        "Eleven, ten, sixteen, six, five, and two students. The six frequencies add to 50. "
        "Calculator, in the notes only: L1 is 1 through 6, L2 is 11, 10, 16, 6, 5, 2. "
        "Window Xmin 0.5 and Xmax 6.5. Histogram plot, not a bar graph. "
        "Try It 2.8: 50 athletes. 20 play one sport, 22 play two, 8 play three. Same kind of histogram."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.10 · a frequency polygon")
            + title("Connect the class frequencies", 36),
            64, 16, 1150,
        ),
        drawing(polygon(), 64, 130, 1152, 390),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'Each point is a class. The labels are the middles: 54.5 holds the five scores from 49.5 to 59.5. '
            'The empty points at 44.5 and 104.5 bring the line down to the axis. The two sides are not mirrors, so the book calls the shape skewed.</p>',
            64, 545, 1150,
        ),
    ], notes=(
        "Table 2.14. Classes 49.5-59.5, 59.5-69.5, 69.5-79.5, 79.5-89.5, 89.5-99.5. "
        "Frequencies 5, 10, 30, 40, 15. Cumulative 5, 15, 45, 85, 100. "
        "The peak is the class centered at 84.5. "
        "Try It 2.10 is presidential age at inauguration. Leave the overlay polygons, Example 2.11, unless a student asks."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.12 · a time series")
            + title("The same measurement, in time order", 34),
            64, 20, 1150,
        ),
        drawing(series_svg(), 64, 150, 1152, 280),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The picture above is only the shape. The book’s graph is the consumer price index, every month, for ten years. '
            'Connect the points in calendar order. Do not change the time unit halfway across, and do not stretch an axis to exaggerate a change.</p>',
            64, 470, 1150,
        ),
    ], notes=(
        "Table 2.19 is a long monthly table. Do not copy it onto a slide. "
        "The teaching point is the order: time on the horizontal axis, the measurement on the vertical axis. "
        "The book’s caution, just before section 2.3: a time series is easy to distort by changing units mid-axis "
        "or by stretching one axis. Purposeful manipulation is presented there as unethical."
    )))
    out.append(quick("Name the graph", [
        ("A histogram’s bars", [("A", "Stay apart"), ("B", "Touch"), ("C", "Form a pie")], "B",
         "A bar graph of categories is the one that leaves gaps."),
        ("3 of 40 scored 90–100. The relative frequency is",
         [("A", "3"), ("B", "0.075"), ("C", "40")], "B", "3 divided by 40."),
        ("The bar for 3 books runs from",
         [("A", "3 to 4"), ("B", "2.5 to 3.5"), ("C", "0.5 to 6.5")], "B",
         "The count sits in the middle of a bar of width 1."),
    ], "One right-arrow shows every answer: 1B, 2B, 3B. Homework 76 through 81."))
    out.append(closing(
        "Before section 2.3",
        "You can build a histogram",
        [
            "Relative frequency is the count divided by n.",
            "Start one extra decimal below the smallest value, and let the bars touch.",
            "A frequency polygon connects the class counts. A time series follows the calendar.",
        ],
        ("2.3 &nbsp; Quartiles", "Where a value sits in an ordered list."),
        "Practice: OpenStax homework 76 through 81.",
        "Items 76 to 81 are the histogram homework. Section 2.3 starts at item 82.",
    ))
    return out


def slides_23():
    out = []
    out.append(opening(
        "Quartiles",
        "Where a value sits<br>in an ordered list.",
        "SECTION 2.3",
        drawing(svg_wrap(
            '<rect x="0" y="0" width="460" height="500" rx="18" fill="#ffffff" stroke="#e4e1da"></rect>'
            '<text x="36" y="70" font-size="16" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="700" letter-spacing="1.4">THE MIDDLE HALF</text>'
            '<text x="36" y="130" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">Q1</text>'
            '<text x="36" y="230" font-size="64" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">2</text>'
            '<text x="170" y="130" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">median</text>'
            '<text x="170" y="230" font-size="64" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="650">7</text>'
            '<text x="320" y="130" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">Q3</text>'
            '<text x="320" y="230" font-size="64" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">9</text>'
            '<text x="36" y="320" font-size="22" fill="#1c242c" font-family="Montserrat, sans-serif">IQR = 9 − 2 = 7</text>'
            '<text x="36" y="390" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">About half the values</text>'
            '<text x="36" y="418" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">sit between 2 and 9.</text>',
            460, 500,
        ), 760, 110, 460, 500),
        "Order the data first. Q2 is the median. Q1 is the median of the lower half. "
        "Q3 is the median of the upper half. This is the book's half method, not a different percentile formula.",
    ))
    out.append(section([
        backdrop(),
        text_block(kicker("A percentile is not a percent score") + title("90th percentile is not a grade of 90"), 64, 36, 1150),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;letter-spacing:0.08em;">WHAT IT MEANS</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;font-weight:650;line-height:1.3;">'
            '90% of the scores are the same as yours or lower. 10% are the same or higher.</p>',
            180,
        ), 64, 190, 1150, 180),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;letter-spacing:0.08em;">THE BOOK’S SAT EXAMPLE</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;font-weight:650;line-height:1.3;">'
            'A college that wants the 75th percentile of the SAT is asking for a score of at least 1220.</p>',
            160,
        ), 64, 400, 1150, 160),
    ], notes=(
        "The book’s college example is the 75th percentile, at least 1220, not the 90th. "
        "Percentiles are used with large populations. Quartiles cut an ordered list into four pieces: "
        "about one quarter on or below Q1, about half on or below Q2, about three quarters on or below Q3."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.16 · 29 ordered ages")
            + title("Find the place, then read the age", 36),
            64, 24, 1150,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">i = (k / 100) × (n + 1). Order the list first.</p>',
            64, 150, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">70TH PERCENTILE</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'i = (70 / 100) × (29 + 1) = 21.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">'
            '21 is a whole number. The 21st age is 64.</p>',
            210,
        ), 64, 230, 560, 210),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">83RD PERCENTILE</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'i = (83 / 100) × 30 = 24.9.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'Average the 24th and 25th ages, 71 and 72. The percentile is 71.5.</p>',
            210,
        ), 656, 230, 560, 210),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;">If i is not a whole number, round it down and up, then average those two ages.</p>',
            64, 500, 1150,
        ),
    ], notes=(
        "Ordered ages: 18, 21, 22, 25, 26, 27, 29, 30, 31, 33, 36, 37, 41, 42, 47, 52, 55, 57, 58, 62, 64, 67, 69, 71, 72, 73, 74, 76, 77. "
        "Position 21 is 64. Position 24 is 71. Position 25 is 72. "
        "The book notes that several percentile formulas exist. Use this one, i = (k/100)(n+1), for this section."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Fourteen ordered values")
            + title("Q1, the median, and Q3", 40),
            64, 24, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Lower half. The middle value is Q1.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:28px;font-weight:650;">1, 1, 2, 2, 4, 6, 6.8</p>'
            '<p style="margin:12px 0 0;color:#2a6f7a;font-size:24px;font-weight:650;">Q1 = 2</p>',
            170,
        ), 64, 170, 1150, 170),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Upper half. The middle value is Q3.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:28px;font-weight:650;">7.2, 8, 8.3, 9, 10, 10, 11.5</p>'
            '<p style="margin:12px 0 0;color:#2a6f7a;font-size:24px;font-weight:650;">Q3 = 9</p>',
            170,
        ), 64, 360, 1150, 170),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">The median is (6.8 + 7.2) / 2 = 7. The IQR is 9 − 2 = 7, the spread of the middle half.</p>',
            64, 560, 1150,
        ),
    ], notes=(
        "Unordered start: 1, 11.5, 6, 7.2, 4, 8, 9, 10, 6.8, 8.3, 2, 2, 10, 1. "
        "n = 14, so the median is the average of the 7th and 8th ordered values and is not itself in either half. "
        "In this example Q1 and Q3 are values in the data. The median, 7, is not."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.13 · 13 house prices")
            + title("A value past the fence", 40),
            64, 28, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The middle price, the 7th of 13</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:36px;font-weight:650;">$488,800</p>',
            130,
        ), 64, 170, 540, 130),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">IQR = 649,000 − 308,750</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:36px;font-weight:650;">$340,250</p>',
            130,
        ), 640, 170, 560, 130),
        text_block(
            '<p style="margin:0 0 12px;color:#1c242c;font-size:24px;line-height:1.35;">'
            '1.5 × 340,250 = 510,375.</p>'
            '<p style="margin:0 0 12px;color:#1c242c;font-size:24px;line-height:1.35;">'
            'Fences: 308,750 − 510,375 = −201,625, and 649,000 + 510,375 = 1,159,375.</p>'
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            '$5,500,000 is the only price above 1,159,375. It is a potential outlier.</p>',
            64, 340, 1150,
        ),
    ], notes=(
        "Ordered prices: 114950, 158000, 230500, 387000, 389950, 479000, 488800, 529000, 575000, 639000, 659000, 1095000, 5500000. "
        "Q1 is the median of the lower six, (230500 + 387000) / 2 = 308750. "
        "Q3 is the median of the upper six, (639000 + 659000) / 2 = 649000. "
        "Use these printed quartiles. A value is a potential outlier if it is below Q1 minus 1.5 IQR or above Q3 plus 1.5 IQR. "
        "The next slide is Try It 2.13. Give them two minutes, then show the answer."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.13 · your turn")
            + title("Eleven salaries", 44)
            + '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;line-height:1.4;">'
            '28,000 &nbsp; 33,000 &nbsp; 40,500 &nbsp; 42,000 &nbsp; 54,000 &nbsp; 54,000<br>'
            '64,500 &nbsp; 68,500 &nbsp; 69,000 &nbsp; 72,000 &nbsp; 120,000</p>'
            + '<p style="margin:18px 0 0;color:#5d6670;font-size:22px;">Already in order. Find the IQR. Is $120,000 an outlier?</p>',
            64, 80, 1100,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">PAUSE</p>'
                '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;line-height:1.35;">'
                'n = 11, so the median is the 6th salary. Q1 and Q3 are the middles of the two halves.</p>',
                140,
            ),
            64, 420, 1100, 140,
        ),
    ], notes="Give them about two minutes. The next slide is the check. Do not start the fence until Q1 and Q3 are on the board."))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.13")
            + title("$120,000 is past the fence", 40),
            64, 28, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Q1 · median · Q3</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">$40,500 · $54,000 · $69,000</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;">IQR = 69,000 − 40,500 = $28,500</p>',
            180,
        ), 64, 170, 1150, 180),
        text_block(
            '<p style="margin:0 0 10px;color:#1c242c;font-size:24px;line-height:1.35;">'
            '1.5 × 28,500 = 42,750. The upper fence is 69,000 + 42,750 = $111,750.</p>'
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            '$120,000 is above that fence. It is a potential outlier. Nothing falls below the lower fence.</p>',
            64, 400, 1150,
        ),
    ], notes=(
        "Lower five: 28000, 33000, 40500, 42000, 54000. Q1 is 40500. "
        "Upper five: 64500, 68500, 69000, 72000, 120000. Q3 is 69000. "
        "Lower fence is 40500 − 42750, which is negative, so no low outlier."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.14 · the same exam, two classes")
            + title("Compare the middle halves", 38),
            64, 24, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">DAY</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">Min 32 · Q1 56 · median 74.5</p>'
            '<p style="margin:6px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">Q3 82.5 · max 99</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;font-weight:650;">IQR 26.5. No outliers.</p>',
            230,
        ), 64, 180, 560, 230),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">NIGHT</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">Min 25.5 · Q1 78 · median 81</p>'
            '<p style="margin:6px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">Q3 89 · max 98</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;font-weight:650;">IQR 11. Outliers 25.5 and 45.</p>',
            230,
        ), 656, 180, 560, 230),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'The night scores sit higher, and their middle half is tighter. '
            'The day fences are 16.25 and 122.25. The night fences are 61.5 and 105.5.</p>',
            64, 460, 1150,
        ),
    ], notes=(
        "Day IQR = 82.5 - 56 = 26.5. Night IQR = 89 - 78 = 11. "
        "1.5 times 26.5 is 39.75, so the day fences are 56 - 39.75 = 16.25 and 82.5 + 39.75 = 122.25. "
        "1.5 times 11 is 16.5, so the night fences are 78 - 16.5 = 61.5 and 89 + 16.5 = 105.5. "
        "45 and 25.5 are below 61.5. No night score is above 105.5."
    )))
    out.append(quick("Locate the value", [
        ("Scoring in the 90th percentile means",
         [("A", "A grade of 90%"), ("B", "90% scored the same or lower"), ("C", "The mean is 90")],
         "B", "It is a position in the ordered list."),
        ("For the 14 values, the IQR is",
         [("A", "7"), ("B", "11.5"), ("C", "2")], "A", "Q3 minus Q1 is 9 − 2."),
        ("The night-class outliers are",
         [("A", "None"), ("B", "25.5 and 45"), ("C", "98")], "B", "Both sit below the fence at 61.5."),
    ], "One right-arrow shows 1B, 2A, 3B. Homework 82 and 83."))
    out.append(closing(
        "Before section 2.4",
        "You can place a value",
        [
            "A percentile is a position, not a percent correct.",
            "Q1, the median, and Q3 cut an ordered list into quarters.",
            "A value below Q1 − 1.5 IQR, or above Q3 + 1.5 IQR, is a potential outlier.",
        ],
        ("2.4 &nbsp; Box plots", "Those five numbers as a picture."),
        "Practice: OpenStax homework 82 and 83.",
        "Items 84 through 89 are the box-plot homework, section 2.4.",
    ))
    return out


def slides_24():
    out = []
    ticks14 = [(1, "1"), (2, "2"), (7, "7"), (9, "9"), (11.5, "11.5")]
    out.append(opening(
        "Box plots",
        "Five numbers, drawn<br>on a scaled line.",
        "SECTION 2.4",
        drawing(box_svg(1, 2, 7, 9, 11.5, ticks14, 460, 500, "MIN, Q1, MEDIAN, Q3, MAX"), 760, 110, 460, 500),
        "The box is Q1 to Q3. The dashed line is the median. Whiskers run to the minimum and the maximum, "
        "unless the plot marks outliers as dots. The axis has to be scaled or the picture lies.",
    ))
    out.append(section([
        backdrop(),
        text_block(kicker("Five numbers") + title("What the picture is made of"), 72, 36, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">MINIMUM</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;">The left whisker ends here.</p>',
            150,
        ), 64, 190, 360, 150),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">Q1 AND Q3</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;">The box. About the middle 50%.</p>',
            150,
        ), 452, 190, 370, 150),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">MEDIAN</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;">A dashed line inside the box.</p>',
            150,
        ), 850, 190, 360, 150),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'The right whisker ends at the maximum. About 25% of the values sit in each quarter. '
            'Some box plots mark an outlier with a dot and stop the whisker at the last value that is not an outlier.</p>',
            64, 400, 1150,
        ),
    ], notes=(
        "The median can sit on Q1 or on Q3. It does not have to be in the center of the box. "
        "Calculator steps stay in the notes: STAT, CALC, 1-Var Stats, then the box-plot plot type. "
        "Do not spend the slide on keystrokes."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("The same 14 values")
            + title("Whiskers out to the ends", 40),
            64, 16, 1150,
        ),
        drawing(box_svg(1, 2, 7, 9, 11.5, ticks14, 1152, 280, "Q1 IS 2 · MEDIAN IS 7 · Q3 IS 9"), 64, 150, 1152, 280),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            'The minimum is 1 and the maximum is 11.5. The box runs from 2 to 9, so the middle half covers 7 units. '
            'Start from a scaled number line. An unscaled box is not useful.</p>',
            64, 480, 1150,
        ),
    ], notes="Figure 2.11. The two whiskers run from Q1 to the smallest value and from Q3 to the largest. The median is the dashed line."))
    height_ticks = [(59, "59"), (64.5, "64.5"), (66, "66"), (70, "70"), (77, "77")]
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.23 · 40 student heights")
            + title("Which quarter is the narrow one?", 34),
            64, 12, 1150,
        ),
        drawing(box_svg(59, 64.5, 66, 70, 77, height_ticks, 1152, 270, "INCHES"), 64, 130, 1152, 270),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The four quarters span 5.5, 1.5, 4, and 7 inches. The second quarter is the narrow one. The fourth is the widest. '
            'Range = 77 − 59 = 18. IQR = 70 − 64.5 = 5.5, so the middle 50% covers 5.5 inches.</p>',
            64, 440, 1150,
        ),
    ], notes=(
        "Minimum 59, Q1 64.5, median 66, Q3 70, maximum 77. "
        "Each quarter holds about 25% of the heights. "
        "The book also notes that 59 through 65 holds more than 25%, so it holds more heights than 66 through 70. "
        "TI: enter the 40 heights, 1-Var Stats. Read minX, Q1, Med, Q3, maxX. The plot type is a box plot."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Fifteen students · minutes of exercise")
            + title("300 minutes is past the fence", 38),
            64, 24, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.45;">Min 0 · Q1 20 · median 40 · Q3 60 · max 300</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.45;">IQR = 60 − 20 = 40.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.45;">Q3 + 1.5 × IQR = 60 + 60 = 120.</p>'
            '<p style="margin:14px 0 0;color:#2a6f7a;font-size:26px;font-weight:650;">300 is greater than 120, so it is a potential outlier.</p>',
            280,
        ), 64, 160, 1150, 280),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'About 75% of these students exercise 60 minutes or less. Half of them fall between 20 and 60 minutes. '
            'Fifteen students is a small sample. The principal should ask more students before buying equipment on this alone.</p>',
            64, 480, 1150,
        ),
    ], notes=(
        "The fifteen times: 0, 40, 60, 30, 60, 10, 45, 30, 300, 90, 30, 120, 60, 0, 20. "
        "If 300 is set aside, the book’s new maximum is 120. Q1 is still 20 and Q3 is still 60. "
        "The conclusion does not change: half the students are between 20 and 60 minutes. "
        "The next slide is Try It 2.22. Same five numbers, then a decision."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.22 · your turn")
            + title("Ten project times", 44)
            + '<p style="margin:14px 0 0;color:#1c242c;font-size:28px;line-height:1.4;">'
            '2, 3, 5, 3, 4, 4, 3, 11, 3, 2 hours.</p>'
            + '<p style="margin:16px 0 0;color:#5d6670;font-size:22px;line-height:1.4;">'
            'The instructor hopes a typical project takes 3 to 4 hours. Find the five numbers. Should the project change?</p>',
            64, 90, 1100,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">PAUSE</p>'
                '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;">Order the ten times first. n is even, so the median is the average of the 5th and 6th.</p>',
                140,
            ),
            64, 420, 1100, 140,
        ),
    ], notes="Ordered: 2, 2, 3, 3, 3, 3, 4, 4, 5, 11. Give them about two minutes."))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.22")
            + title("Leave the project as it is", 40),
            64, 28, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Min · Q1 · median · Q3 · max</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:32px;font-weight:650;">2 · 3 · 3 · 4 · 11</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;">IQR = 4 − 3 = 1. The upper fence is 4 + 1.5 = 5.5.</p>',
            190,
        ), 64, 170, 1150, 190),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.4;">'
            '11 hours is a potential outlier. The middle half is 3 to 4 hours, which is what the instructor hoped. '
            'One long project is not a reason to change the assignment.</p>',
            64, 420, 1150,
        ),
    ], notes=(
        "Lower half 2, 2, 3, 3, 3 so Q1 is 3. Upper half 3, 4, 4, 5, 11 so Q3 is 4. "
        "The 5th and 6th ordered times are both 3, so the median is 3."
    )))
    out.append(quick("Read the box", [
        ("The box holds",
         [("A", "Every value"), ("B", "About the middle 50%"), ("C", "Only the median")],
         "B", "The whiskers cover the rest."),
        ("The dashed line inside the box is",
         [("A", "The mean"), ("B", "The median"), ("C", "The maximum")],
         "B", "Q1 and Q3 are the ends of the box."),
        ("300 minutes of exercise is",
         [("A", "The median"), ("B", "A potential outlier"), ("C", "Q1")],
         "B", "The fence is 60 + 1.5 × 40 = 120."),
    ], "One right-arrow shows 1B, 2B, 3B. Homework 84 through 89."))
    out.append(closing(
        "Before section 2.5",
        "You can read a box",
        [
            "The five numbers are the minimum, Q1, the median, Q3, and the maximum.",
            "The box is the middle half. The whiskers run to the ends.",
            "A scaled axis is part of the picture.",
        ],
        ("2.5 &nbsp; Center", "Mean, median, and mode."),
        "Practice: OpenStax homework 84 through 89.",
        "Section 2.5 homework is items 90 and 91.",
    ))
    return out


def slides_25():
    out = []
    out.append(opening(
        "Center",
        "Mean, median,<br>and mode.",
        "SECTION 2.5",
        drawing(svg_wrap(
            '<rect x="0" y="0" width="460" height="500" rx="18" fill="#ffffff" stroke="#e4e1da"></rect>'
            '<text x="36" y="78" font-size="16" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="700" letter-spacing="1.4">40 EMERGENCY VISITS</text>'
            '<text x="36" y="150" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">mean</text>'
            '<text x="36" y="220" font-size="64" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">23.6</text>'
            '<text x="36" y="290" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">median</text>'
            '<text x="36" y="360" font-size="64" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="650">24</text>'
            '<text x="36" y="430" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">years of age</text>',
            460, 500,
        ), 760, 110, 460, 500),
        "Example 2.26. The calculator result is a mean of 23.6 and a median of 24. "
        "Say average when you mean the arithmetic mean. The symbols: x-bar for a sample, μ for a population.",
    ))
    out.append(section([
        backdrop(),
        text_block(kicker("The mean") + title("Add the values, then divide"), 72, 40, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">SAMPLE MEAN</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:32px;font-weight:650;">x&#772;</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:22px;">The people you actually measured.</p>',
            220,
        ), 72, 200, 520, 220),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">POPULATION MEAN</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:32px;font-weight:650;">μ</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:22px;">Everyone the study is about.</p>',
            220,
        ), 640, 200, 540, 220),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">When someone says average, they mean this mean.</p>',
            72, 480, 1000,
        ),
    ], notes=(
        "Let a calculator do the adding. STAT, EDIT, type the list, STAT, CALC, 1-Var Stats. "
        "Read x-bar. The Law of Large Numbers is the next idea: larger samples, and the sample mean "
        "is very likely to move toward μ. The book returns to that later. One sentence is enough today."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.26 · 40 patients")
            + title("The median has a location", 40),
            64, 28, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Where the median sits</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:32px;font-weight:650;">(40 + 1) / 2 = 20.5</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">Between the 20th and 21st ages. Both are 24, so the median is 24.</p>',
            210,
        ), 64, 180, 1150, 210),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'The mean of the 40 ages is 23.6 years. The location 20.5 is not the median. The median is the age that sits there.</p>',
            64, 440, 1150,
        ),
    ], notes=(
        "Ordered ages, 40 of them, from 3, 4, 8, 8 up to 44, 44, 47. "
        "The 20th and 21st are the two 24s. Calculator: clear L1, STAT EDIT, 1-Var Stats. x-bar = 23.6, Med = 24. "
        "If n is odd, the location (n+1)/2 is a single ordered value. If n is even, average the two middle values."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.27 · a town of 50 people")
            + title("One income pulls the mean", 38),
            64, 28, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The mean</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">(49 × 30,000 + 5,000,000) / 50</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:40px;font-weight:650;">$129,400</p>',
            190,
        ), 64, 180, 560, 190),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The median</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">49 people earn this.</p>'
            '<p style="margin:10px 0 0;color:#2a6f7a;font-size:40px;font-weight:650;">$30,000</p>',
            190,
        ), 656, 180, 560, 190),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'The median is the better center. The income of $5,000,000 is an outlier, and the mean follows it.</p>',
            64, 430, 1150,
        ),
    ], notes=(
        "The book states the median, 30000, and does not print the mean. "
        "49 times 30000 is 1470000. Add 5000000 to get 6470000. Divide by 50 to get 129400. "
        "The next two slides are Try It 2.27. Same question, houses instead of incomes."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.27 · your turn")
            + title("Sixty houses", 48)
            + '<p style="margin:16px 0 0;color:#1c242c;font-size:26px;line-height:1.4;">'
            'One house is worth $2,500,000. Twenty-nine are worth $280,000. The other thirty are worth $315,000.</p>'
            + '<p style="margin:18px 0 0;color:#5d6670;font-size:22px;">Which is the better center, the mean or the median?</p>',
            64, 100, 1100,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">PAUSE</p>'
                '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;line-height:1.35;">'
                'n = 60, so the median is the average of the 30th and 31st ordered prices.</p>',
                140,
            ),
            64, 430, 1100, 140,
        ),
    ], notes="Do not have them add all 60 prices by hand. The next slide shows both numbers."))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.27")
            + title("The median stays with the houses", 36),
            64, 28, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The mean</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">(29 × 280,000 + 30 × 315,000 + 2,500,000) / 60</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:36px;font-weight:650;">$334,500</p>',
            200,
        ), 64, 170, 560, 200),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The median</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">The 30th and 31st prices are both this.</p>'
            '<p style="margin:10px 0 0;color:#2a6f7a;font-size:36px;font-weight:650;">$315,000</p>',
            200,
        ), 656, 170, 560, 200),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'The median is the better center. The house worth $2,500,000 pulls the mean up.</p>',
            64, 430, 1150,
        ),
    ], notes="29 times 280000 is 8120000. 30 times 315000 is 9450000. Add 2500000 to get 20070000. Divide by 60 to get 334500."))
    out.append(section([
        backdrop(),
        text_block(kicker("The mode") + title("The value that appears most"), 72, 28, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">EXAMPLE 2.28</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">Twenty exam scores. 72 appears five times.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">The mode is 72.</p>',
            180,
        ), 64, 170, 560, 180),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">EXAMPLE 2.29</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">430, 430, 480, 480, 495.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Two modes. Bimodal.</p>',
            180,
        ), 656, 170, 560, 180),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The mode works for words too. In red, red, red, green, green, yellow, purple, black, blue, the mode is red. '
            'A weight-loss ad can quote a mean loss of 6 pounds while the mode is 2 pounds.</p>',
            64, 400, 1150,
        ),
    ], notes=(
        "The 20 scores: 50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93. "
        "84 appears three times, so 72 is the only mode. "
        "Try It 2.28, books checked out, the mode is 7, which appears four times. "
        "Try It 2.29, credit scores 680, 680, 700, 720, 720, is also bimodal."
    )))
    out.append(section([
        backdrop(),
        text_block(kicker("One more sentence") + title("Larger samples pull the mean toward μ"), 64, 48, 1150),
        text_block(card_shell(
            '<p style="margin:0;color:#1c242c;font-size:28px;line-height:1.4;">'
            'The Law of Large Numbers: take larger and larger samples, and the sample mean is very likely to get closer to the population mean.</p>'
            '<p style="margin:20px 0 0;color:#5d6670;font-size:22px;">The book returns to this later. Today, the point is what the mean is.</p>',
            220,
        ), 64, 200, 1150, 220),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">In practice a calculator or software does the arithmetic. Read the mean and the median, then say what they tell you.</p>',
            64, 470, 1150,
        ),
    ], notes=(
        "Keystrokes if someone asks: STAT 4 to clear L1, STAT EDIT to type, STAT CALC 1-Var Stats. "
        "x-bar is the sample mean. Med is the median. "
        "A sampling distribution is a relative-frequency picture of many sample means. Do not open that chapter today."
    )))
    out.append(quick("Which center?", [
        ("For the town, the better center is",
         [("A", "The mean, $129,400"), ("B", "The median, $30,000"), ("C", "The maximum")],
         "B", "One income of $5,000,000 pulls the mean."),
        ("The mode of the 20 exam scores is 72 because",
         [("A", "It is the middle score"), ("B", "It appears five times"), ("C", "It is the largest")],
         "B", "84 appears three times."),
        ("For 40 ages, the median is located",
         [("A", "At the 20th age"), ("B", "Between the 20th and 21st"), ("C", "At the mean")],
         "B", "(40 + 1) / 2 = 20.5."),
    ], "One right-arrow shows 1B, 2B, 3B. Homework 90 and 91."))
    out.append(closing(
        "Before section 2.6",
        "You can name the center",
        [
            "The mean is the arithmetic average. Outliers pull it.",
            "The median is the middle of the ordered list. Its location is (n + 1) / 2.",
            "The mode is the most common value, and it works for words.",
        ],
        ("2.6 &nbsp; Skewness", "Which center rides the tail."),
        "Practice: OpenStax homework 90 and 91.",
        "Section 2.6 homework is items 92 and 93.",
    ))
    return out


def slides_26():
    out = []
    sym = [("4", 1), ("5", 1), ("6", 3), ("7", 6), ("8", 3), ("9", 1), ("10", 1)]
    left = [("4", 1), ("5", 1), ("6", 3), ("7", 4), ("8", 1)]
    right = [("6", 1), ("7", 4), ("8", 3), ("9", 1), ("10", 1)]
    out.append(opening(
        "Skewness",
        "The mean rides<br>the long tail.",
        "SECTION 2.6",
        drawing(histogram(right, 460, 500, "SKEWED RIGHT"), 760, 110, 460, 500),
        "Three small data sets from the book, each drawn as a histogram of width 1. "
        "Symmetric: mean, median, and mode are all 7. "
        "Left: 6.3, 6.5, and 7. Right: 7.7, 7.5, and 7. The mean moves the most.",
    ))
    out.append(section([
        backdrop(),
        text_block(
            kicker("A symmetric list")
            + title("Mean, median, and mode are all 7", 34),
            64, 12, 1150,
        ),
        drawing(histogram(sym, 1152, 380, "FREQUENCY"), 64, 130, 1152, 380),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            '4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 10. A vertical line at 7 splits this picture into mirror images. '
            'In a perfectly symmetric shape, the mean and the median agree.</p>',
            64, 540, 1150,
        ),
    ], notes=(
        "Sixteen values. Sum 112, mean 7. The 8th and 9th ordered values are both 7, so the median is 7. "
        "Seven appears six times, so the mode is 7. "
        "A symmetric bimodal picture is different: the two modes would not equal the mean and the median."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Skewed left")
            + title("The mean is the smallest of the three", 34),
            64, 12, 1150,
        ),
        drawing(histogram(left, 1152, 380, "THE TAIL POINTS LEFT"), 64, 130, 1152, 380),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            '4, 5, 6, 6, 6, 7, 7, 7, 7, 8. Mean 6.3. Median 6.5. Mode 7. '
            'The right side looks chopped off. The mean is pulled toward the tail.</p>',
            64, 545, 1150,
        ),
    ], notes="Sum of the ten values is 63, so the mean is 6.3. Ordered, the 5th is 6 and the 6th is 7, so the median is 6.5. Seven appears four times."))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Skewed right")
            + title("The mean is the largest of the three", 34),
            64, 12, 1150,
        ),
        drawing(histogram(right, 1152, 380, "THE TAIL POINTS RIGHT"), 64, 130, 1152, 380),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            '6, 7, 7, 7, 7, 8, 8, 8, 9, 10. Mean 7.7. Median 7.5. Mode 7. '
            'The mean reflects the skew more than the median does.</p>',
            64, 545, 1150,
        ),
    ], notes="Sum is 77, mean 7.7. The 5th value is 7 and the 6th is 8, so the median is 7.5. The mode is 7."))
    out.append(section([
        backdrop(),
        text_block(kicker("The pattern") + title("Often, not always"), 72, 36, 1000),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">SKEWED LEFT</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">The mean is often below the median. The tail points left.</p>',
            180,
        ), 64, 190, 360, 180),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">SYMMETRIC</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">The mean and the median are about equal.</p>',
            180,
        ), 452, 190, 370, 180),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">SKEWED RIGHT</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">The mean is often above the median. The tail points right.</p>',
            180,
        ), 850, 190, 360, 180),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">This is not true for every list. The usual exceptions are discrete data. The median stays nearer the high point. The mean rides out on the tail.</p>',
            64, 430, 1150,
        ),
    ], notes=(
        "The next slide is Example 2.31, three students counting letters. The means and medians are already computed. "
        "Ask which tail each list has before you show the labels."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.31 · letters in a word")
            + title("Three students, three tails", 40),
            64, 20, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">TERRY · RIGHT</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;">Mean 3.7. Median 3.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">7, 9, 3, 3, 3, 4, 1, 3, 2, 2. The 9 pulls the mean up.</p>',
            220,
        ), 64, 160, 370, 220),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">DAVIS · LEFT</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;">Mean 2.7. Median 3.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">3, 3, 3, 4, 1, 4, 3, 2, 3, 1. The 1s pull the mean down.</p>',
            220,
        ), 454, 160, 370, 220),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">MARIS · NEARLY EVEN</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;">Mean 4.6. Median 4.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">2, 3, 4, 4, 4, 6, 6, 6, 8, 3. The two centers nearly agree.</p>',
            220,
        ), 844, 160, 370, 220),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">The median stays near the high point of the list. The mean rides out on the tail.</p>',
            64, 430, 1150,
        ),
    ], notes=(
        "Terry sum 37, mean 3.7, median 3. Davis sum 27, mean 2.7, median 3. Maris sum 46, mean 4.6, median 4. "
        "Maris is the roughly symmetric one. Do not make them recompute all three means unless the hour is long."
    )))
    out.append(quick("Name the tail", [
        ("Mean 7.7, median 7.5, mode 7. The shape is",
         [("A", "Skewed left"), ("B", "Symmetric"), ("C", "Skewed right")],
         "C", "The mean is the largest of the three."),
        ("In the symmetric example, the three centers are",
         [("A", "6.3, 6.5, and 7"), ("B", "All 7"), ("C", "7.7, 7.5, and 7")],
         "B", "The picture is a mirror around 7."),
        ("Skewed left often has the mean",
         [("A", "Above the median"), ("B", "Below the median"), ("C", "Equal to the maximum")],
         "B", "The tail pulls the mean left."),
    ], "One right-arrow shows 1C, 2B, 3B. Homework 92 and 93."))
    out.append(closing(
        "Before section 2.7",
        "You can see the tail",
        [
            "Symmetric: the mean and the median agree.",
            "A left tail often pulls the mean below the median.",
            "A right tail often pulls the mean above the median.",
        ],
        ("2.7 &nbsp; Standard deviation", "How far the values sit from the mean."),
        "Practice: OpenStax homework 92 and 93.",
        "Section 2.7 homework is items 94 through 107.",
    ))
    return out


def slides_27():
    out = []
    out.append(opening(
        "Standard<br>deviation",
        "How far the values sit<br>from the mean.",
        "SECTION 2.7",
        drawing(svg_wrap(
            '<rect x="0" y="0" width="460" height="500" rx="18" fill="#ffffff" stroke="#e4e1da"></rect>'
            '<text x="36" y="64" font-size="16" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="700" letter-spacing="1.4">BOTH MEANS ARE 5</text>'
            '<text x="36" y="130" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">Store A</text>'
            '<text x="36" y="180" font-size="42" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">s = 2</text>'
            '<text x="36" y="250" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">Store B</text>'
            '<text x="36" y="300" font-size="42" fill="#2a6f7a" font-family="Montserrat, sans-serif" font-weight="650">s = 4</text>'
            '<text x="36" y="380" font-size="20" fill="#1c242c" font-family="Montserrat, sans-serif">B’s waits vary more.</text>'
            '<text x="36" y="420" font-size="18" fill="#5d6670" font-family="Montserrat, sans-serif">The mean does not say that.</text>',
            460, 500,
        ), 760, 110, 460, 500),
        "Standard deviation is never negative. It is small when the values hug the mean. "
        "In practice, use a calculator. Concentrate on what the number tells you. "
        "Select Sx for a sample and σx for a population.",
    ))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Two supermarkets")
            + title("Same mean, different spread", 40),
            64, 36, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">STORE A</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Mean wait 5 minutes</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:24px;">Standard deviation 2 minutes</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:20px;">The waits sit closer to 5.</p>',
            240,
        ), 64, 190, 560, 240),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">STORE B</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Mean wait 5 minutes</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:24px;">Standard deviation 4 minutes</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:20px;">The waits are more spread out.</p>',
            240,
        ), 656, 190, 560, 240),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">A larger standard deviation means more variation about the mean.</p>',
            64, 480, 1100,
        ),
    ], notes="The book uses minutes at the checkout. Do not invent a list of waits. The given facts are the two means and the two standard deviations."))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Rosa and Binh, both at store A")
            + title("How many standard deviations away?", 34),
            64, 24, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">ROSA WAITS 7 MINUTES</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:28px;font-weight:650;">5 + (1)(2) = 7</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;">One standard deviation above the mean.</p>',
            180,
        ), 64, 170, 560, 180),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">BINH WAITS 1 MINUTE</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:28px;font-weight:650;">5 + (−2)(2) = 1</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;">Two standard deviations below the mean.</p>',
            180,
        ), 656, 170, 560, 180),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'value = mean + (number of standard deviations) × (standard deviation). '
            'Two standard deviations from the mean is a rough flag that a value is far. The shape of the data changes that call.</p>',
            64, 400, 1150,
        ),
    ], notes=(
        "The number of standard deviations need not be a whole number. "
        "For a sample the symbols are x-bar and s. For a population they are μ and σ. "
        "The empirical rule, about 95% within two standard deviations for a bell shape, comes later. "
        "Do not teach it as a fact for every shape."
    )))
    out.append(section([
        backdrop(),
        text_block(kicker("Sample or population") + title("Divide by n − 1, or by N"), 64, 28, 1100),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">SAMPLE</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:26px;line-height:1.35;">The variance divides by n − 1. The standard deviation is s. On a calculator, read Sx.</p>',
            200,
        ), 64, 180, 560, 200),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:18px;font-weight:700;">POPULATION</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:26px;line-height:1.35;">The variance divides by N. The standard deviation is σ. On a calculator, read σx.</p>',
            200,
        ), 656, 180, 560, 200),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The deviations from the mean add to zero, so the calculation squares them. '
            'Dividing a sample by n − 1 estimates the population variance better than dividing by n. Let the calculator do that arithmetic.</p>',
            64, 430, 1150,
        ),
    ], notes=(
        "Variance is in squared units. The standard deviation is the square root, back in the units of the data. "
        "s estimates σ when the sample looks like the population. "
        "The next slide is the keystroke list. Walk it once with a short list before Example 2.32."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("On the calculator")
            + title("Let it do the arithmetic", 40),
            64, 24, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">1 · ENTER THE LIST</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">STAT, then EDIT. Clear L1. Type one value per row.</p>',
            150,
        ), 64, 160, 560, 150),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">2 · ONE-VARIABLE STATS</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">STAT, CALC, 1-Var Stats, then Calculate.</p>',
            150,
        ), 656, 160, 560, 150),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">3 · READ THE RIGHT LINE</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">x̄ is the mean. Sx is the sample standard deviation. σx is the population one.</p>',
            150,
        ), 64, 340, 1150, 150),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">Keep the calculator’s Sx unrounded while you still have steps to do. Round the final answer.</p>',
            64, 530, 1150,
        ),
    ], notes=(
        "TI-83 or TI-84. To clear a list: put the cursor on L1, CLEAR, ENTER. "
        "STAT 4 is ClrList if someone asks. A phone calculator is enough for a mean. "
        "Standard deviation is the reason the graphing calculator comes out today."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.32 · a sample of 20 fifth-graders")
            + title("Mean 10.53 years, s = 0.72", 34),
            64, 20, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">One standard deviation above</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">10.53 + 0.72 = 11.25</p>',
            140,
        ), 64, 170, 560, 140),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Two standard deviations below</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">10.53 − 1.44 = 9.09</p>',
            140,
        ), 656, 170, 560, 140),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The ages are a sample, so the variance divides by 19, not by 20. '
            'The standard deviation is zero only when every age is the same. A small standard deviation means the ages hug 10.53.</p>',
            64, 360, 1150,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'Graph first. For a skewed picture, the five-number summary is more useful than the standard deviation, because the two tails do not have the same spread.</p>',
            64, 500, 1150,
        ),
    ], notes=(
        "Ages: 9 once, 9.5 twice, 10 four times, 10.5 four times, 11 six times, 11.5 three times. n = 20. "
        "The deviation table uses the mean 10.525. The book then rounds the average to 10.53. "
        "Sum of f times squared deviations is 9.7375. Sample variance is 9.7375 / 19. "
        "s = 0.72 to two decimals. The calculator’s Sx is about 0.715891. Use that unrounded value for further steps, then check the book’s rounded lines: "
        "plus 1s is 11.25, minus 2s is 9.09, and plus or minus 1.5s is 11.61 and 9.45. "
        "The next slides reuse Monday’s 31 exam scores, then Try It 2.32, the baseball ages. "
        "Have them enter the ages. Do not compute s by hand."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 2.33 · the same 31 exam scores")
            + title("Monday’s list, on the calculator", 36),
            64, 20, 1150,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Center</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:26px;font-weight:650;">Mean 73.5 · median 73</p>',
            120,
        ), 64, 155, 560, 120),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Spread</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:26px;font-weight:650;">s = 17.9 · IQR = 29</p>',
            120,
        ), 656, 155, 560, 120),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">The five numbers</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:26px;font-weight:650;">33 · 61 · 73 · 90 · 100</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:18px;">Minimum, Q1, median, Q3, maximum.</p>',
            130,
        ), 64, 300, 1150, 130),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The lower half spreads more: 73 − 33 = 40 points. The upper half spreads 100 − 73 = 27. '
            'That is the long left whisker from the box plot. s = 17.9 says a typical score sits about 18 points from 73.5.</p>',
            64, 470, 1150,
        ),
    ], notes=(
        "Scores: 33, 42, 49, 49, 53, 55, 55, 61, 63, 67, 68, 68, 69, 69, 72, 73, 74, 78, 80, 83, 88, 88, 88, 90, 92, 94, 94, 94, 94, 96, 100. "
        "Unrounded mean is about 73.52 and Sx is about 17.92. The book rounds to 73.5 and 17.9. Q1 is 61 and Q3 is 90, so the IQR is 29."
    )))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.32 · your turn")
            + title("Twenty-five baseball ages", 40)
            + '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.45;">'
            '21, 21, 22, 23, 24, 24, 25, 25, 28, 29, 29, 31, 32,<br>'
            '33, 33, 34, 35, 36, 36, 36, 36, 38, 38, 38, 40</p>'
            + '<p style="margin:16px 0 0;color:#5d6670;font-size:22px;">'
            'Use the calculator. Find the mean, Sx, and the age two standard deviations above the mean.</p>',
            64, 70, 1120,
        ),
        text_block(
            card_shell(
                '<p style="margin:0;color:#2a6f7a;font-size:16px;font-weight:700;">PAUSE</p>'
                '<p style="margin:10px 0 0;color:#1c242c;font-size:24px;">Clear L1 first. Read x̄ and Sx. Then compute x̄ + 2 Sx with the unrounded Sx.</p>',
                120,
            ),
            64, 470, 1120, 120,
        ),
    ], notes="n = 25. Sum is 767. Give them about five minutes to type the list and read the screen."))
    out.append(section([
        backdrop(),
        text_block(
            kicker("Try It 2.32")
            + title("Two standard deviations above is 42.9", 34),
            64, 28, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">From 1-Var Stats</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">x̄ = 30.68 &nbsp;&nbsp; Sx = 6.09</p>',
            140,
        ), 64, 160, 1150, 140),
        text_block(card_shell(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Two standard deviations above the mean</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">30.68 + 2(6.09) = 42.86</p>',
            140,
        ), 64, 320, 1150, 140),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'Nobody on the team is 42.9 years old. The oldest player is 40. '
            'The standard deviation describes the spread. It does not invent a player.</p>',
            64, 500, 1150,
        ),
    ], notes=(
        "Sx to more places is about 6.0945, so two standard deviations above is about 42.87. "
        "The slide uses the two-decimal readings 30.68 and 6.09. "
        "40 is (40 − 30.68) / 6.09 ≈ 1.5 standard deviations above the mean, if someone asks."
    )))
    out.append(quick("Read the spread", [
        ("Store B’s waits vary more because",
         [("A", "The mean is larger"), ("B", "The standard deviation is 4"), ("C", "The range is zero")],
         "B", "Both means are 5 minutes."),
        ("Rosa’s wait of 7 minutes is",
         [("A", "One SD above the mean"), ("B", "Two SDs below the mean"), ("C", "The mean itself")],
         "A", "5 + 1 × 2 = 7."),
        ("For a sample, the calculator reading is",
         [("A", "Sx, divide by n − 1"), ("B", "σx, divide by N"), ("C", "The range")],
         "A", "σx is the population standard deviation."),
    ], "One right-arrow shows 1B, 2A, 3A. Homework 94 through 107. The chapter review starts at 108."))
    out.append(quick("Before Friday", [
        ("The salary of $120,000 is",
         [("A", "The median"), ("B", "A potential outlier"), ("C", "Below the fence")],
         "B", "The fence is $111,750."),
        ("For the 60 houses, the better center is",
         [("A", "The mean, $334,500"), ("B", "The median, $315,000"), ("C", "The $2,500,000 house")],
         "B", "One house pulls the mean up."),
        ("For the 31 exam scores, 17.9 is",
         [("A", "The mean"), ("B", "The sample standard deviation"), ("C", "The IQR")],
         "B", "The mean is 73.5. The IQR is 29."),
    ], "One right-arrow shows 1B, 2B, 3B. This reviews Tuesday, Wednesday, and today before the Friday deadline."))
    out.append(closing(
        "End of Unit 2",
        "You can describe a list",
        [
            "Graph it first: a stemplot, a histogram, or a box.",
            "Then name the center, and say whether a tail is pulling the mean.",
            "The standard deviation says how far the values sit from that mean.",
        ],
        ("Unit 3 &nbsp; Regression", "November 7–9. Sections 12.1–12.3 and 12.5."),
        "Practice: OpenStax homework 94 through 107.",
        "Exam 1 is November 10 and 11 and covers Units 1, 2, and 3. "
        "Item 108 begins the chapter review. Do not start it as if it were a new section.",
    ))
    return out


SHELL = """<!DOCTYPE html>
<html class="sl-root decks export offline loaded">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover, minimal-ui">
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="lib/offline-v2.css">
</head>
<body class="reveal-viewport theme-font-montserrat theme-color-white-blue">
<div class="reveal"><div class="slides">
{slides}
</div></div>
<script>
var SLConfig = {{"deck": {{"slug": "{slug}", "title": "{title}", "description": "{description}", "width": 1280, "height": 720, "margin": 0.05, "theme_font": "montserrat", "theme_color": "white-blue", "center": false, "transition": "slide", "background_transition": "slide", "slide_count": {count}, "version": 2, "rtl": false, "should_loop": false, "shuffle": false, "navigation_mode": "default", "language": "en", "font_typekit": null, "font_google": null, "notes": {{}}}}}};
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


DECKS = [
    ("2.2-histograms", "math117-2-2-histograms", "MATH 117 · 2.2 Histograms",
     "Histograms, frequency polygons, and time series.", slides_22),
    ("2.3-location", "math117-2-3-location", "MATH 117 · 2.3 Quartiles",
     "Percentiles, quartiles, and the IQR.", slides_23),
    ("2.4-boxplots", "math117-2-4-boxplots", "MATH 117 · 2.4 Box plots",
     "The five-number summary as a picture.", slides_24),
    ("2.5-center", "math117-2-5-center", "MATH 117 · 2.5 Center",
     "Mean, median, and mode.", slides_25),
    ("2.6-skewness", "math117-2-6-skewness", "MATH 117 · 2.6 Skewness",
     "How the mean rides the tail.", slides_26),
    ("2.7-spread", "math117-2-7-spread", "MATH 117 · 2.7 Standard deviation",
     "How far the values sit from the mean.", slides_27),
]


def write_deck(folder, slug, page_title, description, builder):
    out = ROOT / folder
    zip_path = ROOT / f"{folder}-slides.zip"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SAMPLE / "lib", out / "lib", ignore=shutil.ignore_patterns(".DS_Store"))
    parts = builder()
    html = SHELL.format(
        title=page_title,
        slug=slug,
        description=description,
        slides="\n".join(parts),
        count=len(parts),
    )
    if "2696400" in html:
        raise SystemExit(f"{folder} still contains a Slides.com user id")
    asset = out / slug
    asset.mkdir()
    (asset / "mark.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 8">'
        '<circle cx="4" cy="4" r="3" fill="#2a6f7a"></circle></svg>\n'
    )
    html = html.replace(
        "</section>",
        f'<img alt="" data-src="{slug}/mark.svg" '
        f'style="width:1px;height:1px;position:absolute;left:0;top:0;opacity:0;"></section>',
        1,
    )
    (out / "index.html").write_text(html)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        dirs = sorted({p.parent.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()})
        for folder_name in dirs:
            if folder_name not in ("", "."):
                zf.writestr(zipfile.ZipInfo(folder_name + "/"), "")
        for path in sorted(out.rglob("*")):
            if path.name == ".DS_Store" or not path.is_file():
                continue
            zf.write(path, path.relative_to(out).as_posix())
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
    tops = sorted({n.split("/")[0] for n in names})
    print(f"{folder}: {len(parts)} slides, zip tops {tops}")


def main():
    if not SAMPLE.is_dir():
        raise SystemExit(f"missing sample export: {SAMPLE}")
    for folder, slug, page_title, description, builder in DECKS:
        write_deck(folder, slug, page_title, description, builder)


if __name__ == "__main__":
    main()
