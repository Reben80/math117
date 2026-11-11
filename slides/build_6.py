"""Unit 4, sections 6.1 and 6.2, taught together on November 11.

OpenStax Introductory Statistics 2e. Sections 6.3 and 6.4 are not on the
calendar. Every number is from the book. Section 7.1 is the next lecture.
"""

import math

import build_2_2_to_2_7 as b


def m(latex):
    """A symbol inside a sentence. Display math would split the line."""
    return "\\(" + latex + "\\)"


def M(latex):
    """An equation on its own line. The player renders $$ as display math."""
    return "$$" + latex + "$$"


MATH_STYLE = (
    '<div class="sl-block" style="width:1px;height:1px;left:0;top:0;">'
    '<style>.katex-display{margin:0.12em 0 !important;}</style></div>'
)


def opening(h1, subtitle, section_label, visual, notes):
    return b.section([
        MATH_STYLE,
        b.backdrop(),
        b.text_block(
            '<p style="margin:0;">'
            '<span style="color:#ffffff;background:#2a6f7a;padding:6px 12px;'
            'letter-spacing:0.12em;font-weight:700;font-size:16px;">MATH 117</span>'
            '<span style="color:#5d6670;font-size:20px;"> &nbsp; Unit 4 · The normal distribution</span></p>',
            72, 148, 700, 48,
        ),
        b.text_block(
            f'<h1 style="margin:0;color:#1c242c;font-size:52px;line-height:0.98;font-weight:650;'
            f'letter-spacing:-0.04em;">{h1}</h1>'
            f'<p style="margin:18px 0 0;color:#1c242c;font-size:24px;line-height:1.3;">{subtitle}</p>'
            f'<p style="margin:16px 0 0;color:#2a6f7a;font-size:20px;font-weight:700;'
            f'letter-spacing:0.08em;">{section_label}</p>',
            72, 214, 640,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;">Prof. Rebin Muhammad</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Montgomery College</p>',
            72, 560, 560,
        ),
        visual,
    ], notes)


FONT = "Montserrat, sans-serif"


def _esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _panel(width, height):
    return (
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>'
    )


def bell_at(left, top, width, height, heading="", mean=0.0, sd=1.0, shade=None,
            marks=(), shade_label="", z0=-3.2, z1=3.2, pins=True):
    """A bell in the book's units. shade is (lo, hi); None means the edge of the window.
    marks are (value, label) in the same units as the mean."""
    pad_l, pad_r, pad_t, pad_b = 32, 20, 40, 36
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base = pad_t + plot_h
    label_size = 16 if width >= 520 else 14

    def X(z):
        return pad_l + (z - z0) / (z1 - z0) * plot_w

    def Y(z):
        return pad_t + 4 + (1 - math.exp(-0.5 * z * z)) * (plot_h - 6)

    def z_of(x):
        return (x - mean) / sd

    steps = 90
    zs = [z0 + i * (z1 - z0) / steps for i in range(steps + 1)]
    parts = [
        _panel(width, height),
        f'<text x="18" y="26" font-size="13" fill="#2a6f7a" font-family="{FONT}" '
        f'font-weight="700" letter-spacing="1.2">{_esc(heading)}</text>',
        f'<line x1="{X(z0):.1f}" y1="{base:.1f}" x2="{X(z1):.1f}" y2="{base:.1f}" '
        f'stroke="#d5e0de" stroke-width="1.6"></line>',
    ]
    if shade:
        lo = z0 if shade[0] is None else max(z0, min(z1, z_of(shade[0])))
        hi = z1 if shade[1] is None else max(z0, min(z1, z_of(shade[1])))
        band = [z for z in zs if lo <= z <= hi]
        if band:
            poly = " ".join(
                [f"{X(band[0]):.1f},{base:.1f}"]
                + [f"{X(z):.1f},{Y(z):.1f}" for z in band]
                + [f"{X(band[-1]):.1f},{base:.1f}"]
            )
            parts.append(f'<polygon points="{poly}" fill="#d7ebe8"></polygon>')
            for edge in (band[0], band[-1]):
                if z0 + 0.05 < edge < z1 - 0.05:
                    parts.append(
                        f'<line x1="{X(edge):.1f}" y1="{Y(edge):.1f}" x2="{X(edge):.1f}" y2="{base:.1f}" '
                        f'stroke="#2a6f7a" stroke-width="2"></line>'
                    )
            if shade_label:
                mid = (band[0] + band[-1]) / 2
                room = base - Y(mid)
                # A flat tail has no room inside the curve, so the words sit just above the axis.
                y = (Y(mid) + base) / 2 if room > 90 else base - 24
                parts.append(
                    f'<text x="{X(mid):.1f}" y="{y:.1f}" text-anchor="middle" font-size="{label_size}" '
                    f'fill="#1c242c" font-family="{FONT}" font-weight="700">{_esc(shade_label)}</text>'
                )
    parts.append(
        f'<polyline points="{" ".join(f"{X(z):.1f},{Y(z):.1f}" for z in zs)}" '
        f'fill="none" stroke="#2a6f7a" stroke-width="2.6"></polyline>'
    )
    placed = []
    for value, label in marks:
        z = z_of(value)
        if z < z0 - 0.02 or z > z1 + 0.02:
            continue
        placed.append((X(z), Y(z), label))
    placed.sort()
    for i, (x, y, label) in enumerate(placed):
        anchor = "middle"
        if i and x - placed[i - 1][0] < 64:
            anchor = "start"
        if i + 1 < len(placed) and placed[i + 1][0] - x < 64 and anchor == "middle":
            anchor = "end"
        if pins:
            parts.append(
                f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{base:.1f}" '
                f'stroke="#2a6f7a" stroke-width="1.6"></line>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#2a6f7a"></circle>'
            )
        parts.append(
            f'<text x="{x:.1f}" y="{height - 12}" text-anchor="{anchor}" font-size="{label_size}" '
            f'fill="#1c242c" font-family="{FONT}" font-weight="650">{_esc(label)}</text>'
        )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def bell(width, height, heading, shade=None, marks=(), shade_label=""):
    """The title-slide bell. Marks are already in z-scores."""
    return bell_at(760, 110, width, height, heading, shade=shade, marks=marks,
                   shade_label=shade_label, pins=False)


