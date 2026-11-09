"""Integrated PMARS simulation: central hub, autonomous fleet and item processing."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from heapq import heappop, heappush
from typing import Optional
import math


Position = tuple[int, int]


class RobotState(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"


class TaskState(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    COLLECTING = "collecting"
    RETURNING = "returning"
    DELIVERED = "delivered"
    BLOCKED = "blocked"


@dataclass
class Item:
    item_id: str
    category: str
    position: Position
    priority: int = 1
    collected: bool = False
    delivered: bool = False


@dataclass
class Task:
    task_id: str
    item: Item
    state: TaskState = TaskState.PENDING
    robot_id: Optional[str] = None


@dataclass
class Robot:
    robot_id: str
    position: Position
    home_position: Optional[Position] = None
    returning_home: bool = False
    state: RobotState = RobotState.IDLE
    task: Optional[Task] = None
    carrying: Optional[Item] = None
    health: float = 1.0
    completed: int = 0
    distance_travelled: int = 0


class GridWorld:
    """Four-connected grid with static obstacles and A* pathfinding."""

    def __init__(
        self,
        width: int = 20,
        height: int = 20,
        obstacles: Optional[set[Position]] = None,
    ):
        if width < 2 or height < 2:
            raise ValueError("World dimensions must be at least 2.")
        self.width = width
        self.height = height
        self.obstacles = set(obstacles or ())
        if any(not self.in_bounds(p) for p in self.obstacles):
            raise ValueError("An obstacle lies outside the world.")

    def in_bounds(self, p: Position) -> bool:
        x, y = p
        return 0 <= x < self.width and 0 <= y < self.height

    def traversable(self, p: Position) -> bool:
        return self.in_bounds(p) and p not in self.obstacles

    def neighbors(self, p: Position):
        x, y = p
        for candidate in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if self.traversable(candidate):
                yield candidate

    @staticmethod
    def heuristic(a: Position, b: Position) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(
        self,
        start: Position,
        goal: Position,
        blocked: Optional[set[Position]] = None,
    ) -> Optional[list[Position]]:
        blocked = set(blocked or ())
        if not self.traversable(start) or not self.traversable(goal):
            return None
        if goal in blocked:
            return None
        if start == goal:
            return [start]

        frontier = []
        heappush(frontier, (self.heuristic(start, goal), 0, start))
        came_from = {}
        cost = {start: 0}

        while frontier:
            _, current_cost, current = heappop(frontier)
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return list(reversed(path))

            if current_cost != cost[current]:
                continue

            for nxt in self.neighbors(current):
                if nxt in blocked:
                    continue
                new_cost = current_cost + 1
                if new_cost < cost.get(nxt, math.inf):
                    cost[nxt] = new_cost
                    came_from[nxt] = current
                    score = new_cost + self.heuristic(nxt, goal)
                    heappush(frontier, (score, new_cost, nxt))

        return None


class PMARSSystem:
    """Centralized task allocation with autonomous grid navigation."""

    def __init__(
        self,
        world: Optional[GridWorld] = None,
        hub_position: Position = (0, 0),
    ):
        self.world = world or GridWorld()
        if not self.world.traversable(hub_position):
            raise ValueError("Hub position must be traversable.")

        self.hub_position = hub_position
        self.robots: dict[str, Robot] = {}
        self.tasks: dict[str, Task] = {}
        self.delivered_items: list[Item] = []
        self.sorted_inventory: dict[str, list[Item]] = {}
        self.ticks = 0
        self.avoided_collisions = 0
        self.blocked_movements = 0
        self.replans = 0
        self._next_task = 1

    def add_robot(
        self,
        robot_id: str,
        position: Position,
        home_position: Optional[Position] = None,
    ) -> Robot:
        if robot_id in self.robots:
            raise ValueError(f"Duplicate robot ID: {robot_id}")
        if not self.world.traversable(position):
            raise ValueError("Robot position must be traversable.")
        if any(r.position == position for r in self.robots.values()):
            raise ValueError("Two robots cannot occupy the same cell.")

        parking = home_position if home_position is not None else position

        if not self.world.traversable(parking):
            raise ValueError("Robot parking position must be traversable.")
        if any(r.home_position == parking for r in self.robots.values()):
            raise ValueError("Two robots cannot share a parking position.")
        if any(r.position == parking for r in self.robots.values()):
            raise ValueError("Parking position is occupied by another robot.")

        robot = Robot(robot_id, position, home_position=parking)
        self.robots[robot_id] = robot
        return robot

    def add_item(
        self,
        item_id: str,
        category: str,
        position: Position,
        priority: int = 1,
    ) -> Task:
        if any(t.item.item_id == item_id for t in self.tasks.values()):
            raise ValueError(f"Duplicate item ID: {item_id}")
        if not category.strip():
            raise ValueError("Item category cannot be empty.")
        if priority < 1:
            raise ValueError("Priority must be at least 1.")
        if not self.world.traversable(position):
            raise ValueError("Item position must be traversable.")

        item = Item(item_id, category, position, priority)
        task = Task(f"T{self._next_task:05d}", item)
        self._next_task += 1
        self.tasks[task.task_id] = task
        return task

    def available_robots(self) -> list[Robot]:
        return sorted(
            (r for r in self.robots.values() if r.state == RobotState.IDLE),
            key=lambda r: r.robot_id,
        )

    def dispatch(self) -> int:
        assigned = 0
        pending = sorted(
            (t for t in self.tasks.values() if t.state == TaskState.PENDING),
            key=lambda t: (-t.item.priority, t.task_id),
        )

        for task in pending:
            idle_robots = self.available_robots()

            if not idle_robots:
                continue

            candidates = []
            for robot in idle_robots:
                path = self.world.find_path(robot.position, task.item.position)
                if path is not None:
                    candidates.append((len(path) - 1, robot.robot_id, robot))

            if not candidates:
                task.state = TaskState.BLOCKED
                continue

            _, _, robot = min(candidates, key=lambda x: (x[0], x[1]))
            robot.task = task
            robot.state = RobotState.BUSY
            task.robot_id = robot.robot_id
            task.state = TaskState.ASSIGNED
            assigned += 1

        return assigned

    def report_health(self, robot_id: str, health: float) -> None:
        if robot_id not in self.robots:
            raise ValueError(f"Unknown robot: {robot_id}")
        if not 0.0 <= health <= 1.0:
            raise ValueError("Health must be between 0 and 1.")
        self.robots[robot_id].health = health
        if health <= 0:
            self.fail_robot(robot_id)

    def fail_robot(self, robot_id: str) -> bool:
        robot = self.robots.get(robot_id)
        if robot is None:
            raise ValueError(f"Unknown robot: {robot_id}")
        if robot.state == RobotState.UNAVAILABLE:
            return False

        if robot.task is not None:
            task = robot.task
            if robot.carrying is not None:
                robot.carrying.position = robot.position
                robot.carrying.collected = False
                robot.carrying.delivered = False
            task.state = TaskState.PENDING
            task.robot_id = None

        robot.task = None
        robot.carrying = None
        robot.state = RobotState.UNAVAILABLE
        return True

    def restore_robot(self, robot_id: str) -> bool:
        robot = self.robots.get(robot_id)
        if robot is None:
            raise ValueError(f"Unknown robot: {robot_id}")
        if robot.state != RobotState.UNAVAILABLE:
            return False
        robot.health = 1.0
        robot.state = RobotState.IDLE
        return True

    def _deliver(self, robot: Robot) -> None:
        item = robot.carrying
        task = robot.task
        if item is None or task is None:
            return

        item.delivered = True
        task.state = TaskState.DELIVERED
        self.delivered_items.append(item)
        self.sorted_inventory.setdefault(item.category, []).append(item)

        robot.completed += 1
        robot.carrying = None
        robot.task = None
        robot.returning_home = True
        robot.state = RobotState.BUSY

    def step(self) -> None:
        self.dispatch()
        ordered = sorted(self.robots.values(), key=lambda r: r.robot_id)

        for robot in ordered:
            if robot.state != RobotState.BUSY:
                continue

            occupied = {
                other.position
                for other in self.robots.values()
                if other.robot_id != robot.robot_id
            }

            # Return delivered robots to their individual parking positions.
            if robot.task is None and robot.returning_home:
                home = robot.home_position

                if home is None or robot.position == home:
                    robot.returning_home = False
                    robot.state = RobotState.IDLE
                    continue

                path = self.world.find_path(
                    robot.position, home, blocked=occupied
                )

                if path is None or len(path) < 2:
                    self.replans += 1
                    self.blocked_movements += 1
                    continue

                robot.position = path[1]
                robot.distance_travelled += 1

                if robot.position == home:
                    robot.returning_home = False
                    robot.state = RobotState.IDLE
                continue

            if robot.task is None:
                continue

            task = robot.task
            target = (
                self.hub_position
                if robot.carrying is not None
                else task.item.position
            )

            path = self.world.find_path(
                robot.position, target, blocked=occupied
            )

            if path is None:
                self.replans += 1
                self.blocked_movements += 1
                continue

            if len(path) == 1:
                if robot.carrying is not None:
                    self._deliver(robot)
                else:
                    robot.carrying = task.item
                    task.item.collected = True
                    task.state = TaskState.RETURNING
                continue

            next_position = path[1]

            if next_position in occupied:
                self.avoided_collisions += 1
                self.blocked_movements += 1
                self.replans += 1
                continue

            robot.position = next_position
            robot.distance_travelled += 1

            if robot.carrying is None and robot.position == task.item.position:
                robot.carrying = task.item
                task.item.collected = True
                task.state = TaskState.RETURNING

            elif robot.carrying is not None and robot.position == self.hub_position:
                self._deliver(robot)

        self.ticks += 1
        self.dispatch()

    def run(self, max_steps: int = 5000) -> dict:
        if max_steps < 0:
            raise ValueError("max_steps cannot be negative.")

        for _ in range(max_steps):
            unfinished_tasks = any(
                t.state in (
                    TaskState.PENDING,
                    TaskState.ASSIGNED,
                    TaskState.COLLECTING,
                    TaskState.RETURNING,
                )
                for t in self.tasks.values()
            )

            robots_still_moving = any(
                r.state == RobotState.BUSY
                for r in self.robots.values()
            )

            if not unfinished_tasks and not robots_still_moving:
                break

            self.step()

        delivered = len(self.delivered_items)
        distances = sum(r.distance_travelled for r in self.robots.values())

        return {
            "simulation_steps": self.ticks,
            "robots": len(self.robots),
            "delivered_items": delivered,
            "total_items": len(self.tasks),
            "pending_tasks": sum(t.state == TaskState.PENDING for t in self.tasks.values()),
            "blocked_tasks": sum(t.state == TaskState.BLOCKED for t in self.tasks.values()),
            "busy_robots": sum(r.state == RobotState.BUSY for r in self.robots.values()),
            "unavailable_robots": sum(r.state == RobotState.UNAVAILABLE for r in self.robots.values()),
            "distance_travelled": distances,
            "avoided_collisions": self.avoided_collisions,
            "blocked_movements": self.blocked_movements,
            "path_replans": self.replans,
            "completion_rate": delivered / len(self.tasks) if self.tasks else 1.0,
            "sorted_categories": sorted(self.sorted_inventory),
        }

    def report(self) -> dict:
        return {
            "robots": {
                rid: {
                    "position": robot.position,
                    "state": robot.state.value,
                    "health": robot.health,
                    "completed": robot.completed,
                    "distance_travelled": robot.distance_travelled,
                }
                for rid, robot in sorted(self.robots.items())
            },
            "tasks": {
                tid: {
                    "item": task.item.item_id,
                    "state": task.state.value,
                    "assigned_robot": task.robot_id,
                }
                for tid, task in sorted(self.tasks.items())
            },
            "sorted_inventory": {
                category: [item.item_id for item in items]
                for category, items in sorted(self.sorted_inventory.items())
            },
        }
