"""Unit 5, November 17–19. Confidence intervals.

OpenStax Introductory Statistics 2e, sections 8.1, 8.2, and 8.3.
Every number is from the book. Section 8.4 and later are not on the calendar.
"""

import build_2_2_to_2_7 as b
import build_6 as s

b.GRAPHS["8.1"] = "https://www.desmos.com/calculator/jrublef2f5"
b.GRAPHS["8.2"] = "https://www.desmos.com/calculator/xs264vqhhe"
b.GRAPHS["8.3"] = "https://www.desmos.com/calculator/82gqmz8nj9"

NB_81 = "https://www.desmos.com/notebook/k5kigk35he"
NB_82 = "https://www.desmos.com/notebook/xg33if0c12"
NB_83 = "https://www.desmos.com/notebook/z7eemsa93g"

FONT = s.FONT


def calc_line(command, how, top, graph):
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


def interval_line(left, top, width, height, lo, hi, points, heading, foot, band=None):
    """points are (value, above, below). band is the interval to shade, in the same units."""
    pad_l = 72 if width >= 700 else 56
    pad_r = 48 if width >= 700 else 36
    axis = int(height * 0.46)
    label_size = 18 if width >= 700 else 15
    above_size = 16 if width >= 700 else 14

    def X(v):
        return pad_l + (v - lo) / (hi - lo) * (width - pad_l - pad_r)

    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="18" y="28" font-size="13" fill="#2a6f7a" font-family="{FONT}" '
        f'font-weight="700" letter-spacing="1.1">{s._esc(heading)}</text>',
    ]
    if band:
        x0, x1 = X(band[0]), X(band[1])
        parts.append(
            f'<rect x="{min(x0, x1):.1f}" y="{axis - 10}" width="{abs(x1 - x0):.1f}" height="20" '
            f'rx="10" fill="#d7ebe8"></rect>'
        )
    parts.append(
        f'<line x1="{X(lo):.1f}" y1="{axis}" x2="{X(hi):.1f}" y2="{axis}" stroke="#d5e0de" stroke-width="3"></line>'
    )
    for value, above, below in points:
        x = X(value)
        parts.append(
            f'<line x1="{x:.1f}" y1="{axis - 28}" x2="{x:.1f}" y2="{axis}" stroke="#2a6f7a" stroke-width="2"></line>'
            f'<circle cx="{x:.1f}" cy="{axis}" r="8" fill="#2a6f7a"></circle>'
        )
        if above:
            parts.append(
                f'<text x="{x:.1f}" y="{axis - 40}" text-anchor="middle" font-size="{above_size}" '
                f'fill="#1c242c" font-family="{FONT}" font-weight="650">{s._esc(above)}</text>'
            )
        if below:
            parts.append(
                f'<text x="{x:.1f}" y="{axis + 36}" text-anchor="middle" font-size="{label_size}" '
                f'fill="#1c242c" font-family="{FONT}" font-weight="650">{s._esc(below)}</text>'
            )
    if foot:
        parts.append(
            f'<text x="{width / 2:.0f}" y="{height - 22}" text-anchor="middle" font-size="16" '
            f'fill="#1c242c" font-family="{FONT}">{s._esc(foot)}</text>'
        )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def slides_81():
    out = []
    out.append(s.opening(
        "A range for the mean",
        "The sample mean is the point estimate.<br>The margin of error is the reach on each side.",
        "SECTION 8.1",
        interval_line(
            760, 130, 450, 470, 2, 12,
            [(4.5, "", "4.5"), (7, "mean 7", ""), (9.5, "", "9.5")],
            "MEAN 7, ERROR BOUND 2.5",
            "4.5 to 9.5",
            band=(4.5, 9.5),
        ),
        "Say: a confidence interval is a range for the population mean. The sample mean sits in the middle. That middle number is the point estimate. The margin of error is how far the interval reaches on each side. "
        "Point at 7, then at 4.5 and 9.5. 7 minus 2.5 is 4.5. 7 plus 2.5 is 9.5. "
        "This section is for a mean when the population standard deviation is known. Section 8.2 is the case when it is not. "
        "The likely mistake is reading 4.5 to 9.5 as a range that holds most of the data. It is a range for the mean. "
        "About one class period. Unit 5 homework, the test, and the discussion are due Wednesday, November 19.",
        unit_line="Unit 5 · Confidence intervals",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The words, then the symbols")
            + b.title("Point estimate, standard error, margin of error", 36),
            64, 22, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            + s.M(r"\mathrm{EBM} = z\frac{\sigma}{\sqrt{n}}") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">'
            'x&#772; is the sample mean, the point estimate for &#956;, the population mean. '
            '&#963; is the population standard deviation. In this section it is known. '
            'n is the sample size.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">'
            'The standard error is &#963; over the square root of n. It is the spread of the sample mean. '
            'z is the standard-normal cutoff with the confidence level in the middle. '
            'EBM is the error bound, the margin of error.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:20px;line-height:1.35;">'
            'The interval is x&#772; minus EBM to x&#772; plus EBM. '
            'To recover the sample mean, average the two ends.</p>',
            64, 140, 620,
        ),
        s.bell_at(
            700, 150, 520, 430, "90% IN THE MIDDLE",
            shade=(-1.645, 1.645), shade_label="90%",
            marks=[(-1.645, "−1.645"), (0, "0"), (1.645, "+1.645")],
            label_gap=48, label_size=15,
        ),
    ], "Say the names before the formula. x-bar is the sample mean. It estimates mu, the population mean. Sigma is the population standard deviation, and in this section it is known. "
       "The standard error is sigma divided by the square root of n. Students met that spread in section 7.1. z is how many standard errors you travel. For 90%, each tail is 5%, and the book uses z = 1.645. Positive is to the right of 0. The same distance is used on both sides of the sample mean. "
       "EBM is the error bound for the mean, the margin of error. To build the interval, start at the sample mean and move that far both ways. To go backwards, average the two ends. Example 8.6: (67.18 + 68.82) / 2 = 68, and 68.82 minus 68 = 0.82. "
       "The likely mistake is calling z a score on the exam. z is a count of standard errors. Alpha is 1 minus the confidence level. Say that only if someone asks."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.1")
            + b.title("Mean 7, error bound 2.5", 44),
            64, 28, 1150,
        ),
        interval_line(
            64, 155, 760, 400, 2, 12,
            [(4.5, "", "4.5"), (7, "sample mean 7", ""), (9.5, "", "9.5")],
            "THE INTERVAL RUNS 2.5 EACH WAY",
            "7 − 2.5 = 4.5 and 7 + 2.5 = 9.5",
            band=(4.5, 9.5),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">We estimate with 95% confidence that the true population mean is between 4.5 and 9.5.</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">4.5 and 9.5 are ends of a range for the mean. They are not data values.</p>',
            850, 200, 370,
        ),
    ], "Point at 7. That is the sample mean, the point estimate. The error bound is 2.5, so the interval reaches 2.5 below 7 and 2.5 above 7. 7 minus 2.5 is 4.5. 7 plus 2.5 is 9.5. "
       "Read the book’s sentence once: we estimate with 95% confidence that the true population mean is between 4.5 and 9.5. "
       "The likely mistake is hearing 4.5 to 9.5 as the scores people got. Those ends were built from the mean and the error bound."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.2 · statistics exams")
            + b.title("Mean 68, standard deviation 3, n = 36", 36),
            64, 20, 1150,
        ),
        interval_line(
            64, 130, 1152, 360, 66.4, 69.6,
            [(67.18, "", "67.18"), (68, "sample mean 68", ""), (68.82, "", "68.82")],
            "90% INTERVAL",
            "Standard error 3/6 = 0.5.    Error bound 1.645 × 0.5 = 0.8225.",
            band=(67.18, 68.82),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '68 − 0.8225 = 67.18 and 68 + 0.8225 = 68.82. The calculator prints (67.178, 68.822).</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'We estimate with 90% confidence that the true mean exam score is between 67.18 and 68.82.</p>',
            64, 520, 1150,
        ),
        calc_line("1.645*3/sqrt(36)", "then 68 minus that, and 68 plus that", 640, "8.1"),
    ], "The population standard deviation is 3 points. The sample size is 36. The sample mean is 68. The confidence level is 90%, so each tail is 5%, and the book uses z = 1.645. "
       "The standard error is 3 divided by the square root of 36. The square root of 36 is 6, so the standard error is 0.5. The error bound is 1.645 times 0.5, which is 0.8225. "
       "68 minus 0.8225 is 67.1775, and the book rounds to 67.18. 68 plus 0.8225 is 68.8225, and the book rounds to 68.82. The calculator prints (67.178, 68.822). "
       "Read the sentence: we estimate with 90% confidence that the true mean exam score is between 67.18 and 68.82. "
       "The likely mistake is using 3 as the standard error and getting 68 plus or minus 1.645 times 3. The 3 has to be divided by the square root of n."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("What 90% means")
            + b.title("About 90 of 100 intervals, not 90% of the scores", 36),
            64, 28, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">THE BOOK’S SENTENCE</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:26px;line-height:1.35;">Ninety percent of all confidence intervals constructed in this way contain the true mean exam score.</p>'
            '<p style="margin:16px 0 0;color:#5d6670;font-size:22px;line-height:1.4;">If we built 100 intervals this way, we would expect 90 of them to contain the true mean.</p>',
            250,
        ), 64, 160, 700, 250),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">NOT THIS</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">67.18 to 68.82 is not the range where 90% of students scored.</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:22px;line-height:1.4;">It is a range for the mean. This one interval either contains the mean or it does not.</p>',
            250,
        ), 788, 160, 428, 250),
    ], "Read the book’s sentence. Ninety percent of intervals made this way contain the true mean. The picture in the book is: build 100 of them, and expect 90 to catch the mean. "
       "Do not say there is a 90% chance that this mean is between 67.18 and 68.82. The mean is a fixed number. The interval is what moved. "
       "The other mistake is treating 67.18 to 68.82 as the scores of 90% of the students. One standard deviation of the scores is 3 points, so the scores themselves sit much farther from 68 than this interval does."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.4 · the same exams")
            + b.title("95% reaches farther than 90%", 40),
            64, 22, 1150,
        ),
        interval_line(
            64, 140, 560, 390, 66.5, 69.5,
            [(67.18, "", "67.18"), (68, "68", ""), (68.82, "", "68.82")],
            "90% · z = 1.645",
            "Error bound 0.8225",
            band=(67.18, 68.82),
        ),
        interval_line(
            656, 140, 560, 390, 66.5, 69.5,
            [(67.02, "", "67.02"), (68, "68", ""), (68.98, "", "68.98")],
            "95% · z = 1.96",
            "Error bound 0.98",
            band=(67.02, 68.98),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '1.96 × 0.5 = 0.98. Then 68 − 0.98 = 67.02 and 68 + 0.98 = 68.98.</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">A higher confidence level makes a wider interval.</p>',
            64, 560, 1150,
        ),
    ], "Same sample mean, same standard deviation, same n. Only the confidence level changes. For 95%, alpha is 0.05, so each tail is 0.025, and the book uses z = 1.96. "
       "The standard error is still 0.5. The error bound is 1.96 times 0.5, which is 0.98. 68 minus 0.98 is 67.02. 68 plus 0.98 is 68.98. "
       "Put the two intervals next to each other. 67.02 to 68.98 is wider than 67.18 to 68.82. To be more confident of catching the mean, the interval has to reach farther. "
       "The likely mistake is thinking a higher confidence level makes a tighter, better interval. It makes a wider one."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.5 · same exams, 90%")
            + b.title("A larger sample makes a smaller error bound", 36),
            64, 24, 1150,
        ),
        *b.three_cards([
            ("n = 36", "Error bound 0.8225", "The original sample. The interval is 67.18 to 68.82."),
            ("n = 100", "Error bound 0.4935", "1.645 × 3 / 10 = 0.4935. The interval gets narrower."),
            ("n = 25", "Error bound 0.987", "1.645 × 3 / 5 = 0.987. The interval gets wider."),
        ], 170, 280),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">The sample mean stays 68. The standard deviation stays 3. Only n changes.</p>',
            64, 500, 1150,
        ),
        calc_line("1.645*3/sqrt(100)", "and 1.645*3/sqrt(25)", 580, "8.1"),
    ], "Leave the mean, the standard deviation, and the 90% level alone. Change only the sample size. "
       "When n is 100, the square root of 100 is 10, so the error bound is 1.645 times 3 divided by 10, which the book gives as 0.4935. "
       "When n is 25, the square root of 25 is 5, so the error bound is 1.645 times 3 divided by 5, which the book gives as 0.987. "
       "A larger sample makes the standard error smaller, so the interval is narrower. A smaller sample does the opposite. "
       "The likely mistake is changing the sample mean when n changes. In this example the book keeps the sample mean at 68. "
       "Example 8.7, if the hour remains: sigma is 15 years, the error bound they want is 2, z is 1.96, and n = (1.96 times 15 divided by 2) squared = 216.09. Round up to 217 students."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 8.2 · 3 minutes",
            "Pizza delivery, 90%",
            "The population standard deviation is 6 minutes. A sample of 28 restaurants has mean delivery time 36 minutes. Find the 90% interval.",
        ),
        interval_line(
            64, 210, 620, 400, 30, 42,
            [(36, "sample mean 36", "")],
            "FIND THE TWO ENDS",
            "z = 1.645. The standard error is 6 / √28.",
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">Start at 36. Move the error bound both ways.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">1.645 × 6 / √28 = 1.865</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">34.13 to 37.87 minutes</p>',
            200,
        ), 720, 280, 490, 200),
    ], "Try It 8.2. Three minutes. The question is on the slide. The worked line is hidden until the fragment. "
       "z is 1.645. The standard error is 6 divided by the square root of 28. The error bound is 1.645 times that, which is 1.865. "
       "36 minus 1.865 is 34.135, which rounds to 34.13. 36 plus 1.865 is 37.865, which rounds to 37.87. "
       "The likely mistake is dividing by 28 instead of the square root of 28, or walking only one direction from 36."))
    out.append(b.quick("Read the interval", [
        ("The sample mean is the",
         [("A", "Point estimate"), ("B", "Margin of error"), ("C", "Population standard deviation")], "A",
         "It is the center of the interval."),
        ("Exams, 90%. The interval is",
         [("A", "67.18 to 68.82"), ("B", "65 to 71"), ("C", "68 to 71")], "A",
         "68 ± 0.8225."),
        ("Raising 90% to 95% makes it",
         [("A", "Narrower"), ("B", "Wider"), ("C", "A share of the scores")], "B",
         "67.02 to 68.98 is wider."),
    ], "Answers: 1A, 2A, 3B. The sample mean is the point estimate. The 90% exam interval is 67.18 to 68.82, not a three-standard-deviation range of scores. "
       "Raising the confidence level to 95% makes the interval wider: 67.02 to 68.98. "
       "The likely mistake on question 2 is 65 to 71, which is about one standard deviation of the scores, not the interval for the mean. "
       "Homework is OpenStax 8.1, items 95 through 103. Unit 5 is due November 19."))
    out.append(b.closing(
        "Before you leave",
        "A range for the mean",
        [
            "The sample mean is the point estimate.",
            "The margin of error is z times the standard error.",
            "The confidence level is a share of intervals, not a share of the data.",
        ],
        ("8.2 The t interval", "The population standard deviation is unknown."),
        "Homework: OpenStax 8.1, items 95 through 103. Unit 5 is due November 19.",
        "To build an interval, start at the sample mean and add and subtract z times sigma over the square root of n. To recover the sample mean, average the two ends. "
        "The calculator card is the class graph. The notebook card is the same examples as a short lesson. "
        "Example 8.7, only if asked: within 2 years, sigma 15, 95%, n rounds up from 216.09 to 217. "
        "Unit 5 homework, the unit test, and the discussion are due Wednesday, November 19.",
        graph="8.1",
        notebook=NB_81,
    ))
    return out


