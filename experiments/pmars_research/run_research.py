"""PMARS reproducible research and benchmarking suite."""
from __future__ import annotations

import csv
import json
import math
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.pmars_core.system import (
    PMARSSystem, GridWorld, RobotState, TaskState
)


class AllocationSystem(PMARSSystem):
    """Research variants sharing the same navigation and simulation core."""

    def __init__(self, *args, strategy="pmars", seed=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.strategy = strategy
        self.rng = random.Random(seed)

    def dispatch(self):
        if self.strategy == "pmars":
            return super().dispatch()

        assigned = 0
        pending = sorted(
            (t for t in self.tasks.values() if t.state == TaskState.PENDING),
            key=lambda t: t.task_id,
        )

        for task in pending:
            idle = self.available_robots()
            candidates = []

            for robot in idle:
                path = self.world.find_path(robot.position, task.item.position)
                if path is not None:
                    candidates.append((len(path) - 1, robot.robot_id, robot))

            if not candidates:
                if idle:
                    task.state = TaskState.BLOCKED
                continue

            if self.strategy == "greedy":
                robot = min(candidates, key=lambda x: (x[0], x[1]))[2]
            elif self.strategy == "random":
                robot = self.rng.choice(candidates)[2]
            else:
                raise ValueError(f"Unknown strategy: {self.strategy}")

            robot.task = task
            robot.state = RobotState.BUSY
            task.robot_id = robot.robot_id
            task.state = TaskState.ASSIGNED
            assigned += 1

        return assigned


def make_scenario(seed, robot_count=4, item_count=12, size=24, strategy="pmars"):
    rng = random.Random(seed)
    obstacles = {
        (8, y) for y in range(1, min(18, size - 1))
        if y not in (4, 9, 14)
    } if size >= 20 else set()

    world = GridWorld(size, size, obstacles)
    system = AllocationSystem(
        world, (0, 0), strategy=strategy, seed=seed
    )

    starts = [(i + 1, 0) for i in range(robot_count)]
    homes = [(size - 1 - i, size - 1) for i in range(robot_count)]

    for i, (start, home) in enumerate(zip(starts, homes), 1):
        system.add_robot(f"R{i:03d}", start, home_position=home)

    reserved = set(starts) | set(homes) | {(0, 0)} | obstacles
    available = [
        (x, y)
        for x in range(2, size)
        for y in range(2, size)
        if (x, y) not in reserved
    ]
    rng.shuffle(available)

    if item_count > len(available):
        raise ValueError("Not enough available cells for requested items.")

    categories = ["electronics", "mechanical", "medical"]

    for i in range(item_count):
        system.add_item(
            f"I{i + 1:03d}",
            categories[i % len(categories)],
            available[i],
            rng.randint(1, 3),
        )

    return system


def finish(system, max_steps=10000):
    result = system.run(max_steps=max_steps)
    result["unfinished_tasks"] = sum(
        t.state in (
            TaskState.PENDING, TaskState.ASSIGNED,
            TaskState.COLLECTING, TaskState.RETURNING
        )
        for t in system.tasks.values()
    )
    result["robots_not_parked"] = sum(
        r.state == RobotState.BUSY for r in system.robots.values()
    )
    result["max_steps_reached"] = (
        result["simulation_steps"] >= max_steps
        and (result["unfinished_tasks"] > 0 or result["robots_not_parked"] > 0)
    )
    return result


def write_csv(path, rows):
    if not rows:
        return
    columns = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def summarize(values):
    values = [float(v) for v in values]
    n = len(values)
    mean = statistics.mean(values) if n else 0.0
    sd = statistics.stdev(values) if n > 1 else 0.0
    margin = 1.96 * sd / math.sqrt(n) if n > 1 else 0.0
    return {
        "n": n,
        "mean": mean,
        "standard_deviation": sd,
        "ci95_low": mean - margin,
        "ci95_high": mean + margin,
    }


def benchmark(output):
    rows = []

    for strategy in ("pmars", "greedy", "random"):
        for seed in range(30):
            system = make_scenario(
                seed, robot_count=4, item_count=12, strategy=strategy
            )
            result = finish(system)
            rows.append({
                "strategy": strategy,
                "seed": seed,
                "robots": 4,
                "items": 12,
                "delivered": result["delivered_items"],
                "completion_rate": result["completion_rate"],
                "distance": result["distance_travelled"],
                "steps": result["simulation_steps"],
                "blocked_movements": result["blocked_movements"],
                "unfinished_tasks": result["unfinished_tasks"],
                "robots_not_parked": result["robots_not_parked"],
                "max_steps_reached": result["max_steps_reached"],
            })

    write_csv(output / "benchmark_trials.csv", rows)

    summary = {}
    for strategy in ("pmars", "greedy", "random"):
        subset = [r for r in rows if r["strategy"] == strategy]
        summary[strategy] = {
            metric: summarize([r[metric] for r in subset])
            for metric in (
                "completion_rate", "distance", "steps",
                "blocked_movements"
            )
        }
        summary[strategy]["completed_trials"] = sum(
            not r["max_steps_reached"] and r["completion_rate"] == 1.0
            for r in subset
        )

    return rows, summary


def robustness(output):
    rows = []

    for seed in range(10):
        system = make_scenario(seed + 1000, 4, 12, strategy="pmars")

        for _ in range(8):
            system.step()

        failure_accepted = system.fail_robot("R001")

        for _ in range(5):
            system.step()

        restoration_accepted = system.restore_robot("R001")
        result = finish(system)

        rows.append({
            "seed": seed + 1000,
            "failure_triggered": failure_accepted,
            "robot_restored": restoration_accepted,
            "delivered": result["delivered_items"],
            "total_items": result["total_items"],
            "completion_rate": result["completion_rate"],
            "unfinished_tasks": result["unfinished_tasks"],
            "robots_not_parked": result["robots_not_parked"],
            "steps": result["simulation_steps"],
            "max_steps_reached": result["max_steps_reached"],
        })

    write_csv(output / "robustness_trials.csv", rows)
    return rows


def scalability(output):
    rows = []

    for robot_count in (1, 2, 4, 8):
        for item_count in (12, 24, 48):
            for seed in range(3):
                system = make_scenario(
                    2000 + seed,
                    robot_count=robot_count,
                    item_count=item_count,
                    size=40,
                    strategy="pmars",
                )
                result = finish(system)

                rows.append({
                    "seed": seed,
                    "robots": robot_count,
                    "items": item_count,
                    "delivered": result["delivered_items"],
                    "completion_rate": result["completion_rate"],
                    "distance": result["distance_travelled"],
                    "steps": result["simulation_steps"],
                    "blocked_movements": result["blocked_movements"],
                    "unfinished_tasks": result["unfinished_tasks"],
                    "robots_not_parked": result["robots_not_parked"],
                    "max_steps_reached": result["max_steps_reached"],
                })

    write_csv(output / "scalability_trials.csv", rows)
    return rows


def generate_report(output, benchmark_summary, robustness_rows, scale_rows):
    lines = [
        "# PMARS Research Release Report",
        "",
        "Automatically generated from the recorded simulation experiments.",
        "",
        "## Benchmark results",
        "",
        "| Strategy | Mean completion | Mean distance | Completed trials |",
        "|---|---:|---:|---:|",
    ]

    for name, data in benchmark_summary.items():
        lines.append(
            f"| {name} | {data['completion_rate']['mean']:.4f} "
            f"| {data['distance']['mean']:.2f} "
            f"| {data['completed_trials']}/30 |"
        )

    lines += [
        "",
        "### Confidence intervals",
        "",
        "The 95% intervals below use mean ± 1.96 × sample SD / square root of n.",
        "",
        "| Strategy | Metric | Mean | 95% interval |",
        "|---|---|---:|---:|",
    ]

    for name, data in benchmark_summary.items():
        for metric in ("completion_rate", "distance", "steps"):
            s = data[metric]
            lines.append(
                f"| {name} | {metric} | {s['mean']:.4f} "
                f"| [{s['ci95_low']:.4f}, {s['ci95_high']:.4f}] |"
            )

    robustness_success = sum(
        r["completion_rate"] == 1.0
        and not r["max_steps_reached"]
        and r["robots_not_parked"] == 0
        for r in robustness_rows
    )

    lines += [
        "",
        "## Robot failure and recovery",
        "",
        f"Completed recovery trials: {robustness_success}/{len(robustness_rows)}.",
        "The experiment injects one simulated robot failure and subsequently "
        "restores that robot. It does not model real radio hardware or network "
        "packet loss.",
        "",
        "## Scalability",
        "",
        "| Robots | Items | Trials | Mean completion | Mean steps |",
        "|---:|---:|---:|---:|---:|",
    ]

    for robots in (1, 2, 4, 8):
        for items in (12, 24, 48):
            group = [
                r for r in scale_rows
                if r["robots"] == robots and r["items"] == items
            ]
            lines.append(
                f"| {robots} | {items} | {len(group)} "
                f"| {statistics.mean(r['completion_rate'] for r in group):.4f} "
                f"| {statistics.mean(r['steps'] for r in group):.2f} |"
            )

    lines += [
        "",
        "## Interpretation and limitations",
        "",
        "- All observations are from a grid-based software simulation.",
        "- The benchmark strategies share the same navigation and movement model.",
        "- PMARS uses priority-ordered nearest-robot assignment.",
        "- Greedy uses task-ID order and nearest-robot assignment.",
        "- Random selects randomly among reachable idle robots.",
        "- The confidence intervals are descriptive, not proof of universal superiority.",
        "- Three seeds per scalability configuration are exploratory, not definitive.",
        "- Physical robots, cameras, real item recognition, and hardware communication "
        "have not been validated by these experiments.",
        "- Any incomplete trial remains in the exported data.",
        "",
        "## Reproducibility",
        "",
        "Seeds, per-trial observations, and aggregate summaries are saved alongside "
        "this report. Run `python experiments/pmars_research/run_research.py` "
        "to regenerate them.",
    ]

    (ROOT / "docs" / "PMARS_RESEARCH_RELEASE.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main():
    output = ROOT / "results" / "pmars_research"
    output.mkdir(parents=True, exist_ok=True)

    print("PMARS research benchmark: 3 strategies x 30 seeds")
    benchmark_rows, benchmark_summary = benchmark(output)

    print("PMARS robot failure and recovery: 10 trials")
    robustness_rows = robustness(output)

    print("PMARS scalability: 4 robot counts x 3 workload sizes x 3 seeds")
    scale_rows = scalability(output)

    payload = {
        "benchmark": benchmark_summary,
        "benchmark_trials": len(benchmark_rows),
        "robustness_trials": len(robustness_rows),
        "scalability_trials": len(scale_rows),
        "limitations": [
            "Software simulation only",
            "No physical robot validation",
            "No real camera-based recognition",
            "No real wireless communication model",
        ],
    }

    (output / "summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    generate_report(
        output, benchmark_summary, robustness_rows, scale_rows
    )

    print("\n========== PMARS RESEARCH RESULTS ==========")
    print(json.dumps(payload, indent=2))
    print("\nGenerated:")
    print(output)
    print(ROOT / "docs" / "PMARS_RESEARCH_RELEASE.md")


if __name__ == "__main__":
    main()

