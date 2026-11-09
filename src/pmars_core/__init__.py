"""PMARS core: stationary hub and mobile collection robots."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


Position = tuple[int, int]


class RobotStatus(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"


class TaskStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    COLLECTING = "collecting"
    RETURNING = "returning"
    DELIVERED = "delivered"


@dataclass
class Item:
    item_id: str
    category: str
    position: Position
    collected: bool = False
    delivered: bool = False


@dataclass
class CollectionTask:
    task_id: str
    item: Item
    status: TaskStatus = TaskStatus.PENDING
    assigned_robot: Optional[str] = None


@dataclass
class MobileRobot:
    robot_id: str
    position: Position
    status: RobotStatus = RobotStatus.IDLE
    current_task: Optional[CollectionTask] = None
    carrying_item: Optional[Item] = None
    completed_tasks: int = 0

    def assign(self, task: CollectionTask) -> bool:
        if self.status != RobotStatus.IDLE:
            return False

        self.current_task = task
        self.status = RobotStatus.BUSY
        task.assigned_robot = self.robot_id
        task.status = TaskStatus.ASSIGNED
        return True

    def set_available(self, available: bool) -> None:
        self.status = (
            RobotStatus.IDLE if available else RobotStatus.UNAVAILABLE
        )

    def _move_toward(self, target: Position) -> None:
        x, y = self.position
        tx, ty = target

        if x != tx:
            x += 1 if tx > x else -1
        elif y != ty:
            y += 1 if ty > y else -1

        self.position = (x, y)

    def step(self, hub_position: Position) -> Optional[Item]:
        if self.status != RobotStatus.BUSY or self.current_task is None:
            return None

        task = self.current_task

        if self.carrying_item is None:
            task.status = TaskStatus.COLLECTING

            if self.position != task.item.position:
                self._move_toward(task.item.position)
                return None

            self.carrying_item = task.item
            task.item.collected = True
            task.status = TaskStatus.RETURNING
            return None

        if self.position != hub_position:
            self._move_toward(hub_position)
            return None

        delivered = self.carrying_item
        delivered.delivered = True

        task.status = TaskStatus.DELIVERED
        self.completed_tasks += 1
        self.carrying_item = None
        self.current_task = None
        self.status = RobotStatus.IDLE

        return delivered


@dataclass
class FleetManager:
    robots: dict[str, MobileRobot] = field(default_factory=dict)

    def register_robot(self, robot: MobileRobot) -> None:
        if robot.robot_id in self.robots:
            raise ValueError(f"Duplicate robot ID: {robot.robot_id}")
        self.robots[robot.robot_id] = robot

    def available_robots(self) -> list[MobileRobot]:
        return sorted(
            (
                robot for robot in self.robots.values()
                if robot.status == RobotStatus.IDLE
            ),
            key=lambda robot: robot.robot_id,
        )


@dataclass
class CentralHub:
    position: Position = (0, 0)
    fleet: FleetManager = field(default_factory=FleetManager)
    tasks: dict[str, CollectionTask] = field(default_factory=dict)
    delivered_items: list[Item] = field(default_factory=list)
    _next_task_number: int = 1

    def register_robot(self, robot: MobileRobot) -> None:
        self.fleet.register_robot(robot)

    def create_collection_task(self, item: Item) -> CollectionTask:
        task_id = f"T{self._next_task_number:04d}"
        self._next_task_number += 1

        task = CollectionTask(task_id=task_id, item=item)
        self.tasks[task_id] = task
        return task

    def dispatch(self) -> int:
        assigned = 0

        pending = sorted(
            (
                task for task in self.tasks.values()
                if task.status == TaskStatus.PENDING
            ),
            key=lambda task: task.task_id,
        )

        for task in pending:
            robots = self.fleet.available_robots()

            if not robots:
                break

            if robots[0].assign(task):
                assigned += 1

        return assigned

    def step(self) -> None:
        self.dispatch()

        for robot in sorted(
            self.fleet.robots.values(),
            key=lambda robot: robot.robot_id,
        ):
            delivered = robot.step(self.position)

            if delivered is not None:
                self.delivered_items.append(delivered)

        self.dispatch()

    def report(self) -> dict:
        return {
            "robots": len(self.fleet.robots),
            "idle_robots": sum(
                r.status == RobotStatus.IDLE
                for r in self.fleet.robots.values()
            ),
            "busy_robots": sum(
                r.status == RobotStatus.BUSY
                for r in self.fleet.robots.values()
            ),
            "unavailable_robots": sum(
                r.status == RobotStatus.UNAVAILABLE
                for r in self.fleet.robots.values()
            ),
            "total_tasks": len(self.tasks),
            "pending_tasks": sum(
                t.status == TaskStatus.PENDING
                for t in self.tasks.values()
            ),
            "delivered_tasks": sum(
                t.status == TaskStatus.DELIVERED
                for t in self.tasks.values()
            ),
            "delivered_items": len(self.delivered_items),
        }


class PMARSSimulation:
    def __init__(self, hub: Optional[CentralHub] = None):
        self.hub = hub or CentralHub()
        self.steps = 0

    def add_robot(self, robot_id: str, position: Position) -> MobileRobot:
        robot = MobileRobot(robot_id=robot_id, position=position)
        self.hub.register_robot(robot)
        return robot

    def add_item(
        self,
        item_id: str,
        category: str,
        position: Position,
    ) -> CollectionTask:
        item = Item(
            item_id=item_id,
            category=category,
            position=position,
        )
        return self.hub.create_collection_task(item)

    def step(self) -> None:
        self.hub.step()
        self.steps += 1

    def run(self, max_steps: int = 1000) -> dict:
        if max_steps < 0:
            raise ValueError("max_steps cannot be negative")

        for _ in range(max_steps):
            if all(
                task.status == TaskStatus.DELIVERED
                for task in self.hub.tasks.values()
            ):
                break

            self.step()

        return {
            "simulation_steps": self.steps,
            **self.hub.report(),
        }