def hop_line(left, top, width, height):
    """The book's own check: center 5, step 2, three steps land on 11."""
    values = [5, 7, 9, 11]
    pad_l, pad_r = 64, 64
    y = 210
    xs = [pad_l + i * (width - pad_l - pad_r) / 3 for i in range(4)]
    parts = [
        _panel(width, height),
        f'<text x="18" y="32" font-size="13" fill="#2a6f7a" font-family="{FONT}" '
        f'font-weight="700" letter-spacing="1.2">CENTER 5, ONE STEP IS 2</text>',
        f'<line x1="{xs[0]:.0f}" y1="{y}" x2="{xs[-1]:.0f}" y2="{y}" stroke="#d5e0de" stroke-width="3"></line>',
    ]
    for i, (x, value) in enumerate(zip(xs, values)):
        parts.append(
            f'<circle cx="{x:.0f}" cy="{y}" r="8" fill="#2a6f7a"></circle>'
            f'<text x="{x:.0f}" y="118" text-anchor="middle" font-size="32" fill="#1c242c" '
            f'font-family="{FONT}" font-weight="650">{value}</text>'
            f'<text x="{x:.0f}" y="268" text-anchor="middle" font-size="18" fill="#5d6670" '
            f'font-family="{FONT}">z = {i}</text>'
        )
        if i:
            mid = (xs[i - 1] + x) / 2
            parts.append(
                f'<text x="{mid:.0f}" y="168" text-anchor="middle" font-size="16" fill="#2a6f7a" '
                f'font-family="{FONT}" font-weight="700">+2</text>'
            )
    parts.append(
        f'<text x="{width / 2:.0f}" y="340" text-anchor="middle" font-size="18" fill="#1c242c" '
        f'font-family="{FONT}">5 + 3(2) = 11, so z = 3</text>'
    )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def scale_line(left, top, width, height, lo, hi, points, heading, foot):
    """points are (value, name, detail). detail sits under the axis, name above."""
    pad_l, pad_r = 90, 80
    y = 150

    def X(v):
        return pad_l + (v - lo) / (hi - lo) * (width - pad_l - pad_r)

    parts = [
        _panel(width, height),
        f'<text x="18" y="28" font-size="13" fill="#2a6f7a" font-family="{FONT}" '
        f'font-weight="700" letter-spacing="1.2">{_esc(heading)}</text>',
        f'<line x1="{X(lo):.0f}" y1="{y}" x2="{X(hi):.0f}" y2="{y}" stroke="#d5e0de" stroke-width="3"></line>',
    ]
    for value, name, detail in points:
        x = X(value)
        parts.append(
            f'<line x1="{x:.0f}" y1="{y - 46}" x2="{x:.0f}" y2="{y}" stroke="#2a6f7a" stroke-width="2"></line>'
            f'<circle cx="{x:.0f}" cy="{y}" r="8" fill="#2a6f7a"></circle>'
            f'<text x="{x:.0f}" y="{y - 58}" text-anchor="middle" font-size="22" fill="#1c242c" '
            f'font-family="{FONT}" font-weight="650">{_esc(name)}</text>'
            f'<text x="{x:.0f}" y="{y + 36}" text-anchor="middle" font-size="16" fill="#5d6670" '
            f'font-family="{FONT}">{_esc(detail)}</text>'
        )
    parts.append(
        f'<text x="{width / 2:.0f}" y="{height - 24}" text-anchor="middle" font-size="18" fill="#1c242c" '
        f'font-family="{FONT}">{_esc(foot)}</text>'
    )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def slides_61():
    out = []
    out.append(opening(
        "The bell curve",
        "Most values sit near the mean.<br>A z-score says how many steps away.",
        "SECTION 6.1",
        bell(460, 480, "THE BELL", shade=(-1, 1), shade_label="most",
             marks=[(-2, "−2"), (-1, "−1"), (0, "mean"), (1, "+1"), (2, "+2")]),
        "Say: the mean and the standard deviation are the ones from Unit 2. The new picture is a bell. A distribution is only the pattern of the values. A normal distribution is this bell. "
        "Point at the peak and call it the mean. Point at one tick and call it one step, one standard deviation. "
        "Do not say random variable, density, or probability on this slide. Probability is the next deck. "
        "About 25 minutes for 6.1, then 6.2 in the same hour. Thursday and Friday are Exam 1, Units 1 through 3 only. Skip the class-height activity in the book.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Before any formula")
            + b.title("The center, the step, the pattern", 44),
            64, 36, 1150,
        ),
        bell_at(64, 168, 1152, 430, "WHERE THE VALUES SIT", shade=(-1, 1), shade_label="most values",
                marks=[(-1, "one step left"), (0, "mean"), (1, "one step right")]),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'The mean is the center. One standard deviation is one step. The distribution is this pattern: most values near the mean, few far out.</p>',
            64, 620, 1150,
        ),
    ], "Point at the peak and say mean. Point from the peak to the next tick and say one step, the standard deviation from Unit 2. "
       "The shaded middle is where most values sit. The two tails are the few. "
       "Say the three words out loud. Mean is the center. Standard deviation is one step. Distribution means the pattern, not a formula. "
       "Ask: where do most of the values sit? Near the middle. "
       "If someone asks what X means later, say X is one value drawn from this pattern. Do not build a definition of a random variable."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The only new arithmetic")
            + b.title("How many steps, and which value", 40),
            64, 36, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">HOW MANY STEPS</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:30px;">' + M(r"z = \frac{x - \mu}{\sigma}") + '</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">μ is the mean. σ is one step. The sign is the side.</p>'
            '<p style="margin:22px 0 0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">WHICH VALUE</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:30px;">' + M(r"x = \mu + z\sigma") + '</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Start at the mean. Add the steps.</p>',
            64, 160, 500,
        ),
        hop_line(590, 160, 626, 400),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;">Read ' + m(r"X \sim N(\mu, \sigma)") + ' as a bell with that center and that step.</p>',
            64, 600, 520,
        ),
    ], "Say: z is not a new kind of data. It is the number of steps from the mean. Do the book’s check on the board: start at 5, three steps of 2, land on 11. "
       "Then read the shorthand once: X ~ N(μ, σ) means a normal bell with that center and that step. Z ~ N(0, 1) is the bell whose center is 0 and whose step is 1. "
       "Watch for: students treating μ and σ as two more variables to solve for. They are given. x is the value. z is the steps."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.1")
            + b.title("Mean 5, one step is 6", 44),
            64, 28, 1150,
        ),
        bell_at(64, 155, 760, 420, "MEAN 5, STEP 6", mean=5, sd=6,
                marks=[(1, "1"), (5, "5"), (17, "17")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;"><b>17 is z = 2.</b> Two steps of 6 above 5. Check: 5 + 2(6) = 17.</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:22px;line-height:1.35;"><b>1 is z = −0.67.</b> (1 − 5) / 6 = −0.666…, below the mean. The book rounds to −0.67.</p>'
            '<p style="margin:16px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Positive is the right side. Negative is the left side.</p>',
            850, 180, 370,
        ),
        b.desmos_line("(17-5)/6 &nbsp;&nbsp; (1-5)/6", 600),
    ], "Say: cover the formula and ask how many steps of 6 it takes to get from 5 to 17. Two. Then show (17−5)/6 = 2 so the formula matches the count. "
       "For 1, the subtraction comes out negative, so the value is below the mean. (1−5)/6 = −0.666…, book −0.67. "
       "The check 5 + (−0.67)(6) is about 1, not exactly 1, because −0.67 was rounded. "
       "Watch for: a positive 0.67. The sign is the side."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.2 · pounds lost in a month")
            + b.title("Average loss 5, one step is 2", 40),
            64, 28, 1150,
        ),
        scale_line(
            64, 170, 1152, 300, -5, 12,
            [(-3, "−3", "gained 3 lb"), (5, "5", "average loss"), (10, "10", "lost 10 lb")],
            "POUNDS LOST. A GAIN IS NEGATIVE.",
            "(10 − 5) / 2 = 2.5 steps right.    (−3 − 5) / 2 = −4 steps left.",
        ),
        b.desmos_line("(10-5)/2 &nbsp;&nbsp; (-3-5)/2", 510),
    ], "Say: the average person loses 5 pounds. One step is 2 pounds. Ten pounds lost is 2.5 steps above that average, (10−5)/2 = 2.5. "
       "A gain of 3 pounds is a negative loss, so the value is −3, not 3. (−3−5)/2 = −4, four steps below the average. "
       "Watch for: students who use +3 and get (3−5)/2 = −1. Ask which side of 'no change' a gain sits on. The book calls the variable weight lost, so a gain is negative."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.2 · two different scales")
            + b.title("The same z can be a different x", 40),
            64, 36, 1150,
        ),
        bell_at(64, 155, 370, 400, "17 POUNDS", mean=5, sd=6, marks=[(5, "5"), (17, "17")]),
        bell_at(455, 155, 370, 400, "4 POUNDS", mean=2, sd=1, marks=[(2, "2"), (4, "4")]),
        bell_at(846, 155, 370, 400, "JEROME, 10 POINTS", mean=16, sd=4, marks=[(10, "10"), (16, "16")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '17 and 4 are different numbers. Both sit two steps above their own average, so both have z = 2. Jerome is 1.5 steps below 16, so z = −1.5.</p>',
            64, 575, 1150,
        ),
    ], "Say: 17 and 4 are different numbers, and both people are equally far above their own average. z is what makes the comparison fair. "
       "(17−5)/6 = 2 and (4−2)/1 = 2. "
       "Jerome is Try It 6.2. The book already gives z = −1.5. Have someone finish the sentence: 1.5 steps to the left of 16. Do not make it a timed turn. "
       "The book’s shorthand is X ~ N(5, 6) and Y ~ N(2, 1). Read it if you write it down. Do not ask them to memorize the tilde."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 6.1 · 3 minutes",
            "One value, one z-score",
            "The center is 12 and one step is 3. How many steps is the value 1 from 12, and which side?",
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:30px;">' + M(r"z = \frac{1 - 12}{3}") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Find z. The picture shows the side. It does not show the number of steps.</p>',
            64, 200, 500,
        ),
        bell_at(600, 190, 616, 360, "CENTER 12, STEP 3", mean=12, sd=3, z0=-4.2, z1=3.2,
                marks=[(1, "1"), (12, "12")]),
        b.desmos_line("(1-12)/3", 590),
    ], "Try It 6.1. The book writes X ~ N(12, 3). Walk it: 1 − 12 = −11, then divide by the step 3. z = −11/3 = −3.67, to the left of 12. "
       "A student who says 3.67 forgot the sign. A student who says −11 forgot to divide by 3. Give them three minutes, then show the next slide."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 6.1")
            + b.title("z = −3.67", 56),
            64, 48, 1150,
        ),
        bell_at(64, 175, 700, 420, "3.67 STEPS TO THE LEFT", mean=12, sd=3, z0=-4.2, z1=3.2,
                shade=(None, 1), marks=[(1, "1"), (12, "12")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:26px;">' + M(r"\frac{1-12}{3} = -\frac{11}{3} = -3.67") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">1 − 12 = −11. Divide by the step, 3. The sign says left.</p>',
            800, 230, 416,
        ),
    ], "Say the arithmetic once, slowly: 1 minus 12 is negative 11. Negative 11 divided by 3 is negative 3.67. Left of 12. Then sit down and go to the heights."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.3 · young men in Chile, 2009–2010")
            + b.title("Mean height 170 cm, step 6.28", 40),
            64, 28, 1150,
        ),
        bell_at(64, 150, 1152, 400, "BOTH HEIGHTS ARE NEAR THE CENTER", mean=170, sd=6.28,
                marks=[(168, "168"), (170, "170"), (177.98, "177.98")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '(168 − 170) / 6.28 = −0.32, a little below average. &nbsp;&nbsp; 170 + 1.27(6.28) = 177.98 cm.</p>',
            64, 570, 1150,
        ),
        b.desmos_line("(168-170)/6.28 &nbsp;&nbsp; 170+1.27*6.28", 620),
    ], "Say: same two moves, and now the step is not a whole number. From a height, count the steps. From the steps, recover the height. "
       "(168−170)/6.28 = −0.318…, and the book rounds to −0.32. 170 + 1.27(6.28) = 177.98 cm. "
       "If someone asks about Example 6.4: a 1984 height and a 2009 height can both be z = −1.5, so they are equally far below their own year’s average. "
       "Try It 6.4, only if asked: SAT 325 is z = −1.5 exactly, (325−496)/114. The score 366.21 is z = −1.14, not the same."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.5 · the 68-95-99.7 rule")
            + b.title("Mean 50, standard deviation 6", 44),
            64, 28, 1150,
        ),
        bell_at(64, 145, 370, 400, "68 OUT OF 100", mean=50, sd=6, shade=(44, 56), shade_label="one step",
                marks=[(44, "44"), (50, "50"), (56, "56")]),
        bell_at(455, 145, 370, 400, "95 OUT OF 100", mean=50, sd=6, shade=(38, 62), shade_label="two steps",
                marks=[(38, "38"), (50, "50"), (62, "62")]),
        bell_at(846, 145, 370, 400, "99.7 OUT OF 100", mean=50, sd=6, shade=(32, 68), shade_label="three steps",
                marks=[(32, "32"), (50, "50"), (68, "68")]),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;">The shaded middle is the share of people, not a test score. 50 − 6 = 44 and 50 + 6 = 56.</p>',
            64, 565, 1150,
        ),
    ], "Say: this percent is a share of the people, not a test score. About 68 out of 100 values sit between 44 and 56. "
       "Hold your hands near the middle for 68, wider for 95, and almost the whole curve for 99.7. "
       "50 − 6 = 44 and 50 + 6 = 56. Two steps is 12, so 38 to 62. Three steps is 18, so 32 to 68. "
       "Example 6.6 is the same rule on the 1984 Chile heights, mean 172.36 and step 6.34: 166.02 to 178.7, then 159.68 to 185.04, then 153.34 to 191.38. Leave it unless you have time."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 6.5 · 2 minutes",
            "Where do 68% of the values sit?",
            "Center 25, one step is 5. About 68 out of 100 values sit between which two numbers?",
        ),
        bell_at(64, 200, 620, 400, "THE MIDDLE SHARE", mean=25, sd=5, shade=(20, 30),
                shade_label="68 out of 100", marks=[(25, "25")]),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.4;">One step below 25, and one step above 25.</p>'
            '<p class="fragment" style="margin:16px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">20 and 30</p>'
            '<p class="fragment" style="margin:8px 0 0;color:#5d6670;font-size:20px;">25 − 5 = 20 and 25 + 5 = 30.</p>',
            180,
        ), 720, 250, 490, 180),
    ], "Try It 6.5. They should not start a z formula. One step below 25 is 20. One step above is 30. "
       "If someone says 20 and 25, they only walked one direction. "
       "Try It 6.6, only if the room is ahead: center 52, step 11. 68% is 41 to 63, 95% is 30 to 74, 99.7% is 19 to 85."))
    out.append(b.quick("Read the sign", [
        ("A value above the mean has z",
         [("A", "Positive"), ("B", "Negative"), ("C", "Zero")], "A",
         "Right of the mean."),
        ("Mean 5, step 6. The value 17 has",
         [("A", "z = 2"), ("B", "z = 12"), ("C", "z = 0.67")], "A",
         "(17 − 5) / 6 = 2."),
        ("About 95% of the values lie within",
         [("A", "1 sd"), ("B", "2 sd"), ("C", "3 sd")], "B",
         "68, 95, 99.7."),
    ], "Answers: 1A, 2A, 3B. If several people pick z = 12, they subtracted and forgot to divide by the step. Do (17−5)/6 on the board before you leave. "
       "Homework is items 60 through 66. Item 67 starts the area work."))
    out.append(b.closing(
        "Before section 6.2",
        "You can place a value on the curve",
        [
            "z is how many steps a value sits from the mean. The sign says which side.",
            "About 68, 95, and 99.7 out of 100 values sit within 1, 2, and 3 steps.",
            "Next, that share of the bell is a probability.",
        ],
        ("6.2 Area", "Same class. The probability is the shaded region."),
        "Homework: OpenStax 6.1, items 60 through 66.",
        "Open 6.2 in the same hour, as soon as the 68-95-99.7 picture has been said once. Do not add another example here.",
    ))
    return out


