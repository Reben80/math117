"""Unit 4 exam-prep gap: OpenStax 7.3 sampling distribution of a proportion,
plus sample size for a proportion (Exam 2 Q8/Q9/Q11/Q17; Units 4–5 review Q9–Q12/Q26).

Short deck. Matches build_6 / build_7 / build_8 design. Not a full rewrite of 7.2–7.4.
"""

import math

import build_2_2_to_2_7 as b
import build_6 as s

# Saved in the instructor's Desmos account. Built from desmos_graphs.js (M117.build("7.3")).
b.GRAPHS["7.3"] = "https://www.desmos.com/calculator/b2mauih92w"


def calc_line(command, how, top, graph="7.3"):
    """The monospace part is what students type. The rest is the Desmos box."""
    label = '<span style="color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">DESMOS</span>'
    if graph and graph in b.GRAPHS and "PLACEHOLDER" not in b.GRAPHS[graph]:
        label = (
            '<a href="' + b.GRAPHS[graph] + '" target="_blank" style="text-decoration:none;">'
            '<span style="color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">DESMOS ↗</span></a>'
        )
    elif graph and graph in b.GRAPHS:
        label = (
            '<span style="color:#2a6f7a;font-size:14px;font-weight:700;letter-spacing:0.12em;">DESMOS ↗</span>'
        )
    return b.text_block(
        '<p style="margin:0;color:#1c242c;font-size:20px;line-height:1.35;">'
        + label
        + '&nbsp;&nbsp;<span style="font-family:Menlo, Consolas, monospace;">' + command + '</span>'
        '&nbsp;&nbsp;<span style="color:#5d6670;">' + how + '</span></p>',
        64, top, 1160,
    )


