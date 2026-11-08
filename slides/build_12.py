"""Unit 3, sections 12.1, 12.2, 12.3, and 12.5.

OpenStax Introductory Statistics 2e. Section 12.4 is the significance test;
the Fall 2026 calendar skips it. Every number is from the book.
"""

import build_2_2_to_2_7 as b


def m(latex):
    """A symbol inside a sentence. Display math would split the line."""
    return "\\(" + latex + "\\)"


def M(latex):
    """An equation on its own line. The player renders $$ as display math."""
    return "$$" + latex + "$$"


def pairs(data):
    """Each pair stays on one line. The row may wrap between pairs."""
    return "".join(
        f'<span style="display:inline-block;white-space:nowrap;margin:0 12px 4px 0;">{x} → {y}</span>'
        for x, y in data
    )


MATH_STYLE = (
    '<div class="sl-block" style="width:1px;height:1px;left:0;top:0;">'
    '<style>.katex-display{margin:0.12em 0 !important;}</style></div>'
)

# Filled in after each graph is saved to the instructor's Desmos account.
# write_deck reads b.GRAPHS, so the links live there.
for key, url in {
    "12.1": "https://www.desmos.com/calculator/95xebowpci",
    "12.2": "https://www.desmos.com/calculator/mxsh8gz3ls",
    "12.3": "https://www.desmos.com/calculator/3c07limkyp",
    "12.5": "https://www.desmos.com/calculator/86veidxfbr",
}.items():
    b.GRAPHS[key] = url


def opening(h1, subtitle, section_label, visual, notes):
    return b.section([
        MATH_STYLE,
        b.backdrop(),
        b.text_block(
            '<p style="margin:0;">'
            '<span style="color:#ffffff;background:#2a6f7a;padding:6px 12px;'
            'letter-spacing:0.12em;font-weight:700;font-size:16px;">MATH 117</span>'
            '<span style="color:#5d6670;font-size:20px;"> &nbsp; Unit 3 · Linear regression</span></p>',
            72, 148, 680, 48,
        ),
        b.text_block(
            f'<h1 style="margin:0;color:#1c242c;font-size:54px;line-height:0.98;font-weight:650;'
            f'letter-spacing:-0.04em;">{h1}</h1>'
            f'<p style="margin:18px 0 0;color:#1c242c;font-size:24px;line-height:1.3;">{subtitle}</p>'
            f'<p style="margin:16px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;'
            f'letter-spacing:0.08em;">{section_label}</p>',
            72, 214, 620,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 540, 560,
        ),
        visual,
    ], notes)


def line_svg(a, slope, x0, x1, width, height, heading, xticks, yticks):
    left, right, top, bottom = 52, 24, 48, 36
    y0, y1 = a + slope * x0, a + slope * x1
    xmin, xmax = x0, x1
    ymin, ymax = min(y0, y1, 0), max(y0, y1, 0)
    pad_x = (xmax - xmin) * 0.08 or 1
    pad_y = (ymax - ymin) * 0.12 or 1
    xmin -= pad_x
    xmax += pad_x
    ymin -= pad_y
    ymax += pad_y
    plot_w = width - left - right
    plot_h = height - top - bottom

    def X(v):
        return left + (v - xmin) / (xmax - xmin) * plot_w

    def Y(v):
        return top + (1 - (v - ymin) / (ymax - ymin)) * plot_h

    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="20" y="30" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        f'font-weight="700" letter-spacing="1.2">{heading}</text>',
        f'<line x1="{X(xmin):.1f}" y1="{Y(0):.1f}" x2="{X(xmax):.1f}" y2="{Y(0):.1f}" '
        f'stroke="#d5e0de" stroke-width="1.4"></line>',
        f'<line x1="{X(0):.1f}" y1="{Y(ymin):.1f}" x2="{X(0):.1f}" y2="{Y(ymax):.1f}" '
        f'stroke="#d5e0de" stroke-width="1.4"></line>',
        f'<line x1="{X(x0):.1f}" y1="{Y(y0):.1f}" x2="{X(x1):.1f}" y2="{Y(y1):.1f}" '
        f'stroke="#2a6f7a" stroke-width="3"></line>',
    ]
    for value, lab in xticks:
        parts.append(
            f'<text x="{X(value):.1f}" y="{height - 12}" text-anchor="middle" font-size="14" '
            f'fill="#5d6670" font-family="Montserrat, sans-serif">{lab}</text>'
        )
    for value, lab in yticks:
        parts.append(
            f'<text x="14" y="{Y(value) + 4:.1f}" font-size="14" fill="#5d6670" '
            f'font-family="Montserrat, sans-serif">{lab}</text>'
        )
    return b.svg_wrap("".join(parts), width, height)


def slope_svg(kind, width, height):
    """Figure 12.4, as a sketch. No data."""
    title = {"up": "b &gt; 0", "flat": "b = 0", "down": "b &lt; 0"}[kind]
    caption = {
        "up": "The line climbs to the right.",
        "flat": "The line is horizontal.",
        "down": "The line falls to the right.",
    }[kind]
    y1, y2 = {"up": (150, 48), "flat": (98, 98), "down": (48, 150)}[kind]
    return b.svg_wrap(
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>'
        f'<text x="20" y="36" font-size="22" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        f'font-weight="700">{title}</text>'
        f'<line x1="36" y1="{y1}" x2="{width - 36}" y2="{y2}" stroke="#2a6f7a" stroke-width="4"></line>'
        f'<text x="20" y="{height - 24}" font-size="16" fill="#1c242c" '
        f'font-family="Montserrat, sans-serif">{caption}</text>',
        width, height,
    )