def slides_82():
    out = []
    out.append(s.opening(
        "When sigma is unknown, use s",
        "The sample standard deviation replaces &#963;.<br>The cutoff is a t-score. The degrees of freedom are n − 1.",
        "SECTION 8.2",
        interval_line(
            760, 140, 450, 460, 6, 11,
            [(7.30, "", "7.30"), (8.23, "mean", ""), (9.15, "", "9.15")],
            "95% · 15 SENSORY RATES",
            "7.30 to 9.15",
            band=(7.30, 9.15),
        ),
        "Say: yesterday sigma was known, so the cutoff was z. Today the population standard deviation is unknown. Use s, the sample standard deviation. "
        "The cutoff is a t-score. The degrees of freedom are n minus 1. "
        "Point at the interval 7.30 to 9.15. That is Example 8.8, a range for the mean sensory rate. "
        "Do not give a lecture on the shape of the t curve. One sentence is enough: the t cutoff sits a little farther out than z, because s is an estimate. "
        "About one class period. The likely mistake is still dividing by n, or using z when the problem gives s.",
        unit_line="Unit 5 · Confidence intervals",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The words, then the symbols")
            + b.title("s estimates sigma. t replaces z.", 40),
            64, 22, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            + s.M(r"\mathrm{EBM} = t\frac{s}{\sqrt{n}}") + '</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">'
            's is the sample standard deviation. It estimates &#963;, which is unknown here. '
            'The degrees of freedom are df = n − 1. '
            't is the cutoff on that t-distribution. The middle area is the confidence level.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:20px;line-height:1.35;">'
            'The standard error is s over the square root of n. '
            'The interval is still the sample mean minus the error bound, to the sample mean plus the error bound.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">'
            'Desmos: tdist(df).inversecdf(area to the left). For 95%, the left area is 0.975. For 90%, it is 0.95.</p>',
            64, 145, 1150,
        ),
        calc_line("tdist(14).inversecdf(0.975)", "the 95% cutoff, df = 14", 560, "8.2"),
    ], "Name s before the formula. s is the sample standard deviation. It stands in for sigma. "
       "The degrees of freedom are n minus 1, because the deviations from the sample mean have to add to zero, so the last one is fixed. Say that once. Do not ask them to memorize a derivation. "
       "t has the same job z had. For a 95% interval the two tails share 5%, so each tail is 0.025, and the area to the left of the positive cutoff is 0.975. "
       "In Desmos, tdist(14).inversecdf(0.975) is about 2.145. The z cutoff for 95% was 1.96. t is a bit farther out, so the interval is a bit wider than a z interval would have been. "
       "The likely mistake is typing inversecdf(0.95) for a 95% interval. 0.95 would leave 5% in the right tail only, which is a 90% interval. "
       "The interval still runs both ways from the sample mean."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.8 · acupuncture, 15 subjects")
            + b.title("Mean 8.2267, s = 1.6722", 40),
            64, 18, 1150,
        ),
        b.data_strip(
            "THE 15 SENSORY RATES",
            "8.6, 9.4, 7.9, 6.8, 8.3, 7.3, 9.2, 9.6, 8.7, 11.4, 10.3, 5.4, 8.1, 5.5, 6.9",
            130, 88,
        ),
        interval_line(
            64, 240, 760, 340, 6, 11,
            [(7.30, "", "7.30"), (8.2267, "mean 8.2267", ""), (9.15, "", "9.15")],
            "95% · df = 14 · ERROR BOUND 0.9240",
            "8.2267 − 0.9240 = 7.30 and 8.2267 + 0.9240 = 9.15",
            band=(7.30, 9.15),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">The book’s interval is (7.30, 9.15). A calculator TInterval prints (7.3006, 9.1527).</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">We estimate with 95% confidence that the true mean sensory rate is between 7.30 and 9.15.</p>',
            850, 270, 370,
        ),
    ], "Fifteen rates, so the degrees of freedom are 14. The book’s sample mean is 8.2267 and the sample standard deviation is 1.6722. "
       "The book’s error bound is 0.9240. 8.2267 minus 0.9240 is 7.3027, and the book rounds the interval to (7.30, 9.15). 8.2267 plus 0.9240 is 9.1507. "
       "A calculator TInterval prints (7.3006, 9.1527). Use the book’s (7.30, 9.15) in the sentence. "
       "Desmos tdist(14).inversecdf(0.975) is about 2.145. Times 1.6722, divided by the square root of 15, is about 0.926, close to the book’s 0.9240. The small gap is rounding. "
       "Read the sentence: we estimate with 95% confidence that the true mean sensory rate is between 7.30 and 9.15. "
       "The likely mistake is using z = 1.96 because the level is 95%. This problem gives a sample standard deviation, so the cutoff is t."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.9 · chemicals in cord blood")
            + b.title("Mean 127.45, s = 25.965, n = 20", 36),
            64, 20, 1150,
        ),
        interval_line(
            64, 130, 1152, 360, 110, 145,
            [(117.412, "", "117.412"), (127.45, "mean 127.45", ""), (137.488, "", "137.488")],
            "90% · df = 19 · t = 1.729",
            "Error bound 1.729 × 25.965 / √20 = 10.038",
            band=(117.412, 137.488),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '127.45 − 10.038 = 117.412 and 127.45 + 10.038 = 137.488.</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'The calculator prints (117.41, 137.49). We estimate with 90% confidence that the mean number of chemicals is between 117.412 and 137.488.</p>',
            64, 520, 1150,
        ),
        calc_line("tdist(19).inversecdf(0.95)", "the book’s t is 1.729", 650, "8.2"),
    ], "Twenty infants, so df is 19. The book’s mean is 127.45 and s is 25.965. The level is 90%, so each tail is 0.05, and the area to the left is 0.95. The book’s t is 1.729. "
       "The error bound is 1.729 times 25.965 divided by the square root of 20. The book gives 10.038. "
       "127.45 minus 10.038 is 117.412. 127.45 plus 10.038 is 137.488. The calculator prints (117.41, 137.49). "
       "The sentence: we estimate with 90% confidence that the mean number of targeted chemicals is between 117.412 and 137.488. "
       "The likely mistake is inversecdf(0.90), which is the wrong tail, or dividing by 20 instead of the square root of 20."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 8.8 · 4 minutes",
            "Hours of sleep, 95%",
            "Twelve subjects: 8.2, 9.1, 7.7, 8.6, 6.9, 11.2, 10.1, 9.9, 8.9, 9.2, 7.5, 10.5. Find the 95% interval for the mean.",
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">n = 12, so df = 11. The left area for a 95% cutoff is 0.975.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">Mean 8.9833. s = 1.2904. t = 2.201.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">2.201 × 1.2904 / √12 = 0.820</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">8.16 to 9.80 hours</p>',
            250,
        ), 200, 230, 880, 250),
        calc_line("tdist(11).inversecdf(0.975)", "then mean and stdev of the twelve", 560, "8.2"),
    ], "Try It 8.8. The book prints the twelve times and does not print the worked answer. The fragment is the same arithmetic as Example 8.8. "
       "The mean of the twelve times is 8.9833. The sample standard deviation is 1.2904. df is 11. "
       "tdist(11).inversecdf(0.975) is 2.201. The error bound is 2.201 times 1.2904 divided by the square root of 12, which is 0.820. "
       "8.9833 minus 0.820 is 8.16. 8.9833 plus 0.820 is 9.80. "
       "The likely mistake is df = 12, or inversecdf(0.95) for a 95% interval."))
    out.append(b.quick("z or t", [
        ("Sigma unknown. The cutoff is",
         [("A", "A z-score"), ("B", "A t-score"), ("C", "The sample mean")], "B",
         "Use t when you use s."),
        ("n = 15. The degrees of freedom are",
         [("A", "15"), ("B", "14"), ("C", "16")], "B",
         "df = n − 1."),
        ("(7.30, 9.15) is a range for",
         [("A", "The mean sensory rate"), ("B", "95% of the subjects"), ("C", "The standard deviation")], "A",
         "An interval for the mean."),
    ], "Answers: 1B, 2B, 3A. When sigma is unknown, the cutoff is a t-score. Fifteen observations give 14 degrees of freedom. "
       "(7.30, 9.15) estimates the mean sensory rate. It is not the range of 95% of the subjects, and it is not s. "
       "Homework is OpenStax 8.2, items 104 through 116. Item 104 is a proportion, filed under this section. The mean problems start at 105. Unit 5 is due November 19."))
    out.append(b.closing(
        "Before you leave",
        "s, then t, then both directions",
        [
            "s estimates the unknown population standard deviation.",
            "The degrees of freedom are n − 1.",
            "The interval is the sample mean plus and minus t times s over the square root of n.",
        ],
        ("8.3 A proportion", "Successes divided by the sample size."),
        "Homework: OpenStax 8.2, items 104 through 116. Unit 5 is due November 19.",
        "inversecdf needs the area to the left: 0.975 for 95%, and 0.95 for 90%. "
        "The calculator card is the class graph. The notebook card is the same examples as a short lesson. "
        "Item 104 is a proportion problem printed under section 8.2. The mean problems start at 105. "
        "Unit 5 is due Wednesday, November 19.",
        graph="8.2",
        notebook=NB_82,
    ))
    return out