def slides():
    out = []
    # 1 · Opening
    out.append(s.opening(
        "Sample proportions also have a sampling distribution",
        "Same idea as sample means, but for a share.<br>"
        "Mean " + s.m(r"p") + ", standard error " + s.m(r"\sqrt{p(1-p)/n}") + ".",
        "SECTION 7.3 · EXAM 2 PREP",
        s.bell_at(
            760, 120, 450, 480, "SAMPLE PROPORTIONS",
            mean=0.6, sd=math.sqrt(0.6 * 0.4 / 49),
            shade=(0.5, 0.7), shade_label="near 0.6",
            marks=[(0.5, "0.5"), (0.6, "0.6"), (0.7, "0.7")],
            z0=-3.2, z1=3.2, label_size=16,
        ),
        "Say: section 7.1 was the sample mean. Today is the sample proportion, p-hat. "
        "Point at the narrow curve. Many samples of the same size give many p-hats. Those p-hats pile up around the true p. "
        "This short deck closes Exam 2 gaps: mean and SE of p-hat, the np and n(1-p) check, probability questions, and sample size for a proportion. "
        "Keep it to about 20–25 minutes. Do not open sections 7.2 or 7.4.",
        unit_line="Unit 4 · Exam 2 prep",
    ))
    # 2 · Formulas
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Sampling distribution of p-hat")
            + b.title("Center at p. Spread shrinks with n.", 38),
            64, 24, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">MEAN</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:30px;">' + s.M(r"\mu_{\hat{p}}=p") + '</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'The average of all possible sample proportions equals the true population proportion.</p>'
            '<p style="margin:18px 0 0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">STANDARD ERROR</p>'
            '<p style="margin:8px 0 0;color:#1c242c;font-size:30px;">'
            + s.M(r"\mathrm{SE}=\sigma_{\hat{p}}=\sqrt{\dfrac{p(1-p)}{n}}") + '</p>'
            '<p style="margin:4px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'How much p-hat typically moves from sample to sample. Larger n makes a smaller SE.</p>',
            64, 145, 620,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">LIKE 7.1, BUT FOR A SHARE</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'Means used ' + s.m(r"\sigma/\sqrt{n}") + '.</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">'
            'Proportions use ' + s.m(r"\sqrt{p(1-p)/n}") + '.</p>'
            '<p style="margin:14px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'p-hat is successes divided by n. It is a share, not a count.</p>',
            320,
        ), 720, 170, 500, 320),
    ], "Say mean first: mu of p-hat equals p. The pile of sample proportions is centered at the true share. "
       "Then SE: square root of p times (1 − p) over n. That is the typical spread of those sample proportions. "
       "Compare once to 7.1: means divide sigma by square root of n. Proportions put p(1 − p) under the square root with n. "
       "Misconception: writing the SE as p(1 − p)/n without the square root. Another: calling the SE the mean."))
    # 3 · Success–failure
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("When the normal model is OK")
            + b.title("Success–failure: both at least 10", 40),
            64, 24, 1150,
        ),
        *b.three_cards([
            ("Expected successes", "np ≥ 10", "n times the true proportion p."),
            ("Expected failures", "n(1 − p) ≥ 10", "n times the failure share."),
            ("Then use", "a normal curve", "Mean p. SE = √[p(1 − p)/n]."),
        ], 160, 280),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'If either count is under 10, do not treat p-hat as approximately normal for these probability questions.</p>'
            '<p style="margin:10px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'Section 8.3 uses a related check for confidence intervals (successes and failures both more than 5). '
            'On Exam 2 sampling-distribution items, use np and n(1 − p) both ≥ 10.</p>',
            64, 500, 1150,
        ),
    ], "Say success–failure before any probability. Expected successes: n times p. Expected failures: n times (1 − p). Both need to be at least 10. "
       "Then the sampling distribution of p-hat is approximately normal with mean p and that SE. "
       "Mention once that 8.3’s confidence-interval check is a cousin (more than 5 each). For these Exam 2 items, stick to ≥ 10. "
       "Misconception: checking only np and skipping failures."))
    # 4 · Mean and SE worked example (Exam Q8 style)
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Worked · mean and SE")
            + b.title("True share 0.64, sample size 210", 40),
            64, 22, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">MEAN OF p-HAT</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:36px;font-weight:650;">0.64</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            + s.m(r"\mu_{\hat{p}}=p") + '. Copy the true proportion.</p>',
            200,
        ), 64, 150, 560, 200),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">STANDARD ERROR</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:28px;line-height:1.3;">'
            + s.m(r"\sqrt{0.64\cdot 0.36/210}") + ' ≈ <b>0.033</b></p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'Round the SE to three decimals when asked.</p>',
            200,
        ), 656, 150, 560, 200),
        calc_line("sqrt(0.64*0.36/210)", "gives about 0.03312 → 0.033", 420, graph="7.3"),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'Exam-style: report the mean as 0.64 and the SE as 0.033. Do not replace p with a sample p-hat here — the true p is given.</p>',
            64, 520, 1150,
        ),
    ], "Read p = 0.64 and n = 210. The mean of the sampling distribution is 0.64. "
       "SE is the square root of 0.64 times 0.36 over 210. Desmos: sqrt(0.64*0.36/210) ≈ 0.03312, and the exam asks for three decimals, 0.033. "
       "Misconception: using 0.64 times 0.36 without dividing by n, or forgetting the square root."))
    # 5 · Normal check (Exam Q9 style)
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Worked · is it normal?")
            + b.title("p = 0.6, n = 49", 44),
            64, 22, 1150,
        ),
        *b.three_cards([
            ("Mean", "0.600", "μ of p-hat equals p."),
            ("SD / SE", "0.06999", "√(0.6·0.4/49). Keep ≥ 5 decimals if asked."),
            ("Normal?", "Yes", "np = 29.4 and n(1 − p) = 19.6, both ≥ 10."),
        ], 155, 300),
        calc_line("sqrt(0.6*0.4/49)", "≈ 0.069985 → 0.06999", 520),
        b.text_block(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'Always check np and n(1 − p) before you shade a normal area for p-hat.</p>',
            64, 600, 1150,
        ),
    ], "Mean 0.600. SE = √(0.6 × 0.4 / 49) ≈ 0.06999 when five decimals are required. "
       "np = 49 × 0.6 = 29.4. n(1 − p) = 49 × 0.4 = 19.6. Both at least 10, so yes, use the normal model. "
       "Misconception: saying no because n = 49 is under 30. The n ≥ 30 rule was for means with an unknown shape. Here the check is np and n(1 − p)."))
    # 6 · Probability for p-hat (Exam Q11 / review style)
    se11 = math.sqrt(0.57 * 0.43 / 580)
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Worked · probability for p-hat")
            + b.title("p = 0.57, n = 580. Between 324 and 336 successes.", 32),
            64, 18, 1150,
        ),
        s.bell_at(
            64, 125, 700, 390, "SAMPLE PROPORTIONS",
            mean=0.57, sd=se11,
            shade=(324 / 580, 336 / 580), shade_label="0.3847",
            marks=[(324 / 580, "324/580"), (0.57, "0.57"), (336 / 580, "336/580")],
            z0=-3.4, z1=3.4, label_size=15, label_gap=52,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'Convert counts to shares first.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">'
            + s.m(r"324/580") + ' and ' + s.m(r"336/580") + '.</p>'
            '<p style="margin:10px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'SE ≈ 0.0206.</p>'
            '<p style="margin:12px 0 0;color:#2a6f7a;font-size:26px;font-weight:650;">'
            'P ≈ 0.3847</p>',
            800, 160, 420,
        ),
        calc_line("normaldist(0.57, sqrt(0.57*0.43/580))", "then Inner, 324/580 to 336/580", 560),
    ], "Say: the question may give counts. Turn them into proportions before you shade. 324/580 and 336/580. "
       "SE = √(0.57 × 0.43 / 580) ≈ 0.0206. Type normaldist(0.57, sqrt(0.57*0.43/580)), then Inner from 324/580 to 336/580. About 0.3847. "
       "Misconception: using normaldist on the counts 324 and 336 with SD 0.0206. The curve is on the proportion scale."))
    # 7 · Your turn
    se10 = math.sqrt(0.25 * 0.75 / 71)
    out.append(b.section([
        b.activity_head(
            "Your turn · 4 minutes",
            "p = 0.25, n = 71",
            "Find " + s.m(r"P(\hat{p} < 0.26)") + ". First write the SE, then use Desmos.",
        ),
        s.bell_at(
            64, 175, 680, 370, "SAMPLE PROPORTIONS",
            mean=0.25, sd=se10,
            shade=(None, 0.26), shade_label="P(p-hat < 0.26)",
            marks=[(0.25, "0.25"), (0.26, "0.26")],
            z0=-3.2, z1=3.2, label_size=16,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'SE = √(0.25 × 0.75 / 71) ≈ 0.0514.</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:14px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">'
            '0.5771</p>'
            '<p class="fragment" data-fragment-index="0" style="margin:8px 0 0;color:#5d6670;font-size:18px;">'
            'np = 17.75 and n(1 − p) = 53.25, both ≥ 10.</p>',
            220,
        ), 780, 230, 440, 220),
        calc_line("normaldist(0.25, sqrt(0.25*0.75/71))", "then Left of 0.26", 600),
    ], "Review-style item. SE ≈ 0.0514. Left of 0.26 is about 0.5771. "
       "Check: 71 × 0.25 = 17.75 and 71 × 0.75 = 53.25, both at least 10. "
       "If they get about 0.42, they used Right. If they get near 0.5 with SD 0.25, they forgot the SE."))
    # 8 · Sample size for a proportion
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Sample size for a proportion")
            + b.title("Round n up. Worst case uses 0.5.", 38),
            64, 22, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:28px;line-height:1.3;">'
            + s.M(r"n=\left(\frac{z}{E}\right)^2\hat{p}\hat{q}") + '</p>'
            '<p style="margin:8px 0 0;color:#5d6670;font-size:20px;line-height:1.35;">'
            'E is the desired margin of error. z matches the confidence level '
            '(90%: 1.645, 95%: 1.96). '
            + s.m(r"\hat{q}=1-\hat{p}") + '.</p>'
            '<p style="margin:14px 0 0;color:#1c242c;font-size:22px;line-height:1.35;">'
            'No prior estimate? Use ' + s.m(r"\hat{p}=\hat{q}=0.5") + '. That choice makes n as large as it needs to be.</p>',
            64, 140, 1150,
        ),
        b.text_block(b.card_shell(
            '<p style="margin:0;color:#2a6f7a;font-size:15px;font-weight:700;letter-spacing:0.12em;">EXAM STYLE · 90%, WITHIN 0.04</p>'
            '<p style="margin:12px 0 0;color:#1c242c;font-size:24px;line-height:1.35;">'
            + s.m(r"n=(1.645/0.04)^2(0.5)(0.5)=422.816") + '</p>'
            '<p style="margin:10px 0 0;color:#2a6f7a;font-size:28px;font-weight:650;">Round up → n = 423</p>',
            180,
        ), 64, 420, 1150, 180),
        calc_line("(1.645/0.04)^2*0.25", "422.816… then always round up", 640),
    ], "Write the formula once. z over E, squared, times p-hat q-hat. No prior p-hat means use 0.5 and 0.5, so the product is 0.25. "
       "Example: 90% confidence, within 0.04. (1.645/0.04)^2 × 0.25 ≈ 422.816. Always round up, so n = 423. Never round to 422. "
       "A second flash if time: 95%, within 0.05 → (1.96/0.05)^2 × 0.25 = 384.16 → n = 385. "
       "Misconception: rounding down, or forgetting the 0.25 when there is no prior estimate."))
    # 9 · Optional mean sample-size reminder
    out.append(b.section([
        b.backdrop(),
        b.text_block(
            b.kicker("Quick reminder from 8.1 notes")
            + b.title("Sample size for a mean", 44),
            64, 28, 1150,
        ),
        b.text_block(
            '<p style="margin:0;color:#1c242c;font-size:30px;line-height:1.3;">'
            + s.M(r"n=\left(z\frac{\sigma}{E}\right)^2") + '</p>'
            '<p style="margin:12px 0 0;color:#5d6670;font-size:22px;line-height:1.35;">'
            'Known population standard deviation σ. Desired margin of error E. Same z cutoffs. Round up.</p>',
            64, 160, 1150,
        ),
        *b.three_cards([
            ("Proportion", "n = (z/E)² p̂q̂", "No prior? Use 0.5 × 0.5."),
            ("Mean", "n = (z σ / E)²", "Needs σ from the problem."),
            ("Both", "Round up", "422.8 → 423. 20.3 → 21."),
        ], 360, 260),
    ], "One slide only. Means use n = (z σ / E)^2 from the 8.1 speaker notes. Proportions use (z/E)^2 p-hat q-hat. "
       "Both round up. Do not linger. If the hour is short, skip this slide and stay on the proportion formula."))
    # 10 · Quick check
    out.append(b.quick("Before Exam 2", [
        ("For p-hat, the mean of the sampling distribution is",
         [("A", "p"), ("B", "√[p(1 − p)/n]"), ("C", "n")], "A",
         "μ of p-hat equals p."),
        ("p = 0.5, n = 100. The SE is",
         [("A", "0.5"), ("B", "0.05"), ("C", "0.25")], "B",
         "√(0.5 × 0.5 / 100) = 0.05."),
        ("No prior p-hat, 95%, E = 0.05. n is",
         [("A", "384"), ("B", "385"), ("C", "196")], "B",
         "(1.96/0.05)^2 × 0.25 = 384.16 → round up."),
    ], "Answers: 1A, 2B, 3B. If they pick 0.25 for the SE, they forgot the square root and the division by n. "
       "If they pick 384, they rounded down. Exam 2 includes these skills on Units 4–5."))
    # 11 · Closing
    closing_graph = "7.3" if "PLACEHOLDER" not in b.GRAPHS.get("7.3", "") else None
    out.append(b.closing(
        "Exam 2 prep",
        "Four moves for p-hat",
        [
            "Mean of p-hat is p. SE is √[p(1 − p)/n].",
            "Normal when np and n(1 − p) are both ≥ 10.",
            "For probabilities, put the SE in normaldist, then Left / Right / Inner.",
            "Sample size: n = (z/E)² p̂q̂. No prior? Use 0.5. Round up.",
        ],
        ("Exam 2", "Units 4 and 5. Sections 6.1, 6.2, 7.1, 8.1, 8.2, 8.3 — plus this 7.3 gap."),
        "Practice: Units 4–5 review Q9–Q12 and Q26. Then Exam 2 Q8, Q9, Q11, Q17.",
        "This deck is short on purpose. It does not replace 7.1 or 8.3. "
        "Desmos commands on the worked slides open the class graph. "
        "Do not change the Exam 2 assignment itself.",
        graph=closing_graph,
    ))
    return out


def main():
    b.write_deck(
        "7.3-sample-proportions",
        "math117-7-3-sample-proportions",
        "MATH 117 · 7.3 Sample proportions (Exam 2 prep)",
        "Sampling distribution of p-hat, probability questions, and sample size for a proportion.",
        slides,
    )


if __name__ == "__main__":
    main()