def curve_svg(width, height):
    """The shape of Figure 12.3. The book prints no equation for it."""
    return b.svg_wrap(
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>'
        '<text x="20" y="32" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        'font-weight="700" letter-spacing="1.2">FIGURE 12.3</text>'
        '<line x1="56" y1="250" x2="520" y2="250" stroke="#d5e0de" stroke-width="1.4"></line>'
        '<line x1="56" y1="40" x2="56" y2="250" stroke="#d5e0de" stroke-width="1.4"></line>'
        '<path d="M56 240 C 140 236, 200 220, 250 170 C 300 120, 340 40, 390 16" '
        'fill="none" stroke="#2a6f7a" stroke-width="3"></path>'
        '<text x="500" y="272" font-size="15" fill="#5d6670" font-family="Montserrat, sans-serif">x</text>'
        '<text x="28" y="36" font-size="15" fill="#5d6670" font-family="Montserrat, sans-serif">y</text>',
        width, height,
    )


def scatter(points, width, height, heading, xlabel, ylabel, line=None, captions=()):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    dx = (xmax - xmin) or 1
    dy = (ymax - ymin) or 1
    xmin -= dx * 0.15
    xmax += dx * 0.1
    ymin -= dy * 0.18
    ymax += dy * 0.16
    extra = 22 * len(captions)
    left, right, top, bottom = 58, 20, 44, 40 + extra
    plot_w = width - left - right
    plot_h = height - top - bottom

    def X(v):
        return left + (v - xmin) / (xmax - xmin) * plot_w

    def Y(v):
        return top + (1 - (v - ymin) / (ymax - ymin)) * plot_h

    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="18" y="28" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        f'font-weight="700" letter-spacing="1.2">{heading}</text>',
    ]
    if line:
        aa, slope = line
        x_lo, x_hi = min(xs), max(xs)
        parts.append(
            f'<line x1="{X(x_lo):.1f}" y1="{Y(aa + slope * x_lo):.1f}" '
            f'x2="{X(x_hi):.1f}" y2="{Y(aa + slope * x_hi):.1f}" '
            f'stroke="#2a6f7a" stroke-width="2.5"></line>'
        )
    for x, y in points:
        parts.append(
            f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="6" fill="#5aa8b4" stroke="#2a6f7a" '
            f'stroke-width="1.5"></circle>'
        )
    parts.append(
        f'<text x="{width / 2:.0f}" y="{height - 14 - extra}" text-anchor="middle" font-size="14" '
        f'fill="#5d6670" font-family="Montserrat, sans-serif">{xlabel}</text>'
    )
    for i, line_text in enumerate(captions):
        parts.append(
            f'<text x="{width / 2:.0f}" y="{height - 10 - (len(captions) - 1 - i) * 18}" '
            f'text-anchor="middle" font-size="13" fill="#1c242c" '
            f'font-family="Montserrat, sans-serif">{line_text}</text>'
        )
    parts.append(
        f'<text x="16" y="56" font-size="13" fill="#5d6670" font-family="Montserrat, sans-serif">{ylabel}</text>'
    )
    return b.svg_wrap("".join(parts), width, height)


EXAM = [(65, 175), (67, 133), (71, 185), (71, 163), (66, 126), (75, 198),
        (67, 153), (70, 163), (71, 159), (69, 151), (69, 159)]
VOCAB = [(3, 655), (4, 1098), (6, 2463), (7, 3195)]
AMELIA = [(5, 15), (7, 22), (9, 28), (10, 31), (11, 33), (12, 36)]
SCUBA = [(50, 80), (60, 55), (70, 45), (80, 35), (90, 25), (100, 22)]
EXAM_CAP = (
    "65→175   67→133   71→185   71→163   66→126   75→198",
    "67→153   70→163   71→159   69→151   69→159",
)
VOCAB_CAP = ("3→655   4→1,098   6→2,463   7→3,195",)
AMELIA_CAP = ("5→15   7→22   9→28   10→31   11→33   12→36",)
SCUBA_CAP = ("50→80   60→55   70→45   80→35   90→25   100→22",)


def pair_table(pairs):
    cells = "".join(
        f'<span style="display:inline-block;width:150px;">{x} → {y}</span>' for x, y in pairs
    )
    return cells


