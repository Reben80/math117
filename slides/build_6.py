"""Unit 4, sections 6.1 and 6.2, taught together on November 11.

OpenStax Introductory Statistics 2e. Sections 6.3 and 6.4 are not on the
calendar. Every number is from the book. Section 7.1 is the next lecture.
"""

import math

import build_2_2_to_2_7 as b

# Saved in the instructor's Desmos account. Built from desmos_graphs.js.
b.GRAPHS["6.2"] = "https://www.desmos.com/calculator/xa9guvmgpd"


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


def opening(h1, subtitle, section_label, visual, notes, unit_line="Unit 4 · The normal distribution"):
    return b.section([
        MATH_STYLE,
        b.backdrop(),
        b.text_block(
            '<p style="margin:0;">'
            '<span style="color:#ffffff;background:#2a6f7a;padding:6px 12px;'
            'letter-spacing:0.12em;font-weight:700;font-size:16px;">MATH 117</span>'
            '<span style="color:#5d6670;font-size:20px;"> &nbsp; ' + unit_line + '</span></p>',
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
            marks=(), shade_label="", z0=-3.2, z1=3.2, pins=True, label_size=None,
            extras=(), label_gap=64):
    """A bell in the book's units. shade is (lo, hi); None means the edge of the window.
    marks are (value, label) in the same units as the mean. A label may contain a newline.
    extras are (z, text) labels inside the plot."""
    stacked = any("\n" in str(label) for _, label in marks)
    pad_l, pad_r, pad_t, pad_b = 32, 20, 40, (70 if stacked else 36)
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base = pad_t + plot_h
    if label_size is None:
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
    for z, text in extras:
        if z0 < z < z1:
            room = base - Y(z)
            y = (Y(z) + base) / 2 if room > 90 else base - 24
            parts.append(
                f'<text x="{X(z):.1f}" y="{y:.1f}" text-anchor="middle" font-size="{label_size}" '
                f'fill="#1c242c" font-family="{FONT}" font-weight="700">{_esc(text)}</text>'
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
        if i and x - placed[i - 1][0] < label_gap:
            anchor = "start"
        if i + 1 < len(placed) and placed[i + 1][0] - x < label_gap and anchor == "middle":
            anchor = "end"
        if pins:
            parts.append(
                f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{base:.1f}" '
                f'stroke="#2a6f7a" stroke-width="1.6"></line>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#2a6f7a"></circle>'
            )
        lines = str(label).split("\n")
        line_h = label_size + 4
        for j, line in enumerate(lines):
            yy = height - 12 - (len(lines) - 1 - j) * line_h
            parts.append(
                f'<text x="{x:.1f}" y="{yy:.1f}" text-anchor="{anchor}" font-size="{label_size}" '
                f'fill="#1c242c" font-family="{FONT}" font-weight="650">{_esc(line)}</text>'
            )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def bell(width, height, heading, shade=None, marks=(), shade_label="", label_gap=64):
    """The title-slide bell. Marks are already in z-scores."""
    return bell_at(760, 110, width, height, heading, shade=shade, marks=marks,
                   shade_label=shade_label, pins=False, label_gap=label_gap)


def hop_line(left, top, width, height):
    """Mean 5, standard deviation 2. x = 5, 7, 9, 11 and z = 0, 1, 2, 3."""
    values = [5, 7, 9, 11]
    pad_l, pad_r = 72, 48
    y = 198
    xs = [pad_l + i * (width - pad_l - pad_r) / 3 for i in range(4)]
    parts = [
        _panel(width, height),
        f'<text x="18" y="28" font-size="13" fill="#2a6f7a" font-family="{FONT}" '
        f'font-weight="700" letter-spacing="1.1">MEAN 5, STANDARD DEVIATION 2</text>',
        f'<line x1="{xs[0]:.0f}" y1="{y}" x2="{xs[-1]:.0f}" y2="{y}" stroke="#d5e0de" stroke-width="3"></line>',
        f'<text x="16" y="112" font-size="13" fill="#5d6670" font-family="{FONT}" font-weight="700">x</text>',
    ]
    for i, (x, value) in enumerate(zip(xs, values)):
        parts.append(
            f'<circle cx="{x:.0f}" cy="{y}" r="8" fill="#2a6f7a"></circle>'
            f'<text x="{x:.0f}" y="112" text-anchor="middle" font-size="30" fill="#1c242c" '
            f'font-family="{FONT}" font-weight="650">{value}</text>'
            f'<text x="{x:.0f}" y="248" text-anchor="middle" font-size="18" fill="#5d6670" '
            f'font-family="{FONT}">z = {i}</text>'
        )
        if i:
            mid = (xs[i - 1] + x) / 2
            parts.append(
                f'<text x="{mid:.0f}" y="158" text-anchor="middle" font-size="15" fill="#2a6f7a" '
                f'font-family="{FONT}" font-weight="700">+2</text>'
                f'<text x="{mid:.0f}" y="176" text-anchor="middle" font-size="13" fill="#2a6f7a" '
                f'font-family="{FONT}">1 SD</text>'
            )
    parts.append(
        f'<text x="{width / 2:.0f}" y="308" text-anchor="middle" font-size="16" fill="#1c242c" '
        f'font-family="{FONT}">Each move of 2 is one standard deviation.</text>'
        f'<text x="{width / 2:.0f}" y="336" text-anchor="middle" font-size="16" fill="#1c242c" '
        f'font-family="{FONT}">z = (11 − 5) / 2 = 3, and x = 5 + 3(2) = 11</text>'
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
        "The mean is the center.<br>"
        "The standard deviation tells how<br>spread out the values are.<br>"
        "One standard deviation is one step from the mean.",
        "SECTION 6.1",
        bell(460, 480, "THE BELL", shade=(-1, 1), shade_label="most",
             marks=[(-2, "−2"), (-1, "−1"), (0, "mean"), (1, "+1"), (2, "+2")],
             label_gap=36),
        "Say: the mean is the center of this bell. The standard deviation tells how spread out the values are. "
        "One standard deviation can be thought of as one step away from the mean. A z-score counts those standard deviations. "
        "Point at the peak and call it the mean. Point from the peak to the next tick and call it one standard deviation. The shade is where most values sit. "
        "Do not say random variable, density, or probability on this slide. Probability is the next deck. "
        "Watch for: hearing 'step' as a new unit, separate from the standard deviation. "
        "About 25 minutes for 6.1, then 6.2 in the same hour. Thursday and Friday are Exam 1, Units 1 through 3 only. Skip the class-height activity in the book.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Before any formula")
            + b.title("The center, the step, the pattern", 44),
            64, 28, 1150,
        ),
        bell_at(64, 158, 1152, 420, "WHERE THE VALUES SIT", shade=(-1, 1), shade_label="most values",
                marks=[(-1, "1 SD below"), (0, "mean"), (1, "1 SD above")], label_gap=36),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'The mean is the center of the distribution. The standard deviation tells how spread out the values are. '
            'One standard deviation is one step away from the mean.</p>',
            64, 600, 1150,
        ),
    ], "Point at the peak: that is the mean, the center. The width of the bell is the standard deviation, how spread out the values are. "
       "Then say one standard deviation is one step from the mean, left or right. The shaded middle is where most values sit. The tails are the few. "
       "Ask: where do most of the values sit? Near the mean. "
       "Watch for: calling the spread a step before connecting it to the standard deviation from Unit 2. "
       "If someone asks what X means later, say x is an individual value from this pattern. Do not build a definition of a random variable."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The only new arithmetic")
            + b.title("How many standard deviations, and which value", 36),
            64, 24, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">HOW MANY STANDARD DEVIATIONS</p>'
            '<p style="margin:4px 0 0;color:#1c242c;font-size:28px;">' + M(r"z = \frac{x - \mu}{\sigma}") + '</p>'
            '<p style="margin:2px 0 0;color:#5d6670;font-size:18px;line-height:1.3;">μ population mean. σ population standard deviation. x an individual value. z how many standard deviations from the mean. Positive is above the mean. Negative is below.</p>'
            '<p style="margin:14px 0 0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">WHICH VALUE</p>'
            '<p style="margin:4px 0 0;color:#1c242c;font-size:28px;">' + M(r"x = \mu + z\sigma") + '</p>'
            '<p style="margin:2px 0 0;color:#5d6670;font-size:18px;line-height:1.3;">Start at the mean. Move z standard deviations.</p>',
            64, 140, 510,
        ),
        hop_line(590, 148, 626, 400),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;line-height:1.3;">Read '
            + m(r"X \sim N(\mu, \sigma)")
            + ' as a bell with that mean and that standard deviation.</p>',
            64, 640, 520,
        ),
    ], "Say: z is not a new measurement. It is how many standard deviations the individual value x is from the mean. "
       "μ is the population mean. σ is the population standard deviation. They are given. "
       "Positive z is above the mean. Negative z is below the mean. "
       "To find z, subtract the mean and divide by σ. To find x, start at the mean and add z times σ. "
       "The number line is mean 5, standard deviation 2. x = 5 is z = 0, x = 7 is z = 1, x = 9 is z = 2, x = 11 is z = 3. Each move of 2 is one standard deviation. "
       "On the board: (11 − 5) / 2 = 3, and 5 + 3(2) = 11. "
       "Watch for: forgetting to divide by σ, so 11 − 5 = 6 and they call that z. "
       "Read X ~ N(μ, σ) once, as a bell with that mean and that standard deviation. Do not ask them to memorize the tilde."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.1")
            + b.title("Mean 5, standard deviation 6", 40),
            64, 28, 1150,
        ),
        bell_at(64, 155, 760, 420, "MEAN 5, SD 6", mean=5, sd=6,
                marks=[(1, "1"), (5, "mean\n5"), (17, "17")], label_gap=36),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;"><b>17 is z = 2.</b> The standard deviation is 6, so 17 is two steps above the mean 5. Check: 5 + 2(6) = 17.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;"><b>1 is z = −0.67.</b> (1 − 5) / 6 = −0.666…, below the mean. The book rounds to −0.67.</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">A positive z-score is above the mean. A negative z-score is below the mean.</p>',
            850, 175, 370,
        ),
        b.desmos_line("(17-5)/6 &nbsp;&nbsp; (1-5)/6", 600),
    ], "The peak is the mean, 5. The standard deviation is 6. Point at 17, two standard deviations above the mean: (17−5)/6 = 2. The check is 5 + 2(6) = 17. "
       "Point at 1, on the left of the mean: (1−5)/6 = −0.666…, and the book rounds to −0.67. A positive z-score is above the mean. A negative z-score is below the mean. "
       "Watch for: a positive 0.67, which drops the sign, or z = 12, which forgets to divide by σ. "
       "The check 5 + (−0.67)(6) is about 1, not exactly 1, because −0.67 was rounded."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.2 · pounds lost in a month")
            + b.title("Mean loss 5, standard deviation 2", 40),
            64, 28, 1150,
        ),
        scale_line(
            64, 160, 1152, 340, -5, 12,
            [(-3, "−3", "gained 3 lb"), (5, "5", "mean"), (10, "10", "lost 10 lb")],
            "POUNDS LOST. MEAN 5, SD 2. A GAIN IS NEGATIVE.",
            "(10 − 5) / 2 = 2.5 SD above the mean.    (−3 − 5) / 2 = −4 SD below.",
        ),
        b.desmos_line("(10-5)/2 &nbsp;&nbsp; (-3-5)/2", 530),
    ], "The mean is an average loss of 5 pounds. The standard deviation is 2 pounds. "
       "Ten pounds lost is above the mean: (10−5)/2 = 2.5. A positive z-score is above the mean. "
       "A gain of 3 pounds is a negative loss, so the value is −3, not +3. (−3−5)/2 = −4, below the mean. A negative z-score is below the mean. "
       "Watch for: treating a gain of 3 pounds as +3 and getting (3−5)/2 = −1. Ask which side of no change a gain sits on. The book calls the variable weight lost, so a gain is negative."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.2 · two different scales")
            + b.title("The same z can be a different x", 40),
            64, 28, 1150,
        ),
        bell_at(64, 148, 370, 390, "17 LB · MEAN 5, SD 6", mean=5, sd=6,
                marks=[(5, "mean\n5"), (17, "17")], label_gap=36),
        bell_at(455, 148, 370, 390, "4 LB · MEAN 2, SD 1", mean=2, sd=1,
                marks=[(2, "mean\n2"), (4, "4")], label_gap=36),
        bell_at(846, 148, 370, 390, "JEROME · MEAN 16, SD 4", mean=16, sd=4,
                marks=[(10, "10"), (16, "mean\n16")], label_gap=36),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
            '17 pounds and 4 pounds are different values. Both are 2 standard deviations above their own mean, so both have z = 2. '
            'The same z-score is the same standardized distance, even when the original values differ. '
            'Jerome’s 10 is 1.5 standard deviations below the mean 16, so z = −1.5.</p>',
            64, 558, 1150,
        ),
    ], "Three bells, three means. 17 pounds: mean 5, standard deviation 6, (17−5)/6 = 2. "
       "4 pounds: mean 2, standard deviation 1, (4−2)/1 = 2. The original values differ. The z-score is the same, so each value is the same standardized distance: two standard deviations above its own mean. "
       "Jerome’s mean is 16 and his score is 10. (10−16)/4 = −1.5, below the mean. The book already gives z = −1.5. "
       "Watch for: deciding 17 and 4 cannot both be z = 2 because the numbers differ, or flipping Jerome’s sign to +1.5. "
       "The book’s shorthand is X ~ N(5, 6) and Y ~ N(2, 1). Read it if you write it down. Do not ask them to memorize the tilde."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 6.1 · 3 minutes",
            "One value, one z-score",
            "The mean is 12 and the standard deviation is 3. How many standard deviations is the value 1 from the mean, and which side?",
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:30px;">' + M(r"z = \frac{1 - 12}{3}") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Find z. The picture shows the side of the mean. It does not show how many standard deviations.</p>',
            64, 210, 510,
        ),
        bell_at(600, 200, 616, 360, "MEAN 12, SD 3", mean=12, sd=3, z0=-4.2, z1=3.2,
                marks=[(1, "1"), (12, "mean\n12")], label_gap=36),
        b.desmos_line("(1-12)/3", 590),
    ], "Try It 6.1. Mean 12, standard deviation 3, individual value 1. The dot for 1 is in the left tail, so z will be negative. The picture does not show the count. "
       "After they work: 1 − 12 = −11, then divide by σ, which is 3. z = −11/3 = −3.67. "
       "Watch for: 3.67 with the wrong sign, or −11 from forgetting to divide by σ. Give them three minutes, then show the next slide."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 6.1")
            + b.title("z = −3.67", 56),
            64, 40, 1150,
        ),
        bell_at(64, 168, 700, 430, "3.67 SD BELOW THE MEAN", mean=12, sd=3, z0=-4.2, z1=3.2,
                shade=(None, 1), marks=[(1, "1"), (12, "mean\n12")], label_gap=36),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:26px;">' + M(r"\frac{1-12}{3} = -\frac{11}{3} = -3.67") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">1 − 12 = −11.<br>Divide by the standard deviation, 3.<br>A negative z-score is below the mean.</p>',
            790, 220, 430,
        ),
    ], "The peak is the mean, 12. The value 1 is far down the left tail. Say the arithmetic once: 1 minus 12 is −11. −11 divided by the standard deviation 3 is −11/3, which is −3.67. "
       "A negative z-score is below the mean. Watch for: dropping the minus, or stopping at −11 because they forgot to divide by σ. Then go to the heights."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.3 · young men in Chile, 2009–2010")
            + b.title("Mean height 170 cm, standard deviation 6.28", 36),
            64, 22, 1150,
        ),
        bell_at(64, 140, 1152, 400, "MEAN 170, SD 6.28", mean=170, sd=6.28,
                marks=[(168, "168"), (170, "mean\n170"), (177.98, "177.98")], label_gap=36),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
            '(168 − 170) / 6.28 = −0.32, below the mean. &nbsp;&nbsp; 170 + 1.27(6.28) = 177.98 cm, above the mean.</p>',
            64, 558, 1150,
        ),
        b.desmos_line("(168-170)/6.28 &nbsp;&nbsp; 170+1.27*6.28", 612),
    ], "The peak is the mean height, 170 cm. The standard deviation is 6.28 cm. 168 is just left of the mean: (168−170)/6.28 = −0.318…, and the book rounds to −0.32. A negative z-score is below the mean. "
       "The other direction starts from z and finds the value: 170 + 1.27(6.28) = 177.98 cm, above the mean. "
       "Watch for: subtracting in the wrong order and reporting +0.32, or adding 1.27 to 170 without multiplying by σ. "
       "If someone asks about Example 6.4: a 1984 height and a 2009 height can both be z = −1.5, the same standardized distance below their own year’s mean. "
       "Try It 6.4, only if asked: SAT 325 is z = −1.5 exactly, (325−496)/114. The score 366.21 is z = −1.14, not the same."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.5 · the 68-95-99.7 rule")
            + b.title("Mean 50, standard deviation 6", 40),
            64, 20, 1150,
        ),
        bell_at(64, 128, 370, 378, "ABOUT 68%", mean=50, sd=6, shade=(44, 56), shade_label="1 SD",
                marks=[(44, "44"), (50, "50"), (56, "56")], label_gap=36),
        bell_at(455, 128, 370, 378, "ABOUT 95%", mean=50, sd=6, shade=(38, 62), shade_label="2 SD",
                marks=[(38, "38"), (50, "50"), (62, "62")], label_gap=36),
        bell_at(846, 128, 370, 378, "ABOUT 99.7%", mean=50, sd=6, shade=(32, 68), shade_label="3 SD",
                marks=[(32, "32"), (50, "50"), (68, "68")], label_gap=36),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.3;">'
            'For an approximately normal distribution, about 68% of the values fall within 1 standard deviation of the mean, about 95% within 2, and about 99.7% within 3.</p>'
            '<p style="margin:6px 0 0;color:#1c242c;font-size:20px;line-height:1.3;">'
            'Mean 50, standard deviation 6: 68% is 44 to 56, 95% is 38 to 62, and 99.7% is 32 to 68.</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:18px;line-height:1.3;">'
            'The shaded middle is a share of the values, not a test score.</p>',
            64, 520, 1150,
        ),
    ], "This rule is for an approximately normal distribution. The shaded middle is a share of the values, not a test score. "
       "About 68% fall within 1 standard deviation of the mean, about 95% within 2, about 99.7% within 3. "
       "Mean 50, standard deviation 6. 50 − 6 = 44 and 50 + 6 = 56, so 68% is 44 to 56. Two standard deviations is 12, so 95% is 38 to 62. Three is 18, so 99.7% is 32 to 68. "
       "Hold your hands near the middle, then wider, then almost the whole curve. "
       "Watch for: walking only one direction, so 50 to 56 instead of 44 to 56, or reading 68 as a score. "
       "Example 6.6 is the same rule on the 1984 Chile heights, mean 172.36 and standard deviation 6.34: 166.02 to 178.7, then 159.68 to 185.04, then 153.34 to 191.38. Leave it unless you have time."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 6.5 · 2 minutes",
            "Where do about 68% of the values fall?",
            "Mean 25, standard deviation 5. Between which two values do about 68% of the observations fall?",
        ),
        bell_at(64, 200, 620, 400, "ABOUT 68%", mean=25, sd=5, shade=(20, 30),
                shade_label="about 68%", marks=[(25, "mean\n25")], label_gap=36),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">Mean 25. Standard deviation 5.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">25 − 5 = 20 and 25 + 5 = 30.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">20 to 30</p>',
            188,
        ), 720, 250, 490, 188),
    ], "Try It 6.5. Mean 25, standard deviation 5. About 68% of the observations fall within 1 standard deviation of the mean, in both directions. "
       "25 − 5 = 20 and 25 + 5 = 30, so the answer is 20 to 30. They should not start a z formula, and this is not an area calculation. "
       "Watch for: walking only one direction and answering 20 to 25, or 25 to 30. "
       "Try It 6.6, only if the room is ahead: mean 52, standard deviation 11. 68% is 41 to 63, 95% is 30 to 74, 99.7% is 19 to 85."))
    out.append(b.quick("Read the sign", [
        ("A value above the mean has a z-score that is",
         [("A", "Positive"), ("B", "Negative"), ("C", "Zero")], "A",
         "Positive means above the mean."),
        ("Mean 5, standard deviation 6. Value 17 has",
         [("A", "z = 2"), ("B", "z = 12"), ("C", "z = 0.67")], "A",
         "(17 − 5) / 6 = 2."),
        ("About 95% of observations fall within",
         [("A", "1 SD"), ("B", "2 SD"), ("C", "3 SD")], "B",
         "Within 2 standard deviations."),
    ], "Answers: 1A, 2A, 3B. A value above the mean has a positive z-score. Mean 5, standard deviation 6, value 17: (17−5)/6 = 2. "
       "About 95% of observations fall within 2 standard deviations of the mean. "
       "Watch for: z = 12, which forgets to divide by σ, and z = 0.67, which divides in the wrong order. "
       "Do (17−5)/6 on the board before you leave. Homework is items 60 through 66. Item 67 starts the area work in 6.2."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Before section 6.2")
            + b.title("You can place a value on the curve", 40),
            72, 36, 1130,
        ),
        b.text_block(
            '<p style="margin:0 0 10px;color:#1c242c;font-size:23px;line-height:1.28;">'
            '1 &nbsp; A normal distribution is described by its mean and standard deviation.</p>'
            '<p style="margin:0 0 10px;color:#1c242c;font-size:23px;line-height:1.28;">'
            '2 &nbsp; A z-score tells how many standard deviations a value is above or below the mean.</p>'
            '<p style="margin:0 0 10px;color:#1c242c;font-size:23px;line-height:1.28;">'
            '3 &nbsp; The 68–95–99.7 rule describes how values are distributed around the mean.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.32;">'
            'In Section 6.1, we learned where a value is on the normal curve. '
            'In Section 6.2, we will use the area under the curve to calculate probabilities.</p>',
            72, 168, 1136,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">NEXT</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:28px;font-weight:650;">6.2 Area</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;">Same class. The probability is the shaded region.</p>',
            118,
        ), 72, 470, 690, 118),
        b.link_card(
            "https://www.desmos.com/notebook/pzbf94y26h",
            792, 470, 416, 140, "NOTEBOOK",
            "The same examples, as a short lesson.", qr=84,
        ),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;">Homework: OpenStax 6.1, items 60 through 66.</p>',
            72, 628, 690,
        ),
    ], "Three things they should leave with. A normal distribution is described by its mean and standard deviation. "
       "A z-score tells how many standard deviations a value is above or below the mean. "
       "The 68–95–99.7 rule describes how values sit around the mean, for an approximately normal distribution. "
       "Then say: in Section 6.1 we learned where a value is on the curve. In Section 6.2 the area under the curve is used to calculate probabilities. "
       "The notebook card is the same examples as a short lesson. There is no class calculator for 6.1. "
       "Do not start an area problem here. Open 6.2 in the same hour. Homework is OpenStax 6.1, items 60 through 66."))
    return out


