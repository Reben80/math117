"""Unit 4, section 7.1. Monday, November 16, after section 6.2.

OpenStax Introductory Statistics 2e. Sections 7.2, 7.3, and 7.4 are not
on the calendar. Every number is from the book. A Try It the book does
not print is labeled that way in the speaker notes.
"""

import math

import build_2_2_to_2_7 as b
import build_6 as s


def slides():
    out = []
    out.append(s.opening(
        "The average stays close",
        "One person can sit far from the mean.<br>The average of a group stays near it.",
        "SECTION 7.1",
        pair(760, 108, 460, 490),
        "Say: section 6.2 was one person. Today is the average of a group. Point at the wide curve and call it one person. Point at the tall narrow curve and call it the average of 25 people. Same center, 90. The average barely moves. "
        "Do not say sampling distribution yet. Say it once after the picture has landed: the pattern of the averages is the sampling distribution, and the central limit theorem says that pattern becomes a bell. "
        "About 35 minutes, after 6.2. If the hour is short, stop after the soccer match. The iPad ages can wait. Skip the dice lab. Skip sections 7.2, 7.3, and 7.4. "
        "Unit 4 homework, the unit test, and the discussion are due today. Exam 2 is Monday, November 23, and covers Units 4 and 5.",
        unit_line="Unit 4 · Sample means",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The only new step")
            + b.title("Divide by the square root of n", 40),
            64, 28, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">THE STEP FOR AN AVERAGE</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:32px;">' + s.M(r"\frac{\sigma}{\sqrt{n}}") + '</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">σ is one person’s step. n is how many you average. The book calls this the standard error.</p>'
            '<p style="margin:18px 0 0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">HOW MANY STEPS</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:32px;">' + s.M(r"z = \frac{\bar{x} - \mu}{\sigma / \sqrt{n}}") + '</p>'
            '<p style="margin:6px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">Same move as section 6.1. The step on the bottom is smaller.</p>',
            64, 155, 560,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">THE BOOK’S CHECK</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;line-height:1.35;">15 / √25 = 3</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Mean 90, one person’s step 15, sample of 25. The average has step 3, not 15.</p>'
            '<p style="margin:16px 0 0;color:#1c242c;font-size:28px;line-height:1.35;">90 + 2(3) = 96</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Two steps above the average is 96. The center is still 90.</p>',
            360,
        ), 660, 170, 556, 360),
    ], "Say the fraction out loud: sigma over the square root of n. n is how many values go into the average, not how many times the class repeats the experiment. "
       "Do the book’s check on the board: 15 divided by the square root of 25 is 15 divided by 5, which is 3. Then two of those steps: 90 + 2(3) = 96. "
       "Read the shorthand once: X-bar ~ N(μ, σ/√n) means a bell with the population’s center and this smaller step. "
       "Watch for: dividing by 25 instead of by 5. That gives 0.6, and the bell is then much too narrow. Also watch for students who move the center to 90/25."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 7.1 · an unknown distribution")
            + b.title("Mean 90, step 15, sample of 25", 40),
            64, 24, 1150,
        ),
        s.bell_at(64, 145, 760, 400, "THE AVERAGE, STEP 3", mean=90, sd=3,
                  shade=(85, 92), shade_label="about 70%",
                  marks=[(85, "85"), (90, "90"), (92, "92")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;"><b>0.6997</b> is the book’s answer. About 70 out of 100 samples land between 85 and 92.</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">The step inside Desmos is 15/√25, which is 3. One person would use 15.</p>',
            850, 180, 370,
        ),
        b.desmos_line("normaldist(90, 15/sqrt(25))", 580),
    ], "Say: the population can be any shape. The averages still make a bell, centered at 90, with step 3. "
       "Type normaldist(90, 15/sqrt(25)). Desmos opens the area box. Choose Inner, and set 85 and 92. Desmos shows more decimals. The book rounds to 0.6997, about 70%. "
       "Watch for: normaldist(90, 15). That is one person, the chapter 6 bell. The sample size has to get into the step. "
       "Part b of the example is the 96 from the previous slide. Two standard errors above 90."))
    out.append(b.section([
        b.activity_head(
            "Your turn · Try It 7.1 · 3 minutes",
            "Mean 45, step 8, sample of 30",
            "What share of the averages fall between 42 and 50? The book does not print this one.",
        ),
        s.bell_at(64, 185, 700, 390, "FIND THE SHADED SHARE", mean=45, sd=8 / math.sqrt(30),
                  shade=(42, 50), shade_label="find this share",
                  marks=[(42, "42"), (45, "45"), (50, "50")], z0=-3.6, z1=3.6),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">The step is 8 / √30, not 8. Write the decimal Desmos gives, then the percent.</p>',
            790, 230, 420,
        ),
        b.desmos_line("normaldist(45, 8/sqrt(30))", 600),
    ], "Try It 7.1. The book does not print this answer. They type normaldist(45, 8/sqrt(30)), then Inner from 42 to 50. Three minutes. "
       "The step is 8/√30 ≈ 1.46, so 42 and 50 are not close calls. A strong student sees that both ends are more than two steps out and says about 98% before typing. "
       "The precise share is 0.9797. If they report a number near 0.5, they used step 8, one person, instead of the average."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Try It 7.1")
            + b.title("About 98%", 56),
            64, 36, 700,
        ),
        s.bell_at(64, 175, 700, 420, "ALMOST THE WHOLE BELL", mean=45, sd=8 / math.sqrt(30),
                  shade=(42, 50), shade_label="about 98%",
                  marks=[(42, "42"), (45, "45"), (50, "50")], z0=-3.6, z1=3.6),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:26px;line-height:1.4;">8 / √30 ≈ 1.46</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">The precise share is 0.9797, which is 97.97%.</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">The book does not print this Try It. 42 and 50 are more than two small steps from 45.</p>',
            800, 210, 420,
        ),
    ], "Say the step once: the square root of 30 is about 5.5, and 8 divided by 5.5 is about 1.46. Then the share is 0.9797, about 98 out of 100 samples. "
       "Ask what 0.9797 is as a percent. Move the decimal two places. Then go to the soccer matches."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 7.2 · soccer, over age 40")
            + b.title("One match wanders. Fifty do not.", 40),
            64, 24, 1150,
        ),
        s.bell_at(64, 145, 760, 400, "AVERAGE OF 50 MATCHES", mean=2, sd=0.5 / math.sqrt(50),
                  shade=(1.8, 2.3), shade_label="99.8%",
                  marks=[(1.8, "1.8"), (2, "2")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.4;">The book’s answer for the average is <b>0.9977</b>.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.4;">One match, step 0.5, gives about 38% for the same hours. The book does not print that 38%.</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:20px;line-height:1.4;">Mean 2 hours. The average’s step is 0.5 / √50 ≈ 0.071.</p>',
            850, 165, 370,
        ),
        b.desmos_line("normaldist(2, 0.5/sqrt(50))", 580),
    ], "Say: a single match averages 2 hours and wanders by half an hour. Between 1.8 and 2.3 hours is ordinary for one match, about 38%. That 38% is the chapter 6 calculation with step 0.5. The book does not print it. "
       "The average of 50 matches has step 0.5/√50 ≈ 0.071. The same hours now cover almost the whole bell. The book’s answer is 0.9977. "
       "The population was already a bell. The new fact is how small the step became. "
       "Try It 7.2, only if asked: SAT time, mean 2.5 hours, step 0.25, n = 60, between 2 and 3 hours. The step is about 0.032, so the share is essentially 1. The book does not print it. "
       "Watch for: typing 0.5 as the step. That answers a different question."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Example 7.3 · ages of iPad users")
            + b.title("Mean 34, step 15, sample of 100", 40),
            64, 24, 1150,
        ),
        s.bell_at(64, 150, 560, 370, "95% OF THE AVERAGES", mean=34, sd=1.5,
                  shade=(None, 36.5), shade_label="95%",
                  marks=[(34, "34"), (36.5, "36.5")]),
        s.bell_at(656, 150, 560, 370, "OVER AGE 30", mean=34, sd=1.5,
                  shade=(30, None), shade_label="99.6%",
                  marks=[(30, "30"), (34, "34")]),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.4;">'
            'The average’s step is 15/√100 = 1.5. The 95th percentile is 36.5, not a person’s age. The chance the average is over 30 is 0.9962.</p>',
            64, 540, 1150,
        ),
        b.desmos_line("normaldist(34, 15/sqrt(100)).inversecdf(0.95)", 600),
    ], "This slide can wait if 6.2 ran long. Say: 100 users, so the step shrinks from 15 years to 1.5 years. The 95th percentile of the average is 36.5. Ninety-five out of 100 samples have an average age of 36.5 or younger. "
       "The trap is using the person’s step. 34 + 1.64(15) is about 59, a person’s age. The average only gets 1.64 steps of 1.5, which is 36.5. The book rounds invNorm to 36.5. "
       "Over 30: 30 is (34 − 30) / 1.5 ≈ 2.7 steps below the mean, so almost every sample of 100 averages more than 30. The book’s area is 0.9962. "
       "Example 7.4, only if asked: app engagement, mean 8.2 minutes, step 1 minute, n = 60. The standard error is 1/√60 ≈ 0.129. The 90th percentile is 8.37 minutes. Between 8 and 8.5 is 0.9293. "
       "Try It 7.4, only if asked: cola cans, mean 16 ounces, step 0.143, n = 34. The chance the average exceeds 16.01 ounces is about 0.342, about 34%. The book does not print it. An average of 16.01 is not a surprise."))
    out.append(b.quick("One person, or the average", [
        ("Mean 90, step 15, n = 25. The average’s step is",
         [("A", "3"), ("B", "15"), ("C", "0.6")], "A",
         "15 / √25 = 3."),
        ("The center of those averages is",
         [("A", "90"), ("B", "3"), ("C", "90 / 25")], "A",
         "The center does not move."),
        ("A sample mean from 85 to 92 happens",
         [("A", "About 70%"), ("B", "About 7%"), ("C", "At the score 96")], "A",
         "0.6997. 96 is a cutoff."),
    ], "Answers: 1A, 2A, 3A. If they pick 0.6, they divided by 25 instead of by the square root of 25. If they pick 15, they used one person’s step. "
       "Do 15/√25 on the board before you leave. Homework is items 61 through 71."))
    out.append(b.closing(
        "Before Tuesday",
        "The average has a smaller step",
        [
            "The center stays the population mean. The step becomes σ / √n.",
            "Type normaldist with the smaller step. Desmos opens the area box. A cutoff uses inversecdf.",
            "Tuesday is one sample, and how sure we are about the mean.",
        ],
        ("8.1 Confidence", "Tuesday. A range for the unknown mean."),
        "Homework: OpenStax 7.1, items 61 through 71. Unit 4 is due today.",
        "Items 72 and up are sums, section 7.2, and the later sections 7.3 and 7.4. This unit stops at 7.1. "
        "Exam 2 is Monday, November 23. It covers Units 4 and 5: sections 6.1, 6.2, 7.1, 8.1, 8.2, and 8.3. The bootstrap unit is not on it.",
    ))
    return out


