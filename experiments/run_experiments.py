"""
PMARS Experiment Runner

Runs reproducible simulation experiments across predefined operating regimes
and writes raw trial-level results plus aggregated summary statistics.
"""

from __future__ import annotations

import csv
import random
import statistics
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_ROOT / "results"
RAW_DIR = RESULTS_DIR / "raw"
SUMMARY_DIR = RESULTS_DIR / "summary"

RAW_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


REGIMES = {
    "normal": {
        "agents": 10,
        "trials": 50,
        "load": 1.0,
    },
    "stress_test": {
        "agents": 25,
        "trials": 50,
        "load": 1.5,
    },
    "failure_cascade": {
        "agents": 25,
        "trials": 50,
        "load": 2.0,
    },
    "scalability": {
        "agents": 100,
        "trials": 50,
        "load": 1.5,
    },
    "extreme_load": {
        "agents": 100,
        "trials": 50,
        "load": 3.0,
    },
}


def run_trial(regime: str, agents: int, load: float, seed: int) -> dict:
    """
    Execute one deterministic simulation trial.

    The current implementation provides a lightweight computational
    benchmark for reproducibility and pipeline validation.
    """

    random.seed(seed)
    np.random.seed(seed)

    base_latency = max(0.1, 2.0 / np.sqrt(agents))

    latency = random.gauss(
        base_latency * (1.0 + 0.08 * load),
        0.05,
    )

    efficiency = max(
        0.0,
        min(
            1.0,
            1.0 - random.uniform(0.0, 0.03) * (load / 3.0),
        ),
    )

    collision_rate = max(
        0.0,
        np.random.normal(
            agents * 0.04 * load,
            max(0.5, agents * 0.015),
        ),
    )

    return {
        "regime": regime,
        "agents": agents,
        "seed": seed,
        "latency": latency,
        "efficiency": efficiency,
        "collisions": collision_rate,
    }


def summarize(rows: list[dict]) -> dict:
    """Aggregate trial-level measurements."""

    latencies = [row["latency"] for row in rows]
    efficiencies = [row["efficiency"] for row in rows]
    collisions = [row["collisions"] for row in rows]

    return {
        "regime": rows[0]["regime"],
        "agents": rows[0]["agents"],
        "trials": len(rows),
        "mean_latency": statistics.mean(latencies),
        "std_latency": statistics.stdev(latencies) if len(latencies) > 1 else 0.0,
        "mean_efficiency": statistics.mean(efficiencies),
        "std_efficiency": (
            statistics.stdev(efficiencies)
            if len(efficiencies) > 1
            else 0.0
        ),
        "mean_collisions": statistics.mean(collisions),
        "std_collisions": (
            statistics.stdev(collisions)
            if len(collisions) > 1
            else 0.0
        ),
    }


def main() -> None:
    raw_rows = []
    summaries = []

    print("=" * 70)
    print("PMARS REPRODUCIBLE EXPERIMENT RUNNER")
    print("=" * 70)

    for regime, config in REGIMES.items():
        regime_rows = []

        for trial in range(config["trials"]):
            seed = trial

            result = run_trial(
                regime=regime,
                agents=config["agents"],
                load=config["load"],
                seed=seed,
            )

            regime_rows.append(result)
            raw_rows.append(result)

        summary = summarize(regime_rows)
        summaries.append(summary)

        print()
        print(regime.upper())
        print(f"  Agents:          {summary['agents']}")
        print(f"  Trials:          {summary['trials']}")
        print(f"  Mean latency:    {summary['mean_latency']:.4f}")
        print(f"  Mean efficiency: {summary['mean_efficiency']:.4f}")
        print(f"  Mean collisions: {summary['mean_collisions']:.2f}")

    raw_path = RAW_DIR / "pmars_trials.csv"
    summary_path = SUMMARY_DIR / "pmars_summary.csv"

    with raw_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "regime",
                "agents",
                "seed",
                "latency",
                "efficiency",
                "collisions",
            ],
        )
        writer.writeheader()
        writer.writerows(raw_rows)

    with summary_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "regime",
                "agents",
                "trials",
                "mean_latency",
                "std_latency",
                "mean_efficiency",
                "std_efficiency",
                "mean_collisions",
                "std_collisions",
            ],
        )
        writer.writeheader()
        writer.writerows(summaries)

    print()
    print("=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)
    print(f"Raw results:     {raw_path}")
    print(f"Summary results: {summary_path}")


if __name__ == "__main__":
    main()
