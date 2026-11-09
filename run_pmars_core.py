from src.pmars_core import PMARSSimulation

def main():
    simulation = PMARSSimulation()

    simulation.add_robot("R001", (2, 2))
    simulation.add_robot("R002", (5, 3))
    simulation.add_robot("R003", (3, 6))

    simulation.add_item("I001", "electronics", (10, 5))
    simulation.add_item("I002", "mechanical", (7, 8))
    simulation.add_item("I003", "medical", (12, 2))
    simulation.add_item("I004", "electronics", (4, 10))
    simulation.add_item("I005", "mechanical", (9, 9))

    results = simulation.run(max_steps=1000)

    print("\n========== PMARS CORE RESULTS ==========")

    for key, value in results.items():
        print(f"{key}: {value}")

    print("\n========== DELIVERY RECORD ==========")

    for item in simulation.hub.delivered_items:
        print(
            f"{item.item_id} | "
            f"{item.category} | "
            f"delivered={item.delivered}"
        )


if __name__ == "__main__":
    main()