def slides_121():
    out = []
    out.append(opening(
        "Linear equations",
        "A straight line, written<br>" + m(r"y = a + bx") + ".",
        "SECTION 12.1",
        b.drawing(line_svg(-1, 2, -2, 8, 460, 480, "y = −1 + 2x",
                           [(0, "0"), (4, "4"), (8, "8")],
                           [(0, "0"), (8, "8"), (15, "15")]), 760, 120, 460, 480),
        "About 20 minutes. This section is the algebra the rest of the unit sits on. "
        "No data yet. y = a + bx is the book's form: a is the intercept, b is the slope. "
        "Say the intercept as 'a' and the slope as 'b'.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The form of a line")
            + b.title(m(r"y = a + bx"), 48),
            64, 36, 1150,
        ),
        *b.three_cards([
            ("x · independent", "You choose it.", "Hours, age, or a third-exam score. You substitute a value for x."),
            ("y · dependent", "The equation gives it.", "Cost, vocabulary, or a final-exam score. Put in an x. The equation gives y."),
            ("a and b", "Start, then tilt.", "a is the y-intercept, the value of y when x = 0. b is the slope."),
        ], 250, 250),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            'One step to the right changes y by b. Any non-vertical line can be written this way.</p>',
            72, 560, 1136,
        ),
    ], notes=(
        "Book: the variable x is the independent variable, and y is the dependent variable. "
        "Typically you choose a value for x and then solve for y. "
        "b = slope and a = y-intercept. The intercept is the y-coordinate of the point (0, a)."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 12.1")
            + b.title("These are lines", 44),
            64, 36, 1150,
        ),
        *b.three_cards([
            ("Linear", m(r"y = 3 + 2x"), m(r"a = 3") + ", " + m(r"b = 2") + ". The line crosses at 3 and climbs by 2."),
            ("Linear", m(r"y = -0.01 + 1.2x"), m(r"a = -0.01") + ", " + m(r"b = 1.2") + ". A small intercept, a gentle climb."),
            ("Try It 12.1", m(r"y = -0.125 - 3.5x"), "Also linear. " + m(r"a = -0.125") + " and " + m(r"b = -3.5") + ", so the line falls."),
        ], 240, 280),
    ], notes=(
        "Example 12.1 prints y = 3 + 2x and y = −0.01 + 1.2x and says both are linear equations. "
        "Try It 12.1 asks whether y = −0.125 − 3.5x is linear. Yes. It has the form a + bx."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 12.2")
            + b.title("Graph " + m(r"y = -1 + 2x"), 40),
            64, 24, 700,
        ),
        b.drawing(line_svg(-1, 2, -2, 8, 700, 430, "y = −1 + 2x",
                           [(-2, "−2"), (0, "0"), (4, "4"), (8, "8")],
                           [(-5, "−5"), (0, "0"), (8, "8"), (15, "15")]), 64, 150, 700, 430),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">'
            + m(r"a = -1") + '. The line crosses the y-axis at −1.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            + m(r"b = 2") + '. Each step to the right raises the line by 2.</p>',
            180,
        ), 800, 180, 416, 180),
        b.desmos_line("y = -1 + 2x", 430, left=800, width=416, graph="12.1" if "12.1" in b.GRAPHS else None),
    ], notes="Example 12.2: graph y = −1 + 2x. Intercept −1, slope 2. Figure 12.2."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 12.2")
            + b.title("Is this a linear equation?", 40),
            64, 28, 1150,
        ),
        b.drawing(curve_svg(560, 300), 64, 180, 560, 300),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:26px;font-weight:650;line-height:1.3;">No.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'A linear equation graphs as a straight line. This curve bends, so it is not ' + m(r"y = a + bx") + '.</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:18px;line-height:1.4;">'
            'The book shows the picture and does not give an equation.</p>',
            280,
        ), 660, 190, 552, 280),
    ], notes=(
        "Try It 12.2 shows Figure 12.3, a curve, and asks whether it is a linear equation and why. "
        "No, because it is not a straight line."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Figure 12.4")
            + b.title("The sign of b is the direction", 40),
            64, 28, 1150,
        ),
        b.drawing(slope_svg("up", 360, 230), 72, 200, 360, 230),
        b.drawing(slope_svg("flat", 360, 230), 460, 200, 360, 230),
        b.drawing(slope_svg("down", 360, 230), 848, 200, 360, 230),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            'Try It 12.1 has ' + m(r"b = -3.5") + ', so that line falls. Svetlana’s line, coming up, has ' + m(r"b = 15") + ', so it climbs.</p>',
            72, 500, 1136,
        ),
    ], notes=(
        "Figure 12.4: if b > 0 the line slopes upward to the right, if b = 0 the line is horizontal, "
        "if b < 0 the line slopes downward to the right. These three sketches have no data."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 12.3 · a tax return")
            + b.title("A fee, plus an hourly rate", 40),
            64, 28, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">THE EQUATION</p>'
            '<p style="margin:4px 0 0;color:#1c242c;font-size:22px;">' + M(r"y = 31.50 + 32x") + '</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'x is the hours the job takes. y is the dollars the customer pays.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            '31.50 is the fee for showing up. 32 is one more hour. Two hours: ' + m(r"31.50 + 32(2) = 95.50") + '.</p>',
            280,
        ), 64, 180, 1150, 280),
        b.desmos_line("y = 31.50 + 32x", 520, graph="12.1" if "12.1" in b.GRAPHS else None),
    ], notes=(
        "Example 12.3. $32 per hour plus a $31.50 one-time charge. "
        "y = 31.50 + 32x. Fixed cost 31.50, and (32)(x) is the processing."
    )))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 12.3 · 3 minutes",
            "Write Emma’s equation",
            "She pays an instructor $50 per class plus $20 per student. "
            "Let x be the number of students. Let y be the total cost.",
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:28px;font-weight:650;line-height:1.35;">'
            'y = ________ + ________ x</p>'
            '<p style="margin:18px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'Which number is the fee for showing up, and which number is the cost of one more student?</p>',
            180,
        ), 72, 250, 1136, 180),
    ], notes="Try It 12.3. Answer on the next slide: y = 50 + 20x."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 12.3")
            + b.title(m(r"y = 50 + 20x"), 44),
            64, 36, 1150,
        ),
        *b.three_cards([
            ("x", "Number of students", "How many students are in the class. That is the number she puts in for x."),
            ("y", "Total cost, in dollars", "The dependent variable. The equation gives what she pays."),
            ("a and b", m(r"a = 50") + ",  " + m(r"b = 20"), "$50 for the class, then $20 more for each student in it."),
        ], 230, 270),
        b.desmos_line("y = 50 + 20x", 560, graph="12.1" if "12.1" in b.GRAPHS else None),
    ], notes="Try It 12.3 solution: y = 50 + 20x. a = 50, b = 20."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 12.4 · Svetlana")
            + b.title("Say what a and b mean", 40),
            64, 28, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:22px;">' + M(r"y = 25 + 15x") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:18px;">$25 to start, plus $15 per hour of tutoring.</p>',
            150,
        ), 64, 160, 1150, 150),
        *b.three_cards([
            ("x", "Hours in the session", "Independent. How long she tutors."),
            ("y", "Dollars she earns", "Dependent. What the equation gives."),
            ("a and b", m(r"a = 25") + ",  " + m(r"b = 15"), "At " + m(r"x = 0") + " she has already charged $25. Each hour adds $15."),
        ], 340, 230),
    ], notes=(
        "Example 12.4. Independent variable: hours tutored in the session. "
        "Dependent variable: dollars earned. y-intercept 25 is the one-time fee when x = 0. "
        "Slope 15: she earns $15 for each hour."
    )))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 12.4 · 3 minutes",
            "Read Ethan’s equation",
            "He charges $25 plus $20 per hour. The book writes " + m(r"y = 25 + 20x") + ".",
        ),
        b.text_block(
            b.revealed_answers([
                ("What is x, and what is y?",
                 "x is hours of work. y is dollars he earns for the visit."),
                ("What are a and b, in a sentence?",
                 "a = 25, the fee at the start. b = 20, so each hour adds $20."),
            ]),
            72, 230, 1136,
        ),
    ], notes=(
        "Try It 12.4. Same shape as Svetlana. x = hours, y = dollars per visit, a = 25, b = 20. "
        "Click once for each answer."
    )))
    out.append(b.quick("Read the equation", [
        ("In " + m(r"y = a + bx") + ", the slope is",
         [("A", "a"), ("B", "b"), ("C", "x")], "B", "b is the change in y for one step in x."),
        ("In Svetlana’s " + m(r"y = 25 + 15x") + ", the 25 is",
         [("A", "A one-time fee"), ("B", "The hourly rate"), ("C", "The hours")], "A",
         "It is y when x = 0."),
        (m(r"y = -0.125 - 3.5x") + " is",
         [("A", "Not linear"), ("B", "Linear"), ("C", "A scatter plot")], "B",
         "Try It 12.1. It has the form a + bx."),
    ], "One right-arrow shows every answer: 1B, 2A, 3B. Practice items 1 through 16."))
    out.append(b.closing(
        "Before section 12.2",
        "You can read a line",
        [
            m(r"y = a + bx") + ". x is independent, y is dependent.",
            "a is the value at x = 0. b is the change for one step to the right.",
            "A curve is not this equation. The next picture is a cloud of points.",
        ],
        ("12.2 &nbsp; Scatter plots", "One point for each pair."),
        "Practice: OpenStax 12.1, items 1 through 16.",
        "Items 1 to 16 are the linear-equation practice. Section 12.2 starts at item 17.",
        graph="12.1" if "12.1" in b.GRAPHS else None,
    ))
    return out


