"""Run repeatable PMARS simulation trials and export raw observations."""
import csv
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.pmars_core.system import PMARSSystem, GridWorld


def run_trial(seed, item_count=12):
    rng = random.Random(seed)
    obstacles = {
        (8, y) for y in range(1, 18) if y not in (4, 9, 14)
    }
    world = GridWorld(24, 24, obstacles)
    system = PMARSSystem(world, (0, 0))

    robot_positions = [
        ((1, 1), (22, 1)),
        ((2, 1), (22, 22)),
        ((1, 2), (1, 22)),
        ((3, 1), (12, 22)),
    ]

    parking_positions = {parking for _, parking in robot_positions}

    for index, (position, parking) in enumerate(robot_positions, 1):
        system.add_robot(
            f"R{index:03d}",
            position,
            home_position=parking,
        )

    available = [
        (x, y)
        for x in range(2, 24)
        for y in range(2, 24)
        if (x, y) not in obstacles
        and (x, y) not in parking_positions
    ]
    rng.shuffle(available)

    categories = ["electronics", "mechanical", "medical"]
    for index in range(item_count):
        system.add_item(
            f"I{index + 1:03d}",
            categories[index % len(categories)],
            available[index],
            rng.randint(1, 3),
        )

    result = system.run(max_steps=10000)
    return {"seed": seed, "item_count": item_count, **result}


def main():
    output = Path("results/pmars_full")
    output.mkdir(parents=True, exist_ok=True)
    rows = [run_trial(seed) for seed in range(30)]

    columns = sorted({key for row in rows for key in row if key != "sorted_categories"})
    with (output / "trial_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: v for k, v in row.items() if k in columns})

    completed = sum(row["delivered_items"] for row in rows)
    requested = sum(row["total_items"] for row in rows)
    print(f"Trials: {len(rows)}")
    print(f"Items delivered: {completed}/{requested}")
    print(f"Aggregate completion rate: {completed / requested if requested else 1.0:.4f}")
    print(f"Raw results: {output / 'trial_results.csv'}")
    print("These are simulation results, not physical robot measurements.")


if __name__ == "__main__":
    main()
