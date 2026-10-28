"""Section 1.4 as a Slides.com HTML export.

Observational studies, randomized experiments, and ethics.
Open index.html, or upload the zip. Shares the day with section 1.3.
"""

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE = Path("/Users/mac-mini/Downloads/slides_deck-8187f8-2")
OUT = ROOT / "1.4-experiments"
ZIP_PATH = ROOT / "1.4-experiments-slides.zip"
SLUG = "math117-1-4-experiments"

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


def dot_row(x, y, n, fill, stroke=None):
    parts = []
    extra = f' stroke="{stroke}" stroke-width="1.6"' if stroke else ""
    for i in range(n):
        parts.append(f'<circle cx="{x + i * 28}" cy="{y}" r="10" fill="{fill}"{extra}></circle>')
    return "".join(parts)


def study_picture():
    left = (
        '<text x="36" y="48" font-size="15" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        'font-weight="700" letter-spacing="2">OBSERVATIONAL</text>'
        '<text x="36" y="86" font-size="26" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">'
        'The groups already exist</text>'
        '<text x="36" y="140" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">Takes vitamin E</text>'
        + dot_row(36, 172, 8, "#2a6f7a")
        + '<text x="36" y="220" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">Does not</text>'
        + dot_row(36, 252, 8, "#d5e0de")
        + '<text x="36" y="320" font-size="18" fill="#1c242c" font-family="Montserrat, sans-serif">'
        'Diet, exercise, and smoking differ too.</text>'
    )
    right = (
        '<text x="610" y="48" font-size="15" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        'font-weight="700" letter-spacing="2">EXPERIMENT</text>'
        '<text x="610" y="86" font-size="26" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">'
        'The researcher assigns the pill</text>'
        '<text x="610" y="140" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">Aspirin</text>'
        + dot_row(610, 172, 8, "#2a6f7a")
        + '<text x="610" y="220" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">Placebo</text>'
        + dot_row(610, 252, 8, "#d7ebe8", "#2a6f7a")
        + '<text x="610" y="320" font-size="18" fill="#1c242c" font-family="Montserrat, sans-serif">'
        'The only planned difference is the pill.</text>'
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1152 370">'
        '<rect x="0" y="0" width="1152" height="370" rx="18" fill="#ffffff" stroke="#e4e1da" stroke-width="1.4"></rect>'
        '<line x1="576" y1="28" x2="576" y2="342" stroke="#e4e1da" stroke-width="1.4"></line>'
        + left + right + "</svg>"
    )
    return drawing(svg, 64, 150, 1152, 370)