def slides_122():
    out = []
    out.append(opening(
        "Scatter plots",
        "One point for each pair.<br>Then look for a direction.",
        "SECTION 12.2",
        b.drawing(scatter(VOCAB, 460, 480, "AGE AND VOCABULARY", "age", "words", captions=VOCAB_CAP), 760, 120, 460, 480),
        "About 20 minutes. Example 12.5 is four children. Try It 12.5 is Amelia’s six games. "
        "No regression line yet. That is section 12.3. The question here is direction and whether a line even makes sense.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Two variables at once")
            + b.title("Each pair becomes a point", 40),
            64, 36, 1150,
        ),
        *b.three_cards([
            ("The pair", "(x, y)", "x goes across. y goes up. One student, one game, one child: one point."),
            ("Direction", "Climb, fall, or neither", "High with high is a positive direction. High with low is a negative direction."),
            ("A line, later", "Only if x explains y", "Closeness to a line is the strength. A horizontal line is no relationship."),
        ], 240, 270),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            'This is bivariate data. “Bi” means two. The chapter uses one independent variable.</p>',
            72, 570, 1136,
        ),
    ], notes=(
        "Book: bivariate data, 'bi' for two variables. A clear direction is high with high, or high with low. "
        "Strength is how close the points are to a line. Exception: points on a horizontal line are a perfect fit "
        "and still show no relationship."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 12.5 · Table 12.1")
            + b.title("Age and vocabulary", 40),
            64, 20, 1150,
        ),
        b.data_strip(
            "FOUR CHILDREN · x = AGE IN YEARS · y = NUMBER OF WORDS",
            "3 → 655 &nbsp;&nbsp; 4 → 1,098 &nbsp;&nbsp; 6 → 2,463 &nbsp;&nbsp; 7 → 3,195",
            150, height=88,
        ),
        b.drawing(scatter(VOCAB, 1152, 340, "EXAMPLE 12.5", "child’s age", "vocabulary size"), 64, 260, 1152, 340),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'The points climb. Older children in this table know more words. Four points, and they follow a line.</p>',
            64, 620, 1150,
        ),
    ], notes=(
        "Example 12.5, Table 12.1. x = child’s age, y = vocabulary size. "
        "Ages 3, 4, 6, 7 and sizes 655, 1098, 2463, 3195. Positive direction. Figure 12.5."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("What to notice")
            + b.title("Direction, then strength", 40),
            64, 28, 1150,
        ),
        *b.three_cards([
            ("Positive", "High with high", "As x grows, y tends to grow. Age and vocabulary climb together."),
            ("Negative", "High with low", "As x grows, y tends to fall. The dive table in 12.3 will do this."),
            ("No relationship", "A cloud, or a flat line", "No direction means no relationship. A horizontal line is a perfect fit, and still no relationship."),
        ], 200, 250),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'Strength is how close the points sit to a line. Close means strong. Spread out means weak. '
            'Look at the whole pattern, and at any point that sits off it.</p>',
            72, 500, 1136,
        ),
    ], notes=(
        "Book, after Try It 12.5. High with high, or high with low. "
        "A horizontal line would be a perfect fit and still no relationship. "
        "Notice the overall pattern and any deviations. Figures 12.6, 12.7, and 12.8 are the book's pictures of these cases."
    )))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 12.5 · 4 minutes",
            "Does Amelia’s idea show up?",
            "She thinks more jump-shot practice comes with more points. Table 12.2. Plot the six games, then decide.",
        ),
        b.data_strip(
            "x = HOURS PRACTICING · y = POINTS IN THE GAME",
            "5 → 15 &nbsp;&nbsp; 7 → 22 &nbsp;&nbsp; 9 → 28 &nbsp;&nbsp; 10 → 31 &nbsp;&nbsp; 11 → 33 &nbsp;&nbsp; 12 → 36",
            250, height=100,
        ),
    ], notes="Try It 12.5, Table 12.2. The pairs continue on this strip: 11 → 33 and 12 → 36. Answer on the next slide."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 12.5")
            + b.title("The points climb", 44),
            64, 20, 700,
        ),
        b.drawing(scatter(AMELIA, 640, 460, "AMELIA · SIX GAMES", "hours of practice", "points", captions=AMELIA_CAP), 64, 150, 640, 460),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:16px;line-height:1.45;">' + pairs(AMELIA) + '</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;font-weight:650;line-height:1.3;">'
            'What she noticed is in the plot.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            'More hours sit with more points. The direction is positive, and the points are close to a line.</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:18px;line-height:1.4;">'
            'The plot shows the pattern. It does not, by itself, say that practice caused the points.</p>',
            320,
        ), 740, 180, 472, 320),
    ], notes=(
        "The book asks whether what Amelia thinks appears to be true. The points rise with practice, so the pattern she noticed is there. "
        "Save causation for the correlation section: correlation does not imply causation. The book’s own warning is in 12.3."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Before the line of best fit")
            + b.title("A line is for predicting", 40),
            64, 48, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:26px;line-height:1.4;">'
            'Draw a line only when one variable helps explain or predict the other.</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'If x is independent and y is dependent, the line predicts y for a given x.</p>'
            '<p style="margin:16px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'Age can sit on the horizontal axis for vocabulary. Hours can sit there for Amelia’s points. '
            'The calculation is next, in 12.3.</p>',
            280,
        ), 64, 200, 1150, 280),
    ], notes=(
        "Book, end of 12.2: we only calculate a regression line if one of the variables helps to explain or predict the other. "
        "If x is independent and y is dependent, the line predicts y for a given x."
    )))
    out.append(b.quick("Read the plot", [
        ("A scatter plot has one point per",
         [("A", "Pair"), ("B", "Category"), ("C", "Bar")], "A", "Each (x, y) is a dot."),
        ("Amelia’s six games",
         [("A", "Climb"), ("B", "Fall"), ("C", "Sit flat")], "A", "More hours, more points."),
        ("Points on a horizontal line show",
         [("A", "No relationship"), ("B", "A perfect cause"), ("C", "A negative slope")], "A",
         "The book’s exception. Flat means y does not change."),
    ], "Answers: 1A, 2A, 3A. Practice items 17 through 19 are the scatter-plot figures in the book."))
    out.append(b.closing(
        "Before section 12.3",
        "You can read a cloud of points",
        [
            "One point per pair. Across is x, up is y.",
            "Name the direction, then how close the points are to a line.",
            "A flat line is no relationship. The next section fits the line.",
        ],
        ("12.3 &nbsp; The regression line", "The line that misses by the least."),
        "Practice: OpenStax 12.2, items 17 through 19.",
        "Items 17 to 19 ask whether a scatter plot looks linear, strong or weak, positive or negative. "
        "Section 12.3 starts at item 20.",
        graph="12.2" if "12.2" in b.GRAPHS else None,
    ))
    return out


