"""Unit S1, November 20–21. Bootstrap confidence intervals.

Introduction to Modern Statistics, chapter 12. The percentiles are the
book’s, from 10,000 resamples. One draw is not the interval.
"""

import build_2_2_to_2_7 as b
import build_6 as s
import build_8 as u

b.GRAPHS["S1"] = "https://www.desmos.com/calculator/ybx1acxbuo"
NB = "https://www.desmos.com/notebook/574zl9ghhq"

FONT = s.FONT
TAP = [0.0417, 0.025, 0.025, 0.0083, 0.05, 0.0333, 0.025, 0, 0.0083, 0]


def calc_line(command, how, top):
    return u.calc_line(command, how, top, "S1")


def resample_dots(left, top, width, height):
    """The book’s first ten tapper resamples. Duplicates stack."""
    lo, hi = -0.004, 0.058
    pad_l, pad_r = 70, 40
    axis = 250

    def X(v):
        return pad_l + (v - lo) / (hi - lo) * (width - pad_l - pad_r)

    stacks = {}
    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#ffffff" '
        f'stroke="#e4e1da" stroke-width="1.4"></rect>',
        f'<text x="18" y="28" font-size="13" fill="#2a6f7a" font-family="{FONT}" '
        f'font-weight="700" letter-spacing="1.1">TEN RESAMPLES FROM THE BOOK, NOT THE INTERVAL</text>',
        f'<line x1="{X(lo):.1f}" y1="{axis}" x2="{X(hi):.1f}" y2="{axis}" stroke="#d5e0de" stroke-width="3"></line>',
    ]
    for value in TAP:
        key = round(value, 4)
        level = stacks.get(key, 0)
        stacks[key] = level + 1
        x = X(value)
        y = axis - 22 - level * 22
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#2a6f7a"></circle>')
    for value, label in ((0, "0"), (0.025, "0.025"), (0.05, "0.05")):
        x = X(value)
        parts.append(
            f'<line x1="{x:.1f}" y1="{axis}" x2="{x:.1f}" y2="{axis + 10}" stroke="#5d6670" stroke-width="2"></line>'
            f'<text x="{x:.1f}" y="{axis + 32}" text-anchor="middle" font-size="16" fill="#1c242c" '
            f'font-family="{FONT}" font-weight="650">{label}</text>'
        )
    parts.append(
        f'<text x="{width / 2:.0f}" y="{height - 22}" text-anchor="middle" font-size="16" fill="#1c242c" '
        f'font-family="{FONT}">The 10,000-resample interval is 0 to 0.0583. These ten dots are not that interval.</text>'
    )
    return b.drawing(b.svg_wrap("".join(parts), width, height), left, top, width, height)


