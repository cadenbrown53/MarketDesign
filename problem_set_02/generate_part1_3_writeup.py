from __future__ import annotations

import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

from matching_mechanisms import (  # noqa: E402
    average_rank,
    deferred_acceptance,
    generate_market,
    immediate_acceptance,
    simulate,
    ttc,
)

MARKET_SEED = 42
SIM_SEED = 123
SIM_N = 1000
WRITEUP_PATH = ROOT / "problem_set_02" / "part1_3_writeup.md"
WRITEUP_TEX_PATH = ROOT / "problem_set_02" / "part1_3_writeup.tex"
PART1_REFERENCE = ROOT / "problem_set_02" / "market_setup_output.md"


def assignment_table(students: list[str], da: dict[str, str], ia: dict[str, str], tt: dict[str, str]) -> str:
    lines = [
        "| Student | DA | IA | TTC |",
        "|---|---|---|---|",
    ]
    for student in students:
        lines.append(f"| {student} | {da[student]} | {ia[student]} | {tt[student]} |")
    return "\n".join(lines)


def average_rank_table(avg_ranks: dict[str, float]) -> str:
    lines = [
        "| Mechanism | Average Rank (lower is better) |",
        "|---|---:|",
    ]
    for mechanism in ("DA", "IA", "TTC"):
        lines.append(f"| {mechanism} | {avg_ranks[mechanism]:.4f} |")
    return "\n".join(lines)


def assignment_table_tex(students: list[str], da: dict[str, str], ia: dict[str, str], tt: dict[str, str]) -> str:
    lines = [
        "\\begin{tabular}{lccc}",
        "\\hline",
        "Student & DA & IA & TTC \\\\",
        "\\hline",
    ]
    for student in students:
        lines.append(f"{student} & {da[student]} & {ia[student]} & {tt[student]} \\\\")
    lines.extend(["\\hline", "\\end{tabular}"])
    return "\n".join(lines)


def average_rank_table_tex(avg_ranks: dict[str, float]) -> str:
    lines = [
        "\\begin{tabular}{lc}",
        "\\hline",
        "Mechanism & Average Rank (lower is better) \\\\",
        "\\hline",
    ]
    for mechanism in ("DA", "IA", "TTC"):
        lines.append(f"{mechanism} & {avg_ranks[mechanism]:.4f} \\\\")
    lines.extend(["\\hline", "\\end{tabular}"])
    return "\n".join(lines)


def interpretation(avg_ranks: dict[str, float]) -> str:
    ordered = sorted(avg_ranks.items(), key=lambda item: item[1])
    best_name, best_value = ordered[0]
    second_name, second_value = ordered[1]
    third_name, third_value = ordered[2]

    gap_best_second = second_value - best_value
    gap_best_third = third_value - best_value

    return " ".join(
        [
            f"Across {SIM_N} simulated markets, {best_name} has the lowest average rank ({best_value:.4f}), so it performs best by this preference-based metric.",
            f"{second_name} is close behind at {second_value:.4f} (a gap of {gap_best_second:.4f}), indicating similar overall assignment quality in expectation.",
            f"{third_name} is higher at {third_value:.4f}, which is {gap_best_third:.4f} worse than {best_name} on average.",
            "Because lower rank means students are assigned closer to their top choices, these differences summarize welfare trade-offs in a compact, reproducible way.",
        ]
    )


def build_writeup() -> tuple[str, dict[str, float], dict[str, float], dict[str, float], dict[str, float]]:
    random.seed(MARKET_SEED)
    students, schools, cap, prefs, prio = generate_market()

    da = deferred_acceptance(students, schools, cap, prefs, prio)
    ia = immediate_acceptance(students, schools, cap, prefs, prio)
    tt = ttc(students, schools, cap, prefs, prio)

    one_market_avg = {
        "DA": average_rank(prefs, da),
        "IA": average_rank(prefs, ia),
        "TTC": average_rank(prefs, tt),
    }

    avg_ranks = simulate(N=SIM_N, seed=SIM_SEED)

    content = f"""# Problem Set 02 — Part 1 to Part 3 Writeup

## Part 1: Preferences and Priorities Summary

The market instance uses 18 students, 3 schools, and school capacity 6 (total capacity 18), with strict random preferences and strict random school priorities.
To match the assignment setup, the one-market realization is generated with `random.seed({MARKET_SEED})`.
The detailed preference and priority lists are already recorded in [market_setup_output.md](market_setup_output.md).

## Part 2: One-Market Matching Table (Seed = {MARKET_SEED})

The table below reports student assignments under Deferred Acceptance (DA), Immediate Acceptance (IA/Boston), and Top Trading Cycles (TTC), all run on the same Part 1 market instance.

{assignment_table(students, da, ia, tt)}

### One-Market Average Rank Check

| Mechanism | Average Rank in this one market |
|---|---:|
| DA | {one_market_avg['DA']:.4f} |
| IA | {one_market_avg['IA']:.4f} |
| TTC | {one_market_avg['TTC']:.4f} |

## Part 3: Simulation Results (N = {SIM_N})

Each simulation draw generates a fresh random market, then computes DA/IA/TTC outcomes and student average rank. The simulation uses fixed seed `seed={SIM_SEED}` for reproducibility.

{average_rank_table(avg_ranks)}

### Interpretation

{interpretation(avg_ranks)}

## Reproducibility

Run the command below from the repository root to regenerate this file and all tables:

```bash
python problem_set_02/generate_part1_3_writeup.py
```
"""

    return content, da, ia, tt, avg_ranks


