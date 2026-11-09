import unittest

from src.pmars_core.system import (
    PMARSSystem, GridWorld, RobotState, TaskState
)


class TestPMARSFullSystem(unittest.TestCase):

    def test_astar_finds_path(self):
        world = GridWorld(8, 8, {(2, 0), (2, 1), (2, 2)})
        path = world.find_path((0, 0), (5, 0))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (5, 0))
        self.assertTrue(all(p not in world.obstacles for p in path))

    def test_unreachable_destination(self):
        world = GridWorld(5, 5, {(1, 0), (0, 1)})
        self.assertIsNone(world.find_path((0, 0), (4, 4)))

    def test_robot_cannot_start_on_obstacle(self):
        world = GridWorld(5, 5, {(1, 1)})
        system = PMARSSystem(world)
        with self.assertRaises(ValueError):
            system.add_robot("R1", (1, 1))

    def test_item_collection_and_delivery(self):
        system = PMARSSystem(GridWorld(10, 10))
        system.add_robot("R1", (1, 1))
        system.add_item("I1", "electronics", (4, 4))
        result = system.run()
        self.assertEqual(result["delivered_items"], 1)
        self.assertEqual(result["completion_rate"], 1.0)

    def test_items_are_sorted_by_category(self):
        system = PMARSSystem(GridWorld(12, 12))
        system.add_robot("R1", (1, 1))
        system.add_item("I1", "medical", (3, 3))
        system.add_item("I2", "electronics", (5, 5))
        system.run()
        self.assertEqual(set(system.sorted_inventory), {"medical", "electronics"})

    def test_priority_assignment(self):
        system = PMARSSystem(GridWorld(12, 12))
        system.add_robot("R1", (1, 1))
        low = system.add_item("LOW", "general", (2, 2), 1)
        high = system.add_item("HIGH", "urgent", (8, 8), 5)
        system.dispatch()
        self.assertEqual(high.robot_id, "R1")
        self.assertIsNone(low.robot_id)

    def test_failure_requeues_task(self):
        system = PMARSSystem(GridWorld(12, 12))
        system.add_robot("R1", (1, 1))
        system.add_robot("R2", (2, 1))
        task = system.add_item("I1", "general", (8, 8))
        system.dispatch()
        failed_robot = task.robot_id
        expected_replacement = "R1" if failed_robot == "R2" else "R2"
        system.fail_robot(failed_robot)
        system.dispatch()
        self.assertEqual(task.state, TaskState.ASSIGNED)
        self.assertEqual(task.robot_id, expected_replacement)

    def test_failure_while_carrying_recovers_item(self):
        system = PMARSSystem(GridWorld(10, 10))
        robot = system.add_robot("R1", (1, 1))
        task = system.add_item("I1", "general", (1, 1))
        system.dispatch()
        system.step()
        self.assertIsNotNone(robot.carrying)
        system.fail_robot("R1")
        self.assertFalse(task.item.collected)
        self.assertIsNone(robot.carrying)
        self.assertEqual(task.state, TaskState.PENDING)

    def test_health_monitoring_triggers_failure(self):
        system = PMARSSystem()
        robot = system.add_robot("R1", (1, 1))
        system.report_health("R1", 0)
        self.assertEqual(robot.state, RobotState.UNAVAILABLE)

    def test_robot_restoration(self):
        system = PMARSSystem()
        robot = system.add_robot("R1", (1, 1))
        system.fail_robot("R1")
        self.assertTrue(system.restore_robot("R1"))
        self.assertEqual(robot.state, RobotState.IDLE)

    def test_duplicate_robot_rejected(self):
        system = PMARSSystem()
        system.add_robot("R1", (1, 1))
        with self.assertRaises(ValueError):
            system.add_robot("R1", (2, 2))

    def test_duplicate_item_rejected(self):
        system = PMARSSystem()
        system.add_item("I1", "general", (2, 2))
        with self.assertRaises(ValueError):
            system.add_item("I1", "general", (3, 3))

    def test_collision_avoidance_does_not_overlap_robots(self):
        world = GridWorld(12, 12)
        system = PMARSSystem(world)
        system.add_robot("R1", (1, 1))
        system.add_robot("R2", (2, 1))
        system.add_item("I1", "general", (5, 5))
        system.add_item("I2", "general", (5, 6))
        system.run()
        positions = [r.position for r in system.robots.values()]
        self.assertEqual(len(positions), len(set(positions)))

    def test_run_waits_until_robot_returns_to_parking(self):
        system = PMARSSystem(GridWorld(12, 12))
        robot = system.add_robot(
            "R1",
            (1, 1),
            home_position=(10, 10),
        )
        system.add_item("I1", "electronics", (4, 4))

        result = system.run(max_steps=500)

        self.assertEqual(result["delivered_items"], 1)
        self.assertEqual(result["busy_robots"], 0)
        self.assertEqual(robot.position, (10, 10))
        self.assertFalse(robot.returning_home)

    def test_empty_system(self):
        result = PMARSSystem().run()
        self.assertEqual(result["completion_rate"], 1.0)
        self.assertEqual(result["delivered_items"], 0)


if __name__ == "__main__":
    unittest.main()
