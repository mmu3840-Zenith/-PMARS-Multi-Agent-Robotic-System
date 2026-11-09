import unittest

from src.pmars_core import (
    PMARSSimulation,
    MobileRobot,
    CentralHub,
    RobotStatus,
    TaskStatus,
    Item,
)


class TestPMARSCore(unittest.TestCase):

    def test_robot_registration(self):
        hub = CentralHub()
        hub.register_robot(MobileRobot("R001", (1, 1)))
        self.assertEqual(len(hub.fleet.robots), 1)

    def test_duplicate_robot_rejected(self):
        hub = CentralHub()
        hub.register_robot(MobileRobot("R001", (1, 1)))

        with self.assertRaises(ValueError):
            hub.register_robot(MobileRobot("R001", (2, 2)))

    def test_task_creation(self):
        hub = CentralHub()
        item = Item("I001", "electronics", (5, 5))
        task = hub.create_collection_task(item)

        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_robot_assignment(self):
        hub = CentralHub()
        robot = MobileRobot("R001", (1, 1))
        hub.register_robot(robot)

        task = hub.create_collection_task(
            Item("I001", "electronics", (3, 3))
        )

        self.assertEqual(hub.dispatch(), 1)
        self.assertEqual(robot.current_task, task)

    def test_unavailable_robot_not_assigned(self):
        hub = CentralHub()
        robot = MobileRobot("R001", (1, 1))
        robot.set_available(False)
        hub.register_robot(robot)

        hub.create_collection_task(
            Item("I001", "electronics", (3, 3))
        )

        self.assertEqual(hub.dispatch(), 0)

    def test_collection_and_delivery(self):
        simulation = PMARSSimulation()
        simulation.add_robot("R001", (1, 1))
        simulation.add_item("I001", "electronics", (4, 4))

        results = simulation.run(max_steps=100)

        self.assertEqual(results["delivered_items"], 1)
        self.assertEqual(results["pending_tasks"], 0)

    def test_multiple_robots_and_items(self):
        simulation = PMARSSimulation()

        simulation.add_robot("R001", (1, 1))
        simulation.add_robot("R002", (2, 2))

        simulation.add_item("I001", "electronics", (5, 5))
        simulation.add_item("I002", "mechanical", (7, 7))
        simulation.add_item("I003", "medical", (8, 3))

        results = simulation.run(max_steps=500)

        self.assertEqual(results["delivered_items"], 3)
        self.assertEqual(results["delivered_tasks"], 3)

    def test_delivery_record(self):
        simulation = PMARSSimulation()
        simulation.add_robot("R001", (1, 1))
        simulation.add_item("I001", "electronics", (2, 2))

        simulation.run(max_steps=100)

        item = simulation.hub.delivered_items[0]
        self.assertTrue(item.delivered)
        self.assertTrue(item.collected)

    def test_robot_returns_to_idle(self):
        simulation = PMARSSimulation()
        robot = simulation.add_robot("R001", (1, 1))
        simulation.add_item("I001", "electronics", (2, 2))

        simulation.run(max_steps=100)

        self.assertEqual(robot.status, RobotStatus.IDLE)
        self.assertEqual(robot.completed_tasks, 1)


if __name__ == "__main__":
    unittest.main()
