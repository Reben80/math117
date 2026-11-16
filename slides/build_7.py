"""Unit 4, section 7.1. Monday, November 16, after section 6.2.

OpenStax Introductory Statistics 2e. Sections 7.2, 7.3, and 7.4 are not
on the calendar. Every number is from the book. A Try It the book does
not print is labeled that way in the speaker notes.
"""

import math

import build_2_2_to_2_7 as b
import build_6 as s


def calc_line(command, how, top):
    """The monospace part is what students type. The rest is the Desmos box."""
    return b.text_block(
        '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
        '<span style="color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">DESMOS</span>'
        '&nbsp;&nbsp;<span style="font-family:Menlo, Consolas, monospace;">' + command + '</span>'
        '&nbsp;&nbsp;<span style="color:#5d6670;">' + how + '</span></p>',
        64, top, 1160,
    )


def slides():
    out = []
    out.append(s.opening(
        "Averages vary less than individual values",
        "Both are centered at the population mean.<br>Sample means have a smaller spread.",
        "SECTION 7.1",
        pair(760, 108, 460, 490),
        "Say: section 6.2 was one observation. Today is the sample mean. Point at the wide curve and call it individual values. Point at the narrow curve and call it sample means, n = 25. Same center, the population mean 90. The sample means vary less. Do not say every sample mean lands close. A sample mean can still sit far out. It just happens less often. "
        "About 40 minutes, after 6.2. If the hour is short, stop after the soccer matches. The iPad ages can wait. Skip the dice lab. Skip sections 7.2, 7.3, and 7.4. "
        "Unit 4 homework, the unit test, and the discussion are due today. Exam 2 is Monday, November 23, and covers Units 4 and 5.",
        unit_line="Unit 4 · Sample means",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("One sample, one average")
            + b.title("Three samples, three sample means", 40),
            64, 24, 1150,
        ),
        sample_card(72, 155, "SAMPLE 1", "90"),
        sample_card(460, 155, "SAMPLE 2", "87"),
        sample_card(848, 155, "SAMPLE 3", "93"),
        means_line(64, 390, 1152, 180),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">The population mean is one fixed center. '
            'Each sample of five students gives one sample mean. Many sample means together form the sampling distribution.</p>',
            64, 590, 1150,
        ),
    ], "Say: take five students and average them. That one number is a sample mean. A different five students give a different sample mean, 87 or 93 instead of 90. "
       "Point at the three dots. Those averages are not the population. If we kept taking samples, the pile of averages is the sampling distribution. "
       "Misconception: calling 90 the population mean. On this slide 90 is just one sample's average. The population mean is the center those averages scatter around."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Two different distributions")
            + b.title("Same center, smaller spread", 40),
            64, 24, 1150,
        ),
        one_curve(64, 150, 560, 400, 15, "INDIVIDUAL VALUES"),
        one_curve(656, 150, 560, 400, 3, "SAMPLE MEANS, n = 25"),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">Mean '
            + s.m(r"\mu") + '. Standard deviation ' + s.m(r"\sigma") + '.</p>',
            64, 560, 540,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">Mean '
            + s.m(r"\mu") + '. Standard error ' + s.m(r"\sigma/\sqrt{n}") + '.</p>',
            656, 560, 560,
        ),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">These curves are sketches. The original population need not be normal. '
            'The Central Limit Theorem says the sample means are approximately normal, and a larger n makes them less variable.</p>',
            64, 620, 1150,
        ),
    ], "Say the two names before any formula. Left is one observation, X, with population mean mu and population standard deviation sigma. Right is the sample mean, X-bar, from samples of 25. Same center. The spread on the right is the standard error, sigma over the square root of n. "
       "Say the curves are sketches, not a promise that the population is a bell. Larger n makes that spread smaller. The Central Limit Theorem is why the right-hand curve is approximately a bell even when the population is not. If the population is badly skewed, 25 may not be enough. "
       "Misconception: students think the population itself got narrower. It did not. Only the distribution of the averages did."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Standard error of the mean")
            + b.title("Divide by the square root of n", 40),
            64, 24, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">STANDARD ERROR</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:30px;">' + s.M(r"\sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}}") + '</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">The typical spread of the sample means. '
            + s.m(r"\sigma") + ' is the population standard deviation. n is the sample size.</p>'
            '<p style="margin:16px 0 0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">Z-SCORE FOR A SAMPLE MEAN</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:30px;">' + s.M(r"z = \frac{\bar{X} - \mu}{\sigma / \sqrt{n}}") + '</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Same move as section 6.1. The bottom is the standard error, which you can think of as the step.</p>',
            64, 145, 580,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">THE BOOK’S CHECK</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:26px;line-height:1.3;">' + s.m(r"\mu = 90,\; \sigma = 15,\; n = 25") + '</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;line-height:1.3;">15 / √25 = 3</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">The standard error is 3, not the population standard deviation 15.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;line-height:1.3;">90 + 2(3) = 96</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Two standard errors above the mean is 96. The center stays 90.</p>',
            400,
        ), 660, 155, 556, 400),
    ], "Say standard error of the mean before you say step. It measures how much sample means vary from one sample to the next. n is the sample size, not the number of times the class repeats the experiment. "
       "On the board: 15 divided by the square root of 25 is 15 divided by 5, which is 3. Then 90 + 2(3) = 96. Read once: X-bar is approximately normal with mean mu and standard deviation sigma over the square root of n. "
       "Misconception: dividing by 25 instead of by 5. That gives 0.6. Another: moving the center to 90/25. The center stays 90."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 7.1 · an unknown distribution")
            + b.title("Mean 90, standard deviation 15, n = 25", 36),
            64, 20, 1150,
        ),
        s.bell_at(64, 130, 740, 390, "SAMPLE MEANS, STANDARD ERROR 3", mean=90, sd=3,
                  shade=(85, 92), shade_label="P(85 to 92)",
                  marks=[(85, "85"), (90, "90"), (92, "92")], label_size=18),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">' + s.m(r"P(85 < \bar{X} < 92) = 0.6997") + '</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Standard error 15/√25 = 3. About 70 of 100 sample means land between 85 and 92.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">The population shape is unknown, so this is a normal approximation.</p>',
            830, 160, 400,
        ),
        calc_line("normaldist(90, 15/sqrt(25))", "then Inner, 85 to 92", 560),
    ], "Say: the population can be any shape. With n = 25, the sample means are approximately normal, centered at the population mean 90, with standard error 3. "
       "Type only the monospace command. Desmos opens the area box. Choose Inner, and set 85 and 92. Desmos shows 0.69971711018. The book rounds to 0.6997. "
       "Misconception: normaldist(90, 15). That is one observation, the chapter 6 bell. The sample size has to get into the standard error. "
       "Part b of the example is the 96 from the previous slide."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 7.1 · 3 minutes",
            "Mean 45, standard deviation 8, n = 30",
            "Find " + s.m(r"P(42 < \bar{X} < 50)") + ". OpenStax prints this question.",
        ),
        s.bell_at(64, 175, 700, 370, "SAMPLE MEANS", mean=45, sd=8 / math.sqrt(30),
                  shade=(42, 50), shade_label="P(42 to 50)",
                  marks=[(42, "42"), (45, "45"), (50, "50")], z0=-3.6, z1=3.6, label_size=18),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">Population mean 45. Population standard deviation 8. Sample size 30.</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">First find the standard error, 8/√30. It is about 1.46, not 8.</p>',
            790, 210, 430,
        ),
        calc_line("normaldist(45, 8/sqrt(30))", "then Inner, 42 to 50", 580),
    ], "Try It 7.1. OpenStax prints the question. It does not print this decimal. The worked answer is the next slide. Three minutes. They type the monospace command, then Inner from 42 to 50. "
       "The standard error is 8/√30 ≈ 1.46, so 42 and 50 are each more than two standard errors from 45. A strong student can say about 98% before typing. "
       "The precise probability is 0.9797. If they report a number near 0.5, they used 8, the population standard deviation, instead of the standard error. "
       "Misconception: this probability is about individual observations. It is about sample means."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 7.1")
            + b.title("About 98% of the sample means", 44),
            64, 28, 1150,
        ),
        s.bell_at(64, 155, 700, 400, "SAMPLE MEANS, STANDARD ERROR 1.46", mean=45, sd=8 / math.sqrt(30),
                  shade=(42, 50), shade_label="0.9797",
                  marks=[(42, "42"), (45, "45"), (50, "50")], z0=-3.6, z1=3.6, label_size=18),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:24px;line-height:1.35;">8 / √30 ≈ 1.46</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">' + s.m(r"P(42 < \bar{X} < 50) = 0.9797") + '</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">That is 97.97% of the sample means, not of individual scores. The book prints the question. This is the worked answer.</p>',
            790, 190, 430,
        ),
        calc_line("normaldist(45, 8/sqrt(30))", "then Inner, 42 to 50", 590),
    ], "Say the standard error once: the square root of 30 is about 5.5, and 8 divided by 5.5 is about 1.46. That 1.46 is the second number inside normaldist. "
       "Then 0.9797 is 97.97%, about 98 of 100 samples. Ask them to move the decimal two places. Tell them the book prints the question and this slide is our worked answer. "
       "Misconception: reading 98% as a share of individual scores. Those would use standard deviation 8, and the probability would be much smaller. Then go to the soccer matches."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 7.2 · soccer, over age 40")
            + b.title("Averages of 50 matches vary less than one match", 34),
            64, 18, 1150,
        ),
        s.bell_at(64, 125, 740, 390, "SAMPLE MEANS, STANDARD ERROR 0.071", mean=2,
                  sd=0.5 / math.sqrt(50), shade=(1.8, 2.3), shade_label="0.9977",
                  marks=[(1.8, "1.8"), (2, "2"), (2.3, "2.3")], z0=-4.0, z1=5.2, label_size=18),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">The book’s answer is <b>0.9977</b>.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">One match, standard deviation 0.5, is about 38% for the same hours. The book does not print that 38%.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Standard error 0.5/√50 ≈ 0.071, so 1.8 and 2.3 sit far out on this curve.</p>',
            830, 150, 400,
        ),
        calc_line("normaldist(2, 0.5/sqrt(50))", "then Inner, 1.8 to 2.3", 555),
    ], "Say: one match has mean 2 hours and population standard deviation 0.5. Between 1.8 and 2.3 is ordinary for one match, about 38%. That comparison is not printed in the book. "
       "The sample mean of 50 matches has standard error 0.5/√50 ≈ 0.071. Point at 1.8 on the left shoulder and at 2.3 far to the right. Almost every sample mean falls between them. The book’s probability is 0.9977. "
       "The population was already a bell. The new fact is the smaller standard error. "
       "Try It 7.2, only if asked: SAT time, mean 2.5, standard deviation 0.25, n = 60, between 2 and 3. The standard error is about 0.032, so the probability is essentially 1. The book does not print it. "
       "Misconception: typing 0.5 as the standard error. That answers the one-match question."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 7.3 · ages of iPad users")
            + b.title("Mean 34, standard deviation 15, n = 100", 36),
            64, 18, 1150,
        ),
        s.bell_at(64, 125, 560, 340, "95TH PERCENTILE OF THE MEANS", mean=34, sd=1.5,
                  shade=(None, 36.5), shade_label="95%",
                  marks=[(34, "34"), (36.5, "36.5")], label_size=18),
        s.bell_at(656, 125, 560, 340, "PROBABILITY ABOVE 30", mean=34, sd=1.5,
                  shade=(30, None), shade_label="0.9962",
                  marks=[(30, "30"), (34, "34")], label_size=18),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">Standard error 15/√100 = 1.5 years. '
            'About 95% of the sample means are below 36.5 years, not 95% of individual ages. '
            + s.m(r"P(\bar{X} > 30) = 0.9962") + '.</p>',
            64, 480, 1150,
        ),
        calc_line("normaldist(34, 15/sqrt(100)).inversecdf(0.95)", "percentile, gives 36.5", 572),
        calc_line("normaldist(34, 15/sqrt(100))", "then Right from 30, gives 0.9962", 616),
    ], "This slide can wait if 6.2 ran long. Say: 100 users, so the standard error shrinks from 15 years to 1.5 years. "
       "inversecdf finds a cutoff. inversecdf(0.95) is 36.467, and the book rounds it to 36.5. About 95% of the sample means are below 36.5 years. A person’s 95th percentile would use 15, not 1.5: 34 + 1.64(15) is about 59. "
       "The right graph is a probability, not a percentile. Type the same normaldist, then Right from 30. The book’s area is 0.9962, because 30 is about 2.7 standard errors below 34. "
       "Example 7.4, only if asked: app engagement, mean 8.2 minutes, standard deviation 1, n = 60. Standard error 1/√60 ≈ 0.129. The 90th percentile is 8.37 minutes. Between 8 and 8.5 is 0.9293. "
       "Try It 7.4, only if asked: cola cans, mean 16 ounces, standard deviation 0.143, n = 34. The probability the sample mean exceeds 16.01 is about 0.342. The book does not print it. "
       "Misconception: treating 36.5 as an age a typical person has. It is an average of 100 people."))
    out.append(b.quick("The sampling distribution", [
        ("A population has mean 90 and standard deviation 15. For samples of 25, the standard error is",
         [("A", "3"), ("B", "15"), ("C", "0.6")], "A",
         "15 / √25 = 3. Not 15, and not 15/25."),
        ("The mean of the sampling distribution is",
         [("A", "90"), ("B", "3"), ("C", "90 / 25")], "A",
         "It equals the population mean."),
        ("About what percent of sample means fall from 85 to 92?",
         [("A", "70%"), ("B", "7%"), ("C", "95%")], "A",
         "0.6997 is about 70%. 95% is a different interval."),
    ], "Answers: 1A, 2A, 3A. If they pick 0.6, they divided by 25 instead of by the square root of 25. If they pick 15, they used the population standard deviation. "
       "If they pick 95%, they are remembering the middle two standard errors, which is not the interval 85 to 92. "
       "Do 15/√25 on the board before you leave. Homework is items 61 through 71."))
    out.append(b.closing(
        "Before Tuesday",
        "Three facts about sample means",
        [
            "The mean of the sampling distribution equals the population mean.",
            "The standard error is the population standard deviation divided by √n.",
            "Sample means get closer to a normal curve as n grows. A skewed population needs a larger n.",
        ],
        ("8.1 Confidence", "Tuesday. A range for the unknown mean."),
        "Homework: OpenStax 7.1, items 61 through 71. Unit 4 is due today.",
        "Items 72 and up are sums, section 7.2, and the later sections 7.3 and 7.4. This unit stops at 7.1. "
        "Exam 2 is Monday, November 23. It covers Units 4 and 5: sections 6.1, 6.2, 7.1, 8.1, 8.2, and 8.3. The bootstrap unit is not on it. "
        "The third fact is the Central Limit Theorem. Do not add conditions they have not seen.",
    ))
    return out