def title_visual():
    def row(x, y, n, fill, stroke=None):
        extra = f' stroke="{stroke}" stroke-width="1.8"' if stroke else ""
        return "".join(
            f'<circle cx="{x + i * 48}" cy="{y}" r="12" fill="{fill}"{extra}></circle>'
            for i in range(n)
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 460 500">'
        '<rect x="8" y="8" width="444" height="484" rx="22" fill="#ffffff" stroke="#e4e1da" stroke-width="1.6"></rect>'
        '<text x="36" y="52" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        'font-weight="700" letter-spacing="1.6">ASSIGNED AT RANDOM</text>'
        '<text x="36" y="150" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">Aspirin</text>'
        + row(36, 186, 8, "#2a6f7a")
        + '<text x="36" y="246" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">Placebo</text>'
        + row(36, 282, 8, "#d7ebe8", "#2a6f7a")
        + '<text x="36" y="380" font-size="22" fill="#1c242c" font-family="Montserrat, sans-serif" font-weight="650">Same people. One difference.</text>'
        '<text x="36" y="418" font-size="16" fill="#5d6670" font-family="Montserrat, sans-serif">The pill is the only planned change.</text>'
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
            '<h1 style="margin:0;color:#1c242c;font-size:60px;line-height:0.98;font-weight:650;'
            'letter-spacing:-0.04em;">Experiments<br>and ethics</h1>'
            '<p style="margin:22px 0 0;color:#1c242c;font-size:26px;line-height:1.3;">'
            'Who already belongs to the group,<br>and who gets assigned</p>'
            '<p style="margin:18px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;letter-spacing:0.08em;">SECTION 1.4</p>',
            72, 214, 640,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 540, 560,
        ),
        title_visual(),
    ], notes="Day 2, second half. Blackboard learning outcome 1.6: observational study versus experiment. About 35 minutes."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Section 1.4")
            + title("Same health difference, two studies", 36),
            64, 24, 1100,
        ),
        study_picture(),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'Random assignment spreads diet, exercise, and smoking across both groups.</p>',
            64, 560, 1150,
        ),
    ], notes="An observational study compares groups that already exist. An experiment assigns the treatment at random, so lurking variables are spread across the groups. Only then can a difference in the response be tied to the treatment."))

    words = [
        ("Explanatory", "The variable the researcher sets. Here, which pill."),
        ("Response", "What gets measured afterward. A heart attack, yes or no."),
        ("Treatments", "The values of the explanatory variable. Aspirin, and a placebo."),
        ("Experimental unit", "One person, or one object, that gets measured."),
        ("Lurking variable", "Something else that differs between the groups and can explain the result."),
    ]
    rows = []
    for name, text in words:
        rows.append(
            '<div style="display:flex;align-items:center;gap:16px;background:#ffffff;'
            'border:1px solid #e4e1da;border-radius:16px;padding:12px 18px;margin-bottom:10px;">'
            f'<div style="width:250px;color:#1c242c;font-size:22px;font-weight:650;flex:none;">{name}</div>'
            f'<div style="color:#5d6670;font-size:20px;line-height:1.3;">{text}</div></div>'
        )
    out.append(section([
        backdrop(),
        text_block(kicker("The words") + title("What an experiment names", 40), 64, 22, 1000),
        text_block("".join(rows), 64, 140, 1152),
    ]))

    blind = [
        ("Placebo", "Looks like the treatment. It cannot itself change the response."),
        ("Control group", "Gets the placebo, so being in the study is the same for everyone."),
        ("Blinding", "The person does not know who received the active treatment."),
        ("Double-blind", "The subjects and the researchers who meet them are both blinded."),
    ]
    cards = []
    for name, text in blind:
        cards.append(
            '<div style="background:#ffffff;border:1px solid #e4e1da;border-radius:18px;'
            'padding:20px 22px;height:150px;box-sizing:border-box;">'
            f'<p style="margin:0;color:#1c242c;font-size:24px;font-weight:650;">{name}</p>'
            f'<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">{text}</p></div>'
        )
    grid = (
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">{"".join(cards)}</div>'
    )
    out.append(section([
        backdrop(),
        text_block(
            kicker("The power of suggestion")
            + title("A pill can work because you expect it to", 34)
            + '<p style="margin:8px 0 0;color:#5d6670;font-size:18px;">'
            'Believing you had taken a performance drug produced times almost as fast as actually taking it.</p>',
            64, 20, 1150,
        ),
        text_block(grid, 64, 200, 1152),
    ], notes="McClung and Collins, 2007, quoted in the section. Taking the drug without knowing produced no significant gain. Blinding keeps that expectation equal in both groups. If people know they got the empty pill, suggestion drops out."))

    facts = [
        ("Population", "People aged 50 to 84"),
        ("Sample", "The 400 who joined"),
        ("Experimental unit", "One person"),
        ("Explanatory", "Oral medication"),
        ("Treatments", "Aspirin or a placebo"),
        ("Response", "A heart attack, yes or no"),
    ]
    cells = []
    for label, value in facts:
        cells.append(
            '<div style="background:#ffffff;border:1px solid #e4e1da;border-radius:16px;'
            'padding:16px 18px;height:120px;box-sizing:border-box;">'
            f'<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">{label}</p>'
            f'<p style="margin:10px 0 0;color:#1c242c;font-size:24px;font-weight:650;line-height:1.2;">{value}</p></div>'
        )
    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.19")
            + title("Does aspirin reduce heart attacks?", 36),
            64, 20, 1100,
        ),
        text_block(
            f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">{"".join(cells)}</div>',
            64, 150, 1152,
        ),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">One pill a day for three years. They do not know which pill. The subjects are blinded.</p>',
            64, 560, 1150,
        ),
    ], notes="The book’s response variable is whether a subject had a heart attack. Researchers count how many in each group. Try It 1.19, medicines A, B, and C and adult height, is the same six labels if you want a second pass. Height will not change in six months. That is a useful aside, not a slide."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.20")
            + title("Can a scent change the time?", 40),
            64, 28, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.1em;">EXPLANATORY</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">The scent of the mask</p>',
            150,
        ), 64, 170, 540, 150),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.1em;">RESPONSE</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Time to finish the maze</p>',
            150,
        ), 640, 170, 540, 150),
        text_block(card_shell(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'Treatments: a floral mask and an unscented mask. Everyone wears both, in a random order.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'Subjects can smell the flowers, so they cannot be blinded. The person with the stopwatch can be.</p>',
            180,
        ), 64, 350, 1116, 180),
    ], notes="Random order spreads any practice effect. Lurking variables are not a group difference here, because every subject gets both treatments. Researchers timing the maze can be blinded. Subjects cannot."))

    out.append(section([
        backdrop(),
        text_block(
            kicker("Example 1.21")
            + title("Birth order cannot be assigned", 40),
            64, 48, 1100,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#1c242c;font-size:28px;line-height:1.35;font-weight:650;">'
            'You cannot hand someone a birth order.</p>'
            '<p style="margin:18px 0 0;color:#5d6670;font-size:24px;line-height:1.4;">'
            'First-born and later-born children already differ in other ways. Those differences stay mixed in. The study stays observational.</p>',
            240,
        ), 64, 200, 1152, 240),
    ], notes="When random assignment is impossible, a response difference cannot be pinned on the explanatory variable alone. Texting and driving, Try It 1.21, can be an experiment: you can assign who texts."))

    ethics = [
        ("a", "A comfortable block", "A convenient sample can be biased. It does not stand for the community."),
        ("b", "Skipped empty houses", "People who are at work never get counted. Relevant data is missing."),
        ("c", "Filled in the forms later", "Copying other residents’ answers is faking data. That is never acceptable."),
    ]
    ethics_rows = []
    for letter, name, text in ethics:
        ethics_rows.append(
            '<div style="display:flex;align-items:center;gap:16px;background:#ffffff;'
            'border:1px solid #e4e1da;border-radius:16px;padding:14px 18px;margin-bottom:12px;">'
            f'{letter_badge(letter)}'
            f'<div style="width:280px;color:#1c242c;font-size:22px;font-weight:650;flex:none;">{name}</div>'
            f'<div style="color:#5d6670;font-size:20px;line-height:1.3;">{text}</div></div>'
        )
    out.append(section([
        backdrop(),
        text_block(kicker("Example 1.22") + title("Three ways to spoil the data", 40), 64, 22, 1000),
        text_block("".join(ethics_rows), 64, 150, 1152),
        text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'Human subjects need informed consent, in writing. An institutional review board approves the study before it starts.</p>',
            64, 560, 1150,
        ),
    ], notes="Stapel, for you only if a student asks: he created data sets, altered data, and misreported how many subjects he had. More than 55 papers. Do not make that a slide. IRB: risks minimized and reasonable against the benefits, consent documented, individual data kept private."))

    def question_block(number, prompt, pairs, answer, why):
        return (
            f'<p style="margin:0 0 8px;min-height:56px;color:#1c242c;font-size:22px;font-weight:650;line-height:1.25;">{number} &nbsp; {prompt}</p>'
            f'{choice_stack(pairs, answer, reveal=True)}'
            f'{reveal_line(why)}'
        )

    out.append(section([
        backdrop(),
        text_block(kicker("Quick check") + title("Name the study", 40), 64, 28, 900),
        text_block(question_block(
            "1", "Vitamin E groups already exist",
            [("A", "Observational study"), ("B", "Randomized experiment")],
            "A", "Nobody assigned the vitamin.",
        ), 64, 160, 370),
        text_block(question_block(
            "2", "Treatments in the aspirin study",
            [("A", "Heart attack or not"), ("B", "Aspirin and a placebo")],
            "B", "A heart attack is the response.",
        ), 454, 160, 370),
        text_block(question_block(
            "3", "Birth order and personality",
            [("A", "Can be assigned at random"), ("B", "Cannot be assigned")],
            "B", "You cannot hand someone a birth order.",
        ), 844, 160, 370),
    ], notes="One right-arrow shows every answer: 1A, 2B, 3B. Arrow again leaves the slide."))

    out.append(section([
        backdrop(),
        text_block(kicker("Unit 1 is complete") + title("You can tell the study apart", 44), 72, 70, 1100),
        text_block(
            '<p style="margin:0 0 12px;color:#1c242c;font-size:26px;">Observational: the groups already exist.</p>'
            '<p style="margin:0;color:#1c242c;font-size:26px;">Experiment: the researcher assigns the treatment.</p>',
            72, 240, 1000,
        ),
        text_block(card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">NEXT WEEK</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Unit 2 · Descriptive statistics</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">OpenStax sections 2.1–2.7. November 2–6.</p>',
            140,
        ), 72, 400, 980, 140),
        text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">'
            'Practice: homework 87–91. The unit test and the discussion are due November 1.</p>',
            72, 590, 1000,
        ),
    ], notes="Homework 87 is the sleep-deprivation driving study: explanatory is amount of sleep, response is performance, treatments are normal sleep and 27 hours awake, units are the 19 drivers, both treatments in random order. Items 88 and 89 are misleading graphs. Items 90 and 91 bring the chapter together. Labs 1.5 and 1.6 are not part of this unit."))

    return out


SHELL = """<!DOCTYPE html>
<html class="sl-root decks export offline loaded">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover, minimal-ui">
<meta charset="utf-8">
<title>MATH 117 · 1.4 Experiments and ethics</title>
<link rel="stylesheet" type="text/css" href="lib/offline-v2.css">
</head>
<body class="reveal-viewport theme-font-montserrat theme-color-white-blue">
<div class="reveal"><div class="slides">
{slides}
</div></div>
<script>
var SLConfig = {{"deck": {{"slug": "math117-1-4-experiments", "title": "MATH 117 · 1.4 Experiments and ethics", "description": "Observational studies, experiments, and ethics.", "width": 1280, "height": 720, "margin": 0.05, "theme_font": "montserrat", "theme_color": "white-blue", "center": false, "transition": "slide", "background_transition": "slide", "slide_count": {count}, "version": 2, "rtl": false, "should_loop": false, "shuffle": false, "navigation_mode": "default", "language": "en", "font_typekit": null, "font_google": null, "notes": {{}}}}}};
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
    print(f"zip {ZIP_PATH} bytes {ZIP_PATH.stat().st_size}")


if __name__ == "__main__":
    main()