def slides():
    out = []
    out.append(s.opening(
        "Resample the data you have",
        "A bootstrap sample is the same records,<br>drawn again with replacement.<br>The middle 95% of those proportions is the interval.",
        "CHAPTER 12",
        u.interval_line(
            760, 140, 450, 470, -0.01, 0.14,
            [(0, "", "0"), (0.048, "0.048", ""), (0.113, "", "0.113")],
            "3 OF 62 · 10,000 RESAMPLES",
            "0 to 11.3%. The national 10% is inside.",
            band=(0, 0.113),
        ),
        "Say: a bootstrap sample is not a new survey. It is the data you already have, drawn again with replacement, at the same size. "
        "The point estimate stays the center. The resamples show how that estimate would vary. "
        "Point at 0.048, which is 3 divided by 62. The shaded interval from the book’s 10,000 resamples runs from 0 to 0.113. The national rate, about 10%, sits inside it. "
        "These percentiles are the book’s. We do not invent a new simulation. "
        "About one class period, Friday and Saturday. Unit S1 is due November 21. Exam 2 does not include this unit.",
        unit_line="Unit S1 · Bootstrap intervals",
    ))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The medical consultant")
            + b.title("3 complications in 62 surgeries", 40),
            64, 24, 1150,
        ),
        *b.three_cards([
            ("Parameter", "p, the true rate", "The true complication rate for this consultant’s clients. The sample does not hand you p."),
            ("Statistic", "p-hat = 0.048", "3 divided by 62. The point estimate. The book writes 0.048."),
            ("A comparison", "About 10%", "The national rate for liver-donor surgeries. That 10% is not p."),
        ], 170, 280),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">The data are observational. A lower rate does not, by itself, show that her work caused it.</p>',
            64, 500, 1150,
        ),
        calc_line("3/62", "the point estimate 0.048", 580),
    ], "The book’s case: one consultant, 3 complications in 62 liver-donor surgeries. "
       "p is the true complication rate for her clients. p-hat is 3 divided by 62, which the book writes as 0.048. That is the statistic, the point estimate. "
       "The national average is about 10%. That number is a comparison. It is not the parameter. "
       "The claim that her work caused the lower rate does not follow. Patients who hire a consultant may also have other advantages. Say confounding once, in that plain sentence, and move on. "
       "The likely mistake is treating 0.048 as the true rate, or treating 10% as the center of the interval."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Sampling with replacement")
            + b.title("Draw 62 records, putting each one back", 36),
            64, 22, 1150,
        ),
        *b.three_cards([
            ("The bag", "59 and 3", "59 records with no complication, and 3 with a complication. The bag is the sample."),
            ("One resample", "62 draws", "Each draw is replaced. A record can appear more than once. The size stays 62."),
            ("Then again", "10,000 times", "Each resample has its own proportion. One proportion is not the interval."),
        ], 160, 280),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">A single simulation lands near 0.048, the rate in the original sample. The next one moves a little. The book uses the pile of 10,000.</p>',
            64, 500, 1150,
        ),
    ], "There are 59 surgeries with no complication and 3 with a complication. A bootstrap draw picks one of the 62 records and puts it back, then does that 62 times. "
       "Because the record goes back, the same patient can be drawn twice. That is sampling with replacement. The sample size stays 62. "
       "One resample produces one bootstrap proportion, written p-hat boot. The book says a single simulation is about 4.8%, with a little variation. "
       "The book then repeats the simulation 10,000 times. The likely mistake is treating the first resample as the confidence interval."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The book’s 10,000 resamples")
            + b.title("The 95% interval is 0 to 0.113", 40),
            64, 20, 1150,
        ),
        u.interval_line(
            64, 130, 1152, 370, -0.02, 0.16,
            [(0, "2.5%", "0"), (0.048, "0.048", ""), (0.10, "10%", ""), (0.113, "97.5%", "0.113")],
            "PERCENTILE INTERVAL",
            "Sort the bootstrap proportions. Lower is the 2.5% value. Upper is the 97.5% value.",
            band=(0, 0.113),
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            '0 to 0.113 is 0% to 11.3% of patients. 10% is inside the interval.</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'The interval does not show that her rate is below the national 10%.</p>',
            64, 530, 1150,
        ),
    ], "The book’s figure: 10,000 bootstrap proportions, centered on 3/62. The 2.5 percentile is 0 and the 97.5 percentile is 0.113. "
       "The 95% percentile interval is those two ends: 0 to 0.113, which is 0% to 11.3%. The ends are shares of patients, not counts of complications. "
       "Point at 10%. It sits inside 0 to 11.3%. So the interval does not show that the consultant’s rate is under the national rate. It might be lower, and it might be higher. "
       "Also say again: even a rate below 10% would not, from these data, show that her work caused it. "
       "The likely mistake is reading 0.113 as 113 patients, or as 11.3 complications."))
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("The tapper and the listener")
            + b.title("3 of 120 listeners guessed the song", 36),
            64, 18, 1150,
        ),
        resample_dots(64, 130, 1152, 420),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'The point estimate is 3/120 = 0.025. One of those ten resamples is 2/120 = 0.0167.</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;">'
            'The book’s 95% interval, from 10,000 resamples, is 0 to 0.0583. That is 0% to 5.83%. 50% is far outside it.</p>',
            64, 570, 1150,
        ),
    ], "Elizabeth Newton’s study, as the book tells it: 120 listeners, and 3 guessed the tapped song. p-hat is 3/120 = 0.025. "
       "The book lists ten bootstrap proportions: 0.0417, 0.025, 0.025, 0.0083, 0.05, 0.0333, 0.025, 0, 0.0083, and 0. The dots are those ten. Duplicates stack. "
       "One of them is 2 correct out of 120, which is 0.0167. That single value is a bootstrap proportion, not the interval. "
       "The book then runs 10,000 resamples. The 2.5 percentile is 0 and the 97.5 percentile is 0.0583. The 95% interval is 0 to 5.83%. "
       "Tappers expected about 50%. 50% is not in the interval, and it is far from the largest resample the book describes. "
       "The likely mistake is averaging the ten dots and calling that the interval."))
    out.append(b.section([
        b.activity_head(
            "Your turn · 2 minutes",
            "Does the interval sit under 10%?",
            "The consultant’s 95% interval is 0 to 11.3%. The national rate is about 10%. Does the interval show that her rate is under 10%?",
        ),
        u.interval_line(
            64, 210, 700, 400, -0.02, 0.16,
            [(0, "", "0"), (0.048, "0.048", ""), (0.10, "10%", ""), (0.113, "", "11.3%")],
            "0 TO 11.3%",
            "Look at whether 10% is inside the shaded interval.",
            band=(0, 0.113),
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">The question is about the national rate, not about a new calculation.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">No. 10% is inside 0 to 11.3%.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#2a6f7a;font-size:22px;font-weight:650;line-height:1.35;">The study is observational, so it also does not show cause.</p>',
            210,
        ), 790, 280, 420, 210),
    ], "This is the book’s question after Figure 12.6. Give them a minute to look at the picture before the fragment. "
       "10% is between 0 and 11.3%, so the interval does not show that her rate is under the national rate. "
       "The second line is the book’s other warning: the data are observational, so the interval does not show that her work caused the complication rate. "
       "The likely mistake is saying yes, because 0.048 is less than 0.10. The point estimate is lower. The interval still reaches past 10%."))
    out.append(b.quick("Point estimate or interval", [
        ("A bootstrap sample is drawn",
         [("A", "With replacement, from the data"), ("B", "From the whole country"), ("C", "Once, and that draw is the interval")], "A",
         "Same records, put back each time."),
        ("3 of 62. The point estimate is",
         [("A", "0.048"), ("B", "0.10"), ("C", "3")], "A",
         "3/62 = 0.048. 10% is the national rate."),
        ("The tapper interval, 0 to 5.83%",
         [("A", "Contains 50%"), ("B", "Does not contain 50%"), ("C", "Is a count of listeners")], "B",
         "50% is far outside 0 to 5.83%."),
    ], "Answers: 1A, 2A, 3B. A bootstrap sample is drawn with replacement from the observed data. One draw is not the interval. "
       "3 of 62 is the point estimate 0.048. The 3 is a count, and 0.10 is the national comparison. "
       "The tapper interval 0 to 5.83% does not contain 50%, and it is a share of listeners, not a count. "
       "Homework is Introduction to Modern Statistics, chapter 12, exercises 1 through 8. Unit S1 is due November 21."))
    out.append(b.closing(
        "Before you leave",
        "The middle of the resamples",
        [
            "A bootstrap sample redraws the data, with replacement.",
            "The 95% interval runs from the 2.5% resample to the 97.5% resample.",
            "One resample is a proportion. It is not the interval.",
        ],
        ("Exam 2", "November 22–23. Units 4 and 5. This unit is not on the exam."),
        "Homework: Introduction to Modern Statistics, chapter 12, exercises 1 through 8. Unit S1 is due November 21.",
        "The consultant interval is the book’s: 0 to 0.113, from 10,000 resamples. The tapper interval is 0 to 0.0583. "
        "The calculator card is the class graph. The notebook card is the same examples as a short lesson. "
        "Do not start a new bootstrap and report different ends. The homework pictures are in the book. "
        "Unit S1 is due Saturday, November 21. Exam 2 does not include this unit.",
        graph="S1",
        notebook=NB,
    ))
    return out


def main():
    b.write_deck(
        "s1-bootstrap",
        "math117-s1-bootstrap",
        "MATH 117 · Bootstrap confidence intervals",
        "Resample the data. The middle 95% of the bootstrap proportions is the interval.",
        slides,
    )


if __name__ == "__main__":
    main()
