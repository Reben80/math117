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


def bell(width, height, heading, shade=None, marks=()):
    """A standard normal sketch. shade is (z0, z1). marks are (z, label)."""
    left, right, top, bottom = 28, 18, 46, 40
    z0, z1 = -3.2, 3.2
    plot_w = width - left - right
    plot_h = height - top - bottom
    base = top + plot_h

    def X(z):
        return left + (z - z0) / (z1 - z0) * plot_w

    def Y(z):
        peak = math.exp(0)
        height_used = plot_h - 10
        return top + 8 + (1 - math.exp(-0.5 * z * z) / peak) * height_used

    steps = 80
    zs = [z0 + i * (z1 - z0) / steps for i in range(steps + 1)]
    curve = " ".join(f"{X(z):.1f},{Y(z):.1f}" for z in zs)
    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="20" y="30" font-size="13" fill="#2a6f7a" font-family="Montserrat, sans-serif" '
        f'font-weight="700" letter-spacing="1.2">{heading}</text>',
        f'<line x1="{X(z0):.1f}" y1="{base:.1f}" x2="{X(z1):.1f}" y2="{base:.1f}" '
        f'stroke="#d5e0de" stroke-width="1.4"></line>',
    ]
    if shade:
        a, c = shade
        band = [z for z in zs if a <= z <= c]
        if band:
            poly = " ".join(
                [f"{X(band[0]):.1f},{base:.1f}"]
                + [f"{X(z):.1f},{Y(z):.1f}" for z in band]
                + [f"{X(band[-1]):.1f},{base:.1f}"]
            )
            parts.append(f'<polygon points="{poly}" fill="#d7ebe8"></polygon>')
            parts.append(
                f'<line x1="{X(c):.1f}" y1="{Y(c):.1f}" x2="{X(c):.1f}" y2="{base:.1f}" '
                f'stroke="#2a6f7a" stroke-width="2"></line>'
            )
    parts.append(
        f'<polyline points="{curve}" fill="none" stroke="#2a6f7a" stroke-width="2.6"></polyline>'
    )
    for z, label in marks:
        parts.append(
            f'<line x1="{X(z):.1f}" y1="{base:.1f}" x2="{X(z):.1f}" y2="{base + 6:.1f}" '
            f'stroke="#5d6670" stroke-width="1.4"></line>'
            f'<text x="{X(z):.1f}" y="{height - 10}" text-anchor="middle" font-size="14" '
            f'fill="#5d6670" font-family="Montserrat, sans-serif">{label}</text>'
        )
    return b.drawing(b.svg_wrap("".join(parts), width, height), 760, 110, width, height)


