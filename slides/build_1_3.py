"""Section 1.3 as a Slides.com HTML export.

Levels of measurement, then a frequency table you can read.
Open index.html, or upload the zip. Day 2 shares the hour with section 1.4.
"""

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE = Path("/Users/mac-mini/Downloads/slides_deck-8187f8-2")
OUT = ROOT / "1.3-frequency"
ZIP_PATH = ROOT / "1.3-frequency-slides.zip"
SLUG = "math117-1-3-frequency"

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


def data_table(headers, rows):
    ths = "".join(
        '<th style="text-align:left;background:#2a6f7a;color:#ffffff;font-size:16px;'
        f'font-weight:650;padding:12px 16px;">{header}</th>'
        for header in headers
    )
    body = []
    for index, row in enumerate(rows):
        bg = "#ffffff" if index % 2 == 0 else "#f3f8f7"
        cells = "".join(
            f'<td style="padding:10px 16px;border-bottom:1px solid #e4e1da;font-size:20px;'
            f'color:#1c242c;background:{bg};">{value}</td>'
            for value in row
        )
        body.append(f"<tr>{cells}</tr>")
    return (
        '<div style="border:1px solid #d5ddd9;border-radius:14px;overflow:hidden;">'
        '<table style="width:100%;border-collapse:collapse;">'
        f'<thead><tr>{ths}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
    )


def bar_chart(labels, heights, max_height, touch=False):
    plot_h = 220
    scale = plot_h / max_height
    n = len(labels)
    usable = 1000
    left = 76
    gap = 0 if touch else 18
    width = usable / n if touch else (usable - gap * (n - 1)) / n
    base = 292
    stroke = ' stroke="#ffffff" stroke-width="2"' if touch else ""
    radius = 0 if touch else 6
    parts = [
        '<rect x="0" y="0" width="1152" height="380" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<line x1="60" y1="{base}" x2="1100" y2="{base}" stroke="#1c242c" stroke-width="1.6"></line>',
    ]
    for i, (label, value) in enumerate(zip(labels, heights)):
        h = max(value * scale, 8)
        x = left + i * (width + gap)
        y = base - h
        label_y = min(y - 10, base - 26)
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{h:.1f}" rx="{radius}" '
            f'fill="#2a6f7a"{stroke}></rect>'
        )
        parts.append(
            f'<text x="{x + width / 2:.1f}" y="{label_y:.1f}" text-anchor="middle" font-size="16" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{value}</text>'
        )
        parts.append(
            f'<text x="{x + width / 2:.1f}" y="{base + 28}" text-anchor="middle" font-size="16" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{label}</text>'
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 380">'
        + "".join(parts) + "</svg>"
    )
    return drawing(svg, 64, 155, 1152, 380)


def title_visual():
    heights = [3, 5, 3, 6, 2, 1]
    labels = ["2", "3", "4", "5", "6", "7"]
    scale = 28
    parts = []
    for i, (label, value) in enumerate(zip(labels, heights)):
        h = value * scale
        x = 48 + i * 64
        y = 300 - h
        parts.append(f'<rect x="{x}" y="{y}" width="46" height="{h}" rx="6" fill="#2a6f7a"></rect>')
        parts.append(
            f'<text x="{x + 23}" y="{y - 10}" text-anchor="middle" font-size="16" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif" font-weight="650">{value}</text>'
        )
        parts.append(
            f'<text x="{x + 23}" y="328" text-anchor="middle" font-size="16" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{label}</text>'
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 460 500">'
        '<rect x="8" y="8" width="444" height="484" rx="22" fill="#ffffff" stroke="#e4e1da" stroke-width="1.6"></rect>'
        '<text x="36" y="52" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        'font-weight="700" letter-spacing="1.6">TWENTY STUDENTS</text>'
        '<line x1="36" y1="300" x2="424" y2="300" stroke="#1c242c" stroke-width="1.6"></line>'
        + "".join(parts)
        + '<text x="36" y="400" font-size="22" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">Hours worked</text>'
        '<text x="36" y="436" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">The tall bar is 5 hours, six students.</text>'
        '</svg>'
    )
    return drawing(svg, 760, 110, 460, 500)