def pair(left, top, width, height):
    """One person, step 15, and the average of 25, step 3. Same center, 90."""
    mean, lo, hi = 90.0, 45.0, 135.0
    pad_l, pad_r, pad_t, pad_b = 28, 16, 36, 34
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
        f'<text x="16" y="24" font-size="13" fill="#2a6f7a" font-family="{s.FONT}" '
        f'font-weight="700" letter-spacing="1.1">MEAN 90</text>',
        f'<polygon points="{fill}" fill="#d7ebe8"></polygon>',
        f'<polyline points="{path(wide)}" fill="none" stroke="#8aa8a4" stroke-width="2.4"></polyline>',
        f'<polyline points="{path(narrow)}" fill="none" stroke="#2a6f7a" stroke-width="2.8"></polyline>',
        f'<line x1="{X(mean):.1f}" y1="{pad_t:.1f}" x2="{X(mean):.1f}" y2="{base:.1f}" '
        f'stroke="#2a6f7a" stroke-width="1.4" stroke-dasharray="4 4"></line>',
    ]
    # The wide curve at 70 (a bit left of center) is high enough for a label.
    wide_y = base - math.exp(-0.5 * ((70 - mean) / 15) ** 2) * (plot_h - 8)
    parts.append(
        f'<text x="{X(62):.1f}" y="{wide_y - 8:.1f}" text-anchor="middle" font-size="14" '
        f'fill="#5d6670" font-family="{s.FONT}">one person</text>'
    )
    peak = base - (plot_h - 8)
    parts.append(
        f'<text x="{X(mean + 12):.1f}" y="{((peak + base) / 2):.1f}" text-anchor="start" font-size="15" '
        f'fill="#1c242c" font-family="{s.FONT}" font-weight="700">average of 25</text>'
    )
    for value, label in ((45, "45"), (90, "90"), (135, "135")):
        parts.append(
            f'<text x="{X(value):.1f}" y="{height - 12}" text-anchor="middle" font-size="14" '
            f'fill="#5d6670" font-family="{s.FONT}">{label}</text>'
        )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def main():
    b.write_deck(
        "7.1-sample-means",
        "math117-7-1-sample-means",
        "MATH 117 · 7.1 The average of a sample",
        "The average has the same center and a smaller step.",
        slides,
    )


if __name__ == "__main__":
    main()