def slides_62():
    out = []
    out.append(opening(
        "Chance is a share",
        "The shaded part is a share of everyone.<br>1 means 100%. Half the bell is 0.50.",
        "SECTION 6.2",
        bell(460, 480, "A SHARE OF THE BELL", shade=(-3.2, 0.4), shade_label="the chance"),
        "Say: this is the first time the word probability means something in this course. It is the shaded share of the bell. The whole bell is 1, which is 100%. Half is 0.50, which is 50%. A probability is never bigger than 1. "
        "Move your hand over the shaded side and call that the chance a value lands there. "
        "A percentile is the Unit 2 word: a cutoff with a given share of the people on one side. "
        "Desmos, not the book’s TI buttons. cdf asks for an area. inversecdf asks for the cutoff. "
        "Less-than and less-than-or-equal are the same area on a smooth curve. Say that only if someone asks. "
        "About 30 minutes. If you are short, stop after the golf scores. The phone ages can wait. Exam Thursday and Friday is still Units 1, 2, and 3.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.7 · read a decimal as a percent")
            + b.title("The two shares add to 100%", 40),
            64, 36, 1150,
        ),
        bell_at(64, 150, 1152, 400, "A SMALL PIECE AND THE REST", shade=(None, -2), shade_label="2.28%"),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '0.0228 is 2.28%. The rest is 1 − 0.0228 = 0.9772, which is 97.72%. They add to 100%. '
            'Try It 6.7 is the same picture: 0.012 is 1.2%, so the right share is 0.988, or 98.8%.</p>',
            64, 570, 1150,
        ),
    ], "Say: a probability in this chapter is a decimal from 0 to 1. To hear it as a percent, move the decimal two places. 0.0228 is 2.28%, a small chance. 0.9772 is 97.72%, almost certain. The line in the picture is z = −2, because that is the table area. The book does not name an x for this one. "
       "Have them add 0.0228 + 0.9772 and see 1. That is the whole bell. "
       "Try It 6.7 is the same move: 0.012 is 1.2% on the left, so the right side is 0.988, or 98.8%. "
       "The book writes P(X < x) for the left share. Read it as 'the chance a value is under x.' Do not stop on the symbol."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.8 · final exams, mean 63, step 5")
            + b.title("The chance of a score over 65", 40),
            64, 24, 1150,
        ),
        bell_at(64, 140, 1152, 390, "THE SHADED SIDE IS THE QUESTION", mean=63, sd=5,
                shade=(65, None), shade_label="about 34%", marks=[(63, "63"), (65, "65")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            '(65 − 63) / 5 = 0.4. The left share is 0.6554, and 1 − 0.6554 = 0.3446, about one student in three. '
            'cdf is the left share, so subtract it from 1.</p>',
            64, 545, 1150,
        ),
        b.desmos_line("1 - normaldist(63,5).cdf(65)", 620),
    ], "Say: translate before you admire the decimal. 0.3446 is about 34.5%, about one student in three. A score over 65 is ordinary, because 65 is less than one step above the average of 63. "
       "(65−63)/5 = 0.4. The book’s table area to the left of that is 0.6554, and 1 − 0.6554 = 0.3446. "
       "Type the Desmos line yourself. Tell them cdf means the left share, so the 1 minus is the question they were asked. "
       "They do not need the z-score to get the area. The z-score only explains why the chance is not small. "
       "Watch for: students who report 0.6554. That is the share who scored 65 or under."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.8 · the same exams")
            + b.title("A sure thing, and two cutoffs", 40),
            64, 28, 1150,
        ),
        bell_at(64, 145, 560, 380, "90% AT OR BELOW 69.4", mean=63, sd=5,
                shade=(None, 69.4), shade_label="90%", marks=[(63, "63"), (69.4, "69.4")]),
        bell_at(656, 145, 560, 380, "70% AT OR BELOW 65.6", mean=63, sd=5,
                shade=(None, 65.6), shade_label="70%", marks=[(63, "63"), (65.6, "65.6")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            'A percentile is a cutoff, not a chance. 85 is about four steps above 63, so the share under 85 is about 100%. The book rounds it to 1.</p>',
            64, 545, 1150,
        ),
        b.desmos_line("normaldist(63,5).inversecdf(0.90)", 610),
    ], "Say: under 85 is not a serious question. Four steps above the average catches essentially everyone, so the chance is about 100%, and the book rounds the area to 1. "
       "A percentile is not a chance. It is a cutoff. The 90th percentile, 69.4, means 90 out of 100 scores are that or lower. Same word as Unit 2. "
       "Desmos: normaldist(63,5).inversecdf(0.90). You hand it the share 0.90 and it hands back the score. The book’s TI command is invNorm(0.90, 63, 5). Do not teach the buttons. "
       "The 70th percentile is 65.6. One sentence in the book says 65.5. The calculator line says 65.6. Use 65.6. "
       "Watch for: students who think 69.4 is a probability. Ask: is 69.4 between 0 and 1? No. It is a score."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 6.8 · 3 minutes",
            "The chance of a score under 65",
            "The average golf score is 68. One step is 3. What share of golfers score under 65?",
        ),
        bell_at(64, 190, 700, 390, "SHADE THE LEFT OF 65", mean=68, sd=3,
                shade=(None, 65), shade_label="find this share", marks=[(65, "65"), (68, "68")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">65 is one step below 68. Write the share to the left of 65 as a decimal.</p>',
            790, 230, 420,
        ),
        b.desmos_line("normaldist(68,3).cdf(65)", 600),
    ], "Try It 6.8. The book does not print this answer. Give them the Desmos line and three minutes. "
       "A strong student sees z = (65−68)/3 = −1 before they type anything: one step below the mean, so the left tail outside the middle 68% is about 16%. "
       "The precise share is 0.1587. If they report 0.84, they found the share who scored over 65."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 6.8")
            + b.title("About 16%", 56),
            64, 40, 1150,
        ),
        bell_at(64, 155, 760, 420, "ONE STEP BELOW THE MEAN", mean=68, sd=3,
                shade=(None, 65), shade_label="about 16%", marks=[(65, "65"), (68, "68")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:26px;">' + M(r"z = \frac{65-68}{3} = -1") + '</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">The precise share is 0.1587, which is 15.87%.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">The middle 68% leaves about 16% on each side. The book does not print this Try It.</p>',
            850, 200, 370,
        ),
    ], "Say: one step below the average is the edge of the middle 68, so each tail is about half of the remaining 32, about 16%. Desmos makes it precise: 0.1587. "
       "Then ask what 0.1587 is as a percent. 15.87%. That translation is the skill."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.9 · hours a home computer is used")
            + b.title("Average 2 hours, step half an hour", 36),
            64, 28, 1150,
        ),
        bell_at(64, 145, 1152, 390, "THE SHARE BETWEEN THE TWO HOURS", mean=2, sd=0.5,
                shade=(1.8, 2.75), shade_label="about 59%",
                marks=[(1.8, "1.8"), (2, "2"), (2.75, "2.75")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            'The book’s area is 0.5886. The bottom quartile, the Unit 2 cutoff, is 1.66 hours. A quarter of households are under it.</p>',
            64, 550, 1150,
        ),
        b.desmos_line("normaldist(2,0.5).cdf(1.8,2.75)", 615),
    ], "Say: 0.5886 is about 59 out of 100 households. The two numbers in cdf are the ends of the interval, not a mean and a step. Mean 2 and step 0.5 are inside normaldist. "
       "1.66 hours is a cutoff, the 25th percentile. A quarter of the households are under it. If you show the command: normaldist(2,0.5).inversecdf(0.25). "
       "Try It 6.9 is golf again, the share between 66 and 70. That area is 0.4950, about half. Skip it if the first golf turn was enough. "
       "Watch for: typing cdf(2, 0.5) as if those were the hours. Those are the center and the step."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.11 · smartphone users, ages 13 to 55+")
            + b.title("Average age 36.9, step 13.9", 40),
            64, 24, 1150,
        ),
        bell_at(64, 140, 1152, 360, "THE MIDDLE HALF OF THE AGES", mean=36.9, sd=13.9,
                shade=(27.5246, 46.2754), shade_label="half",
                marks=[(27.5246, "Q1"), (36.9, "36.9"), (46.2754, "Q3")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            'Q1 is 27.5246 years. Q3 is 46.2754. The IQR is 18.8 years. Forty percent are 40.4 or older, so hand Desmos the left share 0.60.</p>',
            64, 520, 1150,
        ),
        b.desmos_line("normaldist(36.9,13.9).inversecdf(0.60)", 590),
    ], "This slide can wait if the hour is gone. Say: these are the quartiles from Unit 2, found on a bell instead of a list. "
       "The book prints Q1 = 27.5246 and Q3 = 46.2754. Subtract: 46.2754 − 27.5246 = 18.75, and the book rounds the IQR to 18.8 years. "
       "Forty percent at least 40.4 means the right share is 0.40, so you hand Desmos the left share 0.60. inversecdf(0.60) = 40.4215, and the book rounds to 40.4. "
       "The trap is handing Desmos 0.40 and getting the age that has 40% younger, which is the wrong side. "
       "Example 6.10, only if asked: between 23 and 64.7 is 0.8186, at most 50.8 is 0.8413, the 80th percentile is 48.6 years. "
       "Example 6.12, mandarin oranges, center 5.85 cm and step 0.24: the chance a diameter is over 6 cm is 0.2660, the middle 20% runs from 5.79 to 5.91 cm, and the 90th percentile is 6.16 cm."))
    out.append(b.quick("Area or percentile", [
        ("Left area 0.012. The right area is",
         [("A", "0.012"), ("B", "0.988"), ("C", "1.012")], "B",
         "1 − 0.012."),
        ("The chance a final is over 65",
         [("A", "About 34%"), ("B", "About 66%"), ("C", "The score 69.4")], "A",
         "0.3446 is about 34%. 66% scored under 65."),
        ("The 90th percentile of those scores is",
         [("A", "63"), ("B", "65"), ("C", "69.4")], "C",
         "90% score 69.4 or below."),
    ], "Answers: 1B, 2A, 3C. For 2, say the sentence: about 34 out of 100 score over 65. The 66% is the other side. 69.4 is a cutoff, not a chance. "
       "Homework is items 67 through 80."))
    out.append(b.closing(
        "Before the exam",
        "You can find an area, and a percentile",
        [
            "A probability is a share of the bell. Move the decimal two places and it is a percent.",
            "cdf asks Desmos for that share. inversecdf turns a share into the cutoff.",
            "Exam 1 is Thursday and Friday. It does not include this unit.",
        ],
        ("7.1 Sample means", "After the exam. The mean of a sample, not one person."),
        "Homework: OpenStax 6.2, items 67 through 80. Unit 4 is due November 16.",
        "Items 67 to 80 are the area homework. Items 81 to 88 use the raw waiting-time and stadium data in sections 6.3 and 6.4, which this unit skips. "
        "Exam 1 is Thursday and Friday and still covers Units 1, 2, and 3 only. Section 7.1 is not on Exam 1. "
        "Unit 4 homework, the unit test, and the discussion are due Monday, November 16.",
    ))
    return out


DECKS = [
    ("6.1-standard-normal", "math117-6-1-standard-normal", "MATH 117 · 6.1 The standard normal",
     "A z-score counts standard deviations from the mean.", slides_61),
    ("6.2-normal-area", "math117-6-2-normal-area", "MATH 117 · 6.2 Area under the curve",
     "The probability is the area. A percentile goes back to x.", slides_62),
]


def main():
    for folder, slug, title, description, builder in DECKS:
        b.write_deck(folder, slug, title, description, builder)


if __name__ == "__main__":
    main()