def slides_123():
    out = []
    out.append(opening(
        "The regression line",
        "The line that makes the<br>squared gaps as small as possible.",
        "SECTION 12.3",
        b.drawing(scatter(EXAM, 460, 480, "THIRD EXAM AND FINAL", "third exam", "final",
                          line=(-173.51, 4.83)), 760, 120, 460, 480),
        "The long section. Eleven students, third exam out of 80 and final out of 200. "
        "The book’s line is ŷ = −173.51 + 4.83x, with r = 0.6631 and r² = 0.4397. "
        "Say ŷ as 'y-hat'. Desmos does the fit. Students should not compute the sums by hand. "
        "Section 12.4, the significance test, is not in this unit.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 12.6 · 11 statistics students")
            + b.title("Third exam and final exam", 36),
            64, 20, 1150,
        ),
        b.data_strip(
            "x = THIRD EXAM, OUT OF 80 · y = FINAL EXAM, OUT OF 200",
            pair_table(EXAM),
            145, height=130,
        ),
        b.drawing(scatter(EXAM, 1152, 300, "FIGURE 12.9", "third exam score", "final exam score"),
                  64, 300, 1152, 300),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;">'
            'They climb, but not on one line. The question is whether the third exam can predict the final.</p>',
            64, 620, 1150,
        ),
    ], notes=(
        "Table 12.3. Pairs: (65, 175), (67, 133), (71, 185), (71, 163), (66, 126), (75, 198), "
        "(67, 153), (70, 163), (71, 159), (69, 151), (69, 159). "
        "The question in the book: can you predict the final if you know the third exam?"
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("A point, and the point on the line")
            + b.title("The gap is called a residual", 40),
            64, 28, 1150,
        ),
        *b.three_cards([
            ("y-hat", m(r"\hat{y}"), "The value on the line. Say it “y-hat.” It is not, usually, the y in the table."),
            ("Residual", m(r"y - \hat{y}"), "The vertical gap. Positive means the point is above the line."),
            ("SSE", "Add the squared gaps", "The line we use is the one that makes this sum as small as it can be."),
        ], 210, 250),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'There are 11 points, so there are 11 residuals. Add the squared gaps:</p>'
            '<p style="margin:8px 0;color:#1c242c;font-size:22px;">' + M(r"\mathrm{SSE} = \sum (y-\hat{y})^{2}") + '</p>'
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'Any other line would have a larger SSE. This line is the least-squares line.</p>',
            72, 510, 1136,
        ),
    ], notes=(
        "ŷ is read y-hat. Residual ε = y − ŷ, epsilon. "
        "Above the line, the residual is positive and the line underestimated y. "
        "Below the line, the residual is negative and the line overestimated y. "
        "SSE is the sum of the squared residuals. Minimizing SSE is the least-squares criterion."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The formulas")
            + b.title("Where a and b come from", 40),
            64, 24, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:20px;text-align:center;">' + M(r"\hat{y} = a + bx") + '</p>'
            '<p style="margin:0;color:#1c242c;font-size:20px;text-align:center;">'
            + M(r"b = \dfrac{\sum (x-\bar{x})(y-\bar{y})}{\sum (x-\bar{x})^{2}}")
            + " " + M(r"a = \bar{y} - b\bar{x}") + '</p>'
            '<p style="margin:0;color:#1c242c;font-size:20px;text-align:center;">'
            + M(r"b = r\,\dfrac{s_y}{s_x}") + '</p>',
            300,
        ), 64, 150, 1150, 300),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'You do not add these sums by hand. Desmos does. The exact line passes through the two means, '
            + m(r"\bar{x} = 69.18") + ' and ' + m(r"\bar{y} = 160.45") + '.</p>',
            72, 470, 1136,
        ),
        b.desmos_line("table x₁, y₁ &nbsp; then &nbsp; y₁ ~ a + b x₁", 580,
                      graph="12.3" if "12.3" in b.GRAPHS else None),
    ], notes=(
        "Means from the 11 pairs: x-bar = 761/11 = 69.1818, y-bar = 1765/11 = 160.4545. "
        "The book rounds the fitted line to ŷ = −173.51 + 4.83x. "
        "The unrounded fit is a = −173.513 and b = 4.8273, and that line passes through the point of averages. "
        "b = r (sy/sx) is the book's second form of the slope."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The book’s line")
            + b.title(m(r"\hat{y} = -173.51 + 4.83x"), 36),
            64, 16, 1150,
        ),
        b.data_strip("THE 11 STUDENTS · x = THIRD EXAM OUT OF 80 · y = FINAL OUT OF 200", pairs(EXAM), 118, height=108),
        b.drawing(scatter(EXAM, 700, 380, "THIRD EXAM AND FINAL", "third exam", "final",
                          line=(-173.51, 4.83)), 64, 240, 700, 380),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">THE SLOPE, IN WORDS</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            + m(r"b = 4.83") + '. For one more point on the third exam, the final goes up by 4.83 points, on average.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            + m(r"a = -173.51") + ' is the line at ' + m(r"x = 0") + '. Do not read it as a score. These third exams start at 65.</p>',
            250,
        ), 800, 250, 416, 250),
    ], notes=(
        "Book: a = −173.513, b = 4.8273, rounded to ŷ = −173.51 + 4.83x. "
        "Interpretation of the slope, from the book: for a one-point increase on the third exam, "
        "the final exam score increases by 4.83 points, on average. "
        "Also on the calculator screen, which we are not using: r² = 0.43969 and r = 0.663."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("One residual, from the book")
            + b.title("The point (65, 175)", 40),
            64, 36, 1150,
        ),
        *b.three_cards([
            ("On the line", m(r"140.44"), m(r"-173.51 + 4.83(65) = 140.44")),
            ("In the table", "175", "That student scored 175 on the final. The pair is (65, 175)."),
            ("The residual", "35", m(r"175 - 140.44 = 34.56") + ", which the book records as 35. The point is above the line."),
        ], 220, 260),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            'The line guessed about 140. This student scored 175, so the residual is positive. A residual is a miss, not a mistake in the data.</p>',
            72, 540, 1136,
        ),
    ], notes=(
        "Using the rounded line: −173.51 + 4.83(65) = 140.44, and 175 − 140.44 = 34.56. "
        "Section 12.6, which we do not cover, lists this residual as 35 and names the point (65, 175). "
        "Use 35, the book's figure."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The correlation coefficient")
            + b.title("r measures the line", 44),
            64, 28, 1150,
        ),
        *b.three_cards([
            ("The number", m(r"-1 \le r \le 1"), "Close to 1 or −1 is a strong line. Close to 0, the best line is flat: x does not predict y. A curve can still be there, so check the plot."),
            ("The sign", "Same sign as b", "Positive r: x and y climb together. Negative r: one climbs while the other falls."),
            ("These exams", m(r"r = 0.6631"), "Positive, and moderate. The points climb, with a visible scatter."),
        ], 200, 250),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'Strong correlation does not mean x causes y. Correlation does not imply causation. '
            'Desmos reports ' + m(r"r^{2}") + '. The square root has the same sign as ' + m(r"b") + '.</p>',
            72, 500, 1136,
        ),
    ], notes=(
        "Book: r is always between −1 and 1. r = 1 is perfect positive, r = −1 is perfect negative, "
        "and in both cases every point is on the line. r = 0 means no linear correlation, but a curve can also give r near 0, so look at the plot. "
        "The sign of r matches the sign of b. "
        "For the exams the book gives r = 0.6631. The note in the book: strong correlation does not suggest that x causes y."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The coefficient of determination")
            + b.title(m(r"r^{2}") + " is the share the line explains", 36),
            64, 28, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.3;">'
            + M(r"r^{2} = 0.6631^{2} = 0.4397 \approx 44\%") + '</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'About 44% of the variation in the final exams can be explained by the variation in the third exams, using this line.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'The other 56% is the scatter the line misses. ' + m(r"1 - 0.44 = 0.56") + '. '
            '44% is not an exam score, and it is not the percent of points that sit on the line.</p>',
            280,
        ), 64, 180, 1150, 280),
        b.desmos_line("Desmos shows R², not r &nbsp; · &nbsp; r = √R², negative when b is negative", 520,
                      graph="12.3" if "12.3" in b.GRAPHS else None),
    ], notes=(
        "Book: r² = 0.6631² = 0.4397. Approximately 44% of the variation in the final-exam grades "
        "is explained by the variation in the third-exam grades. Approximately 56% is not. "
        "1 − 0.44 = 0.56. Desmos shows R² on the regression, not r. Take the square root and give it the sign of b."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Stay inside the scores you saw")
            + b.title("The third exams run from 65 to 75", 36),
            64, 36, 1150,
        ),
        *b.three_cards([
            ("x = 73", "Inside", "73 is between 65 and 75. The line may be used. The arithmetic is section 12.5."),
            ("x = 50", "Outside", "50 is not a third-exam score in this sample. Do not use the line."),
            ("Plot first", "Then the line", "If the scatter is not roughly linear, do not use the line at all."),
        ], 200, 240),
        b.data_strip("THE 11 PAIRS · x RUNS FROM 65 TO 75", pairs(EXAM), 480, height=120),
    ], notes=(
        "Book reminder: plot the scatter diagram first. Predicting for a third-exam score of 73 is reasonable. "
        "Predicting for a score of 50 is not, because 50 is outside the observed x values, which run from 65 to 75. "
        "The actual predictions are Example 12.11."
    )))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 12.6 · 5 minutes",
            "Fit the dive times",
            "Maximum dive time, in minutes, at six depths. Use Desmos. Predict the time at 110 feet.",
        ),
        b.data_strip(
            "x = DEPTH IN FEET · y = MAXIMUM DIVE TIME IN MINUTES",
            "50 → 80 &nbsp;&nbsp; 60 → 55 &nbsp;&nbsp; 70 → 45 &nbsp;&nbsp; 80 → 35 &nbsp;&nbsp; 90 → 25 &nbsp;&nbsp; 100 → 22",
            240, height=110,
        ),
        b.desmos_line("table x₁, y₁ &nbsp; then &nbsp; y₁ ~ a + b x₁", 400,
                      graph="12.3" if "12.3" in b.GRAPHS else None),
    ], notes=(
        "Table 12.4. Depths 50, 60, 70, 80, 90, 100 with times 80, 55, 45, 35, 25, 22. "
        "Least squares: a = 127.238, b = −1.1143, r = −0.9629. "
        "At 110 feet the line gives 4.67 minutes. "
        "110 is past the last observed depth, 100. Let them compute it, and save the warning for 12.5."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 12.6")
            + b.title("The line falls", 44),
            64, 24, 1150,
        ),
        b.drawing(scatter(SCUBA, 700, 470, "DIVE DEPTH AND TIME", "depth in feet", "minutes",
                          line=(127.24, -1.114), captions=SCUBA_CAP), 64, 150, 700, 470),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:16px;line-height:1.4;">' + pairs(SCUBA) + '</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;">' + M(r"\hat{y} \approx 127.24 - 1.11x") + '</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            'Each extra 10 feet takes away about 11 minutes.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            'At 110 feet the line says about 4.7 minutes.</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:18px;line-height:1.4;">'
            + m(r"r \approx -0.96") + '. Strong, and negative.</p>',
            400,
        ), 800, 160, 416, 400),
    ], notes=(
        "Read a and b from Desmos; they should be near 127.24 and −1.114. "
        "127.238 − 1.1143(110) = 4.67, so about 4.7 minutes. "
        "Rounded the way the exam line is rounded: ŷ = 127.24 − 1.11x. "
        "r = −0.9629. Hold the extrapolation comment for section 12.5: 110 is not in the table."
    )))
    out.append(b.quick("Read the fit", [
        (m(r"\hat{y}") + " is",
         [("A", "A value in the table"), ("B", "The value on the line"), ("C", "The residual")], "B",
         "Y-hat is the estimate."),
        ("For these exams, r is",
         [("A", "0.6631"), ("B", "−0.6631"), ("C", "44")], "A", "Positive, like the slope."),
        (m(r"r^{2} \approx 0.44") + " means 44% of the variation in",
         [("A", "The final"), ("B", "The third exam"), ("C", "The residual")], "A",
         "44% of the ups and downs in the final, not 44% of the score."),
    ], "Answers: 1B, 2A, 3A. Practice items 20 through 27. Skip section 12.4."))
    out.append(b.closing(
        "Before section 12.5",
        "You can fit and read a line",
        [
            "Plot the points first. Fit them in Desmos. You do not add the sums by hand.",
            "Say what b means in a sentence. r has the same sign as b. " + m(r"r^{2}") + " is the share of y the line explains.",
            "Predict only for an x between the x values you saw. Section 12.4 is not in this unit.",
        ],
        ("12.5 &nbsp; Prediction", "Use the line inside the data you saw."),
        "Practice: OpenStax 12.3, items 20 through 27.",
        "Items 20 to 24 are the ten athletes. Items 25 to 27 are short questions about r. "
        "Item 28 starts section 12.4, which is not in this unit.",
        graph="12.3" if "12.3" in b.GRAPHS else None,
    ))
    return out