def slides():
    out = []
    out.append(section([
        backdrop(),
        text_block(
            '<p style="margin:0;">'
            '<span style="color:#ffffff;background:#2a6f7a;padding:6px 12px;'
            'letter-spacing:0.12em;font-weight:700;font-size:16px;">MATH 117</span>'
            '<span style="color:#5d6670;font-size:20px;"> &nbsp; Unit 1 · Sampling and Data</span></p>',
            72, 150, 640,
        ),
        text_block(
            '<h1 style="margin:0;color:#1c242c;font-size:64px;line-height:0.98;font-weight:650;'
            'letter-spacing:-0.04em;">Frequency<br>tables</h1>'
            '<p style="margin:22px 0 0;color:#1c242c;font-size:26px;line-height:1.3;">'
            'How the data are measured,<br>and how often each value shows up</p>'
            '<p style="margin:18px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;letter-spacing:0.08em;">SECTION 1.3</p>',
            72, 214, 640,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 540, 560,
        ),
        title_visual(),
    ], notes="Day 2, first half. About 40 minutes, then section 1.4. Blackboard calls the tables learning outcome 1.5. The four levels are learning outcome 1.3."))

    out.append(section([
        backdrop(),
        text_block(kicker("Section 1.3") + title("Two jobs"), 72, 48, 1000),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:22px;font-weight:650;">01</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Name the level</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Nominal, ordinal, interval, or ratio. The level decides what arithmetic is allowed.</p>',
            230,
        ), 72, 200, 540, 230),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:22px;font-weight:650;">02</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Read the table</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Frequency, relative frequency, and cumulative relative frequency.</p>',
            230,
        ), 656, 200, 540, 230),
    ]))

    levels = [
        ("1", "Nominal", "Names. No order. Favorite food, or a yes/no answer. You cannot calculate with them."),
        ("2", "Ordinal", "An order, and no measured gap. Excellent, good, satisfactory, unsatisfactory."),
        ("3", "Interval", "Differences make sense. Zero is not “none.” 100°F is 60° more than 40°F. 0°F is not the absence of heat."),
        ("4", "Ratio", "A true zero, so ratios make sense. Scores 80 and 20. Zero means no points. 80 is four times 20."),
    ]
    rows = []
    for num, name, text in levels:
        rows.append(
            '<div style="display:flex;align-items:center;gap:16px;background:#ffffff;'
            'border:1px solid #e4e1da;border-radius:16px;padding:14px 18px;margin-bottom:12px;">'
            f'{letter_badge(num)}'
            f'<div style="width:150px;color:#1c242c;font-size:22px;font-weight:650;flex:none;">{name}</div>'
            f'<div style="color:#5d6670;font-size:18px;line-height:1.3;">{text}</div>'
            '</div>'
        )
    out.append(section([
        backdrop(),
        text_block(kicker("Levels of measurement") + title("From names up to ratios", 40), 64, 24, 1000),
        text_block("".join(rows), 64, 140, 1152),
    ], notes="Nominal and ordinal cannot be used in calculations. Interval has meaningful differences. Ratio has a real zero. Exam scores in the book are 80, 68, 20, and 92. 80 is four times 20."))

    prompts = [
        ("a", "Smartphone brand"),
        ("b", "Rank of the top five national parks"),
        ("c", "Temperature in Celsius"),
        ("d", "Hours a student works in a day"),
    ]
    out.append(section([
        backdrop(),
        text_block(
            kicker("Your turn")
            + title("Name the level", 44)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">Nominal, ordinal, interval, or ratio.</p>',
            64, 36, 1000,
        ),
        text_block("".join(f'<div style="margin-top:12px;">{choice(letter, text)}</div>' for letter, text in prompts), 64, 220, 800),
    ], notes="Answers: a nominal, b ordinal, c interval, d ratio. Parks can be ranked. The gap between rank 1 and rank 2 is not a measurement."))

    answers = [
        ("a", "Nominal", "A brand is a name. There is no agreed order."),
        ("b", "Ordinal", "The parks are ranked. The gap between ranks is not a size."),
        ("c", "Interval", "Degrees can be subtracted. Zero Celsius is not “no temperature.”"),
        ("d", "Ratio", "Zero hours means no work. Six hours is three times two hours."),
    ]
    answer_rows = []
    for letter, name, text in answers:
        answer_rows.append(
            '<div style="display:flex;align-items:center;gap:16px;background:#ffffff;'
            'border:1px solid #e4e1da;border-radius:14px;padding:12px 16px;margin-bottom:10px;">'
            f'{letter_badge(letter, filled=True)}'
            f'<div style="width:160px;color:#1c242c;font-size:22px;font-weight:650;flex:none;">{name}</div>'
            f'<div style="color:#5d6670;font-size:20px;">{text}</div></div>'
        )
    out.append(section([
        backdrop(),
        text_block(kicker("Your turn") + title("Four levels", 40), 64, 28, 800),
        text_block("".join(answer_rows), 64, 140, 1152),
    ]))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Twenty students")
            + title("Hours worked in a day", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Each bar is how many students gave that answer. The counts add to 20.</p>',
            64, 20, 1150,
        ),
        bar_chart(["2", "3", "4", "5", "6", "7"], [3, 5, 3, 6, 2, 1], 6),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">Table 1.10. Frequency means how many times that value appears.</p>',
            64, 600, 1100,
        ),
    ], notes="Data: 5, 6, 3, 3, 2, 4, 7, 5, 2, 3, 5, 6, 5, 4, 4, 3, 5, 2, 5, 3. Counts: 2 hours three students, 3 hours five, 4 hours three, 5 hours six, 6 hours two, 7 hours one."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Table 1.12")
            + title("Three columns", 40)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Relative frequency is the count divided by 20. Cumulative adds those shares as you go down.</p>',
            64, 18, 1150,
        ),
        text_block(data_table(
            ["Hours", "Frequency", "Relative", "Cumulative"],
            [
                ["2", "3", "0.15", "0.15"],
                ["3", "5", "0.25", "0.40"],
                ["4", "3", "0.15", "0.55"],
                ["5", "6", "0.30", "0.85"],
                ["6", "2", "0.10", "0.95"],
                ["7", "1", "0.05", "1.00"],
            ],
        ), 64, 150, 1152),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">0.55 means 55% work 4 hours or fewer. The last cumulative entry is 1.</p>',
            64, 580, 1150,
        ),
    ], notes="Rounding rule, if it comes up: the final answer goes one decimal past the data. (4+6+9)/3 = 6.3. Do not round the steps in the middle. Relative frequencies may miss 1 by a rounding hair. They should be close."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Table 1.13 · grouped")
            + title("Heights of 100 soccer players", 36)
            + '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;">'
            'Each bar is a two-inch interval. The tall bar is 66 to 68 inches, 40 players.</p>',
            64, 18, 1150,
        ),
        bar_chart(["60", "62", "64", "66", "68", "70", "72", "74"], [5, 3, 15, 40, 17, 12, 7, 1], 40, touch=True),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'Shorter than 65.95 inches is the first three bars: 5 + 3 + 15 = 23%.</p>',
            64, 600, 1150,
        ),
    ], notes="Example 1.14. 23% is the cumulative relative frequency in the third row. Example 1.15: between 61.95 and 65.95 inches is 0.03 + 0.15 = 18%. Heights are quantitative continuous."))

    levels_q = [("A", "Nominal"), ("B", "Ordinal"), ("C", "Interval"), ("D", "Ratio")]
    read_q = [
        ("A", "55% work exactly 4 hours"),
        ("B", "55% work 4 hours or fewer"),
        ("C", "55% work more than 4 hours"),
    ]

    def question_block(number, prompt, pairs, answer, why):
        return (
            f'<p style="margin:0 0 4px;color:#1c242c;font-size:22px;font-weight:650;">{number} &nbsp; {prompt}</p>'
            f'{choice_stack(pairs, answer, reveal=True)}'
            f'{reveal_line(why)}'
        )

    out.append(section([
        backdrop(),
        text_block(kicker("Quick check") + title("Name it, then read it", 36), 64, 18, 1100),
        text_block(question_block(
            "1", "Excellent down to unsatisfactory", levels_q, "B", "The words have an order.",
        ), 64, 118, 540),
        text_block(question_block(
            "2", "An exam score out of 100", levels_q, "D", "Zero means no points.",
        ), 680, 118, 540),
        text_block(question_block(
            "3", "Cumulative 0.55 means", read_q, "B", "It counts 4 hours and everyone below.",
        ), 64, 470, 900),
    ], notes="One right-arrow shows every answer: 1B ordinal, 2D ratio, 3B. Arrow again leaves the slide. Cumulative relative frequency counts that value and every value below it."))

    out.append(section([
        backdrop(),
        text_block(kicker("Still today") + title("You can name the level<br>and read the table", 44), 72, 70, 1100),
        text_block(
            '<p style="margin:0 0 12px;color:#1c242c;font-size:26px;">Nominal, ordinal, interval, ratio.</p>'
            '<p style="margin:0;color:#1c242c;font-size:26px;">Frequency, relative frequency, cumulative relative frequency.</p>',
            72, 260, 1000,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">NEXT, SAME DAY</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:28px;font-weight:650;">1.4 &nbsp; Experimental design and ethics</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">An observational study, or an experiment that assigns the treatment.</p>',
            140,
        ), 72, 420, 980, 140),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Practice: OpenStax homework 80–86.</p>',
            72, 600, 800,
        ),
    ], notes="Homework 80–86. 80 and 81 are incomplete frequency tables. 85 and 86 read a hurricane table."))

    return out


SHELL = """<!DOCTYPE html>
<html class="sl-root decks export offline loaded">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover, minimal-ui">
<meta charset="utf-8">
<title>MATH 117 · 1.3 Frequency tables</title>
<link rel="stylesheet" type="text/css" href="lib/offline-v2.css">
</head>
<body class="reveal-viewport theme-font-montserrat theme-color-white-blue">
<div class="reveal"><div class="slides">
{slides}
</div></div>
<script>
var SLConfig = {{"deck": {{"slug": "math117-1-3-frequency", "title": "MATH 117 · 1.3 Frequency tables", "description": "Levels of measurement and frequency tables.", "width": 1280, "height": 720, "margin": 0.05, "theme_font": "montserrat", "theme_color": "white-blue", "center": false, "transition": "slide", "background_transition": "slide", "slide_count": {count}, "version": 2, "rtl": false, "should_loop": false, "shuffle": false, "navigation_mode": "default", "language": "en", "font_typekit": null, "font_google": null, "notes": {{}}}}}};
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