def slides_61():
    out = []
    out.append(opening(
        "The bell curve",
        "Most values sit near the mean.<br>A z-score says how many steps away.",
        "SECTION 6.1",
        bell(460, 480, "THE BELL", marks=[(-2, "−2"), (-1, "−1"), (0, "0"), (1, "+1"), (2, "+2")]),
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
        *b.three_cards([
            ("The mean", "The center", "The same mean as Unit 2. On the bell it sits under the highest point."),
            ("The standard deviation", "One step", "A typical distance from the center. A bigger step makes a wider bell."),
            ("The distribution", "The pattern", "Normal means the bell. Most values are near the mean. Few are far out."),
        ], 200, 270),
    ], "Say the three words out loud and tie each one to Unit 2. Mean is the center. Standard deviation is one step. Distribution means the pattern, not a formula. "
       "Ask: where do most of the values sit? Near the middle. "
       "If someone asks what X means later, say X is one value drawn from this pattern. Do not build a definition of a random variable."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The only new arithmetic")
            + b.title("How many steps, and which value", 40),
            64, 36, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">HOW MANY STEPS</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;">' + M(r"z = \frac{x - \mu}{\sigma}") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'μ is the mean. σ is one step. Positive is above the mean. Negative is below it.</p>',
            230,
        ), 64, 190, 560, 230),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">WHICH VALUE</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;">' + M(r"x = \mu + z\sigma") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'Start at the mean. Add the steps. One step above the mean is z = 1.</p>',
            230,
        ), 656, 190, 560, 230),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'Read ' + m(r"X \sim N(\mu, \sigma)") + ' as: a bell, center μ, step σ. The book’s check: center 5 and step 2 puts 11 at z = 3, because 5 + 3(2) = 11.</p>',
            64, 450, 1150,
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
        *b.three_cards([
            ("The value 17", "z = 2", "Two steps of 6 above 5. Check it: 5 + 2(6) = 17."),
            ("The value 1", "z = −0.67", "Below 5. (1 − 5) / 6 is −0.666…, and the book rounds to −0.67."),
            ("The sign", "Which side", "Positive means above the mean. Negative means below the mean."),
        ], 200, 250),
        b.desmos_line("(17-5)/6 &nbsp;&nbsp; (1-5)/6", 500),
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
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">LOST 10 POUNDS</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:32px;font-weight:650;">z = 2.5</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            '2.5 standard deviations to the right of the mean 5.</p>',
            250,
        ), 64, 190, 560, 250),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">GAINED 3 POUNDS</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:32px;font-weight:650;">z = −4</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'A gain is x = −3. Four standard deviations to the left of 5.</p>',
            250,
        ), 656, 190, 560, 250),
        b.desmos_line("(10-5)/2 &nbsp;&nbsp; (-3-5)/2", 490),
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
        *b.three_cards([
            ("First group", "17 pounds, z = 2", "Center 5, step 6. Two of its own steps above its own mean."),
            ("Second group", "4 pounds, z = 2", "Center 2, step 1. Also two of its own steps above its own mean."),
            ("Jerome", "10 points, z = −1.5", "Center 16, step 4. A game of 10 is 1.5 steps below his own mean."),
        ], 210, 280),
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
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:28px;">' + M(r"z = \frac{1 - 12}{3}") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">Find z. Then say whether 1 is left or right of 12.</p>',
            160,
        ), 72, 250, 1136, 160),
        b.desmos_line("(1-12)/3", 460),
    ], "Try It 6.1. The book writes X ~ N(12, 3). Walk it: 1 − 12 = −11, then divide by the step 3. z = −11/3 = −3.67, to the left of 12. "
       "A student who says 3.67 forgot the sign. A student who says −11 forgot to divide by 3. Give them three minutes, then show the next slide."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 6.1")
            + b.title("z = −3.67", 56),
            64, 48, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:26px;">' + M(r"\frac{1-12}{3} = -\frac{11}{3} = -3.67") + '</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            'The value 1 is 3.67 steps to the left of the center 12. The sign is the side.</p>',
            200,
        ), 64, 230, 1150, 200),
    ], "Say the arithmetic once, slowly: 1 minus 12 is negative 11. Negative 11 divided by 3 is negative 3.67. Left of 12. Then sit down and go to the heights."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.3 · young men in Chile, 2009–2010")
            + b.title("Mean height 170 cm, step 6.28", 40),
            64, 28, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">168 CM</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:32px;font-weight:650;">z = −0.32</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'A little below average. 0.32 of a step to the left of 170.</p>',
            230,
        ), 64, 190, 560, 230),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">z = 1.27</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:32px;font-weight:650;">177.98 cm</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            '1.27 steps above 170. The book’s height is 177.98 cm.</p>',
            230,
        ), 656, 190, 560, 230),
        b.desmos_line("(168-170)/6.28 &nbsp;&nbsp; 170+1.27*6.28", 470),
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
        *b.three_cards([
            ("About 68%", "44 to 56", "About 68 out of 100 values, within one step of 50."),
            ("About 95%", "38 to 62", "Within two steps. The z-scores are −2 and +2."),
            ("About 99.7%", "32 to 68", "Within three steps. Almost every value. Almost nobody is farther out."),
        ], 200, 250),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;">50 − 6 = 44 and 50 + 6 = 56. The other two rows use 12 and 18.</p>',
            72, 490, 1100,
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
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.4;">One step below 25, and one step above 25.</p>'
            '<p class="fragment" style="margin:16px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">20 and 30</p>'
            '<p class="fragment" style="margin:8px 0 0;color:#5d6670;font-size:20px;">25 − 5 = 20 and 25 + 5 = 30. The z-scores are −1 and +1.</p>',
            200,
        ), 72, 250, 1136, 200),
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
        bell(460, 480, "A SHARE OF THE BELL", shade=(-3.2, 0.4)),
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
        *b.three_cards([
            ("A small share", "2.28%", "The book’s area 0.0228. Move the decimal two places: 2.28 out of 100."),
            ("Almost everyone", "97.72%", "1 − 0.0228 = 0.9772. The two shares add to 1, which is 100%."),
            ("Try It 6.7", "98.8%", "A left share of 0.012 is 1.2%. The right share is 1 − 0.012 = 0.988."),
        ], 210, 250),
    ], "Say: a probability in this chapter is a decimal from 0 to 1. To hear it as a percent, move the decimal two places. 0.0228 is 2.28%, a small chance. 0.9772 is 97.72%, almost certain. "
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
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">The book’s answer is 0.3446. That is about 34.5%, about one student in three.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            '65 is only 0.4 steps above 63, so a score over 65 is common. The share to the left of 65 is 0.6554, and 1 − 0.6554 = 0.3446.</p>',
            230,
        ), 64, 170, 1150, 230),
        b.desmos_line("1 - normaldist(63,5).cdf(65)", 440),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:18px;line-height:1.4;">'
            'cdf means the share to the left. Subtract that from 1 to get the share to the right. Desmos shows more decimals. The book rounds to 0.3446.</p>',
            64, 510, 1150,
        ),
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
        *b.three_cards([
            ("Under 85", "About 100%", "85 is 4.4 steps above 63. The left share is essentially the whole bell. The book rounds it to 1."),
            ("90th percentile", "69.4", "The cutoff from Unit 2. 90% of the scores are 69.4 or lower."),
            ("70th percentile", "65.6", "70% of the scores are 65.6 or lower. 30% are higher."),
        ], 200, 250),
        b.desmos_line("normaldist(63,5).inversecdf(0.90)", 500),
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
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.4;">65 is one step below 68. Find the share to the left of 65. Write the decimal.</p>',
            140,
        ), 72, 250, 1136, 140),
        b.desmos_line("normaldist(68,3).cdf(65)", 440),
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
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.45;">'
            + M(r"z = \frac{65 - 68}{3} = -1") + '</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">'
            '65 is one step below 68, so this is the left tail. The precise share is 0.1587, about 16%.</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'The middle 68% leaves about 16% on each side. The book does not print this Try It.</p>',
            250,
        ), 64, 200, 1150, 250),
    ], "Say: one step below the average is the edge of the middle 68, so each tail is about half of the remaining 32, about 16%. Desmos makes it precise: 0.1587. "
       "Then ask what 0.1587 is as a percent. 15.87%. That translation is the skill."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 6.9 · hours a home computer is used")
            + b.title("Average 2 hours, step half an hour", 36),
            64, 28, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">BETWEEN 1.8 AND 2.75</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:32px;font-weight:650;">About 59%</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'The book’s area is 0.5886. That is the share of households between 1.8 and 2.75 hours.</p>',
            230,
        ), 64, 180, 560, 230),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">BOTTOM QUARTILE</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:32px;font-weight:650;">1.66 hours</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">'
            'The first quartile from Unit 2. A quarter of households use it less than 1.66 hours.</p>',
            230,
        ), 656, 180, 560, 230),
        b.desmos_line("normaldist(2,0.5).cdf(1.8,2.75)", 460),
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
        *b.three_cards([
            ("First quartile", "27.5246 years", "25 out of 100 users are this age or younger. The Unit 2 quartile."),
            ("Third quartile", "46.2754 years", "75 out of 100 are this age or younger. The IQR is 18.8 years."),
            ("At least this age", "40.4 years", "40 out of 100 are 40.4 or older, so 60 out of 100 are younger."),
        ], 190, 270),
        b.desmos_line("normaldist(36.9,13.9).inversecdf(0.60)", 500),
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