def desmos_how(command, how, top, graph="6.2"):
    """Monospace is what students type. The rest is the Desmos box."""
    label = '<span style="color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">DESMOS ↗</span>'
    if graph in b.GRAPHS:
        label = '<a href="' + b.GRAPHS[graph] + '" target="_blank" style="text-decoration:none;">' + label + '</a>'
    return b.text_block(
        '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
        + label
        + '&nbsp;&nbsp;<span style="font-family:Menlo, Consolas, monospace;">' + command + '</span>'
        '&nbsp;&nbsp;<span style="color:#5d6670;">' + how + '</span></p>',
        64, top, 1160,
    )


def slides_62():
    out = []
    out.append(opening(
        "Probability is an area",
        "The shaded area under the curve is the probability.<br>The whole curve has area 1, which is 100%.",
        "SECTION 6.2",
        bell(460, 480, "A SHARE OF THE BELL", shade=(-3.2, 0.4), shade_label="the area"),
        "Say: a probability is an area under the curve. Run your hand over the shade and call that the probability a value lands there. The whole curve has area 1, which is 100%. Half the bell is 0.50, or 50%. A probability is never bigger than 1. "
        "Standard deviation is the spread, the step from chapter 6.1. Use the word standard deviation first. "
        "cdf starts with a score and returns an area. inversecdf starts with an area and returns a score. "
        "Less-than and less-than-or-equal are the same area on a smooth curve. Say that only if someone asks. "
        "About 30 minutes. If you are short, stop after the golf scores. The phone ages can wait.",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.7 · read a decimal as a percent")
            + b.title("The two areas add to 100%", 40),
            64, 24, 1150,
        ),
        bell_at(64, 145, 1152, 370, "THE SHADE, AND THE REST OF THE CURVE", shade=(None, -2),
                shade_label="2.28%", extras=[(0.7, "97.72%")], label_size=20),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            + m(r"P(X > a) = 1 - P(X \le a)") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'The shade is 0.0228, or 2.28%. The rest is 1 − 0.0228 = 0.9772, or 97.72%.</p>',
            64, 535, 1150,
        ),
    ], "Point at the shade: that small left piece is 0.0228, which is 2.28%. The unshaded rest of the curve is the complement, 1 − 0.0228 = 0.9772. Have them add the two decimals and get 1, the whole area. "
       "The line is z = −2. The book does not name an x for this picture. Write P(X > a) = 1 − P(X ≤ a) once. On a smooth curve, less-than and less-than-or-equal have the same area. "
       "Try It 6.7, only if asked: 0.012 is 1.2% on the left, so the right area is 0.988, or 98.8%. "
       "This is a probability: the shade is an area. A percentile question would hand back a score instead."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.8 · final exams, mean 63, sd 5")
            + b.title("The probability of a score over 65", 36),
            64, 20, 1150,
        ),
        bell_at(64, 125, 1152, 370, "THE SHADED AREA IS P(X > 65)", mean=63, sd=5,
                shade=(65, None), shade_label="0.3446", marks=[(63, "63"), (65, "65")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
            + m(r"P(X > 65) = 1 - P(X \le 65) = 1 - 0.6554 = 0.3446") + '. '
            'About 34%. This is a probability. 69.4 and 65.6, later, are scores.</p>',
            64, 515, 1150,
        ),
        desmos_how("normaldist(63, 5)", "then Right from 65", 580),
    ], "The shade is the right tail, the probability of a score over 65. 65 is only 0.4 standard deviations above 63, so the area is not small. "
       "The area to the left is 0.6554. Subtract from 1: 0.3446, about 34 out of 100. In Desmos, type only normaldist(63, 5), then choose Right from 65. Choosing Left and forgetting to subtract gives 0.6554, the wrong side. "
       "69.4 and 65.6 are not this answer. Those are percentiles, scores, on the later slide."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Two different questions")
            + b.title("Start with a score, or start with an area", 36),
            64, 20, 1150,
        ),
        bell_at(64, 118, 560, 350, "CDF · SCORE → AREA", shade=(None, 0.5),
                shade_label="the area", marks=[(0.5, "score")]),
        bell_at(656, 118, 560, 350, "INVERSECDF · AREA → SCORE", shade=(None, 1.28),
                shade_label="90%", marks=[(1.28, "score")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
            'cdf is score → area, usually the area to the left. The same command also gives a right tail, or the area between two values. '
            'inversecdf is area → score.</p>',
            64, 490, 1150,
        ),
    ], "Left graph: score → area. You know the score. The shade is the unknown probability. That is cdf, usually the left area. The same Desmos box also does a right tail, or the area between two values. "
       "Right graph: area → score. You know 90%. The score is the unknown edge. That is inversecdf. These pictures use no book data. "
       "Misconception: using inversecdf when the problem already gives the score."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.8 · the same exams")
            + b.title("Finding a score from a percentile", 36),
            64, 20, 1150,
        ),
        bell_at(64, 125, 560, 360, "90% AT OR BELOW 69.4", mean=63, sd=5,
                shade=(None, 69.4), shade_label="90%", marks=[(63, "63"), (69.4, "69.4")]),
        bell_at(656, 125, 560, 360, "70% AT OR BELOW 65.6", mean=63, sd=5,
                shade=(None, 65.6), shade_label="70%", marks=[(63, "63"), (65.6, "65.6")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
            'What score has 90% of students at or below it? That score is 69.4, the 90th percentile. '
            'The 70th percentile is 65.6. These are scores, not probabilities.</p>',
            64, 505, 1150,
        ),
        desmos_how("normaldist(63, 5).inversecdf(0.90)", "gives the score 69.4", 575),
    ], "Ask: what score has 90% of students at or below it? Point at the shade, then at the edge. The shade is the 90% you were given. The edge, 69.4, is the score. That is the opposite of finding a probability. "
       "inversecdf(0.90) returns 69.4. The 70th percentile is inversecdf(0.70) = 65.6. One sentence in the book says 65.5. Use 65.6. "
       "If someone asks about a score over 85: that is a probability, about 1, because 85 is about four standard deviations above 63. It is not a percentile. "
       "Misconception: calling 69.4 a probability. Ask whether 69.4 is between 0 and 1. It is a score."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 6.8 · 3 minutes",
            "The probability of a score under 65",
            "Mean 68, standard deviation 3. What share of golfers score under 65?",
        ),
        bell_at(64, 185, 700, 370, "SHADE THE LEFT OF 65", mean=68, sd=3,
                shade=(None, 65), shade_label="find this area", marks=[(65, "65"), (68, "68")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">65 is one standard deviation below 68. The shade is the probability to the left of 65.</p>',
            790, 220, 420,
        ),
        desmos_how("normaldist(68, 3)", "then Left, to 65", 590),
    ], "Try It 6.8. Three minutes. The worked answer is the next slide. "
       "They type normaldist(68, 3), then Left to 65. A strong student sees z = (65−68)/3 = −1 first: one standard deviation below the mean, so the left tail is about 16%. "
       "The precise probability is 0.1587. If they report about 0.84, they found the area above 65. "
       "The score 65 is given, so this is a probability. inversecdf is the other question: the area is given and the score is unknown."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 6.8")
            + b.title("About 16%", 56),
            64, 36, 700,
        ),
        bell_at(64, 155, 740, 400, "ONE STANDARD DEVIATION BELOW", mean=68, sd=3,
                shade=(None, 65), shade_label="about 16%", marks=[(65, "65"), (68, "68")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:26px;">' + M(r"z = \frac{65-68}{3} = -1") + '</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">The probability is 0.1587, which is 15.87%.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Under this normal model, about 16% of golfers score below 65.</p>',
            830, 190, 390,
        ),
    ], "Point at 65, one standard deviation below 68. The shade is the left tail. The middle 68% leaves about 32% split into two tails, so each is about 16%. Desmos makes it 0.1587, or 15.87%. "
       "Say: under this normal model, about 16% of golfers score below 65. The precise probability is 0.1587. Ask them to move the decimal two places. "
       "The shade is the probability. A percentile question would have given about 16% and asked for the score."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.9 · hours a home computer is used")
            + b.title("Mean 2 hours, standard deviation 0.5", 34),
            64, 18, 1150,
        ),
        bell_at(64, 120, 560, 340, "PROBABILITY BETWEEN 1.8 AND 2.75", mean=2, sd=0.5,
                shade=(1.8, 2.75), shade_label="0.5886",
                marks=[(1.8, "1.8"), (2, "2"), (2.75, "2.75")]),
        bell_at(656, 120, 560, 340, "A DIFFERENT TASK: THE 1ST QUARTILE", mean=2, sd=0.5,
                shade=(None, 1.66), shade_label="25%",
                marks=[(1.66, "1.66"), (2, "2")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
            'First the probability: the book’s area between 1.8 and 2.75 is 0.5886, about 59%. '
            'Then a cutoff: the first quartile is 1.66 hours, with 25% of households at or below it.</p>',
            64, 480, 1150,
        ),
        desmos_how("normaldist(2, 0.5)", "then Inner, 1.8 to 2.75", 560),
        desmos_how("normaldist(2, 0.5).inversecdf(0.25)", "gives the quartile 1.66", 600),
    ], "Do the interval first. The shade between 1.8 and 2.75 is a probability, 0.5886, about 59 out of 100 households. Type normaldist(2, 0.5), then Inner from 1.8 to 2.75. The two hours go in the area box. The mean and standard deviation go inside normaldist. "
       "Only after that, the quartile. inversecdf(0.25) is a cutoff, 1.66 hours. A quarter of the households are at or below it. "
       "Try It 6.9, only if asked: golf again, between 66 and 70, area 0.4950. "
       "Misconception: typing the hours 2 and 0.5 as the interval."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.11 · smartphone users, ages 13 to 55+")
            + b.title("Mean age 36.9, standard deviation 13.9", 34),
            64, 18, 1150,
        ),
        bell_at(64, 112, 1152, 360, "Q1 AND Q3, THE MIDDLE HALF", mean=36.9, sd=13.9,
                shade=(27.52, 46.28), shade_label="half", label_size=18,
                marks=[(27.52, "Q1\n27.52"), (36.9, "36.9"), (46.28, "Q3\n46.28")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
            'The shaded half runs from Q1 = 27.52 to Q3 = 46.28. The IQR is 18.8 years. '
            'Forty percent are 40.4 or older, so 60% are to the left. Use inversecdf(0.60).</p>',
            64, 490, 1150,
        ),
        desmos_how("normaldist(36.9, 13.9).inversecdf(0.60)", "gives about 40.4", 560),
    ], "This slide can wait if the hour is gone. The shade is the middle half, from the first quartile to the third. The book prints Q1 = 27.5246 and Q3 = 46.2754. The graph rounds those to 27.52 and 46.28. The difference is 18.75, and the book rounds the IQR to 18.8 years. "
       "The 40.4 question is separate. Forty percent are at least 40.4, so the area to the left of that age is 60%. inversecdf(0.60) = 40.4215, and the book rounds to 40.4. "
       "The trap is typing 0.40. That returns the age with 40% younger, the wrong side. "
       "Q1, Q3, and 40.4 are cutoffs, so use inversecdf. A probability question would start with an age and return an area. "
       "Example 6.10, only if asked: between 23 and 64.7 is 0.8186, at most 50.8 is 0.8413, the 80th percentile is 48.6. "
       "Example 6.12, only if asked: mandarin oranges, mean 5.85 cm, standard deviation 0.24. Over 6 cm is 0.2660. The 90th percentile is 6.16 cm."))
    out.append(b.quick("Area or percentile", [
        ("Left area 0.012. The right area is",
         [("A", "0.012"), ("B", "0.988"), ("C", "1.012")], "B",
         "1 − 0.012."),
        ("The probability a final is over 65 is",
         [("A", "About 34%"), ("B", "About 66%"), ("C", "About 90%")], "A",
         "0.3446 is about 34%. 90% is a percentile."),
        ("The 90th percentile of those scores is",
         [("A", "63"), ("B", "65"), ("C", "69.4")], "C",
         "90% of scores are 69.4 or below."),
    ], "Answers: 1B, 2A, 3C. For question 2, every choice is a probability. About 34% score over 65. About 66% is the other side. About 90% belongs to the percentile question, whose answer is the score 69.4. "
       "Homework is items 67 through 80."))
    out.append(b.closing(
        "Before you leave",
        "Area, cutoff, and spread",
        [
            "A probability is an area. Use cdf.",
            "A percentile is a cutoff. Use inversecdf.",
            "The standard deviation measures the spread.",
        ],
        ("7.1 Sample means", "The mean of a sample, not one person."),
        "Homework: OpenStax 6.2, items 67 through 80. Unit 4 is due November 16.",
        "cdf: type normaldist, then choose Left, Right, or Inner. inversecdf returns the score. "
        "The calculator card is the class graph. The notebook card is the same examples as a short lesson. "
        "Items 81 to 88 are sections 6.3 and 6.4, which this unit skips. "
        "Unit 4 homework, the unit test, and the discussion are due Monday, November 16.",
        graph="6.2",
        notebook="https://www.desmos.com/notebook/s3ainmd7q6",
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