def slides_83():
    out = []
    out.append(s.opening(
        "A share of the population",
        "The sample proportion is successes divided by n.<br>The margin of error reaches both ways from that share.",
        "SECTION 8.3",
        interval_line(
            740, 140, 480, 460, 0.78, 0.90,
            [(0.810, "", "0.810"), (0.842, "0.842", ""), (0.874, "", "0.874")],
            "421 OF 500",
            "About 81% to 87.4%",
            band=(0.810, 0.874),
        ),
        "Say: a proportion is a count of successes divided by the sample size. 421 of 500 is 0.842, the sample proportion. That is the point estimate for the population proportion. "
        "The interval 0.810 to 0.874 is a share of all adults in the city, not a count of people in the sample. "
        "The symbol in the book is p-prime, also read p-hat. Call it the sample proportion. "
        "Use the interval when the successes and the failures are both more than 5. 421 and 79 both clear that. "
        "About one class period. Plus four is one example, not a new course.",
        unit_line="Unit 5 · Confidence intervals",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The words, then the symbols")
            + b.title("Sample proportion, then the error bound", 38),
            64, 22, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.3;">'
            + s.M(r"\hat p=\frac{x}{n}\qquad \mathrm{EBP}=z\sqrt{\frac{\hat p\hat q}{n}}") + '</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">'
            'x is the number of successes. n is the sample size. '
            'p-hat is the sample proportion, the point estimate for p. '
            'q-hat is 1 minus p-hat, the share of failures.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:20px;line-height:1.35;">'
            'EBP is the error bound for the proportion. '
            'The interval is p-hat minus EBP to p-hat plus EBP.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:18px;line-height:1.35;">'
            'Use this when the successes and the failures are both more than 5. '
            'z is the same cutoff as in section 8.1. For 95% the book uses 1.96. For 90% it uses 1.645.</p>',
            64, 140, 1150,
        ),
    ], "Say p-hat before the formula. p-hat is x divided by n, the sample proportion. It estimates p, the population proportion. "
       "q-hat is 1 minus p-hat. The book also writes p-prime. Either name is the sample proportion. "
       "EBP is the error bound for the proportion. It uses p-hat and q-hat because the true p is unknown. "
       "To build the interval, start at p-hat and move EBP both ways. The middle of a finished interval is p-hat. "
       "The check before you start: successes greater than 5, and failures greater than 5. "
       "The likely mistake is putting the count 421 into the interval, or using sigma from the mean formula."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.10 · adults in a large city")
            + b.title("421 of 500 own a smartphone", 40),
            64, 20, 1150,
        ),
        interval_line(
            64, 130, 760, 400, 0.78, 0.90,
            [(0.810, "", "0.810"), (0.842, "p-hat 0.842", ""), (0.874, "", "0.874")],
            "95% · z = 1.96",
            "421/500 = 0.842. Failures: 500 − 421 = 79.",
            band=(0.810, 0.874),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '1.96 × the square root of (0.842 × 0.158 / 500) = 0.032.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '0.842 − 0.032 = 0.810 and 0.842 + 0.032 = 0.874.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'The calculator prints (0.81003, 0.87397). Between 81% and 87.4%.</p>',
            850, 170, 370,
        ),
        calc_line("421/500", "then the error bound with z = 1.96", 600, "8.3"),
    ], "421 successes out of 500. The sample proportion is 421 divided by 500, which is 0.842. The failures are 79, and 0.158 is 1 minus 0.842. Both 421 and 79 are more than 5. "
       "The level is 95%, so the book uses z = 1.96. The error bound is 1.96 times the square root of 0.842 times 0.158 divided by 500, which is 0.03197, and the slide rounds that factor to 0.032. "
       "0.842 minus 0.032 is 0.810. 0.842 plus 0.032 is 0.874. The calculator, without that rounding, prints (0.81003, 0.87397). "
       "The book’s sentence: we estimate with 95% confidence that between 81% and 87.4% of all adult residents of this city have smartphones. "
       "The likely mistake is reporting 421, or 84%, as the interval."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.11 · a class project")
            + b.title("300 of 500 students are registered voters", 36),
            64, 20, 1150,
        ),
        interval_line(
            64, 130, 1152, 360, 0.50, 0.70,
            [(0.564, "", "0.564"), (0.60, "p-hat 0.60", ""), (0.636, "", "0.636")],
            "90% · z = 1.645",
            "Error bound 1.645 × the square root of (0.60 × 0.40 / 500) = 0.036",
            band=(0.564, 0.636),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '0.60 − 0.036 = 0.564 and 0.60 + 0.036 = 0.636. The book’s interval is (0.564, 0.636).</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'We estimate with 90% confidence that between 56.4% and 63.6% of all students are registered voters.</p>',
            64, 520, 1150,
        ),
        calc_line("1.645*sqrt(0.6*0.4/500)", "then 0.60 minus that, and 0.60 plus that", 640, "8.3"),
    ], "300 of 500 is 0.60. The failures are 200. Both are more than 5. The level is 90%, so z is 1.645. "
       "The error bound is 1.645 times the square root of 0.60 times 0.40 divided by 500, which is 0.036. "
       "0.60 minus 0.036 is 0.564. 0.60 plus 0.036 is 0.636. The book’s interval is (0.564, 0.636), and the calculator agrees. "
       "Two wordings from the book: between 56.4% and 63.6% of all students are registered voters. "
       "The likely mistake is a 95% cutoff, 1.96, on a 90% problem."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 8.12 · the plus-four method")
            + b.title("Add two successes and two failures", 38),
            64, 22, 1150,
        ),
        *b.three_cards([
            ("The sample", "6 of 25 smoked", "x = 6 and n = 25. The book uses plus four because the sample is small."),
            ("Plus four", "x = 8, n = 29", "Add two successes and two failures. 6 + 2 = 8 and 25 + 4 = 29."),
            ("95% interval", "0.113 to 0.439", "8/29 = 0.276. The book’s error bound is 0.163."),
        ], 160, 300),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '0.276 − 0.163 = 0.113 and 0.276 + 0.163 = 0.439.</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">We are 95% confident that the true proportion who smoke is between 0.113 and 0.439.</p>',
            64, 510, 1150,
        ),
    ], "Name the method: plus four. Six of 25 students smoked. The book adds two successes and two failures, so x becomes 8 and n becomes 29. "
       "8 divided by 29 is 0.2759, and the book uses 0.276. The book’s error bound is 0.163. "
       "0.276 minus 0.163 is 0.113. 0.276 plus 0.163 is 0.439. The calculator interval is (0.113, 0.439). "
       "The sentence: we are 95% confident that the true proportion of all statistics students who smoke is between 0.113 and 0.439. "
       "The likely mistake is using 6 and 25 after announcing plus four, or adding four successes."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 8.10 · 3 minutes",
            "Who owns a tablet?",
            "98 of 250 people own a tablet. Find the 95% confidence interval for the population proportion.",
        ),
        interval_line(
            64, 210, 620, 390, 0.25, 0.55,
            [(0.392, "98/250", "")],
            "95% · z = 1.96",
            "Successes 98. Failures 152. Both are more than 5.",
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">Start at the sample proportion. Move the error bound both ways.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">98/250 = 0.392. Error bound 0.0605.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">0.331 to 0.453</p>',
            190,
        ), 720, 280, 490, 190),
    ], "Try It 8.10. The book asks for the interval and does not print it in the section. "
       "98 divided by 250 is 0.392. The failures are 152. z is 1.96. "
       "The error bound is 1.96 times the square root of 0.392 times 0.608 divided by 250, which is 0.0605. "
       "0.392 minus 0.0605 is 0.3315. 0.392 plus 0.0605 is 0.4525. Rounded to three decimals, 0.331 to 0.453. "
       "The likely mistake is reporting 98, or forgetting the square root."))
    out.append(b.quick("Proportion, not a count", [
        ("p-hat is",
         [("A", "The sample proportion"), ("B", "The margin of error"), ("C", "A count of people")], "A",
         "Successes divided by n."),
        ("421 of 500, 95%. The interval is about",
         [("A", "81% to 87%"), ("B", "42% to 50%"), ("C", "95% of the people")], "A",
         "0.810 to 0.874."),
        ("Plus four adds",
         [("A", "Two successes and two failures"), ("B", "Four successes"), ("C", "The population proportion")], "A",
         "x + 2 and n + 4."),
    ], "Answers: 1A, 2A, 3A. p-hat is the sample proportion, not the count and not the margin of error. "
       "421 of 500 gives about 81% to 87%, not 42% and not 95% of the people. "
       "Plus four adds two successes and two failures. "
       "Homework is OpenStax 8.3, items 117 through 134. Unit 5 is due November 19."))
    out.append(b.closing(
        "Before you leave",
        "A share, plus and minus",
        [
            "The sample proportion is successes divided by n.",
            "The margin of error uses p-hat and q-hat.",
            "The interval is a share of the population, not a count.",
        ],
        ("Unit S1 · Bootstrap", "November 20–21. Resample the data you have."),
        "Homework: OpenStax 8.3, items 117 through 134. Unit 5 is due November 19.",
        "Successes and failures both need to be more than 5 before this z interval. Plus four is the small-sample adjustment: add two and two. "
        "The calculator card is the class graph. The notebook card is the same examples as a short lesson. "
        "Unit 5 homework, the unit test, and the discussion are due Wednesday, November 19. "
        "Exam 2 is November 22 and 23 and covers Units 4 and 5. Unit S1 is not on that exam.",
        graph="8.3",
        notebook=NB_83,
    ))
    return out


DECKS = [
    ("8.1-known-sigma", "math117-8-1-known-sigma", "MATH 117 · 8.1 A known standard deviation",
     "The sample mean, plus and minus a margin of error.", slides_81),
    ("8.2-t-interval", "math117-8-2-t-interval", "MATH 117 · 8.2 The t interval",
     "When sigma is unknown, use s and a t-score.", slides_82),
    ("8.3-proportion", "math117-8-3-proportion", "MATH 117 · 8.3 A proportion",
     "Successes divided by n, plus and minus a margin of error.", slides_83),
]


def main():
    for folder, slug, title, description, builder in DECKS:
        b.write_deck(folder, slug, title, description, builder)


if __name__ == "__main__":
    main()