def build_writeup_tex(
    students: list[str],
    da: dict[str, str],
    ia: dict[str, str],
    tt: dict[str, str],
    avg_ranks: dict[str, float],
) -> str:
    # one-market averages are recomputed from the same seed-42 market for consistency
    random.seed(MARKET_SEED)
    _, _, _, prefs, _ = generate_market()
    one_market_avg_values = {
        "DA": average_rank(prefs, da),
        "IA": average_rank(prefs, ia),
        "TTC": average_rank(prefs, tt),
    }

    return f"""% Part 1-3 section generated by problem_set_02/generate_part1_3_writeup.py
% This file is intended to be \\input{{problem_set_02/part1_3_writeup.tex}} into a larger document.

\\section*{{Problem Set 02: Parts 1--3}}

\\subsection*{{Part 1: Preferences and Priorities Summary}}
The market instance uses 18 students, 3 schools, and school capacity 6 (total capacity 18), with strict random preferences and strict random school priorities. The one-market realization is generated with \\texttt{{random.seed({MARKET_SEED})}}. Detailed preference and priority lists are documented in \\texttt{{problem\\_set\\_02/market\\_setup\\_output.md}}.

\\subsection*{{Part 2: One-Market Matching Table (Seed = {MARKET_SEED})}}
The table below reports student assignments under Deferred Acceptance (DA), Immediate Acceptance (IA/Boston), and Top Trading Cycles (TTC), all run on the same Part 1 market instance.

\\begin{{center}}
{assignment_table_tex(students, da, ia, tt)}
\\end{{center}}

\\paragraph{{One-Market Average Rank Check}}
\\begin{{center}}
\\begin{{tabular}}{{lc}}
\\hline
Mechanism & Average Rank in this one market \\\\
\\hline
DA & {one_market_avg_values['DA']:.4f} \\\\
IA & {one_market_avg_values['IA']:.4f} \\\\
TTC & {one_market_avg_values['TTC']:.4f} \\\\
\\hline
\\end{{tabular}}
\\end{{center}}

\\subsection*{{Part 3: Simulation Results (N = {SIM_N})}}
Each simulation draw generates a fresh random market, then computes DA/IA/TTC outcomes and student average rank. The simulation uses fixed seed \\texttt{{seed={SIM_SEED}}} for reproducibility.

\\begin{{center}}
{average_rank_table_tex(avg_ranks)}
\\end{{center}}

\\paragraph{{Interpretation}}
{interpretation(avg_ranks)}

\\paragraph{{Reproducibility}}
From the repository root, run \\texttt{{python problem\\_set\\_02/generate\\_part1\\_3\\_writeup.py}} to regenerate both Markdown and LaTeX outputs.
"""


def main() -> None:
    content, da, ia, tt, avg_ranks = build_writeup()
    tex_content = build_writeup_tex(
        students=sorted(da.keys(), key=lambda s: int(s[1:])),
        da=da,
        ia=ia,
        tt=tt,
        avg_ranks=avg_ranks,
    )

    WRITEUP_PATH.write_text(content, encoding="utf-8")
    WRITEUP_TEX_PATH.write_text(tex_content, encoding="utf-8")

    print("One-market mapping table (Part 2)")
    print("| Student | DA | IA | TTC |")
    print("|---|---|---|---|")
    for student in sorted(da.keys(), key=lambda s: int(s[1:])):
        print(f"| {student} | {da[student]} | {ia[student]} | {tt[student]} |")

    print("\nAverage rank table (Part 3, N=1000)")
    print("| Mechanism | Average Rank (lower is better) |")
    print("|---|---:|")
    for mechanism in ("DA", "IA", "TTC"):
        print(f"| {mechanism} | {avg_ranks[mechanism]:.4f} |")

    print(f"\nWriteup generated: {WRITEUP_PATH.relative_to(ROOT)}")
    print(f"LaTeX section generated: {WRITEUP_TEX_PATH.relative_to(ROOT)}")
    if PART1_REFERENCE.exists():
        print(f"Part 1 reference file: {PART1_REFERENCE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
