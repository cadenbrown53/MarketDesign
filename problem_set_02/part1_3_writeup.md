# Problem Set 02 — Part 1 to Part 3 Writeup

## Part 1: Preferences and Priorities Summary

The market instance uses 18 students, 3 schools, and school capacity 6 (total capacity 18), with strict random preferences and strict random school priorities.
To match the assignment setup, the one-market realization is generated with `random.seed(42)`.
The detailed preference and priority lists are already recorded in [market_setup_output.md](market_setup_output.md).

## Part 2: One-Market Matching Table (Seed = 42)

The table below reports student assignments under Deferred Acceptance (DA), Immediate Acceptance (IA/Boston), and Top Trading Cycles (TTC), all run on the same Part 1 market instance.

| Student | DA | IA | TTC |
|---|---|---|---|
| i1 | s2 | s2 | s2 |
| i2 | s3 | s3 | s3 |
| i3 | s3 | s3 | s3 |
| i4 | s3 | s3 | s3 |
| i5 | s1 | s1 | s1 |
| i6 | s1 | s1 | s1 |
| i7 | s3 | s3 | s3 |
| i8 | s2 | s2 | s2 |
| i9 | s2 | s2 | s2 |
| i10 | s2 | s2 | s2 |
| i11 | s1 | s1 | s1 |
| i12 | s3 | s3 | s3 |
| i13 | s1 | s1 | s1 |
| i14 | s2 | s2 | s2 |
| i15 | s1 | s1 | s1 |
| i16 | s1 | s1 | s1 |
| i17 | s2 | s2 | s2 |
| i18 | s3 | s3 | s3 |

### One-Market Average Rank Check

| Mechanism | Average Rank in this one market |
|---|---:|
| DA | 1.2222 |
| IA | 1.2222 |
| TTC | 1.2222 |

## Part 3: Simulation Results (N = 1000)

Each simulation draw generates a fresh random market, then computes DA/IA/TTC outcomes and student average rank. The simulation uses fixed seed `seed=123` for reproducibility.

| Mechanism | Average Rank (lower is better) |
|---|---:|
| DA | 1.2086 |
| IA | 1.1837 |
| TTC | 1.1934 |

### Interpretation

Across 1000 simulated markets, IA has the lowest average rank (1.1837), so it performs best by this preference-based metric. TTC is close behind at 1.1934 (a gap of 0.0097), indicating similar overall assignment quality in expectation. DA is higher at 1.2086, which is 0.0249 worse than IA on average. Because lower rank means students are assigned closer to their top choices, these differences summarize welfare trade-offs in a compact, reproducible way.

## Reproducibility

Run the command below from the repository root to regenerate this file and all tables:

```bash
python problem_set_02/generate_part1_3_writeup.py
```