def slides_125():
    out = []
    out.append(opening(
        "Prediction",
        "Substitute an x you<br>actually saw.",
        "SECTION 12.5",
        b.drawing(scatter(EXAM, 460, 480, "PREDICT INSIDE 65 TO 75", "third exam", "final",
                          line=(-173.51, 4.83)), 760, 120, 460, 480),
        "Short section. One line, three substitutions. "
        "73 and 66 are inside 65 to 75. 90 is not, and the arithmetic gives 261 on an exam out of 200. "
        "Words: interpolation inside, extrapolation outside. "
        "The scuba prediction at 110 feet was an extrapolation. Come back to it.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The same eleven students")
            + b.title("A third-exam score of 73", 40),
            64, 24, 1150,
        ),
        b.data_strip("THE 11 THIRD EXAMS AND FINALS · 73 HAS TO SIT AMONG THESE x VALUES", pairs(EXAM), 145, height=100),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:20px;text-align:center;">' + M(r"\hat{y} = -173.51 + 4.83x") + '</p>'
            '<p style="margin:0;color:#1c242c;font-size:20px;text-align:center;">' + M(r"-173.51 + 4.83(73) = 179.08") + '</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            + m(r"4.83 \times 73 = 352.59") + ', then ' + m(r"352.59 - 173.51 = 179.08") + '. '
            'Students who score 73 are predicted to score 179.08 on the final, on average.</p>',
            230,
        ), 64, 260, 1150, 230),
        b.desmos_line("-173.51 + 4.83*73", 520, graph="12.5" if "12.5" in b.GRAPHS else None),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;">'
            '73 is between the smallest third exam, 65, and the largest, 75. This prediction is allowed.</p>',
            64, 590, 1150,
        ),
    ], notes=(
        "Book: the exam scores range from 65 to 75. Since 73 is between them, substitute. "
        "ŷ = −173.51 + 4.83(73) = 179.08. "
        "We predict that statistics students who earn 73 on the third exam will earn 179.08 on the final, on average."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 12.11")
            + b.title("Two more scores", 44),
            64, 28, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">A · SCORE OF 66</p>'
            '<p style="margin:4px 0 0;color:#1c242c;font-size:20px;">'
            + M(r"-173.51 + 4.83(66) = 145.27") + '</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '66 is between 65 and 75. The predicted final is 145.27.</p>',
            200,
        ), 64, 180, 560, 200),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">B · SCORE OF 90</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;font-weight:650;">Do not predict.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '90 is outside 65 to 75. The line has nothing to stand on.</p>',
            200,
        ), 656, 180, 560, 200),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'The arithmetic for 90 still runs: ' + m(r"-173.51 + 4.83(90) = 261.19") + '. '
            'The final exam is out of 200. A prediction of 261 is the warning, not an answer. '
            'The third exams on the previous slide are 65, 66, 67, 67, 69, 69, 70, 71, 71, 71, 75.</p>',
            72, 430, 1136,
        ),
        b.desmos_line("-173.51 + 4.83*66 &nbsp; and &nbsp; -173.51 + 4.83*90", 560,
                      graph="12.5" if "12.5" in b.GRAPHS else None),
    ], notes=(
        "Example 12.11. (a) 145.27. Check: 4.83 × 66 = 318.78, and 318.78 − 173.51 = 145.27. "
        "(b) Ninety is outside the observed x values, so the prediction is not reliable. "
        "Substituting anyway gives 261.19, and the largest possible final is 200."
    )))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Two words")
            + b.title("Inside the data, or past it", 40),
            64, 36, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">INTERPOLATION</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;font-weight:650;line-height:1.25;">'
            'An x between the ones you saw.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '66 and 73 are between 65 and 75. The predictions 145.27 and 179.08 are interpolation.</p>',
            230,
        ), 64, 190, 560, 230),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">EXTRAPOLATION</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:26px;font-weight:650;line-height:1.25;">'
            'An x outside the ones you saw.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '90 is extrapolation. So is a third-exam score of 50. Do not trust the y the line prints.</p>',
            230,
        ), 656, 190, 560, 230),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;">'
            'Dive times: ' + pairs(SCUBA) + '. The depths stop at 100, so the 4.7 minutes was extrapolation. The arithmetic was right. The prediction is not one to trust.</p>',
            72, 480, 1136,
        ),
    ], notes=(
        "Book: predicting inside the observed x values is interpolation. "
        "Predicting outside them is extrapolation. "
        "Try It 12.6 asked for 110 feet. The observed depths stop at 100, so 4.7 minutes was an extrapolation. "
        "Say so here, not as a correction of the arithmetic."
    )))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 12.11 · 3 minutes",
            "Five hours of practice",
            "Hours per week on a musical instrument, and a math-test score. The book gives the line, not the data.",
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:22px;">' + M(r"\hat{y} = 72.5 + 2.8x") + '</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;">What score does the line give for 5 hours?</p>',
            150,
        ), 72, 240, 1136, 150),
        b.desmos_line("72.5 + 2.8*5", 440, graph="12.5" if "12.5" in b.GRAPHS else None),
    ], notes="Try It 12.11. ŷ = 72.5 + 2.8x. At x = 5, 72.5 + 14 = 86.5. The book does not list the observed hours, so there is no range to check."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 12.11")
            + b.title("86.5", 56),
            64, 48, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:22px;">' + M(r"72.5 + 2.8(5) = 72.5 + 14 = 86.5") + '</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'The line predicts a math score of 86.5 for a student who practices 5 hours a week.</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'The book does not print the hours it observed, so this one is the arithmetic only. When a problem does list the x values, check that 5 sits among them before you trust 86.5.</p>',
            220,
        ), 64, 220, 1150, 220),
    ], notes="72.5 + 2.8 × 5 = 72.5 + 14 = 86.5."))
    out.append(b.quick("Predict, or stop", [
        ("A third-exam score of 73 is",
         [("A", "Interpolation"), ("B", "Extrapolation"), ("C", "Not allowed")], "A",
         "73 is between 65 and 75."),
        ("A third-exam score of 90",
         [("A", "Gives 179"), ("B", "Cannot be trusted"), ("C", "Gives 200")], "B",
         "Outside 65 to 75. The arithmetic gives 261."),
        (m(r"72.5 + 2.8(5)") + " equals",
         [("A", "75.3"), ("B", "86.5"), ("C", "72.5")], "B", "72.5 + 14."),
    ], "Answers: 1A, 2B, 3B. Homework items 67 through 71. Unit 3 is due November 9."))
    out.append(b.closing(
        "Before Exam 1",
        "You can use the line, and you know when not to",
        [
            "Substitute an x that sits between the x values in the data.",
            "Inside is interpolation. Outside is extrapolation, and the y is not reliable.",
            "Exam 1 covers Units 1, 2, and 3.",
        ],
        ("Exam 1", "November 10–11. Units 1, 2, and 3."),
        "Practice: OpenStax 12.5, items 67 through 71. Unit 3 is due November 9.",
        "Items 67 to 71 are the prediction homework. Item 72 starts outliers, which is section 12.6 and not in this unit. "
        "Homework, the unit test, and the discussion are due November 9.",
        graph="12.5" if "12.5" in b.GRAPHS else None,
    ))
    return out


DECKS = [
    ("12.1-lines", "math117-12-1-lines", "MATH 117 · 12.1 Linear equations",
     "The line y = a + bx, before any data.", slides_121),
    ("12.2-scatter", "math117-12-2-scatter", "MATH 117 · 12.2 Scatter plots",
     "One point for each pair, and the direction it shows.", slides_122),
    ("12.3-regression", "math117-12-3-regression", "MATH 117 · 12.3 The regression line",
     "The least-squares line, r, and r squared.", slides_123),
    ("12.5-prediction", "math117-12-5-prediction", "MATH 117 · 12.5 Prediction",
     "Use the line inside the data. Stop outside it.", slides_125),
]


def main():
    for folder, slug, title, description, builder in DECKS:
        b.write_deck(folder, slug, title, description, builder)


if __name__ == "__main__":
    main()
