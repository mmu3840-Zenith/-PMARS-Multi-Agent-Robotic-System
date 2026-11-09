from src.pmars_core.system import PMARSSystem, GridWorld


def main():
    obstacles = {
        (6, y) for y in range(1, 10) if y != 5
    }
    world = GridWorld(20, 20, obstacles)
    system = PMARSSystem(world, (0, 0))

    system.add_robot("R001", (2, 1), home_position=(18, 1))
    system.add_robot("R002", (1, 3), home_position=(18, 18))
    system.add_robot("R003", (3, 2), home_position=(1, 18))

    system.add_item("I001", "electronics", (12, 4), 3)
    system.add_item("I002", "mechanical", (10, 10), 2)
    system.add_item("I003", "medical", (15, 2), 5)
    system.add_item("I004", "electronics", (4, 12), 1)
    system.add_item("I005", "mechanical", (17, 15), 2)

    results = system.run(max_steps=5000)

    print("\n========== PMARS FULL SYSTEM ==========")
    for key, value in results.items():
        print(f"{key}: {value}")

    print("\n========== ROBOT AND TASK REPORT ==========")
    print(system.report())


if __name__ == "__main__":
    main()