def sample_card(left, top, label, average):
    return b.text_block(b.card_shell(
        '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">' + label + '</p>'
        '<p style="margin:14px 0 0;color:#1c242c;font-size:48px;font-weight:650;line-height:1;">' + average + '</p>'
        '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.3;">Five students. One sample mean.</p>',
        200,
    ), left, top, 360, 200)


def means_line(left, top, width, height):
    """Three sample means, not a made-up list of student scores."""
    lo, hi = 84.0, 96.0
    pad_l, pad_r = 90, 90
    axis = 88

    def X(v):
        return pad_l + (v - lo) / (hi - lo) * (width - pad_l - pad_r)

    parts = [
        s._panel(width, height),
        f'<text x="18" y="28" font-size="14" fill="#2a6f7a" font-family="{s.FONT}" '
        f'font-weight="700" letter-spacing="1.1">THREE SAMPLE MEANS</text>',
        f'<line x1="{X(lo):.0f}" y1="{axis}" x2="{X(hi):.0f}" y2="{axis}" stroke="#d5e0de" stroke-width="3"></line>',
    ]
    for value in (87, 90, 93):
        x = X(value)
        parts.append(
            f'<circle cx="{x:.0f}" cy="{axis}" r="9" fill="#2a6f7a"></circle>'
            f'<text x="{x:.0f}" y="132" text-anchor="middle" font-size="22" fill="#1c242c" '
            f'font-family="{s.FONT}" font-weight="650">{value}</text>'
        )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def one_curve(left, top, width, height, sd, heading):
    """One bell on the shared 45-to-135 scale, so n = 25 looks narrow."""
    mean, lo, hi = 90.0, 45.0, 135.0
    pad_l, pad_r, pad_t, pad_b = 36, 24, 48, 40
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base = pad_t + plot_h

    def X(v):
        return pad_l + (v - lo) / (hi - lo) * plot_w

    steps = 80
    pts = []
    for i in range(steps + 1):
        v = lo + i * (hi - lo) / steps
        z = (v - mean) / sd
        y = base - math.exp(-0.5 * z * z) * (plot_h - 8)
        pts.append((X(v), y))
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    fill = f"{pts[0][0]:.1f},{base:.1f} " + path + f" {pts[-1][0]:.1f},{base:.1f}"
    parts = [
        s._panel(width, height),
        f'<text x="18" y="28" font-size="14" fill="#2a6f7a" font-family="{s.FONT}" '
        f'font-weight="700" letter-spacing="1.1">{heading}</text>',
        f'<polygon points="{fill}" fill="#d7ebe8"></polygon>',
        f'<polyline points="{path}" fill="none" stroke="#2a6f7a" stroke-width="2.8"></polyline>',
        f'<line x1="{X(mean):.1f}" y1="{pad_t:.1f}" x2="{X(mean):.1f}" y2="{base:.1f}" '
        f'stroke="#2a6f7a" stroke-width="1.4" stroke-dasharray="4 4"></line>',
    ]
    for value, label in ((45, "45"), (90, "90"), (135, "135")):
        parts.append(
            f'<text x="{X(value):.1f}" y="{height - 14}" text-anchor="middle" font-size="16" '
            f'fill="#1c242c" font-family="{s.FONT}" font-weight="650">{label}</text>'
        )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def pair(left, top, width, height):
    """Individual values, spread 15, and sample means of 25, standard error 3."""
    mean, lo, hi = 90.0, 45.0, 135.0
    pad_l, pad_r, pad_t, pad_b = 28, 16, 78, 36
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base = pad_t + plot_h

    def X(v):
        return pad_l + (v - lo) / (hi - lo) * plot_w

    def curve(sd):
        steps = 70
        pts = []
        for i in range(steps + 1):
            v = lo + i * (hi - lo) / steps
            z = (v - mean) / sd
            y = base - math.exp(-0.5 * z * z) * (plot_h - 8)
            pts.append((X(v), y))
        return pts

    wide = curve(15)
    narrow = curve(3)

    def path(pts):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    fill = f"{narrow[0][0]:.1f},{base:.1f} " + path(narrow) + f" {narrow[-1][0]:.1f},{base:.1f}"
    parts = [
        s._panel(width, height),
        f'<line x1="18" y1="26" x2="48" y2="26" stroke="#6f948e" stroke-width="3.2"></line>',
        f'<text x="56" y="31" font-size="15" fill="#5d6670" font-family="{s.FONT}">Individual values</text>',
        f'<line x1="18" y1="52" x2="48" y2="52" stroke="#2a6f7a" stroke-width="3.2"></line>',
        f'<text x="56" y="57" font-size="15" fill="#1c242c" font-family="{s.FONT}" '
        f'font-weight="700">Sample means (n = 25)</text>',
        f'<polygon points="{fill}" fill="#d7ebe8"></polygon>',
        f'<polyline points="{path(wide)}" fill="none" stroke="#6f948e" stroke-width="2.6"></polyline>',
        f'<polyline points="{path(narrow)}" fill="none" stroke="#2a6f7a" stroke-width="2.8"></polyline>',
        f'<line x1="{X(mean):.1f}" y1="{pad_t:.1f}" x2="{X(mean):.1f}" y2="{base:.1f}" '
        f'stroke="#2a6f7a" stroke-width="1.4" stroke-dasharray="4 4"></line>',
    ]
    for value, label in ((45, "45"), (90, "90"), (135, "135")):
        parts.append(
            f'<text x="{X(value):.1f}" y="{height - 12}" text-anchor="middle" font-size="16" '
            f'fill="#5d6670" font-family="{s.FONT}">{label}</text>'
        )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def main():
    b.write_deck(
        "7.1-sample-means",
        "math117-7-1-sample-means",
        "MATH 117 · 7.1 The average of a sample",
        "Sample means have the same center and a smaller standard error.",
        slides,
    )


if __name__ == "__main__":
    main()
