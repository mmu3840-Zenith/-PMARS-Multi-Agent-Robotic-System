# PMARS Research Release Report

Automatically generated from the recorded simulation experiments.

## Benchmark results

| Strategy | Mean completion | Mean distance | Completed trials |
|---|---:|---:|---:|
| pmars | 1.0000 | 1082.73 | 30/30 |
| greedy | 1.0000 | 1092.80 | 30/30 |
| random | 1.0000 | 1089.60 | 30/30 |

### Confidence intervals

The 95% intervals below use mean ± 1.96 × sample SD / square root of n.

| Strategy | Metric | Mean | 95% interval |
|---|---|---:|---:|
| pmars | completion_rate | 1.0000 | [1.0000, 1.0000] |
| pmars | distance | 1082.7333 | [1068.4374, 1097.0292] |
| pmars | steps | 301.5667 | [297.7916, 305.3417] |
| greedy | completion_rate | 1.0000 | [1.0000, 1.0000] |
| greedy | distance | 1092.8000 | [1078.8808, 1106.7192] |
| greedy | steps | 302.4333 | [298.3971, 306.4695] |
| random | completion_rate | 1.0000 | [1.0000, 1.0000] |
| random | distance | 1089.6000 | [1076.3520, 1102.8480] |
| random | steps | 301.2333 | [297.2411, 305.2255] |

## Robot failure and recovery

Completed recovery trials: 10/10.
The experiment injects one simulated robot failure and subsequently restores that robot. It does not model real radio hardware or network packet loss.

## Scalability

| Robots | Items | Trials | Mean completion | Mean steps |
|---:|---:|---:|---:|---:|
| 1 | 12 | 3 | 1.0000 | 1885.00 |
| 1 | 24 | 3 | 1.0000 | 3757.00 |
| 1 | 48 | 3 | 1.0000 | 7501.00 |
| 2 | 12 | 3 | 1.0000 | 961.00 |
| 2 | 24 | 3 | 1.0000 | 1900.00 |
| 2 | 48 | 3 | 1.0000 | 3779.67 |
| 4 | 12 | 3 | 1.0000 | 507.00 |
| 4 | 24 | 3 | 1.0000 | 981.33 |
| 4 | 48 | 3 | 1.0000 | 1923.33 |
| 8 | 12 | 3 | 1.0000 | 303.00 |
| 8 | 24 | 3 | 1.0000 | 518.00 |
| 8 | 48 | 3 | 1.0000 | 994.33 |

## Interpretation and limitations

- All observations are from a grid-based software simulation.
- The benchmark strategies share the same navigation and movement model.
- PMARS uses priority-ordered nearest-robot assignment.
- Greedy uses task-ID order and nearest-robot assignment.
- Random selects randomly among reachable idle robots.
- The confidence intervals are descriptive, not proof of universal superiority.
- Three seeds per scalability configuration are exploratory, not definitive.
- Physical robots, cameras, real item recognition, and hardware communication have not been validated by these experiments.
- Any incomplete trial remains in the exported data.

## Reproducibility

Seeds, per-trial observations, and aggregate summaries are saved alongside this report. Run `python experiments/pmars_research/run_research.py` to regenerate them.
